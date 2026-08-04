# CFC Workflow — 工业控制系统全流程开发方案

一套**通用全流程详细开发方案**：从需求调查问卷到产品打包发布的完整闭环。
核心转变：先想清楚「开发什么样的项目」（产品画像），再按 8 阶段严格执行。

## 结构

```
cfc-skill/
├── SKILL.md              # 总路由：产品画像 + 通用全流程 + 开发范式 + 外部 skills
├── prompts/              # 8 阶段详细指导（按场景分门别类）
│   ├── phase-0-survey.md    # 需求调研问卷
│   ├── phase-1-orient.md    # 领域建模
│   ├── phase-2-feat.md      # TDD 垂直切片实现
│   ├── phase-3-review.md    # 代码审查
│   ├── phase-3b-fix.md      # Bug 修复
│   ├── phase-4-doc.md       # 文档同步
│   ├── phase-5-version.md   # 版本管理
│   ├── phase-6-release.md   # 发布
│   └── phase-7-cleanup.md   # 产物清理
├── templates/            # 文档与代码模板（可套用）
│   ├── questionnaire.md     # 调查问卷
│   ├── findings.md          # 研究发现
│   ├── PRD.md               # 产品需求文档
│   ├── CONTEXT.md           # 领域术语表
│   ├── handoff.md           # 会话交接
│   ├── spec.md              # 产品规格书
│   ├── test_manual.md       # 测试手册
│   ├── deploy_manual.md     # 部署手册
│   ├── setup.iss            # Inno Setup 安装脚本
│   └── config.yaml          # 系统配置
├── scripts/              # 可执行脚本
│   ├── gen_questionnaire.py # 问卷 → PDF/XLSX
│   ├── build_docs.py        # md → tex → PDF
│   ├── release.py           # 发布链检查/验证
│   └── clean_artifacts.py   # 产物清理（保留最新 N）
└── references/
    ├── PRODUCT_BLUEPRINT.md       # 原型项目产品画像
    ├── ASK_MATT_INTEGRATION.md    # ask-matt 集成
    └── PLANNING_WITH_FILES_ZH.md  # planning-with-files-zh 集成
```

## 安装

```bash
# 方式 1: 软链接到用户 skills（推荐，改动即时生效）
ln -s /d/PythonProjects/ClaudeCodePyProject/cfc-skill ~/.claude/skills/cfc-workflow

# 方式 2: 复制
cp -r /d/PythonProjects/ClaudeCodePyProject/cfc-skill ~/.claude/skills/cfc-workflow
```

## 使用

| 场景 | 入口 |
|------|------|
| 新项目 | 阶段 0 问卷 → 按序走完全流程 |
| 已有项目新增功能 | 阶段 2 → 4 → 5 → 6 → 7 |
| bug 修复 | 阶段 3b → 6（修订号，跳过文档） |
| 快速参考 | 读 SKILL.md 二章（8 阶段表）定位阶段 → 读对应 prompts/ |

## 设计原则

1. **产品画像先行**：任何开发前先回答「开发什么样的项目」（4 问：为谁做/解决什么/运行在哪/如何验证）
2. **阶段可跳过，不可乱序**：已建立画像的项目可跳过 0/1，其余顺序不变
3. **模板脚本可套用**：全部内容为可替换 <占位符> 的模板/可执行脚本，而非一次性 prompt
4. **主动调用外部 skills**：ask-matt 系列（grill/to-prd/to-issues/implement）+ planning-with-files-zh + tdd + code-review 等
