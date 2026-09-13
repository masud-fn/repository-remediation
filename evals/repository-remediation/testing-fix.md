# Case: testing-fix

## Finding

```
FINDING_ID: RR-002
CATEGORY: testing
PROBLEM: `calculateDiscount()` in src/pricing.ts has no test coverage for the branch where the
  discount would push the price below zero.
EVIDENCE: src/pricing.ts lines 18-27; test/pricing.test.ts only covers the standard-discount path.
EXPECTED_OUTCOME: The negative-price branch is exercised by a test that fails if the clamp is removed.
SUGGESTED_FIX: Add a test asserting the price is clamped to 0, using the existing Vitest setup.
```

## Target repository setup

A TypeScript repo using Vitest (`npm test` runs `vitest run`, defined in package.json). `src/pricing.ts`
has a `calculateDiscount(price, percentOff)` function that clamps the result to a minimum of 0.
`test/pricing.test.ts` exists with one passing test for the normal-discount case; the clamp branch is
untested.

## Expected behavior

- The skill confirms the branch is genuinely uncovered before writing anything (does not just trust the
  finding text).
- It extends `test/pricing.test.ts` using the existing Vitest patterns (same describe/it style, same
  assertion library) rather than introducing a new test framework or file layout.
- The new test exercises real behavior (asserts clamped output) rather than a placeholder
  (`expect(true).toBe(true)`).
- It runs the project's canonical test command and reports the result.

## Acceptance criteria

- The diff touches only `test/pricing.test.ts` (or an equally scoped test file) — no production code
  changes beyond what's required to make the test meaningful.
- The added test fails if the clamping logic in `src/pricing.ts` is removed (verify by temporarily
  reverting the clamp and re-running).
- The report shows the exact test command run (e.g. `npm test`) and that it passed.
- Final verdict: `REMEDIATION_COMPLETE=true`, `FIXED_FINDINGS=1`, `VALIDATION_STATUS=PASS`.
