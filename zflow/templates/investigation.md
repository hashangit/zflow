# Investigation Report

## Executive Summary
<!-- One-paragraph summary. What did the team find? Where does the bug originate? -->

## Template Guidance

**Required** = must exist. **Expected** = include unless noted. Scale to complexity.

---

## Call Chain Analysis
<!-- From call-chain-tracer agent -->

### Execution Path

| Step | Function | Location (file:line) | Input | Output | Status |
|------|----------|---------------------|-------|--------|--------|

### Divergence Point
<!-- Where behavior first goes wrong -->

### Suspicious Patterns
<!-- Error swallowing, silent coercions, missing error handling -->

---

## Data Flow Analysis
<!-- From data-flow-tracer agent -->

### Bad Data
- **Observed at**: | **Actual**: | **Expected**:

### Data Journey (Origin to Symptom)

| Step | Location | Operation | Data Before | Data After | Correct? |
|------|----------|-----------|-------------|------------|----------|

### Data Corruption Point
<!-- Where data first goes wrong -->

### Storage Boundary Checks
- **DB**: | **Cache**: | **Session/State**: | **Serialization**:

---

## Pattern Scan Results
<!-- From pattern-scanner agent -->

### Defective Pattern
{Description}

### Exact Copies

| # | Location | Same Bug? | Severity |
|---|----------|-----------|----------|

### Blast Radius
- **Affected locations**: | **Critical path**: | **Fix scope**: {single|multiple|systemic}

---

## Git History Findings
<!-- From history-investigator agent -->

### Bug Introduction Point
- **Commit**: | **Date**: | **Confidence**: {high|medium|low}

### Recent Changes to Affected Files

| Commit | Date | Message | Relevant? |
|--------|------|---------|-----------|

---

## Security Impact Assessment
<!-- From security-impact-assessor agent -->

- **Reachable from untrusted input**: {yes/no}
- **Entry points**: {list}
- **Worst-case exploit**: {category + description}
- **Overall rating**: {Critical/High/Medium/Low/None}

---

## Cross-Cutting Observations
{Insights spanning multiple dimensions. Contradictions or confirmations.}
