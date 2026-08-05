# 审计套件参考实现（combustion-fan-control 实证）

完整可工作的全面测试套件位于 `D:\PythonProjects\ClaudeCodePyProject\combustion-fan-control\tests_audit/`（27 audit + 510 存量全绿，`python -m tests_audit.audit_runner` 一键）。

## 关键文件

| 文件 | 职责 |
|------|------|
| `tests_audit/audit_runner.py` | 一键入口：detect_conflicts → ask_user_conflicts（写 conflicts_pending + exit 2）→ 已裁决跳过 → 跑 pytest |
| `tests_audit/clause_matrix/extract_clauses.py` | xls 参数意义表程序化抽取（_parse_range 解析 lt/range/ambient_plus）→ clauses.json + canonical_spec.json |
| `tests_audit/clause_matrix/decisions_log.json` | 用户裁决记录（param/resolution/date），已裁决冲突不再提问 |
| `tests_audit/dual_backend/divergence_registry.json` | 双后端差异注册表（intended_differences + resolved_differences） |
| `tests_audit/dual_backend/test_dual_parity.py` | 同种子跑 SQLite+TS 规范化比对（MARKER 纳秒级+自清理） |
| `tests_audit/golden_fixture/test_trace_chain.py` | trace_id 贯穿 DB（双后端） |
| `tests_audit/golden_fixture/test_boundary_mutation.py` | 篡改 DB 值 → canonical_validation 拦截 |
| `tests_audit/golden_fixture/test_idempotent_replay.py` | 同 trace_id 两次 → 1 行（唯一索引+并发测试） |
| `tests_audit/legacy_guard/test_legacy_survival.py` | 存量子进程门禁 + 隔离契约 + 真变异抽查 |

## 关键代码模式

### 条款抽取（_parse_range）
```python
def _parse_range(text):
    if text.startswith("＜") or text.startswith("<"):
        body = text[1:].strip()
        m = re.match(r"([\d.]+)\s*([A-Za-z℃°%/³]*)$", body)
        if m: return {"relation": "lt", "threshold": float(m.group(1)), "unit": m.group(2)}
        if "环境温度" in body:
            m2 = re.search(r"\+([\d.]+)", body)
            return {"relation": "ambient_plus", "delta": float(m2.group(1)) or 40.0, "unit": "℃"}
    m = re.match(r"([\d.]+)\s*-\s*([\d.]+)\s*([A-Za-z℃°%/³]*)$", text)
    if m: return {"relation": "range", "lo": float(m.group(1)), "hi": float(m.group(2)), "unit": m.group(3)}
    return {"relation": "unknown", "raw": text}
```

### 冲突检测（xls 条款 vs 项目规则）
```python
def detect_conflicts(params, rules):
    conflicts = []
    rule_by_key = {r["key"]: r for r in rules}
    for var, p in params.items():
        rule = rule_by_key.get(p.get("internal", ""))
        if not rule: continue
        if p.get("relation") == "lt":
            if abs(float(rule.get("value1", 0)) - float(p.get("threshold", 0))) > 1e-9:
                conflicts.append({...})  # 阈值不符
        elif p.get("relation") == "range":
            if abs(float(rule.get("value1", 0)) - float(p.get("lo", 0))) > 1e-9 ...:
                conflicts.append({...})  # 范围不符
        elif p.get("relation") == "ambient_plus":
            conflicts.append({...})  # 相对 vs 绝对 → 必冲突需用户裁决
    return conflicts
```

### trace_id 幂等（Database.insert_sensor_data）
```python
# 前置查重（快速路径）
if trace_id and self._trace_id_exists(trace_id):
    return 0
# 唯一索引兜底：SQLite UNIQUE(trace_id) / TS UNIQUE(time, trace_id)
# SQLite: INSERT OR IGNORE, rowcount==0 → 0
# TS: ON CONFLICT DO NOTHING RETURNING, 无返回 → 0
```

### 真变异抽查（legacy_guard）
```python
def test_mutation_kills_real_rule(tmp_path):
    store = ParameterRuleStore(str(tmp_path / "rules.json"))
    store.set_rule("pressure_inlet", {"mode": "range", "value1": 0.08, "value2": 0.12})
    assert store.evaluate({"pressure_inlet": 0.105}) == []  # 原范围不报警
    store.set_rule("pressure_inlet", {"mode": "range", "value1": 0.11, "value2": 0.12})
    assert store.evaluate({"pressure_inlet": 0.105}) != []  # 变异后必须报警
```

## 实证教训（避免重蹈）

| 坑 | 解法 |
|----|------|
| 探针抓到 TS 字段错位（_SENSOR_KEYS 缺 temp_outlet 致 zip 左移） | 双后端规范化比对即暴露；修复+登记 resolved_differences |
| 秒级 MARKER 碰撞 + 无自清理 → 污染真实库 4874 条假数据 | 纳秒级 MARKER + finally 自清理 |
| get_latest 拦截逻辑倒置（if 非 if not） | 双向正反测试（正常值放行+越界拦截） |
| 变异测试恒真式（只算不算） | 注入真实 evaluate 逻辑 |
| 唯一约束语义分叉（SQLite 全局 vs TS 分区） | 差异注册表登记 unique_trace_scope |
