# ZFlow Workflow Guide

Complete reference for invoking, configuring, and navigating ZFlow workflows.

---

## Invoking the Workflow

ZFlow provides two slash commands, each triggering a different workflow:

### Development Workflow

```
/using-zflow
```

Invokes the full multi-phase development workflow: Brainstorm, Research, Design, Review, UI Design (conditional), Implement, QA, and Document. Use this when planning and building new features, refactoring existing code, or making significant architectural changes.

### Debugging Workflow

```
/using-zflow-debug
```

Invokes the debugging workflow: Reproduce, Investigate, Analyze, Design Fix, Implement Fix, and Verify. Use this when fixing bugs, investigating errors, or resolving test failures.

Both commands require explicit invocation (the `disable-model-invocation: true` setting prevents automatic triggering). This is intentional -- the full workflow spawns multiple sub-agents and should be a deliberate choice.

---

## Development Workflow: Phase-by-Phase Walkthrough

### Phase 0: Brainstorm

**What happens:** A Socratic interviewer agent reads your codebase silently, then engages you in a guided conversation. Questions are asked one at a time in multiple-choice format with explanations, trade-offs, and recommendations grounded in your actual project.

**Input:** Your initial feature description (whatever you typed alongside `/using-zflow`)

**Output:** `scope.md` -- a structured document capturing what needs to be built and why (but not how).

**Human gate:** Yes (default). You review and approve the scope before proceeding.

**What the agent does:**
1. Silently reads project structure, tech stack, README, CLAUDE.md, and planning docs
2. Restates your idea to confirm understanding
3. Asks clarifying questions one at a time (max 8-10 total)
4. Assesses whether the scope should be decomposed into sub-projects
5. Detects whether UI work is involved and flags it
6. Presents a "simplest viable version" tier for consideration

**Tips for best results:**
- Give as much context as possible upfront to reduce the number of questions
- If the agent flags decomposition, seriously consider it -- monolithic scopes produce worse results
- Pay attention to the "simplest viable version" option; starting small and iterating is almost always better

---

### Phase 1: Research

**What happens:** A swarm of 5 parallel agents (6 if UI work detected) fans out across your codebase to gather real context around the scope.

**Input:** `scope.md`

**Output:** `research-report.md` with individual agent reports in `agent-reports/`

**Human gate:** No (default: auto-pass)

**Agents deployed:**
| Agent | Focus |
|-------|-------|
| architecture-scout | Project structure and architecture |
| dependency-mapper | Import chains and module coupling |
| pattern-analyzer | Coding patterns and conventions |
| test-surveyor | Test infrastructure and coverage |
| related-code-finder | Code affected by the planned changes |
| ui-system-scout (conditional) | Design system, components, tokens |

Each agent operates in a forked context with focused instructions. The coordinator merges all reports into a unified research document with cross-cutting "Key Findings."

---

### Phase 2: Design

**What happens:** A senior architect agent maps research findings against the scope, proposes 2-3 solution approaches as guided multiple-choice options, then presents the chosen design section-by-section for incremental approval.

**Input:** `scope.md` + `research-report.md`

**Output:** `solution.md` -- a complete design document with approach, architecture, components, data flow, errors, testing, and task breakdown.

**Human gate:** Yes (default). You approve the approach selection and each design section.

**Sections presented for approval (one at a time):**
1. Architecture Overview
2. Component Breakdown
3. Data Flow
4. Error Handling and Edge Cases
5. Testing Strategy
6. Interface Design (if UI work)
7. Task Breakdown with Dependencies

**Why section-by-section?** This prevents rubber-stamping a long document. Each section is approved individually, so disagreements surface early.

---

### Phase 3: Review

**What happens:** Fresh agents with no prior context examine the scope and solution from multiple viewpoints. Then the coordinator performs a structural self-review.

**Input:** `scope.md` + `solution.md` (reviewers do NOT see the research report -- this is intentional to avoid anchoring bias)

**Output:** `reviewed-solution.md` with an appendix of all reviewer findings.

**Human gate:** Yes (default)

**Agents deployed:**
| Agent | Perspective |
|-------|------------|
| gap-detector | Missing requirements and edge cases |
| overengineering-critic | Unnecessary complexity, YAGNI violations |
| security-reviewer | Attack vectors and auth gaps |
| performance-reviewer | Bottlenecks and scaling concerns |
| alignment-checker | Architecture fit and naming consistency |

**Coordinator self-review checks:**
- No TBD/TODO sections remain
- Architecture does not contradict data flow
- Solution has not drifted beyond scope
- Every section is actionable without guessing
- Every component maps to at least one implementation task

---

### Phase 3.5: UI Design (Conditional)

**What happens:** Only triggered when `scope.md` has `ui_work: true`. If Pencil.dev MCP tools are available, a full visual design workflow runs. If not, the user is asked whether to install Pencil.dev or proceed without it.

**Input:** `reviewed-solution.md`

**Output:** `ui-design-report.md` with design tokens, component specs, screen layouts, and exported reference images.

**Human gate:** Yes (default)

**Sub-phases:**
1. **Design System Setup** -- extract or establish tokens, typography, spacing, component library
2. **UI Design on Canvas** -- design each screen/component using Pencil.dev, iterate with user
3. **Design Review** -- accessibility, responsiveness, consistency, and compliance checks

If Pencil.dev is not available and the user declines to install it, this phase is skipped entirely. Implementation agents will work from text-based specifications instead.

---

### Phase 4: Implement

**What happens:** Implementation agents are deployed in parallel, organized by dependency tiers. Tier 0 tasks (no dependencies) run first, then Tier 1, and so on.

**Input:** `reviewed-solution.md` + optionally `ui-design-report.md`

**Output:** Working code + `impl-report.md`

**Human gate:** No (default: auto-pass)

Each agent receives:
- Its specific task description and success criteria
- Relevant sections of the solution design
- File paths to work on (from research)
- Coding conventions (from pattern analysis)
- Related test patterns (from test survey)
- The Karpathy preamble (surgical changes constraint)

Every deviation from the design must be justified in the impl report.

---

### Phase 5: QA

**What happens:** QA agents run in parallel across multiple dimensions including deep security analysis.

**Input:** `reviewed-solution.md` + `impl-report.md` + actual code changes

**Output:** `qa-report.md` with issues categorized by severity

**Human gate:** Yes (default)

**Agents deployed:**
| Agent | Dimension |
|-------|-----------|
| completeness-checker | Every task from solution is implemented |
| ux-reviewer | API ergonomics, error messages, edge cases |
| code-quality-auditor | Linting, naming, complexity, scope tracing |
| test-coverage-agent | Test coverage and quality |
| design-alignment-qa | Implementation matches reviewed solution |
| security-auditor | Full OWASP Top 10 2025 audit |
| ui-visual-qa (conditional) | Design fidelity, responsive behavior |

**Issue severity levels:**
- **Critical (Security):** Must fix immediately
- **Blocker:** Must fix before merge
- **Major:** Should fix; creates tech debt if not
- **Minor:** Nice to fix; cosmetic or stylistic
- **Note:** Observation for future consideration

If critical or blocker issues exist, the workflow loops back to Phase 4 for targeted fixes.

---

### Phase 6: Document and Commit

**What happens:** A documentation agent updates relevant docs, changelogs, and README files, then commits changes with a structured commit message.

**Input:** Full document chain from scope through qa-report

**Output:** Updated documentation + git commit

**Human gate:** Yes (commit requires approval)

---

## Debugging Workflow: Phase-by-Phase Walkthrough

### Phase D0: Reproduce

**What happens:** Agent confirms the bug is reproducible, documents exact steps, captures error output, and identifies the minimal reproduction case.

**Output:** `repro-report.md`

---

### Phase D1: Investigate

**What happens:** Five parallel agents trace the issue from different angles.

**Output:** `investigation.md`

**Agents:** call-chain-tracer, data-flow-tracer, pattern-scanner, history-investigator, security-impact-assessor

---

### Phase D2: Root Cause Analysis

**What happens:** A deliberation agent synthesizes all findings to identify the true root cause, distinguishing symptom from cause.

**Output:** `root-cause.md`

---

### Phase D3: Design Fix

**What happens:** Three parallel reviewers design and evaluate the proposed fix: minimal fix, regression review, and pattern-wide fix.

**Output:** `fix-design.md`

---

### Phase D4: Implement Fix

**What happens:** Implementation agent applies the fix with a 3-strike escalation rule.

**Output:** Code changes + `fix-impl-report.md`

---

### Phase D5: Verify

**What happens:** Four parallel verifiers confirm the fix works, no regressions, similar patterns are checked, and security is intact.

**Output:** `verification.md`

---

## Document Chain Summary

Each phase produces a document that becomes input for subsequent phases:

```
scope.md  -->  research-report.md  -->  solution.md  -->  reviewed-solution.md
                                                                      |
                                              [If UI] ui-design-report.md
                                                                      |
                                              reviewed-solution.md  -->  impl-report.md
                                                                      |
                                              impl-report.md  -->  qa-report.md  -->  commit
```

In the debug workflow:

```
repro-report.md  -->  investigation.md  -->  root-cause.md  -->  fix-design.md
                                                                          |
                                              fix-design.md  -->  fix-impl-report.md  -->  verification.md
```

---

## How Human Gates Work

At each human gate, the workflow pauses and presents the phase output to the user. The user can:

- **Approve:** Proceed to the next phase
- **Request changes:** The phase agent revises and re-presents
- **Abort:** Stop the workflow entirely

Gates are configured in `.zflow/config.json`:

```json
{
  "gates": {
    "brainstorm": "human",
    "research": "auto",
    "design": "human",
    "review": "human",
    "ui_design": "human",
    "implement": "auto",
    "qa": "human",
    "document": "auto"
  }
}
```

### Gate Modes

| Mode | Behavior |
|------|----------|
| `human` | Pause and wait for user approval before proceeding |
| `auto` | Automatically pass the gate if artifact validation succeeds |

### Auto-Pass

When a gate is set to `auto`, it still validates that the output document exists and follows the template structure. Auto-pass does not skip quality -- it skips the human review step. Use auto-pass for phases where you trust the agent output (e.g., research is factual, implementation follows an approved design).

### What Happens When a Gate Fails

If artifact validation fails (missing document, incomplete sections, boilerplate not replaced), the gate fails regardless of its mode. The coordinator:
1. Reports what failed validation
2. Re-runs the phase (not the individual agent -- the entire phase)
3. If re-run also fails, surfaces the issue to the user

---

## Skipping Phases

For smaller tasks, you can skip phases that are not needed. Configure this in `.zflow/config.json`:

```json
{
  "skip_phases": ["brainstorm", "research"]
}
```

Common skip patterns:

| Scenario | Skip These Phases |
|----------|-------------------|
| Quick fix with known design | brainstorm, research, design, review |
| Already designed, just implement | brainstorm, research, design |
| Known bug in debug workflow | reproduce |
| Non-UI work | Phase 3.5 auto-skipped (no config needed) |

**Important:** When you skip phases, the downstream phases will not have the benefit of the skipped phase's output. For example, skipping research means the design agent works without codebase context. Use this intentionally.

---

## Resuming an Interrupted Workflow

ZFlow tracks progress in `.zflow/current-phase.json`. If a workflow is interrupted (network issue, session ended, manual stop):

1. The `.zflow/` workspace directory persists all completed phase outputs
2. `current-phase.json` records which phase was in progress and its status
3. Re-invoking `/using-zflow` detects the existing workspace
4. The orchestrator resumes from the last completed phase

**Manual resumption:** You can also manually set the resume point by editing `current-phase.json`:

```json
{
  "phase": "implement",
  "status": "pending"
}
```

This tells the orchestrator to start from the implement phase, assuming prior phases' outputs exist in the workspace.

---

## Tips for Getting the Best Results

1. **Be specific in your initial prompt.** The more context you provide upfront, the fewer clarification questions the brainstorm agent needs to ask.

2. **Engage with the brainstorm questions.** The multiple-choice format is designed to surface trade-offs. Reading the options carefully and choosing thoughtfully produces better scope documents.

3. **Resist scope creep during design.** The section-by-section approval is your chance to catch over-engineering. If a section feels more complex than the problem warrants, push back.

4. **Trust the review phase.** Fresh-agent reviews catch things that design agents (anchored by research context) miss. Take review findings seriously, especially from the overengineering-critic.

5. **Configure gates to match your trust level.** If you are confident in the agent's ability for a particular phase type, set it to `auto`. If you want tighter control, keep it as `human`.

6. **Use phase skipping for iterative work.** If you have already run the full workflow once and are iterating on the same feature, skip early phases and jump to implementation or QA.

7. **Review the security audit.** Even if you are not a security expert, read the executive summary of the security audit report. It highlights the most important findings.

8. **Let UI design iterate.** If you are using Pencil.dev, take the time to iterate on the design before implementation. Fixing a design in code is more expensive than fixing it on the canvas.
