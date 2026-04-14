# ZFlow v1.0.1 — Release Notes

**Release Date:** April 15, 2026

---

This is the first official public release of ZFlow. It includes all work from v0.5.0 through v1.0.1.

---

## What is ZFlow?

An adaptive, multi-agent development workflow system that orchestrates specialized AI agents through a complexity-aware, phase-gated software development lifecycle. Works with any skills-capable AI harness — Claude Code, zClaw, Gemini CLI, OpenCode, and others.

Instead of a single AI agent trying to do everything, ZFlow dynamically constructs a pipeline using **35 purpose-built agents** — each with a focused mission — tailored to the specific complexity of your task.

### How to use it

```
/zflow I want to add a notification system to my app
```

That's it. ZFlow auto-detects whether you're building something new or fixing a bug, assesses complexity, and runs the right workflow.

---

## v1.0.1 — Plain Language Communication

All user-facing prompts, questions, and templates now use plain, accessible language — understandable by developers of any experience level.

### What changed

- **Communication Style directive** — 7 guidelines added to the orchestrator that apply to every phase: plain English first, explain jargon in-line, describe what things do not what they're called, short sentences, concrete over abstract, why before what, self-contained recommendations
- **Pipeline proposals** — replaced technical "ZFlow Pipeline Proposal" with plain-language "How should we approach this?"
- **QA gate summaries** — replaced "Root Cause Layer" tables with everyday descriptions like "The code doesn't match the design"
- **Brainstorm questions** — rewrote all 10 dimension examples (e.g. "Engagement metric" → "People actually use it", "New Prisma model" → "Add a new data type")
- **Design phase sections** — renamed from jargon to plain English ("Architecture Overview" → "How it works overall", "Data Flow" → "How data moves around")
- **Gate prompts** — simplified from "Phase Complete" to "{Phase name} step is done" with a "What happens next" preview

### Files changed (6 files)

| File | Change |
|------|--------|
| `zflow/SKILL.md` | Added Communication Style section; simplified pipeline, QA gate, status reporting |
| `zflow/agents/brainstorm/question-patterns.md` | Added Plain Language Rules; rewrote all 10 examples |
| `zflow/agents/brainstorm/socratic-interviewer.md` | Added Communication Style section; updated example opening |
| `zflow/phases/brainstorm.md` | Added Communication Style section |
| `zflow/phases/design.md` | Added Communication Style section; simplified approach and section templates |
| `zflow/references/quick-reference.md` | Simplified human gate prompt template |

---

## v1.0.0 — Phase Document Architecture

Major architectural refactor making ZFlow portable across AI coding platforms.

### What changed

- **Migrated from sub-skill invocation to phase document reading** — phases are now simple `.md` files in `phases/` that the orchestrator reads and follows directly, eliminating platform-specific skill invocation requirements
- **Platform agnostic execution** — works on any AI coding platform that can read files (Claude Code, Gemini CLI, Copilot, OpenCode, etc.)
- **Portable path resolution** — all internal references use `${CLAUDE_SKILL_DIR}` runtime variable, fixing brittle relative paths
- **Simplified structure** — 9 skill files consolidated into 9 leaner phase docs (30-50% smaller each)
- **Clearer orchestrator role** — "read phases/X.md, follow instructions" instead of "invoke sub-skill X via harness mechanism Y"

### User experience impact

- Faster phase transitions — no skill invocation overhead
- More consistent behavior across platforms
- Easier customization — edit `.md` files directly
- Better debugging — single source of truth per phase

### Files changed

- Updated `zflow/SKILL.md` — all phase references changed to phase document reading
- Deleted 9 legacy skill files in `zflow/skills/zflow-*/`
- Added 9 new phase documents in `zflow/phases/`
- Added `zflow/.claude-plugin/` plugin configuration

---

## v0.5.0 — Adaptive Orchestration & Modular Refactor

Transforms ZFlow from a static 8-phase pipeline into an adaptive, complexity-aware orchestration system.

### Adaptive pipeline system

- **4 pipeline profiles** selected by a 1-15 complexity score:
  - **Quick Fix** (Trivial): 3-4 agents, skips Research/Review, uses design sketches
  - **Standard** (Default): Balanced workflow for typical features
  - **Full** (Complex): Comprehensive 8-phase pipeline
  - **Extended** (Critical): Maximum rigor with multiple QA/Review swarms
- **Complexity assessment** across 5 dimensions: affected systems, technical domains, existing patterns, user language, ambiguity
- **Pipeline invariants** enforced regardless of profile: design before implementation, QA after implementation, human gates at critical decisions

### Intelligent QA & loop-back protocol

- **Root Cause Layer classification** — Critical/Blocker findings categorized as Implementation, Design, Scope, or Unknown
- **Smart re-entry** — loops back to the correct layer, not just the previous phase
- **Artifact preservation** — tracks which sections are invalidated to prevent full re-writes

### Core orchestrator refactor

- **"Read, Don't Inline" architecture** — reduced main SKILL.md by 50% by extracting into `/references` directory:
  - `default-config.md` — full JSON schema for configuration
  - `pencil-integration.md` — Pencil.dev detection flow
  - `phase-resumption.md` — interrupt detection and state checking
  - `error-handling.md` — phase failure procedures
  - `quick-reference.md` — naming conventions, checklists, gate templates
- **Harness-agnostic invocation** — sub-skill calling independent of specific AI harnesses

### Agent & prompt enhancements

- **Standardized Karpathy preamble** — all 34 agent prompts use unified behavioral rules
- **Template section classification** — 16 templates with Required/Expected/Optional tiers
- **Abbreviated brainstorm mode** — 3-4 targeted questions for trivial tasks
- **Design alignment logic** — agents can operate without research reports for Quick Fix profiles
- **QA severity grading** — Critical, Blocker, Major, Minor, Note with explicit enforcement
- **Security audit depth** — standardized `audit_depth` settings across all QA agents

---

## Full feature set

- **35 specialized agents** across brainstorming, research, design, review, implementation, QA, debug, and documentation
- **4 adaptive pipeline profiles** — Quick Fix, Standard, Full, Extended
- **2 workflows** — Development (brainstorm through commit) and Debug (reproduce through verify), auto-detected
- **Document-driven handoffs** — every phase produces a structured artifact that feeds the next
- **Parallel execution** — research, review, and QA agents fan out in parallel; phase transitions are gated checkpoints
- **Intelligent QA loop-back** — classifies failures by root cause layer to re-enter the correct phase
- **Human-in-the-loop** — pauses at critical checkpoints for review and approval
- **Pencil.dev integration** — design-first UI workflow with visual canvas when available
- **Phase resumption** — recover from interruptions without losing progress
- **Plain language communication** — all prompts and questions accessible to developers of any experience level
- **Security auditing** — deep OWASP Top 10 review during development, exploit assessment during debugging
- **Configurable** — gate modes, phase skipping, parallelism caps, security depth all adjustable

---

## Installation

Copy the `zflow/` directory into your harness's skills directory:

```bash
# Claude Code
cp -r zflow/ ~/.claude/skills/zflow/

# zClaw
cp -r zflow/ ~/.zclaw/skills/zflow/

# Gemini CLI
cp -r zflow/ ~/.gemini/skills/zflow/
```

---

## Pipeline profiles

| Profile | Complexity | Phases | Agents | Use Case |
|---------|-----------|--------|--------|----------|
| Quick Fix | 4-5 (Trivial) | IMPLEMENT → QA → DOCUMENT | 3-4 | Bug fixes, small tweaks |
| Standard | 6-9 (Normal) | BRAINSTORM → DESIGN → REVIEW → IMPLEMENT → QA → DOCUMENT | 15-20 | Typical features |
| Full | 10+ (Complex) | All 8 phases, full depth | 25-30 | Major architectural changes |
| Extended | 10+ (Critical) | All phases, multiple review/QA swarms | 30+ | High-risk, security-sensitive changes |

---

## What's included

```
zflow/
├── SKILL.md              # Main orchestrator
├── LICENSE.txt           # MIT License
├── .claude-plugin/
│   └── plugin.json       # Plugin metadata
├── phases/               # Phase documentation
│   ├── brainstorm.md     # Phase 0: Scope refinement
│   ├── research.md       # Phase 1: Codebase analysis
│   ├── design.md         # Phase 2: Solution design
│   ├── review.md         # Phase 3: Multi-perspective review
│   ├── ui-design.md      # Phase 3.5: Pencil.dev UI design (conditional)
│   ├── implement.md      # Phase 4: Tiered implementation
│   ├── qa.md             # Phase 5: Quality assurance
│   ├── document.md       # Phase 6: Documentation & commit
│   └── debug.md          # Debug workflow (D0-D5)
├── agents/               # 35 agent prompt templates
│   ├── _shared/          # Shared behavioral preambles
│   ├── brainstorm/
│   ├── research/
│   ├── design/
│   ├── review/
│   ├── ui-design/
│   ├── implement/
│   ├── qa/
│   ├── debug/
│   └── document/
├── templates/            # Phase output templates
├── references/           # Internal reference documentation
└── scripts/              # Workspace and validation scripts
```

100 files, ~14,600 lines across phases, agents, templates, references, and scripts.

---

## Known limitations

- Pencil.dev MCP tools must be installed separately for UI design-first workflow
- Debug workflow requires ability to execute code for reproduction phase
- Phase resumption requires `.zflow/` workspace to be preserved between sessions

---

## Acknowledgments

- **[Superpowers](https://github.com/obra/superpowers)** — inspiration for structured methodology, phase-gated workflows, and escalation protocols
- **Andrej Karpathy's LLM Coding Guidelines** — behavioral rules embedded in every agent prompt (simplicity first, surgical changes, goal-driven execution)

---

## License

[MIT](LICENSE.txt) — use it, modify it, ship it.

---

**Full changelog:** [CHANGELOG.md](CHANGELOG.md)
