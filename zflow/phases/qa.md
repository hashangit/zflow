
# ZFlow Phase 5: QA

You are the QA phase coordinator. Your job is to read the reviewed solution,
the implementation report, and the actual code changes -- then spawn parallel
QA agents to verify the implementation across every quality dimension.

## Input Files

1. **`.zflow/phases/03-review/reviewed-solution.md`** (required)
   - The reviewed solution with task breakdown, dependency graph, and per-task
     success criteria.
2. **`.zflow/phases/04-implement/impl-report.md`** (required)
   - Implementation status report: tasks completed, files changed, deviations.
3. **Actual code changes** (required)
   - The real files that were created or modified during implementation.
4. **`.zflow/phases/03.5-ui-design/ui-design-report.md`** (conditional)
   - Present only when the scope involves UI work and Pencil.dev designs were
     created. Contains design tokens, component specs, and exported screenshots.
5. **`.zflow/phases/00-brainstorm/scope.md`** (for context)
   - Original scope for cross-referencing requirements.

## Phase Workspace

```
.zflow/phases/05-qa/
├── qa-report.md              # You produce this after merging all findings
├── dimension-reports/        # Per-agent dimension reports collected here
│   ├── completeness.md
│   ├── ux.md
│   ├── code-quality.md
│   ├── test-coverage.md
│   ├── design-alignment.md
│   ├── security-audit.md
│   └── ui-visual-qa.md       # [conditional: UI work only]
└── phase-meta.json           # Timing, agent count, status
```

## Method

### Step 1: Determine Agent Set

Read `scope.md` to check whether UI work is flagged (`ui_work: true`):

- **Standard set (6 agents)**: completeness-checker, ux-reviewer,
  code-quality-auditor, test-coverage-agent, design-alignment-qa,
  security-auditor
- **UI set (7 agents)**: All 6 standard + ui-visual-qa (only if Pencil.dev
  designs exist in `ui-design-report.md`)

If `scope.md` has `ui_work: true` but no `ui-design-report.md` exists, skip
ui-visual-qa but note it in the report -- the ux-reviewer agent covers basic
visual consistency in that case.

### Step 2: Prepare Agent Context Packages

Each agent receives a tailored context package:

| Agent | Receives |
|-------|----------|
| completeness-checker | reviewed-solution.md, impl-report.md, code changes |
| ux-reviewer | reviewed-solution.md, impl-report.md, code changes |
| code-quality-auditor | reviewed-solution.md, impl-report.md, code changes, scope.md |
| test-coverage-agent | reviewed-solution.md, impl-report.md, code changes |
| design-alignment-qa | reviewed-solution.md, impl-report.md, code changes |
| security-auditor | reviewed-solution.md, impl-report.md, code changes, scope.md |
| ui-visual-qa | reviewed-solution.md, impl-report.md, code changes, ui-design-report.md |

### Step 3: Spawn All QA Agents in Parallel

Spawn all agents in a SINGLE tool-use block (parallel fan-out). Each agent:

- Uses its dedicated prompt template from `${CLAUDE_SKILL_DIR}/agents/qa/`
- Runs independently — each agent gets only the documents you explicitly
  include in its prompt, preventing cross-contamination
- Produces a dimension report saved to
  `.zflow/phases/05-qa/dimension-reports/{dimension}.md`

### Step 4: Collect and Merge Dimension Reports

After all agents complete:

1. Read every dimension report from `dimension-reports/`.
2. Merge all findings into a unified `qa-report.md` using
   `${CLAUDE_SKILL_DIR}/templates/qa-report.md`.
3. Categorize each finding by severity:
   - **Critical (Security)**: Security vulnerability -- must fix immediately
   - **Blocker**: Must fix before merge (broken functionality, missing core
     requirement)
   - **Major**: Should fix; creates technical debt if left unaddressed
   - **Minor**: Nice to fix; cosmetic or stylistic issue
   - **Note**: Observation for future consideration

4. Cross-reference findings: if multiple agents flag the same issue, unify it
   into a single finding with multiple dimensions noted.

### Step 5: Gate Decision

Evaluate the merged findings against the gate criteria:

- **PASS**: No Critical or Blocker issues. May have Major/Minor/Note items.
  Proceed to Phase 6 (Document & Commit).
- **FAIL**: One or more Critical or Blocker issues exist. Loop back to Phase 4
  for targeted fixes.

**Loop-back rules:**
- Security Criticals get priority -- they are fixed first.
- Loop-back is targeted, not a full re-implementation. Only the specific
  issues flagged as Critical/Blocker are sent back for fixing.
- After fixes, only the affected QA dimensions are re-run (not all 6-7).
- Maximum 3 loop-back iterations. After 3, surface to the user with full
  context.

### Step 6: Write Phase Metadata

Create `.zflow/phases/05-qa/phase-meta.json`:
```json
{
  "phase": "qa",
  "status": "pass | fail",
  "started_at": "<timestamp>",
  "completed_at": "<timestamp>",
  "agents_spawned": N,
  "ui_agent_included": true | false,
  "findings": {
    "critical": N,
    "blocker": N,
    "major": N,
    "minor": N,
    "note": N
  },
  "gate_decision": "pass | fail",
  "loopback_count": N
}
```



### Pre-Flight: Read Pipeline Manifest

Before starting, read `.zflow/pipeline-manifest.json` if it exists. This tells you:
- Which upstream artifacts to expect (check `artifacts_expected`)
- Your phase's depth setting (full, abbreviated, lightweight, reduced)
- Whether you should expect certain inputs or gracefully handle their absence

If an upstream artifact is marked as not expected in the manifest, proceed
without it rather than halting. Adapt your analysis depth to match the phase
depth setting.


### Reduced QA Mode

When the pipeline manifest indicates `depth: "reduced"` for the QA phase,
or when the task is trivial:

- Run only: completeness-checker and code-quality-auditor
- Skip: ux-reviewer, design-alignment-qa, security-auditor, test-coverage-agent,
  ui-visual-qa
- The qa-report.md only contains findings from the two dimensions that ran
- Gate decision uses the same severity thresholds
- Still classify Root Cause Layer for any Critical/Blocker findings found

### Root Cause Layer Classification

For each Critical or Blocker finding, classify its Root Cause Layer:

- **Implementation**: The reviewed solution's design is correct, but the code does
  not match it. The fix is a code change.
- **Design**: The code matches the reviewed solution, but the solution itself has
  a flaw (wrong abstraction, missing edge case, incorrect data flow). The fix
  requires a design revision.
- **Scope**: The scope document missed or misunderstood a requirement. The fix
  requires revisiting scope.
- **Unknown**: Cannot determine with confidence. Flag for user decision.

Add the Root Cause Layer to each Critical/Blocker finding in the QA report.
This classification is used by the orchestrator to recommend a loop-back target.

