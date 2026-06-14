# LowAlt-RouteLab 与 SkyGrid 项目边界

本文档说明 LowAlt-RouteLab 在低空项目群中的职责，以及它与 SkyGrid 的数据交接方式。

## 项目群闭环

```text
LowAlt-RouteLab
航线规划 / 风险评估 / 能耗估计 / TimeSlot 转换
        ↓
SkyGrid
空域预约 / 审批流转 / 冲突检测 / 占用记录 / 消息通知 / 监控治理
```

LowAlt-RouteLab 解决“任务应该怎么飞”的问题，SkyGrid 解决“这段空域能不能被占用、如何审批和审计”的问题。

## LowAlt-RouteLab 的边界

LowAlt-RouteLab 负责算法仿真和占用转换。

- 根据起点、终点、高度层、任务类型生成航线。
- 在禁飞区、障碍物和风险区约束下规划路径。
- 对比 Dijkstra、A*、Theta* 的路径质量和规划耗时。
- 计算路径风险、转弯代价和简化能耗。
- 将路径转换为 `Grid + Level + TimeSlot` 占用序列。
- 通过 `MockSkyGridClient` 演示 SkyGrid 冲突检查和提交动作。

LowAlt-RouteLab 不负责真实审批、真实资源锁定、消息通知、服务治理和审计留痕。

## SkyGrid 的边界

SkyGrid 负责空域资源治理。

- 管理低空资源模型：`Grid + Level + TimeSlot + Date`。
- 接收预约申请。
- 检查硬冲突、禁飞区、风险网格和相邻风险。
- 审批通过后写入 `resource_occupancy`。
- 通过 Outbox、RabbitMQ 和补偿任务保证通知最终一致。
- 写入通知记录、审计日志和幂等消费记录。
- 展示监控、队列、限流、降级和重试状态。

SkyGrid 不负责生成最优路径，也不比较路径算法。

## 交付给 SkyGrid 的数据

LowAlt-RouteLab 输出给 SkyGrid 的关键数据是占用序列。

| 字段 | 含义 | 示例 |
| --- | --- | --- |
| `gridCode` | 网格编号 | `G-01-02` |
| `levelCode` | 高度层 | `L120` |
| `startTime` | 占用开始时间 | `2026-06-08T10:05:00` |
| `endTime` | 占用结束时间 | `2026-06-08T10:10:00` |
| `slotCode` | 离散时间片 | `T-002` |

SkyGrid 根据这些占用单元判断是否存在同一日期、同一网格、同一高度层、同一时间片的重叠。

## 当前实现状态

当前仓库通过 `MockSkyGridClient` 模拟 SkyGrid，保证算法项目可以单独运行和演示。真实接入时，适配层应将 mock 调用替换为 SkyGrid Gateway API：

```text
route-adapter-service
  → SkyGrid Gateway
  → booking-service conflict pre-check
  → booking approval workflow
```

这样可以保持算法服务和治理平台解耦。
