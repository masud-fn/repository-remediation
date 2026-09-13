# Case: ci-local-parity

## Finding

```
FINDING_ID: CI-001
CATEGORY: local-ci-parity
PROBLEM: CI installs dependencies with `npm install` while the repo's committed lockfile and
  documented local workflow use `npm ci`, so CI can silently resolve different dependency versions
  than what's committed.
EVIDENCE: .github/workflows/ci.yml line 15: `run: npm install`; package-lock.json is committed;
  CLAUDE.md says to run `npm ci` locally.
EXPECTED_OUTCOME: CI installs from the exact committed lockfile, matching local development.
SUGGESTED_FIX: Replace `npm install` with `npm ci` in the workflow.
```

## Target repository setup

A Node repo with a committed `package-lock.json`, CLAUDE.md documenting `npm ci` as the canonical
install step, and `.github/workflows/ci.yml` using `npm install`. The workflow's `permissions:` block is
already `contents: read`.

## Expected behavior

- The skill confirms `npm ci` is the documented and lockfile-compatible canonical command before
  changing anything.
- It updates only the install step in the workflow.
- It does not add caching, matrix builds, or other unrelated CI improvements while it's in the file.

## Acceptance criteria

- The only workflow change is `npm install` → `npm ci`.
- `permissions:` is unchanged.
- The report shows the workflow change validated (e.g. via `act`, a dry run, or reasoning about
  `npm ci`'s behavior with the existing lockfile) — not merely asserted.
- Final verdict: `CICD_REMEDIATION_COMPLETE=true`, `FINDINGS_FIXED=1`,
  `LOCAL_VALIDATION_STATUS=PASS`, `SECURITY_REGRESSION_DETECTED=false`,
  `DEPLOYMENT_BEHAVIOR_CHANGED=false`.
