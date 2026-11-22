# Choose a playbook

| Intent | Steps | Evidence |
|---|---|---|
| Investigation | Trace the real entry point, relevant configuration and callers. Use read-only probes. Inspect history for questions about a past decision. | Explain observed behavior, point to sources, and label inferences. |
| Bug fix | Reproduce the reported symptom through the matching entry point. Minimize the input, validate the cause with a runtime check, fix the smallest implicated scope. | The same check fails before and passes after. Use a durable regression test when it captures a relevant failure that existing checks miss. |
| Feature | Identify the input and output shape, errors, state ownership, compatibility, and callers. Prove one vertical slice before expanding. | Run new behavior and relevant existing behavior through their normal entry points. |
| Refactor | Establish baseline behavior for affected callers. Migrate in small units and remove the obsolete path when all supported callers have moved. | Run the same fixtures before and after, including supported persisted data. |
| Performance | Pin input, build, environment, and measurement. Repeat enough to see variation. Trace the dominant cost and test one meaningful change per comparison. | Comparable before and after measurements, command, and raw results or trace. |
| Migration | Define compatibility, phases, recovery, and concurrent writers. Prove one complete path before expanding by dependency. | Check old and new data, interruption/retry behavior, and the final state. |

For a design that is expensive to change, identify the contested constraint and compare plausible options using the same small prototype or fixture. Name what would falsify each option. Use separate workspaces for competing implementations. Add independent review when the decision affects a shared interface or persisted state.

For implementation, reuse existing code and tools where they fit. Verify each unit before extending it. If two attempts fail for the same assumed reason, test the shared assumption before another attempt.
