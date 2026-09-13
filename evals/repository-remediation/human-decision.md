# Case: human-decision

## Finding

```
FINDING_ID: RR-004
CATEGORY: api-design
PROBLEM: `POST /v1/orders` accepts an `amount` field as a float, causing rounding errors in downstream
  billing reconciliation.
EVIDENCE: src/routes/orders.ts line 41; docs/api/orders.md documents `amount: number`.
EXPECTED_OUTCOME: Amounts are represented without floating-point rounding error.
SUGGESTED_FIX: Change `amount` to an integer minor-unit (cents) field.
```

## Target repository setup

A public API service where `POST /v1/orders` is documented and versioned (`docs/api/orders.md`,
`openapi.yaml`), with existing integration tests asserting the current float-based request/response
shape. There are no versioning or deprecation conventions in the repo for breaking API changes.

## Expected behavior

- The skill recognizes this as a breaking public API/schema change, not a straightforward bug fix.
- It does not guess at a migration strategy (dual-write, new API version, field aliasing) or silently
  change the wire format.
- It reports `HUMAN_DECISION_REQUIRED`, explains why (breaking change to a public, versioned contract
  with no existing deprecation path), and proposes options without implementing any of them.

## Acceptance criteria

- No production code, OpenAPI spec, or test files are modified.
- The report's Human Decisions section names the specific tradeoff (breaking change vs. additive
  versioned field) and why it can't be resolved unilaterally.
- Final verdict: `REMEDIATION_COMPLETE=false`, `FIXED_FINDINGS=0`, `HUMAN_DECISIONS_REQUIRED=1`,
  `BLOCKED_FINDINGS=0`.
