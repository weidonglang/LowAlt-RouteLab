# Changelog

本项目遵循语义化版本风格记录重要变更。

## [Unreleased]

- 补充与 SkyGrid 的低空项目群闭环叙事。
- 新增项目边界文档，明确 LowAlt-RouteLab 和 SkyGrid 的职责划分。
- 新增算法实验评估报告，记录 Dijkstra、A*、Theta* 的路径长度、风险、能耗和耗时对比。
- 新增风险模型设计文档和 TimeSlot 占用转换设计文档。
- 新增 v0.1.0 发布检查清单和验证记录。
- 补充截图和图表采集清单。

## [0.1.0] - 2026-06-14

- 完成 20x20 城市低空地图、禁飞区、障碍物和风险区建模。
- 完成 Dijkstra、A*、Theta* 航线规划。
- 完成 C8 转弯代价和 D4 对称增强实验。
- 完成风险评分、风险解释和简化能耗估计。
- 完成路径到 `Grid + Level + TimeSlot` 占用序列转换。
- 完成 Java route-adapter-service 与 `MockSkyGridClient` 联动。
- 完成 Vue 3 前端工作台、算法对比和 SkyGrid mock 联动展示。
