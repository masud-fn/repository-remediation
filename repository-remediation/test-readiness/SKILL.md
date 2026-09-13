---
name: test-readiness
description: Improve a repository's test readiness by establishing a canonical, meaningful, and executable testing contract that works for developers, CI, and coding agents.
metadata:
  short-description: "Improve test readiness"
---

# Test Readiness Remediation

You are responsible for improving the test readiness of an existing software repository.

Your task is not to maximize test count or coverage percentages.

Your task is to establish a reliable, maintainable, and executable testing contract that gives engineers, CI, and AI agents confidence that changes can be validated safely.

The desired outcome is a repository where:

- tests are discoverable
- tests exercise meaningful behavior
- there is a canonical test command
- tests run consistently across environments
- failures are understandable
- test infrastructure follows repository conventions
- critical behavior has appropriate protection
- CI can consume the same testing contract used locally

Do not optimize for the number of tests.

Optimize for confidence in change.

---

# 1. Start With Repository Reality

Before making any testing change, inspect the repository and determine:

- language/runtime
- framework
- application architecture
- package manager
- build system
- existing test frameworks
- existing test directories
- test naming conventions
- existing test scripts
- CI workflows
- component boundaries
- public interfaces
- critical business logic
- external dependencies
- database usage
- messaging/event systems
- API boundaries
- existing mocks, fixtures, factories, and test utilities

Do not assume Jest, Vitest, JUnit, pytest, xUnit, NUnit, Cypress, Playwright, or any other framework.

Adapt to the repository.

---

# 2. Treat Existing Findings as Hypotheses

You may receive findings such as:

- no test suite detected
- no canonical test command
- tests exist but cannot be discovered
- tests fail locally
- test framework configuration is incomplete
- tests are flaky
- important components are untested
- tests depend on developer-specific state
- tests require undocumented services
- coverage configuration is broken
- tests cannot run in CI
- tests are coupled to implementation details

Verify each finding against the current repository before modifying anything.

Use:

`VERIFIED`

`ALREADY_RESOLVED`

`NOT_REPRODUCIBLE`

`BLOCKED_BY_ENVIRONMENT`

Do not modify test infrastructure solely because an assessment suggested doing so.

---

# 3. Discover the Existing Test Contract

Determine whether the repository already has a testing contract.

Identify where applicable:

`TEST_COMMAND`

`UNIT_TEST_COMMAND`

`INTEGRATION_TEST_COMMAND`

`E2E_TEST_COMMAND`

`TEST_FRAMEWORK`

`TEST_CONFIG`

`TEST_DIRECTORIES`

`TEST_FILE_PATTERN`

`FIXTURE_LOCATION`

`MOCKING_STRATEGY`

`COVERAGE_COMMAND`

`COVERAGE_CONFIGURATION`

`TEST_ENVIRONMENT`

`REQUIRED_TEST_SERVICES`

Prefer existing repository commands.

For example:

Prefer:

`npm test`

over requiring engineers to know:

`vitest run --environment=node`

if the repository can expose a stable canonical command.

---

# 4. Establish the Testing Invariant

Before modifying anything, define what should remain true.

Typical invariant:

> A developer or automation agent can make a change and execute a documented canonical command that provides meaningful confidence that the affected behavior still works.

Additional invariants may include:

- tests are deterministic
- tests do not depend on developer-specific state
- tests fail for real regressions
- important behavior has appropriate protection
- test setup is reproducible
- local and CI execution use the same contract

The exact invariant depends on the repository.

---

# 5. Determine Current Test Maturity

Classify the repository.

## LEVEL 0 — No test infrastructure

No test runner or meaningful test suite exists.

## LEVEL 1 — Test infrastructure exists

A test runner exists but coverage is sparse, commands are unclear, or execution is unreliable.

## LEVEL 2 — Core behavior protected

Meaningful unit/component tests exist around important behavior.

## LEVEL 3 — System boundaries protected

Integration tests validate important interactions with databases, APIs, queues, or external systems.

## LEVEL 4 — Critical journeys protected

End-to-end or acceptance tests protect high-value workflows where appropriate.

Do not force every repository to reach Level 4.

Choose the level appropriate to its risk and architecture.

---

# 6. Test Strategy Selection

Select testing techniques based on actual repository risks.

Use:

## Unit tests

For:

- pure business logic
- transformations
- validation
- calculations
- decision logic
- isolated components

## Component/service tests

For:

- service behavior
- module boundaries
- handlers
- controllers
- application services

## Integration tests

For behavior involving:

- databases
- repositories
- message brokers
- external APIs
- file systems
- caches
- infrastructure boundaries

## End-to-end tests

For critical workflows spanning multiple components.

Do not introduce every test type automatically.

Choose the smallest test layer that provides useful confidence.

---

# 7. Prefer Behavior Over Implementation

Tests should primarily verify externally observable behavior.

Prefer:

"When invalid input is provided, the service rejects the request."

over:

"Private method validatePayload() was called exactly once."

Avoid excessive coupling to:

- private methods
- implementation ordering
- internal object shapes
- framework internals

Tests should allow reasonable refactoring without unnecessary breakage.

---

# 8. Identify High-Value Test Targets

Prioritize testing based on risk.

Look for:

- business-critical behavior
- complex conditional logic
- data transformations
- authentication/authorization boundaries
- financial calculations
- state transitions
- error handling
- retry behavior
- concurrency-sensitive logic
- external integration boundaries
- previously failing behavior
- frequently modified code
- code with high blast radius

Do not distribute tests uniformly across the repository.

Test where failure would matter.

---

# 9. Establish a Canonical Test Command

The repository should expose a clear testing entry point.

Examples:

`npm test`

`pnpm test`

`dotnet test`

`mvn test`

`./gradlew test`

`pytest`

Use the repository's existing conventions.

If multiple test layers exist, provide stable commands such as:

`test`

`test:unit`

`test:integration`

`test:e2e`

Do not expose unnecessarily complex framework arguments to normal users.

The canonical command should become a stable interface for:

- developers
- CI
- AI agents
- automation

---

# 10. If No Test Framework Exists

Do not immediately install a preferred framework.

First inspect:

- dependencies
- framework conventions
- historical configuration
- neighboring packages
- repository documentation
- build tooling
- existing test-related files

Choose the most natural testing tool for the existing ecosystem.

Prefer widely supported tooling already compatible with the repository.

Avoid introducing multiple competing test frameworks.

If multiple legitimate options exist and repository intent is unclear:

`HUMAN_DECISION_REQUIRED`

---

# 11. First Test Selection

When establishing testing in a previously untested repository, do not start with trivial examples.

Select a small number of representative tests that prove the infrastructure and protect real behavior.

A good first test should validate:

- meaningful application behavior
- the test runner configuration
- repository module resolution
- dependency setup
- expected failure behavior

Prefer a real use case over:

`expect(true).toBe(true)`

Infrastructure-only tests are acceptable only when explicitly validating test-runner setup.

---

# 12. Happy Path, Failure Path, Edge Cases

For meaningful functionality, consider:

## Happy path

Expected valid behavior.

## Failure path

How the component behaves when input, dependencies, or state are invalid.

## Relevant edge case

Boundary conditions that could produce unexpected behavior.

Do not mechanically create three tests for every method.

Use judgment based on risk.

---

# 13. Test Isolation

Tests should not depend on:

- execution order
- previous tests
- developer machine state
- real production credentials
- existing local database contents
- current time without control
- external network availability unless explicitly integration-tested

Each test should establish the state it requires.

Clean up state when necessary.

---

# 14. Determinism

Avoid flaky tests.

Inspect sources of nondeterminism such as:

- current time
- random values
- asynchronous timing
- race conditions
- external networks
- shared state
- global configuration
- uncontrolled database state
- file-system state
- retries and polling

Use deterministic controls where appropriate.

Do not introduce excessive mocking merely to eliminate all real interaction.

---

# 15. Mocking Strategy

Mock at meaningful boundaries.

Good mock candidates may include:

- third-party APIs
- email/SMS providers
- payment services
- external queues
- remote services

Avoid mocking the code being tested.

Avoid deeply mocking internal implementation chains.

Prefer fakes or lightweight test implementations when they produce more realistic behavior with lower maintenance cost.

---

# 16. External Dependencies

If tests require external systems, determine whether they should use:

- mocks
- fakes
- local containers
- embedded services
- dedicated test infrastructure
- contract testing

Choose based on repository architecture and risk.

Do not make ordinary unit tests depend on real external services.

---

# 17. Database Testing

When testing persistence behavior:

- isolate test data
- use test-specific configuration
- avoid production credentials
- ensure repeatable setup
- clean state predictably
- apply migrations consistently where appropriate

Do not assume an in-memory database behaves identically to production.

If database behavior itself matters, use an appropriately representative test environment.

---

# 18. Configuration and Environment

Document required test configuration.

Tests should clearly distinguish:

- required environment variables
- optional configuration
- test-only values
- external services

Do not require real secrets.

Provide safe test defaults where repository conventions allow.

Never commit real credentials.

---

# 19. Test Data

Prefer test data that is:

- minimal
- readable
- explicit
- relevant to the behavior under test

Avoid giant fixtures that make failures difficult to understand.

Use factories/builders when they materially improve clarity or reduce repetition.

---

# 20. Failure Diagnostics

A failing test should be informative.

Prefer assertions that clearly indicate:

- expected behavior
- actual behavior
- relevant input or state

Avoid vague `toBeTruthy()` assertions when a more precise assertion communicates the contract better.

Use test names that describe the scenario and expected outcome.

---

# 21. CI Test Execution

CI should run the repository's canonical test contract, not an ad hoc framework invocation.

Verify:

- installation step uses lockfile and repo-native package manager
- test command is stable
- required services are available where necessary
- failures are surfaced clearly
- the same command can run locally

Do not create CI-only test logic that developers cannot reproduce.

---

# 22. Coverage and Quality Signals

Coverage can be useful as a supplement, not as a policy objective.

Use coverage to identify blind spots, not to chase arbitrary percentages.

Prefer targeted coverage around risk-prone code.

Do not collapse meaningful testing quality into a single metric.

---

# 23. Flaky Test Management

If tests are flaky, identify the cause before changing expectations.

Potential causes include:

- timing assumptions
- shared state
- non-deterministic ordering
- network dependence
- random data
- race conditions
- unsuitable environment assumptions

Fix root cause, not just retries.

---

# 24. Evolving the Test Suite

As the repository evolves, test quality should evolve with it.

Add or adjust tests when:

- behavior changes
- bug fixes are made
- risky behavior is introduced
- external interfaces change
- integration boundaries change

Do not add tests just to satisfy a metric.

---

# 25. Reproducibility and Setup

The repository should make test setup discoverable and consistent.

Document:

- required services
- environment variables
- setup commands
- fixture generation steps
- cleanup expectations
- platform constraints, if any

Where practical, prefer repository-native configuration over one-off local setup.

---

# 26. Scope Control

Do not turn test-readiness remediation into:

- rewriting the whole test suite
- broad refactors for style
- large framework migrations
- chasing coverage percentages
- adding meaningless tests
- introducing architecture changes solely to enable testing

Use follow-ups such as:

`FOLLOW_UP: CI_CD_READINESS`

`FOLLOW_UP: DESIGN_READINESS`

`FOLLOW_UP: PRODUCTION_READINESS`

---

# 27. Change Safety Classification

## SAFE_AUTOFIX

Examples:

- wiring CI to an existing test command
- fixing stale test script names
- correcting test directories or config names
- documenting an existing testing workflow
- aligning local and CI commands around the same script

## AUTOFIX_WITH_VALIDATION

Examples:

- adding a missing canonical `test` script
- adding a focused failing test for a real bug
- fixing flaky configuration or setup
- adding repository-native test environment guidance
- adjusting test command names to reflect actual repository tooling

## HUMAN_DECISION_REQUIRED

Examples:

- choosing among multiple legitimate test frameworks
- adding major new infrastructure for testing
- introducing broad new architectural testing patterns
- deciding on production-like test systems when repository policy is unclear

---

# 28. Validation

After making test-readiness changes, validate:

1. the canonical test command exists
2. the command runs in the repository environment
3. critical tests pass
4. relevant test suite setup is reproducible
5. CI and local invocation agree on the command contract
6. failures are understandable
7. no secrets or environment-specific values were introduced

If a component cannot be tested locally, report the environment limitation clearly.

---

# 29. Existing Problems

If a test command fails, determine whether the failure is:

`INTRODUCED_BY_CHANGE`

`PRE_EXISTING_FAILURE`

`ENVIRONMENT_FAILURE`

`UNKNOWN`

Do not hide real failures or write tests merely to claim readiness.

---

# 30. Completion Criteria

Test-readiness remediation is complete only when:

1. the initial finding was verified
2. the root cause was understood
3. the repository has a discoverable canonical test contract
4. tests protect meaningful behavior
5. the setup is reproducible and safe
6. local and CI use the same command path where practical
7. failures are diagnosable
8. no unnecessary framework churn was introduced

---

# 31. Required Output

## Test Readiness Summary

`STATUS=SUCCESS|PARTIAL_SUCCESS|NO_CHANGE_REQUIRED|BLOCKED`

## Before

Describe the verified test-readiness problem.

## Root Cause

Explain why the repository lacked a reliable test contract.

## Expected Invariant

State what should remain true after the fix.

## Canonical Test Contract

`TEST_COMMAND=<command|NOT_DISCOVERED>`

`UNIT_TEST_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`INTEGRATION_TEST_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`E2E_TEST_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`TEST_FRAMEWORK=<framework|NOT_DISCOVERED>`

`TEST_CONFIG=<path|NOT_DISCOVERED>`

`TEST_DIRECTORIES=<paths|NOT_DISCOVERED>`

`REQUIRED_TEST_SERVICES=<services|NONE|NOT_DISCOVERED>`

## Changes Applied

For each changed file:

- what changed
- why it was required

## Validation Results

Report exact commands and results.

Examples:

`npm test` — PASS

`pytest` — PASS

`dotnet test` — PASS

`<test command>` — FAIL due to pre-existing issue

## Test Confidence

`DISCOVERABLE=true|false`

`MEANINGFUL=true|false`

`REPRODUCIBLE=true|false`

`CI_COMPATIBLE=true|false`

## Human Decisions

List decisions that could not safely be inferred from repository evidence.

## Follow-Ups

List relevant issues intentionally not fixed.

---

# 32. Final Verdict

`TEST_READINESS_COMPLETE=true|false`

`FINDINGS_FIXED=<count>`

`FINDINGS_BLOCKED=<count>`

`LOCAL_VALIDATION_STATUS=PASS|PARTIAL|FAIL|NOT_RUN`

`REMOTE_CI_STATUS=PASS|FAIL|NOT_VERIFIED`

`SECURITY_REGRESSION_DETECTED=true|false`

`DEPLOYMENT_BEHAVIOR_CHANGED=true|false`
