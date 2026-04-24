# ZFlow — Agent Skills Standards Review

A compliance and best-practice review of the ZFlow skill against the [agentskills.io](https://agentskills.io) specification, dated 2026-04-24.

Source material: the live agentskills.io specification, best-practices, optimizing-descriptions, evaluating-skills, using-scripts, and client-implementation docs. Validator output from the official reference package command:

```bash
uvx --from skills-ref agentskills validate zflow
```

## What ZFlow is doing right

The shape matches the spec well.

- `name: zflow` satisfies every naming rule: lowercase, no leading/trailing hyphens, no consecutive hyphens, ≤ 64 chars, matches the parent directory name `zflow/`.
- `description` is 326 chars — well under the 1024-char cap. It uses imperative phrasing and lists trigger scenarios, though it needs tightening because the current scope is too broad for reliable activation.
- The top-level layout (`SKILL.md`, `scripts/`, `references/`) uses the spec's canonical directory names. The spec explicitly allows "any additional files or directories," so `agents/`, `phases/`, and `templates/` are legal — they are not a compliance problem.
- Every script has a purpose and supports non-interactive execution. Two of the three Python scripts (`validate-phase.py`, `generate-summary.py`) print proper `--help` with flags, exit codes, and usage examples — exactly the "designing scripts for agentic use" pattern.
- File references in `SKILL.md` are one level deep (`phases/brainstorm.md`, `references/pipeline-profiles.md`), which matches the spec's "keep file references one level deep" rule.
- Progressive disclosure is genuinely wired in — `SKILL.md` tells the agent *when* to load each reference ("For the complete profile definitions, read `references/pipeline-profiles.md`"), which best-practices calls out as more useful than a generic "see references/ for details."

## Spec violations (must fix for compliance)

### 1. `disable-model-invocation` is not a spec field

Running `uvx --from skills-ref agentskills validate zflow` returns:

```
Validation failed for zflow:
  - Unexpected fields in frontmatter: disable-model-invocation.
    Only ['allowed-tools', 'compatibility', 'description', 'license', 'metadata', 'name'] are allowed.
```

The spec's frontmatter whitelist is exactly those six fields. `disable-model-invocation` is a Claude Code plugin-system flag that leaked into `SKILL.md`. The spec reserves `metadata` for client-specific extensions.

**Fix:** move it under `metadata:`

```yaml
metadata:
  claude-code:
    disable-model-invocation: "true"
```

Or drop it entirely if the intent is for the skill to be discoverable everywhere.

### 2. Phase templates fail their own validator

The bundled phase validator and bundled templates disagree. A clean agent following the template can still produce an artifact that fails the phase gate.

Confirmed failures:

```bash
python3 zflow/scripts/validate-phase.py reviewed-solution zflow/templates/reviewed-solution.md
python3 zflow/scripts/validate-phase.py impl-report zflow/templates/impl-report.md
python3 zflow/scripts/validate-phase.py verification zflow/templates/verification.md
```

Specific mismatch:

- `reviewed-solution` validator expects `Chosen Approach`, `Architecture Overview`, `Component Breakdown`, and `Reviewer Findings`; the template uses `Original Solution (with Adjustments Applied)` and `Review Appendix`.
- `impl-report` validator expects `Tasks Completed`; the template uses `Per-Task Reports` and `Executive Summary`.
- `verification` validator expects `Verification Result`; the template uses `Verification Summary`.

**Fix:** choose one source of truth. Either rename template headings to match `validate-phase.py`, or update `PHASE_REQUIREMENTS` to match the template vocabulary. This should be treated as P1 because it can block normal workflow execution.

### 3. `SKILL.md` body exceeds both progressive-disclosure caps

The body is 725 lines / ~7,000 tokens. The spec recommends under 500 lines and under 5,000 tokens. This is not a validator-blocking error, but it is the single biggest portability and quality issue.

Sections 6–11 (Development Workflow, QA Loop-Back Protocol, Debug Workflow, Phase Transitions, Status Reporting, Phase Resumption, Error Handling) together are over half the file and are the natural split points.

**Fix:** move the detailed content into `references/` and leave a one-paragraph pointer in `SKILL.md` that tells the agent *when* to load each. Example targets:

- `references/development-workflow.md`
- `references/debug-workflow.md`
- `references/qa-loopback-protocol.md`
- `references/phase-transitions.md`

Keep in `SKILL.md`: the overview, trigger rules, pipeline planning step 1-2, and the pointer table.

## Portability gaps (non-blocking, but standards-relevant)

### 4. Activation model is inconsistent

The description says to use ZFlow whenever the user wants to plan, research, design, implement, QA, or debug a feature or fix. That can match most non-trivial coding tasks. At the same time, `disable-model-invocation: true` says the skill should require explicit invocation.

That puts clients in an awkward spot:

- Standards-compliant description-driven clients may over-trigger ZFlow.
- Claude-specific clients may suppress auto-triggering through a non-standard field.
- Other clients may reject the skill outright because of the non-standard field.

**Fix:** decide the intended activation contract.

If ZFlow is explicit-only, narrow the description:

```yaml
description: >
  Use this skill when the user explicitly asks to run ZFlow or wants a
  structured multi-phase, multi-agent workflow for planning, building, QA,
  documentation, or debugging.
```

If ZFlow should auto-trigger, remove the explicit-only metadata and tune the description with trigger evals.

### 5. `${CLAUDE_SKILL_DIR}` is Claude Code-specific

80 occurrences across 11 files. The spec says to use "relative paths from the skill root" and shows `references/REFERENCE.md` as the canonical form. Client implementation guidance also recommends that activation wrappers provide a skill directory and resource listing so the model can resolve bundled files without relying on a Claude-specific variable.

The `SKILL.md` even already mixes styles in adjacent paragraphs:

- Portable: "read `references/pipeline-profiles.md`"
- Not portable: "read `${CLAUDE_SKILL_DIR}/references/pipeline-profiles.md`"

**Fix:** global find-and-replace of `${CLAUDE_SKILL_DIR}/` → `` across `SKILL.md`, `phases/*.md`, and `references/*.md`. 11 files, 80 occurrences.

### 6. Coordinator instructions contradict the path-passing policy

`SKILL.md` tells the orchestrator to pass paths to subagents and avoid embedding file contents. That matches progressive disclosure and keeps the coordinator context lean.

Several phase docs still instruct the coordinator to read and inline full prompt/template/artifact contents before calling subagents. Examples:

- `phases/brainstorm.md` says to read the Karpathy preamble and codebase-scout prompt and include their contents.
- `phases/research.md` says each agent receives the full contents of the Karpathy preamble, agent prompt, and `scope.md`.
- `phases/design.md` says to include full contents of `scope.md`, `research-report.md`, and templates.

**Fix:** update phase docs to pass resolved file paths instead of contents. Keep only small, task-specific instructions in the subagent prompt. This aligns the phase docs with `references/agent-orchestration.md`, which already documents the desired "pass paths, not contents" pattern.

### 7. No `license` in frontmatter despite a bundled `LICENSE.txt`

One-line add:

```yaml
license: See LICENSE.txt
```

### 8. No `compatibility` field despite environment requirements

The scripts expect `bash`, `python3`, and (via `agent-orchestration.md`) MCP tool discovery. The spec field is designed for exactly this:

```yaml
compatibility: Requires bash and Python 3. Designed for Claude Code; portable to other Skills-compatible agents with minor path adjustments.
```

### 9. `scripts/init-workspace.sh --help` is broken

```
$ bash scripts/init-workspace.sh --help
[zflow] ERROR: Unknown workflow type '--help'. Use 'dev' or 'debug'.
```

The script treats the first positional arg as workflow type. The using-scripts doc is explicit: `--help` is the primary way an agent learns a script's interface.

**Fix:** parse `--help` / `-h` before positional args.

## Best-practice gaps

### 10. Documentation still references the removed sub-skill layout

`README.md` and `references/quick-reference.md` still document `skills/zflow-*/SKILL.md` phase sub-skills, but the current repo uses `phases/*.md` documents. That stale structure appears in the project tree and phase tables.

This matters for agent execution because stale paths can cause a client or subagent to look for files that no longer exist.

**Fix:** update docs and quick reference to show the current layout:

```text
zflow/
├── SKILL.md
├── phases/
├── agents/
├── templates/
├── references/
└── scripts/
```

Use `phases/brainstorm.md`, `phases/research.md`, etc. in phase tables.

### 11. `references/security-checklist.md` approaches the SKILL.md token cap by itself

533 lines / ~5,000 tokens. References can be larger than SKILL.md, but when one reference is the size of a full skill's recommended budget, the best-practices doc ("Aim for moderate detail") suggests splitting by concern so the agent loads only what's relevant.

**Suggested split:**

- `references/security-injection.md`
- `references/security-auth.md`
- `references/security-secrets.md`

And update the QA phase doc to load only the subset relevant to the finding.

### 12. `plugin.json` and `SKILL.md` describe the skill differently

- `plugin.json`: "brainstorm, research, design, review, implement, QA, and document" (7 phases)
- `SKILL.md` description: "plan, research, design, implement, QA, or debug"

The agent only sees the `SKILL.md` description at discovery time. If debugging is a first-class workflow, it should appear there. If it is a sub-mode, leave it out. Either way, align them.

### 13. No `assets/` directory

The spec reserves `assets/` for templates and static resources. Your `templates/` directory holds what the spec would call assets — output format templates for `scope.md`, `qa-report.md`, etc.

This is purely a naming question (both are legal under "additional directories"), but renaming `templates/` → `assets/` would match spec conventions and make the skill more recognizable to anyone reading Anthropic's example skills.

## Priority order

| # | Issue | Type | Effort | Priority |
|---|---|---|---|---|
| 1 | `disable-model-invocation` in frontmatter | Compliance | Trivial | P0 |
| 2 | Phase templates fail `validate-phase.py` | Correctness | Low | P0 |
| 3 | SKILL.md body over 500 lines / 5k tokens | Best practice | Medium | P0 |
| 4 | Activation model is inconsistent | Triggering | Low | P1 |
| 5 | `${CLAUDE_SKILL_DIR}` everywhere | Portability | Low (mechanical) | P1 |
| 6 | Coordinator inlines contents despite path-passing policy | Context efficiency | Low | P1 |
| 9 | `init-workspace.sh --help` broken | Correctness | Trivial | P1 |
| 10 | README / quick reference stale sub-skill layout | Documentation | Trivial | P1 |
| 7 | Missing `license` field | Compliance polish | Trivial | P2 |
| 8 | Missing `compatibility` field | Compliance polish | Trivial | P2 |
| 11 | Oversized security checklist | Best practice | Medium | P3 |
| 12 | `plugin.json` / `SKILL.md` drift | Consistency | Trivial | P3 |
| 13 | `templates/` → `assets/` | Convention | Low | P3 |

## Suggested first patch (all surgical, no structural changes)

1. Move `disable-model-invocation` under `metadata:`
2. Align `validate-phase.py` requirements with template headings, or rename template headings to match the validator
3. Narrow the description or move explicit-only behavior to client metadata
4. Add `license` and `compatibility`
5. Global find-and-replace `${CLAUDE_SKILL_DIR}/` → `` across all `.md`
6. Update phase docs to pass file paths instead of inlining full prompt/template/artifact contents
7. Fix `init-workspace.sh --help` parsing
8. Update README and quick reference to remove stale `skills/zflow-*/SKILL.md` paths

The `SKILL.md` body split (issue 3) is a larger structural change and should be planned separately with explicit sign-off on split points before executing.

## Validation command

After changes, re-run:

```bash
uvx --from skills-ref agentskills validate /Users/hashanw/Developer/zflow/zflow
```

Expected output on a clean pass:

```
Validation passed for /Users/hashanw/Developer/zflow/zflow
```

## References

- [Agent Skills Specification](https://agentskills.io/specification)
- [Best practices for skill creators](https://agentskills.io/skill-creation/best-practices)
- [Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions)
- [Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills)
- [Using scripts in skills](https://agentskills.io/skill-creation/using-scripts)
- [Adding skills support to your agent](https://agentskills.io/client-implementation/adding-skills-support)
- [skills-ref reference validator](https://github.com/agentskills/agentskills)
