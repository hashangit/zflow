# Implementation Report

_Phase 4 of ZFlow -- generated after all tiers complete._

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total tasks | {N} |
| Completed | {N} |
| Partially completed | {N} |
| Failed | {N} |
| Skipped | {N} |
| Tiers executed | {N} |
| Agents spawned | {N} |
| Total files modified | {N} |
| Total files created | {N} |
| Deviations from design | {N} |
| Ready for QA | Yes / No |

**Summary**: {One-paragraph overview of what was implemented and the current
state.}

---

## Per-Task Reports

### Task 1: {Task Name}

- **Status**: COMPLETE | PARTIAL | FAILED
- **Tier**: {N}
- **Agent type**: focused-implementer | ui-implementer

#### Files Changed

| File | Action | Description |
|------|--------|-------------|
| `{path}` | created | {what was added} |
| `{path}` | modified | {what was changed} |

#### Success Criteria

| Criterion | Status | Evidence |
|-----------|--------|----------|
| {criterion 1} | PASS | {how verified} |
| {criterion 2} | PASS | {how verified} |
| {criterion 3} | FAIL | {what is missing} |

#### Deviations from Design

{If none: "None -- implemented exactly as specified."}

| Deviation | Justification |
|-----------|--------------|
| {what differed} | {why it was necessary} |

#### Verification

- Existing tests: {pass/fail/not run}
- New tests added: {yes/no, details}
- Manual verification: {what was checked}

### Task 2: {Task Name}

<!-- Repeat per-task section for each task -->

---

## Integration Notes

_How the results from each tier compose together._

### Tier 0 Results
{How the independent tasks' outputs relate to each other. Any integration
concerns between parallel tasks.}

### Tier 1 Results
{How Tier 1 tasks built on Tier 0 outputs. Any mismatches or adjustments
needed.}

### Tier 2 Results
{Continue for each tier.}

### Cross-Tier Composition
{Overall assessment of how all tiers' outputs fit together. Any integration
issues discovered during tier transitions.}

---

## Deviation Summary

_Aggregate view of all deviations from the reviewed solution across all tasks._

| Task | Deviation | Justification | Impact |
|------|-----------|--------------|--------|
| {task} | {what differed} | {why} | {scope of impact} |

**Total deviations**: {N}

If total deviations > 0, each deviation must satisfy the Karpathy Surgical
Changes constraint: the change was necessary, minimal, and no simpler
alternative existed.

---

## Outstanding Issues

_Issues that were not resolved during implementation._

| # | Issue | Severity | Blocking? | Task |
|---|-------|----------|-----------|------|
| 1 | {description} | blocker/major/minor | yes/no | {which task} |

---

## Issues Found Outside Scope

_Problems discovered by implementation agents in adjacent code that were not
part of their assigned tasks._

| # | Issue | Location | Reported By |
|---|-------|----------|-------------|
| 1 | {description} | `{file:line}` | {agent/task} |

These issues were observed but NOT fixed (Karpathy: report, don't fix outside
scope). They should be triaged separately.

---

## Ready for QA

**Verdict**: {Yes / No}

**Reasoning**: {Why the implementation is or is not ready for the QA phase.
Consider: are all tasks complete? Are there blocking issues? Are deviations
acceptable?}

### If Yes:
All tasks are complete or have acceptable partial completion. Deviations are
documented and justified. The codebase is in a testable state.

### If No:
{List what needs to happen before QA can proceed. Specific blockers,
incomplete tasks, or issues that must be resolved first.}

---

## Phase Metadata

```json
{
  "phase": "implement",
  "status": "{complete|partial|failed}",
  "started_at": "{timestamp}",
  "completed_at": "{timestamp}",
  "total_tasks": N,
  "tasks_completed": N,
  "tasks_partial": N,
  "tasks_failed": N,
  "tiers_executed": N,
  "agents_spawned": N,
  "files_modified": N,
  "files_created": N,
  "deviations_count": N,
  "ready_for_qa": true|false
}
```
