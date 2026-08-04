# 阶段 3b：Bug 修复

> 用途：bug 修复（fix）。走 cfc-fix 模式，第三级修订号发布。

## 铁律

**先复现，再诊断根因，最后修。** 症状修复 = 失败。

```
步骤 1: 复现（必须！不盲目修）
        → 找到可稳定触发 bug 的输入或操作
步骤 2: 诊断根因
        → 复杂 bug 调用 /systematic-debugging（四阶段：反馈环→复现最小化→假设→插桩）
步骤 3: 写回归测试（RED）
        → 测试因该 bug 而失败 — 这是永久防护
步骤 4: 修复（GREEN）
        → 最小改动修复根因，不修症状
步骤 5: 全量验证
        → python -m pytest tests/ 全部通过；启动正常
步骤 6: 更新 task_plan.md / progress.md
```

## 文档联动

- bug 修复**不写入手册**（阶段 4 铁律）
- 版本 = 修订号递增（阶段 5）
- 发布走阶段 6（跳过文档更新步骤）

## 诊断技巧（原型项目实证）

| 症状 | 根因模式 |
|------|---------|
| 导出中文文件名报 latin-1 | RFC 6266 filename* 需 UTF-8 编码 |
| 趋势图无数据也需画轴 | time 轴 min/max 固定 |
| 报警误报持续增大 | setpoint 默认回退（数据行无该列）→ 需从调用链传播真实值 |
| 关闭后托盘残留 | os._exit 跳过 finally → 改为自然退出 |
| 导出 .record 后缀 | 前端保存后缀写错（后端已是 xlsx） |

## 外部 skills

`/systematic-debugging`、`/tdd`（回归测试）、`/verification-before-completion`
