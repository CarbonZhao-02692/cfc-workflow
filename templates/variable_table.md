# <项目名> — 变量表模板（点表 + 意义表融合，单表全信息）

> 一份表填完所有变量信息：协议地址、读写、单位、注释、正常范围、报警设定、roles、系统映射。
> 程序开发时由脚本（如 extract_variables_from_xls.py）抽取为 JSON 驱动表（表驱动架构）。

## 填写说明
- **必填**：key / signal / addr / dtype / rw
- **roles**：control（平台给定，可写控制）/ trend（趋势监测）/ danger（高危，需人工确认）/ read（只读参考）
  - 一个变量可多 role，如平台给定频率 = control + trend
- **系统名 system_name**：程序内部索引（与 MQTT 名对齐时可为空，脚本自动回退 key）
- **正常范围**（value1/value2 + mode）：趋势报警依据（lt=小于/gt=大于/range=区间）
- **报警设定/启用**：如 F_1001_1（高报警值）等，标注关联

## 模板（Sheet「变量表」）

| key | signal(中文名) | addr | dtype | rw | unit | comment | system_name | roles | 正常范围mode | value1 | value2 | 报警关联 |
|-----|--------------|------|-------|----|------|---------|-------------|-------|------------|--------|--------|---------|
| SysRset | 故障复位 | V1.0 | BOOL | R/W | | 系统复位 | sys_reset | danger | | | | |
| F_1001 | 排气温度 | VD1000 | REAL | R | ℃ | 风机出口介质温度（控制点） | | trend | lt | 250 | | F_1001_1/F_1001_2 |
| F_1001_1 | 排气温度高报警设定 | VD20 | REAL | R/W | ℃ | 高报警阈值 | | read | | | | 关联 F_1001 |
| P_1005_1 | 1#平台给定开度 | VD1232 | REAL | R/W | % | 平台控制阀位（实验确认：Valve1_Mode=1 平台有效） | valve_setpoint_1 | control,trend | range | 0 | 100 | |
| P_1006_1 | 1#平台给定频率 | VD1240 | REAL | R/W | Hz | 平台给定频率（实验确认：Fan1_Mode=2+Auto=0 有效） | freq_setpoint_1 | control,trend | range | 0 | 50 | |
| Fan1_Mode | 1#风机控制模式 | VB100 | BYTE | R/W | | 0=按钮 1=PLC 2=平台（实验确认 2 开机） | fan1_mode | read | | | | |
| Valve1_Mode | 1#调节阀控制模式 | V104.2 | BOOL | R/W | | 0=PLC 1=平台 | valve1_mode | read | | | | |
| R_1001_1 | 1#频率反馈 | VD1032 | REAL | R | Hz | 变频器实际频率 | | trend | range | 0 | 50 | |
| ... | | | | | | | | | | | | |

## 模板（Sheet「报警设定」）— 可选，若报警设定独立成表

| key | signal | addr | dtype | rw | unit | 关联变量 | 报警启用key | 报警状态key |
|-----|--------|------|-------|----|------|---------|-----------|-----------|
| F_1001_1 | 排气温度高报警设定 | VD20 | REAL | R/W | ℃ | F_1001 | B_1001_0 | B_1001_3 |
| ... | | | | | | | | |

## 程序开发对照
- 抽取脚本输出 JSON（key/signal/addr/dtype/rw/unit/comment/system_name/roles + rules 正常范围）
- roles 决定 UI 权限（control 可写、danger 需确认、trend 上趋势图）
- system_name 与 MQTT 名对齐时，程序内部直接用 key 索引（无需入站映射）
- 实验确认的控制通道（Mode 语义等）应写入 comment 列，避免重复实验
