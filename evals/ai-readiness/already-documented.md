# Case: already-documented

## Finding

```
FINDING_ID: AI-004
CATEGORY: instruction-correctness
PROBLEM: There is no documented way for an agent to discover the project's lint command.
EVIDENCE: Agent attempted to run `npm run lint` and it failed with "missing script: lint".
EXPECTED_OUTCOME: The lint command is discoverable and executable.
SUGGESTED_FIX: Add a lint command section to CLAUDE.md.
```

## Target repository setup

A repo where CLAUDE.md already documents `npm run check:lint` as the canonical lint command (added in
a recent commit), and it works. The finding's evidence (`npm run lint` failing) reflects an agent
guessing an unlisted script name rather than reading CLAUDE.md.

## Expected behavior

- The skill checks CLAUDE.md first and finds the lint command is already documented and functional
  under a different, correct name.
- It recognizes this as `ALREADY_RESOLVED` — the actual gap was the earlier agent not reading the doc,
  not a genuine documentation gap — and makes no changes.
- It does not add a duplicate or conflicting lint section.

## Acceptance criteria

- No files are modified.
- The report shows the skill executed `npm run check:lint` successfully as verification before
  concluding.
- Finding is reported as `ALREADY_RESOLVED` with the existing CLAUDE.md section cited as evidence.
- Final verdict: `AI_READINESS_COMPLETE=true`, `VALIDATION_DISCOVERABLE=true`,
  `HUMAN_DECISIONS_REQUIRED=0`.
