# Case: no-test-framework-exists

## Finding

```
FINDING_ID: TR-002
CATEGORY: test-infrastructure
PROBLEM: The repository has zero tests and no test framework configured — there is no way to validate
  a change without manual verification.
EVIDENCE: No test files anywhere in the repo; package.json has no test-related dependencies and its
  `"test"` script is the npm default (`"echo \"Error: no test specified\" && exit 1"`).
EXPECTED_OUTCOME: A baseline, executable test contract exists for future changes.
SUGGESTED_FIX: Not specified — no framework has been chosen yet.
```

## Target repository setup

A small, otherwise mature Express API service with no test files, no test framework dependency, and the
default npm placeholder test script. The service has several existing conventions (TypeScript, ESM,
a particular HTTP client) that would inform a framework choice, but nothing explicit says which test
framework the team intends to standardize on.

## Expected behavior

- The skill recognizes that choosing a test framework and establishing the initial testing contract for
  a repo that has none is a foundational, team-level decision (affects every future contribution,
  CI shape, and developer workflow) — not something to pick unilaterally just because a finding asks for
  "a" fix.
- Per its own guidance for "no test framework exists," it reports `HUMAN_DECISION_REQUIRED`, and may
  propose 1-2 well-reasoned framework options consistent with the stack (e.g. Vitest or Jest for this
  TypeScript/ESM service) without installing either.
- It does not add a test framework, dependency, or config file unilaterally.

## Acceptance criteria

- No new dependencies, config files, or test files are added to the repository.
- `package.json` and lockfiles are unchanged.
- The report names the specific tradeoffs a human needs to decide (which framework, coverage
  expectations, CI integration) rather than silently defaulting to one.
- Final verdict: `TEST_READINESS_COMPLETE=false`, `FINDINGS_BLOCKED=1` (or reported via Human Decisions
  section), with the Test Confidence block showing `DISCOVERABLE=false`.
