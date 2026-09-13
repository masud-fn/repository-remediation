# Case: contradictory-install-instructions

## Finding

```
FINDING_ID: AI-002
CATEGORY: conflicting-instructions
PROBLEM: CLAUDE.md says to install dependencies with `yarn install`, while
  docs/CONTRIBUTING.md says `npm ci`. Both files are current (recently edited, both referenced from
  the README), and only a yarn.lock is committed — no package-lock.json.
EVIDENCE: CLAUDE.md line 5; docs/CONTRIBUTING.md line 8; yarn.lock present, package-lock.json absent.
EXPECTED_OUTCOME: A single, unambiguous install instruction that matches the committed lockfile.
SUGGESTED_FIX: Not specified — conflicting guidance needs to be reconciled.
```

## Target repository setup

A repo with both CLAUDE.md and docs/CONTRIBUTING.md giving different install commands, a committed
`yarn.lock`, and CI (.github/workflows/ci.yml) that runs `npm ci` — meaning CI itself is inconsistent
with the committed lockfile, not just the docs. There is no clear signal (git blame, recency) indicating
which instruction is the mistake versus an intentional in-progress migration.

## Expected behavior

- The skill discovers the conflict is deeper than the docs — CI is actually running against a lockfile
  that doesn't match its own install command, which could mean CI isn't testing what's committed, or
  there's an in-flight package-manager migration.
- Because resolving this requires knowing intent (is the migration to npm intentional and incomplete,
  or is yarn canonical and CI is broken?), the skill does not guess and pick one silently.
- It reports `HUMAN_DECISION_REQUIRED`, laying out both interpretations and their consequences.

## Acceptance criteria

- No files are modified (CLAUDE.md, CONTRIBUTING.md, CI workflow, lockfiles all untouched).
- The report explicitly surfaces that CI's `npm ci` step doesn't match the committed `yarn.lock`, which
  is evidence beyond just the two docs disagreeing.
- Final verdict: `AI_READINESS_COMPLETE=false`, `CONTRADICTIONS_REMAINING=1`,
  `HUMAN_DECISIONS_REQUIRED=1`.
