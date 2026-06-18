# LowAlt-RouteLab Performance Report

## Scope

LowAlt v1.0.0 uses the algorithm benchmark as its primary performance evidence.

## Run

```bat
cd /d E:\javacode\LowAlt-RouteLab\algorithm-service
.\.venv\Scripts\python.exe scripts\run_benchmark.py
```

## Output

```text
algorithm-service/benchmarks/results/benchmark-summary.json
algorithm-service/benchmarks/results/benchmark-summary.csv
```

## Metrics

- Path Length
- Turn Count
- Risk Cells Passed
- Risk Score
- Energy Cost
- Planning Time
- Success Rate
- TimeSlot Count

## 2026-06-18 Summary

| Algorithm | Success Rate | Avg Path Length | Avg Planning Time ms |
|---|---:|---:|---:|
| A_STAR | 1.0 | 1759.655 | 8.8 |
| A_STAR_RISK_PENALTY | 1.0 | 1759.655 | 9.0 |
| DIJKSTRA | 1.0 | 1759.655 | 105.8 |
| THETA_STAR | 1.0 | 1706.536 | 8.8 |
| THETA_STAR_RISK_PENALTY | 1.0 | 1706.536 | 8.4 |

## Validation Note

The benchmark uses demo-scale 20x20 scenarios. It provides repeatable local comparison evidence, not real-world UAV performance claims.
