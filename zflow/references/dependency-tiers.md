# Dependency Tiers Reference

How implementation tasks are organized into dependency tiers for parallel execution.

---

## Overview

ZFlow's implementation phase (Phase 4) uses a tiered dependency system to maximize parallelism while respecting task ordering. Tasks with no dependencies run first (Tier 0), then tasks that depend on Tier 0 run next (Tier 1), and so on. Within each tier, all tasks execute in parallel.

---

## How the Dependency Graph Is Built

### Source: Task Breakdown in solution.md

During Phase 2 (Design), the solution architect produces a task breakdown that includes:

1. **Task list** -- each task has an ID, description, and complexity estimate (S/M/L)
2. **Dependency declarations** -- each task lists which other tasks it depends on
3. **Success criteria** -- verifiable conditions for each task

Example task breakdown:

```markdown
## Tasks

### T1: Create User model
- Complexity: S
- Dependencies: none
- Success criteria: User model exists with required fields, migrations run cleanly

### T2: Create Auth middleware
- Complexity: M
- Dependencies: none
- Success criteria: Middleware validates JWT, rejects invalid tokens

### T3: Create UserService
- Complexity: M
- Dependencies: T1 (User model)
- Success criteria: CRUD operations work, validation enforced

### T4: Create User endpoints
- Complexity: M
- Dependencies: T3 (UserService), T2 (Auth middleware)
- Success criteria: All endpoints respond correctly, auth enforced

### T5: Create User tests
- Complexity: S
- Dependencies: T4 (User endpoints)
- Success criteria: Tests cover all endpoints, edge cases, error paths
```

### Building the Graph

The implementation coordinator reads the task breakdown and builds a directed acyclic graph (DAG):

1. Create a node for each task
2. Create edges from dependencies (T3 depends on T1 means edge T1 -> T3)
3. Validate the graph (check for cycles -- see Circular Dependencies below)
4. Compute tiers via topological ordering

---

## How Tasks Are Assigned to Tiers

The tier assignment follows a simple rule:

- **Tier 0:** Tasks with no dependencies (in-degree = 0)
- **Tier 1:** Tasks whose dependencies are all in Tier 0
- **Tier 2:** Tasks whose dependencies are all in Tier 0 or Tier 1
- **Tier N:** Tasks whose dependencies are all in tiers < N

### Formal Algorithm

```
remaining = all tasks
tier = 0

while remaining is not empty:
    tier_tasks = tasks in remaining with all dependencies already assigned
    assign tier_tasks to current tier
    remove tier_tasks from remaining
    tier = tier + 1
```

### Example Assignments

#### Simple Example (3 tasks, 2 tiers)

```
Tasks: Create Model (T1), Create Service (T2), Create Endpoints (T3)
Dependencies: T2 -> T1, T3 -> T2

Tier 0: [T1]           (no dependencies)
Tier 1: [T2]           (depends on T1, which is in Tier 0)
Tier 2: [T3]           (depends on T2, which is in Tier 1)
```

#### Moderate Example (5 tasks, 3 tiers)

```
Tasks:
  T1: Create User model       (no deps)
  T2: Create Auth middleware   (no deps)
  T3: Create UserService      (deps: T1)
  T4: Create User endpoints   (deps: T2, T3)
  T5: Create User tests       (deps: T4)

Tier 0: [T1, T2]      (no dependencies -- run in parallel)
Tier 1: [T3]           (depends on T1 in Tier 0)
Tier 2: [T4]           (depends on T2 in Tier 0 and T3 in Tier 1)
Tier 3: [T5]           (depends on T4 in Tier 2)
```

#### Complex Example (8 tasks, 3 tiers)

```
Tasks:
  T1: Database schema         (no deps)
  T2: Migration scripts       (deps: T1)
  T3: User model              (deps: T1)
  T4: Auth service            (no deps)
  T5: Email service           (no deps)
  T6: User service            (deps: T3, T2)
  T7: Notification service    (deps: T5, T6)
  T8: API endpoints           (deps: T4, T6, T7)

Tier 0: [T1, T4, T5]  (no dependencies -- all run in parallel)
Tier 1: [T2, T3]       (T2 depends on T1; T3 depends on T1 -- both Tier 0)
Tier 2: [T6]           (depends on T2, T3 -- both in Tier 1)
Tier 3: [T7]           (depends on T5 in Tier 0, T6 in Tier 2)
Tier 4: [T8]           (depends on T4 in Tier 0, T6 in Tier 2, T7 in Tier 3)
```

---

## How Parallel Execution Works Within a Tier

### Spawning

When a tier is ready to execute:

1. The coordinator identifies all tasks in the current tier
2. For each task, the coordinator prepares the agent input:
   - The specific task description and success criteria
   - Relevant sections of the reviewed solution design
   - File paths to work on (from research phase)
   - Coding conventions (from pattern analysis)
   - Related test patterns (from test survey)
   - The Karpathy preamble (surgical changes constraint)
   - If UI task: the relevant section of ui-design-report.md
3. All agents for the tier are spawned simultaneously in a single tool-use block
4. The coordinator respects `max_parallel_agents` -- if there are more tasks than the limit, tasks are batched

### Waiting

The coordinator waits for ALL tasks in the current tier to complete before proceeding to the next tier. This is a hard barrier -- even if 4 out of 5 tasks in Tier 1 complete quickly, Tier 2 cannot start until the 5th task finishes.

### Failure Handling

If a task fails in a tier:

1. The coordinator logs the failure
2. Tasks in subsequent tiers that depend on the failed task are marked as blocked
3. Tasks in subsequent tiers that do NOT depend on the failed task proceed normally
4. The impl-report.md notes which tasks were blocked and why
5. The user is informed at the QA gate

---

## Handling Circular Dependencies

### Detection

When building the dependency graph, the coordinator checks for cycles. If task A depends on task B and task B depends on task A, this is a circular dependency and the graph is invalid.

### Resolution Strategies

**Strategy 1: Merge Tasks**

If two tasks have a circular dependency, they may need to be a single task. The implementation coordinator flags this and suggests merging.

Example: If "Create UserService" depends on "Create UserRepository" and vice versa, they should likely be one task: "Create User data layer."

**Strategy 2: Break the Cycle with an Interface**

Introduce an abstraction boundary. Task A depends on an interface, Task B implements the interface. They can be built independently if the interface is agreed upon first.

Example:
- T1: Define IUserRepository interface (Tier 0)
- T2: Create UserRepository implementing IUserRepository (Tier 1)
- T3: Create UserService depending on IUserRepository (Tier 1)

Now T2 and T3 can run in parallel since they both depend only on T1.

**Strategy 3: Sequential Execution**

If the cycle cannot be broken, the tasks must run sequentially. The coordinator splits the cycle by picking a start point and running the tasks one after another.

### User Notification

If circular dependencies are detected, the coordinator:
1. Reports the cycle (which tasks are involved)
2. Suggests one or more resolution strategies
3. Asks the user to confirm the resolution approach
4. This is treated as a soft gate -- the user is consulted even if the implement gate is set to auto

---

## Tier Visualization

For complex implementations, the coordinator can produce a visual representation of the tier structure:

```
Tier 0  ────────────────────────────────────────────────────
  [T1: DB Schema]    [T4: Auth Service]    [T5: Email Service]

Tier 1  ────────────────────────────────────────────────────
  [T2: Migrations]   [T3: User Model]

Tier 2  ────────────────────────────────────────────────────
  [T6: User Service]

Tier 3  ────────────────────────────────────────────────────
  [T7: Notification Service]

Tier 4  ────────────────────────────────────────────────────
  [T8: API Endpoints]

    ──>  =  dependency (arrow points from dependency to dependent)
    T1 ──> T2, T3    T3 ──> T6    T2 ──> T6
    T4 ──> T8        T5 ──> T7    T6 ──> T7
    T7 ──> T8
```

This visualization is included in the `implementation-plan.md` and `impl-report.md` for reference.

---

## Best Practices for Task Decomposition

1. **Keep tasks small and focused.** Each task should have a single clear objective. A task that does "create model, service, and endpoints" should be split into three tasks.

2. **Minimize dependencies.** The fewer dependencies between tasks, the more parallelism is possible. If two tasks can be independent, make them independent.

3. **Use interfaces to break cycles.** If you find a circular dependency, introduce an interface or abstraction to allow independent development.

4. **Group related file changes.** A task should ideally change files that are logically related. Spreading a single concern across multiple tasks creates coordination overhead.

5. **Make success criteria concrete.** Each task's success criteria should be testable. "API endpoints work" is weak. "POST /users returns 201 with valid body, 400 with invalid body, 401 without auth" is strong.

6. **Estimate complexity honestly.** Complexity estimates (S/M/L) help the coordinator allocate resources and predict which tasks might take longer. Don't underestimate.

7. **Consider test tasks.** Tests can be their own tasks (depending on the code they test) or part of the implementation task. For complex features, separate test tasks work better because they get a dedicated agent with test-specific context.
