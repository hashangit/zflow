# QA Report

> Produced by ZFlow Phase 5: QA.
> Input: reviewed-solution.md + impl-report.md + actual code changes.
> This document is the gate for Phase 6. Critical or Blocker findings block progression.

---

## Executive Summary

- **Gate Decision**: PASS | FAIL
- **Total Findings**: N
- **Security Agent Deployed**: Yes | No
- **UI Visual QA Deployed**: Yes | No
- **Loop-back Iterations**: N (0 = first pass)

---

## Severity Breakdown

| Severity | Count | Description |
|----------|-------|-------------|
| **Critical (Security)** | N | Security vulnerability -- must fix immediately |
| **Blocker** | N | Must fix before merge |
| **Major** | N | Should fix; creates technical debt if not |
| **Minor** | N | Nice to fix; cosmetic or stylistic |
| **Note** | N | Observation for future consideration |

---

## Detailed Findings

### QA-001: {Finding Title}

- **Severity**: Critical (Security) | Blocker | Major | Minor | Note
- **Dimension**: Completeness | UX | Code Quality | Test Coverage | Design Alignment | Security | UI Visual
- **Description**: {What was found, why it matters}
- **Location**: `file:line` or `{component/module}`
- **Remediation**: {Specific action to fix}
- **Verification**: {How to confirm the fix works}

### QA-002: {Finding Title}

- **Severity**: {Level}
- **Dimension**: {Dimension}
- **Description**: {What was found}
- **Location**: `file:line`
- **Remediation**: {Fix}
- **Verification**: {Check}

{Continue for each finding. Number sequentially across all dimensions.}

---

## Dimension Summaries

### Completeness Check
- **Status**: Pass | Issues Found
- **Tasks verified**: N complete / N partial / N missing
- **Key finding**: {Most significant, if any}

### UX Review
- **Status**: Pass | Issues Found
- **APIs reviewed**: N
- **Error paths reviewed**: N
- **Key finding**: {Most significant, if any}

### Code Quality (Karpathy Enforcement)
- **Status**: Pass | Issues Found
- **Files reviewed**: N
- **Karpathy violations**: N (scope trace failures / speculative code / unnecessary abstractions / non-surgical changes)
- **Key finding**: {Most significant, if any}

### Test Coverage
- **Status**: Pass | Issues Found
- **Units with tests**: N / N total
- **Estimated coverage**: High | Medium | Low
- **Key finding**: {Most significant, if any}

### Design Alignment
- **Status**: Pass | Issues Found
- **Components aligned**: N / N total
- **Unjustified deviations**: N
- **Key finding**: {Most significant, if any}

### Security Audit
- **Status**: Pass | Issues Found
- **OWASP categories reviewed**: 10/10
- **Findings by severity**: Critical: N / High: N / Medium: N / Low: N / Info: N
- **Key finding**: {Most significant, if any}
- **Full report**: See `dimension-reports/security-audit.md`

### UI Visual QA (Conditional)
- **Status**: Pass | Issues Found | Not Applicable
- **Components verified**: N
- **Design token compliance**: N% compliant
- **Key finding**: {Most significant, if any}

---

## Gate Decision

### Decision: PASS | FAIL

**Reasoning:**
{Why the gate passes or fails. If PASS, note any Major/Minor items that should
be tracked. If FAIL, list the specific Critical/Blocker findings that must be
resolved before proceeding.}

**If FAIL -- Loop-back instructions:**

| Finding ID | Severity | Fix Target | Priority |
|-----------|----------|-----------|----------|
| QA-{NNN} | {Level} | `{file or component}` | {1 = highest} |
| QA-{NNN} | {Level} | `{file or component}` | {2} |

**Security findings are always prioritized first.**

---

## Recommended Actions

### Before Merge (Critical + Blocker)
1. {Specific action tied to a finding ID}
2. {Specific action}

### Before Next Release (Major)
1. {Specific action}
2. {Specific action}

### Future Consideration (Minor + Note)
1. {Specific action}
2. {Specific action}

---

## Appendix: Agent Reports

Individual dimension reports are available at:
- `.zflow/phases/05-qa/dimension-reports/completeness.md`
- `.zflow/phases/05-qa/dimension-reports/ux.md`
- `.zflow/phases/05-qa/dimension-reports/code-quality.md`
- `.zflow/phases/05-qa/dimension-reports/test-coverage.md`
- `.zflow/phases/05-qa/dimension-reports/design-alignment.md`
- `.zflow/phases/05-qa/dimension-reports/security-audit.md`
- `.zflow/phases/05-qa/dimension-reports/ui-visual-qa.md` (if applicable)
