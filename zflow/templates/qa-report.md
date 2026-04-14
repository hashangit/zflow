# QA Report

> Produced by ZFlow Phase 5: QA.
> Critical or Blocker findings block progression to Phase 6.

---

## Template Guidance

**Required** = must exist. **Expected** = include unless noted. **Optional** = discretionary.
Scale output to task complexity.

---

## Executive Summary [Required]

- **Gate Decision**: PASS | FAIL
- **Total Findings**: N
- **Loop-back Iterations**: N (0 = first pass)

---

## Severity Breakdown [Required]

| Severity | Count |
|----------|-------|
| **Critical (Security)** | N |
| **Blocker** | N |
| **Major** | N |
| **Minor** | N |
| **Note** | N |

---

## Detailed Findings [Expected]

### QA-001: {Finding Title}

- **Severity**: Critical (Security) | Blocker | Major | Minor | Note
- **Dimension**: Completeness | UX | Code Quality | Test Coverage | Design Alignment | Security | UI Visual
- **Root Cause Layer** (Critical/Blocker only): Implementation | Design | Scope | Unknown
- **Location**: `file:line` or `{component}`
- **Description**: {What was found, why it matters}
- **Remediation**: {Specific fix}
- **Verification**: {How to confirm}

{Continue for each finding. Number sequentially.}

---

## Dimension Summaries [Expected]

{For each dimension that ran, one entry:}

### {Dimension Name}
- **Status**: Pass | Issues Found
- **Key finding**: {Most significant, if any. "None" if clean.}

---

## Gate Decision [Required]

### Decision: PASS | FAIL

{If PASS: note any Major/Minor items to track.}
{If FAIL: list Critical/Blocker findings that must be resolved.}

**If FAIL — Loop-back instructions:**

| Finding ID | Severity | Fix Target | Priority |
|-----------|----------|-----------|----------|
| QA-{NNN} | {Level} | `{file or component}` | {1=highest} |

Security findings prioritized first.

---

## Recommended Actions [Required]

### Before Merge (Critical + Blocker)
1. {Action tied to finding ID}

### Before Next Release (Major)
1. {Action}

### Future (Minor + Note)
1. {Action}

---

## Root Cause Analysis [Expected]

_Required when Critical or Blocker findings exist._

| Root Cause Layer | Count | Finding IDs | Loop-Back Target |
|-----------------|-------|-------------|------------------|
| Implementation | N | QA-{NNN} | Phase 4 |
| Design | N | QA-{NNN} | Phase 2 |
| Scope | N | QA-{NNN} | Phase 0 |
| Unknown | N | QA-{NNN} | User decision |

---

## Appendix: Agent Reports [Optional]

Individual dimension reports at `.zflow/phases/05-qa/dimension-reports/`:
completeness.md, ux.md, code-quality.md, test-coverage.md, design-alignment.md,
security-audit.md{, ui-visual-qa.md if applicable}
