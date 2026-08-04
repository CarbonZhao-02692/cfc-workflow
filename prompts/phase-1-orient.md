# 阶段 1：领域建模

> 用途：让所有后续会话有统一语言与架构基线。新项目进入或新开发者首次进入时执行。

## 目标

产出 CONTEXT.md（领域术语表 + 架构决策），让「开发什么样的项目」落盘。

## 执行

1. 从 findings.md 提炼：
   - **术语表**：设备/硬件/协议/业务概念 → 表格（术语/定义/来源）
   - **已知约束（不变量）**：影响架构决策的硬约束（如「AI 通道已满」「振动仅 RMS 值」）
   - **关键架构决策（ADR）**：为何选此方案（如「MQTT 云上报 vs 直连」「双后端数据库」）
2. 调用 `/to-prd` 生成 PRD.md（需求 + 技术栈 + 验收标准）
3. 调用 `/to-issues` 将 PRD 拆分为独立 issue

## 架构基线（原型项目，供参考）

```
生产 Windows PC
├── run.py            — 入口（argparse + excepthook + webbrowser + 托盘）
├── src/main.py       — 系统主类（10 步初始化编排 + 生命周期）
├── src/plc/          — Modbus TCP ↔ PLC + MQTT 云客户端
├── src/web/          — Flask + Waitress + Chart.js 单文件前端
├── src/control/      — PID + 三级联锁 + 参数规则
├── src/storage/      — SQLite/TimescaleDB 双后端 + 采集调度
├── src/predictor/    — 异常检测（Isolation Forest）
├── src/monitor/      — 振动 + 电流分析
├── src/report/       — 简报 PDF + 运维记录 xlsx + 导出
├── src/utils/        — 运行时长/设置持久化/MQTT 日志
└── src/debug.py      — 崩溃捕获（3 层）
```

## 产出

- [templates/CONTEXT.md](../templates/CONTEXT.md) — 术语表 + 约束 + ADR
- [templates/PRD.md](../templates/PRD.md)

## 外部 skills

`/to-prd`、`/to-issues`、`/domain-modeling`（模糊术语挑战）、`/grill-with-docs`
