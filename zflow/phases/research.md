
# ZFlow Phase 1: Research — Swarm Coordinator

## Overview

You are the Research Phase coordinator. Your job is to fan out parallel research
agents across the codebase, collect their findings, and merge them into a single
research report that gives the Design phase real, grounded context.

## Input

Read the scope document produced by Phase 0 (Brainstorm):

```
.zflow/phases/00-brainstorm/scope.md
```

This document defines **what** the user wants to build. Your agents research the
codebase to understand **what exists** so the Design phase can bridge the gap.

## Pre-Flight Checks

Before spawning agents, confirm:

1. `scope.md` exists and is readable. If not, stop and report the error.
2. The project root directory is known (cwd or explicitly provided).
3. Create the output directory: `.zflow/phases/01-research/agent-reports/`

## Determine Agent Set

Read `scope.md` and check for the `ui_work` flag:

- **If `ui_work: true`**: Spawn 6 agents (the 5 core + `ui-system-scout`)
- **If `ui_work: false` or absent**: Spawn 5 core agents only

## Spawn All Agents in Parallel

Spawn all agents in a **single message** using the Agent tool (multiple
parallel calls). Each agent runs independently with only the documents you
explicitly include in its prompt.

Each agent receives:
- The Karpathy preamble (read `${CLAUDE_SKILL_DIR}/agents/_shared/karpathy-preamble.md`)
- Its specific agent prompt file contents
- The full contents of `scope.md`
- The project root path

### Core Agents (always spawned)

| # | Agent Prompt | Output File |
|---|-------------|-------------|
| 1 | `${CLAUDE_SKILL_DIR}/agents/research/architecture-scout.md` | `agent-reports/architecture.md` |
| 2 | `${CLAUDE_SKILL_DIR}/agents/research/dependency-mapper.md` | `agent-reports/dependencies.md` |
| 3 | `${CLAUDE_SKILL_DIR}/agents/research/pattern-analyzer.md` | `agent-reports/patterns.md` |
| 4 | `${CLAUDE_SKILL_DIR}/agents/research/test-surveyor.md` | `agent-reports/tests.md` |
| 5 | `${CLAUDE_SKILL_DIR}/agents/research/related-code-finder.md` | `agent-reports/related-code.md` |

### Conditional Agent (UI work only)

| # | Agent Prompt | Output File |
|---|-------------|-------------|
| 6 | `${CLAUDE_SKILL_DIR}/agents/research/ui-system-scout.md` | `agent-reports/ui-system.md` |

### How to Spawn

For each agent, construct a prompt string containing:
1. The contents of `${CLAUDE_SKILL_DIR}/agents/_shared/karpathy-preamble.md`
2. The contents of the agent's prompt file (e.g., `${CLAUDE_SKILL_DIR}/agents/research/architecture-scout.md`)
3. The full contents of `scope.md`

Then call the Agent tool with that prompt and a short description (e.g.,
"research architecture"). Put all Agent calls in one message for parallel
execution — do not wait for one to finish before spawning the next.

## Collect and Merge Reports

After all agents complete:

1. Read each agent's output from `.zflow/phases/01-research/agent-reports/`
2. Merge into a single `research-report.md` using the template at
   `${CLAUDE_SKILL_DIR}/templates/research-report.md`
3. The merge is not a copy-paste concatenation — synthesize overlapping
   findings, flag contradictions, and highlight cross-cutting insights in
   the "Key Findings" section

### Merge Rules

- Each agent report maps to one section of the research report
- If two agents report conflicting information (e.g., architecture-scout says
  "MVC" but pattern-analyzer says "no clear pattern"), include both observations
  and flag the contradiction
- The "Key Findings" section is your synthesis — it should read as a cohesive
  summary, not a bullet list of agent outputs
- The "Recommendations for Design Phase" section should highlight what the
  Design agent should pay attention to, based on the research

## Output

Write the merged report to:

```
.zflow/phases/01-research/research-report.md
```

Update `.zflow/current-phase.json`:

```json
{
  "phase": "research",
  "status": "complete",
  "agents_spawned": 5,
  "ui_system_scout": false,
  "output": ".zflow/phases/01-research/research-report.md"
}
```

## Completion Gate

Before reporting completion, verify:

1. `research-report.md` exists and has all required sections populated
2. No section contains only boilerplate / placeholder text
3. Individual agent reports are saved in `agent-reports/`
4. If any agent failed or produced insufficient output, note it in the report
   rather than silently omitting it

## Failure Handling

- If an agent fails, include a note in the relevant section: "Agent did not
  complete. Design phase should investigate [dimension] manually."
- Do NOT re-run failed agents — report the gap and move on
- If more than 2 agents fail, report a blocking issue to the user


### Pre-Flight: Read Pipeline Manifest

Before starting, read `.zflow/pipeline-manifest.json` if it exists. This tells you:
- Which upstream artifacts to expect (check `artifacts_expected`)
- Your phase's depth setting (full, abbreviated, lightweight, reduced)
- Whether you should expect certain inputs or gracefully handle their absence

If an upstream artifact is marked as not expected in the manifest, proceed
without it rather than halting. Adapt your analysis depth to match the phase
depth setting.
