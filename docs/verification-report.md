# Verification Report

验收时间：2026-06-08

## 1. algorithm-service pytest

命令：

```bash
cd algorithm-service
..\.venv\Scripts\python.exe -m pytest -q
```

实际运行时使用命令：

```powershell
..\.venv\Scripts\python.exe -m pytest -q
```

结果：

```text
59 passed in 0.57s
```

结论：通过。

## 2. algorithm-service 核心接口

启动命令：

```bash
cd algorithm-service
uvicorn app.main:app --host 127.0.0.1 --port 8001
```

实际服务：

```text
http://127.0.0.1:8001
```

### GET /health

关键响应：

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

### POST /api/plan

请求算法：`A_STAR`

关键响应：

```json
{
  "code": 200,
  "message": "planned successfully",
  "data": {
    "success": true,
    "algorithm": "A_STAR",
    "distance": 2321.32,
    "turnCount": 1,
    "riskLevel": "MEDIUM",
    "energySafe": true
  }
}
```

### POST /api/plan/compare

请求算法：

```text
DIJKSTRA, A_STAR, THETA_STAR
```

关键响应：

```json
{
  "code": 200,
  "message": "compared successfully",
  "data": {
    "results": [
      { "success": true, "algorithm": "DIJKSTRA" },
      { "success": true, "algorithm": "A_STAR" },
      { "success": true, "algorithm": "THETA_STAR" }
    ]
  }
}
```

### POST /api/timeslot/convert

关键响应：

```json
{
  "code": 200,
  "message": "timeslot converted successfully",
  "data": {
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
}
```

### POST /api/benchmark/symmetry

关键响应：

```json
{
  "code": 200,
  "message": "symmetry benchmark completed",
  "data": {
    "taskCount": 5,
    "augmentedTaskCount": 10,
    "algorithms": [
      {
        "algorithm": "A_STAR",
        "successRate": 1.0,
        "distanceVarianceUnderD4": 0.0
      }
    ]
  }
}
```

结论：核心接口通过。

## 3. route-adapter-service mvn test

命令：

```bash
cd route-adapter-service
mvn test
```

结果：

```text
Tests run: 5, Failures: 0, Errors: 0, Skipped: 0
BUILD SUCCESS
```

结论：通过。

## 4. Java 调用 Python 与 MockSkyGridClient

启动服务：

```text
algorithm-service: http://127.0.0.1:8001
route-adapter-service: http://127.0.0.1:8081
```

验收流程：

```text
POST /api/tasks
POST /api/tasks/{id}/plan
POST /api/tasks/{id}/check-conflict
POST /api/tasks/{id}/submit-skygrid
```

关键结果：

```json
{
  "taskId": 1,
  "createStatus": "CREATED",
  "planStatus": "PLANNED",
  "algorithm": "A_STAR",
  "pathCount": 18,
  "occupancyCount": 18,
  "conflictStatus": "RISK_CONFLICT",
  "conflictCount": 1,
  "submitStatus": "MOCK_SUBMITTED",
  "bookingId": "MOCK-SG-1-1"
}
```

结论：通过。

## 5. frontend npm install / build

命令：

```bash
cd frontend
npm install
npm run build
```

结果：

```text
npm install: completed
npm run build: built successfully
```

已知提示：

- `npm audit` 报告 2 个 moderate vulnerabilities。未执行 `npm audit fix --force`，避免破坏依赖版本。
- Vite 提示 bundle chunk 大于 500 kB，主要来自 Element Plus 和 ECharts。MVP 阶段不影响运行。

结论：构建通过，存在非阻塞提示。

## 6. Docker Compose

命令：

```bash
docker compose up --build -d
```

结果：

```text
failed to fetch anonymous token from auth.docker.io: EOF
```

失败发生在拉取基础镜像 metadata 阶段：

- `python:3.12-slim`
- `node:24-alpine`
- `nginx:1.27-alpine`
- `eclipse-temurin:17-jre`
- `maven:3.9.10-eclipse-temurin-17`

结论：未完成启动。当前判断为 Docker Hub/Registry 网络访问问题，不是项目代码或 Compose 配置中的应用逻辑错误。

补充检查：

```bash
docker compose config
```

结果：Compose 配置可以正常解析，服务、端口、依赖和环境变量展开正确。

建议：

- 网络恢复后重新执行 `docker compose up --build -d`。
- 或预先 `docker pull` 所需基础镜像。
- 或配置 Docker 国内镜像源。

## 7. 综合结论

最终综合测试重新启动了三个本地服务：

```text
frontend: http://127.0.0.1:5173
algorithm-service: http://127.0.0.1:8001
route-adapter-service: http://127.0.0.1:8081
```

最终综合测试结果：

```text
algorithm-service pytest: 59 passed
route-adapter-service mvn test: Tests run: 5, Failures: 0, Errors: 0
frontend npm run build: built successfully
frontend page: HTTP 200
frontend -> algorithm proxy: HTTP 200
algorithm /api/plan/compare: 3 algorithm results
route-adapter-service task plan: PLANNED
TimeSlot occupancy count: 18
MockSkyGrid conflict status: RISK_CONFLICT
```

通过项：

- Python 单元测试。
- Python 核心 API。
- Java 单元测试。
- Java 调用 Python。
- MockSkyGridClient 冲突检查和提交。
- 前端依赖安装与构建。

已知问题：

- Docker Compose 因 Docker Hub token 获取 EOF 未能完成镜像构建。
- 前端存在非阻塞 bundle 体积提示。
- npm audit 有 2 个 moderate vulnerabilities，未做破坏性自动升级。
