# 算法实验评估报告

本文档记录 LowAlt-RouteLab 在 `demo-city-20x20` 地图上的算法对比实验。实验目标不是证明某一个算法绝对最优，而是展示路径长度、转弯次数、风险、能耗和规划耗时之间的取舍。

## 实验环境

| 项目 | 值 |
| --- | --- |
| 地图 | `demo-city-20x20` |
| 网格规模 | `20 x 20` |
| 网格尺寸 | `100m x 100m` |
| 高度层 | `L120` |
| 任务类型 | `POWER_LINE_INSPECTION` |
| 起点 | `G-01-01` |
| 终点 | `G-18-16` |
| 邻接模式 | 8 邻接 |
| 风险规避 | `avoidRisk=true` |

数据来自本地直接调用算法模块的一次样例运行。不同机器上 `planningTimeMs` 可能略有波动，应以同一环境内的相对差异为准。

## Dijkstra / A* / Theta* 对比

| Algorithm | Path Length | Turn Count | Risk Score | Energy Cost | Planning Time | Path Nodes | Visited Nodes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Dijkstra | 2321.320 | 1 | 0.254 | 14.228 | 94 ms | 18 | 2328 |
| A* | 2321.320 | 1 | 0.254 | 14.228 | 4 ms | 18 | 95 |
| Theta* | 2270.574 | 1 | 0.295 | 13.923 | 4 ms | 3 | 95 |

## 结果解读

- Dijkstra 能找到稳定可行路径，但访问节点数最高，适合作为基线。
- A* 在相同路径质量下显著减少访问节点，适合低空任务实时规划。
- Theta* 通过 line-of-sight smoothing 减少路径节点和路径长度，但风险分数略高，说明平滑路径可能更靠近风险区域。
- 能耗与路径距离、转弯次数、风险格有关；Theta* 在该样例中距离更短，所以估算能耗更低。

## 风险规避前后对比

该实验使用更容易体现风险规避差异的任务：

| 项目 | 值 |
| --- | --- |
| 起点 | `G-01-20` |
| 终点 | `G-20-10` |
| 算法 | `A_STAR` |
| 高风险格判断 | `riskWeight >= 0.2` |

| Mode | Path Length | High Risk Cells Passed | Risk Score | Energy Cost | Path Nodes |
| --- | ---: | ---: | ---: | ---: | ---: |
| `avoidRisk=false` | 2314.214 | 1 | 0.124 | 14.385 | 20 |
| `avoidRisk=true` | 2314.214 | 0 | 0.056 | 14.185 | 20 |

路径差异：

| Mode | Path Preview |
| --- | --- |
| `avoidRisk=false` | `G-01-20 → G-02-19 → G-03-18 → G-04-17 → G-05-16 → ... → G-20-10` |
| `avoidRisk=true` | `G-01-20 → G-02-20 → G-03-20 → G-04-20 → G-05-20 → ... → G-20-10` |

该样例中，风险规避没有增加路径长度，但绕开了一个高风险格，风险分数下降约 54.8%。

## TimeSlot 转换示例

以下示例来自 `G-01-01 → G-18-16` 的 A* 路径前 5 个节点，参数为：

| 参数 | 值 |
| --- | --- |
| 高度层 | `L120` |
| 开始时间 | `2026-06-08 10:00:00` |
| 速度 | `10 m/s` |
| 网格尺寸 | `100m` |
| 时间片 | `5 min` |

| Path Segment | Grid | Level | Start Time | End Time | Slot |
| ---: | --- | --- | --- | --- | --- |
| 1 | `G-01-01` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` | `T-001` |
| 2 | `G-02-01` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` | `T-002` |
| 3 | `G-03-01` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` | `T-003` |
| 4 | `G-04-02` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` | `T-004` |
| 5 | `G-05-03` | `L120` | `2026-06-08T10:00:00` | `2026-06-08T10:05:00` | `T-005` |

说明：当前转换结果使用 `sequenceNo` 表达路径顺序，实际 SkyGrid 侧判断冲突时关注的是 `Grid + Level + slotStart + slotEnd`。

## 可复现实验命令

启动算法服务后可通过接口复现实验：

```bash
curl -X POST http://127.0.0.1:8001/api/plan/compare \
  -H "Content-Type: application/json" \
  -d "{\"mapId\":\"demo-city-20x20\",\"taskType\":\"POWER_LINE_INSPECTION\",\"startGrid\":\"G-01-01\",\"endGrid\":\"G-18-16\",\"level\":\"L120\",\"algorithms\":[\"DIJKSTRA\",\"A_STAR\",\"THETA_STAR\"],\"avoidRisk\":true,\"allowDiagonal\":true}"
```

风险规避对比：

```bash
curl -X POST http://127.0.0.1:8001/api/plan \
  -H "Content-Type: application/json" \
  -d "{\"mapId\":\"demo-city-20x20\",\"taskType\":\"POWER_LINE_INSPECTION\",\"startGrid\":\"G-01-20\",\"endGrid\":\"G-20-10\",\"level\":\"L120\",\"algorithm\":\"A_STAR\",\"avoidRisk\":true,\"allowDiagonal\":true}"
```

