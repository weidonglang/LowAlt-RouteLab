# 群论增强模块

LowAlt-RouteLab 的群论模块只作为航迹规划的数学增强，不改变项目主线。当前实现包含 C8 离散航向群和 D4 网格对称变换。

## C8 离散航向

C8 将相邻网格的 8 个运动方向编码为：

```text
N=0, NE=1, E=2, SE=3, S=4, SW=5, W=6, NW=7
```

转弯步数使用模 8 最短距离：

```text
delta = abs(d2 - d1)
steps = min(delta, 8 - delta)
angle = steps * 45
```

该模块位于：

```text
algorithm-service/app/group_theory/direction_group.py
```

当前已接入 `cost_model.edge_cost`，A* 和 Dijkstra 的搜索状态包含“网格 + 入射方向”，因此转弯代价会参与路径选择。

## D4 网格对称

D4 包含正方形网格上的 8 种旋转/反射：

```text
IDENTITY
ROTATE_90
ROTATE_180
ROTATE_270
FLIP_HORIZONTAL
FLIP_VERTICAL
FLIP_MAIN_DIAGONAL
FLIP_ANTI_DIAGONAL
```

该模块位于：

```text
algorithm-service/app/group_theory/symmetry_transformer.py
```

它可以同步变换：

- 任务起点 `startGrid`
- 任务终点 `endGrid`
- 地图 `grids`
- 禁飞区 `noFlyZones`
- 障碍物 `obstacles`
- 风险区 `riskZones`

## 对称性增强实验

接口：

```http
POST /api/benchmark/symmetry
```

用途：

1. 读取 benchmark task。
2. 对每个任务应用 D4 变换。
3. 对变换后的地图和任务运行 Dijkstra / A* / Theta*。
4. 统计成功率、平均距离、平均规划耗时、平均风险分和 D4 距离方差。

示例请求：

```json
{
  "mapId": "demo-city-20x20",
  "benchmarkTaskFile": "benchmark_tasks.json",
  "algorithms": ["DIJKSTRA", "A_STAR", "THETA_STAR"],
  "transforms": ["IDENTITY", "ROTATE_90", "ROTATE_180", "ROTATE_270"]
}
```

