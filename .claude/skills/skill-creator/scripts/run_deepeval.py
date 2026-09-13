#!/usr/bin/env python3
"""Grade a skill eval run using DeepEval's GEval metric.

Reads a run directory, evaluates each assertion from eval_metadata.json against
the transcript and output files using GEval (LLM-as-a-judge), and writes
grading.json in the exact schema the eval-viewer expects.

Usage (from skill-creator directory after `uv sync --extra <provider>`):
  uv run python -m scripts.run_deepeval \\
    --eval-dir workspace/iteration-1/eval-0/with_skill/run-1 \\
    --eval-metadata workspace/iteration-1/eval-0/eval_metadata.json \\
    --provider claude

  uv run python -m scripts.run_deepeval \\
    --eval-dir ... --eval-metadata ... \\
    --provider bedrock --region us-east-1

  uv run python -m scripts.run_deepeval \\
    --eval-dir ... --eval-metadata ... \\
    --provider copilot --grader-model gpt-4o
"""

import argparse
import json
import sys
import time
from pathlib import Path

from scripts.deepeval_providers import get_model

_TEXT_SUFFIXES = {
    ".txt", ".md", ".json", ".csv", ".html", ".xml",
    ".py", ".js", ".ts", ".sh", ".yaml", ".yml", ".toml",
}

# Per-section character cap passed to the judge LLM. Keeps the concatenated
# actual_output well within model context limits (80K chars ≈ 20K tokens).
_MAX_SECTION_CHARS = 40_000

# Number of extra retry attempts after the first GEval failure, to survive
# transient rate-limits or network hiccups.
_MAX_RETRIES = 2


def _truncate(text: str, limit: int, label: str) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n\n[... {label} truncated at {limit} chars ...]"


def _read_outputs(outputs_dir: Path) -> str:
    """Concatenate all readable output files into one string for GEval."""
    if not outputs_dir.exists():
        return ""
    parts = []
    for f in sorted(outputs_dir.iterdir()):
        if f.name == "metrics.json":
            continue
        if f.suffix.lower() in _TEXT_SUFFIXES:
            try:
                parts.append(f"=== {f.name} ===\n{f.read_text(errors='replace')}")
            except OSError:
                pass
    return "\n\n".join(parts)


def _read_user_notes(outputs_dir: Path) -> dict:
    """Read user_notes.md written by the executor and surface it as uncertainties."""
    notes_path = outputs_dir / "user_notes.md"
    result: dict = {"uncertainties": [], "needs_review": [], "workarounds": []}
    if not notes_path.exists():
        return result
    text = notes_path.read_text(errors="replace").strip()
    if text:
        result["uncertainties"].append(text)
    return result


def _grade_expectations(
    expectations: list[str],
    eval_prompt: str,
    transcript: str,
    output_content: str,
    provider_model,
    verbose: bool = False,
) -> list[dict]:
    """Run one GEval call per expectation and return graded results."""
    from deepeval.metrics import GEval
    from deepeval.test_case import LLMTestCase, SingleTurnParams

    # Truncate each section independently so a single large file can't blow the
    # judge's context window and cause every expectation to record as an error.
    actual_output = (
        f"TRANSCRIPT:\n{_truncate(transcript, _MAX_SECTION_CHARS, 'transcript')}"
        f"\n\nOUTPUT FILES:\n{_truncate(output_content, _MAX_SECTION_CHARS, 'outputs')}"
    )
    results = []

    for expectation in expectations:
        if verbose:
            print(f"  Grading: {expectation[:80]}", file=sys.stderr)

        metric = GEval(
            name=expectation[:60],
            criteria=(
                "Determine whether the following expectation is satisfied by the "
                f"transcript and output files. Expectation: {expectation}"
            ),
            evaluation_params=[SingleTurnParams.ACTUAL_OUTPUT],
            model=provider_model,
            threshold=0.5,
        )
        test_case = LLMTestCase(
            input=eval_prompt,
            actual_output=actual_output,
        )

        passed = False
        evidence = ""
        for attempt in range(_MAX_RETRIES + 1):
            try:
                metric.measure(test_case)
                passed = metric.is_successful()
                evidence = metric.reason or (
                    "Passed based on evaluation." if passed else "Failed based on evaluation."
                )
                break
            except Exception as exc:
                if attempt < _MAX_RETRIES:
                    delay = 2 ** attempt
                    print(
                        f"  Warning: GEval attempt {attempt + 1} failed ({exc}), "
                        f"retrying in {delay}s...",
                        file=sys.stderr,
                    )
                    time.sleep(delay)
                else:
                    evidence = f"GEval error (not a quality failure): {exc}"
                    print(
                        f"  Warning: GEval failed after {_MAX_RETRIES + 1} attempts: {exc}",
                        file=sys.stderr,
                    )

        if verbose:
            status = "PASS" if passed else "FAIL"
            print(f"    [{status}] {evidence[:120]}", file=sys.stderr)

        results.append({"text": expectation, "passed": passed, "evidence": evidence})

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Grade an eval run with DeepEval (drop-in for grader subagent)"
    )
    parser.add_argument(
        "--eval-dir",
        required=True,
        help="Path to run dir, e.g. iteration-1/eval-0/with_skill/run-1",
    )
    parser.add_argument(
        "--eval-metadata",
        required=True,
        help="Path to eval_metadata.json for this eval",
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=["claude", "bedrock", "copilot"],
        help="LLM provider to use as the judge",
    )
    parser.add_argument(
        "--grader-model",
        default=None,
        help="Override model ID for the judge (uses provider default if omitted)",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="AWS region (bedrock only; falls back to AWS_BEDROCK_REGION env var)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print per-assertion progress to stderr",
    )
    args = parser.parse_args()

    eval_dir = Path(args.eval_dir)
    outputs_dir = eval_dir / "outputs"
    transcript_path = eval_dir / "transcript.md"
    grading_path = eval_dir / "grading.json"

    # Load eval metadata (prompt + assertions)
    metadata = json.loads(Path(args.eval_metadata).read_text())
    eval_prompt = metadata.get("prompt", "")
    # Use `or []` to handle both missing key and explicit null value.
    expectations: list[str] = metadata.get("assertions") or []
    if not expectations:
        print("Warning: no assertions found in eval_metadata.json", file=sys.stderr)

    # Read transcript and output files
    transcript = (
        transcript_path.read_text(errors="replace") if transcript_path.exists() else ""
    )
    output_content = _read_outputs(outputs_dir)

    # Pull in timing and metrics written by the executor (if present)
    timing_data: dict = {}
    timing_path = eval_dir / "timing.json"
    if timing_path.exists():
        try:
            timing_data = json.loads(timing_path.read_text())
        except Exception:
            pass

    metrics_data: dict | None = None
    metrics_path = outputs_dir / "metrics.json"
    if metrics_path.exists():
        try:
            metrics_data = json.loads(metrics_path.read_text())
        except Exception:
            pass

    # Read executor notes before grading so they surface in the benchmark viewer.
    user_notes_summary = _read_user_notes(outputs_dir)

    # Instantiate the grader model
    if args.verbose:
        print(f"Provider: {args.provider}" + (f" ({args.grader_model})" if args.grader_model else ""), file=sys.stderr)
    provider_model = get_model(args.provider, model=args.grader_model, region=args.region)

    # Grade each expectation
    grader_start = time.time()
    graded = _grade_expectations(
        expectations=expectations,
        eval_prompt=eval_prompt,
        transcript=transcript,
        output_content=output_content,
        provider_model=provider_model,
        verbose=args.verbose,
    )
    grader_duration = round(time.time() - grader_start, 1)

    passed_count = sum(1 for r in graded if r["passed"])
    total_count = len(graded)

    # Build timing section using executor data when available
    timing: dict = {"grader_duration_seconds": grader_duration}
    if "executor_duration_seconds" in timing_data:
        timing["executor_duration_seconds"] = timing_data["executor_duration_seconds"]
    executor_elapsed = timing_data.get("total_duration_seconds", 0)
    timing["total_duration_seconds"] = round(executor_elapsed + grader_duration, 1)

    grading: dict = {
        "expectations": graded,
        "summary": {
            "passed": passed_count,
            "failed": total_count - passed_count,
            "total": total_count,
            "pass_rate": round(passed_count / total_count, 2) if total_count else 0.0,
        },
        "timing": timing,
        "claims": [],
        "user_notes_summary": user_notes_summary,
        "eval_feedback": {
            "suggestions": [],
            "overall": "Graded automatically via DeepEval GEval. Implicit claim extraction and eval critique were not performed.",
        },
    }
    if metrics_data is not None:
        grading["execution_metrics"] = metrics_data

    grading_path.write_text(json.dumps(grading, indent=2))

    if args.verbose:
        print(
            f"Done: {passed_count}/{total_count} passed. Written to {grading_path}",
            file=sys.stderr,
        )

    print(json.dumps(grading, indent=2))


if __name__ == "__main__":
    main()
