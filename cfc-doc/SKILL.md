---
name: cfc-doc
description: Use when updating project documentation and manuals after a feature change, or generating PDF manuals. Enforces the "no bug fixes in manuals" principle. Also used by cfc-release for the doc step.
---

# cfc-doc — 文档更新

功能变化 → 更新产品文档并编译 PDF，按版本目录归档。

## 铁律

1. **不写 bug 修复**：手册只写用户可见功能；bug 修复与代码机制完善**永不**写入任何手册
2. **只改最新文档**：不改动历史文档目录
3. 版本目录可保留（如规格书 14 章），但其中的 bug 修复内容必须清除

## 文档集（每版本目录 docs/vX.Y.Z/）

| 文档 | 内容 | 何时更新 |
|------|------|---------|
| 产品规格书 | 功能规格（含「vX.Y 新增功能」章节） | 次/主版本 |
| 全功能测试手册 | 验收清单（含「vX.Y 新增功能测试」章节） | 次/主版本 |
| 部署手册 | 安装/调试/数据库后端 | 次/主版本 |
| handoff.md | 会话交接+变更清单 | 每次发布 |

## 新增功能章节写法

```
## X.Y vX.Y 新增功能
### X.Y.1 <功能名>
<用户可见行为描述>（参数/界面/格式示例）
```
**注意**：复制上一版本目录时，sed 替换版本号会把「vX.Y 新增功能」章节内容一并改名——必须**重写**为本次真实新增功能。

## 工具链

```
md → build_docs.py（pandoc → xelatex ×3）→ PDF
```
`python build_docs.py 产品规格书_v1.4.md 产品规格书`

## 参考

- 模板：`../templates/spec.md`、`../templates/test_manual.md`、`../templates/deploy_manual.md`
- 脚本：`../scripts/build_docs.py`
