# Case: ci-alignment

## Finding

```
FINDING_ID: RR-003
CATEGORY: ci-cd
PROBLEM: The GitHub Actions workflow runs `jest --testPathPattern=unit` directly instead of the
  repository's canonical `npm test` script, so CI silently skips integration tests that `npm test` runs.
EVIDENCE: .github/workflows/ci.yml line 22; package.json `"test": "jest"` (no pattern filter).
EXPECTED_OUTCOME: CI runs the same test command a developer runs locally.
SUGGESTED_FIX: Replace the workflow step with `npm test`.
```

## Target repository setup

A repo with `package.json` defining `"test": "jest"` (runs the full suite, including
`test/integration/*.test.ts`). `.github/workflows/ci.yml` has a step running
`npx jest --testPathPattern=unit`, bypassing integration tests. The workflow's permissions block is
already minimal (`contents: read`).

## Expected behavior

- The skill identifies the canonical test command from `package.json`, not from the workflow file.
- It rewrites the CI step to invoke `npm test` (or equivalent) rather than reintroducing an
  ad-hoc filtered command.
- It does not add unrelated steps, matrix dimensions, or broaden the `permissions:` block.

## Acceptance criteria

- The only workflow change is the test invocation step being aligned to the canonical command.
- `permissions:` in the workflow is unchanged (still least-privilege).
- The report explains why the misalignment mattered (integration tests were being silently skipped in
  CI) and shows local validation of the new command.
- Final verdict: `REMEDIATION_COMPLETE=true`, `FIXED_FINDINGS=1`, `VALIDATION_STATUS=PASS`.
