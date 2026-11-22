# Coordinate agents and sessions

Use the current session for short work. Start one execution owner and an independent verifier where needed. Add parallel work only where inputs, outputs, and write ownership can be isolated. Follow [model routing](model-routing.md) for each worker.

## Group before opening another conversation

In Hermes Desktop, use `desktop_project` or the Project UI to look up the project by identity and workspace. Reuse it or create one with the actual project directory. Open related desktop conversations there. Read back the target project and session placement after creating or moving a chat. A desktop move can re-anchor the working directory. Preserve the original workspace of running workers and worktrees, and index them by profile, durable session ID or link, task, path, and artifact. If the surface cannot group sessions, store the index in a private directory outside the shared checkout and release artifacts. For a local index inside a Git workspace, verify its path with `git check-ignore -- <path>` and confirm `git ls-files -- <path>` returns no tracked file before writing session metadata. Keep private session links and absolute workspace paths out of shared task briefs and commits. Check that records can be found again.

## Pick one owner for execution state

- Use `delegate_task` for isolated short work in the current process. Pass the actual workspace, version, allowed changes, expected artifact, and check. Keep a clear handoff if the work needs to survive the session.
- Use Hermes Kanban for persistent assignment if available. Check the board, scheduler, profile, and scope before enqueuing. A task with an assignee may be picked up automatically. Give implementation tasks separate worktrees or isolated directories. Create downstream cards with their dependencies already attached and use a stable idempotency key for each logical task when supported. Use `--board <slug>` on every read and write. Verify card, run, result, and linked evidence on that board.
- Use a Claude Code or Codex bridge only when its actual model, permissions, and workdir are known. Assign queue state to either the external runner or native worker for each task. If the bridge owns the claim, check successful claim before executing and read back result writes. Preserve failures and partial artifacts for recovery.

With the `terminal` tool, confirm `hermes kanban create --help` on the installed build before selecting flags. Common examples are `hermes kanban --board <slug> show <task-id>` and `hermes kanban --board <slug> create <title> --assignee <profile> --parent <task-id> --workspace worktree:<repo-path> --idempotency-key <key>`. Omit the parent flag on root tasks. Pass the relevant rules in the brief because a worker may have its own skill directory.

## Handoffs and recovery

Give each owner the task ID, goal, acceptance checks, inputs, revision, workspace, write scope, dependencies, and expected artifact. Ask for the observed result, exact evidence, and remaining blocker. Record relevant session IDs and project links. For long runs, record the time and retry limits, authorization, and a stopping condition. Keep a short log of consequential decisions, evidence, and unresolved items. Before resuming, check completion, active ownership, and existing outputs. Reclaim or retry only after understanding the previous attempt and preserving its useful work.
