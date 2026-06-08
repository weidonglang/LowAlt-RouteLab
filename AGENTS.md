# AGENTS.md — LowAlt-RouteLab Codex 开发说明书

> 本文件用于指导 Codex / 代码代理开发 **LowAlt-RouteLab：城市低空无人机航迹规划与风险评估仿真系统**。  
> 项目目标不是做普通后台管理系统，而是实现一个能够和 SkyGrid 低空资源平台联动的“航线规划 + 风险评估 + 时间片占用转换 + 冲突校验”算法仿真项目。

---

## 0. 给 Codex 的总要求

你是本项目的开发代理。请严格按以下要求执行：

1. **优先实现可运行 MVP，不要一开始追求复杂 3D、ROS、真实无人机飞控。**
2. **所有功能必须能本地运行、能测试、能展示。**
3. **先做 Python FastAPI 算法服务，再做 Java 适配服务，再做 Vue 前端。**
4. **每完成一个阶段，都要补充 README、接口说明、运行命令和测试用例。**
5. **不要删除已有代码；如需重构，先说明原因并保持兼容。**
6. **所有接口返回统一 JSON 结构。**
7. **算法模块必须可独立测试，不依赖前端和 SkyGrid。**
8. **SkyGrid 未启动时，必须使用 mock client 保证项目可演示。**
9. **群论模块只作为数学增强，不要喧宾夺主，不要把项目写成纯数学项目。**
10. **项目最终必须能展示：航线规划、风险评分、算法对比、D4 对称性增强实验、C8 转弯代价、TimeSlot 转换、SkyGrid 冲突校验。**

---

## 1. 项目名称与定位

### 1.1 项目名称

中文名：

```text
LowAlt-RouteLab：城市低空无人机航迹规划与风险评估仿真系统
```

英文名：

```text
LowAlt-RouteLab: UAV Route Planning and Risk Evaluation Simulator for Urban Low-Altitude Airspace
```

### 1.2 项目定位

本项目面向低空技术与工程方向，构建一个低空无人机任务规划仿真系统。系统将城市低空空域离散为：

```text
Grid + Level + TimeSlot
```

并在此基础上实现：

- 低空网格地图建模；
- 禁飞区建模；
- 障碍物建模；
- 风险区建模；
- A* / Dijkstra / Theta* 航迹规划；
- C8 离散航向与转弯代价计算；
- D4 网格对称变换与测试样本增强；
- 航线风险评分；
- 简化能耗估计；
- 路径转 TimeSlot 占用序列；
- SkyGrid 冲突校验与预约提交适配；
- 前端可视化演示。

### 1.3 与 SkyGrid 的关系

SkyGrid 负责：

```text
空域资源管理 / 预约审批 / 冲突检测 / 通知审计 / 微服务治理
```

LowAlt-RouteLab 负责：

```text
航线生成 / 风险评估 / 能耗估计 / TimeSlot 占用转换 / 算法对比实验
```

二者关系：

```text
用户输入任务
  ↓
LowAlt-RouteLab 生成航线
  ↓
路径转 Grid + Level + TimeSlot
  ↓
调用 SkyGrid 检查冲突
  ↓
无冲突则提交预约审批
```

---

## 2. 技术栈

### 2.1 algorithm-service

```text
Python 3.10+
FastAPI
Pydantic
NumPy
NetworkX，可选
pytest
uvicorn
```

### 2.2 route-adapter-service

```text
Java 17+
Spring Boot 3.x
Spring Web
Spring Validation
Spring Data JPA / MyBatis Plus 二选一
MySQL
Redis，可选
OpenFeign 或 RestTemplate/WebClient
```

### 2.3 frontend

```text
Vue 3
Vite
TypeScript
Element Plus
ECharts
Canvas / SVG
Axios
Pinia，可选
```

### 2.4 部署

```text
Docker Compose
MySQL 8
Redis 7，可选
Nginx，可选
```

---

## 3. 推荐仓库结构

请按如下结构创建或整理项目：

```text
LowAlt-RouteLab
├── AGENTS.md
├── README.md
├── docs
│   ├── architecture.md
│   ├── api-design.md
│   ├── algorithm-design.md
│   ├── group-theory-module.md
│   ├── experiment-plan.md
│   └── interview-notes.md
├── algorithm-service
│   ├── app
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── schemas
│   │   │   ├── common.py
│   │   │   ├── map_schema.py
│   │   │   ├── plan_schema.py
│   │   │   ├── risk_schema.py
│   │   │   └── timeslot_schema.py
│   │   ├── routers
│   │   │   ├── map_router.py
│   │   │   ├── plan_router.py
│   │   │   ├── risk_router.py
│   │   │   ├── timeslot_router.py
│   │   │   └── benchmark_router.py
│   │   ├── core
│   │   │   ├── map_loader.py
│   │   │   ├── graph_builder.py
│   │   │   ├── cost_model.py
│   │   │   └── validators.py
│   │   ├── algorithms
│   │   │   ├── dijkstra.py
│   │   │   ├── astar.py
│   │   │   ├── theta_star.py
│   │   │   └── path_utils.py
│   │   ├── group_theory
│   │   │   ├── direction_group.py
│   │   │   ├── symmetry_transformer.py
│   │   │   ├── permutation_tasks.py
│   │   │   └── symmetry_benchmark.py
│   │   ├── risk
│   │   │   ├── risk_evaluator.py
│   │   │   └── risk_explainer.py
│   │   ├── energy
│   │   │   └── energy_estimator.py
│   │   ├── timeslot
│   │   │   └── timeslot_converter.py
│   │   └── utils
│   │       ├── grid_id.py
│   │       ├── geometry.py
│   │       └── priority_queue.py
│   ├── data
│   │   ├── maps
│   │   │   └── demo-city-20x20.json
│   │   └── benchmark_tasks
│   │       └── benchmark_tasks.json
│   ├── tests
│   │   ├── test_astar.py
│   │   ├── test_dijkstra.py
│   │   ├── test_direction_group.py
│   │   ├── test_symmetry_transformer.py
│   │   ├── test_risk_evaluator.py
│   │   └── test_timeslot_converter.py
│   ├── requirements.txt
│   └── README.md
├── route-adapter-service
│   ├── src
│   ├── pom.xml
│   └── README.md
├── frontend
│   ├── src
│   ├── package.json
│   └── README.md
├── docker-compose.yml
└── scripts
    ├── run_algorithm_demo.py
    ├── run_benchmark.py
    └── generate_demo_map.py
```

---

## 4. 第一优先级：algorithm-service

请优先完成 `algorithm-service`，因为这是项目核心。

### 4.1 FastAPI 启动入口

实现：

```text
algorithm-service/app/main.py
```

要求：

- 注册 map、plan、risk、timeslot、benchmark 路由；
- 提供 `/health` 接口；
- 启动后访问 Swagger 文档；
- 所有接口统一返回 JSON。

示例接口：

```http
GET /health
```

返回：

```json
{
  "code": 200,
  "message": "algorithm-service is running",
  "data": {
    "service": "LowAlt-RouteLab algorithm-service",
    "status": "UP"
  }
}
```

---

## 5. 地图数据模型

### 5.1 demo 地图

必须创建：

```text
algorithm-service/data/maps/demo-city-20x20.json
```

地图大小：

```text
20 × 20
```

每个 Grid 表示：

```text
100m × 100m
```

高度层：

```text
L60, L90, L120, L150, L180
```

示例结构：

```json
{
  "mapId": "demo-city-20x20",
  "width": 20,
  "height": 20,
  "gridSizeMeters": 100,
  "levels": ["L60", "L90", "L120", "L150", "L180"],
  "grids": [
    {
      "gridId": "G-01-01",
      "x": 1,
      "y": 1,
      "terrainType": "URBAN",
      "riskBase": 0.1,
      "isNoFly": false,
      "isObstacle": false
    }
  ],
  "noFlyZones": [
    {
      "zoneId": "NFZ-001",
      "name": "机场保护区",
      "gridIds": ["G-08-08", "G-08-09", "G-09-08", "G-09-09"],
      "blockedLevels": ["L60", "L90", "L120", "L150", "L180"]
    }
  ],
  "obstacles": [
    {
      "obstacleId": "OBS-001",
      "name": "高层建筑群",
      "gridIds": ["G-04-05", "G-04-06", "G-05-05"],
      "blockedLevels": ["L60", "L90", "L120"]
    }
  ],
  "riskZones": [
    {
      "riskZoneId": "RZ-001",
      "name": "人流密集区",
      "gridIds": ["G-10-11", "G-10-12", "G-11-11", "G-11-12"],
      "riskWeight": 0.65,
      "riskType": "DENSE_POPULATION"
    }
  ]
}
```

### 5.2 地图加载器

实现：

```text
app/core/map_loader.py
```

功能：

- 根据 mapId 加载 JSON；
- 校验地图尺寸；
- 校验 gridId 合法性；
- 构建快速查询索引；
- 提供禁飞区、障碍物、风险区查询。

验收标准：

- 能正确加载 demo-city-20x20；
- 查询任意 gridId 是否禁飞；
- 查询任意 gridId 在某 level 是否障碍；
- 查询任意 gridId 的风险权重。

---

## 6. Grid ID 工具

实现：

```text
app/utils/grid_id.py
```

功能：

```python
def to_grid_id(x: int, y: int) -> str:
    ...

def parse_grid_id(grid_id: str) -> tuple[int, int]:
    ...

def is_valid_grid_id(grid_id: str, width: int, height: int) -> bool:
    ...
```

规则：

```text
x=1, y=1 -> G-01-01
x=20, y=20 -> G-20-20
```

必须写测试：

```text
tests/test_grid_id.py
```

---

## 7. 路径规划算法

### 7.1 Dijkstra

实现：

```text
app/algorithms/dijkstra.py
```

功能：

- 输入地图、起点、终点、level；
- 避开禁飞区；
- 避开当前 level 下的障碍物；
- 输出 path、distance、visitedCount、planningTimeMs。

验收标准：

- 在无障碍地图中找到最短路径；
- 在有禁飞区地图中绕开禁飞区；
- 起点或终点非法时返回清晰错误；
- 无路径时返回 `success=false`，不得崩溃。

### 7.2 A*

实现：

```text
app/algorithms/astar.py
```

A* 公式：

```text
f(n) = g(n) + h(n)
```

启发函数：

- 4 邻接：曼哈顿距离；
- 8 邻接：欧氏距离。

本项目默认先实现 8 邻接。

### 7.3 低空代价函数

实现：

```text
app/core/cost_model.py
```

边代价公式：

```text
Cost(n → m) =
    α · distance_cost
  + β · risk_cost
  + γ · turn_cost
  + δ · energy_cost
  + λ · level_change_cost
  + μ · conflict_cost
```

第一阶段可先实现：

```text
distance_cost + risk_cost + turn_cost
```

后续扩展 energy、level、conflict。

默认权重：

```json
{
  "distance": 0.50,
  "risk": 0.25,
  "turn": 0.15,
  "energy": 0.05,
  "conflict": 0.05
}
```

任务类型权重：

```json
{
  "LOGISTICS_DELIVERY": {
    "distance": 0.55,
    "risk": 0.20,
    "turn": 0.10,
    "energy": 0.10,
    "conflict": 0.05
  },
  "POWER_LINE_INSPECTION": {
    "distance": 0.30,
    "risk": 0.35,
    "turn": 0.15,
    "energy": 0.10,
    "conflict": 0.10
  },
  "EMERGENCY_RESCUE": {
    "distance": 0.65,
    "risk": 0.10,
    "turn": 0.10,
    "energy": 0.05,
    "conflict": 0.10
  }
}
```

### 7.4 Theta*

实现：

```text
app/algorithms/theta_star.py
```

目标：

- 基于 A* 结果进行路径平滑；
- 使用 line-of-sight 检查；
- 不允许直线穿越禁飞区或障碍物；
- 输出平滑后的 path、turnCount、distance。

如时间不够，先实现简化版：

```text
A* path -> remove unnecessary middle points if line-of-sight is clear
```

---

## 8. 群论增强模块

本模块是项目数学亮点，但必须轻量、可运行、可测试。

### 8.1 C8 离散航向群

实现：

```text
app/group_theory/direction_group.py
```

8 个方向：

```text
N  = 0
NE = 1
E  = 2
SE = 3
S  = 4
SW = 5
W  = 6
NW = 7
```

实现函数：

```python
def direction_between(a: tuple[int, int], b: tuple[int, int]) -> int:
    """返回从 a 到 b 的 C8 方向编号。"""

def turn_steps(d1: int, d2: int) -> int:
    """使用模 8 运算计算最小转向步数。"""

def turn_angle_degrees(d1: int, d2: int) -> int:
    """每一步代表 45°，返回转弯角度。"""

def turn_cost(d1: int, d2: int, weight: float = 1.0) -> float:
    """返回转弯代价。"""
```

转弯步数公式：

```text
delta = abs(d2 - d1)
turn_steps = min(delta, 8 - delta)
```

验收标准：

```text
N -> E  = 2 steps = 90°
N -> S  = 4 steps = 180°
NW -> N = 1 step  = 45°
E -> NE = 1 step  = 45°
```

必须写测试：

```text
tests/test_direction_group.py
```

### 8.2 D4 网格对称变换

实现：

```text
app/group_theory/symmetry_transformer.py
```

D4 变换包括：

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

对于 `width = height = N` 的正方形网格，坐标从 1 开始。

变换规则：

```text
IDENTITY:          (x, y) -> (x, y)
ROTATE_90:         (x, y) -> (y, N + 1 - x)
ROTATE_180:        (x, y) -> (N + 1 - x, N + 1 - y)
ROTATE_270:        (x, y) -> (N + 1 - y, x)
FLIP_HORIZONTAL:   (x, y) -> (x, N + 1 - y)
FLIP_VERTICAL:     (x, y) -> (N + 1 - x, y)
FLIP_MAIN_DIAGONAL:(x, y) -> (y, x)
FLIP_ANTI_DIAGONAL:(x, y) -> (N + 1 - y, N + 1 - x)
```

实现函数：

```python
def transform_point(x: int, y: int, n: int, transform: str) -> tuple[int, int]:
    ...

def transform_grid_id(grid_id: str, n: int, transform: str) -> str:
    ...

def transform_grid_list(grid_ids: list[str], n: int, transform: str) -> list[str]:
    ...

def transform_task(task: dict, n: int, transform: str) -> dict:
    ...

def transform_map(map_data: dict, transform: str) -> dict:
    ...
```

必须同步变换：

- startGrid；
- endGrid；
- noFlyZones；
- obstacles；
- riskZones；
- benchmark task。

验收标准：

- 对 20 × 20 地图，`ROTATE_90(G-01-01) = G-01-20`；
- `ROTATE_180(G-01-01) = G-20-20`；
- `FLIP_MAIN_DIAGONAL(G-03-05) = G-05-03`；
- 对同一任务连续执行 4 次 ROTATE_90 后回到原任务；
- 对同一任务连续执行 2 次 FLIP_HORIZONTAL 后回到原任务。

必须写测试：

```text
tests/test_symmetry_transformer.py
```

### 8.3 D4 对称性增强实验

实现：

```text
app/group_theory/symmetry_benchmark.py
```

流程：

```text
读取 benchmark_tasks.json
  ↓
对每个任务应用 D4 的 8 种变换
  ↓
生成增强任务集
  ↓
分别运行 Dijkstra / A* / Theta*
  ↓
统计 path length、planning time、risk score、success rate
```

输出指标：

```json
{
  "taskCount": 20,
  "augmentedTaskCount": 160,
  "algorithms": [
    {
      "algorithm": "A_STAR",
      "successRate": 1.0,
      "avgDistance": 2450.0,
      "avgPlanningTimeMs": 18.4,
      "avgRiskScore": 0.27,
      "distanceVarianceUnderD4": 0.015
    }
  ]
}
```

### 8.4 置换思想，多任务点可选

实现：

```text
app/group_theory/permutation_tasks.py
```

该模块为 P2 功能，可以晚点做。

功能：

- 输入起点、终点、若干任务点；
- 当任务点数量 `n <= 6` 时枚举访问顺序；
- 计算每种顺序的总路径代价；
- 返回最优顺序。

不要把这个功能放进 MVP 主线。

---

## 9. 风险评估模块

实现：

```text
app/risk/risk_evaluator.py
app/risk/risk_explainer.py
```

风险评分公式：

```text
risk_score =
    w1 × no_fly_near_risk
  + w2 × obstacle_near_risk
  + w3 × risk_zone_risk
  + w4 × turn_risk
  + w5 × level_change_risk
  + w6 × conflict_near_risk
  + w7 × energy_risk
```

第一阶段实现：

```text
risk_zone_risk + turn_risk + obstacle_near_risk + no_fly_near_risk
```

风险等级：

```text
0.00 - 0.25 LOW
0.25 - 0.50 MEDIUM
0.50 - 0.75 HIGH
0.75 - 1.00 DANGEROUS
```

返回示例：

```json
{
  "riskScore": 0.31,
  "riskLevel": "MEDIUM",
  "mainFactors": [
    "路径经过 2 个中风险网格",
    "距离禁飞区 NFZ-001 最近 1 个网格",
    "当前航线存在 6 次转弯",
    "未发现硬冲突"
  ]
}
```

验收标准：

- 经过风险区的路径风险分高于不经过风险区的路径；
- 转弯次数多的路径风险略高；
- 靠近禁飞区的路径能给出解释；
- 输出必须包含 riskScore、riskLevel、mainFactors。

---

## 10. 能耗估计模块

实现：

```text
app/energy/energy_estimator.py
```

简化公式：

```text
energy_cost =
    base_cost_per_meter × distance
  + turn_cost × turn_count
  + climb_cost × level_change_count
  + risk_penalty × risk_grid_count
```

默认参数：

```json
{
  "baseCostPerMeter": 0.006,
  "turnCost": 0.3,
  "climbCost": 1.2,
  "riskPenalty": 0.2,
  "batteryLimit": 80.0
}
```

输出：

```json
{
  "estimatedBatteryUsage": 34.5,
  "batteryLimit": 80.0,
  "energySafe": true
}
```

说明：

```text
本项目中的能耗模型是任务规划阶段的简化估算模型，不等同于真实飞控能耗模型。
```

---

## 11. TimeSlot 转换模块

实现：

```text
app/timeslot/timeslot_converter.py
```

输入：

```json
{
  "path": ["G-01-01", "G-01-02", "G-02-03"],
  "level": "L120",
  "startTime": "2026-06-08 10:00:00",
  "speed": 10.0,
  "gridSizeMeters": 100,
  "slotMinutes": 5
}
```

输出：

```json
{
  "occupancyUnits": [
    {
      "gridId": "G-01-01",
      "levelId": "L120",
      "slotStart": "2026-06-08 10:00:00",
      "slotEnd": "2026-06-08 10:05:00",
      "sequenceNo": 1
    }
  ]
}
```

规则：

- 路径移动是连续的；
- SkyGrid 管理是离散的；
- 一个 TimeSlot 内可能包含多个 Grid；
- 输出去重，避免同一个 `gridId + levelId + slotStart + slotEnd` 重复。

验收标准：

- 能把路径转换为占用序列；
- 能按 5 分钟聚合；
- 能处理斜向移动距离；
- 能输出 sequenceNo。

---

## 12. algorithm-service API

### 12.1 健康检查

```http
GET /health
```

### 12.2 获取地图

```http
GET /api/maps/{mapId}
```

### 12.3 执行规划

```http
POST /api/plan
```

请求：

```json
{
  "mapId": "demo-city-20x20",
  "taskType": "POWER_LINE_INSPECTION",
  "startGrid": "G-01-01",
  "endGrid": "G-18-16",
  "level": "L120",
  "algorithm": "A_STAR",
  "avoidRisk": true,
  "allowDiagonal": true
}
```

响应：

```json
{
  "code": 200,
  "message": "planned successfully",
  "data": {
    "success": true,
    "algorithm": "A_STAR",
    "path": ["G-01-01", "G-02-02", "G-03-03"],
    "distance": 4280.0,
    "estimatedTimeSeconds": 430,
    "turnCount": 6,
    "planningTimeMs": 18,
    "riskScore": 0.31,
    "riskLevel": "MEDIUM",
    "estimatedBatteryUsage": 34.5,
    "energySafe": true,
    "riskFactors": [
      "路径经过 2 个中风险网格"
    ]
  }
}
```

### 12.4 算法对比

```http
POST /api/plan/compare
```

请求：

```json
{
  "mapId": "demo-city-20x20",
  "startGrid": "G-01-01",
  "endGrid": "G-18-16",
  "level": "L120",
  "algorithms": ["DIJKSTRA", "A_STAR", "THETA_STAR"]
}
```

### 12.5 TimeSlot 转换

```http
POST /api/timeslot/convert
```

### 12.6 D4 对称性实验

```http
POST /api/benchmark/symmetry
```

请求：

```json
{
  "mapId": "demo-city-20x20",
  "benchmarkTaskFile": "benchmark_tasks.json",
  "algorithms": ["DIJKSTRA", "A_STAR", "THETA_STAR"],
  "transforms": [
    "IDENTITY",
    "ROTATE_90",
    "ROTATE_180",
    "ROTATE_270",
    "FLIP_HORIZONTAL",
    "FLIP_VERTICAL",
    "FLIP_MAIN_DIAGONAL",
    "FLIP_ANTI_DIAGONAL"
  ]
}
```

---

## 13. route-adapter-service

该服务用于连接前端、algorithm-service 和 SkyGrid。

如果用户已有 SkyGrid 项目，则保留接口适配；如果没有启动 SkyGrid，则使用 mock client。

### 13.1 核心功能

- 创建任务；
- 调用 algorithm-service 规划；
- 保存规划结果；
- 调用 SkyGrid 检查冲突；
- 提交 SkyGrid 预约；
- 查询任务历史。

### 13.2 数据库表

#### route_task

```sql
CREATE TABLE route_task (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_name VARCHAR(128) NOT NULL,
    task_type VARCHAR(64) NOT NULL,
    start_grid VARCHAR(32) NOT NULL,
    end_grid VARCHAR(32) NOT NULL,
    start_level VARCHAR(32) NOT NULL,
    target_level VARCHAR(32),
    start_time DATETIME NOT NULL,
    drone_model VARCHAR(64),
    algorithm VARCHAR(32),
    avoid_risk TINYINT DEFAULT 1,
    allow_level_change TINYINT DEFAULT 0,
    connect_skygrid TINYINT DEFAULT 1,
    status VARCHAR(32) DEFAULT 'CREATED',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### route_plan

```sql
CREATE TABLE route_plan (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL,
    algorithm VARCHAR(32) NOT NULL,
    path_json JSON NOT NULL,
    distance DOUBLE,
    estimated_time INT,
    turn_count INT,
    level_change_count INT,
    risk_score DOUBLE,
    risk_level VARCHAR(32),
    battery_usage DOUBLE,
    energy_safe TINYINT,
    planning_time_ms INT,
    status VARCHAR(32),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### route_occupancy_unit

```sql
CREATE TABLE route_occupancy_unit (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    plan_id BIGINT NOT NULL,
    grid_id VARCHAR(32) NOT NULL,
    level_id VARCHAR(32) NOT NULL,
    slot_start DATETIME NOT NULL,
    slot_end DATETIME NOT NULL,
    sequence_no INT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### route_conflict_check_record

```sql
CREATE TABLE route_conflict_check_record (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    task_id BIGINT NOT NULL,
    plan_id BIGINT NOT NULL,
    conflict_status VARCHAR(32) NOT NULL,
    conflict_count INT DEFAULT 0,
    skygrid_response JSON,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 13.3 Java API

#### 创建任务

```http
POST /api/tasks
```

#### 执行规划

```http
POST /api/tasks/{taskId}/plan
```

#### 检查 SkyGrid 冲突

```http
POST /api/tasks/{taskId}/check-conflict
```

#### 提交 SkyGrid

```http
POST /api/tasks/{taskId}/submit-skygrid
```

#### 查询任务

```http
GET /api/tasks/{taskId}
```

---

## 14. SkyGrid Client

实现两个版本：

```text
RealSkyGridClient
MockSkyGridClient
```

### 14.1 MockSkyGridClient

必须先实现。

模拟返回：

```json
{
  "conflictStatus": "RISK_CONFLICT",
  "conflictCount": 1,
  "conflicts": [
    {
      "gridId": "G-05-07",
      "levelId": "L120",
      "slotStart": "2026-06-08 10:10:00",
      "slotEnd": "2026-06-08 10:15:00",
      "conflictType": "ADJACENT_GRID_RISK",
      "description": "相邻网格已有模拟任务，建议人工复核"
    }
  ]
}
```

### 14.2 RealSkyGridClient

后续对接真实 SkyGrid：

```http
POST /api/occupancy/check
POST /api/bookings
GET /api/bookings/{id}
```

如果真实 SkyGrid 接口不同，请在 `docs/api-design.md` 记录映射关系。

---

## 15. 前端开发要求

前端至少包含 5 个页面。

### 15.1 任务创建页

功能：

- 选择地图；
- 选择起点；
- 选择终点；
- 选择高度层；
- 选择起飞时间；
- 选择任务类型；
- 选择算法；
- 是否规避风险；
- 是否连接 SkyGrid；
- 点击开始规划。

### 15.2 航线规划展示页

展示：

- 网格地图；
- 起点；
- 终点；
- 禁飞区；
- 障碍物；
- 风险区；
- 规划航线；
- 路径节点序列；
- 距离；
- 耗时；
- 转弯次数；
- 能耗估计。

### 15.3 风险评估页

展示：

- riskScore；
- riskLevel；
- riskFactors；
- risk grid 列表；
- 能耗安全性；
- 安全建议。

### 15.4 算法对比页

展示：

- Dijkstra；
- A*；
- Theta*；
- 路径长度对比；
- 规划耗时对比；
- 转弯次数对比；
- 风险评分对比。

### 15.5 SkyGrid 联动页

展示：

- TimeSlot 占用表；
- 冲突检测结果；
- 冲突点高亮；
- 一键提交预约；
- 预约状态。

---

## 16. 视觉规则

网格地图建议使用 Canvas 或 SVG。

颜色建议：

```text
起点：绿色
终点：蓝色
航线：亮色高亮
禁飞区：红色
障碍物：深灰色
风险区：橙色
冲突点：红色边框或闪烁
普通网格：浅灰色
```

前端目标：

```text
让评委一眼看出这不是普通表格系统，而是低空航线规划与空域资源占用系统。
```

---

## 17. 测试要求

### 17.1 Python 单元测试

必须覆盖：

```text
grid_id
map_loader
dijkstra
astar
theta_star
direction_group
symmetry_transformer
risk_evaluator
energy_estimator
timeslot_converter
```

运行命令：

```bash
cd algorithm-service
pytest -q
```

### 17.2 API 测试

启动：

```bash
cd algorithm-service
uvicorn app.main:app --reload --port 8001
```

测试：

```bash
curl http://localhost:8001/health
```

### 17.3 Java 测试

运行：

```bash
cd route-adapter-service
mvn test
```

### 17.4 前端运行

```bash
cd frontend
npm install
npm run dev
```

---

## 18. 开发阶段

### Phase 0：初始化

目标：

- 创建仓库结构；
- 创建 README；
- 创建 algorithm-service；
- 跑通 FastAPI `/health`；
- 创建 demo-city-20x20.json。

验收：

```text
uvicorn app.main:app --reload --port 8001 能启动
GET /health 返回 UP
```

### Phase 1：地图与 A*

目标：

- 完成 grid_id；
- 完成 map_loader；
- 完成 graph_builder；
- 完成 A*；
- 完成 `/api/plan`；
- 能绕开禁飞区和障碍物。

验收：

```text
POST /api/plan 返回 path
path 不包含禁飞区和障碍物
pytest 通过
```

### Phase 2：Dijkstra + Theta* + 算法对比

目标：

- 完成 Dijkstra；
- 完成 Theta* 简化版；
- 完成 `/api/plan/compare`；
- 返回 distance、turnCount、planningTimeMs。

验收：

```text
算法对比接口可用
前端或 Swagger 能看到三种算法结果
```

### Phase 3：风险与能耗

目标：

- 完成 risk_evaluator；
- 完成 risk_explainer；
- 完成 energy_estimator；
- 接入规划结果。

验收：

```text
/api/plan 返回 riskScore、riskLevel、riskFactors、estimatedBatteryUsage
```

### Phase 4：群论增强

目标：

- 完成 C8 direction_group；
- 将 turn_cost 接入 A*；
- 完成 D4 symmetry_transformer；
- 完成 D4 symmetry benchmark；
- 完成 group-theory-module.md。

验收：

```text
pytest tests/test_direction_group.py 通过
pytest tests/test_symmetry_transformer.py 通过
POST /api/benchmark/symmetry 返回增强实验结果
```

### Phase 5：TimeSlot 转换

目标：

- 完成 timeslot_converter；
- 完成 `/api/timeslot/convert`；
- 输出 occupancyUnits。

验收：

```text
给定 path + startTime，能输出 Grid + Level + TimeSlot 占用序列
```

### Phase 6：route-adapter-service

目标：

- 创建 Spring Boot 服务；
- 创建任务表；
- 调用 algorithm-service；
- 保存任务和规划结果；
- 实现 MockSkyGridClient。

验收：

```text
POST /api/tasks 创建任务
POST /api/tasks/{id}/plan 调用 Python 并保存结果
POST /api/tasks/{id}/check-conflict 返回 mock 冲突结果
```

### Phase 7：frontend

目标：

- 创建 Vue 3 前端；
- 完成任务创建页；
- 完成航线展示页；
- 完成风险评估页；
- 完成算法对比页；
- 完成 SkyGrid 联动页。

验收：

```text
可以通过页面创建任务、查看航线、查看风险、查看算法对比、查看冲突结果
```

### Phase 8：Docker Compose 与文档

目标：

- 写 docker-compose.yml；
- 写 README；
- 写 docs；
- 补充截图；
- 补充复试问答。

验收：

```text
按 README 能启动项目
文档能解释项目价值、架构、算法、群论增强、演示流程
```

---

## 19. README 必须包含

README 至少包含：

```text
1. 项目简介
2. 项目架构图
3. 与 SkyGrid 的关系
4. 核心功能
5. 技术栈
6. 快速启动
7. API 示例
8. 算法说明
9. 群论增强模块说明
10. 演示截图
11. 测试命令
12. 复试项目介绍
```

---

## 20. 复试表达重点

最终项目要能这样介绍：

```text
我围绕低空技术与工程方向做了两个互补项目。SkyGrid 负责低空空域资源的预约、审批、冲突检测和微服务治理；LowAlt-RouteLab 负责低空无人机航线规划和风险评估。LowAlt-RouteLab 将低空环境建模为 Grid + Level + TimeSlot，支持禁飞区、障碍物、风险区和已有占用约束下的 A* / Theta* 路径规划，并引入 C8 离散航向群计算转弯代价、D4 二面体群进行网格对称变换和测试增强。系统最终能把规划路径转换为 SkyGrid 可识别的占用时间片，完成从航线生成到预约审批和冲突检测的完整闭环。
```

---

## 21. 不要做的事情

Codex 开发时不要做以下事情：

1. 不要接真实无人机飞控。
2. 不要接 ROS2。
3. 不要一开始上 Cesium 3D。
4. 不要把项目变成纯可视化大屏。
5. 不要把群论写成项目主线。
6. 不要引入过多中间件导致项目跑不起来。
7. 不要依赖真实 SkyGrid 才能演示。
8. 不要只写接口不写测试。
9. 不要只写 README 不写可运行代码。
10. 不要生成大量无用样板代码。

---

## 22. 最终验收清单

项目完成时必须满足：

```text
[ ] algorithm-service 能独立启动
[ ] /health 正常
[ ] demo-city-20x20 地图可加载
[ ] /api/plan 可返回 A* 路径
[ ] 路径能绕开禁飞区和障碍物
[ ] Dijkstra / A* / Theta* 可对比
[ ] C8 转弯代价可测试
[ ] D4 地图对称变换可测试
[ ] D4 symmetry benchmark 可运行
[ ] riskScore 和 riskFactors 可返回
[ ] energy estimate 可返回
[ ] path 可转换为 TimeSlot 占用序列
[ ] route-adapter-service 可创建任务并调用 algorithm-service
[ ] MockSkyGridClient 可返回冲突结果
[ ] frontend 可展示网格、航线、风险和冲突
[ ] README 完整
[ ] docs 完整
[ ] pytest 通过
[ ] Java 单元测试通过
[ ] 前端能启动
[ ] Docker Compose 可选但建议完成
```

---

## 23. 给 Codex 的第一条开发指令建议

如果用户让你开始开发，请从这里开始：

```text
请先初始化 LowAlt-RouteLab 仓库结构，优先实现 algorithm-service。第一步完成 FastAPI 项目骨架、/health 接口、demo-city-20x20.json 地图文件、grid_id 工具、map_loader，并补充 pytest 测试。不要先写前端，不要先写 Java 服务。
```

---

## 24. 给 Codex 的第二条开发指令建议

当 Phase 0 完成后继续：

```text
请在 algorithm-service 中实现 A* 路径规划，支持 8 邻接、禁飞区绕行、障碍物绕行、基础风险代价，并提供 POST /api/plan 接口。要求补充 test_astar.py，确保路径不经过禁飞区和障碍物。
```

---

## 25. 给 Codex 的第三条开发指令建议

当 A* 完成后继续：

```text
请实现 C8 离散航向群 direction_group.py，并把转弯代价接入 A* cost_model。然后实现 D4 二面体群 symmetry_transformer.py，用于地图和任务的旋转/反射变换。要求补充完整测试，验证 ROTATE_90 连续四次回到原点、FLIP 连续两次回到原点、C8 转弯步数计算正确。
```

---

## 26. 最终目标

本项目最终要证明：

```text
我不仅能做 Java 后端平台，还能围绕低空技术与工程方向，把无人机航线规划、风险评估、离散空域资源占用、冲突检测和数学建模增强整合成一个可运行、可展示、可测试的工程项目。
```
