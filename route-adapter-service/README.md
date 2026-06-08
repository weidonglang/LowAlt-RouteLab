# route-adapter-service

LowAlt-RouteLab 的 Java 适配服务，负责连接前端、Python `algorithm-service` 和 SkyGrid。

当前阶段使用内存存储和 `MockSkyGridClient`，保证没有 MySQL、Redis、真实 SkyGrid 时也能演示。

## 运行

先启动 Python 算法服务：

```bash
cd ../algorithm-service
uvicorn app.main:app --reload --port 8001
```

再启动 Java 适配服务：

```bash
mvn spring-boot:run
```

默认端口：

```text
http://localhost:8081
```

## API

创建任务：

```bash
curl -X POST http://localhost:8081/api/tasks \
  -H "Content-Type: application/json" \
  -d "{\"taskName\":\"demo task\",\"taskType\":\"POWER_LINE_INSPECTION\",\"startGrid\":\"G-01-01\",\"endGrid\":\"G-18-16\",\"startLevel\":\"L120\",\"startTime\":\"2026-06-08T10:00:00\",\"algorithm\":\"A_STAR\"}"
```

执行规划：

```bash
curl -X POST http://localhost:8081/api/tasks/1/plan
```

检查 Mock SkyGrid 冲突：

```bash
curl -X POST http://localhost:8081/api/tasks/1/check-conflict
```

提交 Mock SkyGrid：

```bash
curl -X POST http://localhost:8081/api/tasks/1/submit-skygrid
```

查询任务：

```bash
curl http://localhost:8081/api/tasks/1
```

## 测试

```bash
mvn test
```

