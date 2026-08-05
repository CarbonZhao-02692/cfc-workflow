---
name: cfc-test
description: Use when generating a comprehensive full program-product test suite for a project, running the issue-based test-fix loop, or verifying a project against its authoritative spec documents. Also use when starting a new project from scratch (cfc-start) or updating a project (cfc-update) — both must invoke this skill.
---

# cfc-test — 全面测试及优化套件

生成**完整全面的全量程序-产品性测试套件**，不仅测程序错误，还查产品性/功能性（跨层数据一致性、对照权威文档验收、内部一致性防"左右脑互搏"）。

## 核心原则（从 combustion-fan-control 审计套件提炼）

| 原则 | 说明 |
|------|------|
| **条款矩阵** | 权威标准（xls 参数表/规格书/手册）程序化抽取 → 条款 JSON + canonical_spec 同源；期望值只能从权威文档推导，禁止从当前程序输出抓金标 |
| **冲突→用户提问** | 不同文档对同一参数标准不一致 → **不猜测、不裁决，向用户提问**（decisions_log 记裁决，文档再变才重问） |
| **黄金固件** | trace_id 贯穿（MQTT→DB→API→前端→报表）；边界突变注入必须被检测器拦截；幂等去重（唯一索引+并发竞态） |
| **双后端共生** | 同种子数据跑 SQLite+TS 规范化比对；差异注册表版本化（未登记差异→fail open） |
| **存量门禁** | 现有全部测试纳入子进程门禁 + 隔离契约 + **真变异抽查**（注入真实逻辑，非恒真式） |
| **issue 化** | 所有发现的问题/用户提出的问题/改进 → 拆解本地 issue → 逐项修复 |

## 工作流

```
cfc-test
  ├─ 1. 建 issue 目录（.scratch/<project>/issues/）拆解需求
  ├─ 2. 抽取权威条款 → clauses.json + canonical_spec.json（同源）
  ├─ 3. 交叉验证 → 冲突向用户提问（AskUserQuestion）→ decisions_log
  ├─ 4. 构建套件：条款矩阵 / 黄金固件 / 双后端 / 存量门禁
  ├─ 5. audit_runner 一键跑 → 全绿？
  │    ├─ 否 → 问题 issue 化 → 评估影响 → 修复 → 补测试 → 重跑（循环）
  │    └─ 是 → 完成
```

**cfc-update 集成**：每次更新前必须先调 cfc-test issue 化需求 → 评估影响面（哪些测试需新增/修改）→ 制定计划 → 更新与修复 → 针对性测试 → 测试问题再 issue 化 → 循环直到全通过。

## 套件模板（直接复制到项目 tests_audit/）

```
tests_audit/
├── audit_runner.py        # 一键入口（冲突检测→暂停提问→跑测试）
├── clause_matrix/         # 条款矩阵（extract_clauses.py + clauses.json + canonical_spec.json + decisions_log.json）
├── golden_fixture/        # 黄金固件（trace_id 贯穿/边界突变/幂等）
├── dual_backend/          # 双后端共生（分歧探针/差异注册表）
└── legacy_guard/          # 存量门禁（子进程全量/隔离契约/真变异）
```

参考完整实现：`../references/AUDIT_SUITE_REFERENCE.md`（combustion-fan-control 审计套件产物路径与关键代码）。

## 关键实现要点

### 条款抽取（extract_clauses.py）
- 权威表程序化解析（xlrd 读 xls 参数表）→ 10+ 参数条款（clause_id/名称/阈值/单位/关系）
- `＜6.5 mm/s`→lt/6.5/mm/s；`0.08-0.12bar`→range/lo/hi/bar；`＜环境温度+40℃`→ambient_plus/delta
- canonical_spec 与条款**同源**（同一条抽取函数）→ 防两套标准

### 冲突检测（audit_runner.py）
```python
conflicts = detect_conflicts(params, rules)  # xls条款 vs 项目规则
if conflicts:
    ask_user_conflicts(conflicts)  # 写 conflicts_pending.json + exit 2
# 已裁决（decisions_log）跳过；未裁决暂停提问
```

### 黄金固件 trace_id
- DB 加 trace_id 列（双后端建表 + 旧库 ALTER 无损）
- 幂等：唯一索引（SQLite UNIQUE(trace_id)，TS UNIQUE(time, trace_id)）+ 前置查重 + ON CONFLICT DO NOTHING
- 边界突变：canonical_validation opt-in（防误杀真实数据），篡改越界值必须被拦

### 存量门禁
```python
subprocess.run([sys.executable, "-m", "pytest", "tests/", "-q", ...])
# + 随机顺序隔离契约 + 真变异（注入真实 evaluate 逻辑）
```

## 验证（verification-before-completion）

- `python -m tests_audit.audit_runner` → exit 0 全绿
- 存量 + 审计全部通过
- 变异抽查实证：变异阈值 → 真实测试必须失败

## 常见错误

| 错误 | 修复 |
|------|------|
| 期望值从当前程序输出抓金标 | 期望只能来自权威文档推导 |
| 冲突自动裁决（取宽松/平均） | 必须向用户提问，永不静默消解 |
| 变异测试恒真式（只算不算） | 注入真实逻辑，变异后必须失败 |
| 测试间耦合/顺序依赖 | 隔离契约：随机顺序+单测独立 |
| 双后端假等价 | 差异注册表版本化，未登记差异 fail open |
