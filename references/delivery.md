# Acceptance and handoff

For a short single-owner change, reuse the project's smallest real check. Add the checks below only for affected surfaces. For a consequential invariant spanning workers or stores, settle the unit, state owner, transaction boundary and failure behavior before splitting implementation. Ask a separate reviewer to challenge one concrete assumption.

| Surface | Reusable project check | Evidence for the recipient |
|---|---|---|
| Calculations | Freeze representative input and independent expected values. Include different units, a zero denominator and a rejected final row when relevant. Compare the generated output and check the previous valid artifact after failure. | Input version, discrepancies and reproducible command |
| Stateful work | Follow one record across modules. Try a cumulative over-allocation, compare state before and after rejection, restart and read it again. | Expected and observed values at the real entry point |
| Visual reports | At desktop and intended phone widths, perform a recipient task such as locating an exception or reading an amount. Inspect effective text size, clipped columns and access to offscreen actions. | Viewport, task outcome and screenshot; separate aesthetic judgement |
| Desktop attachments | Run `python <skill-directory>/scripts/attachment.py "<file>"` on the machine hosting the file. Send each output line on its own. For a remote worker, first transfer the file to a location the recipient's Desktop can access. If preview is required, open the actual attachment and inspect the content; verify download separately when required. | Resolved path and which recipient operations were observed |
| Kanban | The coordinating session records the board and task before dispatch. A worker returns the artifact, check and blocker. The authorized owner rechecks the exact card, writes the result once and reads it back. If blocked, retain a pending handoff and retry through the authorized owner on resume. | Board, task, observed status and pending writeback owner |

## Office work with or without a reviewer present

With a reviewer present, show the source row, conflicting values, decision needed and affected outputs. Record the decision and rerun the affected batch. For unattended work agree on the smallest independently publishable batch, allowed writes, time or cost limit, and stop conditions. Continue independent batches when one has a business exception. Keep the last valid version. On return, hand over accepted drafts, held batches with source references, decisions needed, and the safe resume point. Formal sign-off follows the user's authority. A scheduled wake or recovery claim requires a real scheduler and restart check.

When comparing workflows, record the model, input snapshot, task scope, endpoint, human interventions, model calls and elapsed time. Separate application runtime from development time and human wait. Label a scripted approval as simulated and an unavailable bill as unknown.
