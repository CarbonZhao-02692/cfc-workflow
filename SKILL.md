---
name: cfc-workflow
description: 工业控制系统（PLC 上位机类）完整开发工作流 — 从需求问卷到产品打包发布的通用全流程方案。重点回答「开发什么样的项目」：先建立产品画像，再按 8 阶段严格执行。当用户提到助燃风机、CFC、combustion fan、PLC上位机、风机智能控制、Modbus TCP、工业上位机、工控系统开发时触发。
---

# CFC Workflow — 工业控制系统全流程开发方案

本 skill 是一套**通用全流程详细开发方案**：从项目初期调查问卷开始，一直到产品打包发布。
核心转变：先想清楚「**开发什么样的项目**」（产品画像），再谈「如何开发」（流程执行）。

```
┌─────────────────────────────────────────────────────┐
│  第 0 层：产品画像（开发什么样的项目）                  │
│  回答 4 问：为谁做？解决什么？运行在哪？如何验证？      │
│  → references/PRODUCT_BLUEPRINT.md（本项目画像）      │
├─────────────────────────────────────────────────────┤
│  第 1 层：通用全流程（8 阶段，严格按序）               │
│  调研 → 建模 → 实现 → 审查 → 文档 → 版本 → 发布 → 清理 │
│  → prompts/ 每阶段有详细指导                          │
├─────────────────────────────────────────────────────┤
│  第 2 层：可套用资产（模板 + 脚本）                   │
│  templates/ 文档与代码模板  scripts/ 可执行脚本       │
└─────────────────────────────────────────────────────┘
```

## 一、产品画像 — 开发什么样的项目

**任何开发开始前，先完成产品画像。** 本 skill 的原型项目是「助燃风机智能控制系统」——
一台运行在 Windows 上位机的工业 PLC 监控系统。它的产品特征（可直接套用到同类工控项目）：

### 1.1 系统形态
| 特征 | 说明 |
|------|------|
| **运行环境** | 生产现场 Windows PC（可能离线、无外网、无开发工具） |
| **通信** | PLC（Modbus TCP/S7）采集 + MQTT 云上报双通道 |
| **控制** | PID 自动调控（阀门/变频器）+ 三级安全联锁 + 手动控制覆盖 |
| **监测** | 振动/电流/温度趋势分析 + 故障预测（ML 离线推理） |
| **人机界面** | 本地 Web 界面（Flask + Chart.js），无 Node 依赖，单文件 HTML |
| **数据** | 多后端数据库（SQLite 默认 / PostgreSQL / TimescaleDB 时序） |
| **部署** | 离线安装包（Python embeddable + pip 离线 whl + Inno Setup） |

### 1.2 文档体系（产品级）
| 文档 | 用途 | 版本策略 |
|------|------|---------|
| 产品规格书 | 功能规格说明（面向用户） | 按版本目录 `docs/vX.Y.Z/` 归档 |
| 全功能测试手册 | 逐项验收清单 | 同版本目录 |
| 部署手册 | 现场安装与调试步骤 | 同版本目录 |
| handoff.md | 会话交接 + 变更清单 | 每次发布更新 |
| **铁律：文档只写功能，bug 修复与内部机制不入手册** | | |

### 1.3 版本与产物策略
| 项 | 规则 |
|----|------|
| 版本号 | `x.y.z`：主=大版本（用户指定）；次=用户可见功能变化；修订=bug/优化（用户无感知） |
| 后缀 | 安装包带 `beta`，代码注释不带 |
| 安装包 | `FanControl_Setup_vX.Y.Zbeta.exe`（Inno Setup 编译） |
| 产品包 | `FanControl_vX.Y.Z_DeployPack.zip`（安装包 + 各版本 PDF） |
| 清理 | 同一主版本号下只保留最新两个产物（包 + 文档 + exe） |

### 1.4 完整产品画像
→ [references/PRODUCT_BLUEPRINT.md](references/PRODUCT_BLUEPRINT.md)（架构、功能清单、数据流、部署拓扑）

## 二、通用全流程 — 8 阶段详细开发方案

> 每个阶段都有：目标 → 输入 → 执行 → 输出 → 调用的外部 skill → 可套用模板/脚本。
> 详细指导见 [prompts/](prompts/) 对应文件。

### 阶段 0：需求调研（问卷）
- **目标**：用领域专家的回答填平未知，产出可开发的规格
- **执行**：设计问卷（分章节 + 每题标注必要度 ★★★★★ + 「对程序开发的意义」）→ 专家 Q&A → 分析统计 → findings.md
- **外部 skill**：`/grill-with-docs`（有仓库）或 `/grill-me`（无仓库）→ `/to-prd` → `/to-issues`
- **模板/脚本**：[templates/questionnaire.md](templates/questionnaire.md)、[scripts/gen_questionnaire.py](scripts/gen_questionnaire.py)

### 阶段 1：领域建模
- **目标**：术语表 + 架构决策落盘（CONTEXT.md），让后续所有会话有统一语言
- **执行**：从 findings 提炼术语表、已知约束（不变量）、关键架构决策（ADR）
- **产出**：CONTEXT.md + PRD.md（`/to-prd` 生成）

### 阶段 2：TDD 垂直切片实现
- **目标**：每个需求一个「红色测试 → 最小实现 → 提交」循环
- **执行**：
  1. 把需求拆为垂直切片（每个切片：一个用户可见行为）
  2. 每切片：写失败测试（RED）→ 最小实现（GREEN）→ 提交
  3. 全量回归 + JS/语法校验
- **外部 skill**：`/tdd`、`/task-planning`、`/task-runner`、`/implement`、`/planning-with-files-zh`
- **模板**：[templates/task_plan.md](templates/task_plan.md)、[templates/progress.md](templates/progress.md)

### 阶段 3：代码审查
- **目标**：质量门禁（可读性/不可变性/错误处理/安全/测试覆盖 ≥80%）
- **外部 skill**：`/code-review`、`/security-review`、`/grilling`（魔鬼代言人）

### 阶段 4：文档同步
- **目标**：功能变化 → 更新规格书/测试手册/部署手册，按版本目录归档并编译 PDF
- **铁律**：bug 修复与代码机制完善**不写入手册**；只改最新文档，不动历史文档
- **脚本**：[scripts/build_docs.py](scripts/build_docs.py)（md→tex→pdf，pandoc+xelatex 两遍）

### 阶段 5：版本管理
- **目标**：按变化级别计算新版本号并落地
- **执行**：次版本递增（用户可见功能）→ 修订号递增（bug/优化）→ 主版本用户指定
- **产出**：`installer/setup.iss` 版本号 + 提交 `chore: bump version to X.Y.Z`

### 阶段 6：发布
- **目标**：编译安装包 + 重建产品压缩包 + 逐项验证
- **执行**（严格顺序，每步提交）：
  1. bump 版本 → `chore: bump version to X.Y.Zbeta`
  2. handoff/CHANGELOG → `docs: update changelog for vX.Y.Zbeta`
  3. [仅次/主版本] 文档更新 + PDF → `docs: update manuals for vX.Y.Zbeta`
  4. ISCC 编译安装包 → `chore: build installer vX.Y.Zbeta`
  5. 重建 DeployPack（从旧 zip 提取不变条目 + 替换新 exe/PDF）→ `chore: rebuild deploy pack vX.Y.Zbeta`
  6. 验证：全量测试 exit 0、exe 大小合理、zip 完整性 OK
- **脚本**：[scripts/release.py](scripts/release.py)

### 阶段 7：产物清理
- **目标**：同一主版本号只保留最新两个（包 + 文档目录 + exe）
- **脚本**：[scripts/clean_artifacts.py](scripts/clean_artifacts.py)

## 三、开发范式（通用要义）

这些是不与具体项目绑定的**铁律**，任何阶段都适用：

| # | 范式 | 要求 |
|---|------|------|
| 1 | **TDD 垂直切片** | 一需求一切片，先 RED 后 GREEN，每片独立提交；禁止水平切片（先写完全部测试再实现） |
| 2 | **每次修改必提交** | Conventional Commits（feat/fix/refactor/docs/test/chore/perf/ci），不累积到流程末尾 |
| 3 | **测试门禁** | 全量 pytest exit 0 才算完成；新增功能必须带测试 |
| 4 | **不可变性** | 不修改入参，返回新对象；`update` 不 `modify` |
| 5 | **显式错误处理** | 每层显式处理，不静默吞异常；崩溃捕获（dump_crash）三层兜底 |
| 6 | **功能-only 文档** | 手册只写用户可见功能；bug 修复与内部机制永不入手册 |
| 7 | **版本驱动发布** | 一切发布从 bump 开始，每步提交，产物不入 git（gitignore） |
| 8 | **离线优先** | 部署依赖离线化（embeddable + whl）；大依赖在线下载时用国内源 |
| 9 | **中文 UTF-8** | 所有中文文件纯 UTF-8 无 BOM，写后抽查无乱码 |
| 10 | **上下文字节管理** | 结构化搜索（Grep）先于全量读取；规划文件（task_plan/findings/progress）持久化 |

## 四、外部 skills 调用表

本 skill 主动调用以下外部 skills（按阶段）：

| 外部 skill | 调用阶段 | 用途 |
|-----------|---------|------|
| `/ask-matt` | 顶层路由 | 用户请求 → 路由到本 skill |
| `/grill-with-docs` / `/grill-me` | 阶段 0 | 结构化需求访谈（有无仓库两种） |
| `/to-prd` | 阶段 1 | 从访谈生成 PRD |
| `/to-issues` | 阶段 1 | PRD 拆分为独立 issue |
| `/task-planning` / `/task-runner` | 阶段 2 | 任务规划与执行 |
| `/implement` | 阶段 2 | 驱动 TDD 实现 |
| `/tdd` | 阶段 2 | 红色-绿色循环参考 |
| `/code-review` / `/security-review` | 阶段 3 | 质量门禁 |
| `/grilling` | 阶段 3 | 魔鬼代言人审查 |
| `/planning-with-files-zh` | 全程 | 磁盘工作记忆（task_plan/findings/progress 钩子） |
| `/systematic-debugging` | 全程 | 复杂 bug 根因排查 |
| `/verification-before-completion` | 阶段 6 | 发布前验证 |

## 五、目录结构

```
cfc-skill/
├── SKILL.md              ← 本文件（总路由：产品画像 + 全流程 + 范式）
├── prompts/              ← 8 阶段详细指导（每阶段一份）
│   ├── phase-0-survey.md
│   ├── phase-1-orient.md
│   ├── phase-2-feat.md
│   ├── phase-3-fix.md
│   ├── phase-4-review.md
│   ├── phase-5-doc.md
│   ├── phase-6-release.md
│   └── phase-7-cleanup.md
├── templates/            ← 文档与代码模板（可套用）
│   ├── questionnaire.md   # 调查问卷模板
│   ├── findings.md        # 研究发现
│   ├── PRD.md             # 产品需求文档
│   ├── CONTEXT.md         # 领域术语表
│   ├── task_plan.md       # 任务计划
│   ├── progress.md        # 进度日志
│   ├── handoff.md         # 会话交接
│   ├── spec.md            # 产品规格书
│   ├── test_manual.md     # 全功能测试手册
│   ├── deploy_manual.md   # 部署手册
│   ├── setup.iss          # Inno Setup 安装脚本
│   └── config.yaml        # 系统配置
├── scripts/              ← 可执行脚本（直接运行）
│   ├── gen_questionnaire.py  # 问卷 → PDF/XLSX
│   ├── build_docs.py         # md → tex → PDF（pandoc+xelatex）
│   ├── release.py            # 发布链检查/产物验证
│   └── clean_artifacts.py    # 按主版本保留最新 N 清理
└── references/
    ├── PRODUCT_BLUEPRINT.md      # 原型项目完整产品画像
    ├── ASK_MATT_INTEGRATION.md   # ask-matt 集成说明
    └── PLANNING_WITH_FILES_ZH.md # planning-with-files-zh 集成说明
```

## 使用方式

1. **新项目**：从「阶段 0 问卷」开始 → 按 8 阶段推进
2. **已有项目新增功能**：阶段 2 → 4 → 5 → 6 → 7（跳过问卷/建模，若产品画像已建立）
3. **bug 修复**：阶段 2（cfc-fix 模式，第三级修订号）→ 阶段 6（跳过文档）
4. **任何时刻**：先读 [references/PRODUCT_BLUEPRINT.md](references/PRODUCT_BLUEPRINT.md) 确认产品画像，再读对应阶段 prompt
