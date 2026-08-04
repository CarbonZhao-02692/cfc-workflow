# Ask Matt 与本 skill 的集成

> **前置条件**: 本 skill (`cfc-workflow`) 需要 ask-matt 作为上层路由器。ask-matt 已安装在 `~/.claude/skills/ask-matt/`。

## 角色关系

```
用户请求
  │
  ▼
/ask-matt          ← 顶层路由器：识别用户意图，路由到正确流程
  │
  ├── main flow: idea → ship
  │     ├── /grill-with-docs  → 需求访谈 → CONTEXT.md + ADR
  │     ├── /to-prd           → PRD.md
  │     ├── /to-issues        → 拆分为独立 issue
  │     └── /implement        → 驱动 TDD 实现
  │           │
  │           ▼
  │     cfc-workflow ← 📍 本 skill（项目级实现）
  │           │
  │           ▼
  │     sub-skills: feat / fix / review / deploy / doc / debug
  │
  ├── on-ramps
  │     ├── /triage → 处理用户提交的原始 issue
  │     └── /diagnosing-bugs → 复杂 Bug 调试
  │
  └── codebase health
        └── /improve-codebase-architecture → 架构改进
```

## 本项目在使用 ask-matt 过程中产生的文件

| ask-matt 流程 | 产物 |
|-------------|------|
| `/grill-with-docs` | `CONTEXT.md`（领域术语表）、`docs/adr/`（架构决策） |
| 电气工程师 Q&A | `findings.md`（51 题分析结论） |
| `/to-prd` | `PRD.md`（产品需求文档） |
| `/to-issues` | `.scratch/combustion-fan-control/issues/01~10.md` |
| `/implement` | `src/` 全部源码、`tests/` 全部测试 |

## 安装 ask-matt

如 ask-matt 尚未安装，从原仓库获取：

```bash
# 确认安装位置
ls ~/.claude/skills/ask-matt/SKILL.md
```

## 调用示例

```bash
# 方式1: 用户直接调用
/ask-matt 实现一个数据导出功能

# 方式2: 内部路由（自动）
ask-matt 识别到 combustion-fan-control 项目 → 自动加载 cfc-workflow
```

## 关键集成点

1. `/implement` 在进入本项目目录时自动加载 `cfc-workflow` skill
2. 本 skill 的 `cfc-review` 对应 `/implement` 中的「code-review 两轴审查」
3. `cfc-feat` 对应 `/implement` 内部的 TDD 循环
4. 跨 session 工作时：`compact` → 新 session → `session-catchup.py` → 继续
