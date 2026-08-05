---
name: cfc-update
description: Use when updating or maintaining an existing project — fixing bugs, adding new features, or optimizing functionality. Must first invoke cfc-test to issue-ize requirements, then plan, implement, test, and loop until green.
---

# cfc-update — 更新维护程序

修复问题、新增或优化功能。**每次更新必须先调 cfc-test issue 化需求**。

## 工作流（强制循环）

```
cfc-update
  ├─ 1. 调 cfc-test：issue 化用户需求（拆解本地 issue）
  │       评估影响哪些方面（新增/修改哪些测试脚本）
  ├─ 2. 制定更新或修复计划（task_plan.md）
  ├─ 3. 程序更新与修复（TDD 垂直切片）
  ├─ 4. 新增/修改测试脚本
  ├─ 5. 针对性测试 → 测出问题
  │       ├─ 问题 → issue 化 → 评估 → 修复 → 补测试 → 重跑（循环）
  │       └─ 全通过 → 完成
```

**核心**：测试驱动的更新循环——每轮针对性测试发现的问题都 issue 化，评估影响，修复，补测试，直到全部通过。这是 cfc-test 流程的一部分。

## 更新类型与版本

| 类型 | 版本级别 | 文档 |
|------|---------|------|
| bug 修复/内部优化 | 修订号 | 不更新手册（只更新 handoff） |
| 用户可见新功能 | 次版本 | 更新手册（调 cfc-doc） |
| 用户指定 | 主版本 | 更新手册 |

## 修复原则

- **先复现再修**（diagnosing-bugs：反馈环→复现最小化→假设→插桩）
- 回归测试先行（RED→GREEN）
- 不修症状修根因
- 每项修复独立 commit（Conventional Commits）

## 完成后

- 调 cfc-release 发布（bump 版本 → handoff → 文档[cfc-doc] → 打包）
- 更新 progress.md

## 参考

- issue 化模板：`../templates/issue_template.md`
- 测试循环：`../cfc-test/SKILL.md`
- 开发范式：`../SKILL.md` 第三章（TDD 垂直切片/每次修改必提交/不可变性等）
