# 算法设计

## 地图模型

系统使用 `demo-city-20x20` 地图：

```text
20 × 20 grids
grid size = 100m × 100m
levels = L60, L90, L120, L150, L180
```

每个网格包含：

- `gridId`
- `x`
- `y`
- `terrainType`
- `riskBase`
- `isNoFly`
- `isObstacle`

地图还包含：

- 禁飞区 `noFlyZones`
- 障碍物 `obstacles`
- 风险区 `riskZones`

## Grid ID

规则：

```text
x=1, y=1   -> G-01-01
x=20, y=20 -> G-20-20
```

工具函数位于：

```text
algorithm-service/app/utils/grid_id.py
```

## 路径规划

当前支持：

- Dijkstra
- A*
- Theta*

默认允许 8 邻接移动。

### 可通行条件

某网格在指定高度层可通行，需要满足：

```text
not no-fly
and not obstacle at current level
```

### 边代价

第一阶段实现：

```text
cost = distance_weight * distance_cost
     + risk_weight * risk_cost
     + turn_weight * turn_cost
```

任务类型权重：

- `LOGISTICS_DELIVERY`
- `POWER_LINE_INSPECTION`
- `EMERGENCY_RESCUE`

## C8 转弯代价

8 个方向编码：

```text
N=0, NE=1, E=2, SE=3, S=4, SW=5, W=6, NW=7
```

转弯步数：

```text
delta = abs(d2 - d1)
steps = min(delta, 8 - delta)
```

A* / Dijkstra 的搜索状态不是单纯的 `gridId`，而是：

```text
(gridId, incomingDirection)
```

这样到达同一网格但航向不同的状态可以有不同代价，转弯代价会真实影响路径选择。

## Theta*

当前实现为简化版：

```text
A* path -> line-of-sight smoothing
```

平滑时使用 Bresenham 直线检查，不允许直线穿越禁飞区或当前高度层障碍物。

## 风险评估

当前风险项：

- 风险区风险
- 转弯风险
- 靠近禁飞区风险
- 靠近障碍物风险

输出：

- `riskScore`
- `riskLevel`
- `riskFactors`

风险等级：

```text
0.00 - 0.25 LOW
0.25 - 0.50 MEDIUM
0.50 - 0.75 HIGH
0.75 - 1.00 DANGEROUS
```

## 能耗估计

简化公式：

```text
energy =
  baseCostPerMeter * distance
  + turnCost * turnCount
  + climbCost * levelChangeCount
  + riskPenalty * riskGridCount
```

当前无高度切换，`levelChangeCount = 0`。

## TimeSlot 转换

路径移动是连续的，SkyGrid 占用是离散的。

转换规则：

1. 起点时间为 `startTime`。
2. 每段移动时间由 `segmentDistance / speed` 累加。
3. 每个路径节点按到达时刻映射到 TimeSlot。
4. 同一个 `gridId + levelId + slotStart + slotEnd` 去重。
5. 输出稳定递增 `sequenceNo`。

