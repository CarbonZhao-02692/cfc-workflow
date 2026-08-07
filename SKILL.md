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

## 控制/预测开发经验（2026-08-07 固化）

### 变量表驱动（单表全信息）
- 用 `templates/变量表模板.xlsx`（全中文）让用户一次填完所有变量信息
- **变量名必须与 MQTT 变量名一致**（程序内部直接用变量名做索引，不做入站映射；该原则强制）
- 角色（参考意义）：调节（判定是否需调节）/ 工况（判定系统工况）/ 自动（可自动控制）/ 只读
- 说明列必须写清具体值含义（0=关闭、1=PLC、2=平台）
- 地址可留空；不用于判定的正常范围可留空
- **示例数据列写明可能值及含义，解析读取用户返回表格时忽略示例数据列**（避免把示例当真实配置）
- 抽取脚本 → JSON 驱动表 → 程序表驱动（roles 决定 UI 权限）

### 控制通道（PLC 平台模式，实测确认）
- 温度控制点 = 排气温度（F_1001，规则上限如 250℃）
- 阀位控制：ValveN_Mode=1(平台) + P_1005_N=给定（精确跟随）
- 风机控制：FanN_Mode=2(平台) + Auto=0 + P_1006_N=给定（升降频可靠）
- 风机停机：FanN_Mode=0 + FanN_On=0（Auto=1 仅兜底）
- **Auto=1=自动模式常导致停机**（升频不可靠根因），平台控制必须 Auto=0
- 用户写请求：阀位/温度 → 调节逻辑；风机/其他 → 直写 topic

### 预测-介入架构（按风机实例化）
- 每风机一个完整单元（TemperaturePredictor + Judge + Controller + Learner）
- 平时只监测预测，温度可能超限才介入（开最大→达标→逐步 5° 降回→交回 PLC）
- 学习模型优化介入增速/步长（温度平稳 + 快速降温）
- 前端多档预测弹窗（30/15/10/5 分钟），10s 未点自动介入

### 测试范式
- 新增模块必须 TDD（red→green→commit）
- fake system 注入真实组件（FanControlManager 等）做契约测试

## 更多经验（2026-08-07 v1.6.x 固化）

### S7 直连 PLC（snap7）
- S7-200 SMART 必须 `set_connection_type(3)`（缺此设置读空/失败，rack/slot 不适用）
- V 区 = Area.DB + db=1；手动 socket 协议 param_len=0x10 仍读空 → 必须 ct3
- 手写 S7 PDU 排查极耗时 → 优先用 snap7 库 + ct3

### 图表四者统一（单一配置源）
- 总览/趋势图/简报/PDF 图表共用 `chart_config.py`（TREND_SERIES：field/label/color/unit/axis）
- 1#/2# 相同参数合并同图，**每图 ≤4 条曲线**
- 后端 matplotlib 与前端 Chart.js 都从同一配置取 → 改一处四处对齐

### 统一关机流程（所有入口共用）
- 前端按钮/托盘右键/命令行 Ctrl+C/关窗口(SIGBREAK) → 同一 `system.stop()`
- stop 开头 `announce_shutdown()`（模块级标志 + 实例标志双保险）→ SSE 推 shutdown → 前端关闭态
- SSE 周期 5s→1s（广播 1s 内送达，消除关闭延迟）
- 托盘先广播再 stop（不依赖时序）

### 一键启停（实验确认，勿凭猜测）
- 开机 = Mode=2（平台）；停机 = Mode=0 + On=0（Mode=0 需 On=0 配合）
- 前端按钮逻辑必须对照实验 findings，不臆造

### 兜底机制
- 关键操作加兜底守卫：停机后频率不降 → 强制 Mode2+写0 → 仍失败报警提示检查 PLC 旋钮

### 打包（安装后可直接运行）
- **设置文件必须打包**（mqtt_settings/variables/rules/ui_settings/link_settings/runtime.json）
- 否则安装后无配置无法运行

### 前端教训
- **模板字符串 `${...}` 只能写在 `<script>` 内**，写 HTML 里会原样显示乱码
- 报警"弹出"用 ctypes MessageBox（前台必弹，异步线程），winotify toast 可能被系统静音
- 未处理报警用导航角标（10s 自动刷新）

### 测试范式补充
- 全量测试排除 PG 依赖文件（test_database/test_startup/test_database_ts）避免挂起
- TS 后端查询前 rollback 清 aborted 事务（autocommit=False 下查询抛错会连锁失败）
- 批量 patch 后必须验证无递归/无污染（sed/python 替换易误插）
