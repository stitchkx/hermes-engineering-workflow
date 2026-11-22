# Hermes Engineering Workflow

A single local skill for investigating, changing, verifying, and handing off software work in Hermes Agent. Start with an observable goal. Work through the smallest relevant playbook. For multi-session work, group recoverable conversations within one Hermes Project or retain their session references in a project index. 本技能可直接接收中文任务。

## 项目介绍与致谢

Hermes Engineering Workflow 是供 Hermes Agent 加载的独立工程技能。它把一项需求从调查带到交付：先写出使用者能观察到的完成条件，再沿实际入口开发和验证，最后把产物、仍待判断的问题和恢复位置交给下一位经办人。它可以从一个本地 CLI 任务开始，也可配合 Hermes Projects、Kanban 和独立 worker 处理跨会话工作。[Hermes Skills 文档](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills)

### 工程方法来源：Lauren Tan（poteto）的 pstack

感谢 Lauren Tan（poteto）在 Cursor 的插件仓库公开 pstack。作者在项目介绍中讲述了在 Meta、Netflix 和 Cursor 的工程经历，以及参与 React Compiler 的工作。本项目借鉴了以下工作方法，并为每项方法选择了 Hermes 中可执行、可读回的交付方式。[作者与 pstack 项目介绍](https://github.com/cursor/plugins/tree/main/pstack) · [上游 MIT 许可证](https://github.com/cursor/plugins/blob/main/pstack/LICENSE)

| 借鉴的方法 | 在这个 Skill 中如何执行 |
|---|---|
| 按目标选择调查、修复、功能或性能剧本 | 修缺陷从可复现的失败开始；性能任务先固定输入和基线。[pstack 入口](https://github.com/cursor/plugins/tree/main/pstack/skills/poteto-mode) · [本包剧本](references/playbooks.md) |
| 在设计阶段厘清接口、状态归属和并行边界 | 多人碰同一份库存余额时，先定写入者和事务边界；可独立验收的任务再并行。[上游设计指南](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/04-design.md) · [Hermes 协作方式](references/coordination.md) |
| 用真实入口证明交付 | 报表与独立预期对账；服务写入后重新读取；面向手机的报告要实际找到并读出关键数字。[上游验证指南](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/06-verify-and-ship.md) · [本包验收方法](references/verification.md) |
| 为长任务约定权限、停止条件和次日交接 | 用 Project 保留会话归属，用 Kanban 记录依赖和结果；遇到需要业务判断的数据时，交回原始值、影响范围和恢复入口。[上游夜间运行指南](https://github.com/cursor/plugins/blob/main/pstack/docs/guide/07-overnight.md) · [本包交接清单](references/delivery.md) |

### 模型接入：Magpie 与 Hermes provider

感谢 Magpie 在本项目最初使用环境中提供多模型接入。这里的 `magpie` 是 Hermes 配置中的供应商键，同一个键下可以出现来自不同模型家族的完整 ID。用户先在自己的 Hermes profile 中配置供应商和凭据；本包提供只读发现脚本及选型规则。安装此 Skill 本身不会开通模型服务。[发现脚本](scripts/discover_models.py) · [路由规则](references/model-routing.md)

- **自动选择**先查 `magpie`，再查已配置的 `magpie-*`。根据任务能力与用户确认的预算选型；没有合适候选时，再查该 profile 的默认及其他供应商。目录中出现模型只证明它已列入配置，价格与可用性要按实际账户核对。
- **明确指定**时保留供应商键和完整模型 ID，包括其中的斜杠。派单前检查执行端的回退设置；无法保证指定路由时，先说明阻塞原因。列出候选的命令是 `python scripts/discover_models.py`，查看其他员工配置可加 `--profile <name>`。
- **独立使用**时也可以只配置其他 Hermes provider。仓库发布的是工作流、模板、发现与交付检查脚本；模型服务、密钥和计费由安装者管理。

例如处理材料台账，可以要求“按工段、专业和单位汇总，坏行不得覆盖上一份有效报告”。执行者生成 HTML 后，复核者从原始 CSV 独立复算一组金额，用坏输入重跑，再在目标设备上打开报告。这样一份交接既能回答数字怎么算，也能回答使用者是否拿到了可读的成果。

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
