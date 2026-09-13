---
name: ci-cd-readiness
description: Verify and remediate CI/CD readiness issues while preserving the repository's architecture, conventions, and least-privilege security model.
metadata:
  short-description: "Fix CI/CD readiness gaps"
---

# CI/CD Readiness Remediation
You are responsible for improving the CI/CD readiness of an existing software repository.

Your task is not to redesign the delivery platform.

Your task is to identify and remediate concrete CI/CD gaps using the repository's existing architecture, tooling, workflows, and conventions.

The desired outcome is a CI/CD pipeline that is:

- deterministic
- reproducible
- aligned with local development
- reliable on pull requests and the default branch
- secure by default
- easy to diagnose when it fails
- minimally complex
- safe to evolve
Do not optimize for adding more pipeline stages.

Optimize for creating a reliable validation and delivery contract.

---

# 1. Start With Repository Reality
Before making any CI/CD change, inspect the repository and determine:

- language/runtime
- package manager
- dependency lockfiles
- monorepo or single-project structure
- application components
- existing CI platform
- existing workflows
- deployment/release workflows
- canonical repository commands
- test framework
- build system
- lint/type-check tooling
- runtime/toolchain version configuration
- environment requirements
- artifact generation
- deployment targets
Do not assume Node, Java, .NET, Python, GitHub Actions, or any specific technology.

Adapt to the repository.

---

# 2. Treat Existing Findings as Hypotheses
You may receive findings such as:

- CI failing on the default branch
- tests not executed in CI
- no canonical test command
- build not validated
- lint/type-check not executed
- runtime not pinned
- duplicated CI logic
- unsafe workflow permissions
- release pipeline not validated
- inconsistent local and CI commands
Verify each finding against the current repository before modifying anything.

Use:

`VERIFIED`

`ALREADY_RESOLVED`

`NOT_REPRODUCIBLE`

`BLOCKED_BY_ENVIRONMENT`

Do not change files simply because an assessment recommended doing so.

---

# 3. Discover the Canonical Validation Contract
Determine the repository's intended commands.

Where applicable identify:

`INSTALL_COMMAND`

`LINT_COMMAND`

`TYPECHECK_COMMAND`

`TEST_COMMAND`

`BUILD_COMMAND`

`FORMAT_CHECK_COMMAND`

`PACKAGE_MANAGER`

`RUNTIME_VERSION`

`CI_PLATFORM`

`DEPLOY_COMMAND`

`RELEASE_COMMAND`

Prefer existing top-level repository commands.

For example, prefer:

`npm test`

over embedding:

`vitest run`

directly inside CI when `npm test` is intended to be the project's stable interface.

CI should consume repository commands.

CI should not become the only place where repository behavior is defined.

---

# 4. Establish the CI Invariant
Before making changes, define what should be guaranteed.

Typical invariant:

> Every change merged into the default branch has passed the same canonical validation contract that developers and automation can execute locally.
Depending on the repository, this may include:

1. deterministic dependency installation
2. lint
3. type-check
4. tests
5. build
6. security checks
7. artifact validation
Only require checks that are relevant to this repository.

Do not invent validation stages simply because they are common elsewhere.

---

# 5. Local and CI Parity
CI and local development should use the same underlying commands wherever practical.

Avoid situations such as:

Local:

`npm test`

CI:

`npx vitest run src/**/*.spec.ts --environment node`

Prefer:

CI → `npm test`

This keeps:

- developers
- CI
- AI agents
- repository automation
on the same contract.

If local and CI commands intentionally differ, document why.

---

# 6. Dependency Installation
Inspect how dependencies are installed.

Prefer deterministic installation.

Examples:

Node:

- `npm ci`
- frozen lockfile equivalent for the selected package manager
Python:

- locked requirements or supported dependency lock mechanism
Java:

- repository-supported Maven/Gradle wrapper
.NET:

- repository-supported SDK/toolchain configuration
Do not replace the repository's package manager.

Verify that CI respects the committed lockfile where applicable.

---

# 7. Runtime and Toolchain Determinism
Determine whether CI and developers are using a predictable runtime/toolchain.

Check for repository-native mechanisms such as:

- `.nvmrc`
- `.node-version`
- `package.json` engines
- `.tool-versions`
- `global.json`
- Java toolchain configuration
- Python version configuration
- container definitions
If the runtime is not pinned and the intended version can be reliably inferred from repository evidence, introduce the smallest suitable pin.

If the correct runtime cannot be determined confidently:

`HUMAN_DECISION_REQUIRED`

Do not guess.

---

# 8. Pull Request Validation
Inspect pull-request CI.

Verify whether PRs execute the repository's meaningful validation contract.

Where applicable this may include:

`install → lint → typecheck → test → build`

Do not blindly create all stages.

Determine which stages actually apply.

Important validation should fail the workflow when the underlying command fails.

Do not suppress meaningful failures using patterns such as:

`|| true`

or equivalent mechanisms unless intentionally required and explicitly documented.

---

# 9. Default Branch Health
The default branch should represent a known-good repository state.

Inspect:

- currently configured branch workflows
- triggers
- required validation
- branch-specific behavior
- failures caused by outdated commands
- missing pipeline stages
- inconsistent environment configuration
If CI fails on the default branch:

identify the root cause before adding new CI functionality.

Do not layer additional automation over a broken baseline.

Prioritize restoring the existing validation contract first.

---

# 10. Testing in CI
If tests exist:

ensure CI executes the canonical test command.

If no canonical test command exists but the repository clearly has an existing test runner:

create the smallest stable repository-level command and make CI call it.

Example:

Instead of CI calling a framework directly:

`npx jest`

prefer adding:

`"test": "jest"`

and letting CI run:

`npm test`

where this aligns with repository conventions.

If no test suite exists, do not create meaningless tests merely to make CI green.

Report the absence of tests as a dependency on Testing Readiness unless the requested remediation explicitly includes establishing testing infrastructure.

---

# 11. Build Validation
Determine whether the repository produces something that should be built before merge.

Examples:

- application bundle
- compiled binary
- container
- package
- library
- generated artifact
If a canonical build command exists, determine whether it should be executed in PR validation.

A build failure should be caught before deployment wherever practical.

Do not add expensive build stages without understanding their value and cost.

---

# 12. Workflow Structure
Prefer simple workflows.

Avoid unnecessary:

- job duplication
- YAML duplication
- repeated dependency installation
- repeated environment setup
- excessive workflow indirection
- repository-specific logic embedded only in CI
Where multiple workflows require the same repository behavior, prefer repository scripts or established reusable workflow patterns.

Do not create abstractions merely to reduce a small number of YAML lines.

---

# 13. Job Dependencies
Make dependencies between jobs explicit.

For example:

`validate → build → package → deploy`

Do not allow deployment to proceed if its required validation has failed.

Avoid unnecessary serialization when jobs can safely execute independently.

Optimize for correctness first, then execution efficiency.

---

# 14. Caching
Use caching only when it provides meaningful value.

Cache candidates may include:

- dependency caches
- package-manager caches
- build caches
Never rely on cache contents for correctness.

The pipeline should still succeed from a cold cache.

Cache keys should reflect meaningful dependency inputs such as lockfiles.

Do not introduce complicated caching during basic readiness remediation unless pipeline cost or duration justifies it.

---

# 15. CI Security
Apply least privilege.

Inspect workflow permissions.

Do not unnecessarily grant:

- repository write access
- package write access
- deployment permissions
- token access
- pull-request write permissions
- broad GitHub token permissions
Do not expose secrets to workflows that do not need them.

Be particularly careful with workflows triggered by external pull requests.

Never:

- print secrets
- hardcode credentials
- disable TLS verification
- weaken authentication
- expose production environment variables for validation-only jobs

---

# 16. Third-Party Actions and Dependencies
Inspect third-party CI actions/plugins.

Follow repository or organizational conventions for version pinning.

Avoid unnecessary third-party actions when the CI platform or existing tooling already provides equivalent functionality.

Do not perform broad dependency modernization unless explicitly required.

---

# 17. Release and Deployment Pipelines
Treat deployment workflows separately from validation workflows.

Do not modify production deployment semantics unless the finding requires it.

If deployment remediation is requested, inspect:

- deployment trigger
- environment
- artifact source
- approval gates
- environment protection
- version identification
- migration sequencing
- health verification
- rollback capability
A deployment should consume an already validated artifact where the repository architecture supports this.

Avoid rebuilding materially different artifacts during deployment.

---

# 18. Artifacts
When CI produces deployable artifacts, determine whether they are:

- reproducible
- traceable to a commit
- immutable where appropriate
- generated after successful validation
Prefer clear linkage between:

`commit → validation → artifact → deployment`

Do not introduce artifact infrastructure if the repository does not need it.

---

# 19. Failure Diagnostics
A CI failure should be understandable.

Ensure important commands:

- return meaningful exit codes
- expose useful logs
- fail at the correct stage
Avoid hiding failures behind generic scripts that provide no diagnostic information.

When practical, jobs should make it obvious whether failure occurred during:

- setup
- lint
- type-check
- test
- build
- packaging
- deployment
Do not introduce unnecessary logging frameworks into CI.

---

# 20. Concurrency
Inspect whether duplicate or obsolete workflow runs waste resources or create deployment risk.

For validation workflows, consider cancellation of superseded runs where supported and appropriate.

For deployments, ensure concurrency behavior cannot accidentally overlap unsafe production changes.

Do not introduce concurrency rules without understanding deployment semantics.

---

# 21. Timeouts and Hanging Jobs
Where supported and appropriate, ensure critical jobs cannot run indefinitely.

Use reasonable workflow/job timeouts based on existing execution characteristics.

Do not invent aggressively short timeouts that create flaky CI.

---

# 22. Monorepo Awareness
If the repository is a monorepo:

determine whether validation should operate:

- across the entire repository
- per workspace/component
- only on affected components
Prefer existing workspace/build-system capabilities.

Do not introduce complex change-detection logic unless repository scale requires it.

Correctness is more important than optimizing every CI second.

---

# 23. Scope Control
Do not turn CI/CD remediation into:

- repository modernization
- test-suite redesign
- architectural refactoring
- deployment-platform migration
- package-manager migration
- framework upgrade
If another problem is discovered, record:

`FOLLOW_UP`

unless it directly blocks the requested CI/CD fix.

---

# 24. Change Safety Classification
Classify each proposed change.

## SAFE_AUTOFIX
Examples:

- fixing stale command references
- wiring an existing test command into CI
- correcting broken workflow syntax
- using an existing canonical build command
- correcting obvious trigger mistakes

## AUTOFIX_WITH_VALIDATION
Examples:

- introducing a canonical validation script
- pinning runtime/toolchain versions
- restructuring workflow jobs
- introducing caching
- changing CI permissions
- modifying release workflow logic

## HUMAN_DECISION_REQUIRED
Examples:

- replacing the CI platform
- changing deployment strategy
- changing production approval policy
- changing branch-protection policy
- introducing a new artifact registry
- changing secrets-management strategy
- modifying environment promotion models
Do not infer organizational policy.

---

# 25. Validation of CI Changes
After modification, validate as much of the pipeline contract locally as possible.

Run applicable canonical commands.

For example:

`INSTALL_COMMAND`
`LINT_COMMAND`
`TYPECHECK_COMMAND`
`TEST_COMMAND`
`BUILD_COMMAND`

Also validate CI configuration syntax where supported.

If workflow execution itself cannot be reproduced locally, clearly distinguish:

`LOCAL_VALIDATION_PASS`

from:

`REMOTE_CI_NOT_VERIFIED`

Never claim CI passes unless there is evidence that CI actually executed successfully.

---

# 26. Existing Failures
If a validation command fails, determine whether the failure was:

`INTRODUCED_BY_CHANGE`

`PRE_EXISTING_FAILURE`

`ENVIRONMENT_FAILURE`

`UNKNOWN`

Do not modify unrelated application code merely to make CI green unless it directly belongs to the requested remediation.

Do not hide pre-existing failures.

---

# 27. Completion Criteria
CI/CD remediation is complete only when:

1. the original finding has been verified
2. its root cause has been identified
3. canonical repository commands are used where appropriate
4. local and CI validation are aligned
5. the smallest reasonable pipeline change has been made
6. relevant validation has passed
7. no security controls were weakened
8. no unnecessary deployment behavior was changed
9. remaining unverified behavior is explicitly documented
A changed YAML file alone does not mean the finding is fixed.

---

# 28. Required Output

## CI/CD Remediation Summary
`STATUS=SUCCESS|PARTIAL_SUCCESS|NO_CHANGE_REQUIRED|BLOCKED`

---

## Before
Describe the verified CI/CD problem.

Include:

- affected workflow
- affected command
- affected trigger/job
- observed failure or missing validation

---

## Root Cause
Explain why the problem existed.

Avoid restating the symptom.

---

## Expected Invariant
State what should now remain true.

Example:

> Every pull request and default-branch update executes the same canonical test command available to developers locally.

---

## Changes Applied
For each changed file:

`<file>`

- what changed
- why it was required

---

## Canonical Validation Contract
Report discovered commands:

`INSTALL_COMMAND=<command|NOT_DISCOVERED>`

`LINT_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`TYPECHECK_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`TEST_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`BUILD_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`RUNTIME_VERSION=<version|NOT_DISCOVERED>`

`PACKAGE_MANAGER=<value>`

`CI_PLATFORM=<value>`

---

## Validation Results
Report exact commands and results.

Example:

`npm ci` — PASS

`npm run lint` — PASS

`npm run typecheck` — PASS

`npm test` — PASS

`npm run build` — PASS

`.github/workflows/ci.yml syntax` — PASS

Never fabricate execution results.

---

## CI Verification
Report:

`LOCAL_VALIDATION=PASS|PARTIAL|FAIL|NOT_RUN`

`REMOTE_CI=PASS|FAIL|NOT_VERIFIED`

Do not treat local execution as proof that remote CI succeeded.

---

## Security Impact
Report whether the remediation changed:

- workflow permissions
- secrets usage
- deployment credentials
- external actions
- environment access
Use:

`SECURITY_IMPACT=NONE|LOW|MEDIUM|HIGH`

Explain any non-NONE result.

---

## Blast Radius
`BLAST_RADIUS=LOW|MEDIUM|HIGH`

Explain which developer, CI, release, or production workflows could be affected.

---

## Follow-Ups
List relevant issues discovered but intentionally not fixed.

---

# 29. Final Verdict
Return:

`CICD_REMEDIATION_COMPLETE=true|false`

`FINDINGS_FIXED=<count>`

`FINDINGS_BLOCKED=<count>`

`LOCAL_VALIDATION_STATUS=PASS|PARTIAL|FAIL|NOT_RUN`

`REMOTE_CI_STATUS=PASS|FAIL|NOT_VERIFIED`

`SECURITY_REGRESSION_DETECTED=true|false`

`DEPLOYMENT_BEHAVIOR_CHANGED=true|false`
