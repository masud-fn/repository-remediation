#!/usr/bin/env python3
"""Validate the repository-remediation skill package without third-party dependencies."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
UI = ROOT / "agents" / "openai.yaml"
CI_CD_REFERENCE = ROOT / "references" / "ci-cd-readiness.md"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if not SKILL.is_file():
        fail("SKILL.md is missing")
    if not UI.is_file():
        fail("agents/openai.yaml is missing")
    if not CI_CD_REFERENCE.is_file():
        fail("references/ci-cd-readiness.md is missing")

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        fail("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end == -1:
        fail("SKILL.md has no closing frontmatter delimiter")

    frontmatter = text[4:end]
    body = text[end + 5 :]
    required_frontmatter = ("name:", "description:")
    for field in required_frontmatter:
        if not any(line.startswith(field) for line in frontmatter.splitlines()):
            fail(f"SKILL.md frontmatter is missing {field}")

    name = next(line.split(":", 1)[1].strip() for line in frontmatter.splitlines() if line.startswith("name:"))
    if name != "repository-remediation":
        fail(f"unexpected skill name: {name}")
    if "[TODO" in text:
        fail("SKILL.md contains unfinished TODO content")

    required_sections = (
        "## Operating workflow",
        "## Area-specific rules",
        "## Validation and failure handling",
        "## Required report",
        "REMEDIATION_COMPLETE=",
    )
    for section in required_sections:
        if section not in body:
            fail(f"SKILL.md is missing required guidance: {section}")

    ui_text = UI.read_text(encoding="utf-8")
    for field in ("display_name:", "short_description:", "default_prompt:"):
        if field not in ui_text:
            fail(f"agents/openai.yaml is missing {field}")

    print("PASS: repository-remediation skill structure is valid")


if __name__ == "__main__":
    main()
