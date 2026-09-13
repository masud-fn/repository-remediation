"""Shared utilities for skill-creator scripts."""

import os
import re
import yaml


def parse_frontmatter(content: str) -> dict:
    """Extract and parse the YAML frontmatter block from a SKILL.md's raw text."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md missing frontmatter (no opening/closing ---)")

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in SKILL.md frontmatter: {e}") from e

    if not isinstance(frontmatter, dict):
        raise ValueError("SKILL.md frontmatter must be a YAML dictionary")

    return frontmatter


def claude_subprocess_env() -> dict:
    """Environment for shelling out to `claude -p`, with CLAUDECODE removed.

    The guard is for interactive terminal conflicts when nesting `claude -p`
    inside a Claude Code session; programmatic subprocess usage is safe.
    """
    return {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
