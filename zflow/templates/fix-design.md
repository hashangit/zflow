# Fix Design

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---


## Root Cause Reference
- **Root cause**: <!-- one-line statement from root-cause.md -->
- **Confidence**: <!-- High/Medium/Low -->
- **Location**: <!-- file:line -->
- **Security impact**: <!-- rating from security-impact-assessor -->

## Proposed Fix
<!-- One paragraph describing the minimal change that addresses the root cause. Explain WHY this fix addresses the cause, not just WHAT changes. -->

## Code Changes

### {file path}
**Change**: <!-- what changes and why -->

**Before**:
```language
// Current (defective) code
```

**After**:
```language
// Fixed code
```

**Justification**: <!-- why this specific change addresses the root cause -->

<!-- Repeat section for each additional file -->

### {file path}
<!-- ... -->

## Regression Risk Assessment
- **Risk level**: <!-- low | medium | high -->
- **Callers of changed functions**: <!-- list code that calls changed functions -->
- **Contract changes**: <!-- any API/behavior/signature changes -->
- **Tests depending on buggy behavior**: <!-- list if any -->
- **New edge cases introduced**: <!-- edge cases the fix creates -->

## Pattern Fix
- **Similar patterns found**: <!-- yes/no — reference pattern scan results -->
- **Fix scope**: <!-- this bug only | same change includes patterns | follow-up PR -->
- **Additional fix locations**: <!-- file:line list if fixing in same change -->
- **Follow-up items**: <!-- if not fixing in same change, list for tracking -->

## Security Review of Fix
- **Addresses security impact?**: <!-- yes/no — explain how -->
- **Introduces new attack surface?**: <!-- yes/no — explain -->
- **Error messages safe?**: <!-- yes/no — no info leakage -->
- **Sensitive data handling correct?**: <!-- yes/no -->
- **Overall fix is security-safe**: <!-- yes/no -->

## Success Criteria
<!-- Karpathy: Goal-Driven. Define verifiable criteria for the fix. -->

1. <!-- Original bug reproduction steps produce correct behavior -->
2. <!-- Full test suite passes -->
3. <!-- Specific edge case X handled correctly -->
4. <!-- No new test failures introduced -->

## Rollback Plan
- **Revert method**: <!-- git revert / manual undo / feature toggle -->
- **Data concerns**: <!-- any data migration or state concerns -->
- **Reversibility**: <!-- fully reversible | partial | irreversible -->
- **Revert test**: <!-- how to verify revert worked -->
