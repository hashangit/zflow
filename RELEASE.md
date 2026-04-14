# ZFlow v1.0.0 — Release Notes

**Release Date:** April 14, 2026

---

## 🎉 What's New

ZFlow v1.0.0 marks the first stable release of the adaptive, multi-agent development workflow system. This release introduces a major architectural refactor that makes ZFlow **portable across AI coding platforms** while simplifying the internal execution model.

### 🏗️ Phase Document Architecture (Breaking Internal Change)

**Before v1.0.0:** Each phase was a standalone sub-skill with its own SKILL.md that needed to be invoked through harness-specific mechanisms (Skill tool in Claude Code, skill activation in Gemini CLI).

**In v1.0.0:** Phases are now simple markdown documents in the `phases/` directory that the orchestrator reads and follows directly.

**Why this matters:**
- **Platform agnostic** — works on any AI coding platform that can read files
- **Simpler** — 9 skill files consolidated into 9 leaner phase docs (30-50% smaller each)
- **Portable paths** — all references use `${CLAUDE_SKILL_DIR}` runtime variable
- **Easier to customize** — edit a `.md` file, no need to understand skill invocation semantics
- **Better debugging** — single source of truth per phase, no invocation chain tracing

### 📋 Full v1.0.0 Feature Set

- **4 adaptive pipeline profiles** (Quick Fix, Standard, Full, Extended) selected by a 1-15 complexity score
- **35 specialized agents** across brainstorming, research, design, review, implementation, QA, and documentation
- **Document-driven handoffs** — every phase produces a structured artifact
- **Parallel where possible, sequential where necessary** — research, review, and QA agents fan out in parallel
- **Intelligent QA Loop-Back** — classifies failures (Implementation, Design, Scope) to loop back to the correct layer
- **Human-in-the-loop** — workflow pauses at critical checkpoints for review and approval
- **Pencil.dev integration** — design-first UI workflow with visual canvas when available
- **Debug workflow** — structured 6-phase debugging from reproduction to verified fix
- **Phase resumption** — recover from interruptions without losing progress

---

## 📦 Installation

### Claude Code

```bash
# Install as a skill
claude skill add zflow
```

### Gemini CLI

Place the `zflow/` directory in your skills directory.

### Manual

Clone or copy the `zflow/` directory into your project's skill location.

---

## 🚀 Quick Start

```
using-zflow: Add a dark mode toggle to the settings page
```

ZFlow will:
1. Assess complexity and propose a pipeline profile
2. Guide you through a brainstorm to refine the scope
3. Research your codebase for relevant context
4. Design a solution with your approval
5. Review the design with 5 parallel reviewers
6. Implement the solution with dependency-ordered agents
7. Run QA across 6-7 quality dimensions
8. Generate documentation and a commit

---

## 📊 Pipeline Profiles

| Profile | Complexity | Phases | Agents | Use Case |
|---------|-----------|--------|--------|----------|
| Quick Fix | 4-5 (Trivial) | IMPLEMENT → QA → DOCUMENT | 3-4 | Bug fixes, small tweaks |
| Standard | 6-9 (Normal) | BRAINSTORM → DESIGN → REVIEW → IMPLEMENT → QA → DOCUMENT | 15-20 | Typical features |
| Full | 10+ (Complex) | All 8 phases, full depth | 25-30 | Major architectural changes |
| Extended | 10+ (Critical) | All phases, multiple review/QA swarms | 30+ | High-risk, security-sensitive changes |

---

## 🔄 Migration from Pre-1.0.0

If you were using ZFlow before v1.0.0:

- **No action required** — the external workflow is identical
- **Phase docs moved** — skills/zflow-\*/SKILL.md → phases/*.md
- **Path references updated** — all internal refs now use `${CLAUDE_SKILL_DIR}`
- **Behavior unchanged** — same phases, same artifacts, same human gates

---

## 📁 What's Included

```
zflow/
├── SKILL.md              # Main orchestrator
├── CHANGELOG.md          # Version history
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
├── agents/               # Agent prompt templates
├── references/           # Supporting documentation
├── templates/            # Phase output templates
└── evals/                # Evaluation benchmarks
```

---

## ⚡ What Changed from v0.5.0

| Area | v0.5.0 | v1.0.0 |
|------|--------|--------|
| Phase execution | Sub-skill invocation | Phase document reading |
| Phase files | 9 SKILL.md in `skills/zflow-*/` | 9 .md in `phases/` |
| Path resolution | Relative paths | `${CLAUDE_SKILL_DIR}` |
| Platform support | Harness-specific | Harness-agnostic |
| Phase doc size | Larger (with frontmatter) | 30-50% smaller |
| Orchestrator role | "Invoke sub-skill X via mechanism Y" | "Read phases/X.md, follow instructions" |
| External workflow | Same | Same |

---

## 🐛 Known Limitations

- Pencil.dev MCP tools must be installed separately for UI design-first workflow
- Debug workflow requires ability to execute code for reproduction phase
- Phase resumption requires `.zflow/` workspace to be preserved between sessions

---

## 📝 License

[MIT](LICENSE.txt) — use it, modify it, ship it.

---

## 🙏 Acknowledgments

- **[Superpowers](https://github.com/obra/superpowers)** — inspiration for structured methodology, phase-gated workflows, and escalation protocols
- **Andrej Karpathy's LLM Coding Guidelines** — behavioral rules embedded in every agent prompt (simplicity first, surgical changes, goal-driven execution)

---

**Full changelog:** [CHANGELOG.md](CHANGELOG.md)
