# Maintain and evaluate the skill

- Run the package tests in a clean checkout and verify Hermes discovers the one skill with all referenced files present. Read the exact CLI help for features used on the target build.
- Run one real defect or small feature in a disposable workspace. Capture the pre-change behavior, final artifact, post-change result, and any missed steps. Verify the evidence outside the implementing session.
- For a material skill change, compare a baseline and the revision on the same organic task with the same model, tools, starting repo, and separate workspaces. Keep the scoring rubric from the implementing sessions. Grade from artifacts and permitted tool traces. Include acceptance, regressions, scope, and reproducibility; report what remains inconclusive.
- For a multi-agent claim, run isolated tasks with real workers and a downstream verifier. Check artifact paths, dependencies, result writeback, and recoverable conversation references. Record which checks used the actual gateway and which used the CLI only.
- For recurring errors, choose the smallest durable fix. Prefer a repo constraint or repeatable check when it can enforce a behavior, and demonstrate a known failure. Keep machine paths, chat IDs, credentials, and original-workspace logs out of the public package.
