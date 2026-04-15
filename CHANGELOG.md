# Changelog

All notable changes to ZFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.2] - 2026-04-15

### Added

- **Token efficiency directives** (`SKILL.md`) — New context budget section establishing
  lean coordinator behavior: delegate heavy lifting to subagents, never echo file contents,
  keep gate summaries short, read phase docs on demand, merge reports via synthesis agents,
  and keep user-facing messages conversational.

- **Subagent delegation for heavy work** (`SKILL.md`, `references/workflow-guide.md`,
  `agents/brainstorm/codebase-scout.md`, `agents/design/approach-researcher.md`,
  `agents/design/solution-assembler.md`) — Expanded the "delegate heavy lifting" directive
  with concrete delegation rules: the coordinator dispatches work to subagents and only
  coordinates results, never produces artifact content itself.

- **Coordinator delegation directives** (`references/agent-orchestration.md`) — Rewrote the
  Coordinator Responsibilities section around a "dispatcher, not worker" principle. Added a
  "Coordinator Must NOT Do Itself" table covering reading workspace artifacts, reading agent
  prompt files, merging reports, writing phase outputs, and building dependency graphs. Added
  the "Pass Paths, Not Contents" pattern — subagents receive file paths and read them
  themselves rather than having the coordinator embed file contents in prompts. Added the
  "Synthesis Agent Pattern" — each phase spawns a synthesis agent to read worker reports,
  merge findings, and write the final phase output, keeping the coordinator's context lean.

- **Rate-limit retry with sequential fallback** (`references/agent-orchestration.md`,
  `SKILL.md`) — When spawning agents encounters rate limits (429/529), server errors (503),
  or connection failures, the coordinator follows a 4-step escalation: retry parallel once,
  fall back to sequential (one agent at a time), reduce to small batches (2 agents), then
  proceed with available results and log gaps. Includes a decision flow diagram and
  coordinator behavior rules during fallback.

### Changed

- **Slimmed reference files for token efficiency** — Optimized multiple reference and agent
  files by trimming verbose prose, shortening labels, condensing explanations, and removing
  redundant content while preserving all technical accuracy:
  - `references/security-patterns.md` — trimmed verbose prose, shortened labels, condensed
    explanations
  - `references/security-checklist.md` — already optimized in prior pass
  - `agents/brainstorm/question-patterns.md` — condensed question examples and reduced
    redundancy
  - `references/workflow-guide.md` — tightened descriptions and removed verbose context

- **Updated "Merge, don't concatenate" directive** (`SKILL.md`) — Replaced with "Merge via
  synthesis agent" directing the coordinator to spawn a synthesis agent for report merging
  instead of doing it itself.

### Files Changed

- `zflow/SKILL.md` — Added token efficiency directives; delegation directives; rate-limit
  retry bullet; replaced merge directive with synthesis agent pattern
- `zflow/references/agent-orchestration.md` — Rewrote Coordinator Responsibilities with
  delegation table, pass-paths-not-contents pattern, synthesis agent pattern, and rate-limit
  retry fallback with decision flow
- `zflow/references/security-patterns.md` — Trimmed verbose prose, shortened labels
- `zflow/references/security-checklist.md` — Already optimized
- `zflow/agents/brainstorm/question-patterns.md` — Condensed question examples
- `zflow/agents/brainstorm/codebase-scout.md` — Delegation directive updates
- `zflow/agents/design/approach-researcher.md` — Delegation directive updates
- `zflow/agents/design/solution-assembler.md` — Delegation directive updates
- `zflow/references/workflow-guide.md` — Tightened descriptions
- `zflow/phases/brainstorm.md` — Token efficiency reference updates
- `zflow/phases/design.md` — Token efficiency reference updates
- `zflow/phases/document.md` — Token efficiency reference updates
- `zflow/references/karpathy-guidelines.md` — Token efficiency reference updates
- `zflow/references/escalation-patterns.md` — Token efficiency reference updates
- `zflow/templates/*.md` — Slimmed templates (scope, research-report, solution,
  reviewed-solution, qa-report, impl-report, implementation-plan, investigation)

### Backward Compatibility

No breaking changes. All phase artifacts, config schemas, agent prompts, and workflow
logic remain identical. Changes are limited to coordinator behavior directives (how the
orchestrator manages its context and delegates work) and internal file optimization
(reducing token consumption without changing content).

---

## [v1.0.1] - 2026-04-15

### Added

- **Plain Language Communication Style directive** — New top-level section in
  `SKILL.md` establishing 7 guidelines for all user-facing ZFlow communication:
  plain English first, explain jargon in-line, describe what things do not what
  they're called, short sentences, concrete over abstract, why before what, and
  self-contained recommendations. This directive applies to every phase doc,
  agent prompt, gate summary, and template in ZFlow.

### Changed

- **Pipeline proposal template** (`SKILL.md`) — Replaced the technical
  "ZFlow Pipeline Proposal" format (complexity score, profile name, phase
  depth/agents/gate table) with a plain-language "How should we approach this?"
  format that describes each step in everyday terms. Internal complexity scoring
  still happens but is no longer exposed to the user.

- **QA gate template** (`SKILL.md`) — Replaced "Root Cause Layer" terminology
  and severity classification tables with plain-language issue descriptions:
  "Testing found N issues that need fixing" with explanations like "The code
  doesn't match the design" or "The design itself has a flaw."

- **Human gate prompt template** (`references/quick-reference.md`) — Simplified
  from "Phase Complete: {phase_name}" with artifact paths and key decisions to
  "{Phase name} step is done" with plain-language summaries and a "What happens
  next" section that previews the upcoming step.

- **Brainstorm question patterns** (`agents/brainstorm/question-patterns.md`) —
  Added "Plain Language Rules" section with 5 concrete rules. Rewrote all 10
  dimension examples to use accessible language:
  - "Engagement metric" → "People actually use it"
  - "Minimal dependency addition" → "No new tools or packages"
  - "New Prisma model" → "Add a new data type"
  - "REST — Match existing pattern" → "Add new endpoints — same pattern as the rest"
  - "Match existing error pattern" → "Same as the rest of the app"
  - "Non-breaking — Additive only" → "Add the new stuff without changing the old"

- **Socratic interviewer agent** (`agents/brainstorm/socratic-interviewer.md`) —
  Added "Communication Style" section directing plain language usage. Updated
  example opening to explain tools like Prisma in context.

- **Brainstorm phase doc** (`phases/brainstorm.md`) — Added "Communication
  Style" section.

- **Design phase doc** (`phases/design.md`) — Added "Communication Style"
  section. Renamed approach proposal template labels from "Pros/Cons/Effort/
  Risk/Codebase Fit" to "Good because/Downsides/How much work/How risky/Why it
  fits your project". Renamed section sequence headers to plain English:
  "Architecture Overview" → "How it works overall", "Component Breakdown" →
  "What gets built or changed", "Data Flow" → "How data moves around",
  "Error Handling & Edge Cases" → "What happens when things go wrong",
  "Testing Strategy" → "Testing plan", "Task Breakdown" → "Step-by-step plan".

- **Workflow detection prompt** (`SKILL.md`) — Simplified "Development — Plan,
  research, design, and implement from scratch" to "Building something new —
  we'll plan, design, and build from scratch".

- **Status reporting** (`SKILL.md`) — Changed "Deploying N parallel agents" to
  "Running N research tasks in parallel" and "Tier N: count agents running" to
  "Working on group N of tasks".

### Files Changed

- `zflow/SKILL.md` — Added Communication Style section; simplified pipeline
  proposal, QA gate, workflow detection, and status reporting templates
- `zflow/agents/brainstorm/question-patterns.md` — Added Plain Language Rules;
  rewrote all 10 dimension examples
- `zflow/agents/brainstorm/socratic-interviewer.md` — Added Communication Style
  section; updated example opening
- `zflow/phases/brainstorm.md` — Added Communication Style section
- `zflow/phases/design.md` — Added Communication Style section; simplified
  approach proposal template and section sequence headers
- `zflow/references/quick-reference.md` — Simplified human gate prompt template

### Backward Compatibility

No breaking changes. All phase artifacts, config schemas, agent prompts, and
workflow logic remain identical. Only the *wording* of user-facing prompts,
questions, and templates changed — the underlying decisions and processes are
the same.

---

## [v1.0.0] - 2026-04-14

### Changed

- **Migrate from sub-skill invocation model to phase document reading architecture** —
  Major architectural shift in how ZFlow phases are executed. Previously, each phase was
  a standalone sub-skill with its own SKILL.md that needed to be invoked through
  harness-specific mechanisms (Skill tool in Claude Code, skill activation in Gemini CLI).
  Now, phases are simple markdown documents in the `phases/` directory that the orchestrator
  reads and follows directly. This eliminates platform-specific skill invocation requirements,
  nested SKILL.md overhead with duplicate frontmatter and metadata, and the conceptual gap
  between "what the orchestrator does" and "how phases execute".

### Objectives

- **Portability**: Phase docs work identically across Claude Code, Gemini CLI, Copilot, or
  any LLM environment — no harness-specific integrations needed
- **Simplicity**: Removed 9 separate SKILL.md files, replacing them with 9 leaner .md
  documents in `phases/`. Each phase doc is 30-50% shorter because it no longer needs skill
  frontmatter, invocation metadata, or nested orchestration instructions
- **Path resolution**: All internal references now use `${CLAUDE_SKILL_DIR}` — a runtime
  variable that resolves to the skill's root directory regardless of installation location,
  fixing brittle relative paths that broke when the skill was installed in non-standard locations
- **Clearer orchestrator role**: The orchestrator's job is now unambiguous —
  "read phases/<phase>.md, follow its instructions" instead of the previous
  "invoke sub-skill X via harness mechanism Y with parameters Z"

### User Experience Impact

- Faster phase transitions — no skill invocation overhead, the orchestrator reads a doc
  and proceeds immediately
- More consistent behavior — phases execute identically regardless of which AI coding
  platform the user runs ZFlow on
- Easier customization — users can edit phase docs directly without navigating nested
  skill directories or understanding skill invocation semantics
- Better debugging — when a phase behaves unexpectedly, the phase doc is a single readable
  source of truth with no need to trace through skill invocation chains

### Usage Pattern Changes

- **Before**: Users needed to ensure their AI platform supported the specific skill invocation
  mechanism (Claude Code's Skill tool, Gemini's skill activation)
- **After**: Any platform that can read files and follow instructions works — the lowest
  common denominator is much lower
- **Before**: Phase docs were buried in `skills/zflow-*/SKILL.md` paths that varied per phase
- **After**: All phase docs are at `phases/<phase>.md` — uniform, predictable, easy to navigate

### Files Changed

- Updated `zflow/SKILL.md` — all phase references changed from sub-skill invocation language
  to phase document reading language; replaced relative paths with `${CLAUDE_SKILL_DIR}`;
  clarified orchestrator role constraints
- Deleted 9 legacy skill files: `zflow/skills/zflow-brainstorm/SKILL.md`,
  `zflow/skills/zflow-research/SKILL.md`, `zflow/skills/zflow-design/SKILL.md`,
  `zflow/skills/zflow-review/SKILL.md`, `zflow/skills/zflow-ui-design/SKILL.md`,
  `zflow/skills/zflow-implement/SKILL.md`, `zflow/skills/zflow-qa/SKILL.md`,
  `zflow/skills/zflow-document/SKILL.md`, `zflow/skills/zflow-debug/SKILL.md`
- Added 9 new phase documents in `zflow/phases/`: `brainstorm.md`, `research.md`,
  `design.md`, `review.md`, `ui-design.md`, `implement.md`, `qa.md`, `document.md`,
  `debug.md`
- Added `zflow/.claude-plugin/` — plugin configuration directory

### Backward Compatibility

This is an internal restructuring — the external workflow (phases 0-6 + debug flow) remains
identical. Users running ZFlow will see the same phase sequence, same artifacts, and same
human gates. The change is purely in how phases are loaded and executed internally. No
breaking changes to artifact formats, config schemas, or agent prompts.

---

### v0.5.0 (2026-04-14) — Adaptive Orchestration & Modular Refactor

This major update transforms ZFlow from a static 8-phase pipeline into an **adaptive, complexity-aware orchestration system** and modularizes the core engine for better scalability.

#### 🚀 Adaptive Pipeline System
- **Dynamic Profile Selection:** ZFlow now dynamically selects from 4 task-optimized profiles based on a 1-15 complexity score:
    - **Quick Fix (Trivial):** 3-4 agents, abbreviated brainstorm, skips Research/Review phases, and uses "Design Sketches" for speed.
    - **Standard (Default):** The balanced, structured workflow for typical features.
    - **Full (Complex):** Comprehensive 8-phase pipeline with exhaustive Research and Review.
    - **Extended (Critical):** Maximum rigor with multiple QA/Review swarms and structural validation for high-risk changes.
- **Complexity Assessment Rubric:** Implemented a multi-signal scoring rubric across five dimensions:
    - **Affected Systems:** Counts distinct modules or architectural layers.
    - **Technical Domains:** Varieties of tech stacks (Backend, UI, Database, etc.).
    - **Existing Patterns:** Follows established code vs. requiring new abstractions.
    - **User Language:** Quality and detail level of the initial prompt.
    - **Ambiguity:** Level of technical uncertainty or requirement gaps.
- **Pipeline Invariants:** Core guarantees (Design-before-Implementation, QA-after-Implementation, Human-in-the-Loop gates) are now enforced regardless of the selected profile.

#### 🔄 Intelligent QA & Loop-Back Protocol
- **Root Cause Layer Classification:** Critical/Blocker findings are now categorized into **Implementation**, **Design**, **Scope**, or **Unknown**.
- **Smart Re-entry Protocol:**
    - Implementation errors trigger targeted re-Implementation.
    - Design flaws loop back to the Design phase while attempting to preserve valid implementation work.
    - Scope mismatches (e.g., user rejection) loop back to Brainstorm for clarification.
- **Artifact Preservation:** Logic added to prevent full re-writes by tracking which sections of a solution or implementation are invalidated.

#### 🏗️ Core Orchestrator Refactor (Modularization)
- **"Read, Don't Inline" Architecture:** Reduced the main `SKILL.md` size by 50% by extracting content into a new `/references` directory:
    - `default-config.md`: Full JSON schema for ZFlow configuration.
    - `pencil-integration.md`: Pencil.dev detection flow and decision logic.
    - `phase-resumption.md`: Logic for detecting interrupts and state checking.
    - `error-handling.md`: Unified procedures for phase failures and missing artifacts.
    - `quick-reference.md`: Naming conventions, checklists, and human gate prompt templates.
- **Harness-Agnostic Invocation:** Sub-skill calling conventions are now independent of specific AI harnesses (Claude, zClaw, Gemini).

#### 🤖 Agent & Prompt Enhancements
- **Standardized Karpathy Preamble:** All 34 agent prompts now use a unified inclusion note for `agents/_shared/karpathy-preamble.md`, ensuring behavioral consistency.
- **Template Section Classification:** 16 templates updated with a three-tier (Required/Expected/Optional) system to reduce boilerplate for simple tasks.
- **Abbreviated Brainstorm Mode:** Guided path for Trivial tasks reduced to 3-4 targeted questions.
- **Design Alignment Logic:** Design agents can now operate without Research Reports for "Quick Fix" profiles.
- **QA Severity Grading:** Improved categorization (Critical, Blocker, Major, Minor, Note) with explicit enforcement rules for loop-backs.
- **Security Audit Depth:** Standardized `audit_depth` settings across all QA agents.
