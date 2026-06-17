# LowAlt-RouteLab Performance Report

## Scope

LowAlt v0.6.0 uses the algorithm benchmark as its primary performance evidence.

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

## 2026-06-17 Summary

| Algorithm | Success Rate | Avg Path Length | Avg Planning Time ms |
|---|---:|---:|---:|
| A_STAR | 0.8 | 2068.503 | 6.25 |
| A_STAR_RISK_PENALTY | 0.8 | 2068.503 | 6.25 |
| DIJKSTRA | 0.8 | 2068.503 | 84 |
| THETA_STAR | 0.8 | 2008.17 | 6.25 |
| THETA_STAR_RISK_PENALTY | 0.8 | 2008.17 | 6.5 |

## Validation Note

The benchmark uses demo-scale 20x20 scenarios. It provides repeatable local comparison evidence, not real-world UAV performance claims.
