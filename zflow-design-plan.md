# ZFlow — Multi-Agent Development Workflow System

## Design Plan & Architecture Document (v2)

---

## 1. Vision & Philosophy

ZFlow is an opinionated, multi-agent development workflow system built as a Claude Code skill. It takes inspiration from the Superpowers framework's structured methodology but goes significantly further by implementing a **full software development lifecycle** through orchestrated **sub-agent swarms**.

### Core Principles

**Agent Specialization**: Each phase deploys purpose-built agents with focused prompts rather than a single monolithic agent trying to do everything. A brainstorming agent thinks differently than an implementation agent.

**Document-Driven Handoffs**: Every phase produces a structured artifact (markdown document) that becomes the input for the next phase. This creates an auditable trail and enables any phase to be re-run independently.

**Parallel Where Possible, Sequential Where Necessary**: Research agents fan out in parallel. Implementation agents fan out in parallel per dependency tier. Review agents fan out in parallel across concern dimensions. But phase transitions are sequential gates.

**No Fix Without Understanding**: Borrowed from Superpowers' "Iron Law" — no implementation without design, no design without research, no debugging fix without root cause. Every phase earns its right to proceed.

**Human-in-the-Loop Gates**: The workflow pauses at critical checkpoints for human review before proceeding to the next phase.

### Karpathy Behavioral Guidelines (Embedded System-Wide)

The following principles from Andrej Karpathy's LLM coding guidelines are **baked into every agent prompt** across ZFlow. They are not a separate phase — they are constraints that govern how every agent thinks and acts:

**Think Before Coding**: Every agent must state assumptions explicitly before acting. If multiple interpretations exist, present them — don't pick silently. If a simpler approach exists, say so. If something is unclear, stop and name what's confusing.

**Simplicity First**: Minimum code that solves the problem. No features beyond what was asked. No abstractions for single-use code. No speculative "flexibility" or "configurability." If 200 lines could be 50, rewrite it. Every agent asks: "Would a senior engineer say this is overcomplicated?"

**Surgical Changes**: Touch only what you must. Don't "improve" adjacent code, comments, or formatting. Don't refactor things that aren't broken. Match existing style. Remove only imports/variables/functions that YOUR changes made unused. Every changed line must trace directly to the user's request.

**Goal-Driven Execution**: Transform tasks into verifiable goals. Every implementation task has success criteria defined upfront. Each step has a verification check. Strong success criteria let agents loop independently; weak criteria require human clarification.

These guidelines are enforced at three levels:
1. **Agent prompt preamble**: Every agent template includes the Karpathy constraints as a "Behavioral Rules" section
2. **Review phase**: The `overengineering-critic` agent specifically audits against Simplicity First and Surgical Changes
3. **QA phase**: The `code-quality-auditor` checks that every changed line traces to the scope

---

## 2. Workflow Overview

### 2.1 Development Workflow (`/using-zflow`)

```
Phase 0: BRAINSTORM ──► Phase 1: RESEARCH ──► Phase 2: DESIGN ──► Phase 3: REVIEW
     │                       │                      │                     │
     ▼                       ▼                      ▼                     ▼
  scope.md            research-report.md      solution.md          reviewed-solution.md
                                                                         │
                                                    ┌────────────────────┤
                                                    ▼                    ▼
                                            [If UI work detected]  [Non-UI path]
                                            Phase 3.5: UI DESIGN        │
                                                    │                    │
                                                    ▼                    │
                                            ui-design-report.md         │
                                                    │                    │
                                                    ├────────────────────┘
                                                    ▼
                      Phase 4: IMPLEMENT ──► Phase 5: QA ──► Phase 6: DOCUMENT
                           │                      │                  │
                           ▼                      ▼                  ▼
                      impl-report.md         qa-report.md      changelog + commit
                                          (incl. security)
```

**Phase 0 — Brainstorm (Guided Socratic Discovery)**
A specialized brainstorming agent first silently reads the codebase for context, then engages the user through guided multiple-choice questions (with explanations, trade-offs, and recommendations grounded in the actual project). It assesses scope for decomposition, proposes 2-3 solution approaches, then presents the design section-by-section for incremental approval — not as a monolithic dump. Produces `scope.md`. Also detects whether the scope involves UI work and flags it for the Pencil.dev conditional path.

**Phase 1 — Research (Agent Swarm)**
A swarm of parallel research agents fans out across the codebase and documentation to gather real context around the scope. Each agent has a focused research dimension (architecture, dependencies, patterns, tests, related code). If UI work is flagged, an additional `ui-system-scout` agent joins the swarm. Produces `research-report.md`.

**Phase 2 — Design (Approach Selection + Section-by-Section Design)**
A senior architect agent maps research findings against the scope, then proposes 2-3 solution approaches as guided multiple-choice (with pros/cons, effort, risk, and codebase fit). After the user picks an approach, the design is presented section-by-section (architecture → components → data flow → errors → testing → tasks) with user approval at each step. Produces `solution.md`.

**Phase 3 — Review (Multi-Perspective + Spec Self-Review)**
Fresh agents — with no prior context bias — examine scope + solution from multiple viewpoints: gap analysis, over-engineering detection, security review, performance implications, and existing architecture alignment. The coordinator then performs a structural self-review (completeness, consistency, actionability, ambiguity scan). Produces `reviewed-solution.md` with adjustments.

**Phase 3.5 — UI Design (Conditional: Pencil.dev Integration)**
Triggered only when the scope involves UI work. If Pencil.dev MCP tools are available, a UI design agent works with the user to build/refine the interface design on the Pencil canvas before implementation begins. If Pencil.dev is not available, the user is asked whether to install it or proceed without it. See Section 7 for full details.

**Phase 4 — Implement (Parallel Agent Swarm)**
Implementation agents are deployed in parallel, organized by dependency tiers. Tier 0 (no dependencies) runs first, then Tier 1, etc. Each agent gets a focused task slice from the solution. All agents operate under Karpathy's Surgical Changes constraint. Produces working code + `impl-report.md`.

**Phase 5 — QA (Multi-Dimension Agents)**
QA agents run in parallel across dimensions: implementation completeness, user experience, accuracy, code quality, coding standards, design alignment, test coverage, **and deep security vulnerability analysis**. Produces `qa-report.md` with issues categorized by severity.

**Phase 6 — Document & Commit**
A documentation agent updates relevant docs, changelogs, and README files based on everything produced. Then commits the changes with a well-structured commit message.

---

### 2.2 Debugging Workflow (`/using-zflow-debug`)

```
Phase D0: REPRODUCE ──► Phase D1: INVESTIGATE ──► Phase D2: ANALYZE
      │                        │                         │
      ▼                        ▼                         ▼
  repro-report.md        investigation.md          root-cause.md
                                                         │
                                                         ▼
Phase D3: DESIGN FIX ──► Phase D4: IMPLEMENT FIX ──► Phase D5: VERIFY
      │                        │                           │
      ▼                        ▼                           ▼
  fix-design.md           fix-impl-report.md         verification.md
                                                    (incl. security)
```

**Phase D0 — Reproduce**
Agent confirms the bug is reproducible, documents exact reproduction steps, captures error output, and identifies the minimal reproduction case.

**Phase D1 — Investigate (Agent Swarm)**
Parallel investigation agents trace the issue through multiple dimensions: call chain analysis (trace backward from symptom), data flow analysis (follow invalid data to its source), pattern analysis (find similar patterns that may share the bug), history analysis (git blame/log to understand what changed), and **security impact analysis** (assess whether the bug has security implications).

**Phase D2 — Root Cause Analysis**
A deliberation agent synthesizes all investigation findings to identify the true root cause. Must distinguish symptom from cause. Produces a root cause hypothesis with supporting evidence.

**Phase D3 — Design Fix (Multi-Perspective Review)**
Fresh agents review the proposed fix from multiple angles: does it address root cause (not just symptom)? Does it introduce regressions? Is it the minimal effective change (Karpathy: Surgical Changes)? Does it align with existing patterns? **Does it introduce or leave open any security vulnerabilities?**

**Phase D4 — Implement Fix**
Implementation agent applies the fix under Karpathy constraints. If three fix attempts fail (Superpowers' escalation pattern), triggers an architectural review with a senior agent.

**Phase D5 — Verify**
Verification agents confirm: original bug is fixed, no regressions introduced, related patterns are checked, tests pass, edge cases are covered, and **no security vulnerabilities were introduced by the fix**.

---

## 3. Complete File Structure

```
# Repository layout

├── README.md                          # End-user documentation (repo landing page)
├── CLAUDE.md                          # Claude Code behavioral guidelines
├── zflow-design-plan.md               # This file — architecture & design reference
├── evals/                             # Test infrastructure for validating ZFlow
│   ├── evals.json
│   └── files/
│       ├── sample-scope.md
│       └── sample-codebase/
│
└── zflow/                             # Package — copy this to your harness's skills dir
    ├── SKILL.md                       # Main skill entry point — orchestrator
    ├── LICENSE.txt                    # License terms
    │
    ├── skills/                        # Sub-skills (invoked by orchestrator)
    │   ├── zflow-brainstorm/
    │   │   └── SKILL.md               # Socratic brainstorming agent
    │   ├── zflow-research/
    │   │   └── SKILL.md               # Research swarm coordinator
    │   ├── zflow-design/
    │   │   └── SKILL.md               # Solution architect agent
    │   ├── zflow-review/
    │   │   └── SKILL.md               # Multi-perspective review agents
    │   ├── zflow-ui-design/
    │   │   └── SKILL.md               # Pencil.dev UI design coordinator
    │   ├── zflow-implement/
    │   │   └── SKILL.md               # Parallel implementation coordinator
    │   ├── zflow-qa/
    │   │   └── SKILL.md               # QA agent swarm coordinator
    │   ├── zflow-document/
    │   │   └── SKILL.md               # Documentation & commit agent
    │   └── zflow-debug/
    │       └── SKILL.md               # Debugging workflow orchestrator
    │
    ├── agents/                        # Sub-agent prompt templates
    │   │
    │   ├── _shared/
    │   │   └── karpathy-preamble.md   # Behavioral rules injected into ALL agents
    │   │
    │   ├── brainstorm/
    │   │   ├── socratic-interviewer.md
    │   │   └── question-patterns.md
    │   │
    │   ├── research/
    │   │   ├── architecture-scout.md
    │   │   ├── dependency-mapper.md
    │   │   ├── pattern-analyzer.md
    │   │   ├── test-surveyor.md
    │   │   ├── related-code-finder.md
    │   │   └── ui-system-scout.md     # [UI] Conditional
    │   │
    │   ├── design/
    │   │   └── solution-architect.md
    │   │
    │   ├── review/
    │   │   ├── gap-detector.md
    │   │   ├── overengineering-critic.md
    │   │   ├── security-reviewer.md
    │   │   ├── performance-reviewer.md
    │   │   └── alignment-checker.md
    │   │
    │   ├── ui-design/
    │   │   ├── pencil-designer.md
    │   │   ├── design-system-builder.md
    │   │   └── ui-review-agent.md
    │   │
    │   ├── implement/
    │   │   ├── focused-implementer.md
    │   │   └── ui-implementer.md       # [UI] Conditional
    │   │
    │   ├── qa/
    │   │   ├── completeness-checker.md
    │   │   ├── ux-reviewer.md
    │   │   ├── code-quality-auditor.md
    │   │   ├── test-coverage-agent.md
    │   │   ├── design-alignment-qa.md
    │   │   ├── security-auditor.md     # OWASP deep audit
    │   │   └── ui-visual-qa.md         # [UI] Conditional
    │   │
    │   ├── debug/
    │   │   ├── reproducer.md
    │   │   ├── call-chain-tracer.md
    │   │   ├── data-flow-tracer.md
    │   │   ├── pattern-scanner.md
    │   │   ├── history-investigator.md
    │   │   ├── security-impact-assessor.md
    │   │   ├── root-cause-analyst.md
    │   │   ├── fix-designer.md
    │   │   └── fix-verifier.md
    │   │
    │   └── document/
    │       └── documentation-writer.md
    │
    ├── assets/                        # Output document templates
    │   ├── scope.md
    │   ├── approach-proposal.md
    │   ├── research-report.md
    │   ├── solution.md
    │   ├── reviewed-solution.md
    │   ├── ui-design-report.md
    │   ├── implementation-plan.md
    │   ├── impl-report.md
    │   ├── qa-report.md
    │   ├── qa-checklist.md
    │   ├── security-audit-report.md
    │   ├── repro-report.md
    │   ├── investigation.md
    │   ├── root-cause.md
    │   ├── fix-design.md
    │   └── verification.md
    │
    ├── references/
    │   ├── workflow-guide.md
    │   ├── agent-orchestration.md
    │   ├── phase-gates.md
    │   ├── dependency-tiers.md
    │   ├── escalation-patterns.md
    │   ├── karpathy-guidelines.md
    │   ├── pencil-integration.md
    │   ├── security-auth.md
    │   ├── security-config.md
    │   ├── security-crypto.md
    │   ├── security-injection.md
    │   ├── security-patterns-js.md
    │   ├── security-patterns-python.md
    │   └── security-patterns-web.md
    │
    └── scripts/
        ├── init-workspace.sh
        ├── validate-phase.py
        ├── generate-summary.py
        └── check-pencil-availability.sh
```

---

## 4. Detailed Component Design

### 4.1 Main SKILL.md — The Orchestrator

The main `SKILL.md` is the entry point invoked by `/using-zflow`. It:

1. Determines which workflow to run (dev or debug) based on user input
2. Initializes a `.zflow/` workspace directory under the project root
3. Detects Pencil.dev availability for UI workflows
4. Orchestrates phase transitions with human gate checks
5. Manages the document chain (each phase reads previous phase output)
6. Provides status reporting and phase resumption

**Frontmatter:**
```yaml
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
```

The `disable-model-invocation: true` ensures only manual `/using-zflow` invocation triggers the full workflow (it's heavyweight and should be intentional).

### 4.2 Karpathy Preamble — Shared Agent Behavioral Rules

The file `agents/_shared/karpathy-preamble.md` is injected as a prefix into every agent's prompt. It contains:

```markdown
# Behavioral Rules (Required — Applies to All ZFlow Agents)

You MUST follow these rules in addition to your specific mission:

## Think Before Acting
- State your assumptions explicitly before doing anything.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, name what's confusing. Do not guess.

## Simplicity First
- Minimum output that solves the problem. Nothing speculative.
- No features, abstractions, or "flexibility" beyond what was asked.
- No error handling for impossible scenarios.
- If your output is overcomplicated, simplify before submitting.

## Surgical Precision
- Touch only what your mission requires.
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- Every changed line must trace directly to the scope requirements.

## Goal-Driven Verification
- Define success criteria before starting work.
- For each step: what will you do, and how will you verify it worked?
- Format your plan as:
  1. [Step] → verify: [check]
  2. [Step] → verify: [check]

## When In Doubt
- Ask. Don't assume.
- Surface tradeoffs rather than hiding them.
- If you notice unrelated issues, mention them — don't fix them.
```

### 4.3 Workspace Structure (Runtime)

When ZFlow runs, it creates a workspace to track progress:

```
.zflow/
├── current-phase.json        # {"phase": "research", "status": "in_progress"}
├── config.json               # User preferences, gate settings
├── phases/
│   ├── 00-brainstorm/
│   │   ├── scope.md          # Completed brainstorm output
│   │   └── phase-meta.json   # Timing, agent count, status
│   ├── 01-research/
│   │   ├── research-report.md
│   │   ├── agent-reports/    # Individual agent findings
│   │   │   ├── architecture.md
│   │   │   ├── dependencies.md
│   │   │   ├── patterns.md
│   │   │   ├── tests.md
│   │   │   ├── related-code.md
│   │   │   └── ui-system.md  # [conditional: UI work]
│   │   └── phase-meta.json
│   ├── 02-design/
│   │   ├── solution.md
│   │   └── phase-meta.json
│   ├── 03-review/
│   │   ├── reviewed-solution.md
│   │   ├── reviewer-reports/
│   │   │   ├── gaps.md
│   │   │   ├── overengineering.md
│   │   │   ├── security.md
│   │   │   ├── performance.md
│   │   │   └── alignment.md
│   │   └── phase-meta.json
│   ├── 03.5-ui-design/       # [conditional: UI work + Pencil.dev]
│   │   ├── ui-design-report.md
│   │   ├── design-tokens.json
│   │   ├── component-specs.md
│   │   └── phase-meta.json
│   ├── 04-implement/
│   │   ├── implementation-plan.md
│   │   ├── impl-report.md
│   │   ├── task-reports/     # Per-task agent reports
│   │   └── phase-meta.json
│   ├── 05-qa/
│   │   ├── qa-report.md
│   │   ├── dimension-reports/
│   │   │   ├── completeness.md
│   │   │   ├── ux.md
│   │   │   ├── code-quality.md
│   │   │   ├── test-coverage.md
│   │   │   ├── design-alignment.md
│   │   │   ├── security-audit.md    # Deep security findings
│   │   │   └── ui-visual-qa.md      # [conditional: UI work]
│   │   └── phase-meta.json
│   └── 06-document/
│       ├── changes-summary.md
│       └── phase-meta.json
└── debug/                    # Debug workflow runs
    └── session-{timestamp}/
        ├── d0-reproduce/
        ├── d1-investigate/
        │   └── security-impact.md   # Security implications assessment
        ├── d2-analyze/
        ├── d3-design-fix/
        ├── d4-implement-fix/
        └── d5-verify/
```

### 4.4 Agent Prompt Template Design

Each agent prompt in `agents/` follows a consistent structure. The Karpathy preamble is prepended to every agent:

```markdown
{Include: agents/_shared/karpathy-preamble.md}

# Role: {Agent Name}

## Identity
You are a {role description}. You specialize in {specialty}.

## Context
You are part of a ZFlow {phase} phase. You have been deployed alongside
other parallel agents, each with a different focus area.

## Input
{What this agent receives — file paths, scope doc, previous phase output}

## Mission
{Specific, focused task with clear boundaries}

## Method
1. {Step-by-step methodology}
2. {Concrete actions to take}
3. {What to look for specifically}

## Success Criteria (Karpathy: Goal-Driven)
- {Verifiable criteria for this agent's output}
- {How to know the mission is complete}

## Output Format
{Exact structure of the document this agent must produce}

## Anti-Patterns
- {What NOT to do}
- {Common mistakes to avoid}
- Making changes beyond your mission scope (Karpathy: Surgical)
- Adding speculative features (Karpathy: Simplicity First)

## Boundaries
- {What is in scope for this agent}
- {What is explicitly out of scope — defer to other agents}
```

### 4.5 Phase Gate Design

Each phase transition requires:

1. **Artifact Validation**: The output document exists and follows the template structure
2. **Completeness Check**: All required sections are populated (not boilerplate)
3. **Human Gate** (configurable): User reviews and approves before proceeding
4. **Automatic Progression** (optional): For trusted workflows, gates can auto-pass

Gate configuration in `config.json`:
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
  },
  "max_parallel_agents": 5,
  "escalation_threshold": 3
}
```

---

## 5. Detailed Phase Specifications

### 5.1 Phase 0: Brainstorm (Guided Socratic Discovery)

**Agent**: `socratic-interviewer.md`
**Mode**: Interactive (not forked — needs conversation with user)
**Goal**: Transform a vague idea into a crisp, validated design specification through guided exploration

This phase takes heavy inspiration from the Superpowers brainstorming methodology: questions are asked one at a time, prefer multiple-choice format with explanations and recommendations, and the design is presented section-by-section for incremental approval — not dumped as a monolithic document.

#### Step 1: Explore Project Context

Before asking the user anything, the brainstorming agent silently reads the codebase to understand:
- Project structure, tech stack, and architectural patterns
- Existing related features or modules
- Testing patterns and conventions
- README, CLAUDE.md, and any planning docs

This context informs every question the agent asks — questions are grounded in what the project actually looks like, not generic.

#### Step 2: Scope Assessment

The agent's first interaction with the user is to assess scope:
- Restate the user's idea to confirm understanding
- If the request describes **multiple independent subsystems**, flag this immediately and help decompose into sub-projects before proceeding
- Surface any immediate ambiguities (Karpathy: don't pick silently)

#### Step 3: Guided Clarification Questions (One at a Time)

Questions are asked **one at a time**. The agent prefers **multiple-choice format** with explanations, context, and a recommendation — but uses open-ended questions when the topic is genuinely open.

**Multiple-Choice Question Format:**

```
Based on your project's current auth setup (JWT tokens via middleware),
how should we handle permissions for this new feature?

  A) **Role-based access control (RBAC)**
     Add role checks to the existing JWT middleware. Fits your current
     pattern. Best if permissions map cleanly to user roles.
     → Recommended: aligns with your existing auth architecture.

  B) **Attribute-based access control (ABAC)**
     More granular — checks properties of the user, resource, and context.
     More flexible but adds complexity to your middleware layer.
     → Consider if: you need rules like "user can edit only their own
       department's records."

  C) **Simple ownership check**
     Just verify the requesting user owns the resource. No roles needed.
     Minimal change to your codebase.
     → Consider if: this feature only involves users accessing their own data.

  D) **Something else**
     Describe your preferred approach.

My recommendation: (A) — your existing middleware already parses roles
from the JWT, so this requires the least new infrastructure.
```

**Why this format works:**
- Options are grounded in the actual codebase (not generic)
- Each option has a brief explanation of what it means and when it's appropriate
- Trade-offs are surfaced explicitly
- A recommendation is given with reasoning (but user always decides)
- An escape hatch ("Something else") respects user's autonomy

**Open-Ended Question Format** (when truly open):

```
What does "real-time" mean for this feature?

Context: Your project currently uses REST endpoints with polling
intervals of ~5 seconds. Moving to WebSockets or SSE would be a
significant architectural change.

Some possibilities to consider:
- Sub-second updates (would need WebSocket/SSE infrastructure)
- Updates within 5-10 seconds (achievable with your current polling)
- "Fresh on page load" (simplest — just cache invalidation)

What latency would your users actually notice?
```

#### Step 4: Question Dimensions

The agent works through these dimensions, selecting relevant ones based on context (not all are needed for every project):

**Core Dimensions (always explored):**

| Dimension | Example Question Style |
|-----------|----------------------|
| Problem & Users | "Who is this for, and what pain point does it solve?" (open-ended — genuinely different per project) |
| Success Criteria | Multiple-choice: measurable outcomes with suggested metrics based on similar features in codebase |
| Constraints | Multiple-choice: tech stack compatibility, timeline, backward compatibility options with trade-offs |
| Scope Boundaries | Multiple-choice: "Which of these are in scope?" with recommendation for MVP cut |
| Simplest Viable Version | Multiple-choice: present 2-3 scope tiers (minimal / standard / full) with effort estimates (Karpathy: Simplicity First) |

**Conditional Dimensions (explored when relevant):**

| Dimension | Trigger | Example |
|-----------|---------|---------|
| UI Work | Always asked | "Does this feature involve any user interface?" → if yes, follow-up on design system, component library, responsive requirements |
| Data Model | When feature involves storage | Multiple-choice: schema approaches grounded in existing DB patterns |
| API Design | When feature involves endpoints | Multiple-choice: REST vs GraphQL vs RPC, versioning strategy, matching existing patterns |
| Error Handling | When feature involves user-facing operations | Multiple-choice: error recovery strategies with UX implications |
| Migration / Compatibility | When modifying existing features | Multiple-choice: migration strategies with risk assessments |

**Maximum 8-10 questions total**. The agent doesn't ask all dimensions — it picks the ones that matter most based on the project context and the user's initial description. If the user gives detailed upfront context, fewer questions are needed.

#### Step 5: Synthesize Scope Document

After all questions are answered, the agent assembles the findings into a structured `scope.md` and presents it to the user for confirmation. This document captures **what** needs to be built and **why** — but NOT how. The "how" belongs to Phase 2 (Design), which has the benefit of real codebase research from Phase 1.

**Output**: `scope.md` using template with sections: Problem Statement, Success Criteria, Constraints, Affected Systems, Scope Boundaries, MVP Definition, Known Risks, User's Mental Model, **UI Work Flag** (yes/no + design system details if applicable).

**What scope.md intentionally does NOT include** (these belong in later phases):
- Solution approach or architecture (→ Phase 2: Design, after Phase 1 research grounds it in the codebase)
- Component breakdown or data flow (→ Phase 2: Design)
- Implementation details (→ Phase 4: Implement)
- Testing strategy specifics (→ Phase 2: Design)

### 5.2 Phase 1: Research

**Coordinator**: `zflow-research/SKILL.md`
**Agents**: 5 parallel sub-agents (all `context: fork`, `agent: Explore`) + conditional 6th
**Input**: `scope.md`
**Mode**: All agents run in parallel

| Agent | Focus | Key Actions |
|-------|-------|-------------|
| `architecture-scout` | Project structure & architecture | Map directory structure, identify architectural patterns, find entry points |
| `dependency-mapper` | Dependency analysis | Trace imports, identify affected modules, map coupling |
| `pattern-analyzer` | Coding patterns & conventions | Find similar implementations, identify naming conventions, style patterns |
| `test-surveyor` | Test infrastructure | Map test patterns, coverage areas, testing frameworks, fixtures |
| `related-code-finder` | Related/affected code | Find code that will be affected by changes, potential conflicts |
| `ui-system-scout` | **[Conditional: UI flagged]** Design system survey | Survey existing component library, design tokens, CSS architecture, responsive patterns, accessibility standards |

**Output**: Individual agent reports merged into `research-report.md` with sections for each dimension plus a cross-cutting "Key Findings" synthesis.

### 5.3 Phase 2: Design (Approach Selection + Section-by-Section Design)

**Agent**: `solution-architect.md`
**Mode**: Interactive (not forked — needs conversation with user for approach selection and section approval)
**Input**: `scope.md` + `research-report.md`

This phase is where the "how" gets decided. The Design agent has two critical advantages the Brainstorm agent didn't: the full `research-report.md` with real codebase context, and the user-validated scope. The methodology follows the Superpowers pattern of proposing approaches and presenting design incrementally.

#### Step 1: Propose 2-3 Approaches (Guided Multiple-Choice)

The architect agent maps scope requirements against research findings, then proposes 2-3 solution approaches — not as a single chosen path, but as options grounded in the actual codebase with trade-offs:

```
Based on your scope and what the research agents found in your codebase,
here are three approaches:

## Approach A: Extend Existing Service (Recommended)
Add the notification logic to your existing EventService.
- Pros: No new services, fits current architecture, fastest to implement
- Cons: EventService grows larger, may need refactoring later
- Effort: Small (2-3 files changed)
- Risk: Low
- Codebase fit: EventService already handles 4 similar event types

## Approach B: New Notification Microservice
Create a standalone NotificationService with its own queue.
- Pros: Clean separation, independently deployable, scalable
- Cons: New infrastructure (message queue), more complex deployment
- Effort: Medium (new service + integration)
- Risk: Medium (new infrastructure)
- Codebase fit: No existing message queue infrastructure found

## Approach C: Event-Driven with Existing Queue
Use your existing Redis pub/sub to broadcast events, add listeners.
- Pros: Leverages existing infrastructure, loosely coupled
- Cons: Redis pub/sub is fire-and-forget (no guaranteed delivery)
- Effort: Small-Medium (new listeners, reuse infra)
- Risk: Low-Medium (delivery guarantees)
- Codebase fit: Redis already used for caching in 3 services

I recommend Approach A because your EventService already handles
similar patterns and the research shows no scaling concerns at your
current load. Which approach resonates, or would you like a hybrid?
```

**For each alternative, assess: which is simplest? Prefer it unless complexity is justified** (Karpathy: Simplicity First).

#### Step 2: Present Design Section-by-Section

Once the user picks an approach, the architect presents the detailed design **incrementally, one section at a time** — not as a monolithic document dump. Each section is scaled to its complexity (a few sentences if straightforward, up to 200-300 words if nuanced). User approves each section before the next is presented.

**Section sequence:**

1. **Architecture Overview** — high-level structure, how it fits in the existing system
   → *"Does this structure make sense? Any concerns?"*

2. **Component Breakdown** — what gets created/modified, responsibilities of each
   → *"Are these the right boundaries between components?"*

3. **Data Flow** — how data moves through the system, state management
   → *"Does this flow handle your edge cases?"*

4. **Error Handling & Edge Cases** — failure modes, recovery strategies
   → *"Are there failure scenarios I'm missing?"*

5. **Testing Strategy** — what gets tested, how, test categories
   → *"Does this coverage feel sufficient?"*

6. **If UI: Interface Design** — component hierarchy, interactions, responsive behavior
   → *"Does this match your vision for the UI?"*

7. **Task Breakdown with Dependencies** — implementation tasks, dependency graph, per-task success criteria
   → *"Does this sequencing make sense? Anything missing?"*

Disagreements are resolved before moving to the next section. This prevents the failure mode of a user rubber-stamping a 500-line design doc they didn't read.

#### Step 3: Assemble Solution Document

After all sections are approved, the agent assembles them into `solution.md`:

1. Compile all approved sections into a coherent document
2. Add: Approach Summary, Alternatives Considered (with rejection rationale)
3. Ensure implementation tasks have dependency graph + per-task success criteria (Karpathy: Goal-Driven)
4. Estimate complexity per task (S/M/L)
5. Compile Risk Register from concerns raised during section reviews
6. List Open Questions (anything the user flagged as "decide later")
7. **If UI work: include component breakdown, state management approach, and design-to-code mapping**

**Output**: `solution.md` with sections: Chosen Approach (with rationale), Alternatives Considered, Architecture Overview, Component Breakdown, Data Flow, Error Handling, Testing Strategy, Task Breakdown (with dependency graph + success criteria per task), Risk Register, Open Questions.

### 5.4 Phase 3: Review (Multi-Perspective + Spec Self-Review)

**Coordinator**: `zflow-review/SKILL.md`
**Agents**: 5 parallel sub-agents (all `context: fork`) + coordinator self-review
**Input**: `scope.md` + `solution.md`
**Critical**: These agents do NOT receive research-report.md — they bring fresh eyes

#### Step 1: Parallel Multi-Perspective Review

| Agent | Perspective | Key Questions |
|-------|------------|---------------|
| `gap-detector` | Completeness | What requirements aren't addressed? What edge cases are missed? |
| `overengineering-critic` | **Simplicity (Karpathy enforcer)** | What can be simplified? What's YAGNI? What adds complexity without value? Would a senior engineer say this is overcomplicated? Are there abstractions for single-use code? |
| `security-reviewer` | Security | What attack vectors? What data exposure? What auth gaps? |
| `performance-reviewer` | Performance | What bottlenecks? What scaling concerns? What resource usage? |
| `alignment-checker` | Architecture | Does it fit existing patterns? Does it create tech debt? Consistent naming? |

#### Step 2: Spec Self-Review (Coordinator)

After merging reviewer findings, the coordinator performs a structural integrity check on the solution document:
- **Completeness**: No "TBD", "TODO", or incomplete sections remain
- **Internal consistency**: Architecture section doesn't contradict data flow; component responsibilities don't overlap
- **Scope alignment**: Solution hasn't drifted beyond what `scope.md` defined
- **Actionability**: Every section is specific enough that a downstream implementation agent could act on it without guessing
- **Ambiguity scan**: Flag requirements that could be interpreted multiple ways
- **Task coverage**: Every component in the design maps to at least one implementation task

Any self-review issues are fixed inline and noted in the output.

#### Step 3: Produce Reviewed Solution

**Output**: `reviewed-solution.md` — the original solution with adjustments applied, plus an appendix containing: all reviewer findings, which were accepted/rejected with rationale, and any self-review fixes applied.

---

### 5.5 Phase 3.5: UI Design (Conditional — Pencil.dev Integration)

**Trigger**: Only when `scope.md` has `ui_work: true`
**Coordinator**: `zflow-ui-design/SKILL.md`

#### Decision Flow

```
scope.md has ui_work: true?
    │
    ├── No → Skip to Phase 4
    │
    └── Yes → Check Pencil.dev MCP tools available?
                │
                ├── Yes → Full Pencil.dev UI design flow
                │
                └── No → Ask user:
                          "Your scope includes UI work. Pencil.dev enables
                           design-first development with a visual canvas.
                           Would you like to:"
                          [A] Install Pencil.dev and use design-first flow
                          [B] Proceed without it (standard code-first UI)
                          │
                          ├── [A] → Guide install → Full Pencil.dev flow
                          └── [B] → Standard implementation (no Phase 3.5)
```

#### Full Pencil.dev Flow (When Available)

**Sub-Phase 3.5a — Design System Setup**

Agent: `design-system-builder.md`

1. Check if the project already has a design system (from `ui-system-scout` research)
2. If existing: Extract tokens and component patterns via Pencil MCP tools
   - `get_variables` → read existing design tokens
   - `get_guidelines` → load style archetypes
3. If new: Work with user to establish:
   - Color palette (primary, secondary, neutral, semantic)
   - Typography scale (font families, sizes, weights)
   - Spacing system (4px/8px grid)
   - Component library choice (Shadcn, custom, etc.)
   - Responsive breakpoints
4. Set up design tokens in Pencil via `set_variables`

**Sub-Phase 3.5b — UI Design on Canvas**

Agent: `pencil-designer.md`

1. Open the `.pen` file for the feature via `open_document`
2. For each screen/component in the solution:
   - Find empty canvas space via `find_empty_space_on_canvas`
   - Design the component using `batch_design` with proper tokens
   - Use design system components (reusable instances via `ref`)
3. Present screenshots to user via `get_screenshot` for approval
4. Iterate based on user feedback
5. Capture final layouts via `snapshot_layout`

**Sub-Phase 3.5c — Design Review**

Agent: `ui-review-agent.md`

1. Take screenshots of all designed screens via `get_screenshot`
2. Review against:
   - Accessibility (contrast ratios, touch targets, screen reader flow)
   - Responsiveness (does the layout logic work at all breakpoints?)
   - Consistency (do all screens use the same tokens and patterns?)
   - Design system compliance (no off-system values)
3. Check for overlaps/clipping via `snapshot_layout`
4. Export approved designs via `export_nodes` for implementation reference

**Output**: `ui-design-report.md` containing: design system tokens, component specifications, screen-by-screen layout descriptions, exported reference images, implementation notes for each component, and accessibility requirements.

#### Standard Flow (Without Pencil.dev)

If the user chooses [B], Phase 3.5 is skipped entirely. The implementation agents will work from the text-based component specifications in `reviewed-solution.md` using a code-first approach. The `ui-implementer.md` agent will still be used but will work without visual design references.

---

### 5.6 Phase 4: Implement

**Coordinator**: `zflow-implement/SKILL.md`
**Agents**: N parallel implementation agents (grouped by dependency tier)
**Input**: `reviewed-solution.md` + optionally `ui-design-report.md`

**Dependency Tier System:**
```
Tier 0: Tasks with no dependencies          → Run in parallel
         ↓ (wait for all Tier 0 complete)
Tier 1: Tasks depending only on Tier 0      → Run in parallel
         ↓ (wait for all Tier 1 complete)
Tier 2: Tasks depending on Tier 0 or 1      → Run in parallel
         ↓ ...and so on
```

Each implementation agent receives:
- The specific task description from the solution
- The relevant section of the solution design
- **Verifiable success criteria for their task** (Karpathy: Goal-Driven)
- File paths to work on (from research phase)
- Coding conventions (from pattern analysis)
- Related test patterns (from test survey)
- **The Karpathy preamble** (Surgical Changes constraint)
- **If UI task: the relevant section of `ui-design-report.md`** with design tokens and component specs

**UI-specific implementation**: When a task involves UI components and Pencil.dev designs exist, the `ui-implementer.md` agent receives the exported screenshots and component specs from Phase 3.5. It implements pixel-perfect to the design, using the exact design tokens.

**Output**: Working code changes + `impl-report.md` listing each task's status, files changed, and any deviations from the design (Karpathy: every deviation must be justified).

### 5.7 Phase 5: QA

**Coordinator**: `zflow-qa/SKILL.md`
**Agents**: 6 parallel QA agents (7 if UI work)
**Input**: `reviewed-solution.md` + `impl-report.md` + actual code changes

| Agent | Dimension | Checklist Focus |
|-------|-----------|-----------------|
| `completeness-checker` | Implementation completeness | Every task from solution is implemented; no partial implementations |
| `ux-reviewer` | User experience | API ergonomics, error messages, edge case handling, documentation |
| `code-quality-auditor` | Code quality **(Karpathy enforcer)** | Linting, naming, complexity, duplication, error handling, logging. **Also enforces**: every changed line traces to scope; no speculative features; no unnecessary abstractions |
| `test-coverage-agent` | Test coverage | All new code has tests; edge cases covered; test quality |
| `design-alignment-qa` | Design alignment | Implementation matches the reviewed solution; no drift |
| **`security-auditor`** | **Deep security analysis** | **Full OWASP Top 10 2025 audit — see Section 8** |
| `ui-visual-qa` | **[Conditional: UI work]** Visual QA | Design fidelity against Pencil.dev exports; responsive behavior; accessibility |

**Output**: `qa-report.md` with issues categorized as:
- **Critical (Security)**: Security vulnerability — must fix immediately
- **Blocker**: Must fix before merge
- **Major**: Should fix; creates technical debt if not
- **Minor**: Nice to fix; cosmetic or stylistic
- **Note**: Observation for future consideration

**Gate**: If critical or blocker issues exist, loop back to Phase 4 for targeted fixes (not full re-implementation). Security criticals get priority.

### 5.8 Phase 6: Document & Commit

**Agent**: `documentation-writer.md`
**Mode**: `context: fork`
**Input**: Full chain — `scope.md` through `qa-report.md`

**Actions:**
1. Update/create relevant documentation (README, API docs, inline comments)
2. Update CHANGELOG with a well-structured entry
3. Generate a commit message following conventional commits
4. Stage changes and commit (with human approval gate)
5. **If security findings were addressed: note them in CHANGELOG under Security section**

---

## 6. Debugging Workflow Specifications

### 6.1 Phase D0: Reproduce

**Agent**: `reproducer.md`
**Mode**: Interactive (needs to run code, observe output)

1. Understand the reported bug from user description
2. Identify the minimal reproduction steps
3. Execute reproduction and capture actual vs. expected behavior
4. Document environment, inputs, and exact error output
5. Classify: crash, wrong output, performance, intermittent, security vulnerability, etc.

**Output**: `repro-report.md`

### 6.2 Phase D1: Investigate (Agent Swarm)

**Agents**: 5 parallel investigators (expanded from 4 — added security)
**Input**: `repro-report.md`

| Agent | Focus |
|-------|-------|
| `call-chain-tracer` | Trace execution backward from the symptom to find where things go wrong |
| `data-flow-tracer` | Follow the invalid/corrupted data backward to find where it was introduced |
| `pattern-scanner` | Search codebase for similar patterns that may share the same bug |
| `history-investigator` | Git blame/log analysis — what changed recently? Any relevant commits? |
| **`security-impact-assessor`** | **Assess whether this bug has security implications: can it be exploited? Does it expose data? Does it bypass auth? What's the blast radius from a security perspective?** |

**Output**: Individual investigation reports merged into `investigation.md`

### 6.3 Phase D2: Root Cause Analysis

**Agent**: `root-cause-analyst.md`
**Mode**: `context: fork`, `agent: Plan`
**Input**: `repro-report.md` + `investigation.md`

**Iron Law**: Must distinguish SYMPTOM from CAUSE. The root cause is the earliest point in the chain where the correct behavior diverges.

**Methodology (with Karpathy Think-Before-Coding):**
1. State assumptions about what's happening before analyzing (Karpathy)
2. Map the causal chain from root to symptom
3. Identify the specific line(s) of code where the defect lives
4. Explain WHY the defect exists (misunderstanding, race condition, missing check, etc.)
5. Assess blast radius — what else is affected?
6. **Assess security impact** — if the `security-impact-assessor` flagged concerns, factor them into the root cause analysis
7. Confidence level: High / Medium / Low (if Low, recommend more investigation)

**Output**: `root-cause.md`

### 6.4 Phase D3: Design Fix (Multi-Perspective)

**Agents**: 3 parallel reviewers reviewing the proposed fix design
**Input**: `root-cause.md`

- **Minimal Fix Agent**: Design the smallest possible fix that addresses root cause (Karpathy: Surgical Changes — minimum change that solves the problem)
- **Regression Reviewer**: Identify potential regressions from the proposed fix
- **Pattern Fix Agent**: If pattern-scanner found similar issues, design a systematic fix

**Output**: `fix-design.md`

### 6.5 Phase D4: Implement Fix

**Agent**: `focused-implementer.md` (with Karpathy preamble)
**Input**: `fix-design.md`

**Escalation Pattern** (from Superpowers):
- Attempt 1: Implement the designed fix
- Attempt 2: If tests still fail, re-analyze with fresh context
- Attempt 3: If still failing, escalate to architectural review with a senior agent
- After 3 failures: Pause and surface to the user with full context

**Karpathy enforcement**: Each attempt must define success criteria before starting. Every changed line must trace to the fix design.

**Output**: Code changes + `fix-impl-report.md`

### 6.6 Phase D5: Verify

**Agents**: 4 parallel verifiers (expanded from 3 — added security)
**Input**: All previous debug phase outputs + code changes

- **Regression Verifier**: Run full test suite, verify no new failures
- **Fix Verifier**: Confirm original bug reproduction steps now pass
- **Pattern Verifier**: If similar patterns were fixed, verify those too
- **Security Verifier**: If security impact was flagged, confirm the fix doesn't introduce new vulnerabilities and properly addresses any security concerns from the impact assessment

**Output**: `verification.md`

---

## 7. Pencil.dev Integration — Full Specification

### 7.1 Why Pencil.dev for UI Work?

Traditional agent-driven UI development suffers from "code-first blindness" — agents write CSS and markup without seeing the result, leading to misaligned spacing, inconsistent tokens, and accessibility gaps. Pencil.dev provides a visual canvas where the design can be created, reviewed, and approved before a single line of implementation code is written.

Key integration points:
- `.pen` files are JSON and live in the repo (version-controlled like code)
- MCP tools give agents full read/write access to the design canvas
- Design tokens (variables) can be extracted and injected into implementation code
- Screenshots provide visual verification at every stage

### 7.2 MCP Tool Usage Map

| Phase | Tool | Purpose |
|-------|------|---------|
| Research | `get_variables`, `get_guidelines` | Survey existing design system |
| UI Design | `open_document` | Open/create `.pen` file |
| UI Design | `find_empty_space_on_canvas` | Find space for new designs |
| UI Design | `batch_design` | Create screens and components |
| UI Design | `set_variables` | Set/update design tokens |
| UI Design | `get_screenshot` | Present designs to user |
| UI Design | `snapshot_layout` | Validate layout structure |
| UI Design | `export_nodes` | Export designs for implementation reference |
| QA | `get_screenshot` | Compare implementation to design |
| QA | `batch_get` | Read design specs for comparison |
| QA | `snapshot_layout` | Check for layout issues |

### 7.3 Availability Detection

The orchestrator detects Pencil.dev availability by checking for `mcp__pencil__` prefixed tools at runtime. The `check-pencil-availability.sh` script provides a quick check.

### 7.4 Graceful Degradation

When Pencil.dev is not available and the user declines to install it:
- Phase 3.5 is skipped entirely
- The `solution-architect` in Phase 2 includes more detailed text-based component specs
- The `ui-implementer` works from text descriptions instead of visual designs
- The `ui-visual-qa` agent is skipped (no design reference to compare against)
- The `ux-reviewer` agent gets expanded scope to cover basic visual consistency

---

## 8. Deep Security Vulnerability Analysis — Full Specification

### 8.1 Philosophy

Security is not a checkbox. The ZFlow security audit is a deep, systematic analysis performed by a specialized agent that thinks like an attacker. It is modeled on professional penetration testing methodology adapted for static code review, grounded in the OWASP Top 10 2025 framework.

### 8.2 The `security-auditor.md` Agent

This is a dedicated QA agent that runs in parallel with other QA agents during Phase 5. It receives the full code changes, the scope document, and the solution design.

**Agent Identity**: You are a senior application security engineer and penetration tester. You think like an attacker. Your job is not to rubber-stamp code but to find every way it can be exploited, abused, or made to behave unexpectedly.

### 8.3 OWASP Top 10 2025 Audit Checklist

The security auditor follows this systematic checklist, organized by the 2025 OWASP rankings:

#### A01: Broken Access Control (Rank #1)
**What to scan for:**
- Direct object reference vulnerabilities (IDOR) — can user A access user B's resources by changing an ID?
- Missing access control checks on API endpoints
- Horizontal privilege escalation (same role, different user's data)
- Vertical privilege escalation (user accessing admin functions)
- CORS misconfiguration (`Access-Control-Allow-Origin: *` with credentials)
- Server-Side Request Forgery (SSRF) — application making HTTP requests to user-controlled URLs

**Verification method:**
- Trace authorization checks before ALL data access operations
- Confirm object ownership validation (requesting user must own the resource)
- Check role/permission validation per endpoint
- Verify CORS headers are restrictive

#### A02: Security Misconfiguration (Rank #2)
**What to scan for:**
- Default credentials still enabled
- Verbose error messages exposing stack traces, file paths, SQL queries
- Missing security headers (CSP, X-Frame-Options, HSTS, X-Content-Type-Options)
- Debug mode enabled in production configuration
- Exposed configuration with secrets
- Unnecessary services/ports open

**Verification method:**
- Search for default credentials patterns
- Check error handling returns generic messages to users
- Verify security headers are set in response middleware
- Confirm debug=false in production configs

#### A03: Software Supply Chain Failures (Rank #3)
**What to scan for:**
- Dependencies with known CVEs (run `npm audit` / `pip-audit` / equivalent)
- Outdated/unmaintained dependencies
- Untrusted package sources
- Missing lock files
- No integrity verification on dependencies
- Typosquatting risk in package names

**Verification method:**
- Execute dependency audit commands
- Check package publish dates and maintainer reputation
- Verify lock files exist and are committed
- Check for unusual or suspicious package names

#### A04: Cryptographic Failures (Rank #4)
**What to scan for:**
- Weak hashing algorithms (MD5, SHA1 for passwords)
- Hardcoded encryption keys or salts
- Missing encryption for sensitive data at rest
- Missing TLS enforcement
- Predictable random number generation (`Math.random()` for security-critical values)
- Poor key management

**Verification method:**
- Search for MD5/SHA1 usage in auth contexts
- Search for hardcoded key patterns (long hex/base64 strings in source)
- Confirm passwords use bcrypt/scrypt/Argon2 with adequate cost
- Verify HTTPS enforcement and HSTS

#### A05: Injection (Rank #5)
**What to scan for:**
- SQL injection (string concatenation in queries)
- NoSQL injection (user input in query operators)
- OS command injection (user input in exec/system calls)
- XSS — reflected, stored, and DOM-based
- Template injection
- LDAP/XPath injection
- **LLM prompt injection** (if AI features: user input flowing into model prompts)

**Verification method:**
- Trace ALL user input from entry point to query/command execution
- Confirm parameterized queries/prepared statements
- Verify output encoding is context-appropriate (HTML/JS/URL/CSS)
- Check for `dangerouslySetInnerHTML`, `innerHTML`, `eval()`, `exec()`

#### A06: Insecure Design (Rank #6)
**What to scan for:**
- Business logic flaws (can steps be skipped? can limits be bypassed?)
- Race conditions and TOCTOU (time-of-check/time-of-use)
- Missing rate limiting on sensitive operations
- Insufficient input validation for business rules
- Missing anti-automation controls

**Verification method:**
- Review business logic flows for authorization at each step
- Check for atomic operations on financial/sensitive changes
- Verify rate limiting exists on login, signup, API calls
- Test workflow cannot be bypassed via direct API calls

#### A07: Authentication Failures (Rank #7)
**What to scan for:**
- Weak password requirements
- Missing brute-force protection (no lockout/rate limit)
- Insecure session management (predictable tokens, no expiration)
- Missing MFA where needed
- Credential recovery flaws (user enumeration via "forgot password")
- Hardcoded credentials

**Verification method:**
- Check password policy >= 12 chars with complexity
- Confirm lockout after N failed attempts
- Verify session tokens are cryptographically random, have expiration
- Check no credentials in logs or error responses

#### A08: Software/Data Integrity Failures (Rank #8)
**What to scan for:**
- Insecure deserialization of untrusted data
- Missing integrity checks on critical data
- CI/CD pipeline security gaps
- Auto-update without verification
- Unsigned artifacts

**Verification method:**
- Search for `pickle.loads()`, `ObjectInputStream`, `unserialize()` with untrusted input
- Verify integrity checks on external data
- Check CI/CD config for security (no secrets in plain text, restricted permissions)

#### A09: Logging & Alerting Failures (Rank #9)
**What to scan for:**
- Missing logging of security-relevant events (login, access denied, privilege changes)
- Secrets in log output (passwords, tokens, API keys)
- Insufficient log context for incident response
- Log injection vulnerabilities
- No alerting on suspicious patterns

**Verification method:**
- Confirm auth events are logged with: timestamp, user, action, resource, result
- Search for sensitive data in log statements
- Verify log output is sanitized (no injection)

#### A10: Mishandling of Exceptional Conditions (Rank #10)
**What to scan for:**
- "Failing open" — defaulting to allow on error
- Silently swallowed exceptions (`catch: pass`)
- Sensitive information in error responses
- Unhandled exceptions in critical paths
- Missing boundary validation (null, empty, max values)

**Verification method:**
- Check all catch blocks actually handle the error
- Verify errors fail securely (deny by default)
- Confirm error messages are generic to users, detailed only in server logs

### 8.4 Additional Security Checks (Beyond OWASP)

#### Secrets & Credentials Exposure
- Scan for API keys, passwords, tokens in source (`/[a-zA-Z0-9]{32,}/` patterns)
- Check `.env` files are in `.gitignore`
- Verify no secrets in configuration files committed to repo
- Search for common credential patterns: `api_key=`, `password=`, `secret=`, `token=`, `AWS_`

#### CSRF Protection
- Verify CSRF tokens on all state-changing requests (POST/PUT/DELETE)
- Check SameSite cookie attribute
- Verify token validation on server side

#### File Upload Security
- Check file type validation (not just extension — check magic bytes)
- Verify upload size limits
- Confirm uploaded files are not served from application domain
- Check for path traversal in file names

#### API Security
- Rate limiting on all endpoints
- Input validation and size limits
- Proper HTTP method enforcement
- API versioning for breaking changes
- No sensitive data in URL parameters

### 8.5 Security Audit Output Format

The `security-audit-report.md` template:

```markdown
# Security Audit Report

## Executive Summary
- Total findings: {N}
- Critical: {N} | High: {N} | Medium: {N} | Low: {N} | Informational: {N}
- OWASP categories with findings: {list}

## Findings

### [SEV-001] {Finding Title}
- **Severity**: Critical / High / Medium / Low / Informational
- **OWASP Category**: A01-A10
- **Location**: `file:line`
- **Description**: What was found
- **Attack Scenario**: How this could be exploited
- **Evidence**: Code snippet showing the vulnerability
- **Remediation**: Specific fix with code example
- **Verification**: How to confirm the fix works

### [SEV-002] ...

## Clean Categories
OWASP categories reviewed with no findings: {list}

## Dependency Audit
- Command run: {e.g., npm audit}
- Results: {summary}
- Vulnerabilities found: {list with severity}

## Recommendations
- Immediate actions (Critical/High findings)
- Short-term improvements
- Long-term security posture enhancements
```

### 8.6 Security in the Debug Workflow

The `security-impact-assessor.md` agent in debug Phase D1 follows a focused subset:

1. **Can this bug be triggered by an attacker?** (Is it reachable from untrusted input?)
2. **What's the worst-case exploit?** (Data breach? Privilege escalation? Denial of service?)
3. **Is this bug already being exploited?** (Check logs for suspicious patterns)
4. **Does the fix introduce new attack surface?** (Preview of fix security implications)

If the security impact is rated High or Critical, the bug is flagged for expedited handling and the fix design must include security review.

---

## 9. Key Design Decisions & Rationale

### 9.1 Why Sub-Skills Instead of One Monolithic SKILL.md?

A single SKILL.md with all 7 phases would be 2000+ lines — far beyond the recommended 500-line limit. By splitting into sub-skills under `skills/`, each phase is self-contained, independently testable, and can be invoked standalone (e.g., `/using-zflow-debug` for just debugging).

### 9.2 Why Agent Prompt Templates in `agents/` Instead of Inline?

Agent prompts are 50-150 lines each. With 25+ agents, inlining them bloats the skill files. Keeping them in `agents/` follows the progressive disclosure pattern: the coordinator SKILL.md references them, and they're loaded on-demand when spawning sub-agents.

### 9.3 Why Templates for Output Documents?

Templates ensure consistency across runs and make it easy for downstream phases to parse upstream outputs. They also serve as implicit contracts between phases.

### 9.4 Why `disable-model-invocation: true`?

The full ZFlow workflow is heavyweight (potentially 25+ sub-agent spawns). It should only run when the user explicitly invokes `/using-zflow`, not when Claude thinks it might be helpful.

### 9.5 Why Fresh Agents for Review (Phase 3)?

Giving review agents the research report would anchor them to the same context as the design agent. By only giving them scope + solution, they bring a fresh perspective and are more likely to catch assumptions baked into the research-influenced design.

### 9.6 Why Karpathy Guidelines as a Shared Preamble?

Embedding behavioral rules into individual agent prompts would lead to inconsistency and maintenance burden. A single `karpathy-preamble.md` file ensures every agent gets identical behavioral constraints, and updating the rules means changing one file.

### 9.7 Why Pencil.dev as a Conditional Phase, Not Always Required?

Not all projects need UI work. Not all developers have Pencil.dev installed. Making it conditional respects both realities while providing the best possible workflow when it IS available. The graceful degradation to text-based specs means no functionality is lost — only visual fidelity of the design-first approach.

### 9.8 Why a Dedicated Security Auditor Instead of Expanding Existing Agents?

Security requires adversarial thinking — the opposite of a developer's mindset. Mixing security concerns into a code-quality agent dilutes both. A dedicated `security-auditor` agent with its own OWASP-aligned checklist, attack-scenario thinking, and specific output format produces significantly more thorough findings than a generalist agent with "also check for security issues" tacked on.

---

## 10. Agent Orchestration Patterns

### 10.1 Parallel Fan-Out

Used in: Research, Review, QA, Debug Investigation

```
Coordinator reads phase input
    ├── Spawn Agent A (context: fork) ──► Report A
    ├── Spawn Agent B (context: fork) ──► Report B
    ├── Spawn Agent C (context: fork) ──► Report C
    └── Spawn Agent D (context: fork) ──► Report D
              │
              ▼
    Coordinator merges reports into phase output
```

All agents in a fan-out are spawned in the SAME message (single tool-use block with multiple Agent calls) to maximize parallelism.

### 10.2 Tiered Fan-Out

Used in: Implementation

```
Coordinator builds dependency graph from solution
    │
    ├── Tier 0: Spawn agents for independent tasks ──► Wait for all
    │       │
    │       ▼
    ├── Tier 1: Spawn agents for Tier-0-dependent tasks ──► Wait for all
    │       │
    │       ▼
    └── Tier N: Continue until all tasks complete
```

### 10.3 Sequential Handoff

Used in: Phase-to-phase transitions

```
Phase N completes ──► Validate output ──► Human gate ──► Phase N+1 reads output
```

### 10.4 Conditional Branch

Used in: UI Design phase

```
Scope flag: ui_work?
    │
    ├── No  → Skip to Phase 4
    └── Yes → Pencil.dev available?
                ├── Yes → Phase 3.5 (full UI design)
                └── No  → Ask user → Install or Skip
```

### 10.5 Escalation Loop

Used in: Debug fix implementation

```
Attempt fix ──► Run tests ──► Pass? ──► Done
                    │
                    ▼ Fail
              Attempt < 3? ──► Yes ──► Re-analyze + retry
                    │
                    ▼ No
              Escalate to senior agent / surface to user
```

---

## 11. Configuration & Customization

### 11.1 User-Configurable Options

Users can customize ZFlow behavior via `.zflow/config.json`:

```json
{
  "workflow": {
    "gates": {
      "brainstorm": "human",
      "research": "auto",
      "design": "human",
      "review": "human",
      "ui_design": "human",
      "implement": "auto",
      "qa": "human",
      "document": "auto"
    },
    "skip_phases": [],
    "max_parallel_agents": 5
  },
  "ui": {
    "pencil_enabled": "auto",
    "design_system": null,
    "component_library": null
  },
  "security": {
    "audit_depth": "full",
    "owasp_categories": "all",
    "dependency_scan": true,
    "secrets_scan": true,
    "security_severity_threshold": "medium"
  },
  "debug": {
    "escalation_threshold": 3,
    "auto_run_tests": true,
    "security_impact_assessment": true,
    "gates": {
      "reproduce": "auto",
      "investigate": "auto",
      "analyze": "human",
      "design_fix": "human",
      "implement_fix": "auto",
      "verify": "auto"
    }
  },
  "karpathy": {
    "simplicity_enforcement": "strict",
    "surgical_changes_enforcement": "strict",
    "require_success_criteria": true
  },
  "preferences": {
    "commit_style": "conventional",
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "language": "typescript"
  }
}
```

### 11.2 Phase Skipping

For smaller tasks, users can skip phases:
- Quick fix: Skip brainstorm, research → jump to design
- Known bug: Skip reproduce → jump to investigate
- Already designed: Skip brainstorm, research, design → jump to review
- Non-UI work: Phase 3.5 auto-skipped

### 11.3 Security Configuration

The security audit can be configured:
- `audit_depth`: "full" (all OWASP categories) | "targeted" (only categories relevant to changed code) | "minimal" (top 5 only)
- `owasp_categories`: "all" | array of specific categories like ["A01", "A05", "A07"]
- `dependency_scan`: whether to run `npm audit` / `pip-audit` etc.
- `secrets_scan`: whether to scan for hardcoded credentials
- `security_severity_threshold`: minimum severity to report ("critical" | "high" | "medium" | "low")

---

## 12. Implementation Priority & Roadmap

### MVP (Phase 1 — Build First)
1. Main `SKILL.md` orchestrator with phase management
2. `karpathy-preamble.md` shared behavioral rules
3. Brainstorm skill + socratic interviewer agent
4. Research skill + 3 core research agents (architecture, patterns, related-code)
5. Design skill + solution architect agent
6. Implement skill + focused implementer agent
7. All output templates
8. `workflow-guide.md` reference

### Enhancement (Phase 2)
9. Review skill + 5 reviewer agents
10. QA skill + 5 QA agents (without security auditor initially)
11. Document skill + documentation writer agent
12. Phase gates with human-in-the-loop
13. Workspace initialization script

### Security Integration (Phase 3)
14. `security-auditor.md` agent with full OWASP checklist
15. `security-auth.md`, `security-config.md`, `security-crypto.md`, `security-injection.md` — OWASP category reference documents
16. `security-patterns-js.md`, `security-patterns-python.md`, `security-patterns-web.md` — language-specific patterns
17. `security-audit-report.md` template
18. `security-impact-assessor.md` for debug workflow
19. Security verification agent for debug Phase D5

### UI & Pencil.dev Integration (Phase 4)
20. `zflow-ui-design/SKILL.md` coordinator
21. `pencil-designer.md`, `design-system-builder.md`, `ui-review-agent.md`
22. `ui-implementer.md` implementation agent
23. `ui-visual-qa.md` QA agent
24. `ui-system-scout.md` research agent
25. `pencil-integration.md` reference
26. `check-pencil-availability.sh` script

### Debug Workflow (Phase 5)
27. Debug orchestrator skill
28. Reproduce + investigation agents (including security-impact-assessor)
29. Root cause analyst
30. Fix design + implementation with escalation
31. Verification agents (including security verifier)

### Polish (Phase 6)
32. Configuration system (`config.json`)
33. Phase resumption (pick up where you left off)
34. Eval test suite
35. Summary report generation script
36. Description optimization for triggering accuracy
37. `karpathy-guidelines.md` reference with ZFlow-specific annotations

---

## 13. Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Skill directories | `zflow-{phase}` | `zflow-research` |
| Agent prompts | `{role-name}.md` | `architecture-scout.md` |
| Shared agent files | `_shared/{name}.md` | `_shared/karpathy-preamble.md` |
| Templates | `{output-name}.md` | `scope.md` |
| Phase outputs | `{descriptive-name}.md` | `research-report.md` |
| Workspace dirs | `{NN}-{phase}/` | `01-research/` |
| Config files | `{name}.json` | `config.json` |
| Scripts | `{verb}-{noun}.{ext}` | `validate-phase.py` |
| Security findings | `SEV-{NNN}` | `SEV-001` |

---

## 14. Risk Assessment

| Risk | Mitigation |
|------|-----------|
| Token cost from many sub-agents | Configurable `max_parallel_agents`; agents use `agent: Explore` (fast) where possible |
| Context loss between phases | Document chain ensures all context is persisted in files |
| Sub-agent quality variance | Highly structured agent prompts + Karpathy preamble for consistency |
| Workflow too heavyweight for small tasks | `disable-model-invocation: true` + phase skipping |
| Agents doing redundant work | Clear scope boundaries in each agent prompt |
| Output template drift | Validation script checks structure before phase transitions |
| Karpathy rules ignored by agents | Enforced at 3 levels: preamble, review agent, QA agent |
| Pencil.dev not available | Graceful degradation to text-based specs, user prompted for choice |
| Security audit too noisy (false positives) | Configurable severity threshold + require attack scenario for each finding |
| Security audit misses real vulnerabilities | OWASP-structured checklist ensures systematic coverage, not ad-hoc scanning |
| UI implementation doesn't match design | Visual QA agent with screenshot comparison when Pencil.dev available |

---

## 15. Success Metrics

A successful ZFlow implementation should achieve:

- **First-time correctness**: Features implemented correctly on first pass >80% of the time
- **Reduced debugging cycles**: Bugs found and fixed with root cause on first attempt >90%
- **Audit trail**: Every decision documented and traceable from scope through implementation
- **Resumability**: Any phase can be re-run independently without losing prior work
- **Parallelism efficiency**: Research/Review/QA phases complete in wall-clock time of their slowest agent, not sum of all agents
- **Karpathy compliance**: <5% of code changes flagged as "beyond scope" in QA review
- **Security coverage**: 100% of OWASP Top 10 2025 categories reviewed per audit
- **UI fidelity**: When Pencil.dev is used, >95% of design tokens correctly applied in implementation
- **Zero false security confidence**: No security vulnerabilities shipped that the audit checklist covered

---

## Appendix A: Agent Inventory (Complete)

| # | Agent | Phase | Parallel Group | Focus |
|---|-------|-------|----------------|-------|
| 1 | socratic-interviewer | 0-Brainstorm | Solo (interactive) | Guided discovery with multiple-choice questions, approach proposals, section-by-section design |
| 2 | architecture-scout | 1-Research | Research swarm | Project structure |
| 3 | dependency-mapper | 1-Research | Research swarm | Dependency chains |
| 4 | pattern-analyzer | 1-Research | Research swarm | Code conventions |
| 5 | test-surveyor | 1-Research | Research swarm | Test infrastructure |
| 6 | related-code-finder | 1-Research | Research swarm | Affected code |
| 7 | ui-system-scout | 1-Research | Research swarm (conditional) | Design system |
| 8 | solution-architect | 2-Design | Solo | Solution design |
| 9 | gap-detector | 3-Review | Review swarm | Missing requirements |
| 10 | overengineering-critic | 3-Review | Review swarm | Simplicity (Karpathy) |
| 11 | security-reviewer | 3-Review | Review swarm | Security design review |
| 12 | performance-reviewer | 3-Review | Review swarm | Performance concerns |
| 13 | alignment-checker | 3-Review | Review swarm | Architecture fit |
| 14 | pencil-designer | 3.5-UI Design | UI swarm (conditional) | Canvas design |
| 15 | design-system-builder | 3.5-UI Design | UI swarm (conditional) | Token/component system |
| 16 | ui-review-agent | 3.5-UI Design | UI swarm (conditional) | Design QA |
| 17 | focused-implementer | 4-Implement | Impl tier (×N) | Code implementation |
| 18 | ui-implementer | 4-Implement | Impl tier (conditional) | UI implementation |
| 19 | completeness-checker | 5-QA | QA swarm | Implementation completeness |
| 20 | ux-reviewer | 5-QA | QA swarm | User experience |
| 21 | code-quality-auditor | 5-QA | QA swarm | Code quality (Karpathy) |
| 22 | test-coverage-agent | 5-QA | QA swarm | Test coverage |
| 23 | design-alignment-qa | 5-QA | QA swarm | Solution alignment |
| 24 | security-auditor | 5-QA | QA swarm | OWASP security audit |
| 25 | ui-visual-qa | 5-QA | QA swarm (conditional) | Visual regression |
| 26 | documentation-writer | 6-Document | Solo | Docs & commit |
| 27 | reproducer | D0-Reproduce | Solo (interactive) | Bug reproduction |
| 28 | call-chain-tracer | D1-Investigate | Debug swarm | Execution tracing |
| 29 | data-flow-tracer | D1-Investigate | Debug swarm | Data flow tracing |
| 30 | pattern-scanner | D1-Investigate | Debug swarm | Similar pattern scan |
| 31 | history-investigator | D1-Investigate | Debug swarm | Git history analysis |
| 32 | security-impact-assessor | D1-Investigate | Debug swarm | Security impact check |
| 33 | root-cause-analyst | D2-Analyze | Solo | Root cause synthesis |
| 34 | fix-designer | D3-Design Fix | Fix review (×3) | Minimal fix design |
| 35 | fix-verifier | D5-Verify | Verify swarm (×4) | Fix + regression verify |

**Total: 35 agent templates** (26 for dev workflow, 9 for debug workflow; some shared)
