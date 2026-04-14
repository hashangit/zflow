# Error Handling Reference

## Phase Failure

If a sub-skill fails or produces invalid output:

1. Report the failure clearly to the user
2. Identify what went wrong (missing sections, validation failure, etc.)
3. Offer options:
   - Retry the phase
   - Skip the phase (with warning about downstream impact)
   - Abort the workflow

## Artifact Missing

If a previous phase's artifact is missing when the next phase needs it:

1. Check if it exists at an unexpected path
2. If found, update paths and proceed
3. If not found, ask user: "Phase {N} output is missing. Re-run Phase {N}
   or abort?"

## Sub-Skill Not Found

If a referenced sub-skill does not exist:

```
Phase sub-skill not found: skills/zflow-{phase}/SKILL.md

This phase has not been implemented yet. You can:
  [A] Skip this phase and proceed to the next
  [B] Abort and implement the missing sub-skill first
```

## Configuration Errors

If `.zflow/config.json` is malformed or missing fields, use defaults
for any missing values and log a warning. Do not abort the workflow
for configuration issues.
