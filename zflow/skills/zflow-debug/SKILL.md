---
name: zflow-debug
description: >
  Structured multi-agent debugging workflow. Use when the user reports a bug,
  regression, crash, wrong output, performance issue, or security vulnerability
  and wants a systematic root-cause analysis and fix. Invoked only by the
  ZFlow orchestrator — does not auto-trigger on user messages.
disable-model-invocation: true
---

# ZFlow Debug Workflow Orchestrator

You are the debug workflow coordinator. You orchestrate a structured, multi-phase
debugging process that goes from bug report to verified fix through specialized
sub-agents. Every phase produces a document that feeds into the next.

## Iron Law

No fix without root cause. No root cause without investigation. No investigation
without reproduction. Every phase earns its right to proceed.

## Workflow Phases

```
D0: REPRODUCE ──► D1: INVESTIGATE ──► D2: ANALYZE ──► D3: DESIGN FIX ──► D4: IMPLEMENT ──► D5: VERIFY
      │                  │                   │                │                 │                │
      ▼                  ▼                   ▼                ▼                 ▼                ▼
  repro-report.md   investigation.md    root-cause.md    fix-design.md    fix-impl-report.md  verification.md
```

## Initialization

1. Create the debug workspace:
   ```
   .zflow/debug/session-{timestamp}/
       ├── d0-reproduce/
       ├── d1-investigate/
       ├── d2-analyze/
       ├── d3-design-fix/
       ├── d4-implement-fix/
       └── d5-verify/
   ```

2. Determine bug type from user description:
   - **crash**: Application terminates or throws unhandled exception
   - **wrong-output**: Produces incorrect results
   - **performance**: Slow, memory leak, excessive resource usage
   - **intermittent**: Not consistently reproducible
   - **security-vulnerability**: Exploitable flaw, data exposure, auth bypass

3. Load configuration from `.zflow/config.json` if it exists (use defaults otherwise):
   - `debug.escalation_threshold` (default: 3)
   - `debug.auto_run_tests` (default: true)
   - `debug.security_impact_assessment` (default: true)
   - `debug.gates` (per-phase gate settings)

## Phase Execution

### Phase D0: Reproduce

**Agent prompt**: Read `agents/debug/reproducer.md` (include the Karpathy preamble from `agents/_shared/karpathy-preamble.md`)
**Mode**: Interactive (agent needs to run code and observe output)
**Gate**: `auto` by default (reproduction is self-validating)

Steps:
1. Spawn the reproducer agent with the user's bug description
2. Agent confirms reproducibility, documents steps, captures error output
3. Agent identifies minimal reproduction case
4. Output saved to `.zflow/debug/session-{timestamp}/d0-reproduce/repro-report.md`
5. Validate: reproduction steps exist, expected vs actual documented, classification assigned

If bug is NOT reproducible:
- Ask user for more context (environment, timing, frequency)
- Attempt 2 more reproduction tries with varied inputs
- If still not reproducible, mark as `intermittent` and proceed with best-effort investigation

### Phase D1: Investigate (Agent Swarm)

**Agents** (spawn all in parallel):

| Agent | Prompt File | Focus |
|-------|----------|-------|
| Call Chain Tracer | `agents/debug/call-chain-tracer.md` | Trace execution backward from symptom |
| Data Flow Tracer | `agents/debug/data-flow-tracer.md` | Follow invalid data to its source |
| Pattern Scanner | `agents/debug/pattern-scanner.md` | Find similar patterns that may share the bug |
| History Investigator | `agents/debug/history-investigator.md` | Git blame/log analysis |
| Security Impact Assessor | `agents/debug/security-impact-assessor.md` | Security implications of the bug |

**Mode**: All agents run independently in parallel
**Gate**: `auto` by default

Steps:
1. Read `repro-report.md` from D0
2. Spawn all 5 investigation agents simultaneously in a single tool-use block.
   For each agent, read its prompt file and the Karpathy preamble from
   `agents/_shared/karpathy-preamble.md`, and include both plus the
   `repro-report.md` contents in the agent's prompt.
3. Each agent receives `repro-report.md` as input
4. Merge individual reports into `investigation.md`
5. Save to `.zflow/debug/session-{timestamp}/d1-investigate/investigation.md`
6. If security-impact-assessor rated High/Critical: flag for expedited handling

### Phase D2: Root Cause Analysis

**Agent prompt**: Read `agents/debug/root-cause-analyst.md` (include Karpathy preamble from `agents/_shared/karpathy-preamble.md`)
**Mode**: Independent agent
**Gate**: `human` by default (critical checkpoint)

Steps:
1. Read `repro-report.md` and `investigation.md`
2. Spawn root-cause-analyst agent
3. Agent synthesizes findings into root cause hypothesis
4. Output saved to `.zflow/debug/session-{timestamp}/d2-analyze/root-cause.md`
5. **HUMAN GATE**: Present root cause to user for review
   - Show: Symptom, Root Cause, Causal Chain, Confidence Level
   - Ask: "Does this root cause analysis align with your understanding?"
   - If user disagrees or confidence is Low: loop back to D1 for more investigation
   - If user approves: proceed to D3

### Phase D3: Design Fix

**Agent prompt**: Read `agents/debug/fix-designer.md` (include Karpathy preamble from `agents/_shared/karpathy-preamble.md`)
**Mode**: Independent agent
**Gate**: `human` by default (critical checkpoint)

Steps:
1. Read `root-cause.md`
2. Spawn fix-designer agent with 3 parallel reviewers:
   - **Minimal Fix Reviewer**: Is this the smallest possible fix? (Karpathy: Surgical Changes)
   - **Regression Risk Reviewer**: What could break from this fix?
   - **Pattern Fix Reviewer**: Do similar patterns need the same fix?
3. Output saved to `.zflow/debug/session-{timestamp}/d3-design-fix/fix-design.md`
4. **HUMAN GATE**: Present fix design to user for review
   - Show: Proposed changes, regression risks, pattern fixes
   - Ask: "Does this fix design look correct? Any concerns?"
   - If user approves: proceed to D4
   - If user wants changes: update fix-design.md and re-gate

### Phase D4: Implement Fix

**Agent**: `agents/implement/focused-implementer.md` (shared with dev workflow)
**Mode**: Independent agent
**Gate**: `auto` by default

Steps:
1. Read `fix-design.md`
2. Spawn focused-implementer agent with the fix design
3. Agent applies the fix under Karpathy Surgical Changes constraint

**Escalation Pattern** (3-strike rule):
```
Attempt 1: Implement designed fix → run tests
  │ Pass → Done, proceed to D5
  └ Fail →
Attempt 2: Re-analyze with fresh context → implement adjusted fix → run tests
  │ Pass → Done, proceed to D5
  └ Fail →
Attempt 3: Deeper re-analysis → implement → run tests
  │ Pass → Done, proceed to D5
  └ Fail →
ESCALATE: Pause. Present full context to user.
  "Three fix attempts have failed. This may indicate:
   A) The root cause analysis is incomplete
   B) The fix design doesn't address the actual defect
   C) There's an architectural issue involved
   Recommend: Architectural review before proceeding."
```

4. Output saved to `.zflow/debug/session-{timestamp}/d4-implement-fix/fix-impl-report.md`

### Phase D5: Verify

**Agent prompt**: Read `agents/debug/fix-verifier.md` (include Karpathy preamble from `agents/_shared/karpathy-preamble.md`)
**Mode**: Independent agent (4 parallel verification dimensions)
**Gate**: `auto` by default

Steps:
1. Read all previous debug phase outputs + code changes
2. Spawn verification across 4 dimensions:
   - **Regression Verification**: Full test suite passes
   - **Fix Verification**: Original bug reproduction steps now pass
   - **Pattern Verification**: Similar fixes (if any) also work
   - **Security Verification**: Fix doesn't introduce new vulnerabilities
3. Output saved to `.zflow/debug/session-{timestamp}/d5-verify/verification.md`
4. If any dimension fails: loop back to D4 for targeted fix (does NOT count as escalation attempt)
5. If all dimensions pass: present summary to user

## Final Summary

After D5 completes, present to the user:

```
## Debug Session Complete

**Bug**: {one-line description}
**Root Cause**: {one-line root cause}
**Fix**: {one-line fix summary}
**Files Changed**: {list}
**Tests**: {pass/fail counts}
**Security Impact**: {None / addressed / flagged}
**Session Workspace**: .zflow/debug/session-{timestamp}/

All phase artifacts preserved for audit trail.
```

## Phase Resumption

If a debug session is interrupted, check `.zflow/debug/session-{timestamp}/` for
the latest completed phase and resume from there. Each phase's output document is
the input for the next, so any phase can be re-run independently.

## Anti-Patterns

- Do NOT skip D0 (reproduce) to jump straight to investigation
- Do NOT implement a fix before D2 (root cause) is confirmed
- Do NOT patch symptoms — always address root cause
- Do NOT exceed 3 fix attempts without escalating
- Do NOT run verification on incomplete fixes
- Do NOT ignore security-impact-assessor findings
