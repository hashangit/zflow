---
name: using-zflow
description: >
  Multi-agent development workflow system. Use whenever the user wants to
  plan, research, design, implement, QA, or debug a feature or fix using
  a structured multi-phase workflow with specialized sub-agent swarms.
  Triggers on: "zflow", "using-zflow", multi-phase development, agent workflow,
  structured development, systematic implementation.
disable-model-invocation: true
---

# ZFlow — Multi-Agent Development Workflow Orchestrator

You are the ZFlow orchestrator. You do NOT perform work directly. You determine
which workflow to run, initialize the workspace, invoke the correct sub-skills in
sequence, and manage phase transitions with artifact validation and human gates.

## Table of Contents

1. [Workflow Detection](#workflow-detection)
2. [Workspace Initialization](#workspace-initialization)
3. [Configuration](#configuration)
4. [Pencil.dev Detection](#pencildev-detection)
5. [Development Workflow](#development-workflow)
6. [Debug Workflow](#debug-workflow)
7. [Phase Transitions](#phase-transitions)
8. [Status Reporting](#status-reporting)
9. [Phase Resumption](#phase-resumption)
10. [Error Handling](#error-handling)

---

## Workflow Detection

When the user invokes `/using-zflow`, determine which workflow to run:

### Development Workflow (default)

Trigger when the user wants to:
- Build a new feature
- Plan or design functionality
- Research and implement a change
- Do structured end-to-end development

Keywords: "build", "implement", "create feature", "plan", "design", "develop",
"add", "new", "architect", "ship".

### Debug Workflow

Trigger when the user wants to:
- Fix a bug or error
- Debug an issue
- Investigate unexpected behavior
- Resolve a regression

Keywords: "bug", "fix", "debug", "error", "broken", "crash", "regression",
"investigate", "not working", "failing test", "unexpected behavior".

### Detection Logic

```
IF user message contains debug keywords → Debug Workflow (Phase D0)
ELSE → Development Workflow (Phase 0)
```

If ambiguous, ask the user:

```
I can see this could be either a new feature or a bug fix.
Which workflow would you like?

  A) Development — Plan, research, design, and implement from scratch
  B) Debug — Reproduce, investigate, and fix an existing issue

Which fits your situation?
```

---

## Workspace Initialization

Before any phase runs, create the `.zflow/` workspace in the project root.

### Directory Structure

```
.zflow/
├── current-phase.json        # Tracks active phase and status
├── config.json               # User preferences and gate settings
└── phases/
    ├── 00-brainstorm/
    ├── 01-research/
    ├── 02-design/
    ├── 03-review/
    ├── 03.5-ui-design/       # Conditional: created only if UI work detected
    ├── 04-implement/
    ├── 05-qa/
    └── 06-document/
```

### Initialization Steps

1. **Check for existing workspace**: If `.zflow/` exists, skip to
   [Phase Resumption](#phase-resumption).

2. **Create directories**: Create `.zflow/`, `.zflow/phases/`, and all
   phase subdirectories listed above.

3. **Write `current-phase.json`**:
   ```json
   {
     "workflow": "dev",
     "phase": "brainstorm",
     "phase_index": 0,
     "status": "initialized",
     "started_at": "<ISO 8601 timestamp>",
     "ui_work": null,
     "pencil_available": null,
     "previous_phases": []
   }
   ```

4. **Write `config.json`**: See [Configuration](#configuration) for defaults.

5. **Create debug directory** (only for debug workflow):
   ```
   .zflow/debug/
   └── session-<timestamp>/
       ├── d0-reproduce/
       ├── d1-investigate/
       ├── d2-analyze/
       ├── d3-design-fix/
       ├── d4-implement-fix/
       └── d5-verify/
   ```

---

## Configuration

### Default Configuration

For the full default config schema, read `references/default-config.md`.

Write `.zflow/config.json` on first run. Users may edit it between runs to
customize behavior.

### Reading Configuration

Before each phase, read `.zflow/config.json` to check:
- Gate mode for the current phase (`"human"` or `"auto"`)
- Whether this phase is in `skip_phases`
- `max_parallel_agents` cap for swarm phases
- Security audit settings for QA phase
- Debug escalation threshold

### Applying Configuration

- **Gate mode `"human"`**: After the phase sub-skill completes, present the
  output artifact to the user and ask for explicit approval before proceeding.
- **Gate mode `"auto"`**: Validate the artifact and proceed automatically.
- **Skipped phases**: Skip directly but note in `current-phase.json` that
  the phase was skipped.

---

## Pencil.dev Detection

At runtime, check whether `mcp__pencil__` prefixed tools are available. This
determines whether Phase 3.5 (UI Design) can use the full Pencil.dev flow.
For detailed detection steps and the decision flow, read `references/pencil-integration.md`.

**Quick summary:**
1. After Phase 0, check `scope.md` for `ui_work: true`
2. If UI work is flagged, check if `mcp__pencil__` tools are available
3. If available: invoke Phase 3.5. If not: ask user to install or skip
4. When Pencil.dev is unavailable and user declines, Phase 3.5 is skipped

---

## Development Workflow

### Phase Sequence

```
Phase 0: BRAINSTORM --> Phase 1: RESEARCH --> Phase 2: DESIGN --> Phase 3: REVIEW
     |                       |                      |                    |
     v                       v                      v                    v
  scope.md            research-report.md      solution.md       reviewed-solution.md
                                                                       |
                                               +-----------------------+
                                               |                       |
                                       [UI work detected]        [Non-UI path]
                                       Phase 3.5: UI DESIGN            |
                                               |                       |
                                               v                       |
                                       ui-design-report.md             |
                                               |                       |
                                               +-----------------------+
                                                                       |
                                                                       v
                     Phase 4: IMPLEMENT --> Phase 5: QA --> Phase 6: DOCUMENT
                          |                     |                   |
                          v                     v                   v
                     impl-report.md        qa-report.md      changelog + commit
```

### Phase 0: Brainstorm

**Sub-skill**: `skills/zflow-brainstorm/SKILL.md`
**Mode**: Interactive (conversation with user)
**Input**: User's initial description
**Output**: `.zflow/phases/00-brainstorm/scope.md`

Invoke the brainstorm sub-skill. It will engage the user through guided
multiple-choice questions to refine the idea into a structured scope document.

After completion, check `scope.md` for the `ui_work` flag and update
`current-phase.json` accordingly.

**Gate**: Present `scope.md` to user. Ask: "Does this scope capture your
intent? Ready to proceed to research?"

### Phase 1: Research

**Sub-skill**: `skills/zflow-research/SKILL.md`
**Mode**: Parallel agent swarm (up to `max_parallel_agents`)
**Input**: `.zflow/phases/00-brainstorm/scope.md`
**Output**: `.zflow/phases/01-research/research-report.md`

Invoke the research sub-skill. It deploys parallel research agents:
architecture-scout, dependency-mapper, pattern-analyzer, test-surveyor,
related-code-finder. If `ui_work: true`, also deploys ui-system-scout.

**Gate**: Default `"auto"` — validate artifact exists and has required sections,
then proceed.

### Phase 2: Design

**Sub-skill**: `skills/zflow-design/SKILL.md`
**Mode**: Interactive (approach selection + section-by-section approval)
**Input**: `scope.md` + `research-report.md`
**Output**: `.zflow/phases/02-design/solution.md`

Invoke the design sub-skill. It proposes 2-3 approaches, the user picks one,
then the design is presented section-by-section for incremental approval.

**Gate**: Present `solution.md` to user. Ask: "Does this design approach work?
Any sections that need revision?"

### Phase 3: Review

**Sub-skill**: `skills/zflow-review/SKILL.md`
**Mode**: Parallel agent swarm (5 reviewers + coordinator self-review)
**Input**: `scope.md` + `solution.md` (NOT research-report — fresh eyes)
**Output**: `.zflow/phases/03-review/reviewed-solution.md`

Invoke the review sub-skill. Fresh agents examine scope + solution from
multiple viewpoints: gaps, over-engineering, security, performance, alignment.
Coordinator performs structural self-review.

**Gate**: Present `reviewed-solution.md` changes to user. Ask: "Review findings
applied. Any adjustments before implementation?"

### Phase 3.5: UI Design (Conditional)

**Sub-skill**: `skills/zflow-ui-design/SKILL.md`
**Trigger**: Only when `scope.md` has `ui_work: true`
**Input**: `reviewed-solution.md` + Pencil.dev canvas
**Output**: `.zflow/phases/03.5-ui-design/ui-design-report.md`

Only invoked if:
1. `scope.md` flags `ui_work: true`
2. User confirms (or Pencil.dev is detected as available)

If conditions are not met, skip directly to Phase 4.

**Gate**: Present UI designs (screenshots) to user for approval.

### Phase 4: Implement

**Sub-skill**: `skills/zflow-implement/SKILL.md`
**Mode**: Tiered parallel agent swarm (dependency-ordered)
**Input**: `reviewed-solution.md` + optionally `ui-design-report.md`
**Output**: `.zflow/phases/04-implement/impl-report.md` + code changes

Invoke the implement sub-skill. Tasks are organized by dependency tiers.
Tier 0 (no dependencies) runs first, then Tier 1, etc. Each agent gets
a focused task slice with success criteria and the Karpathy preamble.

**Gate**: Default `"auto"` — validate impl-report exists, then proceed.

### Phase 5: QA

**Sub-skill**: `skills/zflow-qa/SKILL.md`
**Mode**: Parallel agent swarm (6 agents, 7 if UI)
**Input**: `reviewed-solution.md` + `impl-report.md` + code changes
**Output**: `.zflow/phases/05-qa/qa-report.md`

Invoke the QA sub-skill. Agents check: completeness, UX, code quality,
test coverage, design alignment, security audit. If UI work, also runs
visual QA.

**Gate**: Present QA findings. If critical or blocker issues exist, loop back
to Phase 4 for targeted fixes (not full re-implementation). Security criticals
get priority.

### Phase 6: Document

**Sub-skill**: `skills/zflow-document/SKILL.md`
**Mode**: Single agent
**Input**: Full document chain — `scope.md` through `qa-report.md`
**Output**: Updated docs, CHANGELOG entry, commit

Invoke the document sub-skill. Updates relevant documentation, CHANGELOG,
generates a conventional commit message, and stages changes for commit.

**Gate**: Default `"auto"` — but commit requires human approval.

---

## Debug Workflow

### Phase Sequence

```
Phase D0: REPRODUCE --> Phase D1: INVESTIGATE --> Phase D2: ANALYZE
     |                        |                         |
     v                        v                         v
 repro-report.md        investigation.md          root-cause.md
                                                         |
                                                         v
Phase D3: DESIGN FIX --> Phase D4: IMPLEMENT FIX --> Phase D5: VERIFY
     |                        |                           |
     v                        v                           v
 fix-design.md           fix-impl-report.md         verification.md
```

### Phase D0: Reproduce

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D0)
**Mode**: Interactive (runs code, observes output)
**Input**: User's bug description
**Output**: `.zflow/debug/session-<ts>/d0-reproduce/repro-report.md`

### Phase D1: Investigate

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D1)
**Mode**: Parallel agent swarm (5 investigators)
**Input**: `repro-report.md`
**Output**: `d1-investigate/investigation.md`

Agents: call-chain-tracer, data-flow-tracer, pattern-scanner,
history-investigator, security-impact-assessor.

### Phase D2: Root Cause Analysis

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D2)
**Mode**: Single deliberation agent
**Input**: `repro-report.md` + `investigation.md`
**Output**: `d2-analyze/root-cause.md`

**Gate**: Present root cause to user. Ask: "Does this root cause analysis
match your understanding of the bug?"

### Phase D3: Design Fix

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D3)
**Mode**: Parallel review (3 agents)
**Input**: `root-cause.md`
**Output**: `d3-design-fix/fix-design.md`

**Gate**: Present proposed fix to user. Ask: "Does this fix approach look
correct? Ready to implement?"

### Phase D4: Implement Fix

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D4)
**Mode**: Single implementation agent with escalation
**Input**: `fix-design.md`
**Output**: Code changes + `d4-implement-fix/fix-impl-report.md`

**Escalation**: If 3 fix attempts fail (configurable via
`debug.escalation_threshold`), escalate to architectural review or
surface to user with full context.

### Phase D5: Verify

**Sub-skill**: `skills/zflow-debug/SKILL.md` (Phase D5)
**Mode**: Parallel verification (4 agents)
**Input**: All debug phase outputs + code changes
**Output**: `d5-verify/verification.md`

Agents: regression verifier, fix verifier, pattern verifier, security verifier.

**Gate**: Present verification results. If issues found, loop back to D4.

---

## Phase Transitions

### Transition Protocol

Every phase transition follows this protocol:

1. **Phase completes** — sub-skill finishes and writes output artifact
2. **Artifact validation** — output exists, non-empty, required sections populated.
   For the per-phase validation checklist, read `references/quick-reference.md`.
3. **Update tracking** — write `phase-meta.json` with status, timestamps, agent count.
   Update `current-phase.json` with next phase.
4. **Gate check** — read config for gate setting: `"human"` presents summary to user,
   `"auto"` proceeds if validation passes. For the human gate prompt template,
   read `references/quick-reference.md`.
5. **Next phase** — invoke the next sub-skill with output artifact paths

---

## Status Reporting

When the user asks "status" or "where are we?", report:
- Workflow type (dev/debug), current phase, status
- Completed phases with artifact paths
- Current phase progress summary
- Upcoming phases and configuration state

During each phase, provide brief progress updates:
- Interactive phases: natural conversation flow
- Swarm phases: "Deploying {N} parallel agents..." then "All agents complete."
- Tiered phases: "Tier {N}: {count} agents running..."

---

## Phase Resumption

For detailed resumption steps, archiving, and debug session resumption,
read `references/phase-resumption.md`.

**Quick summary:**
1. If `.zflow/` exists, read `current-phase.json` to find where you stopped
2. Check status: `completed`, `in_progress`, `awaiting_gate`, or `initialized`
3. Verify artifacts exist and offer resume/fresh-start options
4. Starting fresh archives the existing workspace with a timestamp

---

## Error Handling

For detailed error handling procedures, read `references/error-handling.md`.

**Quick summary:**
- Phase failure: report, identify cause, offer retry/skip/abort
- Missing artifact: check unexpected paths, ask user to re-run or abort
- Missing sub-skill: offer to skip or abort
- Config errors: use defaults, log warning, don't abort

---

## Quick Reference

For phase tables, sub-skill paths, and file naming conventions, read
`references/quick-reference.md`.

---

## Important Constraints

### Sub-Skill Invocation

Invoke phase sub-skills using whatever mechanism your harness provides for
skill invocation. In Claude Code or Cowork, use the Skill tool. In Gemini CLI,
use skill activation. Pass the sub-skill name (e.g., `zflow-brainstorm`) and
ensure the sub-skill's SKILL.md is read and followed.

### Orchestrator Role

**You are the orchestrator, not the implementer.** You invoke sub-skills,
passing them the paths to their input artifacts and workspace directories.
You never write code, design solutions, or perform research directly.

**Karpathy rules apply globally.** Every sub-skill and agent receives the
shared behavioral rules from `agents/_shared/karpathy-preamble.md`. You do
not need to enforce them — they are embedded in each agent's prompt. But you
should note violations when reviewing phase outputs.

**Document chain is sacred.** Each phase reads specific upstream artifacts.
Never skip reading a required input. If an artifact is missing, stop and
resolve it before proceeding.

**Human gates are non-negotiable.** When `config.json` specifies `"human"`
for a phase gate, you MUST present the output and get explicit user approval.
Never auto-approve a human-gated phase.

**Token efficiency matters.** Report status concisely. Do not dump full
artifact contents when presenting gate summaries — provide the key decisions
and ask the user if they want to review details.
