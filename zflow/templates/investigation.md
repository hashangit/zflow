# Investigation Report

## Executive Summary
<!-- One-paragraph summary of investigation findings. What did the team find? Where does the bug originate? -->

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---

---

## Call Chain Analysis
<!-- From call-chain-tracer agent -->

### Execution Path

| Step | Function | Location (file:line) | Input | Output | Status |
|------|----------|---------------------|-------|--------|--------|
| 1    |          |                     |       |        | ok     |

### Divergence Point
<!-- Where behavior first goes wrong -->

### Suspicious Patterns in Chain
<!-- Error swallowing, silent coercions, missing error handling -->

---

## Data Flow Analysis
<!-- From data-flow-tracer agent -->

### Bad Data Identification
- **Observed at**:
- **Actual value**:
- **Expected value**:

### Data Journey (Origin to Symptom)

| Step | Location (file:line) | Operation | Data Before | Data After | Correct? |
|------|---------------------|-----------|-------------|------------|----------|
| 1    |                     |           |             |            |          |

### Data Corruption Point
<!-- Where data first goes wrong -->

### Storage Boundary Checks
- **Database**:
- **Cache**:
- **Session/State**:
- **Serialization**:

---

## Pattern Scan Results
<!-- From pattern-scanner agent -->

### Defective Pattern
<!-- Description of the pattern that contains the bug -->

### Exact Copies Found

| # | Location (file:line) | Same Bug? | Severity | Context |
|---|---------------------|-----------|----------|---------|
| 1 |                     |           |          |         |

### Structurally Similar Code

| # | Location (file:line) | Similar Pattern | Same Risk? | Notes |
|---|---------------------|----------------|------------|-------|
| 1 |                     |                |            |       |

### Shared Utility Analysis
- **Utility**:
- **Total callers**:
- **Is utility itself buggy?**:

### Blast Radius
- **Total affected locations**:
- **Critical path affected**:
- **Estimated fix scope**: <!-- single location | multiple locations | systemic -->

---

## Git History Findings
<!-- From history-investigator agent -->

### Recent Changes to Affected Files

| Commit | Date | Message | Files Changed | Relevant? |
|--------|------|---------|---------------|-----------|
|        |      |         |               |           |

### Bug Introduction Point
- **Commit**:
- **Date**:
- **Change description**:
- **Confidence**: <!-- high | medium | low -->

### Related Changes
<!-- Other commits around the same time that may be connected -->

---

## Security Impact Assessment
<!-- From security-impact-assessor agent -->

### Attack Reachability
- **Reachable from untrusted input**:
- **Entry points**:
- **Authentication required**:

### Worst-Case Exploit
- **Category**:
- **Description**:

### Overall Security Impact Rating
<!-- Critical | High | Medium | Low | None -->

---

## Cross-Cutting Observations
<!-- Insights that span multiple investigation dimensions. Contradictions or confirmations between findings. Notable patterns that don't fit neatly into one dimension. -->
