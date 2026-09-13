# Case: uncovered-critical-branch

## Finding

```
FINDING_ID: TR-001
CATEGORY: coverage-gap
PROBLEM: `applyRefund()` in src/billing/refunds.ts has no test coverage for the case where the refund
  amount exceeds the original charge.
EVIDENCE: src/billing/refunds.ts lines 22-30; test/billing/refunds.test.ts covers only the standard
  full-refund path.
EXPECTED_OUTCOME: The over-refund guard is exercised by a test that fails if the guard is removed.
SUGGESTED_FIX: Add a test asserting `applyRefund()` throws/rejects when amount > original charge.
```

## Target repository setup

A repo using Jest (`npm test` → `jest`), with `src/billing/refunds.ts` exporting `applyRefund(charge,
amount)` that throws `RefundExceedsChargeError` when `amount > charge.total`. `test/billing/
refunds.test.ts` exists with a passing happy-path test; the over-refund guard is untested.

## Expected behavior

- The skill verifies the branch is genuinely untested (not just trusts the finding) by reading the
  existing test file and, ideally, checking coverage output if available.
- It adds a test using the existing Jest conventions in the same file/describe block, asserting the
  specific thrown error type/message, not a generic "it throws" placeholder.
- It runs the canonical test command and confirms the new test passes, then confirms it fails if the
  guard is temporarily removed (regression-proving the test).

## Acceptance criteria

- Diff is scoped to `test/billing/refunds.test.ts` only.
- The new test fails when the over-refund guard in `refunds.ts` is reverted, and passes otherwise.
- Final verdict: `TEST_READINESS_COMPLETE=true`, `FINDINGS_FIXED=1`, `LOCAL_VALIDATION_STATUS=PASS`.
- Test Confidence block: `DISCOVERABLE=true`, `MEANINGFUL=true`, `REPRODUCIBLE=true`,
  `CI_COMPATIBLE=true`.
