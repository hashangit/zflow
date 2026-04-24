# Solution Design

> Produced by ZFlow Phase 2: Design.
> Input: scope.md (requirements) + research-report.md (codebase analysis).
> This document is the contract for implementation. Every section was user-approved.

---

## Template Guidance

**Required** = must exist. **Expected** = include unless noted. **Optional** = discretionary.
Scale output to task complexity — a few sentences if straightforward, more detail if nuanced.

---

## Chosen Approach [Required]

**Approach:** {Name}

**Rationale:** {Why selected. Tied to research findings and scope. Notes if simplest viable.}

---

## Alternatives Considered [Optional]

### {Alternative A}
- **Summary:** {One paragraph}
- **Why rejected:** {Reason}

---

## Architecture Overview [Required]

{High-level structure. How it fits into existing system. Key decisions and rationale.
Scaled to complexity.}

---

## Component Breakdown [Required]

### {Component 1} ({New | Modified})
- **Responsibility:** {What it does}
- **Files:** {Paths}
- **Key decisions:** {Non-obvious choices}

{Repeat per component.}

---

## Data Flow [Expected]

{How data moves end-to-end. State management. Input/output contracts between components.}

---

## Error Handling & Edge Cases [Expected]

### Failure Modes
| Component | Failure | Recovery | User Impact |
|-----------|---------|----------|-------------|

### Edge Cases
- {Case}: {Handling}

---

## Testing Strategy [Expected]

| Category | Scope | Priority | Approach |
|----------|-------|----------|----------|
| Unit | {What} | Must/Should | {How} |
| Integration | {What} | Must/Should | {How} |

### Critical Path Tests
- {Test}: Verifies {behavior}

---

## [If UI: Interface Design] [Optional]

> Only when scope.md has ui_work: true.

### Component Hierarchy
{Tree structure of components}

### User Interactions
| Interaction | Trigger | State Change | Response |
|-------------|---------|--------------|----------|

### Design-to-Code Mapping
| Design Element | Code Construct | Token |
|----------------|---------------|-------|

---

## Task Breakdown [Required]

### Dependency Graph
```
Tier 0: [Task A, Task B]
Tier 1: [Task C (deps: A), Task D (deps: A, B)]
Tier 2: [Task E (deps: C, D)]
```

### Task Details

#### Task 1: {Name}
- **Description:** {What}
- **Files:** {Paths}
- **Dependencies:** {Prerequisites}
- **Tier:** {N} | **Complexity:** {S/M/L}
- **Success Criteria:** {verifiable outcomes}

{Repeat per task.}

---

## Risk Register [Expected]

| # | Risk | Likelihood | Impact | Mitigation |
|---|------|-----------|--------|------------|

---

## Open Questions

- {Question}: {Context}
{Leave empty if none. Don't fabricate.}
