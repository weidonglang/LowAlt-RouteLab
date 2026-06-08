# 5 分钟复试演示流程

## 0:00 - 0:30 项目定位

介绍：

```text
LowAlt-RouteLab 是城市低空无人机航迹规划与风险评估仿真系统。它把低空空域建模为 Grid + Level + TimeSlot，完成从任务输入、航线规划、风险和能耗评估、TimeSlot 占用转换，到 SkyGrid mock 冲突校验的闭环。
```

强调：

- 不是普通 CRUD。
- 核心是低空航线规划和空域资源占用转换。
- 与 SkyGrid 形成互补。

## 0:30 - 1:00 架构说明

打开 README 或架构图说明：

```text
frontend -> route-adapter-service -> algorithm-service
route-adapter-service -> MockSkyGridClient
```

说明三个服务：

- Python FastAPI：算法。
- Java Spring Boot：任务编排和 SkyGrid 适配。
- Vue 前端：可视化演示工作台。

## 1:00 - 2:00 创建任务并规划

打开：

```text
http://127.0.0.1:5173/
```

在任务创建页展示：

- 起点：`G-01-01`
- 终点：`G-18-16`
- 高度层：`L120`
- 任务类型：`POWER_LINE_INSPECTION`
- 算法：`A_STAR`

点击开始规划。

讲解：

- Python 算法服务会加载 `demo-city-20x20` 地图。
- 路径会避开禁飞区和当前高度层障碍物。
- 规划结果包含距离、耗时、转弯次数、风险和能耗。

## 2:00 - 2:45 航线展示与风险评估

切到航线展示页：

- 指出 SVG 网格地图。
- 指出禁飞区、障碍物、风险区、起点、终点和航线。

切到风险评估页：

- 展示 `riskScore`。
- 展示 `riskLevel`。
- 展示 `riskFactors`。
- 展示 `estimatedBatteryUsage` 和 `energySafe`。

说明风险来自：

- 风险区。
- 转弯。
- 靠近禁飞区。
- 靠近障碍物。

## 2:45 - 3:30 算法对比

切到算法对比页，点击执行对比。

讲解：

- Dijkstra：无启发，访问节点更多。
- A*：使用启发函数，规划更快。
- Theta*：基于 A* 结果做 line-of-sight 平滑。

展示指标：

- 距离。
- 规划耗时。
- 转弯次数。
- 风险分。

## 3:30 - 4:15 群论增强

说明 C8：

```text
将 N, NE, E, SE, S, SW, W, NW 编码为 0-7，用模 8 运算计算转弯步数，并接入 A* / Dijkstra 的边代价。
```

说明 D4：

```text
对 20x20 正方形网格做旋转和反射，生成对称增强任务，用 benchmark 观察算法在对称场景下的稳定性。
```

可展示接口：

```text
POST /api/benchmark/symmetry
```

## 4:15 - 5:00 SkyGrid 联动

切到 SkyGrid 联动页。

展示：

- TimeSlot 占用表。
- 点击冲突检查。
- 展示 mock 冲突状态 `RISK_CONFLICT`。
- 点击提交预约。
- 展示 mock booking 状态 `MOCK_SUBMITTED`。

收尾：

```text
这个项目最终实现了从低空航线生成，到风险评估、占用时间片转换、冲突检测和预约提交的完整闭环。后续可以把内存仓储换成 MySQL，把 MockSkyGridClient 换成真实 SkyGrid 接口。
```

