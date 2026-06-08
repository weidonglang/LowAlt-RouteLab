# algorithm-service

LowAlt-RouteLab 的 Python 算法服务，当前阶段提供 FastAPI 启动入口、健康检查、demo 地图加载、Grid ID 工具、地图索引查询、A* / Dijkstra / Theta* 路径规划、基础风险评估和简化能耗估计。

## 运行

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

健康检查：

```bash
curl http://localhost:8001/health
```

地图接口：

```bash
curl http://localhost:8001/api/maps/demo-city-20x20
```

路径规划：

```bash
curl -X POST http://localhost:8001/api/plan \
  -H "Content-Type: application/json" \
  -d "{\"mapId\":\"demo-city-20x20\",\"taskType\":\"POWER_LINE_INSPECTION\",\"startGrid\":\"G-01-01\",\"endGrid\":\"G-18-16\",\"level\":\"L120\",\"algorithm\":\"A_STAR\",\"avoidRisk\":true,\"allowDiagonal\":true}"
```

算法对比：

```bash
curl -X POST http://localhost:8001/api/plan/compare \
  -H "Content-Type: application/json" \
  -d "{\"mapId\":\"demo-city-20x20\",\"startGrid\":\"G-01-01\",\"endGrid\":\"G-18-16\",\"level\":\"L120\",\"algorithms\":[\"DIJKSTRA\",\"A_STAR\",\"THETA_STAR\"]}"
```

D4 对称性实验：

```bash
curl -X POST http://localhost:8001/api/benchmark/symmetry \
  -H "Content-Type: application/json" \
  -d "{\"mapId\":\"demo-city-20x20\",\"benchmarkTaskFile\":\"benchmark_tasks.json\",\"algorithms\":[\"A_STAR\"],\"transforms\":[\"IDENTITY\",\"ROTATE_90\"]}"
```

TimeSlot 转换：

```bash
curl -X POST http://localhost:8001/api/timeslot/convert \
  -H "Content-Type: application/json" \
  -d "{\"path\":[\"G-01-01\",\"G-01-02\",\"G-02-03\"],\"level\":\"L120\",\"startTime\":\"2026-06-08 10:00:00\",\"speed\":10.0,\"gridSizeMeters\":100,\"slotMinutes\":5}"
```

规划响应核心字段：

- `path`：规划网格序列
- `distance`：路径距离，单位米
- `turnCount`：转弯次数
- `riskScore` / `riskLevel` / `riskFactors`：风险评分、等级和解释
- `estimatedBatteryUsage` / `batteryLimit` / `energySafe`：简化能耗估计

## 测试

```bash
pytest -q
```
