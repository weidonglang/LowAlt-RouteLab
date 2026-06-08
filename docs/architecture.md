# 架构说明

LowAlt-RouteLab 是一个城市低空无人机航迹规划与风险评估仿真系统。系统把低空空域抽象成：

```text
Grid + Level + TimeSlot
```

核心目标是完成从任务输入、航线生成、风险/能耗评估、TimeSlot 占用转换，到 SkyGrid 冲突校验的演示闭环。

## 系统组成

```text
frontend
  ↓
route-adapter-service
  ↓
algorithm-service
  ↓
demo map / benchmark tasks

route-adapter-service
  ↓
MockSkyGridClient
```

## algorithm-service

Python FastAPI 算法服务，负责：

- 加载 `demo-city-20x20` 地图。
- 查询禁飞区、障碍物、风险区。
- 执行 Dijkstra / A* / Theta* 路径规划。
- 计算 C8 转弯代价。
- 执行 D4 对称变换与 benchmark。
- 评估风险和能耗。
- 转换路径为 TimeSlot 占用序列。

核心路径：

```text
algorithm-service/app
├── algorithms
├── core
├── energy
├── group_theory
├── risk
├── routers
├── schemas
├── timeslot
└── utils
```

## route-adapter-service

Java Spring Boot 适配服务，负责：

- 创建航线任务。
- 调用 Python 算法服务执行规划。
- 调用 Python TimeSlot 转换接口。
- 暂存任务、规划结果、占用序列和冲突结果。
- 调用 `MockSkyGridClient` 完成模拟冲突检查和预约提交。

当前使用内存仓储，目的是优先保证可运行 MVP。后续可以替换为 MySQL 表：

- `route_task`
- `route_plan`
- `route_occupancy_unit`
- `route_conflict_check_record`

## frontend

Vue 3 前端工作台，负责：

- 创建任务。
- 展示网格地图、禁飞区、障碍物、风险区、航线和冲突点。
- 展示风险、能耗、路径节点。
- 展示 Dijkstra / A* / Theta* 算法对比。
- 展示 TimeSlot 占用表和 SkyGrid mock 结果。

前端开发环境通过 Vite proxy 访问：

```text
/algorithm-api -> http://127.0.0.1:8001
/adapter-api   -> http://127.0.0.1:8081
```

## 数据流

```text
1. 前端输入任务参数
2. route-adapter-service 创建任务
3. route-adapter-service 调用 algorithm-service /api/plan
4. algorithm-service 返回路径、距离、风险、能耗
5. route-adapter-service 调用 algorithm-service /api/timeslot/convert
6. route-adapter-service 保存占用序列
7. 前端触发 SkyGrid 冲突检查
8. MockSkyGridClient 返回模拟冲突
9. 前端展示冲突点和预约状态
```

## 与 SkyGrid 的关系

SkyGrid 负责空域资源管理、预约审批、冲突检测和通知审计。

LowAlt-RouteLab 负责航线生成、风险评估、能耗估计和 TimeSlot 占用转换。

当前项目中 SkyGrid 由 `MockSkyGridClient` 模拟，保证没有真实 SkyGrid 时仍可演示完整流程。

