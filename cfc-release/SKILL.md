---
name: cfc-release
description: Use when finishing an update or maintenance flow and publishing the product package — bump version, update handoff, optionally invoke cfc-doc, commit to local git, build installer, rebuild deploy pack, verify.
---

# cfc-release — 完成更新后发布产品包

完成更新或维护流程后发布：文档 → 本地 git → 打包。

## 发布链（严格顺序，每步 git commit）

```
步骤 1: 确定版本变化级别（bug修复=修订号 / 用户可见功能=次版本 / 用户指定=主版本）
步骤 2: bump 版本（installer/setup.iss MyAppVersion+Suffix）
        → commit "chore: bump version to X.Y.Zbeta"
步骤 3: 更新 handoff.md / CHANGELOG
        → commit "docs: update changelog for vX.Y.Zbeta"
步骤 4: [仅次/主版本] 调 cfc-doc 更新文档（含"不写 bug 修复"原则）
        → commit "docs: update manuals for vX.Y.Zbeta"
步骤 5: ISCC 编译安装包
        → commit "chore: build installer vX.Y.Zbeta"（exe 被 gitignore）
步骤 6: 重建 DeployPack（提取旧 zip 不变条目 + 替换新 exe/PDF）
        → commit "chore: rebuild deploy pack vX.Y.Zbeta"
步骤 7: 验证：全量测试 exit 0 + exe 大小合理 + zip 完整性 OK
```

## 版本规则

| 级别 | 何时 | 示例 |
|------|------|------|
| 主版本 | 用户手动要求 | 1.x.x → 2.x.x |
| 次版本 | 用户可见功能增减 | 1.2.x → 1.3.0 |
| 修订号 | bug 修复/内部优化 | 1.2.3 → 1.2.4 |

- 安装包带 `beta` 后缀；代码注释不带
- 文档目录 `docs/vX.Y.Z/` 完整三级版本号；文件名中文 + 前两级版本号

## 产物清理

同一主版本号只保留最新两个（exe/zip/docs）：
`python scripts/clean_artifacts.py --dir products --keep 2 --pattern "FanControl_v*.zip"`

## 参考

- 完整流程：`../prompts/phase-6-release.md`
- 脚本：`../scripts/release.py`（版本检查/zip 验证）、`../scripts/clean_artifacts.py`
