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
| `cd algorithm-service; pytest -q` | 通过 | 使用项目内 `.venv` 执行，`59 passed in 0.64s` |
| `cd route-adapter-service; mvn test` | 通过 | 临时设置 `JAVA_HOME=C:\Program Files\Java\jdk-17.0.18+8` 后执行，`Tests run: 5, Failures: 0, Errors: 0, Skipped: 0` |
| `cd frontend; npm run build` | 通过 | 先执行 `npm install` 补齐 `vue-tsc`，随后构建成功；存在大 chunk 警告 |

## 算法验收点

| 验收点 | 状态 | 说明 |
| --- | --- | --- |
| `/health` 正常返回 | 通过 | `test_api.py` 覆盖 |
| `demo-city-20x20` 加载 400 个网格 | 通过 | 地图 API 测试覆盖 |
| A* 能生成从 `G-01-01` 到 `G-18-16` 的路径 | 通过 | API 测试覆盖 |
| Dijkstra / A* / Theta* 对比接口正常 | 通过 | API 测试覆盖 |
| TimeSlot 转换返回占用单元 | 通过 | API 和 converter 测试覆盖 |
| SkyGrid mock 检查和提交链路可演示 | 通过 | Java 适配服务测试覆盖 `MockSkyGridClient` 和 `RouteTaskService` |

## 已知限制

- Python 测试使用项目内 `.venv`，该目录已加入 `.gitignore`，不会提交。
- Python 依赖安装时默认源超时，使用清华 PyPI 镜像完成安装：`-i https://pypi.tuna.tsinghua.edu.cn/simple`。
- Java 测试初次执行失败是因为系统 `JAVA_HOME` 指向 `D:\DevEnvManager\current\jdk`，该路径不可用；临时设置为本机 JDK 17 后通过。
- 前端初次构建失败是因为未安装依赖，执行 `npm install` 后 `vue-tsc -b && vite build` 通过。
- 当前截图目录只包含采集清单，真实截图需在前端运行后补充。
- 真实 SkyGrid 集成仍由 `MockSkyGridClient` 模拟。
