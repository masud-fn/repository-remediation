#!/usr/bin/env python3
"""Eval runner for skills — executes quality evals end-to-end and exits 0/1.

Reads a skill's evals/evals.json, injects the skill content (SKILL.md + all
reference files) into each eval prompt, runs each through the chosen provider,
grades assertions with DeepEval GEval, and exits with code 0 if the overall
pass rate meets the threshold, or 1 if it does not.

Usage (from skill-creator directory after `uv sync --extra <provider>`):
    uv run python -m scripts.run_quality_evals \\
        --skill-path plugins/fn-software-engineering/skills/fn-api-design \\
        --provider claude \\
        --fail-under 0.8

    uv run python -m scripts.run_quality_evals \\
        --skill-path plugins/fn-software-engineering/skills/fn-api-design \\
        --provider bedrock --region us-east-1

    uv run python -m scripts.run_quality_evals \\
        --skill-path plugins/fn-software-engineering/skills/fn-api-design \\
        --provider copilot --eval-ids 1,2,3

    uv run python -m scripts.run_quality_evals \\
        --skill-path plugins/fn-software-engineering/skills/fn-api-design \\
        --provider claude \\
        --grader-model claude-opus-4-8

Providers:
    claude   — claude -p CLI (local, no API key needed)
    copilot  — GitHub Models via LiteLLM (requires GITHUB_TOKEN)
    bedrock  — AWS Bedrock via IAM (requires AWS_BEDROCK_REGION)
"""

import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from scripts.deepeval_providers import get_model
from scripts.run_deepeval import _grade_expectations

_REF_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml"}


def _load_skill_context(skill_path: Path) -> str:
    """Load SKILL.md and all files in references/ into a single context block."""
    skill_md = (skill_path / "SKILL.md").read_text(errors="replace")
    parts = [f"<skill_instructions>\n{skill_md}\n</skill_instructions>"]

    refs_dir = skill_path / "references"
    if refs_dir.exists():
        for ref_file in sorted(refs_dir.iterdir()):
            if ref_file.is_file() and ref_file.suffix.lower() in _REF_SUFFIXES:
                content = ref_file.read_text(errors="replace")
                parts.append(
                    f'<reference name="{ref_file.name}">\n{content}\n</reference>'
                )

    return "\n\n".join(parts)


def _run_single_eval(
    model,
    grader_model,
    skill_context: str,
    eval_case: dict,
    verbose: bool,
) -> dict:
    """Execute one eval prompt through the skill and grade its assertions."""
    eval_id = eval_case["id"]
    prompt = eval_case["prompt"]
    assertions = eval_case.get("assertions") or []

    full_prompt = f"{skill_context}\n\nNow complete this task:\n{prompt}"

    if verbose:
        print(f"  [eval {eval_id:>2}] executing...", file=sys.stderr)

    exec_start = time.time()
    transcript, _ = model.generate(full_prompt)
    exec_seconds = round(time.time() - exec_start, 1)

    if verbose:
        print(
            f"  [eval {eval_id:>2}] done in {exec_seconds}s, "
            f"grading {len(assertions)} assertions...",
            file=sys.stderr,
        )

    graded = _grade_expectations(
        expectations=assertions,
        eval_prompt=prompt,
        transcript=transcript,
        output_content="",
        provider_model=grader_model,
        verbose=verbose,
    )

    passed = sum(1 for r in graded if r["passed"])
    total = len(graded)

    return {
        "eval_id": eval_id,
        "passed": passed,
        "total": total,
        "pass_rate": round(passed / total, 2) if total else 0.0,
        "exec_seconds": exec_seconds,
        "assertions": graded,
    }


def main():
    parser = argparse.ArgumentParser(
        description="CI eval runner: execute skill evals end-to-end and exit 0/1"
    )
    parser.add_argument(
        "--skill-path",
        required=True,
        help="Path to skill directory (must contain SKILL.md and evals/evals.json)",
    )
    parser.add_argument(
        "--provider",
        required=True,
        choices=["claude", "bedrock", "copilot"],
        help="LLM provider for skill execution",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override model ID for skill execution (claude: passes --model to CLI; others: API model ID)",
    )
    parser.add_argument(
        "--grader-model",
        default=None,
        help="Override model ID for grading assertions (default: same as --model)",
    )
    parser.add_argument(
        "--region",
        default=None,
        help="AWS region (bedrock only; falls back to AWS_BEDROCK_REGION env var)",
    )
    parser.add_argument(
        "--fail-under",
        type=float,
        default=0.8,
        metavar="RATE",
        help="Minimum overall pass rate (0–1) to exit 0 (default: 0.8)",
    )
    parser.add_argument(
        "--eval-ids",
        default=None,
        help="Comma-separated eval IDs to run; omit to run all",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=4,
        help="Number of parallel eval workers (default: 4)",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="PATH",
        help="Write full results JSON to this path in addition to stdout",
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    skill_path = Path(args.skill_path)
    evals_path = skill_path / "evals" / "evals.json"

    if not evals_path.exists():
        print(f"Error: evals.json not found at {evals_path}", file=sys.stderr)
        sys.exit(2)

    evals_data = json.loads(evals_path.read_text())
    evals = evals_data["evals"]

    if args.eval_ids:
        requested = {int(x.strip()) for x in args.eval_ids.split(",")}
        evals = [e for e in evals if e["id"] in requested]
        if not evals:
            print(f"Error: no evals matched IDs {requested}", file=sys.stderr)
            sys.exit(2)

    skill_name = evals_data.get("skill_name", skill_path.name)
    skill_context = _load_skill_context(skill_path)
    model = get_model(args.provider, model=args.model, region=args.region)
    grader_model = (
        get_model(args.provider, model=args.grader_model, region=args.region)
        if args.grader_model
        else model
    )
    if args.grader_model:
        print(
            f"Grading with {args.grader_model} "
            f"(execution with {args.model or 'default'})",
            file=sys.stderr,
        )

    print(
        f"Running {len(evals)} evals for '{skill_name}' via {args.provider} "
        f"(threshold: {args.fail_under:.0%}, workers: {args.workers})...",
        file=sys.stderr,
    )

    results = []
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {
            executor.submit(_run_single_eval, model, grader_model, skill_context, e, args.verbose): e
            for e in evals
        }
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as exc:
                eval_case = futures[future]
                print(
                    f"  [eval {eval_case['id']:>2}] ERROR: {exc}", file=sys.stderr
                )
                result = {
                    "eval_id": eval_case["id"],
                    "passed": 0,
                    "total": len(eval_case.get("assertions") or []),
                    "pass_rate": 0.0,
                    "exec_seconds": 0.0,
                    "error": str(exc),
                    "assertions": [],
                }
            results.append(result)
            status = "PASS" if result["passed"] == result["total"] else "FAIL"
            print(
                f"  [{status}] eval {result['eval_id']:>2}: "
                f"{result['passed']}/{result['total']} "
                f"({result['pass_rate']:.0%})",
                file=sys.stderr,
            )

    results.sort(key=lambda r: r["eval_id"])

    total_passed = sum(r["passed"] for r in results)
    total_assertions = sum(r["total"] for r in results)
    overall_rate = (
        round(total_passed / total_assertions, 2) if total_assertions else 0.0
    )
    passed_threshold = overall_rate >= args.fail_under

    summary = {
        "skill": skill_name,
        "provider": args.provider,
        "grader_model": args.grader_model,
        "evals_run": len(results),
        "overall_pass_rate": overall_rate,
        "total_passed": total_passed,
        "total_assertions": total_assertions,
        "threshold": args.fail_under,
        "passed_threshold": passed_threshold,
        "evals": results,
    }

    print(json.dumps(summary, indent=2))

    if args.output:
        Path(args.output).write_text(json.dumps(summary, indent=2))
        if args.verbose:
            print(f"Results written to {args.output}", file=sys.stderr)

    verdict = "PASSED" if passed_threshold else "FAILED"
    print(
        f"\n{verdict}: {overall_rate:.0%} overall "
        f"({'≥' if passed_threshold else '<'} threshold {args.fail_under:.0%})",
        file=sys.stderr,
    )

    sys.exit(0 if passed_threshold else 1)


if __name__ == "__main__":
    main()
