# Implementation Plan

_Phase 4 of ZFlow -- generated before agent execution._

---

## Overview

- **Solution**: `{brief description from reviewed-solution.md}`
- **Total tasks**: {N}
- **Total tiers**: {N}
- **UI tasks**: {N} (agents: `ui-implementer`)
- **Non-UI tasks**: {N} (agents: `focused-implementer`)

---

## Dependency Graph

```
{ASCII visualization of the task dependency graph}

Example:
  [A: Types] ──┬──> [D: API Layer] ──┬──> [F: Integration]
  [B: DB]     ──┤                     │
  [C: Auth]   ──┘                     └──> [G: E2E Tests]
               └──> [E: UI Components]──> [H: Polish]
```

---

## Tier Breakdown

### Tier 0 -- Independent Tasks (no dependencies)

| # | Task | Agent Type | Complexity | Estimated Files |
|---|------|-----------|------------|-----------------|
| 1 | {task name} | focused-implementer | S/M/L | {count} |
| 2 | {task name} | ui-implementer | S/M/L | {count} |

### Tier 1 -- Depends on Tier 0

| # | Task | Agent Type | Complexity | Dependencies | Estimated Files |
|---|------|-----------|------------|-------------|-----------------|
| 3 | {task name} | focused-implementer | S/M/L | {task refs} | {count} |

### Tier 2 -- Depends on Tier 0-1

| # | Task | Agent Type | Complexity | Dependencies | Estimated Files |
|---|------|-----------|------------|-------------|-----------------|
| 4 | {task name} | focused-implementer | S/M/L | {task refs} | {count} |

<!-- Continue for additional tiers as needed -->

---

## Per-Task Details

### Task 1: {Task Name}

- **Tier**: {N}
- **Agent type**: focused-implementer | ui-implementer
- **Description**: {task description from solution}
- **Design section**: {which section of reviewed-solution.md this maps to}
- **Input files**:
  - `{path/to/existing/file}` (modify)
  - `{path/to/new/file}` (create)
- **Success criteria**:
  - [ ] {criterion 1}
  - [ ] {criterion 2}
  - [ ] {criterion 3}
- **Coding conventions**: {relevant patterns from research}
- **Test patterns**: {how to test this, from research}
- **UI design reference** (if UI task):
  - Design report section: {section reference}
  - Exported screenshots: {file paths}
  - Design tokens: {which tokens apply}
  - Component specs: {spec reference}

### Task 2: {Task Name}

<!-- Repeat per-task details for each task -->

---

## Execution Order

```
Phase 1: Tier 0
  ├── Agent 1 (Task 1) ──> report
  ├── Agent 2 (Task 2) ──> report
  └── Agent 3 (Task 3) ──> report
  Wait for all Tier 0 agents to complete.

Phase 2: Tier 1
  ├── Agent 4 (Task 4) ──> report
  └── Agent 5 (Task 5) ──> report
  Wait for all Tier 1 agents to complete.

Phase 3: Tier 2
  └── Agent 6 (Task 6) ──> report
  Wait for completion.

Total agents: {N}
Estimated wall-clock phases: {N} (one per tier)
```

---

## Parallelization Strategy

### Within Each Tier
- All tasks in the same tier are spawned simultaneously in a single
  parallel agent block.
- Each agent receives only its task context -- no cross-task awareness.
- Agents do not share state. All coordination happens through the
  coordinator.

### Between Tiers
- Tier N+1 does not begin until all Tier N tasks have completed (or failed
  with documented justification).
- Failed tasks are assessed for downstream impact before the next tier
  starts.

### Agent Capacity
- Maximum parallel agents: {from config, default 5}
- If a tier has more tasks than the maximum, tasks are batched into groups
  that fit within the limit, processing groups sequentially within the tier.

---

## Risk Assessment

| Risk | Impact | Mitigation |
|------|--------|-----------|
| {potential issue} | {what happens} | {how to handle it} |

---

## Notes

{Any additional context, decisions, or caveats about the implementation plan.}
