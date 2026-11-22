---
name: hermes-engineering-workflow
description: Use when building, debugging, or verifying software changes.
license: MIT
compatibility: Hermes Agent with file and terminal tools. Git, browser, delegation, Projects, and Kanban are optional for their respective workflows.
metadata:
  version: "0.1.0"
---

# Hermes Engineering Workflow

## When to use

Use for a codebase investigation, bug fix, feature, refactor, performance change, migration, or delivery review. The user can invoke `/hermes-engineering-workflow` with the goal and a condition that can be checked. Honor repository rules and the user's requested scope.

## Procedure

1. Establish the goal, allowed scope, behaviors to preserve, and observable completion criteria. Find the normal entry point and trace the affected callers and state before editing. Resolve routine uncertainty with repository evidence or a small reversible experiment. Keep explanation-only work read-only.
2. Select a path in [playbooks](references/playbooks.md) and record its relevant steps. Reproduce a defect before fixing it. Define the data shape and compatibility for a feature. Measure a baseline for performance work. For a complex boundary, test the costly design assumption before committing to it.
3. Choose [model routing](references/model-routing.md) before dispatch. In auto mode, check configured Magpie routes first, then other eligible providers if needed. Honor the user's explicit provider and full model ID. Deliver the smallest independently verifiable change first. Keep one owner for a coupled change. Split concurrent work only after the interface, shared state, and workspace ownership are clear. For multiple agents or conversations, follow [coordination](references/coordination.md) before starting them.
4. Follow [verification](references/verification.md) against the actual artifact. Record expected and actual behavior, the command or direct observation, and the version or workspace. For consequential changes, ask an independent agent to review the exact revision and capture its verdict. A skipped or inconclusive check stays unverified.
5. Close work against evidence. Read back state after any writeback. Distinguish implementation complete, PR ready, and merged. Push, publish, or merge only within the user's scope. If blocked, report the exact unmet criterion and keep completed evidence. If the same premise leads to repeated failure, test it directly. When an error recurs, use a reusable check or regression test and demonstrate that it catches the known failure.

## Pitfalls

- A successful process exit, installed integration, or done card proves only that specific event. Verify the requested outcome at its real entry point.
- Session paths, terminal execution directories, and worker worktrees can differ. Pass an explicit `workdir` or absolute path and verify the target before changing it.
- A restart or retry can duplicate work. Read the exact board and task, ownership, and existing artifacts before reassigning it.

## Verification

Every acceptance criterion has a result or a concrete reason it remains unverified. Important changes have a recorded independent review status. For project work, task, session, and artifact references are recoverable from the Project or its index. Use [maintenance](references/maintenance.md) to evaluate changes to this skill.
