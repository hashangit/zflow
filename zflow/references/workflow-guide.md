# ZFlow Workflow Guide

Reference for invoking, configuring, and navigating ZFlow workflows.

---

## Invoking the Workflow

| Command | Workflow | Use When |
|---------|----------|----------|
| `/using-zflow` | Brainstorm → Research → Design → Review → UI Design → Implement → QA → Document | New features, refactoring, architectural changes |
| `/using-zflow-debug` | Reproduce → Investigate → Analyze → Design Fix → Implement Fix → Verify | Bugs, errors, test failures |

Both require explicit invocation (`disable-model-invocation: true` prevents auto-triggering).

---

## Development Workflow: Phase-by-Phase

### Phase 0: Brainstorm

Socratic interviewer reads codebase silently, then engages in guided conversation. Questions one at a time in multiple-choice format with explanations and recommendations grounded in your project.

| | |
|---|---|
| **Input** | Your initial feature description |
| **Output** | `scope.md` — what to build and why (not how) |
| **Human gate** | Yes (default) |

**Agent steps:**
1. Reads project structure, tech stack, README, CLAUDE.md, planning docs
2. Restates your idea to confirm understanding
3. Asks clarifying questions one at a time (max 8-10)
4. Assesses scope decomposition need
5. Detects UI involvement and flags it
6. Presents "simplest viable version" tier

**Tips:**
- More upfront context = fewer questions
- Seriously consider decomposition if flagged
- "Simplest viable version" is almost always the right starting point

---

### Phase 1: Research

5-6 parallel agents fan out across your codebase to gather context around the scope.

| | |
|---|---|
| **Input** | `scope.md` |
| **Output** | `research-report.md` + individual reports in `agent-reports/` |
| **Human gate** | No (auto-pass) |

| Agent | Focus |
|-------|-------|
| architecture-scout | Project structure and architecture |
| dependency-mapper | Import chains and module coupling |
| pattern-analyzer | Coding patterns and conventions |
| test-surveyor | Test infrastructure and coverage |
| related-code-finder | Code affected by planned changes |
| ui-system-scout (conditional) | Design system, components, tokens |

Agents operate independently; coordinator merges into unified document with cross-cutting "Key Findings."

---

### Phase 2: Design

Senior architect maps research against scope, proposes 2-3 approaches as multiple-choice options, then presents chosen design section-by-section for incremental approval.

| | |
|---|---|
| **Input** | `scope.md` + `research-report.md` |
| **Output** | `solution.md` — approach, architecture, components, data flow, errors, testing, task breakdown |
| **Human gate** | Yes (default) |

**Sections presented one at a time:**
1. Architecture Overview
2. Component Breakdown
3. Data Flow
4. Error Handling and Edge Cases
5. Testing Strategy
6. Interface Design (if UI work)
7. Task Breakdown with Dependencies

Section-by-section approval prevents rubber-stamping; disagreements surface early.

---

### Phase 3: Review

Fresh agents (no prior context) examine scope and solution from multiple viewpoints. Coordinator performs structural self-review.

| | |
|---|---|
| **Input** | `scope.md` + `solution.md` (reviewers do NOT see research report — avoids anchoring bias) |
| **Output** | `reviewed-solution.md` + appendix of reviewer findings |
| **Human gate** | Yes (default) |

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

Only triggered when `scope.md` has `ui_work: true`. Full visual design via Pencil.dev if MCP available; otherwise user chooses to install or proceed without.

| | |
|---|---|
| **Input** | `reviewed-solution.md` |
| **Output** | `ui-design-report.md` — design tokens, component specs, screen layouts, exported images |
| **Human gate** | Yes (default) |

**Sub-phases:**
1. **Design System Setup** — extract/establish tokens, typography, spacing, component library
2. **UI Design on Canvas** — design each screen/component via Pencil.dev, iterate with user
3. **Design Review** — accessibility, responsiveness, consistency, compliance checks

If Pencil.dev unavailable and user declines install, phase skipped. Implementation works from text specs.

---

### Phase 4: Implement

Implementation agents deployed in parallel, organized by dependency tiers (Tier 0 first, then Tier 1, etc.).

| | |
|---|---|
| **Input** | `reviewed-solution.md` + optionally `ui-design-report.md` |
| **Output** | Working code + `impl-report.md` |
| **Human gate** | No (auto-pass) |

**Each agent receives:** task description + success criteria, relevant solution sections, file paths, coding conventions, test patterns, Karpathy preamble (surgical changes constraint). Every deviation from design must be justified in impl report.

---

### Phase 5: QA

QA agents run in parallel across multiple dimensions including deep security analysis.

| | |
|---|---|
| **Input** | `reviewed-solution.md` + `impl-report.md` + actual code changes |
| **Output** | `qa-report.md` with issues by severity |
| **Human gate** | Yes (default) |

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

| Level | Action |
|-------|--------|
| Critical (Security) | Must fix immediately |
| Blocker | Must fix before merge |
| Major | Should fix; creates tech debt if not |
| Minor | Nice to fix; cosmetic or stylistic |
| Note | Observation for future consideration |

Critical/blocker issues loop back to Phase 4 for targeted fixes.

---

### Phase 6: Document and Commit

| | |
|---|---|
| **Input** | Full document chain from scope through qa-report |
| **Output** | Updated documentation + git commit |
| **Human gate** | Yes (commit requires approval) |

---

## Debugging Workflow: Phase-by-Phase

| Phase | What Happens | Output |
|-------|-------------|--------|
| **D0: Reproduce** | Confirms reproducibility, documents steps, captures error output, identifies minimal reproduction | `repro-report.md` |
| **D1: Investigate** | Five parallel agents: call-chain-tracer, data-flow-tracer, pattern-scanner, history-investigator, security-impact-assessor | `investigation.md` |
| **D2: Root Cause** | Deliberation agent synthesizes findings, distinguishes symptom from cause | `root-cause.md` |
| **D3: Design Fix** | Three reviewers: minimal fix, regression review, pattern-wide fix | `fix-design.md` |
| **D4: Implement Fix** | Applies fix with 3-strike escalation rule | Code + `fix-impl-report.md` |
| **D5: Verify** | Four verifiers: fix works, no regressions, similar patterns checked, security intact | `verification.md` |

---

## Document Chain Summary

Development:
```
scope.md --> research-report.md --> solution.md --> reviewed-solution.md
                                                                      |
                                              [If UI] ui-design-report.md
                                                                      |
                                              reviewed-solution.md --> impl-report.md --> qa-report.md --> commit
```

Debug:
```
repro-report.md --> investigation.md --> root-cause.md --> fix-design.md --> fix-impl-report.md --> verification.md
```

---

## Human Gates

At each gate: **Approve** | **Request changes** (agent revises) | **Abort**.

Configure in `.zflow/config.json`:
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

| Mode | Behavior |
|------|----------|
| `human` | Pause and wait for user approval |
| `auto` | Pass automatically if artifact validation succeeds |

Auto-pass validates output exists and follows template structure — skips human review, not quality.

**Gate failure:** If validation fails, coordinator reports failure, re-runs the entire phase, surfaces issue to user if re-run also fails.

---

## Skipping Phases

Configure in `.zflow/config.json`:
```json
{ "skip_phases": ["brainstorm", "research"] }
```

| Scenario | Skip These |
|----------|------------|
| Quick fix with known design | brainstorm, research, design, review |
| Already designed, just implement | brainstorm, research, design |
| Known bug in debug workflow | reproduce |
| Non-UI work | Phase 3.5 auto-skipped (no config needed) |

Skipped phases' outputs unavailable downstream. E.g., skipping research means design works without codebase context.

---

## Resuming Interrupted Workflows

Tracked in `.zflow/current-phase.json`. On interruption:
1. `.zflow/` workspace persists all completed phase outputs
2. `current-phase.json` records in-progress phase and status
3. Re-invoking `/using-zflow` detects existing workspace
4. Orchestrator resumes from last completed phase

Manual resumption — edit `current-phase.json`: `{"phase": "implement", "status": "pending"}`

---

## Tips for Best Results

1. **Be specific upfront.** More context = fewer clarification questions.
2. **Engage with brainstorm questions.** Multiple-choice surfaces trade-offs.
3. **Resist scope creep during design.** Section-by-section approval catches over-engineering.
4. **Trust the review phase.** Fresh-agent reviews catch things anchored agents miss.
5. **Match gates to trust level.** Auto for trusted phases, human for control.
6. **Skip phases for iterative work.** After one full run, jump to implementation/QA.
7. **Review the security audit summary.** Highlights most important findings.
8. **Let UI design iterate.** Fixing design on canvas is cheaper than in code.

---

## Dynamic Pipeline Construction

ZFlow assesses task complexity before starting and proposes a pipeline profile. User approves or customizes.

### Complexity Scoring

5 signals scored 1-3 each: affected systems, technical domains, existing patterns, user language, ambiguity.

| Score | Level | Profile |
|-------|-------|---------|
| 4-5 | Trivial | Quick Fix |
| 6-9 | Standard | Standard |
| 10+ | Complex | Full or Extended |

### Pipeline Profiles

| Profile | Phases | Use Case |
|---------|--------|----------|
| **Quick Fix** | IMPLEMENT (design sketch) → QA (reduced) → DOCUMENT | Single-function fix, config change |
| **Standard** | BRAINSTORM (abbreviated) → DESIGN → REVIEW → IMPLEMENT → QA → DOCUMENT | Typical feature, 2-3 modules |
| **Full** | Full 8-phase pipeline | Cross-cutting, multi-system |
| **Extended** | Full + deeper research + extended security | Greenfield, security-critical |

See `references/pipeline-profiles.md` for complete definitions.

### User Override

Options: Accept, Upgrade, Downgrade, Customize specific phases, Use full pipeline.

### QA Loop-Back

When QA finds Critical/Blocker issues, classified by root cause layer:
- **Implementation** → Phase 4
- **Design** → Phase 2
- **Scope** → Phase 0

Orchestrator recommends target; user decides. See `references/phase-gates.md` for artifact preservation rules.

### Template Flexibility

Three-tier section classification:
- **Required** — must be present or gate fails
- **Expected** — should be present; if omitted, note why
- **Optional** — include, restructure, or omit freely

Output proportional to task complexity — no padded boilerplate.
