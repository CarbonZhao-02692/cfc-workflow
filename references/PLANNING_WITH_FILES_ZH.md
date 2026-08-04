# Planning-with-files-zh 与本 skill 的集成

> **前置条件**: 本 skill (`cfc-workflow`) 需要 planning-with-files-zh 提供自动钩子机制。该 skill 已安装在 `~/.claude/skills/planning-with-files-zh/`。

## 钩子机制（自动运行，无需手动触发）

```
UserPromptSubmit 钩子
  └→ 检测 task_plan.md 是否存在 → 提示读取规划文件

PreToolUse 钩子（匹配 Write|Edit|Bash|Read|Glob|Grep）
  └→ 自动输出 task_plan.md 前 30 行到上下文

PostToolUse 钩子（匹配 Write|Edit）
  └→ 提示更新 progress.md + 更新 task_plan.md 状态

Stop 钩子
  └→ 运行 check-complete.ps1 检查所有阶段是否完成
```

## 本项目使用的规划文件

| 文件 | 用途 | 更新频率 |
|------|------|----------|
| `task_plan.md` | 阶段列表、状态、技术决策、错误记录 | 每阶段完成后 |
| `progress.md` | 会话日志、测试结果、创建/修改的文件列表 | 每次 Edit/Write 后 |
| `findings.md` | Q&A 发现、领域知识、硬件约束 | 研究发现后 |

## 本项目使用 planning-with-files-zh 的实际流程

### 初始化

```bash
# 首次进入项目（或 /clear 后）
python "$HOME/.claude/skills/planning-with-files-zh/scripts/session-catchup.py" "$(pwd)"
# → 自动检测上一个会话的未同步上下文
# → 如果有差异: 读取 git diff + 规划文件 → 更新进度
```

### 每个阶段的工作流

```
1. 读 task_plan.md  → 确认当前阶段和 TODO
2. 执行开发工作    → PreToolUse 自动注入 plan header
3. 写/改文件        → PostToolUse 提示更新 progress.md
4. 验证测试         → 写入 progress.md
5. 更新 task_plan.md → 标记阶段完成
```

### 会话恢复

| 步骤 | 操作 |
|------|------|
| 1 | 运行 `session-catchup.py` |
| 2 | 读取 `task_plan.md`、`progress.md`、`findings.md` |
| 3 | 读取 `git diff --stat` 查看代码变更 |
| 4 | 根据恢复报告更新规划文件 |
| 5 | 继续任务 |

## 规划文件模板位置

```
~/.claude/skills/planning-with-files-zh/templates/
├── task_plan.md          # 任务计划模板
├── findings.md           # 研究发现模板
├── progress.md           # 进度日志模板
└── session-recovery.md   # 会话恢复模板
```

## 关键规则

- 不在 `task_plan.md` 中保存网页搜索结果（外部内容仅写入 `findings.md`）
- 每次工具调用前读取 plan 文件刷新注意力
- 错误记录到 `task_plan.md` 「遇到的错误」表
- 同一错误 3 次尝试失败 → 改变策略 → 向用户求助
