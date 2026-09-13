# Case: already-resolved

## Finding

```
FINDING_ID: RR-001
CATEGORY: dependency
PROBLEM: package.json pins `left-pad` to a version with a known vulnerability (CVE-2024-XXXX).
EVIDENCE: package.json line 14 shows "left-pad": "1.1.0".
EXPECTED_OUTCOME: Vulnerable dependency version is no longer present.
SUGGESTED_FIX: Bump left-pad to >=1.3.0.
```

## Target repository setup

A small Node.js repo where `package.json` and `package-lock.json` already pin `left-pad` to `1.3.0`
(the fix has already shipped in a prior commit). The finding's evidence is stale.

## Expected behavior

- The skill re-reads `package.json`/`package-lock.json` before touching anything and discovers the
  version is already fixed.
- No files are modified.
- The finding is reported as `ALREADY_RESOLVED`, not silently dropped.

## Acceptance criteria

- No diff is produced against the target repository.
- The finding's result block reports `ALREADY_RESOLVED` with the evidence that shows the current,
  already-fixed version.
- Final verdict: `REMEDIATION_COMPLETE=true`, `FIXED_FINDINGS=0`, `ALREADY_RESOLVED=1`,
  `BLOCKED_FINDINGS=0`, `HUMAN_DECISIONS_REQUIRED=0`.
