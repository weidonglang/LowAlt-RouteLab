# LowAlt-RouteLab Demo Scenarios

Demo scenario files are stored in:

```text
algorithm-service/demo_scenarios
```

Available scenarios:

- `east_district_inspection.json`: v0.2.0 real SkyGrid integration scenario.
- `risk_avoidance_demo.json`: route planning with risk avoidance enabled.
- `hard_conflict_replan_demo.json`: expected SkyGrid hard conflict and suggestion flow.
- `long_distance_patrol.json`: long-distance Theta* patrol scenario.

These files are used by demo scripts and can also be submitted directly to route-adapter-service:

```text
POST /api/tasks
POST /api/tasks/{taskId}/plan
POST /api/tasks/{taskId}/check-conflict
POST /api/tasks/{taskId}/submit-skygrid
POST /api/tasks/{taskId}/conflict-suggestions
```
