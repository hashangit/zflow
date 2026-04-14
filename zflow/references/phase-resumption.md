# Phase Resumption Reference

## Resuming a Previous Run

When `/using-zflow` is invoked and `.zflow/` already exists:

1. **Read `.zflow/current-phase.json`** to determine where the previous
   run stopped.

2. **Check status field**:
   - `"completed"` — all phases done, offer to start a new run
   - `"in_progress"` — phase was interrupted, re-invoke that phase
   - `"awaiting_gate"` — human gate was pending, re-present the gate
   - `"initialized"` — workspace was created but no phase started

3. **Verify artifacts**: Check that previous phase outputs still exist
   and are intact.

4. **Resume prompt**:
   ```
   ZFlow workspace found from a previous run.

   **Previous state**: Phase {name} ({status})
   **Started**: {timestamp}

   Would you like to:
     [A] Resume from Phase {name}
     [B] Start fresh (this will archive the existing workspace)
     [C] View status report
   ```

## Archiving

If the user chooses to start fresh, rename `.zflow/` to
`.zflow.archive.<timestamp>/` before creating a new workspace.

## Debug Session Resumption

Debug sessions work the same way. Check `.zflow/debug/session-{timestamp}/`
for the latest completed phase and resume from there. Each phase's output
document is the input for the next, so any phase can be re-run independently.
