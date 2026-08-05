---
name: cfc-workflow
description: Use when the user explicitly invokes this skill or asks to develop/maintain/update an industrial control project (PLC host computer, fan control, Modbus TCP, MQTT remote). Routes to the correct sub-skill based on the prompt and writes an implementation plan. Enforces hard skill-invocation requirements.
---

# CFC Workflow — 工业控制系统全流程路由

**主路由 skill**：根据用户 prompt 判定应走的流程，挑选子 skills，编写计划。

## 路由决策

```
用户 prompt
  ├─ 从零创建/初始化项目 → cfc-start（问卷含 mqtt 变量表/参数意义表 → 实现 → 必调 cfc-test）
  ├─ 更新维护（修 bug/新功能/优化）→ cfc-update（先调 cfc-test issue化 → 循环测试修复）
  ├─ 生成全面测试套件 / 验证产品性 → cfc-test
  ├─ 发布/打包 → cfc-release（bump → handoff → cfc-doc → ISCC → DeployPack）
  ├─ 更新文档 → cfc-doc（不写 bug 修复）
  └─ 明确子 skill 名 → 直接调用
```

## 子 skills

| 子 skill | 用途 |
|----------|------|
| **cfc-start** | 初始化 + 从零（或近零）编写项目；问卷含 mqtt 变量表/参数范围意义表模板；结束必调 cfc-test |
| **cfc-update** | 更新维护：修复/新增/优化；先调 cfc-test issue化需求 → 计划 → 实现 → 测试循环 |
| **cfc-test** | 生成完整全面全量程序-产品性测试及优化套件；issue 化循环 |
| **cfc-release** | 完成更新后发布：bump → handoff → 文档(cfc-doc) → git → 打包 → DeployPack |
| **cfc-doc** | 文档更新；铁律：不写 bug 修复 |

## 流程关系

```
cfc-start ──→ cfc-test（强制：生成套件+测试+修复）──→ cfc-release
cfc-update ─→ cfc-test（issue化→循环测试修复）────→ cfc-release
cfc-release ─→ cfc-doc（次/主版本时）
```

## Skill 调用硬性指标（强制）

1. **每次从零创建（cfc-start）结束** → 必须调 cfc-test 生成完整全量测试套件并测试、修复
2. **每次更新（cfc-update）** → 必须先调 cfc-test issue 化用户需求，评估影响（新增/修改哪些测试脚本）→ 制定计划 → 程序更新与修复 → 新增/修改测试 → 针对性测试 → 测出问题再 issue 化 → 循环直到全部通过
3. 全程使用 `/planning-with-files-zh`（task_plan/progress 持久化）
4. 实现用 `/tdd`（RED→GREEN 垂直切片）
5. 复杂任务用 `/dispatching-parallel-agents` 并行
6. 完成后 `/code-review` 两轴审查
7. 发布前 `/verification-before-completion` 逐项验证

## 开发范式（通用要义）

| # | 范式 |
|---|------|
| 1 | TDD 垂直切片（一需求一切片，RED→GREEN→commit） |
| 2 | 每次修改必提交（Conventional Commits） |
| 3 | 测试门禁（全量 pytest exit 0 才算完成） |
| 4 | 不可变性（不修改入参） |
| 5 | 显式错误处理（不静默吞异常） |
| 6 | 功能-only 文档（bug 修复永不入手册） |
| 7 | 版本驱动发布（bump 开始，每步提交） |
| 8 | 离线优先（大依赖在线用国内源） |
| 9 | 中文 UTF-8 无 BOM |
| 10 | issue 化（所有问题/改进拆解本地 issue 逐项修复） |

## 目录结构

```
cfc-skill/
├── SKILL.md              # 本文件（路由）
├── cfc-start/            # 从零创建（含 mqtt 变量表/参数意义表模板）
├── cfc-update/           # 更新维护（issue化循环）
├── cfc-test/             # 全面测试套件（条款矩阵/黄金固件/双后端/存量门禁）
├── cfc-release/          # 发布（bump→handoff→doc→打包）
├── cfc-doc/              # 文档（不写 bug 修复）
├── prompts/              # 阶段详细指导（9 份）
├── templates/            # 文档模板（含新 mqtt 变量表/参数意义表）
├── scripts/              # 可执行脚本
└── references/           # 产品蓝图/审计套件参考/ask-matt 集成/planning 集成
```

## 使用

| 场景 | 入口 |
|------|------|
| 新项目 | cfc-start → cfc-test → cfc-release |
| 更新/修 bug/新功能 | cfc-update（内部循环 cfc-test）→ cfc-release |
| 只测不改 | cfc-test |
| 只发布 | cfc-release |
| 只文档 | cfc-doc |
