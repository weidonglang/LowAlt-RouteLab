# LowAlt-RouteLab v0.1.0 发布检查清单

版本标题：

```text
LowAlt-RouteLab v0.1.0 - UAV Route Planning and Risk Evaluation Simulator
```

## 发布定位

v0.1.0 是 LowAlt-RouteLab 的低空航线规划与风险评估封版版本，重点证明系统具备以下能力：

- 20x20 城市低空地图建模。
- Dijkstra、A*、Theta* 路径规划。
- C8 离散航向转弯代价。
- D4 对称增强 benchmark。
- 风险评分、风险解释和能耗估计。
- 路径到 `Grid + Level + TimeSlot` 占用序列转换。
- 通过 `MockSkyGridClient` 模拟 SkyGrid 冲突检查和预约提交。
- 与 SkyGrid 组成低空项目群闭环。

## 必备文档

| 文档 | 状态 |
| --- | --- |
| `README.md` | 已补项目群闭环 |
| `docs/project-boundary.md` | 已补 |
| `docs/architecture.md` | 已存在 |
| `docs/demo-script.md` | 已存在 |
| `docs/algorithm-evaluation-report.md` | 已补 |
| `docs/risk-model-design.md` | 已补 |
| `docs/timeslot-conversion-design.md` | 已补 |
| `docs/release-validation.md` | 待执行验证后更新 |

## 必备截图

| 截图 | 状态 |
| --- | --- |
| `assets/diagrams/algorithm-comparison.png` | 待补真实图 |
| `assets/diagrams/skygrid-integration.png` | 待补真实图 |
| `assets/screenshots/astar-vs-theta.png` | 待补真实截图 |
| `assets/screenshots/risk-heatmap.png` | 待补真实截图 |
| `assets/screenshots/timeslot-occupancy.png` | 待补真实截图 |

## 发布前验证命令

```powershell
cd algorithm-service
pytest -q
cd ..\route-adapter-service
mvn test
cd ..\frontend
npm run build
```

## GitHub Release 内容建议

```markdown
## Highlights

- Route planning with Dijkstra, A* and Theta* on a 20x20 low-altitude grid map.
- Risk-aware planning with no-fly zones, obstacles and risk zones.
- Risk score, risk factors and simplified energy estimation.
- TimeSlot occupancy conversion for SkyGrid integration.
- Mock SkyGrid conflict check and submission flow.
- Algorithm evaluation report with reproducible benchmark commands.

## Validation

See docs/release-validation.md.

## Known Limits

- SkyGrid integration currently uses MockSkyGridClient.
- Screenshots should be regenerated from a running local frontend.
```

## 发布前确认

- [ ] README 已说明与 SkyGrid 的关系。
- [ ] 算法实验报告已完成。
- [ ] 风险模型和 TimeSlot 设计文档已完成。
- [ ] 测试和构建结果已写入 `docs/release-validation.md`。
- [ ] 没有提交 `.env`、日志、构建产物或真实密钥。
- [ ] GitHub Release 标题和说明已准备。

