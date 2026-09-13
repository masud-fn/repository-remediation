# Behavioral evaluation cases

These cases are run manually with a disposable target repository. They check decisions that a static
validator (`scripts/validate_skill.py`) cannot prove — whether the skill investigates evidence,
classifies remediation authority correctly, and reports the required machine-readable verdict.

## How to run a case

1. Create a scratch git repository containing only the files described in the case's **Target repository
   setup**.
2. Invoke the relevant skill with the case's **Finding** as input.
3. Inspect the changed files, the commands actually run, and the final report.
4. Check every line in **Acceptance criteria**, including the required verdict fields from that skill's
   `SKILL.md`.

A case passes only if every acceptance criterion holds — a correct final verdict with the wrong files
changed (or vice versa) is a failure.

## Cases by skill

| Skill | Cases |
| --- | --- |
| [`repository-remediation`](repository-remediation/) | [`already-resolved`](repository-remediation/already-resolved.md), [`testing-fix`](repository-remediation/testing-fix.md), [`ci-alignment`](repository-remediation/ci-alignment.md), [`human-decision`](repository-remediation/human-decision.md), [`pre-existing-failure`](repository-remediation/pre-existing-failure.md) |
| [`ai-readiness`](ai-readiness/) | [`stale-command-reference`](ai-readiness/stale-command-reference.md), [`contradictory-install-instructions`](ai-readiness/contradictory-install-instructions.md), [`missing-security-boundary`](ai-readiness/missing-security-boundary.md), [`already-documented`](ai-readiness/already-documented.md) |
| [`ci-cd-readiness`](ci-cd-readiness/) | [`ci-local-parity`](ci-cd-readiness/ci-local-parity.md), [`pre-existing-ci-failure`](ci-cd-readiness/pre-existing-ci-failure.md), [`unpinned-third-party-action`](ci-cd-readiness/unpinned-third-party-action.md), [`unjustified-permission-broadening`](ci-cd-readiness/unjustified-permission-broadening.md) |
| [`test-readiness`](test-readiness/) | [`uncovered-critical-branch`](test-readiness/uncovered-critical-branch.md), [`no-test-framework-exists`](test-readiness/no-test-framework-exists.md), [`placeholder-assertions`](test-readiness/placeholder-assertions.md), [`flaky-time-based-test`](test-readiness/flaky-time-based-test.md) |

Every case file gives the finding to hand the skill, the minimal disposable repository state it assumes,
and the acceptance criteria — including which final verdict fields must be present and what values they
must take.
