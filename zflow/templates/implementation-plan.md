# Implementation Plan

_Phase 4 of ZFlow — generated before agent execution._

## Template Guidance

**Required** = must exist. **Expected** = include unless noted. Scale to complexity.

---

## Overview

- **Solution**: `{brief description}`
- **Total tasks**: {N} | **Tiers**: {N} | **UI tasks**: {N}

---

## Dependency Graph [Required]

```
{ASCII visualization}

Example:
  [A: Types] ──┬──> [D: API] ──┬──> [F: Integration]
  [B: DB]     ──┤               └──> [G: E2E Tests]
  [C: Auth]   ──┘
```

---

## Tier Breakdown [Required]

### Tier 0 — Independent

| # | Task | Agent | Complexity | Files |
|---|------|-------|------------|-------|

### Tier 1 — Depends on Tier 0

| # | Task | Agent | Complexity | Deps | Files |
|---|------|-------|------------|------|-------|

{Continue for additional tiers.}

---

## Per-Task Details [Expected]

### Task 1: {Name}

- **Tier**: {N} | **Agent**: {type}
- **Description**: {from solution}
- **Files**: {paths}
- **Success criteria**: {verifiable outcomes}
- **Conventions**: {relevant patterns}
- **UI reference** (if UI): {design report section + tokens}

{Repeat per task.}

---

## Execution Order [Required]

```
Tier 0: [Task A, Task B] — parallel → wait
Tier 1: [Task C (deps: A), Task D (deps: A,B)] — parallel → wait
Tier 2: [Task E (deps: C,D)] → wait
Total agents: {N}
```

---

## Risk Assessment [Optional]

| Risk | Impact | Mitigation |
|------|--------|-----------|
