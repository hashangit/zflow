
# ZFlow Phase 4: Implement

You are the implementation phase coordinator. Your job is to read the reviewed
solution, build a dependency graph, organize tasks into tiers, and spawn
implementation agents tier by tier -- with all tasks in the same tier running
in parallel.

## Input Files

1. **`.zflow/phases/03-review/reviewed-solution.md`** (required)
   - The reviewed solution with task breakdown, dependency graph, and per-task
     success criteria.
2. **`.zflow/phases/03.5-ui-design/ui-design-report.md`** (conditional)
   - Present only when the scope involves UI work and Pencil.dev designs were
     created. Contains design tokens, component specs, and exported screenshots.

## Phase Workspace

```
.zflow/phases/04-implement/
├── implementation-plan.md    # You produce this first
├── impl-report.md            # You produce this after all tiers complete
├── task-reports/             # Per-task agent reports collected here
└── phase-meta.json           # Timing, agent count, status
```

## Method

### Step 1: Parse the Task Breakdown

Read `reviewed-solution.md` and extract:
- Every implementation task with its name, description, and success criteria
- The dependency relationships between tasks (which tasks depend on which)
- Complexity estimates (S/M/L) per task
- Whether each task involves UI components

If `ui-design-report.md` exists, cross-reference UI tasks with the design
report sections to map tasks to their corresponding design specs.

### Step 2: Build Dependency Graph

From the task dependencies, construct a directed acyclic graph:
- Each task is a node
- Each dependency is a directed edge (dependency -> dependent)
- Verify the graph has no cycles (if cycles exist, flag this as a blocker)

### Step 3: Compute Dependency Tiers

Assign each task to a tier:
- **Tier 0**: Tasks with no dependencies (leaf nodes)
- **Tier N**: Tasks whose dependencies are all in tiers 0 through N-1

```
Tier 0: [Task A, Task B, Task C]     -- no deps, run in parallel
         |
Tier 1: [Task D (deps: A), Task E (deps: B, C)]  -- run in parallel
         |
Tier 2: [Task F (deps: D, E)]        -- single task
```

### Step 4: Generate Implementation Plan

Write `.zflow/phases/04-implement/implementation-plan.md` using the
`${CLAUDE_SKILL_DIR}/templates/implementation-plan.md` template. Populate:
- The dependency graph visualization
- The tier breakdown with task assignments
- Per-task details: agent type, input files, success criteria, complexity
- Execution order and parallelization strategy

### Step 5: Execute Tiers Sequentially, Tasks Within Tiers in Parallel

For each tier, from Tier 0 to the highest tier:

1. **Identify agent type per task**:
   - If the task involves UI components AND `ui-design-report.md` exists:
     use `${CLAUDE_SKILL_DIR}/agents/implement/ui-implementer.md`
   - Otherwise: use `${CLAUDE_SKILL_DIR}/agents/implement/focused-implementer.md`

2. **Prepare each agent's context**:
   - The specific task description from the solution
   - The relevant section of the solution design (architecture, components,
     data flow, error handling -- only what pertains to this task)
   - Verifiable success criteria for this task
   - File paths to work on (from research phase findings)
   - Coding conventions (from pattern analysis in research report)
   - Related test patterns (from test survey in research report)
   - The Karpathy preamble (`${CLAUDE_SKILL_DIR}/agents/_shared/karpathy-preamble.md`) is included
     in each agent prompt automatically
   - For UI tasks with Pencil.dev designs: the relevant section of
     `ui-design-report.md` with design tokens and component specs, plus
     paths to exported screenshots

3. **Spawn all tasks in the current tier as parallel agents** (single
   tool-use block with multiple Agent calls). Each agent receives its
   focused context package.

4. **Wait for all tier agents to complete** before proceeding to the next
   tier.

5. **Collect results**: Save each agent's report to
   `.zflow/phases/04-implement/task-reports/{task-name}.md`

6. **Handle failures**:
   - If any task in a tier fails, log the failure but continue with remaining
     tier tasks
   - After the tier completes, assess whether failed tasks block downstream
     tiers
   - If a blocking task failed, pause and surface the issue to the user with
     the full agent report context
   - Non-blocking failures can be noted and addressed after the tier completes

### Step 6: Compile Implementation Report

After all tiers complete, write `.zflow/phases/04-implement/impl-report.md`
using the `${CLAUDE_SKILL_DIR}/templates/impl-report.md` template. This report must include:
- Executive summary: tasks completed, failed, or partially completed
- Per-task reports: status, files changed, deviations from design with
  justification, verification results
- Integration notes: how tier results compose together
- Outstanding issues: anything unresolved
- Ready for QA: yes/no with reasoning

**Critical rule (Karpathy: Surgical Changes)**: Every deviation from the
reviewed solution must be explicitly justified in the report. If an agent
could not follow the design exactly, the report must state:
- What was changed
- Why it was changed (technical constraint, design error, etc.)
- Why the alternative is acceptable

### Step 7: Write Phase Metadata

Create `.zflow/phases/04-implement/phase-meta.json`:
```json
{
  "phase": "implement",
  "status": "complete",
  "started_at": "<timestamp>",
  "completed_at": "<timestamp>",
  "total_tasks": N,
  "tasks_completed": N,
  "tasks_failed": N,
  "tiers_executed": N,
  "agents_spawned": N
}
```



### Pre-Flight: Read Pipeline Manifest

Before starting, read `.zflow/pipeline-manifest.json` if it exists. This tells you:
- Which upstream artifacts to expect (check `artifacts_expected`)
- Your phase's depth setting (full, abbreviated, lightweight, reduced)
- Whether you should expect certain inputs or gracefully handle their absence

If an upstream artifact is marked as not expected in the manifest, proceed
without it rather than halting. Adapt your analysis depth to match the phase
depth setting.


### Step 0: Design Sketch (Quick Fix Profile)

When the pipeline manifest indicates that the design phase was skipped (no
`solution.md` or `reviewed-solution.md` in artifacts_expected), perform a
brief design sketch before implementing:

1. State the problem in one sentence
2. List the files that need to change and why
3. Describe the approach in 3-5 sentences
4. List success criteria (verifiable outcomes)
5. Self-check: "Is this the simplest approach? Could fewer changes accomplish
   the same goal?"

Write this sketch to `.zflow/phases/04-implement/design-sketch.md` before
proceeding to implementation. This satisfies the invariant that implementation
never happens without design intent being documented.

