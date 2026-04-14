# Phase Gates Reference

Criteria and configuration for phase transitions in ZFlow workflows.

---

## Overview

Every phase transition in ZFlow passes through a gate. The gate ensures that the output is valid, complete, and (optionally) reviewed by a human before the next phase begins. Gates are the primary quality control mechanism between phases.

---

## Gate Components

Each gate performs up to three checks:

### 1. Artifact Validation

The output document exists and follows the expected template structure. This is always performed regardless of gate mode.

**Template Section Classification:**

Templates use a three-tier section classification:
- **Required** sections MUST be present and populated. Absence causes gate failure.
- **Expected** sections SHOULD be present. If omitted, a one-line note explaining why is required.
- **Optional** sections are NOT validated. Include, restructure, or omit freely.

**Checks:**
- The output file exists at the expected path in `.zflow/phases/`
- All **Required** sections from the template are present and populated
- **Expected** sections are either present or explicitly noted as omitted with a reason
- No required section is left as boilerplate (no "TBD", "TODO", or unmodified template text in Required sections)
- The document is non-empty and well-formed

**Example:** `scope.md` must contain Required sections (Problem Statement, Success Criteria, Scope Boundaries, MVP Definition). Expected sections (Constraints, Affected Systems, Known Risks) should be present or noted as omitted. Optional sections (User's Mental Model, Explicitly Deferred) are not validated.

### 2. Completeness Check

All required sections are populated with meaningful content. This goes beyond structural validation to verify semantic completeness.

**Checks:**
- Each section has substantive content (not just a heading)
- Cross-references within the document are consistent (e.g., task dependencies reference tasks that exist)
- The scope boundaries clearly define what is in and out of scope
- Success criteria are measurable and unambiguous

### 3. Human Approval

The user reviews the output and decides whether to proceed. Only performed when the gate mode is `human`.

**Options for the user:**
- **Approve:** Proceed to the next phase
- **Request changes:** Specify what needs to change; the phase re-runs with the feedback
- **Abort:** Stop the workflow entirely

---

## Default Gate Settings

### Development Workflow

| Phase | Default Gate | Rationale |
|-------|-------------|-----------|
| Brainstorm | human | Scope is foundational -- getting it wrong propagates errors |
| Research | auto | Research is factual; trust the agent to gather codebase data |
| Design | human | Design decisions have high impact; user should validate |
| Review | human | Review may adjust the solution; user should see changes |
| UI Design | human | Visual design requires human aesthetic judgment |
| Implement | auto | Implementation follows an approved design; trust the agent |
| QA | human | QA findings may require user decisions on severity triage |
| Document | auto | Documentation is straightforward once everything else is approved |

### Debugging Workflow

| Phase | Default Gate | Rationale |
|-------|-------------|-----------|
| Reproduce | auto | Reproduction is factual |
| Investigate | auto | Investigation is factual |
| Analyze | human | Root cause interpretation may need human judgment |
| Design Fix | human | Fix approach should be validated before implementation |
| Implement Fix | auto | Fix follows an approved design |
| Verify | auto | Verification is factual (tests pass or fail) |

---

## Customizing Gates

Edit `.zflow/config.json` to change gate behavior:

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
    }
  },
  "debug": {
    "gates": {
      "reproduce": "auto",
      "investigate": "auto",
      "analyze": "human",
      "design_fix": "human",
      "implement_fix": "auto",
      "verify": "auto"
    }
  }
}
```

### Gate Modes

| Mode | Artifact Validation | Completeness Check | Human Review |
|------|:------------------:|:-----------------:|:------------:|
| `human` | Yes | Yes | Yes |
| `auto` | Yes | Yes | No |

Note: artifact validation and completeness checks always run. The only difference between modes is whether the user is asked to review.

---

## How Auto-Pass Works

When a gate is set to `auto`:

1. The phase completes and writes its output
2. Artifact validation runs (file exists, structure is correct)
3. Completeness check runs (sections are populated)
4. If both pass, the workflow proceeds automatically to the next phase
5. If either fails, the gate fails even in auto mode

**Auto-pass does NOT skip quality checks.** It only skips the human review step. The structural and completeness validations are always enforced.

### When to Use Auto-Pass

Use auto-pass for phases where:
- The output is primarily factual (research, investigation, reproduction)
- The output follows an already-approved design (implementation, documentation)
- You trust the agent's output quality for that phase type
- You want to reduce interaction overhead for well-understood work

### When to Keep Human Gates

Keep human review for phases where:
- The output involves judgment calls (scope, design, fix approach)
- The output may be adjusted before proceeding (review, QA findings)
- You want to catch over-engineering or scope drift early
- Aesthetic or subjective decisions are involved (UI design)

---

## What Happens When a Gate Fails

### Artifact Validation Failure

If the output file is missing, structurally invalid, or contains unmodified template text:

1. The coordinator reports the specific validation failure
2. The phase is re-run from scratch
3. If re-run also produces a failing output, the issue is surfaced to the user (even in auto mode)
4. The user can then decide to retry, adjust configuration, or abort

### Completeness Check Failure

If sections are present but semantically incomplete:

1. The coordinator reports which sections failed completeness checks
2. The phase is re-run with the completeness feedback injected into the agent context
3. If re-run still fails, the issue surfaces to the user

### Human Gate Rejection

When a user requests changes at a human gate:

1. The user's feedback is captured
2. The phase agent receives the feedback along with its original input
3. The agent revises the output addressing the feedback
4. The revised output goes through the gate again (including artifact validation)
5. This loop continues until the user approves or aborts

---

## Overriding Gates for Rapid Iteration

### Skip Phases Entirely

For rapid iteration, skip phases that are not needed:

```json
{
  "workflow": {
    "skip_phases": ["brainstorm", "research"]
  }
}
```

When phases are skipped:
- The workspace directories for those phases are not created
- Downstream phases operate without those outputs (design works without research, implementation works without design)
- The coordinator warns if a downstream phase expects input that is not available

### Set All Gates to Auto

```json
{
  "workflow": {
    "gates": {
      "brainstorm": "auto",
      "research": "auto",
      "design": "auto",
      "review": "auto",
      "ui_design": "auto",
      "implement": "auto",
      "qa": "auto",
      "document": "auto"
    }
  }
}
```

This runs the full workflow with minimal human interaction. Artifact validation and completeness checks still enforce structural quality. Use this only when you have high confidence in the workflow for the type of task you are doing.

### Resume and Skip

You can combine resumption with phase skipping. For example, if you ran through brainstorm and research, then want to jump straight to implementation with an existing design:

1. Place your existing design at `.zflow/phases/03-review/reviewed-solution.md`
2. Set `current-phase.json` to `{"phase": "implement", "status": "pending"}`
3. Set `skip_phases` to include the phases you manually completed
4. Run `/using-zflow` -- it will resume from the implement phase

---

## Gate Validation Details by Phase

### Phase 0: Brainstorm (scope.md)

Required sections:
- Problem Statement
- Success Criteria (must be measurable)
- Constraints
- Affected Systems
- Scope Boundaries (clear in/out)
- MVP Definition
- Known Risks
- UI Work Flag (yes/no)

### Phase 1: Research (research-report.md)

Required sections:
- Architecture overview
- Dependency map
- Pattern inventory
- Test infrastructure
- Related/affected code
- UI system (conditional)
- Key Findings (synthesis)

### Phase 2: Design (solution.md)

Required sections:
- Chosen Approach (with rationale)
- Alternatives Considered
- Architecture Overview
- Component Breakdown
- Data Flow
- Error Handling
- Testing Strategy
- Task Breakdown (with dependency graph + success criteria per task)
- Risk Register
- Open Questions

### Phase 3: Review (reviewed-solution.md)

Required sections:
- All solution.md sections (with adjustments applied)
- Appendix: reviewer findings
- Appendix: accepted/rejected findings with rationale
- Appendix: self-review fixes applied

### Phase 4: Implement (impl-report.md)

Required sections:
- Per-task status (completed/partial/failed)
- Files changed per task
- Deviations from design (with justification for each)
- Any unimplemented tasks with reason

### Phase 5: QA (qa-report.md)

Required sections:
- Executive summary (counts by severity)
- Per-dimension findings
- Security audit findings (or clean report)
- Recommended actions

### Phase 6: Document

Required:
- Updated documentation files
- CHANGELOG entry
- Commit message (conventional commits format)

---

## QA Gate Loop-Back Protocol

When QA finds Critical or Blocker issues, the orchestrator classifies findings by
Root Cause Layer and presents a recommendation to the user:

### Root Cause Layer Classification

| Layer | Meaning | Recommended Loop-Back |
|-------|---------|----------------------|
| Implementation | Design is sound, code doesn't match it | Phase 4 (Implement) |
| Design | Code matches design, design is flawed | Phase 2 (Design) |
| Scope | Scope missed a requirement | Phase 0 (Brainstorm) |
| Unknown | Ambiguous | User decides |

### Artifact Preservation by Loop-Back Target

| Loop-Back To | Preserved | Regenerated |
|-------------|-----------|-------------|
| Phase 4 | All design artifacts | code + impl-report |
| Phase 2 | scope.md, research-report.md, qa-report.md (as context) | solution.md, reviewed-solution.md, impl-report.md |
| Phase 0 | research-report.md | Everything else (soft restart) |

### Constraints

- Security Criticals always get priority regardless of loop-back target
- Maximum 3 iterations for the total QA feedback loop
- Phase 2 and Phase 0 loop-backs always require user confirmation
- The orchestrator presents options and a recommendation; the user decides

---

## Dynamic Pipeline Gates

When a pipeline profile other than Full is selected, gate behavior adapts:

- **Quick Fix**: Only implement, QA, and document phases have gates. Design sketch gate replaces design gate.
- **Standard**: Research gate is skipped (phase not run). Brainstorm gate is abbreviated.
- **Full**: Standard gate configuration as documented above.
- **Extended**: All gates default to human.

Gate modes are recorded in `pipeline-manifest.json` per phase.
