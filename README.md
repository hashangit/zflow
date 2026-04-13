# ZFlow

A multi-agent development workflow system that orchestrates specialized AI agents through a structured, phase-gated software development lifecycle. Works with any skills-capable AI harness — Claude Code, zClaw, Gemini CLI, OpenCode, and others.

Instead of a single AI agent trying to do everything, ZFlow deploys **35 purpose-built agents** — each with a focused mission — working in parallel swarms through a document-driven pipeline from brainstorm to commit.

---

## Why ZFlow?

Building software with AI agents works best when each agent has a clear, narrow focus. A brainstorming agent should think differently than an implementation agent. A security reviewer needs an adversarial mindset that a code-quality checker doesn't.

ZFlow applies this principle systematically:

- **Specialized agents**, not one monolithic prompt — each phase deploys agents with focused roles and boundaries
- **Document-driven handoffs** — every phase produces a structured artifact that becomes the input for the next, creating an auditable trail
- **Parallel where possible, sequential where necessary** — research, review, and QA agents fan out in parallel; phase transitions are gated checkpoints
- **No fix without understanding** — no implementation without design, no design without research, no debugging fix without root cause
- **Human-in-the-loop** — the workflow pauses at critical checkpoints for your review and approval

---

## Two Workflows

ZFlow provides two distinct workflows depending on what you're doing:

### Development Workflow (`/using-zflow`)

For building new features, planning functionality, or doing structured end-to-end development.

```
Brainstorm → Research → Design → Review → [UI Design] → Implement → QA → Document
    │            │          │         │          │            │        │        │
 scope.md   research   solution  reviewed   ui-design    code +    qa.md   commit +
            report.md   .md     solution    report.md   impl       security
                                  .md                    report.md   audit
```

### Debug Workflow (`/using-zflow-debug`)

For fixing bugs, investigating issues, or resolving regressions.

```
Reproduce → Investigate → Analyze → Design Fix → Implement Fix → Verify
     │            │           │          │              │            │
 repro.md   investigation  root      fix-          code +       verification
              .md        cause.md   design.md    impl report      .md
```

---

## Getting Started

### Prerequisites

An AI harness that supports skills and sub-agents. ZFlow works with:

- [Claude Code](https://claude.ai/code)
- [zClaw](https://github.com/hashangit/zclaw)
- [Gemini CLI](https://github.com/google-gemini/gemini-cli)
- [OpenCode](https://github.com/opencode-ai/opencode)
- Any other skills-compatible harness

No additional frameworks or dependencies required.

### Installation

Copy the `zflow/` directory into your harness's skills directory:

```bash
# Claude Code
cp -r zflow/ ~/.claude/skills/zflow/

# zClaw
cp -r zflow/ ~/.zclaw/skills/zflow/

# Gemini CLI
cp -r zflow/ ~/.gemini/skills/zflow/
```

That's it — no build step, no dependencies to install, no configuration required to start.

### Your First Run

```
/using-zflow I want to add a notification system to my app
```

ZFlow will:
1. Engage you in a guided brainstorming conversation with multiple-choice questions grounded in your actual codebase
2. Deploy research agents to analyze your architecture, dependencies, patterns, and tests
3. Present 2-3 design approaches for you to choose from, then refine the design section-by-section
4. Run fresh review agents to catch gaps, over-engineering, and security concerns
5. Implement in parallel, organized by dependency tiers
6. Run a full QA sweep including security audit
7. Update docs and prepare a commit

Each phase pauses for your approval before continuing. You stay in control.

---

## Development Workflow In Detail

### Phase 0: Brainstorm

**What happens**: A Socratic interviewer agent reads your codebase for context, then asks you guided questions — one at a time, in multiple-choice format with recommendations grounded in your actual project. It assesses scope, surfaces ambiguities, and helps decompose complex requests.

**You'll see**: Questions like *"Based on your current auth setup, how should we handle permissions?"* with options that reference your actual codebase patterns.

**Output**: `scope.md` — what needs to be built and why, but not how.

### Phase 1: Research

**What happens**: 5-6 parallel agents fan out across your codebase — one maps architecture, another traces dependencies, another finds existing patterns, another surveys test infrastructure, and another finds related code. If UI work is detected, a design system scout joins the swarm.

**You'll see**: *"Deploying 6 parallel research agents..."* then *"All agents complete. Merging findings..."*

**Output**: `research-report.md` — real codebase context organized by dimension.

### Phase 2: Design

**What happens**: A senior architect agent maps your scope against the research findings, then proposes 2-3 solution approaches with trade-offs. You pick one. Then the design is presented section-by-section — architecture, components, data flow, errors, testing, tasks — each approved before the next.

**You'll see**: Approach comparisons like *"Extend Existing Service (Recommended)"* vs *"New Microservice"* with effort, risk, and codebase fit ratings.

**Output**: `solution.md` — the full technical design with task breakdown and dependency graph.

### Phase 3: Review

**What happens**: 5 fresh agents — with no prior context bias — examine your scope and solution from different angles: missing requirements, over-engineering, security holes, performance concerns, and architecture alignment. The coordinator then runs a structural self-review for completeness and consistency.

**Key reviewer**: The `overengineering-critic` specifically enforces simplicity — *would a senior engineer say this is overcomplicated?*

**Output**: `reviewed-solution.md` — your solution with adjustments and a full appendix of reviewer findings.

### Phase 3.5: UI Design (Conditional)

**What happens**: Only triggered when your scope involves UI work. If [Pencil.dev](https://pencil.dev) MCP tools are available, a design agent creates the interface on a visual canvas — building design tokens, components, and screen layouts — before any implementation code is written. You approve designs via screenshots.

**If Pencil.dev is not available**: You're asked whether to install it or proceed with standard code-first UI development.

**Output**: `ui-design-report.md` — design tokens, component specs, layout descriptions, and exported reference images.

### Phase 4: Implement

**What happens**: Implementation agents are deployed in parallel, organized by dependency tiers. Tier 0 tasks (no dependencies) run first, then Tier 1, and so on. Each agent gets a focused task slice with success criteria and operates under surgical change constraints.

**You'll see**: *"Tier 0: 3 agents running..."* then *"Tier 1: 2 agents running..."*

**Output**: Working code + `impl-report.md` — every file changed and any deviations from the design.

### Phase 5: QA

**What happens**: 6-7 parallel QA agents check different dimensions: completeness, UX, code quality, test coverage, design alignment, and a **deep OWASP Top 10 security audit**. If UI work was done, a visual QA agent compares implementation against designs.

**Issues are categorized**: Critical (security), Blocker, Major, Minor, or Note. Critical and blocker issues loop back to Phase 4 for targeted fixes.

**Output**: `qa-report.md` — all findings by severity.

### Phase 6: Document

**What happens**: A documentation agent updates relevant docs, CHANGELOG, and README based on everything produced. Generates a conventional commit message and stages changes.

**Output**: Updated documentation + commit (requires your approval).

---

## Debug Workflow In Detail

### Phase D0: Reproduce

Agent confirms the bug is reproducible, documents exact steps, captures error output, and identifies the minimal reproduction case.

### Phase D1: Investigate

5 parallel agents trace the issue: backward from the symptom (call chain), backward from invalid data (data flow), similar patterns in the codebase, recent git history, and **security impact assessment** (can this be exploited?).

### Phase D2: Root Cause Analysis

A deliberation agent synthesizes all findings to identify the true root cause — distinguishing symptom from cause with supporting evidence.

### Phase D3: Design Fix

3 parallel reviewers check the proposed fix: does it address root cause (not just symptom)? Does it introduce regressions? Is it the minimal effective change?

### Phase D4: Implement Fix

Implementation agent applies the fix. If 3 attempts fail, the issue escalates to architectural review.

### Phase D5: Verify

4 parallel verifiers confirm: bug is fixed, no regressions, similar patterns are checked, and no security vulnerabilities were introduced.

---

## Agent Inventory

35 specialized agents, each with a focused mission:

### Brainstorm (1 agent)
| Agent | Focus |
|-------|-------|
| Socratic Interviewer | Guided discovery with multiple-choice questions grounded in your codebase |

### Research (6 agents, conditional)
| Agent | Focus |
|-------|-------|
| Architecture Scout | Project structure and architectural patterns |
| Dependency Mapper | Import chains and module coupling |
| Pattern Analyzer | Coding conventions and existing implementations |
| Test Surveyor | Test infrastructure, frameworks, and coverage |
| Related Code Finder | Code affected by the proposed changes |
| UI System Scout | *Conditional* — design system, tokens, component library |

### Design (1 agent)
| Agent | Focus |
|-------|-------|
| Solution Architect | Approach selection and section-by-section design |

### Review (5 agents)
| Agent | Focus |
|-------|-------|
| Gap Detector | Missing requirements and edge cases |
| Overengineering Critic | Simplicity enforcement |
| Security Reviewer | Security implications of the design |
| Performance Reviewer | Performance and scaling concerns |
| Alignment Checker | Architecture fit and consistency |

### UI Design (3 agents, conditional)
| Agent | Focus |
|-------|-------|
| Pencil Designer | Visual canvas design via Pencil.dev |
| Design System Builder | Token and component system |
| UI Review Agent | Accessibility, responsiveness, consistency |

### Implementation (2 agents)
| Agent | Focus |
|-------|-------|
| Focused Implementer | Single-task implementation with surgical changes |
| UI Implementer | *Conditional* — implements from Pencil.dev designs |

### QA (7 agents)
| Agent | Focus |
|-------|-------|
| Completeness Checker | Every solution task is implemented |
| UX Reviewer | API ergonomics, error messages, edge cases |
| Code Quality Auditor | Linting, naming, complexity — enforces simplicity |
| Test Coverage Agent | Test quality and edge case coverage |
| Design Alignment QA | Implementation matches the reviewed solution |
| Security Auditor | Full OWASP Top 10 2025 deep audit |
| UI Visual QA | *Conditional* — design fidelity and accessibility |

### Debug (9 agents)
| Agent | Focus |
|-------|-------|
| Reproducer | Minimal bug reproduction |
| Call Chain Tracer | Execution path backward from symptom |
| Data Flow Tracer | Invalid data traced to source |
| Pattern Scanner | Similar patterns that share the bug |
| History Investigator | Git blame/log analysis |
| Security Impact Assessor | Can this bug be exploited? |
| Root Cause Analyst | Synthesize true root cause |
| Fix Designer | Minimal effective fix design |
| Fix Verifier | Fix confirmation + regression check |

### Document (1 agent)
| Agent | Focus |
|-------|-------|
| Documentation Writer | Docs, CHANGELOG, commit message |

---

## Security

Security isn't a checkbox in ZFlow — it's a dedicated workflow dimension:

**During Development**: The QA phase includes a deep security audit covering the full OWASP Top 10 2025 — broken access control, injection, cryptographic failures, misconfiguration, and more. Every finding includes an attack scenario, not just a code smell.

**During Debugging**: A security impact assessor evaluates whether bugs can be exploited, what the blast radius would be, and whether fixes introduce new attack surface.

**Configurable depth**: Set `audit_depth` to `"full"` (all OWASP categories), `"targeted"` (only relevant categories), or `"minimal"` (top 5). Control the severity threshold for reporting.

---

## Configuration

ZFlow creates a `.zflow/` workspace in your project root on first run. Edit `.zflow/config.json` to customize:

### Phase Gates

Control which phases pause for your approval (`"human"`) and which proceed automatically (`"auto"`):

```json
{
  "workflow": {
    "gates": {
      "brainstorm": "human",
      "research": "auto",
      "design": "human",
      "review": "human",
      "implement": "auto",
      "qa": "human",
      "document": "auto"
    }
  }
}
```

### Phase Skipping

For smaller tasks, skip phases you don't need:

```json
{
  "workflow": {
    "skip_phases": ["research"]
  }
}
```

### Parallelism

Control how many agents run simultaneously:

```json
{
  "workflow": {
    "max_parallel_agents": 5
  }
}
```

### Security Settings

```json
{
  "security": {
    "audit_depth": "full",
    "dependency_scan": true,
    "secrets_scan": true,
    "security_severity_threshold": "medium"
  }
}
```

### Full Defaults

See the default configuration in the [design plan](zflow-design-plan.md#111-user-configurable-options).

---

## Workspace Structure

When ZFlow runs, it creates a `.zflow/` directory to track progress:

```
.zflow/
├── current-phase.json          # Active phase tracking
├── config.json                 # Your preferences
└── phases/
    ├── 00-brainstorm/
    │   └── scope.md
    ├── 01-research/
    │   ├── research-report.md
    │   └── agent-reports/      # Individual agent findings
    ├── 02-design/
    │   └── solution.md
    ├── 03-review/
    │   ├── reviewed-solution.md
    │   └── reviewer-reports/
    ├── 03.5-ui-design/         # Only if UI work
    ├── 04-implement/
    │   ├── implementation-plan.md
    │   └── impl-report.md
    ├── 05-qa/
    │   └── qa-report.md
    └── 06-document/
```

Resume anytime — if you interrupt ZFlow and run `/using-zflow` again, it picks up where you left off.

---

## Project Structure

```
zflow/
├── SKILL.md                        # Main orchestrator entry point
├── LICENSE.txt                     # MIT License
│
├── skills/                         # Phase sub-skills
│   ├── zflow-brainstorm/SKILL.md
│   ├── zflow-research/SKILL.md
│   ├── zflow-design/SKILL.md
│   ├── zflow-review/SKILL.md
│   ├── zflow-ui-design/SKILL.md
│   ├── zflow-implement/SKILL.md
│   ├── zflow-qa/SKILL.md
│   ├── zflow-document/SKILL.md
│   └── zflow-debug/SKILL.md
│
├── agents/                         # 35 agent prompt templates
│   ├── _shared/karpathy-preamble.md
│   ├── brainstorm/
│   ├── research/
│   ├── design/
│   ├── review/
│   ├── ui-design/
│   ├── implement/
│   ├── qa/
│   ├── debug/
│   └── document/
│
├── templates/                      # Output document templates
├── references/                     # Internal reference documentation
├── scripts/                        # Workspace and validation scripts
└── evals/                          # Test scenarios
```

100 files, ~14,600 lines across skills, agents, templates, references, and evals.

---

## Design Principles

These principles shape every agent's behavior in ZFlow:

**Think Before Coding** — State assumptions explicitly. Present alternatives rather than picking silently. Stop and ask when something is unclear.

**Simplicity First** — Minimum code that solves the problem. No speculative features, no abstractions for single-use code, no "flexibility" that wasn't requested.

**Surgical Changes** — Touch only what's necessary. Don't refactor adjacent code. Match existing style. Every changed line must trace directly to the scope.

**Goal-Driven Execution** — Define success criteria before starting. Each step has a verification check. Strong criteria let agents loop independently.

These rules are enforced at three levels: embedded in every agent's prompt preamble, audited by the overengineering-critic during review, and verified by the code-quality-auditor during QA.

---

## Commands

| Command | Workflow |
|---------|----------|
| `/using-zflow` | Development workflow — brainstorm through commit |
| `/using-zflow-debug` | Debug workflow — reproduce through verify |

These are heavyweight workflows that should run when you explicitly choose them. The exact invocation syntax depends on your harness — slash commands in Claude Code and zClaw, skill activation in Gemini CLI, etc.

---

## Acknowledgments

ZFlow builds on two foundational ideas:

**[Superpowers](https://github.com/obra/superpowers)** — zFlow draws inspiration from the Superpowers skill framework's structured methodology: brainstorming before implementation, writing plans before executing, verification before completion, and phase-gated workflows with human checkpoints. The skill architecture, agent orchestration patterns, and escalation protocols are inspired by Superpowers conventions

**Andrej Karpathy's LLM Coding Guidelines** — The behavioral rules that govern every ZFlow agent — think before coding, simplicity first, surgical changes, goal-driven execution — are adapted from Karpathy's widely shared principles for effective AI-assisted development. These aren't just documented; they're baked into every agent's prompt as enforceable constraints, with dedicated review and QA agents that specifically audit against them.

---

## License

[MIT](LICENSE.txt) — use it, modify it, ship it.
