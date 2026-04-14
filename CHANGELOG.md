# Changelog

All notable changes to ZFlow will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
