# 阶段 2：TDD 垂直切片实现

> 用途：新功能开发（feat）。每个需求一个「红色测试 → 最小实现 → 提交」循环。

## 目标

按垂直切片交付用户可见功能，每个切片带测试、独立提交、不返工。

## 铁律

1. **一需求一切片**，每片：写失败测试（RED）→ 最小实现（GREEN）→ 提交
2. **禁止水平切片**：不得先写完所有测试再实现（那是在测试想象的行为）
3. **每个提交可独立运行**：全量测试中途任意 commit 都能通过（除预存在失败）
4. 测试写在**公共接缝**（用户可见行为/API 边界），不测内部实现
5. 需求不清晰 → 先回阶段 0 澄清，不猜测

## 执行步骤（每切片）

```
1. 从需求列表取一个切片（用户可见行为）
2. 写失败测试（AAA: Arrange-Act-Assert，断言来自独立来源不重复实现逻辑）
3. 跑测试确认 RED（必须亲眼看到失败）
4. 最小实现使测试通过（GREEN）
5. 跑该测试文件 + 相关回归
6. 提交: <type>: <描述>（type: feat/fix/refactor/docs/test/chore/perf/ci）
```

## 切片粒度参考

| 切片类型 | 例子 | 测试位置 |
|---------|------|---------|
| 后端 API | 导出端点/设置开关/查询 | tests/test_<模块>_api.py |
| 纯逻辑 | 时间格式化/规则校验/统计 | tests/test_<模块>.py |
| 前端交互 | 按钮/弹窗/图表（JS 语法用 node 校验） | —（新 Function 校验） |

## 全量验证

```bash
# 全量测试（排除预存在失败文件）
python -c "import sys; sys.exit(__import__('pytest').main(['tests/','-q','--no-header','--ignore=tests/test_startup.py','--ignore=tests/test_database.py']))"

# JS 语法校验（单文件 HTML 内联 script）
node -e "const fs=require('fs');const m=fs.readFileSync('src/web/templates/x.html','utf8').match(/<script>([\s\S]*?)<\/script>/);new Function(m[1])"
```

## 外部 skills

- `/tdd` — 红色-绿色循环参考
- `/task-planning` `/task-runner` — 多切片任务规划执行
- `/implement` — ask-matt 驱动实现
- `/planning-with-files-zh` — 规划文件持久化

## 模板

- [templates/task_plan.md](../templates/task_plan.md) — 切片清单/状态/技术决策/错误记录
- [templates/progress.md](../templates/progress.md) — 会话进度日志

## 常见坑（原型项目实证）

| 坑 | 解法 |
|----|------|
| 测试断言与实现同源（tautological） | 期望值来自独立来源（已知好值/手算示例） |
| 全局状态污染（monkeypatch 泄漏） | 每测试独立 setup，用 tmp_path |
| Windows 编码（latin-1/GBK） | 中文文件纯 UTF-8；导出文件名用 RFC 5987 filename* |
| 时间相关测试脆弱 | 用相对当前时间构造，不用固定过期时间戳 |
