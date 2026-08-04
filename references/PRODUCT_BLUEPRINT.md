# 产品蓝图 — 助燃风机智能控制系统（原型项目画像）

> 本文件回答「开发什么样的项目」。重写 skill 时以此为本项目画像基准，
> 提炼出的通用全流程见 SKILL.md。

## 1. 产品定位

运行在**生产现场 Windows 上位机**的智能控制系统，通过 Modbus TCP 与 Siemens S7-200 SMART PLC 通信，实现助燃风机（鼓风机）的：

| 能力 | 说明 |
|------|------|
| 实时数据采集 | 温度、压力、流量、振动（X/Y/Z/轴承温度）、电流、频率、阀门开度、故障码 |
| 自动温度调控 | PID 控制新风阀门，维持入口温度目标值（120°C ±2%） |
| 设备监测 | 振动趋势（ISO 阈值）、电流负载分析 |
| 故障预测 | 轴承/叶轮不平衡/管道积灰/过滤器堵塞（Isolation Forest） |
| 安全联锁 | 三级（就地/PLC/智能体），报警即切控制 |
| 云上报 | MQTT 双向：传感器上行 + 控制指令下行 |

## 2. 技术栈

| 层 | 技术 |
|----|------|
| 运行 | Python 3.12 embeddable（免安装，离线部署） |
| PLC 通信 | pymodbus（Modbus TCP） |
| 云通信 | paho-mqtt（读 topic 上行 / 写 topic 下行 / 状态 topic） |
| Web | Flask + Waitress（生产 WSGI）+ Chart.js v4（单文件 HTML + SSE 实时） |
| 存储 | SQLite（默认）/ PostgreSQL / TimescaleDB（时序+压缩+保留策略） |
| 调度 | APScheduler（采集 30s / 简报 2h） |
| ML | scikit-learn Isolation Forest（离线训练+推理） |
| 报表 | reportlab（简报 PDF）+ matplotlib（趋势图）+ openpyxl（运维 xlsx） |

## 3. 系统架构

```
生产 Windows PC
├── run.py            — 入口（argparse + excepthook + 浏览器 + 托盘 + 60s 无连接自终止）
├── src/main.py       — FanControlSystem（10 步初始化 + 生命周期 + 会话计数）
├── src/plc/          — Modbus TCP 驱动 + MQTTFanClient（映射/过滤/重连）
├── src/web/          — standalone_app（Flask 单文件前端 + SSE + 全部 API）
├── src/control/      — PID（自整定）/ Interlock（三级）/ parameter_rules / manual
├── src/storage/      — Database（双后端）/ DataCollector / space_monitor
├── src/monitor/      — VibrationMonitor / CurrentMonitor
├── src/predictor/    — features / anomaly（Isolation Forest）/ models
├── src/report/       — briefing（PDF 简报）/ record_excel（运维表）/ labels / export
├── src/utils/        — runtime_tracker / ui_settings / mqtt_variables / mqtt_log
├── src/debug.py      — 3 层崩溃捕获（安装/启动/运行）
└── src/tray.py       — 系统托盘（双击开前端/右键菜单）
```

## 4. 关键数据流

```
PLC → Modbus TCP → 采集器 → SQLite/TimescaleDB → 前端 SSE（0.5s 心跳）
PLC → MQTT 读topic → 内存快照（_latest_mqtt_data）→ 变量表自动收录 → 规则监测
控制：PID 计算 → 联锁检查 → 控制过滤（MQTT 变量表开关）→ MQTT 写topic → PLC
简报：每 2h → PDF（KPI/6 趋势图/报警表/时间线）→ reports/
```

## 5. Web 界面（10 页）

| 页 | 内容 |
|----|------|
| 实时总览 | 卡片 + 运行时长 + 系统统计卡（计数/磁盘/日期范围） |
| 趋势图 | 6 张（温度/振动/电流-频率双轴/阀门/风压风量双轴/油液），固定 2h 窗口，30s 刷新 |
| 故障预测 | 健康评分 + 4 模式概率 + 评分明细 + 建议 |
| 报警记录 | 最近 50 条 |
| 系统配置 | PID/自整定/测试模式 6 开关/手动控制/参数范围规则 |
| 数据导出 | 时间段选择 + CSV/XLSX/PDF 简报/批量运维表/打包 ZIP |
| 运行简报 | 列表 + 查看（开 PDF）+ 下载 + 运维表 |
| MQTT 设置 | Broker/Topic + 变量表（读取/监测/控制开关 + 自动收录） |
| 实时消息 | MQTT 收/发原始字符串，每秒刷新 |

## 6. 文档与发布特征

| 项 | 特征 |
|----|------|
| 文档 | 3 本手册（规格书/测试手册/部署手册）× 版本目录 docs/vX.Y.Z/，md→tex→pdf |
| 铁律 | 文档只写功能；bug 修复与机制永不入手册 |
| 版本 | x.y.z + beta 后缀；次版本=用户可见功能；修订=内部 |
| 安装包 | Inno Setup：Python embeddable + 离线 whl + 项目代码（~97MB） |
| 数据库安装 | SQLite 零依赖；PG 在线（阿里云 PostGIS 源 100MB + EDB 兜底）；TimescaleDB 离线扩展 |
| 产物清理 | 同一主版本号保留最新两个（exe/zip/docs） |

## 7. 开发范式（本项目实证，已提炼到 SKILL.md 三章）

TDD 垂直切片 / 每次修改必提交（Conventional Commits）/ 测试门禁 exit 0 /
不可变性 / 显式错误处理 / 功能-only 文档 / 版本驱动发布 / 离线优先 / 中文 UTF-8 无 BOM
