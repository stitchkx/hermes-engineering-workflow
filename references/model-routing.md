# Route models in Hermes

Choose the model before starting work. Use a task-level choice so a single job does not modify the user's global defaults or the defaults of unrelated workers.

| Mode | Decision |
|---|---|
| Auto (default) | Check eligible routes under the `magpie` provider and configured `magpie-*` variants first. Apply the user's budget and capability requirements within that group. Prefer a confirmed subscription route for routine work when the user has that arrangement. If no eligible Magpie route is available, check the target profile's configured default and then other configured providers. Separate review context alone does not require a different model. |
| Pinned | Preserve the requested provider and full model ID, including any upstream prefix. If either is missing, resolve it from the current provider's configured catalog without guessing across providers. Verify the route before launching. |

For task-based selection, check the worker profile's actual `model.provider` and `model.default`. For a read-only inventory, use `terminal` to run `python <skill-directory>/scripts/discover_models.py` or add `--profile <worker-profile>`. It orders configured entries as `magpie`, `magpie-*`, then the active non-Magpie provider and other configured providers. An empty catalog on a named entry means the configuration did not list model IDs for it. The inventory omits credentials, endpoints, and custom headers.

Use the installed Hermes model picker or the provider's current catalog as availability evidence where needed. Configured candidates do not establish current reachability, price, or vision/tool support. Follow the user's provider, billing, and capability constraints. Once one Magpie route satisfies them, avoid probing or launching other providers just to compare availability. Use the configured Hermes provider key and exact full model ID. Different Magpie entries can use different API modes.

## Apply a task-level selection

- **Current session.** Use the surface's existing model picker or session-scoped override when available. For an isolated CLI run, check `hermes --help` and use `hermes --provider <provider> -m <full-model-id> -z <prompt>` on builds that expose those flags. Add `-s hermes-engineering-workflow` if the task needs this skill. An explicit provider makes the route unambiguous.
- **Kanban.** Prefer `--model <full-model-id> --provider <provider>` at task creation when supported. This avoids the window where an assigned card can dispatch before a pin is applied. For an existing card awaiting dispatch, inspect `hermes kanban set-model --help`, set the override on the explicit board, and read it back. A running worker retains its active route. To use a profile default on a later run, clear a stale task override using the installed CLI's documented syntax.
- **`delegate_task`.** Inspect the actual tool schema. When it inherits its parent model or lacks an override, route the work through a separately configured worker or task-scoped CLI invocation if a different model is required. Writing a model name in the brief does not select it.
- **External runner.** Check its selected provider and model separately. Hermes profile selection does not configure the external process.

Preserve explicit pins on retry. If a pinned route is unavailable, report the specific problem. For auto routing, try an eligible fallback from the next priority group. Obtain a decision when all remaining routes exceed the user's constraints. Record the requested provider key and observed model separately if Hermes normalizes the runtime provider to `custom`. Label configuration-only results accordingly.
