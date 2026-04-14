# Implementation Report

_Phase 4 of ZFlow — generated after all tiers complete._

## Template Guidance

**Required** = must exist. **Expected** = include unless noted. **Optional** = discretionary.
Scale output to task complexity.

---

## Executive Summary [Required]

| Metric | Value |
|--------|-------|
| Total tasks | {N} |
| Completed | {N} |
| Partial / Failed | {N} / {N} |
| Tiers executed | {N} |
| Files changed | {N} |
| Deviations from design | {N} |
| Ready for QA | Yes / No |

**Summary**: {One sentence on what was implemented and current state.}

---

## Per-Task Reports [Required]

### Task 1: {Task Name}

- **Status**: COMPLETE | PARTIAL | FAILED
- **Tier**: {N}

#### Files Changed

| File | Action | Description |
|------|--------|-------------|
| `{path}` | created/modified | {what} |

#### Success Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| {criterion} | PASS/FAIL | {how verified} |

#### Deviations from Design

{If none: "None." Otherwise:}

| Deviation | Justification |
|-----------|--------------|
| {what differed} | {why} |

### Task 2: {Task Name}

{Repeat per task.}

---

## Integration Notes [Expected]

{How tiers compose together. Note mismatches or adjustments between tiers.
Skip if single-tier.}

---

## Deviation Summary [Expected]

| Task | Deviation | Justification | Impact |
|------|-----------|--------------|--------|
| {task} | {what differed} | {why} | {scope} |

Total deviations: {N}. Each must satisfy Karpathy Surgical Changes.

---

## Outstanding Issues

| # | Issue | Severity | Blocking? | Task |
|---|-------|----------|-----------|------|
| 1 | {description} | blocker/major/minor | yes/no | {task} |

---

## Ready for QA [Required]

**Verdict**: {Yes / No}

{If No: what must happen before QA.}

---

## Phase Metadata

```json
{
  "phase": "implement",
  "status": "{complete|partial|failed}",
  "total_tasks": N,
  "tasks_completed": N,
  "tiers_executed": N,
  "files_changed": N,
  "deviations_count": N,
  "ready_for_qa": true|false
}
```
