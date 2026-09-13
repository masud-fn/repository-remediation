# Case: flaky-time-based-test

## Finding

```
FINDING_ID: TR-004
CATEGORY: flaky-test
PROBLEM: `test/session.test.ts`'s "expires after 30 minutes" test intermittently fails in CI because it
  calls `new Date()` directly instead of controlling time, so it's sensitive to real wall-clock timing
  and scheduling jitter.
EVIDENCE: test/session.test.ts lines 10-18; CI history shows ~4% failure rate on this test over the
  last month with no corresponding code change.
EXPECTED_OUTCOME: The test is deterministic regardless of when or how fast it runs.
SUGGESTED_FIX: Use the test framework's fake timers instead of real `Date`/`setTimeout`.
```

## Target repository setup

A repo using Vitest, where `src/session.ts` computes expiry via `Date.now() + ttlMs`, and
`test/session.test.ts` creates a session, sleeps using a real `setTimeout`, then checks expiry — making
the test both slow and occasionally flaky under CI scheduling pressure. Vitest's fake timer API
(`vi.useFakeTimers()`) is already used elsewhere in the test suite (e.g. `test/cache.test.ts`), so there
is a repository convention to follow.

## Expected behavior

- The skill identifies the root cause (real-time dependency) rather than papering over the flake with a
  retry annotation or a longer sleep/timeout.
- It rewrites the test using the project's existing fake-timer convention (matching `test/cache.test.ts`'s
  pattern), advancing simulated time instead of sleeping in real time.
- It verifies the fix by running the test repeatedly (or reasoning about why fake timers eliminate the
  timing dependency) rather than asserting it's fixed without evidence.

## Acceptance criteria

- The diff is scoped to `test/session.test.ts`; no retry/quarantine annotations are added as a
  workaround.
- The rewritten test no longer calls real `setTimeout`/sleeps and uses the same fake-timer API as
  `test/cache.test.ts`.
- The report explains the root cause (wall-clock dependency) and why the fix removes it, not just that
  the test "passed this time."
- Final verdict: `TEST_READINESS_COMPLETE=true`, `FINDINGS_FIXED=1`, `LOCAL_VALIDATION_STATUS=PASS`,
  Test Confidence `REPRODUCIBLE=true`.
