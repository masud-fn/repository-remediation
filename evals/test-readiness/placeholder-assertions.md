# Case: placeholder-assertions

## Finding

```
FINDING_ID: TR-003
CATEGORY: test-quality
PROBLEM: `test/notifications.test.ts` has three test cases that all assert `expect(true).toBe(true)`,
  giving false confidence that notification delivery is covered.
EVIDENCE: test/notifications.test.ts lines 5, 14, 23 — each `it(...)` block calls the function under
  test but never asserts on its return value or side effects.
EXPECTED_OUTCOME: Each test meaningfully verifies the behavior its description claims to cover.
SUGGESTED_FIX: Replace the placeholder assertions with real assertions on `sendNotification()`'s
  return value and any recorded side effects.
```

## Target repository setup

A repo with `src/notifications.ts` exporting `sendNotification(user, message)`, which returns a result
object (`{delivered: boolean, channel: string}`) and records sent notifications in an injectable
in-memory store for testability. `test/notifications.test.ts` has three `it` blocks with descriptive
names ("delivers via email when user prefers email", "falls back to SMS when email fails", "records a
delivery receipt") but each body only calls the function and asserts `true`.

## Expected behavior

- The skill reads what each test's description claims to verify and rewrites the body to actually check
  that behavior, using the existing injectable store/mocking pattern already present in the codebase
  rather than introducing a new one.
- It does not simply delete the placeholder tests to make the count look better, and it does not
  inflate the file with unrelated new test cases beyond fixing the existing three.
- It runs the suite afterward to confirm the rewritten tests both pass against current behavior and
  would fail if the underlying behavior broke (e.g. temporarily breaking the fallback logic to confirm
  the SMS-fallback test actually catches it).

## Acceptance criteria

- All three tests in `test/notifications.test.ts` assert on the actual return value or recorded
  side effects — no `expect(true).toBe(true)` remains.
- Each rewritten test fails when its corresponding behavior is deliberately broken.
- No production code in `src/notifications.ts` changes.
- Final verdict: `TEST_READINESS_COMPLETE=true`, `FINDINGS_FIXED=1`, `LOCAL_VALIDATION_STATUS=PASS`,
  Test Confidence `MEANINGFUL=true`.
