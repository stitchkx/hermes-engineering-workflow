# Hermes Engineering Workflow

A single local skill for investigating, changing, verifying, and handing off software work in Hermes Agent. Start with an observable goal. Work through the smallest relevant playbook. For multi-session work, group recoverable conversations within one Hermes Project or retain their session references in a project index. 本技能可直接接收中文任务。

## Install

Obtain this repository as a Git checkout or download its archive. Keep the complete skill directory named `hermes-engineering-workflow` so the local references, evidence template, and checker remain available. Use `hermes config path` to locate the target profile's configuration. From this checkout, copy the skill into that profile's `skills` directory with Python 3.9 or later:

```text
python scripts/install.py <profile-skills-directory>
hermes skills list --enabled-only
```

Use the same profile for installation and invocation. If the current session has a cached skill catalog, open a fresh session. The installer refuses an existing destination so an existing edition can be reviewed before replacement. This is a user-local package. Hermes with file and terminal tools is enough for the core flow. Optional Projects, Kanban, browser, Git, and delegation support extend it when available.

## Use

```text
/hermes-engineering-workflow 导出重试后会重复写入。先复现，再修复并确认重试不会新增重复记录。
/hermes-engineering-workflow Investigate why the cache survives logout. Keep this read-only.
/hermes-engineering-workflow Coordinate the migration in this project. Verify the first migrated caller before opening independent workstreams.
```

The skill starts at [SKILL.md](SKILL.md). The references define the playbooks, verification, coordination, and skill evaluation. Copy [the evidence template](assets/evidence.json) to your project and optionally check its structure:

```text
python scripts/check_evidence.py path/to/evidence.json
python scripts/check_evidence.py path/to/evidence.json --require-pass
python -m unittest discover -s tests -v
```

The acceptance checker validates the evidence record. The original CLI, API, UI, or store checks establish behavior. `--require-pass` rejects failed or unverified rows. An example record starts unverified.

## Model routing

Say “自动选模型，优先订阅” to check suitable Magpie routes first, then other configured providers when needed. Say “使用 `<provider>` 的 `<full-model-id>`” to pin a task. [Delivery checks](references/delivery.md) cover independent calculation checks, mobile reports, Desktop attachments, and attended or unattended handoffs. [Model routing](references/model-routing.md) covers session, Kanban, and delegation behavior. Run `python scripts/discover_models.py` from this checkout to view configured candidates in precedence order, with `--profile <name>` for another profile. The inventory is read-only and shows provider keys and model IDs.

## Scope and provenance

Profiles and model budgets come from the user's own configuration. The release ships no provider credentials, project session records, long-running processes, or third-party worker configuration. This is an independent Hermes adaptation inspired by Lauren Tan (poteto)'s pstack. See the [pstack guide](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/README.md), the [Agent Skills specification](https://agentskills.io/specification), and the [Hermes Skills docs](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

[MIT license](LICENSE)
