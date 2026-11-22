# Verify the change

## Select the real surface

| Surface | Proof |
|---|---|
| CLI | Run the actual command with representative input. Check exit status, output, and files or records written. |
| API | Call the running endpoint. Assert status, relevant fields, and the resulting persisted state. |
| UI | Exercise the changed interaction in the running app. Capture a meaningful assertion, screenshot, or trace. |
| Storage or queue | Read back the exact affected record or task. Check any required repeat, failure, and recovery behavior. |
| Performance | Repeat the same workload and environment before and after. Keep the raw output and relevant variation. |

Locate the repository, workspace, and revision before running checks. Use the `terminal` tool's `workdir` or an absolute path. Follow repository setup instructions and reuse existing commands. Compare failures with the baseline by case and cause. Confirm any results reported by another agent through its artifacts or an independent readback.

Record actual results per criterion. Use `pass` only when the expected behavior was observed. Use `fail` with the observation and reproducible entry point. Use `unverified` with the missing prerequisite and the check already attempted. When user-facing proof needs review, preserve the exact output, log, record ID, or trace in its appropriate workspace.

## Independent review and delivery

Provide an independent reviewer the requirement, exact head or working-tree diff, baseline, and evidence. Ask for reproducible correctness or regression findings tied to the reviewed revision. Apply authorized fixes and recheck affected evidence. If an independent review is required but unavailable, leave it unverified. Check PR state and head after any authorized write. A ready PR can be left at that state until merge is authorized.

## Reuse verification for a project

When the same setup is needed repeatedly, capture the project's stable root, prerequisites, start/health checks, seed inputs, commands or UI steps, assertions, and evidence destinations in a project-local runbook or smoke script. Prove the documented path from a clean workspace, with a known failing case if available.

For a repeatable acceptance record, adapt [evidence.json](../assets/evidence.json) and run the optional `scripts/check_evidence.py` with Python 3.9 or later. It checks record completeness and status consistency. Real behavior still comes from the original commands and observed artifacts.
