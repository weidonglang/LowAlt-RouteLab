# LowAlt-RouteLab v0.1.0 验证记录

验证日期：2026-06-14

本文档记录 v0.1.0 封版前的测试、构建和验收命令执行结果。未执行或失败的项目必须说明原因，不伪造通过结果。

## 环境

| 项目 | 要求 |
| --- | --- |
| Python | 3.10+ |
| Java | 17+ |
| Maven | 3.9+ |
| Node.js | 18+ |
| npm | 9+ |

## 验证命令

| 命令 | 状态 | 结果 |
| --- | --- | --- |
| `cd algorithm-service; pytest -q` | 待执行 | 待更新 |
| `cd route-adapter-service; mvn test` | 待执行 | 待更新 |
| `cd frontend; npm run build` | 待执行 | 待更新 |

## 算法验收点

| 验收点 | 状态 | 说明 |
| --- | --- | --- |
| `/health` 正常返回 | 待验证 | 由 `test_api.py` 覆盖 |
| `demo-city-20x20` 加载 400 个网格 | 待验证 | 由地图测试覆盖 |
| A* 能生成从 `G-01-01` 到 `G-18-16` 的路径 | 待验证 | 由 API 测试覆盖 |
| Dijkstra / A* / Theta* 对比接口正常 | 待验证 | 由 API 测试覆盖 |
| TimeSlot 转换返回占用单元 | 待验证 | 由 API 和 converter 测试覆盖 |
| SkyGrid mock 检查和提交链路可演示 | 待验证 | 需要 Java 适配服务 |

## 已知限制

- 本文档会在实际执行测试命令后更新。
- 当前截图目录只包含采集清单，真实截图需在前端运行后补充。
- 真实 SkyGrid 集成仍由 `MockSkyGridClient` 模拟。

