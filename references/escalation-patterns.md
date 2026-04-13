# Escalation Patterns Reference

When and how to escalate issues in ZFlow workflows.

---

## Overview

Escalation in ZFlow is the process of increasing the level of attention, expertise, or human involvement when an agent encounters a problem it cannot resolve independently. Escalation happens in both the development and debugging workflows, though the patterns differ.

---

## The 3-Strike Rule (Debug Workflow)

The primary escalation mechanism is the 3-strike rule, used during Phase D4 (Implement Fix) of the debugging workflow.

### How It Works

```
Attempt 1: Implement the designed fix --> Run tests --> Pass? --> Done
                                                        |
                                                        v Fail
Attempt 2: Re-analyze with fresh context + failure info --> Implement revised fix --> Run tests --> Pass? --> Done
                                                                                            |
                                                                                            v Fail
Attempt 3: Re-analyze with all accumulated failure context --> Implement --> Run tests --> Pass? --> Done
                                                                                           |
                                                                                           v Fail
ESCALATE: Senior architectural review OR surface to user
```

### Attempt 1: Direct Fix

- Implement the fix exactly as designed in `fix-design.md`
- Run the test suite to verify
- If tests pass: done, proceed to verification
- If tests fail: proceed to Attempt 2

**What the agent gets:** The fix design + original root cause analysis + reproduction steps

### Attempt 2: Re-Analysis with Fresh Context

- The agent receives the failure output from Attempt 1 (test failures, error messages, unexpected behavior)
- Re-analyzes the problem: was the fix design wrong? Was the root cause incomplete? Was there a secondary issue?
- Designs a revised fix based on the new information
- Implements the revised fix
- If tests pass: done
- If tests fail: proceed to Attempt 3

**What the agent gets:** Everything from Attempt 1 + Attempt 1 failure output + revised analysis

### Attempt 3: Full Context Re-Analysis

- The agent receives all accumulated failure context from Attempts 1 and 2
- Performs a deep re-examination of the entire problem
- Considers whether the root cause analysis itself was wrong
- May take a completely different approach to the fix
- Implements the new approach
- If tests pass: done
- If tests fail: ESCALATE

**What the agent gets:** Everything from Attempts 1-2 + Attempt 2 failure output + full reconsideration

### After 3 Failures: Escalation

The coordinator has two escalation options:

**Option A: Senior Architectural Review**
- Spawn a fresh agent with a "senior architect" perspective
- Provide all accumulated context: root cause, fix design, three attempts, all failure outputs
- The senior agent reviews the entire problem de novo and proposes a path forward
- If the senior agent proposes a fix, it is implemented as Attempt 4
- If the senior agent concludes the problem needs design-level changes, escalate to user

**Option B: Surface to User**
- Present the full context to the user: what was tried, what failed, what was learned
- The user decides: provide more context, change the approach, fix manually, or abort

**Default behavior:** After 3 failures, the coordinator surfaces to the user (Option B) with the option to request a senior architectural review (Option A).

---

## Escalation to Architectural Review

### When It Happens

Architectural review escalation is triggered when:

1. **Three fix attempts fail** (debug workflow)
2. **The root cause analysis has low confidence** (the root-cause-analyst flagged it as Low)
3. **The fix design requires changes to the architecture** (not just a localized bug fix)
4. **Multiple related bugs suggest a systemic design issue**

### What the Architectural Review Does

1. Re-examines the original design decisions that led to the bug
2. Evaluates whether the architecture needs modification
3. Proposes either a targeted architectural fix or a broader refactoring plan
4. If refactoring is needed, recommends running a development workflow cycle

### Who Performs It

A fresh agent with the `solution-architect.md` prompt (the same agent used in Phase 2 of the development workflow). This agent has architectural-level thinking but no prior context about the specific bug -- it reviews everything with fresh eyes.

---

## Escalation to User

### When It Happens

The user is surfaced to directly when:

1. **Three fix attempts fail AND senior review does not resolve it**
2. **The root cause is outside the codebase** (infrastructure, third-party service, configuration)
3. **The fix requires a decision that only the user can make** (API contract change, breaking change, feature trade-off)
4. **Security impact is rated High or Critical** (the user needs to know immediately)
5. **Cost or time estimates exceed reasonable bounds** (the workflow is taking too long)

### What the User Receives

When surfacing to the user, the coordinator provides:

1. **Summary:** One-paragraph explanation of what happened
2. **Root Cause:** The root cause analysis
3. **Attempts Made:** What was tried and what happened for each attempt
4. **Failure Analysis:** Why each attempt failed (in plain language)
5. **Current State:** What the codebase looks like now (any partial changes)
6. **Options:** What the user can do next (with recommendations)

### User Options

- **Provide additional context:** The user shares information the agents did not have
- **Change approach:** The user directs a different fix strategy
- **Fix manually:** The user takes over and resolves it outside ZFlow
- **Abort:** Stop the workflow; partial changes are preserved in the workspace
- **Run development workflow:** If the issue is architectural, switch to a full development cycle

---

## Escalation Paths: Development vs Debug

### Development Workflow Escalation

The development workflow has fewer escalation points because phases are sequential with human gates. Escalation happens at:

| Trigger | Action |
|---------|--------|
| QA finds critical/blocker issues | Loop back to Phase 4 for targeted fixes |
| QA critical issues persist after fix loop | Surface to user with full QA findings |
| Security audit finds critical vulnerability | Immediate notification + required fix before proceeding |
| Implementation task fails | Coordinator retries once, then marks as blocked and continues |
| Multiple implementation tasks blocked | Surface to user with dependency analysis |

### Debug Workflow Escalation

The debug workflow has more structured escalation because fix attempts are iterative:

| Trigger | Action |
|---------|--------|
| Root cause confidence is Low | Flag for extra scrutiny in fix design phase |
| Fix attempt 1 fails | Re-analyze with failure context |
| Fix attempt 2 fails | Deep re-analysis with all context |
| Fix attempt 3 fails | Escalate: senior review or surface to user |
| Security impact is High/Critical | Expedited handling + mandatory security review of fix |
| Pattern scanner finds similar bugs | Escalate from single fix to systematic pattern fix |

---

## Timeout Escalation

### Agent Timeouts

Each sub-agent has a reasonable execution timeout. If an agent exceeds this timeout:

1. The coordinator kills the agent
2. The agent's partial output (if any) is preserved
3. The coordinator retries the agent once with the same input
4. If the retry also times out, the task is marked as timed out
5. For fan-out patterns (research, review, QA), other agents continue; the timed-out agent's dimension is marked as incomplete
6. For tiered patterns (implementation), dependent tasks are marked as blocked

### Phase Timeouts

If an entire phase exceeds a generous timeout:

1. The coordinator reports which agents completed and which did not
2. Partial results are preserved in the workspace
3. The user is informed and can decide to retry, proceed with partial results, or abort

### Configuring Timeouts

Timeouts are not directly configurable via `config.json` but can be influenced by:

- `max_parallel_agents`: Fewer parallel agents means each gets more resources
- Task complexity estimates (S/M/L): The coordinator uses these to allocate time budgets
- Escalation threshold: Setting this to a value other than 3 changes how many fix attempts are made before escalating

```json
{
  "debug": {
    "escalation_threshold": 3
  }
}
```

---

## Cost Escalation

### Token Cost Awareness

ZFlow spawns many sub-agents, each consuming tokens. The coordinator monitors accumulated cost:

1. After each phase completes, the coordinator estimates the token cost of the completed phase
2. If the cumulative cost exceeds a reasonable threshold, the coordinator warns the user
3. The user can decide to continue, switch to lighter phases, or abort

### Cost Control Mechanisms

- `max_parallel_agents`: Limits simultaneous agent spawns (default: 5)
- `audit_depth`: Controls how thorough the security audit is (full/targeted/minimal)
- Phase skipping: Skip phases that are not needed to reduce total agent spawns
- Auto gates: Reduce human interaction overhead but do not reduce agent count

### When Cost Becomes an Escalation Trigger

If the coordinator detects that the current workflow is significantly exceeding expected costs (e.g., a Phase 4 implementation that should have 3 tiers is on tier 7 because tasks keep failing), it:

1. Pauses the current phase
2. Reports the cost situation to the user
3. Recommends adjustments (reduce max_parallel_agents, skip remaining tiers, abort)
4. The user decides how to proceed

---

## Security Escalation

Security findings have their own escalation path due to their urgency:

### During Development (QA Phase)

| Severity | Action |
|----------|--------|
| Critical | Immediate notification. Fix is required before proceeding. Loops back to Phase 4. |
| High | Strongly recommended fix. User is informed and decides whether to fix now or defer. |
| Medium | Included in QA report. User triages at the QA gate. |
| Low / Informational | Noted in QA report. No escalation. |

### During Debugging (Investigation Phase)

If the `security-impact-assessor` rates the bug's security impact as High or Critical:

1. The root cause analysis includes security impact assessment
2. The fix design must include security review
3. The fix verification includes a dedicated security verifier
4. The user is notified at the earliest possible gate (D2: Analyze)
5. The fix is treated as expedited -- it takes priority over other workflow concerns

---

## Escalation Decision Matrix

| Situation | Development Workflow | Debug Workflow |
|-----------|---------------------|----------------|
| Single agent failure | Retry once, continue | Retry once, continue |
| Phase-level failure | Re-run phase once | Apply 3-strike rule |
| Persistent failure | Surface to user | Senior review then user |
| Security critical | Immediate loop-back | Expedited fix path |
| Cost overrun | Warn user, offer options | Warn user, offer options |
| Timeout | Preserve partial, retry | Preserve partial, retry |
| Low confidence output | Flag in next phase input | Extra scrutiny in next phase |
| User rejection at gate | Revise and re-present | Revise and re-present |
