# 阶段 0：需求调研（问卷）

> 用途：新项目启动、获取领域专家知识（如电气工程师 Q&A）、评审现有需求时激活。
> 这是整个项目开发的**第一步**，产出决定后续所有阶段的输入质量。

## 目标

用领域专家的回答填平未知项，产出可开发的规格（findings.md → PRD）。

## 输入

- 初步需求/已有材料（PRD 草案、口头需求）
- 领域专家（电气工程师、现场运维）

## 执行步骤

### 1. 技术栈与未知项分析
- 解析已有材料，列出需要确认的未知项
- 按「通信/执行机构/控制逻辑/监测/安全/数据/预测/部署」分类

### 2. 问卷设计
- 按章节组织（每章 5-15 题），参考模板 [templates/questionnaire.md](../templates/questionnaire.md)
- 每题标注：**必要度**（★★★★★ 核心必答 / ★★★☆☆ 可选）+ **对程序开发的意义**（让专家理解为什么问）
- 提前标记可合并问题（避免信息重复）
- 添加「遗漏问题补充」章节（专家反向输入）

### 3. 问答执行
- 有代码仓库 → `/grill-with-docs`（有状态访谈）
- 无代码仓库 → `/grill-me`（无状态访谈）
- 输出 questions.md（供专家填写）+ questions.pdf（reportlab）+ questions_review.xlsx（openpyxl 审查表）

### 4. 答案分析 → findings.md
- 统计：已回答/未回答/需补充数量
- 未回答的用默认值并显式标记（写清「用默认值」）
- 按框架整理（参考 [templates/findings.md](../templates/findings.md)）：
  ```markdown
  ## 一、<主题>
  ### <关键发现>     — 一句话结论 + 证据来源（第 X 题回答）
  ### <技术细节>     — 具体参数值、型号、地址
  ### <约束/已知限制> — 影响架构决策的硬约束
  ```

### 5. 下游交付
- `/to-prd` → PRD.md（需求 + 技术栈 + 验收标准）
- 产出 CONTEXT.md（领域术语表）→ 阶段 1

## 输出

| 产物 | 模板/脚本 |
|------|----------|
| questions.md / questions.pdf | [scripts/gen_questionnaire.py](../scripts/gen_questionnaire.py) |
| questions_review.xlsx | 同上 |
| findings.md | [templates/findings.md](../templates/findings.md) |
| PRD.md | [templates/PRD.md](../templates/PRD.md) |

## 已踩坑（原型项目）

| 问题 | 解法 |
|------|------|
| 专家不理解问题背景 | 每题加「用途（对程序开发的意义）」列 |
| 问题过多导致拒答 | 必要度排序：★★★★★ 必答，★★★☆☆ 可选 |
| 遗漏关键问题 | 保留「遗漏问题补充」Sheet 让专家反向输入 |
| 同名问题重复 | 提前标记「建议合并」并高亮 |
