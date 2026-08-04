# 阶段 7：产物清理

> 用途：控制产物膨胀。同一主版本号下只保留最新两个（产品包 + 文档目录 + 安装包 exe）。

## 规则

| 产物 | 保留规则 |
|------|---------|
| `products/*_DeployPack.zip` | 同一主版本号下最新两个 |
| `docs/vX.Y.Z/` | 同一主版本号下最新两个 |
| `installer/*_Setup_*.exe` | 同一主版本号下最新两个；主版本 0 可只留 0.6.0 |

## 执行

```bash
# 产品包
rm -f products/FanControl_v1.0.0beta_DeployPack.zip ...   # 删除旧版

# 文档目录
rm -rf docs/v0.0.0 docs/v0.1.0 ... docs/v1.2.0beta

# 安装包 exe（installer/ 下）
rm -f installer/FanControl_Setup_v1.0.1beta.exe ...
```

或一键执行 [scripts/clean_artifacts.py](../scripts/clean_artifacts.py)：

```bash
python scripts/clean_artifacts.py --dir products --keep 2 --pattern "FanControl_v*.zip"
python scripts/clean_artifacts.py --dir installer --keep 2 --pattern "FanControl_Setup_v*.exe" --group-major
```

## 注意

- 产物（exe/zip/pdf）通常被 `.gitignore` 忽略，删除后 git 提交可能「nothing to commit」——正常
- 文档目录（.md/.tex/build_docs.py）在 git 中，删除需提交
- 清理后验证：`ls products/`、`ls docs/` 只剩最新两个
