# Escalation Patterns Reference

When and how to escalate issues in ZFlow workflows.

---

## The 3-Strike Rule (Debug Workflow)

The primary escalation mechanism for Phase D4 (Implement Fix):

```
Attempt 1: Designed fix → tests → pass=done / fail→Attempt 2
Attempt 2: Re-analyze + failure context → revised fix → tests → pass=done / fail→Attempt 3
Attempt 3: Deep re-analysis + all context → new approach → tests → pass=done / fail→ESCALATE
```

### After 3 Failures: Escalation Options

| Option | Description |
|--------|-------------|
| **Senior Architectural Review** | Fresh agent with `solution-architect.md` prompt reviews everything de novo. If it proposes a fix → Attempt 4. If it needs design changes → escalate to user. |
| **Surface to User** | Present full context: what was tried, what failed, what was learned. User decides next action. |

**Default:** Surface to user with option to request senior review.

---

## Escalation Triggers

### Architectural Review

- Three fix attempts fail
- Root cause analysis has Low confidence
- Fix requires architecture-level changes (not a localized bug fix)
- Multiple related bugs suggest systemic design issue

### User Escalation

- Three fix attempts fail AND senior review doesn't resolve
- Root cause is outside the codebase (infrastructure, third-party, config)
- Fix requires only-user decision (API contract change, breaking change)
- Security impact rated High or Critical
- Cost or time exceeds reasonable bounds

### What the User Receives

1. **Summary:** One-paragraph what happened
2. **Root Cause:** The analysis
3. **Attempts Made:** What was tried + outcome per attempt
4. **Current State:** What the codebase looks like now
5. **Options:** Next steps with recommendations

**User options:** Provide context | Change approach | Fix manually | Abort | Run development workflow

---

## Escalation by Workflow

### Development Workflow

| Trigger | Action |
|---------|--------|
| QA critical/blocker | Loop back to Phase 4 for targeted fixes |
| QA critical persists after fix loop | Surface to user with QA findings |
| Security audit: critical vulnerability | Immediate notification + required fix |
| Implementation task fails | Retry once, then mark blocked and continue |
| Multiple tasks blocked | Surface to user with dependency analysis |

### Debug Workflow

| Trigger | Action |
|---------|--------|
| Root cause confidence Low | Flag for extra scrutiny in fix design |
| Fix attempt fails | Re-analyze with failure context, retry |
| 3 fix attempts fail | Escalate: senior review or surface to user |
| Security impact High/Critical | Expedited handling + mandatory security review |
| Similar bugs found | Escalate from single fix to systematic pattern fix |

---

## Timeout Escalation

### Agent Timeouts

1. Kill the agent, preserve partial output
2. Retry once with same input
3. If retry times out: mark task as timed out
4. Fan-out patterns: other agents continue, timed-out dimension marked incomplete
5. Tiered patterns: dependent tasks marked blocked

### Phase Timeouts

1. Report which agents completed/didn't
2. Preserve partial results in workspace
3. User decides: retry, proceed with partial, or abort

### Cost Escalation

The coordinator monitors token cost. If significantly exceeding expectations:

1. Pause current phase
2. Report cost situation to user
3. Recommend adjustments (reduce `max_parallel_agents`, skip remaining tiers, abort)

**Cost controls:** `max_parallel_agents` (default 5), `audit_depth`, phase skipping.

---

## Security Escalation

### During Development (QA Phase)

| Severity | Action |
|----------|--------|
| Critical | Immediate notification. Required fix before proceeding. Loop back to Phase 4. |
| High | Strongly recommended fix. User decides fix now or defer. |
| Medium | In QA report. User triages at QA gate. |
| Low / Info | Noted in QA report. No escalation. |

### During Debugging

If security impact is High/Critical:
1. Root cause analysis includes security assessment
2. Fix design must include security review
3. Fix verification includes dedicated security verifier
4. User notified at earliest gate (D2: Analyze)
5. Fix is expedited — priority over other workflow concerns

---

## Decision Matrix

| Situation | Development | Debug |
|-----------|------------|-------|
| Single agent failure | Retry once, continue | Retry once, continue |
| Phase-level failure | Re-run phase once | Apply 3-strike rule |
| Persistent failure | Surface to user | Senior review → user |
| Security critical | Immediate loop-back | Expedited fix path |
| Cost overrun | Warn user, offer options | Warn user, offer options |
| Timeout | Preserve partial, retry | Preserve partial, retry |
| Low confidence output | Flag in next phase | Extra scrutiny next phase |
| User rejection at gate | Revise, re-present | Revise, re-present |
