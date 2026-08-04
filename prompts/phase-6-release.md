# 阶段 6：发布（cfc-release）

> 用途：功能更新与发布。从修改代码到发布新版安装包 + 产品压缩包的完整流程。

## 目标

按严格顺序产出：新版本安装包 exe + 产品压缩包 zip，每步提交、逐项验证。

## 版本编号规则

三级格式 `x.y.z`：

| 级别 | 何时递增 | 示例 |
|------|---------|------|
| 主版本 | 仅用户手动要求 | 1.x.x → 2.x.x |
| 次版本 | **用户可见**功能增减/变化（新按钮/页面/API/控制行为/告警类型） | 1.2.x → 1.3.0 |
| 修订号 | bug 修复/代码优化/文档/配置（用户无感知） | 1.2.3 → 1.2.4 |

**界定**：用户能直接看到/点击/输入/感受到 = 次版本；内部重构/测试/日志 = 修订号。
归零规则：次/主版本变化 → 其后级别归零（1.2.3 → 1.3.0）。

后缀：安装包带 `beta`，代码注释不带；正式版仅用户明确要求时移除。

## 发布链（严格顺序，每步 git commit）

```
步骤 1: 确定版本变化级别（功能增减 / bug 修复 / 代码优化）
步骤 2: bump 版本
        installer/setup.iss: MyAppVersion + MyAppVersionSuffix
        → commit "chore: bump version to X.Y.Zbeta"
步骤 3: 更新 handoff.md / CHANGELOG（变更摘要 + 当前版本）
        → commit "docs: update changelog for vX.Y.Zbeta"
步骤 4: [仅次/主版本] 更新功能文档
        新建 docs/vX.Y.Z/ 目录 → 更新 .md 版本号 → 更新 .tex → xelatex 编译 PDF（2 遍）
        → commit "docs: update manuals for vX.Y.Zbeta"
步骤 5: 编译安装包
        ISCC.exe installer/setup.iss（编译器: C:\Users\<user>\AppData\Local\Programs\Inno Setup 6\ISCC.exe）
        验证输出文件存在且大小合理（新增大文件会体现在体积）
        → commit "chore: build installer vX.Y.Zbeta"（exe 被 gitignore，实际无内容变更）
步骤 6: 重建产品压缩包
        Python zipfile: 从旧 ZIP 提取不变条目 + 替换新版安装包 + 新版 PDF
        → commit "chore: rebuild deploy pack vX.Y.Zbeta"（zip 被 gitignore）
步骤 7: 验证
        - 全量测试 exit 0
        - 安装包大小合理
        - ZIP 完整性（testzip() is None）+ 条目数正确
```

## 文档更新规则

| 变化级别 | 功能类文档（.md/.tex/.pdf） | handoff.md/CHANGELOG |
|---------|---------------------------|---------------------|
| 次/主 | **必须**新建 docs/vX.Y.Z/ 目录 | **必须** |
| 修订 | 不动（文档仅反映功能） | 如有则更新 |

## 文档命名规则

| 位置 | 规则 | 示例 |
|------|------|------|
| 文档目录 | 完整三级版本号 | `docs/v1.2.0beta/` |
| 文档文件名 | 中文名，仅前两级版本号 | `产品规格书_v1.2.pdf` |
| 文档内版本声明 | 仅前两级 | 版本 v1.2 |
| 安装包文件名 | 完整三级 + 后缀 | `FanControl_Setup_v1.2.1beta.exe` |

## 产物清理（阶段 7 联动）

同一主版本号只保留最新两个（安装包 exe / DeployPack zip / 文档目录）。
→ [scripts/clean_artifacts.py](../scripts/clean_artifacts.py)

## 脚本

- [scripts/release.py](../scripts/release.py) — 发布链自动化：版本检查、git 提交链校验、产物验证

## 外部 skills

- `/verification-before-completion` — 发布前逐项验证
- `/planning-with-files-zh` — 进度记录

## 安全提醒

- 外部凭据（MQTT Broker 密码等）在 handoff 文档中**打码**；含密码的配置文件不入外部仓库
