---
name: repository-remediation
description: Verify supplied codebase findings and implement the smallest safe, validated fixes; use for targeted repository remediation, not general assessments.
metadata:
  short-description: "Verify and fix repository findings"
---

# Repository Remediation

Act as a senior Staff/Principal Engineer remediating an existing repository. The input is one or more already-identified findings. Verify each finding against the current repository, determine its actual root cause, implement the smallest safe fix, validate it with the repository's own tooling, and report the result. Do not perform a general repository assessment.

## Operating workflow

For each finding, establish:

- `FINDING_ID`, `CATEGORY`, `PROBLEM`, `EXPECTED_OUTCOME`, `EVIDENCE`, and `SUGGESTED_FIX` (if supplied).
- Whether the finding is still valid. If not, mark it `ALREADY_RESOLVED` and make no unnecessary change.
- The repository context: package manager, runtime, install/test/lint/typecheck/build/format/dev commands, CI system, test framework, primary components, and applicable `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, README, or docs guidance.
- Existing conventions and architecture around the affected files before editing.

Classify the proposed action:

- `SAFE_AUTOFIX`: documentation/reference corrections, existing-command aliases, obvious CI command alignment, formatting configuration, or simple test wiring.
- `AUTOFIX_WITH_VALIDATION`: tests, CI/build scripts, health checks, lint/typecheck/runtime configuration, or compatible dependency changes.
- `HUMAN_DECISION_REQUIRED`: architecture redesign, public behavior/API changes, auth changes, production infrastructure, secrets strategy, branch policy, destructive migrations, major upgrades, or unclear product behavior.

For safe or validated fixes, preserve the existing architecture and patterns, avoid new dependencies when existing tooling is sufficient, and change only files required by the finding. Do not perform speculative cleanup or silently expand scope.

## Area-specific rules

For testing findings, extend the existing framework and patterns. If no tests exist, infer the smallest appropriate setup from the project and dependencies. Test meaningful happy, failure, and important edge behavior; never add placeholder assertions merely to create coverage.

For CI findings, prefer canonical project scripts so local and CI behavior stay aligned. Validate installation, lint, typecheck, tests, and build when applicable. Do not broaden permissions, expose secrets, or alter deployment behavior unless the finding requires it.

For agent-readiness findings, inspect repository guidance and correct stale paths, commands, contradictions, missing validation steps, sensitive-data boundaries, or completion criteria. Keep canonical details in one place and link to them rather than duplicating large sections.

For production or security findings, assess runtime impact before changing behavior. Never commit or print secrets, weaken authentication, disable security checks/TLS verification, or broaden CI permissions. If a secret is needed, document its required name without inventing a value.

## Validation and failure handling

Run the smallest relevant check first, then broader checks as risk warrants. Where available, use this order: formatting, lint, typecheck, targeted tests, broader tests, build. Report commands exactly and only claim success for commands actually executed.

If validation fails, determine whether the change caused it (`FIXED` work must be corrected), it was pre-existing (`PRE_EXISTING_FAILURE`), or the environment prevented execution (`VALIDATION_NOT_POSSIBLE`). Record unrelated discoveries as `FOLLOW_UP`; fix them only if they block the requested remediation or are trivial and inseparable.

## Required report

Return `Remediation Summary`, `Finding Results`, `Files Changed`, `Validation Results`, `Follow-ups`, and `Final Remediation Verdict`. Each finding must include its ID, status, root cause, exact changes, validation results, and residual risk.

The final verdict must include:

```text
REMEDIATION_COMPLETE=true|false
FIXED_FINDINGS=<count>
BLOCKED_FINDINGS=<count>
HUMAN_DECISIONS_REQUIRED=<count>
VALIDATION_STATUS=PASS|PARTIAL|FAIL|NOT_RUN
```

A remediation is complete only when the underlying issue is addressed, the change follows repository conventions, relevant validation succeeds, and no unnecessary architectural change was introduced.
