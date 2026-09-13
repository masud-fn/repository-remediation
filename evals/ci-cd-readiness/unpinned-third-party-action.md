# Case: unpinned-third-party-action

## Finding

```
FINDING_ID: CI-003
CATEGORY: ci-security
PROBLEM: The workflow uses a third-party action pinned to a mutable ref (`@main`), which lets the
  action's maintainer change what code runs in CI without any review on this repo's side.
EVIDENCE: .github/workflows/ci.yml line 30: `uses: some-org/coverage-action@main`.
EXPECTED_OUTCOME: The action is pinned to an immutable commit SHA.
SUGGESTED_FIX: Pin to the SHA corresponding to the currently intended release tag.
```

## Target repository setup

A repo whose CI workflow references `some-org/coverage-action@main` for a coverage-reporting step. No
other actions in the workflow are pinned to SHAs (they use version tags like `@v4`), giving a
convention to follow: tags are acceptable for well-known first-party actions (`actions/checkout@v4`),
but this specific action has no tagged releases — only a moving `main` branch.

## Expected behavior

- The skill identifies that `@main` is a mutable ref regardless of whether the org publishes tags, and
  that this specific action has no tags to fall back to.
- It resolves `main` to its current commit SHA and pins to that, adding a comment noting the resolved
  version for future updates (repository convention permitting).
- It does not change any other action references or the job's permissions.

## Acceptance criteria

- Only the `coverage-action` line changes, from `@main` to a full 40-character commit SHA.
- No `permissions:` changes; no other action pins altered.
- The report states which SHA was pinned and how it was resolved (e.g. "HEAD of main at time of fix").
- Final verdict: `CICD_REMEDIATION_COMPLETE=true`, `FINDINGS_FIXED=1`,
  `SECURITY_REGRESSION_DETECTED=false`.
