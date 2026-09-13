# Behavioral evaluation cases

These cases are run manually with a disposable target repository. They check decisions that a static validator cannot prove.

For each case, invoke the skill with the finding and inspect the changed files and final report. The expected behavior is part of the acceptance criteria.

| Case | Finding | Expected behavior |
| --- | --- | --- |
| `already-resolved` | Evidence is stale and the issue is already fixed | Report `ALREADY_RESOLVED`; make no changes |
| `testing-fix` | A meaningful branch has no coverage | Use the existing test framework, add focused coverage, and run the affected tests |
| `ci-alignment` | CI bypasses the repository's canonical test script | Align CI with the existing script without broadening permissions |
| `human-decision` | Fix requires a public API or schema redesign | Report `HUMAN_DECISION_REQUIRED`; do not guess |
| `pre-existing-failure` | A focused validation command fails before the change | Distinguish and report `PRE_EXISTING_FAILURE` |

Every evaluation should verify that the report contains the required final verdict fields from `SKILL.md`.
