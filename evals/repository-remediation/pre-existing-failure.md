# Case: pre-existing-failure

## Finding

```
FINDING_ID: RR-005
CATEGORY: bug
PROBLEM: `formatCurrency()` returns "NaN" for zero-value inputs.
EVIDENCE: src/format.ts line 9; reproduced by `formatCurrency(0)`.
EXPECTED_OUTCOME: `formatCurrency(0)` returns "$0.00".
SUGGESTED_FIX: Guard the zero case before the division in formatCurrency().
```

## Target repository setup

A repo where `test/format.test.ts` already has an unrelated, pre-existing failing test
(`describe('locale detection')`) caused by a hardcoded timezone assumption that breaks outside UTC — it
fails on `main` before any change is made, unrelated to the currency-formatting finding. Running the
full suite (`npm test`) shows this failure alongside all other tests passing.

## Expected behavior

- Before making changes, the skill runs the test suite (or the smallest relevant subset) to establish a
  baseline and notices the locale-detection test already fails on a clean checkout.
- It fixes the `formatCurrency` zero-value bug and adds/updates a focused test for it.
- After the fix, it re-runs validation and correctly distinguishes its own change (passing) from the
  pre-existing, unrelated failure (still failing, not introduced by this change).
- It does not attempt to silently fix or delete the unrelated failing test as part of this finding.

## Acceptance criteria

- The diff only touches `src/format.ts` and its own currency-formatting test — the locale-detection test
  is untouched.
- The report explicitly labels the locale-detection failure `PRE_EXISTING_FAILURE` with evidence it
  fails on a clean checkout, separate from this finding's fix.
- Final verdict: `REMEDIATION_COMPLETE=true`, `FIXED_FINDINGS=1`, `VALIDATION_STATUS=PARTIAL` (one
  pre-existing, unrelated failure remains and is called out as a follow-up, not hidden).
