---
name: ai-readiness
description: Improve the repository's AI/agent readiness by fixing stale guidance, validating executable commands, and clarifying architecture, safety, and completion boundaries.
metadata:
  short-description: "Improve AI/agent repository readiness"
---

# AI Readiness Remediation

You are responsible for improving the AI / agent readiness of an existing software repository.

Your task is not to make the repository "AI-specific."

Your task is to make the repository understandable, navigable, executable, and safely modifiable by coding agents without reducing its usability for human engineers.

The desired outcome is a repository where an AI coding agent can reliably determine:

- what the repository does
- how it is structured
- how to install dependencies
- how to run the application
- how to test changes
- how to lint and type-check
- how to build
- which architectural constraints must be preserved
- which areas are sensitive
- what should not be modified
- how changes should be reviewed
- what constitutes a completed change

Do not optimize for more documentation.

Optimize for correct, concise, executable repository guidance.

---

# 1. Start With Repository Reality

Before making any AI-readiness change, inspect:

- repository purpose
- application/component structure
- language/runtime
- package manager
- build system
- test framework
- CI/CD system
- developer documentation
- architecture documentation
- contribution guidance
- code ownership
- agent-specific instructions
- security-sensitive areas
- generated files
- deployment-related files
- canonical repository commands

Inspect relevant instruction sources such as:

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `CONTRIBUTING.md`
- `/docs`
- architecture decision records
- developer guides
- repository-local skills
- editor/agent instruction files

Do not assume any particular agent platform.

---

# 2. Treat Existing Findings as Hypotheses

Verify findings such as:

- broken references in agent instructions
- stale commands
- contradictory guidance
- missing setup instructions
- missing test instructions
- missing validation steps
- undocumented architecture boundaries
- missing code-review guidance
- missing secrets-handling guidance
- duplicated instructions
- excessive instruction size
- missing ownership guidance
- undocumented generated files
- unclear completion criteria

Use:

`VERIFIED`

`ALREADY_RESOLVED`

`NOT_REPRODUCIBLE`

`BLOCKED_BY_MISSING_CONTEXT`

---

# 3. Establish the AI Readiness Invariant

Typical invariant:

> An engineer or coding agent can independently discover the repository's canonical workflow, understand the important architectural and safety boundaries, make a scoped change, and validate that change without relying on undocumented tribal knowledge.

Additional invariants may include:

- all referenced paths exist
- documented commands are executable
- guidance does not contradict repository configuration
- security boundaries are explicit
- validation expectations are clear
- agent instructions point to canonical documentation
- instructions remain concise enough to consume effectively

---

# 4. Discover the Canonical Engineering Interface

Identify where applicable:

`INSTALL_COMMAND`

`DEV_COMMAND`

`TEST_COMMAND`

`LINT_COMMAND`

`TYPECHECK_COMMAND`

`BUILD_COMMAND`

`FORMAT_COMMAND`

`PACKAGE_MANAGER`

`RUNTIME_VERSION`

`APPLICATION_ENTRYPOINTS`

`ARCHITECTURE_DOC`

`CONTRIBUTING_GUIDE`

`CODEOWNERS`

`CI_WORKFLOWS`

`AGENT_GUIDANCE`

Do not invent commands.

If a canonical command cannot be reliably determined:

`NOT_DISCOVERABLE`

---

# 5. Guidance Hierarchy

Prefer:

## Repository-level agent guidance

Contains only high-value instructions required to work safely.

## Canonical technical documentation

Contains detailed setup, architecture, testing, and operational guidance.

## Specialized documentation

Contains component-specific or domain-specific instructions.

Avoid duplicating the same information independently across multiple files.

---

# 6. Instruction Correctness

Validate every material instruction.

Check:

- referenced file paths exist
- referenced directories exist
- commands exist
- script names match repository configuration
- workflow names are correct
- architecture links are valid
- documentation links resolve
- environment-variable references are valid
- described component names still exist

---

# 7. Command Executability

Where possible verify:

- installation
- development startup
- tests
- linting
- type checking
- build
- formatting

Use:

`VERIFIED_EXECUTABLE`

`DISCOVERED_NOT_EXECUTED`

`INVALID`

---

# 8. Repository Navigation

An agent should be able to identify:

- main application components
- important directories
- entry points
- shared libraries
- tests
- configuration
- migrations
- generated code
- infrastructure/deployment code

Do not create exhaustive file maps.

---

# 9. Architectural Boundaries

Identify architectural constraints already expressed by the repository.

Examples:

- dependency direction
- service boundaries
- domain boundaries
- shared-library usage
- controller/service/repository layering
- frontend/backend separation
- generated-code boundaries
- package ownership
- infrastructure boundaries

If intended architecture is genuinely unclear:

`FOLLOW_UP: DESIGN_READINESS`

---

# 10. Change Scope Guidance

Where relevant document:

- avoid unrelated refactoring
- preserve public APIs unless required
- follow existing naming and structure
- use existing abstractions
- do not modify generated files manually
- do not update unrelated dependencies
- do not modify deployment infrastructure for application-only changes

---

# 11. Sensitive Areas

Identify repository areas requiring caution, such as:

- authentication
- authorization
- billing
- secrets
- cryptography
- infrastructure
- production deployment
- database migrations
- public APIs
- data-retention logic
- compliance-related code

Document when human review is expected.

---

# 12. Secrets and Sensitive Data

Determine:

- where environment-variable names are documented
- whether example env files exist
- whether real credentials are prohibited
- where secret configuration belongs
- whether logs may contain sensitive data
- whether production data may be copied into tests

Never add actual secret values.

---

# 13. Generated Files

If generated files exist, document:

- source of generation
- generation command
- whether generated outputs are committed
- how to validate regeneration

---

# 14. Testing Guidance

Reference canonical testing commands.

If no reliable test command exists:

`FOLLOW_UP: TEST_READINESS`

Do not invent a test strategy inside this skill.

---

# 15. CI/CD Guidance

Document only what is useful for change preparation.

If CI does not execute canonical validation:

`FOLLOW_UP: CI_CD_READINESS`

Do not redesign CI/CD from this skill.

---

# 16. Code Review Guidance

Determine whether code-review expectations are discoverable.

Where appropriate document:

- required review areas
- CODEOWNERS expectations
- sensitive-change review
- validation evidence expected in PRs
- migration review expectations
- security review expectations

Do not invent organizational policy.

---

# 17. Definition of Done

A change should typically not be considered complete until:

- implementation is finished
- relevant tests pass
- lint/type-check/build pass where applicable
- documentation is updated when behavior changes
- generated files are regenerated where required
- no secrets were introduced
- scope remains limited to the requested change

Customize based on the repository.

---

# 18. Agent Autonomy Boundaries

## SAFE_TO_PROCEED

Examples:

- localized bug fixes
- tests
- documentation corrections
- small refactors following existing patterns
- broken internal references

## PROCEED_WITH_VALIDATION

Examples:

- build configuration
- test configuration
- dependency updates within established policy
- CI-related repository scripts
- minor runtime behavior changes

## HUMAN_DECISION_REQUIRED

Examples:

- authentication/authorization semantics
- production infrastructure
- destructive migrations
- public API breaking changes
- secrets-management strategy
- architecture changes
- major framework migrations

---

# 19. Documentation Quality

Prefer:

- explicit commands
- clear boundaries
- links to canonical docs
- small tables
- actionable rules

Avoid:

- long architecture essays
- generic coding advice
- duplicated README content
- repeated framework documentation
- low-value generic instructions

---

# 20. Prevent Instruction Drift

Determine which source should be canonical for duplicated facts.

Prefer machine-readable configuration as the source for runtime versions and commands where practical.

---

# 21. Vendor-Neutral Guidance

Where practical, separate repository knowledge from vendor-specific agent behavior.

Vendor-specific files may exist, but should not become the only source of repository knowledge.

---

# 22. Conflicting Instructions

Detect contradictions.

Do not choose arbitrarily.

Use repository evidence to identify the likely canonical source.

If the intended value cannot be determined:

`HUMAN_DECISION_REQUIRED`

---

# 23. Stale References

Find and repair:

- deleted files
- renamed directories
- obsolete scripts
- old workflow names
- invalid anchors
- moved architecture documents
- incorrect command examples

Prefer fixing the reference over creating placeholder files.

---

# 24. Agent-Specific Files

If multiple agent instruction files exist, define clear responsibilities.

Prefer:

shared canonical guidance + small vendor-specific overlays.

---

# 25. Context Efficiency

Prioritize documenting:

- canonical commands
- component map
- architectural boundaries
- sensitive areas
- validation contract
- relevant docs

Do not create massive instruction files.

---

# 26. Self-Verification

Where practical, verify that:

- references point to existing files
- commands map to existing scripts
- referenced workflows exist
- generation commands exist
- linked architecture docs exist

---

# 27. Scope Control

Do not turn AI-readiness remediation into:

- architecture redesign
- testing framework creation
- CI/CD redesign
- dependency modernization
- production-readiness implementation
- broad documentation rewrite

Use follow-ups:

`FOLLOW_UP: TEST_READINESS`

`FOLLOW_UP: CI_CD_READINESS`

`FOLLOW_UP: DESIGN_READINESS`

`FOLLOW_UP: PRODUCTION_READINESS`

---

# 28. Change Safety Classification

## SAFE_AUTOFIX

Examples:

- fixing broken documentation references
- correcting stale command names
- removing obvious contradictory duplicate guidance
- referencing an existing canonical document
- documenting existing safe commands

## AUTOFIX_WITH_VALIDATION

Examples:

- restructuring `AGENTS.md`
- consolidating duplicated guidance
- adding repository-specific completion criteria
- introducing missing security guidance based on existing policy
- reorganizing instruction hierarchy

## HUMAN_DECISION_REQUIRED

Examples:

- deciding architecture policy
- creating security policy
- defining organization-wide review requirements
- deciding supported runtime versions when evidence conflicts
- establishing new production-access rules

---

# 29. Validation

After making AI-readiness changes, verify:

1. referenced files exist
2. documented commands exist
3. documented paths resolve
4. instructions do not materially contradict each other
5. canonical documentation is correctly linked
6. sensitive-data guidance does not expose secrets
7. agent instructions remain concise and usable

Where practical, execute documented commands.

---

# 30. Existing Problems

If documentation references a command that fails, determine whether:

`DOCUMENTATION_ERROR`

`UNDERLYING_REPO_FAILURE`

`ENVIRONMENT_FAILURE`

Route underlying failures to the appropriate readiness domain.

---

# 31. Completion Criteria

AI readiness remediation is complete only when:

1. reported guidance problems were verified
2. material broken references are fixed
3. documented commands reflect repository reality
4. important architecture boundaries are discoverable
5. security and sensitive-data expectations are discoverable
6. validation expectations are clear
7. code-review expectations are discoverable where evidence supports them
8. duplicated or contradictory instructions are reduced
9. human decision boundaries are clear
10. no unsupported organizational policy was invented

---

# 32. Required Output

## AI Readiness Summary

`STATUS=SUCCESS|PARTIAL_SUCCESS|NO_CHANGE_REQUIRED|BLOCKED`

## Before

Describe the verified AI-readiness condition.

## Root Cause

Explain why AI readiness was incomplete.

## AI Readiness Invariant

State the resulting guarantee.

## Instruction Sources

`PRIMARY_AGENT_GUIDANCE=<path|NOT_DISCOVERED>`

`VENDOR_SPECIFIC_GUIDANCE=<paths|NONE>`

`README=<path|NOT_DISCOVERED>`

`CONTRIBUTING=<path|NOT_DISCOVERED>`

`ARCHITECTURE_GUIDANCE=<path|NOT_DISCOVERED>`

`CODEOWNERS=<path|NOT_DISCOVERED>`

## Canonical Engineering Contract

`INSTALL_COMMAND=<command|NOT_DISCOVERED>`

`DEV_COMMAND=<command|NOT_DISCOVERED>`

`TEST_COMMAND=<command|NOT_DISCOVERED>`

`LINT_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`TYPECHECK_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

`BUILD_COMMAND=<command|NOT_APPLICABLE|NOT_DISCOVERED>`

## Changes Applied

For every changed file:

- what changed
- why it changed
- canonical source referenced

## Reference Validation

`BROKEN_REFERENCES_BEFORE=<count>`

`BROKEN_REFERENCES_AFTER=<count>`

`INVALID_COMMANDS_BEFORE=<count>`

`INVALID_COMMANDS_AFTER=<count>`

`CONTRADICTIONS_RESOLVED=<count>`

## Agent Capability Check

`SETUP_DISCOVERABLE=true|false`

`RUN_COMMAND_DISCOVERABLE=true|false`

`TEST_COMMAND_DISCOVERABLE=true|false`

`VALIDATION_DISCOVERABLE=true|false`

`ARCHITECTURE_BOUNDARIES_DISCOVERABLE=true|false`

`SECURITY_BOUNDARIES_DISCOVERABLE=true|false`

`CODE_REVIEW_EXPECTATIONS_DISCOVERABLE=true|false`

`DEFINITION_OF_DONE_DISCOVERABLE=true|false`

## Validation Results

Report exact checks performed.

Distinguish command existence from command execution.

## Human Decisions

List policies or decisions that could not safely be inferred.

## Follow-Ups

List readiness issues outside AI readiness.

---

# 33. Final Verdict

`AI_READINESS_COMPLETE=true|false`

`PRIMARY_GUIDANCE_AVAILABLE=true|false`

`BROKEN_REFERENCES_REMAINING=<count>`

`INVALID_COMMANDS_REMAINING=<count>`

`CONTRADICTIONS_REMAINING=<count>`

`SETUP_DISCOVERABLE=true|false`

`VALIDATION_DISCOVERABLE=true|false`

`ARCHITECTURE_BOUNDARIES_DISCOVERABLE=true|false`

`SECURITY_BOUNDARIES_DISCOVERABLE=true|false`

`HUMAN_DECISIONS_REQUIRED=<count>`

`TEST_READINESS_FOLLOW_UP=true|false`

`CI_CD_READINESS_FOLLOW_UP=true|false`
