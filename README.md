# CFC Workflow — 工业控制系统全流程开发方案

一套 **AI 智能体可严格遵循的通用全流程详细开发方案**，覆盖从项目初期调查问卷到产品打包发布的完整闭环。

> **核心理念**：先想清楚「**开发什么样的项目**」（产品画像），再按 8 阶段严格执行（如何开发）。
> 重写自燃烧风机控制项目（combustion-fan-control）的开发实践，已提炼为不绑定具体项目的通用方案。

---

## 一、这个 skill 解决什么

| 问题 | 解法 |
|------|------|
| 新项目不知从哪开始 | 阶段 0 问卷 → 用领域专家答案填平未知 |
| 开发中跑偏/返工 | 产品画像先行 + 每阶段有明确输入/输出/验证 |
| 文档与代码脱节 | 版本目录归档 + 功能-only 铁律 |
| 发布混乱 | 版本规则 + 发布链每步提交 + 逐项验证 |
| 产物膨胀 | 阶段 7 清理（同一主版本保留最新两个） |

## 二、使用方式

### 场景路由

| 场景 | 入口 |
|------|------|
| **新项目** | 阶段 0 → 1 → 2 → 3 → 4 → 5 → 6 → 7（全流程） |
| **已有项目新增功能** | 阶段 2 → 4 → 5 → 6 → 7（产品画像已建立可跳 0/1） |
| **Bug 修复** | 阶段 3b → 6（修订号发布，跳过文档） |
| **快速参考** | 读 [SKILL.md](SKILL.md) 二章 8 阶段表定位 → 读对应 [prompts/](prompts/) |

### 三句话启动

```bash
# 1. 安装（软链接到用户 skills）
ln -s /d/PythonProjects/ClaudeCodePyProject/cfc-skill ~/.claude/skills/cfc-workflow

# 2. 新项目：先读产品画像模板，再进阶段 0
cat references/PRODUCT_BLUEPRINT.md prompts/phase-0-survey.md

# 3. 每阶段完成 → 更新 task_plan.md/progress.md（planning-with-files-zh 钩子）
```

## 三、目录结构

```
cfc-skill/
├── SKILL.md                    # ★ 总路由：产品画像 + 8 阶段全流程 + 10 条范式 + 外部 skills
├── README.md                   # 本文件（使用说明）
├── prompts/                    # 阶段指导（按场景分门别类，9 份）
│   ├── phase-0-survey.md       #   需求调研问卷（设计/问答/分析）
│   ├── phase-1-orient.md       #   领域建模（CONTEXT/PRD/ADR）
│   ├── phase-2-feat.md         #   TDD 垂直切片实现
│   ├── phase-3-review.md       #   代码审查质量门禁
│   ├── phase-3b-fix.md         #   Bug 修复（复现→根因→回归）
│   ├── phase-4-doc.md          #   文档同步（功能-only 铁律）
│   ├── phase-5-version.md      #   版本管理（次/修订判定）
│   ├── phase-6-release.md      #   发布链（7 步严格顺序）
│   └── phase-7-cleanup.md      #   产物清理（保留最新 N）
├── templates/                  # 文档/代码模板（可套用，10 份）
│   ├── questionnaire.md        #   调查问卷模板
│   ├── findings.md             #   研究发现
│   ├── PRD.md                  #   产品需求文档
│   ├── CONTEXT.md              #   领域术语表
│   ├── handoff.md              #   会话交接
│   ├── spec.md                 #   产品规格书
│   ├── test_manual.md          #   测试手册
│   ├── deploy_manual.md        #   部署手册
│   ├── setup.iss               #   Inno Setup 安装脚本
│   └── config.yaml             #   系统配置
├── scripts/                    # 可执行脚本（直接运行，4 份）
│   ├── gen_questionnaire.py    #   问卷 → PDF + XLSX 审查表
│   ├── build_docs.py           #   md → tex → PDF（pandoc+xelatex 中文）
│   ├── release.py              #   发布链检查（版本/zip/exe 验证）
│   └── clean_artifacts.py      #   产物清理（按主版本保留最新 N）
└── references/                 # 参考资料
    ├── PRODUCT_BLUEPRINT.md          # 原型项目完整产品画像（开发什么样）
    ├── ASK_MATT_INTEGRATION.md       # ask-matt 集成说明
    └── PLANNING_WITH_FILES_ZH.md     # planning-with-files-zh 集成说明
```

## 四、核心设计

### 1. 产品画像先行（第 0 层）
任何开发开始前回答 4 问：
- **为谁做**？→ 目标用户/现场环境
- **解决什么**？→ 核心痛点/能力清单
- **运行在哪**？→ 硬件/OS/网络约束（决定离线/在线策略）
- **如何验证**？→ 验收标准/测试门禁

→ 本项目画像见 [references/PRODUCT_BLUEPRINT.md](references/PRODUCT_BLUEPRINT.md)

### 2. 8 阶段全流程（第 1 层）
```
调研(0) → 建模(1) → 实现(2) → 审查(3) → 文档(4) → 版本(5) → 发布(6) → 清理(7)
```
阶段可跳过（已建立画像），不可乱序。每阶段：目标 → 输入 → 执行 → 输出 → 外部 skill → 模板/脚本。

### 3. 10 条开发范式（第 2 层）
TDD 垂直切片 / 每次修改必提交 / 测试门禁 exit 0 / 不可变性 / 显式错误处理 /
功能-only 文档 / 版本驱动发布 / 离线优先（国内源）/ 中文 UTF-8 无 BOM / 上下文管理

### 4. 主动调用外部 skills
| skill | 用途 |
|-------|------|
| `/ask-matt` 系列（grill-with-docs / grill-me / to-prd / to-issues / implement） | 需求访谈 → PRD → issue → TDD 实现 |
| `/planning-with-files-zh` | 磁盘工作记忆（task_plan/findings/progress 钩子） |
| `/tdd` | 红-绿循环参考 |
| `/code-review` `/security-review` `/grilling` | 质量门禁 |
| `/systematic-debugging` | 复杂 bug 根因排查 |
| `/verification-before-completion` | 发布前逐项验证 |

## 五、从原型项目提炼的通用要义

| 原型实践 | 通用要义 |
|---------|---------|
| 电气工程师 74 题问卷 | 问卷=章节化 + 必要度 + 「对开发的意义」 |
| TDD 每切片 red→green→commit | 垂直切片禁止水平切片 |
| 文档只写功能（bug 不入册） | 手册=用户契约，内部机制不入册 |
| 版本 x.y.z + beta | 次版本=用户可见，修订=内部 |
| 发布链 7 步每步提交 | 版本驱动，产物 gitignore |
| 离线部署 + 国内源 | 离线优先，大依赖在线用国内镜像 |
| 产物清理保留最新两个 | 控制膨胀，定期归档 |

## 六、安装与维护

```bash
# 安装（软链接，改动即时生效）
ln -s /d/PythonProjects/ClaudeCodePyProject/cfc-skill ~/.claude/skills/cfc-workflow

# 验证
ls ~/.claude/skills/cfc-workflow/SKILL.md

# 更新（本仓库 git 管理）
cd /d/PythonProjects/ClaudeCodePyProject/cfc-skill && git pull
```

> 本 skill 目录本身有独立 git 仓库，所有修改按 Conventional Commits 提交。
