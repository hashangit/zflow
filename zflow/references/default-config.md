# Default Configuration Reference

The default `.zflow/config.json` written on first run. Users may edit it between
runs to customize behavior.

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
    },
    "skip_phases": [],
    "max_parallel_agents": 5
  },
  "ui": {
    "pencil_enabled": "auto",
    "design_system": null,
    "component_library": null
  },
  "security": {
    "audit_depth": "full",
    "owasp_categories": "all",
    "dependency_scan": true,
    "secrets_scan": true,
    "security_severity_threshold": "medium"
  },
  "debug": {
    "escalation_threshold": 3,
    "auto_run_tests": true,
    "security_impact_assessment": true,
    "gates": {
      "reproduce": "auto",
      "investigate": "auto",
      "analyze": "human",
      "design_fix": "human",
      "implement_fix": "auto",
      "verify": "auto"
    }
  },
  "karpathy": {
    "simplicity_enforcement": "strict",
    "surgical_changes_enforcement": "strict",
    "require_success_criteria": true
  },
  "preferences": {
    "commit_style": "conventional",
    "test_command": "npm test",
    "lint_command": "npm run lint",
    "language": "typescript"
  }
}
```

## Gate Modes

- **`"human"`**: After the phase completes, present the output artifact to the user and ask for explicit approval before proceeding.
- **`"auto"`**: Validate the artifact and proceed automatically.

## Key Settings

- **`skip_phases`**: Array of phase names to skip (e.g., `["research"]`).
- **`max_parallel_agents`**: Cap for simultaneous agents in fan-out phases. Default 5.
- **`security.audit_depth`**: `"full"` or `"quick"`. Controls OWASP coverage in QA.
- **`debug.escalation_threshold`**: Number of fix attempts before escalating. Default 3.
