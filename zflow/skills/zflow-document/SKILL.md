---
name: zflow-document
description: >
  Documentation and commit phase for ZFlow. Reads the full document chain
  (scope.md through qa-report.md), updates/creates documentation (README,
  API docs, inline comments), updates CHANGELOG, generates a conventional
  commit message, and stages changes for commit with a human approval gate.
  Invoked by the main ZFlow orchestrator during Phase 6. Does not
  auto-trigger on user messages.
disable-model-invocation: true
---

# ZFlow Phase 6: Document & Commit

You are the documentation and commit phase coordinator. Your job is to review
the full document chain, update all relevant documentation, generate a
CHANGELOG entry, create a conventional commit message, and stage everything
for the user to approve and commit.

## Input Files

Read the complete document chain in order:

1. **`.zflow/phases/00-brainstorm/scope.md`** (required)
   - Original requirements and intent.
2. **`.zflow/phases/01-research/research-report.md`** (required)
   - Codebase context that informed the design.
3. **`.zflow/phases/02-design/solution.md`** (required)
   - The chosen approach and task breakdown.
4. **`.zflow/phases/03-review/reviewed-solution.md`** (required)
   - The reviewed solution with adjustments.
5. **`.zflow/phases/03.5-ui-design/ui-design-report.md`** (conditional)
   - Present only when UI work was designed with Pencil.dev.
6. **`.zflow/phases/04-implement/impl-report.md`** (required)
   - Implementation status, files changed, deviations.
7. **`.zflow/phases/05-qa/qa-report.md`** (required)
   - QA findings, severity ratings, resolved issues.

## Phase Workspace

```
.zflow/phases/06-document/
├── changes-summary.md    # You produce this: summary of all changes
└── phase-meta.json       # Timing, status
```

## Method

### Step 1: Read the Full Document Chain

Read every document listed above in order. Build a complete picture of:

- What was requested (scope.md)
- What was planned (solution.md, reviewed-solution.md)
- What was actually built (impl-report.md)
- What passed QA (qa-report.md)
- Whether security findings were addressed (qa-report.md security section)

If any required document is missing, stop and report which one. The document
chain must be complete before documentation can be accurate.

### Step 2: Identify Documentation Needs

From the document chain, determine what needs updating:

1. **README.md** — if the change adds new features, changes usage, adds
   dependencies, or modifies the public API
2. **API documentation** — if endpoints were added, changed, or removed
3. **Inline code comments** — if complex logic was introduced that needs
   explanation beyond what the code itself conveys
4. **Configuration docs** — if new config options were added
5. **CHANGELOG.md** — always updated for this phase

Do NOT update documentation for trivial changes. If the implementation was
a bug fix with no API impact, only the CHANGELOG needs updating.

### Step 3: Deploy the Documentation Writer Agent

Spawn the documentation writer agent. For its prompt:
1. Read `agents/document/documentation-writer.md`
2. Read `agents/_shared/karpathy-preamble.md` (include the Karpathy preamble)
3. Include the full contents of: `scope.md`, `impl-report.md`,
   `qa-report.md`, and the list of changed files from `impl-report.md`
4. Call the Agent tool with that prompt and description "documentation writer"

The agent will:
- Update/create relevant documentation files
- Generate a CHANGELOG entry
- Create a conventional commit message

### Step 4: Collect and Review Agent Output

After the documentation writer completes:

1. Read its output report from `.zflow/phases/06-document/changes-summary.md`
2. Verify the CHANGELOG entry is well-structured and accurate
3. Verify the commit message follows conventional commits format
4. Check that documentation updates are proportional to the change size
5. If security findings were addressed in QA, confirm the CHANGELOG has
   a Security section noting them

### Step 5: Present for Human Approval

Display the following to the user for review:

1. **CHANGELOG entry** — the full entry that will be added
2. **Commit message** — the conventional commit message
3. **Documentation changes summary** — list of files updated and what changed
4. **Staged files list** — all files that will be included in the commit

Ask: "Review the above. Ready to commit, or would you like changes?"

### Step 6: Commit (After Approval)

Once the user approves:

1. Stage all relevant files (documentation + implementation + config changes)
2. Do NOT stage files that should not be committed (.env, secrets, build
   artifacts, .zflow/ workspace files)
3. Commit with the approved conventional commit message

### Step 7: Write Phase Metadata

Create `.zflow/phases/06-document/phase-meta.json`:
```json
{
  "phase": "document",
  "status": "complete",
  "started_at": "<timestamp>",
  "completed_at": "<timestamp>",
  "docs_updated": ["<list of docs>"],
  "changelog_updated": true,
  "commit_hash": "<short hash>"
}
```

## Conventional Commit Format

The commit message must follow the Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: feat, fix, docs, style, refactor, perf, test, chore, security

**Rules**:
- Subject line: max 72 characters, imperative mood, no period
- Body: explain what and why (not how), wrap at 72 characters
- Footer: reference issues, note breaking changes
- If security findings were addressed: type is `security` or include a
  `Security:` trailer in the footer
- **Co-author requirement**: Every commit MUST end with exactly one co-author:
  `Co-Authored-By: ZFlow <noreply@inferencequotient.com>`. No other co-author lines.
  The git author is always the user running ZFlow.

## CHANGELOG Entry Format

```markdown
## [X.Y.Z] - YYYY-MM-DD

### Added
- {New feature or capability}

### Changed
- {Change to existing functionality}

### Fixed
- {Bug fix}

### Security
- {Security vulnerability addressed} (if applicable)

### Removed
- {Removed feature or capability}
```

Only include sections that have entries. Do not create empty sections.



### Pre-Flight: Read Pipeline Manifest

Before starting, read `.zflow/pipeline-manifest.json` if it exists. This tells you:
- Which upstream artifacts to expect (check `artifacts_expected`)
- Your phase's depth setting (full, abbreviated, lightweight, reduced)
- Whether you should expect certain inputs or gracefully handle their absence

If an upstream artifact is marked as not expected in the manifest, proceed
without it rather than halting. Adapt your analysis depth to match the phase
depth setting.

## Anti-Patterns

- Do NOT modify code — documentation only
- Do NOT over-document trivial changes
- Do NOT commit without explicit user approval
- Do NOT include .zflow/ workspace files in the commit
- Do NOT stage files with secrets or credentials
- Do NOT include any co-author other than ZFlow in the commit message
- Do NOT write a vague CHANGELOG entry like "various improvements"
- Do NOT skip the CHANGELOG update

## Success Criteria

- All relevant documentation is current and accurate
- CHANGELOG has a well-structured entry reflecting the change
- Commit message follows conventional commits format
- No code files are modified during this phase
- User explicitly approved before commit
- If security findings were addressed: noted in CHANGELOG Security section
- Phase metadata is written and accurate
