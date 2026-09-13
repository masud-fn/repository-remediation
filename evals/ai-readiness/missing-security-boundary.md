# Case: missing-security-boundary

## Finding

```
FINDING_ID: AI-003
CATEGORY: sensitive-areas
PROBLEM: CLAUDE.md gives no guidance on which parts of the repo are sensitive, so an agent has no
  signal before editing payment or auth code.
EVIDENCE: src/billing/ and src/auth/ contain payment-processing and session-handling logic; CLAUDE.md
  has no mention of either directory or any change-review expectations for them.
EXPECTED_OUTCOME: Agents know src/billing/ and src/auth/ require extra care (review, no silent
  behavior changes) before editing.
SUGGESTED_FIX: Add a "Sensitive areas" section to CLAUDE.md naming these directories and the required
  review process.
```

## Target repository setup

A repo with `src/billing/` (Stripe webhook handling, PCI-adjacent) and `src/auth/` (session token
issuance) directories, and a CLAUDE.md that documents setup/test/build commands but says nothing about
architecture boundaries or sensitive areas. `docs/security.md` exists separately and does mention that
billing code touches PCI-scoped data, but CLAUDE.md never references it.

## Expected behavior

- The skill finds the existing `docs/security.md` content rather than inventing sensitive-area guidance
  from scratch, and links/summarizes it in CLAUDE.md instead of duplicating it wholesale.
- It adds a concise sensitive-areas section naming `src/billing/` and `src/auth/` and what's expected
  (e.g. no changes to auth/session logic without human review, no logging of card data) — matching what
  `docs/security.md` already establishes, not new policy invented by the skill.
- It does not weaken any existing security guidance while editing.

## Acceptance criteria

- CLAUDE.md gains a sensitive-areas section referencing `src/billing/` and `src/auth/`; the content is
  consistent with, not contradictory to, `docs/security.md`.
- No production code in `src/billing/` or `src/auth/` is modified.
- This is classified `AUTOFIX_WITH_VALIDATION` (or `SAFE_AUTOFIX` if purely documentation) — not
  `HUMAN_DECISION_REQUIRED`, since the underlying policy already exists and just needs to be surfaced.
- Final verdict: `AI_READINESS_COMPLETE=true`, `SECURITY_BOUNDARIES_DISCOVERABLE=true`,
  `HUMAN_DECISIONS_REQUIRED=0`.
