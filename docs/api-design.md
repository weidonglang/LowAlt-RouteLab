# API 设计

所有服务返回统一结构：

```json
{
  "code": 200,
  "message": "success message",
  "data": {}
}
```

## algorithm-service

默认地址：

```text
http://127.0.0.1:8001
```

### 健康检查

```http
GET /health
```

### 获取地图

```http
GET /api/maps/demo-city-20x20
```

### 路径规划

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

支持算法：

```text
DIJKSTRA
A_STAR
THETA_STAR
```

响应核心字段：

```json
{
  "success": true,
  "algorithm": "A_STAR",
  "path": ["G-01-01", "G-02-01"],
  "distance": 2321.32,
  "estimatedTimeSeconds": 232,
  "turnCount": 1,
  "planningTimeMs": 4,
  "visitedCount": 47,
  "riskScore": 0.254,
  "riskLevel": "MEDIUM",
  "riskFactors": ["path is within 1 grid of a no-fly zone"],
  "estimatedBatteryUsage": 14.228,
  "batteryLimit": 80.0,
  "energySafe": true
}
```

### 算法对比

```http
POST /api/plan/compare
```

### TimeSlot 转换

```http
POST /api/timeslot/convert
```

请求：

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

响应：

```json
{
  "occupancyUnits": [
    {
      "gridId": "G-01-01",
      "levelId": "L120",
      "slotStart": "2026-06-08T10:00:00",
      "slotEnd": "2026-06-08T10:05:00",
      "sequenceNo": 1
    }
  ]
}
```

### D4 对称性实验

```http
POST /api/benchmark/symmetry
```

## route-adapter-service

默认地址：

```text
http://127.0.0.1:8081
```

### 创建任务

```http
POST /api/tasks
```

请求：

```json
{
  "taskName": "demo task",
  "taskType": "POWER_LINE_INSPECTION",
  "startGrid": "G-01-01",
  "endGrid": "G-18-16",
  "startLevel": "L120",
  "startTime": "2026-06-08T10:00:00",
  "algorithm": "A_STAR"
}
```

### 执行规划

```http
POST /api/tasks/{taskId}/plan
```

该接口会：

1. 调用 Python `/api/plan`。
2. 调用 Python `/api/timeslot/convert`。
3. 保存规划快照和占用序列。

### 检查冲突

```http
POST /api/tasks/{taskId}/check-conflict
```

当前返回 `MockSkyGridClient` 的模拟冲突。

### 提交 SkyGrid

```http
POST /api/tasks/{taskId}/submit-skygrid
```

当前返回 mock booking ID。

### 查询任务

```http
GET /api/tasks/{taskId}
```

