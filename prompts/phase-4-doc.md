# 阶段 4：文档同步

> 用途：功能变化 → 更新产品文档并编译 PDF，按版本目录归档。

## 铁律

1. **文档只写功能**：bug 修复和代码机制完善**永不**写入任何手册
2. **只改最新文档**：不改动历史文档目录
3. 版本目录可保留（如 14 章规格书），但其中的 bug 修复内容必须清除

## 工具链

```
Markdown (.md)
  └→ scripts/build_docs.py
       ├→ pandoc → LaTeX（ctexart 中文文档类）
       ├→ xelatex 编译 2-3 遍（中文必需 xelatex，pdflatex 不支持）
       └→ PDF (.pdf)
```

## 文档集（每版本目录 docs/vX.Y.Z/）

| 文档 | 内容 | 何时更新 |
|------|------|---------|
| 产品规格书 | 功能规格说明（含「vX.Y 新增功能」章节） | 次/主版本 |
| 全功能测试手册 | 逐项验收清单（含「vX.Y 新增功能测试」章节） | 次/主版本 |
| 部署手册 | 现场安装/调试/数据库后端说明 | 次/主版本 |
| handoff.md | 会话交接 + 变更清单 | 每次发布 |

## 新增功能章节写法

```
## X.Y vX.Y 新增功能
### X.Y.1 <功能名>
<用户可见行为描述>（参数、界面、格式示例）
```

**注意**：复制上一版本目录时，`sed 's/v1.3/v1.4/g'` 会把「v1.3 新增功能」章节标题与内容一起改名——
必须**重写**该章节为本次真实新增功能，不能沿用旧内容。

## 执行

```bash
# 1. 复制上一版本目录
cp -r docs/v1.3.0beta docs/v1.4.0beta

# 2. 全局替换版本号（md/tex/build_docs.py 的 DOC_VERSION/DOC_DATE）
sed -i 's/v1\.3/v1.4/g' docs/v1.4.0beta/*.md docs/v1.4.0beta/*.tex

# 3. 重写「新增功能」章节为真实内容；删残留旧版本 pdf

# 4. 编译 PDF
cd docs/v1.4.0beta && python build_docs.py 产品规格书_v1.4.md 产品规格书
```

## 模板

- [templates/spec.md](../templates/spec.md) — 产品规格书
- [templates/test_manual.md](../templates/test_manual.md) — 测试手册
- [templates/deploy_manual.md](../templates/deploy_manual.md) — 部署手册
