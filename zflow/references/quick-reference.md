# Quick Reference Tables

## Artifact Validation Checklist

For each phase, verify the output has required sections:

| Phase | Artifact | Required Sections |
|-------|----------|-------------------|
| Brainstorm | `scope.md` | Problem Statement, Success Criteria, Constraints, Scope Boundaries, MVP Definition, UI Work Flag |
| Research | `research-report.md` | Architecture Findings, Dependency Map, Patterns, Test Infrastructure, Key Findings synthesis |
| Design | `solution.md` | Chosen Approach, Architecture Overview, Component Breakdown, Data Flow, Task Breakdown with Dependencies |
| Review | `reviewed-solution.md` | All solution sections + Reviewer Findings appendix |
| UI Design | `ui-design-report.md` | Design Tokens, Component Specs, Screen Layouts, Accessibility Requirements |
| Implement | `impl-report.md` | Task Status, Files Changed, Deviations from Design |
| QA | `qa-report.md` | Issues by Severity, Completeness Assessment, Security Findings |
| Document | commit | CHANGELOG entry, Updated docs |

## Human Gate Prompt Template

When a human gate is required:

```
## Phase Complete: {phase_name}

**Output**: {artifact_path}
**Duration**: {elapsed}
**Agents Used**: {count}

### Summary
{2-3 sentence summary of what was produced}

### Key Decisions
- {decision 1}
- {decision 2}

Ready to proceed to {next_phase_name}?

  [A] Approve — proceed to next phase
  [B] Request changes — I'll provide feedback
  [C] Abort workflow
```

## Dev Workflow Phases

| # | Phase | Sub-Skill | Gate | Key Artifact |
|---|-------|-----------|------|-------------|
| 0 | Brainstorm | `skills/zflow-brainstorm/SKILL.md` | human | `scope.md` |
| 1 | Research | `skills/zflow-research/SKILL.md` | auto | `research-report.md` |
| 2 | Design | `skills/zflow-design/SKILL.md` | human | `solution.md` |
| 3 | Review | `skills/zflow-review/SKILL.md` | human | `reviewed-solution.md` |
| 3.5 | UI Design | `skills/zflow-ui-design/SKILL.md` | human | `ui-design-report.md` |
| 4 | Implement | `skills/zflow-implement/SKILL.md` | auto | `impl-report.md` |
| 5 | QA | `skills/zflow-qa/SKILL.md` | human | `qa-report.md` |
| 6 | Document | `skills/zflow-document/SKILL.md` | auto | changelog + commit |

## Debug Workflow Phases

| # | Phase | Sub-Skill | Gate | Key Artifact |
|---|-------|-----------|------|-------------|
| D0 | Reproduce | `skills/zflow-debug/SKILL.md` | auto | `repro-report.md` |
| D1 | Investigate | `skills/zflow-debug/SKILL.md` | auto | `investigation.md` |
| D2 | Analyze | `skills/zflow-debug/SKILL.md` | human | `root-cause.md` |
| D3 | Design Fix | `skills/zflow-debug/SKILL.md` | human | `fix-design.md` |
| D4 | Implement Fix | `skills/zflow-debug/SKILL.md` | auto | `fix-impl-report.md` |
| D5 | Verify | `skills/zflow-debug/SKILL.md` | auto | `verification.md` |

## File Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Sub-skill dirs | `zflow-{phase}` | `zflow-research` |
| Agent prompts | `{role-name}.md` | `architecture-scout.md` |
| Shared files | `_shared/{name}.md` | `_shared/karpathy-preamble.md` |
| Templates | `{output-name}.md` | `scope.md` |
| Workspace phase dirs | `{NN}-{phase}/` | `01-research/` |
| Config files | `{name}.json` | `config.json` |
| Security findings | `SEV-{NNN}` | `SEV-001` |
