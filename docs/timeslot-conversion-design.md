# TimeSlot 占用转换设计

本文档说明 LowAlt-RouteLab 如何把连续路径转换为 SkyGrid 可识别的离散时空占用序列。

## 背景

路径规划输出的是有序网格路径：

```text
G-01-01 → G-02-01 → G-03-01 → G-04-02
```

SkyGrid 判断冲突时使用的是离散占用单元：

```text
Grid + Level + TimeSlot + Date
```

因此 LowAlt-RouteLab 必须把路径上的每个节点映射到具体时间片。

## 输入参数

| 参数 | 含义 | 示例 |
| --- | --- | --- |
| `path` | 路径网格序列 | `["G-01-01", "G-01-02"]` |
| `level` | 高度层 | `L120` |
| `startTime` | 任务开始时间 | `2026-06-08 10:00:00` |
| `speed` | 飞行速度 | `10.0` |
| `gridSizeMeters` | 单个网格尺寸 | `100` |
| `slotMinutes` | 时间片长度 | `5` |

## 转换规则

1. 第一个路径节点使用 `startTime` 作为到达时刻。
2. 后续节点根据上一段移动距离和速度累加飞行时间。
3. 每个节点的到达时刻向下取整到对应 TimeSlot。
4. `slotEnd = slotStart + slotMinutes`。
5. 对相同 `gridId + levelId + slotStart + slotEnd` 去重。
6. 输出稳定递增的 `sequenceNo`，保留路径顺序。

## 时间片取整

例如 `slotMinutes = 5`：

| 到达时刻 | TimeSlot |
| --- | --- |
| `10:00:00` | `10:00 - 10:05` |
| `10:04:59` | `10:00 - 10:05` |
| `10:05:00` | `10:05 - 10:10` |
| `10:09:59` | `10:05 - 10:10` |

## 输出结构

| 字段 | 含义 |
| --- | --- |
| `gridId` | 网格编号 |
| `levelId` | 高度层 |
| `slotStart` | 占用开始时间 |
| `slotEnd` | 占用结束时间 |
| `sequenceNo` | 路径顺序 |

示例：

| sequenceNo | gridId | levelId | slotStart | slotEnd |
| ---: | --- | --- | --- | --- |
| 1 | `G-01-01` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` |
| 2 | `G-01-02` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` |
| 3 | `G-02-03` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` |

## 冲突检测语义

SkyGrid 接收占用单元后，可以用以下维度判断硬冲突：

```text
same date
same gridId
same levelId
overlapped slotStart/slotEnd
```

这意味着 LowAlt-RouteLab 不需要知道 SkyGrid 内部审批流程，只需要输出稳定、可解释的占用序列。

## API 示例

```bash
curl -X POST http://127.0.0.1:8001/api/timeslot/convert \
  -H "Content-Type: application/json" \
  -d "{\"path\":[\"G-01-01\",\"G-01-02\",\"G-02-03\"],\"level\":\"L120\",\"startTime\":\"2026-06-08 10:00:00\",\"speed\":10.0,\"gridSizeMeters\":100,\"slotMinutes\":5}"
```

该接口返回的 `occupancyUnits` 可由 `route-adapter-service` 保存，并交给 `MockSkyGridClient` 或真实 SkyGrid Gateway 做冲突检查。

