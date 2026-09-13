# Case: stale-command-reference

## Finding

```
FINDING_ID: AI-001
CATEGORY: instruction-correctness
PROBLEM: CLAUDE.md tells agents to run `npm run test` to validate changes, but the repo migrated to
  pnpm and the script no longer exists under that name.
EVIDENCE: CLAUDE.md line 12: "Run `npm run test` before committing."; package.json has no npm
  lockfile, only pnpm-lock.yaml, and the script is `pnpm test`.
EXPECTED_OUTCOME: The documented validation command actually executes successfully.
SUGGESTED_FIX: Update CLAUDE.md to `pnpm test`.
```

## Target repository setup

A repo that migrated from npm to pnpm several months ago (pnpm-lock.yaml present, no
package-lock.json). CLAUDE.md still says `npm run test` and `npm run build`. `pnpm test` and
`pnpm build` both work.

## Expected behavior

- The skill actually executes the documented command (or determines from the lockfile/scripts which
  package manager is canonical) rather than trusting the finding's wording alone.
- It corrects every stale package-manager reference in CLAUDE.md consistently (test, build, install),
  not just the one cited in the finding.
- It does not touch unrelated guidance in the file.

## Acceptance criteria

- All `npm ...` command references in CLAUDE.md are updated to `pnpm ...` equivalents; no new
  contradictions are introduced elsewhere in the file.
- The skill's report shows it ran `pnpm test` (and any other corrected command) successfully after the
  edit.
- This is classified `SAFE_AUTOFIX`.
- Final verdict: `AI_READINESS_COMPLETE=true`, `INVALID_COMMANDS_REMAINING=0`,
  `SETUP_DISCOVERABLE=true`, `VALIDATION_DISCOVERABLE=true`, `HUMAN_DECISIONS_REQUIRED=0`.
