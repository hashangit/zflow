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

When a human gate is required, present a clear, jargon-free summary:

```
## {Phase name} step is done

**What we produced**: {plain-language description, e.g. "A document describing
what you want to build and why"}
**Time spent**: {elapsed, or "just now" if brief}
**Number of agents that worked on this**: {count}

### What was decided
- {decision 1 in plain language}
- {decision 2 in plain language}

### What happens next
{Brief description of the next step, e.g. "Next, we'll research your codebase
to understand how this fits with what's already there."}

Ready to move on?

  [A] Looks good — proceed to the next step
  [B] I have changes or feedback
  [C] Stop the workflow
```

## Dev Workflow Phases

| # | Phase | Phase Doc | Gate | Key Artifact |
|---|-------|-----------|------|-------------|
| 0 | Brainstorm | `phases/brainstorm.md` | human | `scope.md` |
| 1 | Research | `phases/research.md` | auto | `research-report.md` |
| 2 | Design | `phases/design.md` | human | `solution.md` |
| 3 | Review | `phases/review.md` | human | `reviewed-solution.md` |
| 3.5 | UI Design | `phases/ui-design.md` | human | `ui-design-report.md` |
| 4 | Implement | `phases/implement.md` | auto | `impl-report.md` |
| 5 | QA | `phases/qa.md` | human | `qa-report.md` |
| 6 | Document | `phases/document.md` | auto | changelog + commit |

## Debug Workflow Phases

| # | Phase | Phase Doc | Gate | Key Artifact |
|---|-------|-----------|------|-------------|
| D0 | Reproduce | `phases/debug.md` | auto | `repro-report.md` |
| D1 | Investigate | `phases/debug.md` | auto | `investigation.md` |
| D2 | Analyze | `phases/debug.md` | human | `root-cause.md` |
| D3 | Design Fix | `phases/debug.md` | human | `fix-design.md` |
| D4 | Implement Fix | `phases/debug.md` | auto | `fix-impl-report.md` |
| D5 | Verify | `phases/debug.md` | auto | `verification.md` |

## File Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Phase docs | `{phase}.md` | `research.md` |
| Agent prompts | `{role-name}.md` | `architecture-scout.md` |
| Shared files | `_shared/{name}.md` | `_shared/karpathy-preamble.md` |
| Templates | `{output-name}.md` | `scope.md` (in `assets/`) |
| Workspace phase dirs | `{NN}-{phase}/` | `01-research/` |
| Config files | `{name}.json` | `config.json` |
| Security findings | `SEV-{NNN}` | `SEV-001` |
