---
name: cfc-start
description: Use when initializing a new project or writing a project from scratch (or near-scratch). Handles the questionnaire phase, including MQTT variable table and parameter range/meaning table templates that the user must fill in. Must end by invoking cfc-test to generate a full test suite.
---

# cfc-start — 从零创建项目

初始化以及从零开始（或接近于从零开始）编写项目。

## 流程

```
cfc-start
  ├─ 1. 需求问卷（含 mqtt 变量表 / 参数范围·意义表模板）
  ├─ 2. 领域建模（CONTEXT/PRD/ADR）
  ├─ 3. TDD 垂直切片实现
  ├─ 4. 【强制】调 cfc-test 生成完整全量测试套件并测试、修复
  └─ 5. 完成（调 cfc-release 发布）
```

**每次 cfc-start 结束后必须调 cfc-test** 生成完整全量测试套件并测试、修复到全绿。

## 前期询问（新增模板）

**问卷阶段**除常规技术/通信/控制/安全/部署问题外，**必须包含**：

### 1. MQTT 变量表模板（要求用户填写）
```
| 变量名(程序内key) | MQTT通信名 | 中文标签 | 单位 | 读取开关 | 监测开关 | 控制开关 |
|------------------|-----------|---------|------|---------|---------|---------|
| temp_inlet       | F_1004    | 入口温度  | °C   | 开      | 开      | 关      |
| frequency        | R_1001_1  | 频率     | Hz   | 开      | 开      | 开      |
| ...              |           |         |      |         |         |         |
```
作用：确定变量表基线（哪些读/测/控开），生成 mqtt_variables.json 默认值。

### 2. 参数范围·意义表模板（要求用户填写）
```
| 序号 | 名称 | 变量名 | 正常范围 | 参数意义 | 状态判定 | 备注 |
|------|------|--------|---------|---------|---------|------|
| 1    | 振动速度X | VX | ＜6.5 mm/s | 振动强度 | 松动/磨损指标 | |
| ...  |           |    |            |          |              | |
```
作用：权威标准源——条款矩阵与 canonical_spec 都由它程序化抽取（cfc-test 用）。

**模板文件**：`../templates/mqtt_variable_table.md` + `../templates/param_meaning_table.md`（复制给用户填写）。

## 关键约束

- 产品画像先行（为谁做/解决什么/运行在哪/如何验证）
- 问卷后产出 findings.md → PRD → CONTEXT
- TDD 每切片 red→green→commit
- 结束必调 cfc-test

## 参考

- 问卷模板：`../templates/questionnaire.md`
- 开发范式：`../SKILL.md` 第三章
