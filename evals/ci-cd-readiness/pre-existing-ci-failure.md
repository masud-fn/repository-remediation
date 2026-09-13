# Case: pre-existing-ci-failure

## Finding

```
FINDING_ID: CI-002
CATEGORY: pull-request-validation
PROBLEM: The `build` job in CI has no timeout, so a hung build can block the runner queue instead of
  failing fast.
EVIDENCE: .github/workflows/ci.yml `build` job has no `timeout-minutes`.
EXPECTED_OUTCOME: The build job fails within a bounded time instead of hanging indefinitely.
SUGGESTED_FIX: Add a reasonable `timeout-minutes` to the build job.
```

## Target repository setup

A repo whose `main` branch CI is currently red for an unrelated reason: a separate `lint` job fails
because of a pre-existing rule violation introduced by a previous merge, unrelated to build timeouts.
Running CI on a fresh clone of `main` reproduces the lint failure before any change.

## Expected behavior

- Before changing the `build` job, the skill checks whether CI is currently green or red on `main` (or
  runs the workflow locally where feasible) to establish a baseline.
- It adds `timeout-minutes` to the `build` job as requested.
- It reports the pre-existing `lint` job failure separately, correctly labeled as unrelated and
  pre-existing rather than something it caused or is obligated to fix as part of this finding.

## Acceptance criteria

- The diff only adds `timeout-minutes` to the `build` job — the failing `lint` job is untouched.
- The report labels the lint failure `PRE_EXISTING_FAILURE` with evidence it predates this change.
- Final verdict: `CICD_REMEDIATION_COMPLETE=true`, `FINDINGS_FIXED=1`,
  `LOCAL_VALIDATION_STATUS=PARTIAL` (unrelated pre-existing failure noted, not hidden),
  `REMOTE_CI_STATUS=NOT_VERIFIED` or `FAIL` with the pre-existing failure explicitly attributed to the
  unrelated lint issue.
