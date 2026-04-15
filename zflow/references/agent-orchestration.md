# Agent Orchestration Reference

How ZFlow coordinates sub-agent swarms across phases.

---

## Overview

ZFlow uses five orchestration patterns to coordinate sub-agents. Each pattern is chosen based on the dependency structure of the work being done. The coordinator (the phase's SKILL.md) is responsible for spawning agents, collecting results, and managing transitions.

---

## Pattern 1: Parallel Fan-Out

**Used in:** Research (Phase 1), Review (Phase 3), QA (Phase 5), Debug Investigation (Phase D1)

```
Coordinator reads phase input
    +-- Spawn Agent A (independent) --> Report A
    +-- Spawn Agent B (independent) --> Report B
    +-- Spawn Agent C (independent) --> Report C
    +-- Spawn Agent D (independent) --> Report D
              |
              v
    Coordinator merges reports into phase output
```

**When it is used:** When multiple independent analyses need to run on the same input. Each agent examines the input from a different perspective but does not depend on other agents' results.

**How spawning works:** All agents in a fan-out are spawned in the SAME message (a single tool-use block with multiple Agent calls). This maximizes parallelism -- all agents begin executing simultaneously rather than sequentially.

**How the coordinator merges results:**

1. Each agent writes its report to a designated file in the workspace (e.g., `agent-reports/architecture.md`)
2. The coordinator waits for all agents to complete
3. The coordinator reads all individual reports
4. Common findings across agents are elevated to "Key Findings"
5. Contradictions between agents are flagged for resolution
6. The merged output follows the phase's template structure

**Agent isolation:** Each fan-out agent runs independently — it receives only what
you explicitly include in its prompt string. Agents launched via the Agent tool
cannot see each other's work or the parent conversation, preventing groupthink.
Construct each agent's prompt by combining: the Karpathy preamble, the agent's
specific prompt file, and the relevant input documents.

**Example -- Research Phase:**
- architecture-scout maps the project structure
- dependency-mapper traces import chains
- pattern-analyzer identifies coding conventions
- test-surveyor maps test infrastructure
- related-code-finder locates affected code
- All five agents read `scope.md` independently and produce separate reports
- The coordinator synthesizes them into `research-report.md`

---

## Pattern 2: Tiered Fan-Out

**Used in:** Implementation (Phase 4)

```
Coordinator builds dependency graph from solution
    |
    +-- Tier 0: Spawn agents for independent tasks --> Wait for all
    |       |
    |       v
    +-- Tier 1: Spawn agents for Tier-0-dependent tasks --> Wait for all
    |       |
    |       v
    +-- Tier N: Continue until all tasks complete
```

**When it is used:** When tasks have dependencies between them but tasks within the same dependency level are independent. This is the implementation-specific pattern because code changes often depend on earlier code changes.

**How tiers are determined:**

1. The solution's task breakdown includes a dependency graph
2. Tasks with no dependencies are assigned to Tier 0
3. Tasks that depend only on Tier 0 tasks are assigned to Tier 1
4. Tasks that depend on Tier 0 or Tier 1 are assigned to Tier 2
5. This continues until all tasks are assigned

**Within a tier:** All tasks at the same tier level run in parallel. The coordinator spawns one agent per task simultaneously.

**Between tiers:** The coordinator waits for ALL tasks in the current tier to complete before spawning agents for the next tier. This ensures that dependent code changes are in place before the next tier begins.

**Example:**

```
Tier 0 (parallel):   Create User model  |  Create Database migration  |  Set up API routes
                       |                        |                            |
Tier 1 (parallel):   UserService (depends on User model + DB migration)
                       |
Tier 2 (parallel):   UserEndpoints (depends on UserService + API routes)  |  UserTests (depends on UserService)
```

---

## Pattern 3: Sequential Handoff

**Used in:** Phase-to-phase transitions

```
Phase N completes --> Validate output --> Human gate --> Phase N+1 reads output
```

**When it is used:** Between every phase transition. This is not an agent pattern per se, but the mechanism that governs how phases connect.

**Steps:**
1. Phase N completes and writes its output document
2. Artifact validation checks that the document exists and follows the template
3. If the gate is set to `human`, the user reviews and approves
4. If the gate is set to `auto`, validation passing is sufficient
5. Phase N+1's coordinator reads the output as its input

**Why sequential:** Each phase builds on the output of the previous phase. Research informs design. Design informs review. Review informs implementation. These cannot safely overlap because later phases depend on the conclusions of earlier phases.

---

## Pattern 4: Conditional Branch

**Used in:** UI Design phase (Phase 3.5)

```
Scope flag: ui_work?
    |
    +-- No  --> Skip to Phase 4
    |
    +-- Yes --> Pencil.dev MCP tools available?
                |
                +-- Yes --> Phase 3.5 (full UI design flow)
                |
                +-- No  --> Ask user: Install or Skip?
                              |
                              +-- Install --> Guide install --> Full Pencil.dev flow
                              +-- Skip --> Standard implementation (no Phase 3.5)
```

**When it is used:** When a phase should only execute under certain conditions. Currently used for the UI Design phase, but the pattern applies to any optional phase.

**Decision points:**
1. Is UI work part of the scope? (from `scope.md` `ui_work` flag)
2. Are Pencil.dev MCP tools available? (runtime detection)
3. Does the user want to install Pencil.dev? (if tools not available)

**Graceful degradation:** If the condition is not met, the workflow continues without the optional phase. Downstream agents receive adjusted context (text-based specs instead of visual designs, for example).

---

## Pattern 5: Escalation Loop

**Used in:** Debug fix implementation (Phase D4)

```
Attempt fix --> Run tests --> Pass? --> Done
                    |
                    v Fail
              Attempt < 3? --> Yes --> Re-analyze with fresh context + retry
                    |
                    v No
              Escalate to senior agent / surface to user
```

**When it is used:** When a fix attempt may fail and needs retry logic with escalating expertise.

**How it works:**

1. **Attempt 1:** Implement the designed fix, run tests
2. **Attempt 2:** If tests still fail, re-analyze the problem with fresh context (the failure output from Attempt 1), design a revised fix, implement it
3. **Attempt 3:** If still failing, re-analyze again with all accumulated failure context
4. **After 3 failures:** Escalate -- either to a senior architectural review agent or surface the full context to the user for human decision

**Why 3 strikes:** Three attempts give the agent enough room to learn from failures while preventing infinite retry loops. Each attempt builds on the failure context of previous attempts, so the agent gets progressively better informed.

**Karpathy enforcement:** Each attempt must define success criteria before starting. Every changed line must trace to the fix design.

---

## Configuring Max Parallel Agents

The `max_parallel_agents` setting in `.zflow/config.json` controls how many agents can run simultaneously in a fan-out or tiered fan-out:

```json
{
  "max_parallel_agents": 5
}
```

**How it works:**

- If a phase has 6 agents to spawn but `max_parallel_agents` is 5, the coordinator spawns 5 first, waits for one to complete, then spawns the 6th.
- This prevents excessive token consumption from too many simultaneous agents.
- The default is 5, which balances parallelism with cost.

**When to increase:** If you have a large number of independent tasks (e.g., 10 implementation tasks at the same tier) and want to maximize wall-clock speed, increase this value.

**When to decrease:** If you are concerned about token cost or the sub-agents are competing for resources (file system, network), decrease this value.

---

## Agent Isolation

### Independent Agents (most phases)

Most agents run independently — each receives only what you explicitly include
in its prompt string:
- The Karpathy preamble (from `agents/_shared/karpathy-preamble.md`)
- Their specific agent prompt file (role, mission, method, output format)
- The input documents you include (e.g., `scope.md` contents)

**Why this matters:**
- Agents cannot be influenced by each other's reasoning during parallel execution
- Each agent's analysis is independent and unbiased
- Review agents in Phase 3 deliberately do NOT receive the research report to avoid anchoring bias

**Trade-off:** Independent agents cannot see prior phase context that was not explicitly passed. This is by design — the document chain ensures all necessary context is persisted in files.

### Interactive Agents

Some phases (brainstorming in Phase 0, design in Phase 2) run in the main
conversation thread because they need to converse with the user. These are not
spawned as separate agents — the phase runs directly in the orchestrator's
context.

---

## Coordinator Responsibilities

Each phase's SKILL.md acts as the coordinator. The coordinator is a **dispatcher,
not a worker**. It decides what to do and delegates the doing.

1. **Dispatch workers:** Spawn subagents to read inputs, analyze code, and produce reports
2. **Dispatch writer:** Spawn a synthesis agent to read worker reports, merge them, and
   write the final phase output document
3. **Monitor completion:** Wait for all agents in a group to finish
4. **Validate:** Check the output follows the template structure (quick structural check only)
5. **Gate check:** Present to user if the gate is set to `human`
6. **Persist:** Confirm the output was written to the workspace directory

### Coordinator Must NOT Do Itself

| Task | Delegate to |
|------|-------------|
| Read and analyze workspace artifacts (scope.md, research-report.md, etc.) | Subagent |
| Read agent prompt files and templates to embed in prompts | Pass paths to subagent — let it read them |
| Merge multiple agent reports into a single output | Synthesis subagent |
| Write the final phase output document | Synthesis subagent |
| Analyze task dependencies, build dependency graphs | Subagent |

### How to Pass File Paths Instead of Contents

When spawning a subagent, do NOT read the file and embed its contents in the
prompt. Instead, pass the resolved file path and let the agent read it:

```
Bad:  Read scope.md → paste contents into agent prompt
Good: "Read .zflow/phases/00-brainstorm/scope.md, then [agent instructions]"
```

For skill-internal files (agent prompts, templates, Karpathy preamble), resolve
`${CLAUDE_SKILL_DIR}` to its absolute path before passing to the agent, since
subagents may not have access to the variable.

### Synthesis Agent Pattern

Each phase that collects multiple worker reports should spawn a **synthesis agent**
as the final step:

1. Worker agents complete and write individual reports to the workspace
2. Coordinator spawns a synthesis agent that:
   - Receives the list of report file paths to read
   - Receives the output template file path
   - Reads all reports, merges overlapping findings, flags contradictions
   - Writes the final merged output to the designated file
3. Coordinator validates the output exists and has required sections
4. Coordinator runs the gate check

This keeps the coordinator's context lean — it never loads the full content of
worker reports or output templates.

---

## Error Handling in Orchestration

### Individual Agent Failure

If an individual agent fails (timeout, error, incomplete output):

1. The coordinator logs the failure
2. If the failed agent's output is critical (e.g., architecture-scout in research), the coordinator re-spawns that agent with the same input
3. If re-spawn also fails, the coordinator notes the gap in the merged output and proceeds with available information
4. The phase output includes a "Coverage Gaps" section noting any agent whose analysis is missing

This ensures the workflow is resilient -- one failing agent does not block the entire phase.

### Rate Limits and Server Unavailability

When spawning agents and encountering rate limits (429/529), server errors (503),
or connection failures ("server temporarily unavailable"):

**Step 1 — Retry parallel.** Wait a short pause and re-attempt the same parallel
spawn. Often the issue is transient.

**Step 2 — Fall back to sequential.** If the parallel retry also fails, the
coordinator spawns agents **one at a time** instead of in a single batch. Each
agent is launched only after the previous one completes.

**Step 3 — Reduce batch size.** If sequential still triggers rate limits, split
the remaining agents into smaller batches (e.g., 2 at a time) and retry.

**Step 4 — Proceed with available results.** If agents still fail after
sequential + reduced-batch attempts, follow the individual agent failure
procedure above: log gaps and proceed.

**Decision flow:**

```
Parallel spawn fails (rate limit / server error)?
    |
    +-- Yes --> Short pause --> Retry parallel spawn
    |               |
    |               +-- Success --> Continue normally
    |               +-- Fail again --> Switch to sequential (one agent at a time)
    |                                      |
    |                                      +-- Success --> Continue normally
    |                                      +-- Fail --> Reduce batch to 2 agents
    |                                                      |
    |                                                      +-- Success --> Continue
    |                                                      +-- Fail --> Proceed with gaps
    |
    +-- No --> Continue normally
```

**Coordinator behavior during fallback:**
- When switching to sequential, spawn each remaining agent individually
- Each sequential agent gets the same prompt and input as the parallel version
- Do NOT re-spawn agents that already completed successfully
- Track which agents succeeded vs. failed to avoid duplicate work
