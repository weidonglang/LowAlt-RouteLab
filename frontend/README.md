# frontend

LowAlt-RouteLab 的 Vue 3 前端工作台。

## 功能页面

- 任务创建
- 航线规划展示
- 风险评估
- 算法对比
- SkyGrid 联动

## 运行

先启动后端：

```bash
cd ../algorithm-service
uvicorn app.main:app --reload --port 8001
```

```bash
cd ../route-adapter-service
mvn spring-boot:run
```

启动前端：

```bash
npm install
npm run dev
```

访问：

```text
http://127.0.0.1:5173/
```

## 构建

```bash
npm run build
```

