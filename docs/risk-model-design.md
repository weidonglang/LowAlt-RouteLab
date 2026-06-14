# 风险模型设计

本文档说明 LowAlt-RouteLab 如何在低空航线规划中表达风险，并把风险转化为可解释的规划结果。

## 风险来源

系统当前使用 `demo-city-20x20` 地图，风险来自四类因素：

| 风险项 | 含义 | 处理方式 |
| --- | --- | --- |
| 风险区 | 城市低空中的高风险区域 | 增加路径风险权重 |
| 禁飞区邻近 | 路径靠近禁飞网格 | 生成风险提示 |
| 障碍物邻近 | 路径靠近当前高度层障碍物 | 生成风险提示 |
| 转弯复杂度 | 路径转弯次数多 | 增加风险与能耗 |

禁飞区和障碍物本身是硬约束，不是普通风险。路径规划不能穿越禁飞区，也不能穿越当前高度层被障碍物阻断的网格。

## 风险权重

每个网格的风险权重由两部分合成：

```text
riskWeight(grid) = max(grid.riskBase, riskZoneWeight)
```

- `riskBase` 来自基础地图。
- `riskZoneWeight` 来自风险区配置。

规划阶段会根据 `avoidRisk` 决定风险是否进入搜索代价：

| 参数 | 行为 |
| --- | --- |
| `avoidRisk=false` | 更关注距离和转弯，允许经过风险较高但可通行的网格 |
| `avoidRisk=true` | 将风险权重计入边代价，倾向绕开风险区 |

## 风险评分

路径规划完成后，系统对完整路径执行风险评估，输出：

- `riskScore`
- `riskLevel`
- `riskFactors`

风险等级：

| Score | Level |
| ---: | --- |
| `0.00 - 0.25` | `LOW` |
| `0.25 - 0.50` | `MEDIUM` |
| `0.50 - 0.75` | `HIGH` |
| `0.75 - 1.00` | `DANGEROUS` |

## 风险解释

`riskFactors` 用于让规划结果可解释，而不是只返回一个分数。典型解释包括：

- 当前路径是否经过风险区。
- 当前路径是否靠近禁飞区。
- 当前路径是否靠近障碍物。
- 当前路径是否包含较多转弯。

这类解释适合在前端风险评估页展示，也适合答辩时说明路径为什么被判定为中风险或高风险。

## 与能耗模型的关系

风险不是只影响安全，也会影响能耗估计。当前简化能耗模型会把风险格数量作为 `riskPenalty` 的输入：

```text
energy =
  baseCostPerMeter * distance
  + turnCost * turnCount
  + climbCost * levelChangeCount
  + riskPenalty * riskGridCount
```

当前版本没有高度切换，`levelChangeCount = 0`。

## 与 SkyGrid 的关系

LowAlt-RouteLab 输出的是算法侧风险评估，SkyGrid 侧仍会做治理侧冲突检测。

| 系统 | 风险/冲突职责 |
| --- | --- |
| LowAlt-RouteLab | 规划阶段规避风险区，输出 `riskScore` 和 `riskFactors` |
| SkyGrid | 审批阶段判断硬冲突、禁飞冲突、风险网格和相邻网格风险 |

因此风险在项目群中分两层：

1. 算法层尽量生成更低风险的航线。
2. 治理层判断这条航线在目标时间片是否可以占用。

