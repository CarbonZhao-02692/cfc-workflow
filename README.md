# CFC Workflow — 工业控制系统全流程开发方案（AI 智能体 Skill）

一套供 **AI 智能体（Claude Code）严格遵循的通用全流程详细开发方案**：从项目初期调查问卷到产品打包发布的完整闭环，且**每次更新都伴随全面测试套件验证**。

> 从燃烧风机控制项目（combustion-fan-control，含 Modbus TCP PLC 通信、MQTT 远程、PID 控制、双后端数据库、全面审计测试套件）的实践提炼，已剥离为不绑定具体项目的通用方案。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| **产品画像先行** | 先回答「开发什么样的项目」（为谁做/解决什么/运行在哪/如何验证），再谈如何开发 |
| **5 子 skill 分工** | cfc-start / cfc-update / cfc-test / cfc-release / cfc-doc，主 SKILL.md 路由 |
| **测试驱动更新** | 每次更新先 issue 化需求 → 评估影响 → 计划 → 实现 → 测试循环直到全绿 |
| **全面测试套件** | 条款矩阵 + 黄金固件（trace_id 贯穿）+ 双后端共生 + 存量门禁 + 真变异抽查 |
| **交叉验证冲突提问** | 不同文档对同一参数标准不一致 → 不猜测，直接向用户提问裁决 |
| **Skill 调用硬性指标** | 强制调用 tdd / planning-with-files-zh / code-review / verification-before-completion 等 |
| **issue 化原则** | 所有问题/改进拆解本地 issue，逐项修复 |

---

## 🧩 子 skills

### cfc-start — 从零创建项目
初始化 + 从零（或近零）编写项目。
- **前期问卷含 mqtt 变量表 / 参数范围·意义表模板**（要求用户填写，作为权威标准源）
- TDD 垂直切片实现
- **结束必调 cfc-test** 生成完整全量测试套件并测试、修复

### cfc-update — 更新维护程序
修复 bug、新增或优化功能。
- **先调 cfc-test issue 化用户需求** → 评估影响（新增/修改哪些测试脚本）→ 制定计划
- 程序更新与修复 → 新增/修改测试 → 针对性测试 → 测出问题再 issue 化 → **循环直到全部通过**

### cfc-test — 全面测试及优化套件
生成**完整全面的全量程序-产品性测试套件**（不仅测程序错误，还查产品性/功能性）。
- **条款矩阵**：权威文档程序化抽取 → clauses + canonical_spec 同源；期望值只能从文档推导
- **黄金固件**：trace_id 贯穿 + 边界突变检测 + 幂等去重
- **双后端共生**：同种子 SQLite+TS 规范化比对 + 差异注册表
- **存量门禁**：现有测试全量纳入 + 隔离契约 + 真变异抽查
- **冲突→用户提问**：decisions_log 裁决闭环

### cfc-release — 发布产品包
完成更新后发布：bump 版本 → handoff → 文档（cfc-doc）→ 本地 git → ISCC 打包 → DeployPack → 验证。

### cfc-doc — 文档更新
功能变化 → 更新手册并编译 PDF。
- **铁律：不写 bug 修复**（手册只写用户可见功能）

---

## 🔄 流程关系

```
cfc-start ──→ cfc-test（强制：生成套件+测试+修复）──→ cfc-release
cfc-update ─→ cfc-test（issue化→循环测试修复）────→ cfc-release
cfc-release ─→ cfc-doc（次/主版本时）
```

---

## 📦 目录结构

```
cfc-skill/
├── SKILL.md              # 主路由（prompt 判定流程 + skill 调用硬性指标）
├── cfc-start/            # 从零创建（含 mqtt 变量表/参数意义表模板）
├── cfc-update/           # 更新维护（issue化循环）
├── cfc-test/             # 全面测试套件（条款矩阵/黄金固件/双后端/存量门禁）
├── cfc-release/          # 发布（bump→handoff→doc→打包）
├── cfc-doc/              # 文档（不写 bug 修复）
├── prompts/              # 阶段详细指导（9 份：问卷→清理）
├── templates/            # 文档模板（含 mqtt 变量表/参数意义表/issue 模板）
├── scripts/              # 可执行脚本（问卷生成/文档编译/发布检查/清理）
└── references/           # 产品蓝图/审计套件参考/ask-matt 集成/planning 集成
```

---

## 🚀 安装

```bash
# 软链接到用户 skills（改动即时生效）
ln -s /path/to/cfc-skill ~/.claude/skills/cfc-workflow
```

## 🛠 使用

| 场景 | 入口 |
|------|------|
| 新项目 | `cfc-start` → `cfc-test` → `cfc-release` |
| 更新/修 bug/新功能 | `cfc-update`（内部循环 cfc-test）→ `cfc-release` |
| 只测不改 | `cfc-test` |
| 只发布 | `cfc-release` |
| 只文档 | `cfc-doc` |

## 📚 前置依赖 skills

- `/tdd` — RED→GREEN 垂直切片
- `/planning-with-files-zh` — 磁盘工作记忆（task_plan/progress 钩子）
- `/code-review` `/security-review` — 质量门禁
- `/verification-before-completion` — 发布前逐项验证
- `/dispatching-parallel-agents` — 复杂任务并行
- `/systematic-debugging` — 复杂 bug 根因排查

## 📄 参考实现

完整可工作的审计测试套件实证：`references/AUDIT_SUITE_REFERENCE.md`（combustion-fan-control tests_audit/，27 audit + 510 存量全绿，含条款抽取/冲突检测/trace_id 幂等/真变异等关键代码模式）。

---

## 📜 许可

MIT — 自由使用、修改、分发（保留出处）。
