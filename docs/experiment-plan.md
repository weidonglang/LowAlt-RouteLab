# 实验计划

## 目标

验证 LowAlt-RouteLab 在低空航线规划场景中的几个核心能力：

- 不同算法的路径质量和规划耗时。
- 风险规避对路径的影响。
- C8 转弯代价对航迹平滑度的影响。
- D4 对称增强下算法表现是否稳定。
- TimeSlot 转换是否能支撑 SkyGrid 占用检查。

## 实验一：算法对比

接口：

```http
POST /api/plan/compare
```

对比算法：

- Dijkstra
- A*
- Theta*

指标：

- `distance`
- `planningTimeMs`
- `turnCount`
- `riskScore`
- `visitedCount`

预期现象：

- Dijkstra 访问节点更多。
- A* 规划速度更快。
- Theta* 通过 line-of-sight 平滑减少中间节点。

## 实验二：风险规避

变量：

```text
avoidRisk = true / false
```

观察：

- 路径是否绕开风险区。
- `riskScore` 是否下降。
- `distance` 是否增加。

## 实验三：C8 转弯代价

观察：

- `turnCount`
- 路径折线形态
- `planningTimeMs`

C8 的意义在于让转弯不只是展示指标，而是进入搜索代价。

## 实验四：D4 对称性增强

接口：

```http
POST /api/benchmark/symmetry
```

流程：

```text
读取 benchmark_tasks.json
对每个任务应用 D4 变换
运行 Dijkstra / A* / Theta*
统计平均距离、平均耗时、平均风险和距离方差
```

指标：

- `taskCount`
- `augmentedTaskCount`
- `successRate`
- `avgDistance`
- `avgPlanningTimeMs`
- `avgRiskScore`
- `distanceVarianceUnderD4`

## 实验五：SkyGrid 联动

流程：

```text
创建任务
执行规划
生成 TimeSlot 占用
MockSkyGridClient 检查冲突
MockSkyGridClient 提交预约
```

验证点：

- 占用序列包含 `gridId`、`levelId`、`slotStart`、`slotEnd`。
- 冲突结果可在前端高亮展示。
- 预约状态可回写任务详情。

