# ZFlow Pipeline Profiles

Source of truth for ZFlow's dynamic pipeline construction. The orchestrator
(`zflow/SKILL.md`) references this file during pipeline planning.

---

## Overview

ZFlow assesses task complexity before starting and selects an appropriate
pipeline profile. Each profile defines which phases run, how deeply they execute,
and how many agents deploy. The user always approves the proposed pipeline
before execution begins.

---

## Complexity Assessment Rubric

Score the task on 5 signals (1-3 points each):

| Signal | Trivial (1) | Standard (2) | Complex (3) |
|--------|-------------|--------------|-------------|
| Affected systems | 1 module | 2-3 modules | 4+ modules or cross-cutting |
| Technical domains | 1 layer (e.g., API only) | 2 layers (e.g., API + DB) | 3+ layers (API + DB + UI) |
| Existing patterns | Identical pattern exists | Similar pattern exists | Novel for this codebase |
| User language | "just", "quick", "fix", "simple" | neutral description | "redesign", "migrate", "new system" |
| Ambiguity | Clear spec, no unknowns | Some unknowns | Highly ambiguous |

**Scoring:**
- Score 4-5 → Trivial → Quick Fix
- Score 6-9 → Standard → Standard profile
- Score 10-15 → Complex → Full or Extended

**Heuristics (override score when applicable):**
- User explicitly says "quick fix" or "just X" → lean toward Quick Fix
- Task involves security, auth, payments, PII → minimum Standard
- Task involves multiple independent systems → minimum Full
- Task is greenfield or security-critical → Extended
- User always has final say and can override

---

## Profile 1: Quick Fix

- **Complexity**: Trivial (score 4-5)
- **Phases**: IMPLEMENT (with embedded design sketch) → QA (reduced) → DOCUMENT
- **Use cases**: single-function fix, config change, copy-paste error, small refactor
- **Agent count**: ~3-4 total
- **Human gates**: design sketch, QA findings, commit
- **What's skipped**: brainstorm, research, design, review, full QA
- **How invariants are maintained**:
  - Design before implementation: mandatory design sketch (problem, files, approach, success criteria, simplicity self-check)
  - Overengineering review: self-check in design sketch
  - QA after implementation: reduced (completeness-checker + code-quality-auditor)

## Profile 2: Standard

- **Complexity**: Standard (score 6-9)
- **Phases**: BRAINSTORM (abbreviated) → DESIGN → REVIEW → IMPLEMENT → QA → DOCUMENT
- **Use cases**: typical feature, 2-3 module change, new endpoint with tests
- **Agent count**: ~10-15 total
- **Human gates**: brainstorm, design, review, QA findings, commit
- **What's skipped**: research (design does lightweight scan instead)
- **What's abbreviated**: brainstorm max 3-4 questions instead of 8-10

## Profile 3: Full

- **Complexity**: Complex (score 10-12)
- **Phases**: BRAINSTORM → RESEARCH → DESIGN → REVIEW → [UI DESIGN] → IMPLEMENT → QA → DOCUMENT
- **Use cases**: cross-cutting feature, multi-system change, new subsystem
- **Agent count**: ~20-30 total
- **Human gates**: brainstorm, design, review, QA findings, commit
- This is the current ZFlow default — all phases at full depth

## Profile 4: Extended

- **Complexity**: Complex + novel/security-critical (score 13-15)
- **Phases**: Full pipeline with deeper research and extended security QA
- **Use cases**: greenfield feature, security-critical changes, major migration
- **Agent count**: ~30+ total
- **What's extended**: deeper research agents, full OWASP audit with dependency scanning, all gates human

---

## Invariants

These MUST hold regardless of pipeline profile:

1. **Design before implementation**: Full phases have dedicated design. Quick Fix embeds a mandatory design sketch. No implementation without documented design intent.
2. **QA after implementation**: Always present. Depth varies.
3. **Overengineering review before implementation**: Standard/Full/Extended use the dedicated critic agent. Quick Fix uses a simplicity self-check in the design sketch.
4. **Human gate at critical decisions**: Minimum: pipeline approval, design/sketch, QA findings, commit.
5. **Document chain coherence**: Missing artifacts handled via pipeline manifest.
6. **Scope always documented**: Even Quick Fix produces minimal scope within the design sketch.

---

## Pipeline Manifest Schema

`.zflow/pipeline-manifest.json` is written during workspace initialization:

```json
{
  "profile": "quick-fix | standard | full | extended",
  "complexity_score": 0,
  "assessed_at": "ISO 8601 timestamp",
  "phases": [
    {
      "name": "string",
      "depth": "full | abbreviated | lightweight | reduced",
      "agents": 0,
      "gate": "human | auto"
    }
  ],
  "skipped_phases": ["string"],
  "artifacts_expected": {
    "scope.md": false,
    "research-report.md": false,
    "solution.md": false,
    "reviewed-solution.md": false,
    "ui-design-report.md": false,
    "impl-report.md": true,
    "qa-report.md": true
  }
}
```

### Quick Fix Example
```json
{
  "profile": "quick-fix",
  "complexity_score": 5,
  "phases": [
    { "name": "implement", "depth": "lightweight", "agents": 1, "gate": "human" },
    { "name": "qa", "depth": "reduced", "agents": 2, "gate": "human" },
    { "name": "document", "depth": "full", "agents": 1, "gate": "human" }
  ],
  "skipped_phases": ["brainstorm", "research", "design", "review"],
  "artifacts_expected": {
    "scope.md": false, "research-report.md": false, "solution.md": false,
    "reviewed-solution.md": false, "ui-design-report.md": false,
    "impl-report.md": true, "qa-report.md": true
  }
}
```

### Standard Example
```json
{
  "profile": "standard",
  "complexity_score": 7,
  "phases": [
    { "name": "brainstorm", "depth": "abbreviated", "agents": 1, "gate": "human" },
    { "name": "design", "depth": "full", "agents": 1, "gate": "human" },
    { "name": "review", "depth": "full", "agents": 5, "gate": "human" },
    { "name": "implement", "depth": "full", "agents": "dynamic", "gate": "auto" },
    { "name": "qa", "depth": "full", "agents": 6, "gate": "human" },
    { "name": "document", "depth": "full", "agents": 1, "gate": "auto" }
  ],
  "skipped_phases": ["research"],
  "artifacts_expected": {
    "scope.md": true, "research-report.md": false, "solution.md": true,
    "reviewed-solution.md": true, "ui-design-report.md": false,
    "impl-report.md": true, "qa-report.md": true
  }
}
```

### Full Example
```json
{
  "profile": "full",
  "complexity_score": 11,
  "phases": [
    { "name": "brainstorm", "depth": "full", "agents": 1, "gate": "human" },
    { "name": "research", "depth": "full", "agents": 6, "gate": "auto" },
    { "name": "design", "depth": "full", "agents": 1, "gate": "human" },
    { "name": "review", "depth": "full", "agents": 5, "gate": "human" },
    { "name": "implement", "depth": "full", "agents": "dynamic", "gate": "auto" },
    { "name": "qa", "depth": "full", "agents": 6, "gate": "human" },
    { "name": "document", "depth": "full", "agents": 1, "gate": "auto" }
  ],
  "skipped_phases": [],
  "artifacts_expected": {
    "scope.md": true, "research-report.md": true, "solution.md": true,
    "reviewed-solution.md": true, "ui-design-report.md": false,
    "impl-report.md": true, "qa-report.md": true
  }
}
```

### Extended Example
```json
{
  "profile": "extended",
  "complexity_score": 13,
  "phases": [
    { "name": "brainstorm", "depth": "full", "agents": 1, "gate": "human" },
    { "name": "research", "depth": "full", "agents": 8, "gate": "human" },
    { "name": "design", "depth": "full", "agents": 1, "gate": "human" },
    { "name": "review", "depth": "full", "agents": 5, "gate": "human" },
    { "name": "implement", "depth": "full", "agents": "dynamic", "gate": "human" },
    { "name": "qa", "depth": "full", "agents": 7, "gate": "human" },
    { "name": "document", "depth": "full", "agents": 1, "gate": "human" }
  ],
  "skipped_phases": [],
  "artifacts_expected": {
    "scope.md": true, "research-report.md": true, "solution.md": true,
    "reviewed-solution.md": true, "ui-design-report.md": false,
    "impl-report.md": true, "qa-report.md": true
  }
}
```

---

## Downstream Adaptation Rules

| Skipped Phase | Downstream Adaptation |
|---------------|----------------------|
| Research | Design agent does lightweight codebase scan. Notes "no research phase". More conservative design. |
| Brainstorm (abbreviated) | Design agent gets raw description + abbreviated scope. |
| Review (Quick Fix) | Implementation proceeds from design sketch. Sketch includes simplicity self-check. |
| Full QA | Reduced QA runs completeness-checker + code-quality-auditor only. Same severity thresholds. |
| Design (Quick Fix) | Design sketch embedded in implement phase — brief but mandatory. |

---

## Profile Selection Flow

```
User invokes /using-zflow
        |
        v
Orchestrator assesses complexity (5 signals)
        |
        v
Select recommended profile
        |
        v
Present proposal to user with options:
  [A] Accept recommendation
  [B] Upgrade to more rigorous profile
  [C] Downgrade to lighter profile
  [D] Customize specific phases
  [E] Use full pipeline (current ZFlow default)
        |
        v
User approves or overrides
        |
        v
Write pipeline-manifest.json
        |
        v
Initialize workspace (only included phase directories)
        |
        v
Execute pipeline per manifest
```
