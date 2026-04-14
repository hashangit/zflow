# Solution Design

> Produced by ZFlow Phase 2: Design.
> Input: scope.md (requirements) + research-report.md (codebase analysis).
> This document is the contract for implementation. Every section was user-approved.

---

## Template Guidance

This template provides a recommended structure. Sections marked **Required** must
be present — downstream phases depend on them. Sections marked **Expected** should
be present unless you note a reason for omission. Sections marked **Optional** are
suggestions — include, restructure, or omit as the task demands. Produce output
proportional to complexity.

---

## Chosen Approach [Required]

**Approach:** {Name}

**Rationale:** {Why this approach was selected over alternatives. Tied to research findings
and scope constraints. Explicitly notes if this is the simplest viable approach.}

---

## Alternatives Considered [Optional]

### {Alternative A Name}
- **Summary:** {One paragraph}
- **Why rejected:** {Specific reason — effort too high, doesn't fit codebase, risk too great,
  unnecessary complexity, etc.}

### {Alternative B Name}
- **Summary:** {One paragraph}
- **Why rejected:** {Specific reason}

---

## Architecture Overview [Required]

{High-level structure of the solution. How it fits into the existing system.
Key design decisions and their rationale. Diagrams or descriptions as appropriate.

Scaled to complexity: a few sentences if straightforward, up to 200-300 words if nuanced.}

---

## Component Breakdown [Required]

### {Component 1 Name} ({New | Modified})
- **Responsibility:** {What this component does}
- **Files affected:** {Paths}
- **Key decisions:** {Any non-obvious choices with rationale}

### {Component 2 Name} ({New | Modified})
- **Responsibility:** {What this component does}
- **Files affected:** {Paths}
- **Key decisions:** {Any non-obvious choices with rationale}

{Continue for each component.}

---

## Data Flow [Expected]

{How data moves through the system end-to-end. State management approach.
Input/output contracts between components. What gets persisted and where.

Scaled to complexity.}

---

## Error Handling & Edge Cases [Expected]

### Failure Modes
| Component | Failure | Recovery | User Impact |
|-----------|---------|----------|-------------|
| {Component} | {What fails} | {How it recovers} | {What user sees} |

### Edge Cases
- {Edge case 1}: {Handling strategy}
- {Edge case 2}: {Handling strategy}

---

## Testing Strategy [Expected]

### Test Categories
| Category | Scope | Priority | Approach |
|----------|-------|----------|----------|
| Unit | {What's tested} | {Must/Should/Nice} | {How} |
| Integration | {What's tested} | {Must/Should/Nice} | {How} |
| E2E | {What's tested} | {Must/Should/Nice} | {How} |

### Critical Path Tests
- {Test 1}: Verifies {behavior}
- {Test 2}: Verifies {behavior}

### Edge Case Tests
- {Test 1}: Verifies {edge case behavior}

---

## [If UI: Interface Design] [Optional]

> This section is included only when scope.md has ui_work: true.

### Component Hierarchy
```
{Parent Component}
├── {Child Component A}
│   ├── {Sub-component}
│   └── {Sub-component}
└── {Child Component B}
    └── {Sub-component}
```

### User Interactions
| Interaction | Trigger | State Change | Component Response |
|-------------|---------|--------------|-------------------|
| {Action} | {User does X} | {State updates} | {Component re-renders / navigates} |

### Responsive Behavior
- **Desktop:** {Layout description}
- **Tablet:** {Layout changes}
- **Mobile:** {Layout changes}

### Design-to-Code Mapping
| Design Element | Code Construct | Design Token |
|----------------|---------------|--------------|
| {Button style} | {Component path} | {Token name} |

---

## Task Breakdown [Required]

### Dependency Graph
```
Tier 0 (no dependencies):
  - Task A
  - Task B

Tier 1 (depends on Tier 0):
  - Task C (depends on: Task A)
  - Task D (depends on: Task A, Task B)

Tier 2 (depends on Tier 0+1):
  - Task E (depends on: Task C, Task D)
```

### Task Details

#### Task 1: {Name}
- **Description:** {What needs to be done}
- **Files:** {Paths to create or modify}
- **Dependencies:** {Which tasks must complete first}
- **Tier:** {0/1/2/...}
- **Complexity:** {S/M/L}
- **Success Criteria:**
  - {Criterion 1 — verifiable}
  - {Criterion 2 — verifiable}

#### Task 2: {Name}
- **Description:** {What needs to be done}
- **Files:** {Paths}
- **Dependencies:** {Prerequisites}
- **Tier:** {0/1/2/...}
- **Complexity:** {S/M/L}
- **Success Criteria:**
  - {Criterion 1 — verifiable}
  - {Criterion 2 — verifiable}

{Continue for each task.}

---

## Risk Register [Expected]

| # | Risk | Likelihood | Impact | Mitigation | Raised During |
|---|------|-----------|--------|------------|---------------|
| R1 | {Description} | {Low/Med/High} | {Low/Med/High} | {Strategy} | {Which section review} |
| R2 | {Description} | {Low/Med/High} | {Low/Med/High} | {Strategy} | {Which section review} |

---

## Open Questions

- {Question 1}: {Context / what needs to be decided / by when}
- {Question 2}: {Context / what needs to be decided / by when}

{Leave empty if no open questions remain. Do not fabricate questions.}
