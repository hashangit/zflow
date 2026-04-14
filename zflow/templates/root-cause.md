# Root Cause Analysis

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---


## Symptom Description
<!-- What the user observes: error message, wrong output, crash behavior. Be specific and factual. -->

## Root Cause Statement
<!-- One clear sentence: "The root cause is {specific defect} at {file:line}, which exists because {why}." -->

## Causal Chain
<!-- Step-by-step from root cause to symptom. Each link must be supported by investigation evidence. -->

1. **Root Cause**: <!-- specific defect at file:line -->
   - Why: <!-- why this defect exists -->
   - Evidence: <!-- what investigation found -->

2. **Intermediate Effect**: <!-- what happens because of the root cause -->
   - Why: <!-- how root cause produces this -->
   - Evidence: <!-- supporting evidence -->

3. **Symptom**: <!-- what the user observes -->
   - Why: <!-- how the chain produces this symptom -->
   - Evidence: <!-- supporting evidence -->

## Defect Location
- **File**: <!-- path to file -->
- **Line(s)**: <!-- line numbers -->
- **Function/Method**: <!-- function name -->
- **Code**: <!-- exact defective code snippet -->

```python
# Defective code here
```

## Why It Exists
<!-- Category and explanation -->
- **Category**: <!-- misunderstanding | race-condition | missing-check | wrong-assumption | copy-paste-error | incomplete-refactoring | missing-error-handling | logic-error | configuration-error | other -->
- **Explanation**: <!-- why this defect was introduced. What was the developer thinking? What assumption was wrong? -->

## Blast Radius
- **Directly affected**: <!-- code paths that definitely exhibit the bug -->
- **Potentially affected**: <!-- code paths that may be affected (from pattern scan) -->
- **Estimated scope**: <!-- single location | module | cross-cutting -->
- **Critical paths affected**: <!-- auth, payments, data integrity — if any -->

## Security Implications
- **Security impact rating**: <!-- from security-impact-assessor -->
- **Root cause creates vulnerability**: <!-- yes/no with explanation -->
- **Fix must address**: <!-- specific security requirements for the fix -->

## Confidence Level
- **Level**: <!-- High | Medium | Low -->
- **Justification**: <!-- why this confidence level -->
- **Uncertainties**: <!-- what remains uncertain -->

## Recommended Investigation
<!-- Only fill this section if confidence is Low. What additional steps would increase confidence? -->

- [ ] <!-- Additional investigation step 1 -->
- [ ] <!-- Additional investigation step 2 -->
