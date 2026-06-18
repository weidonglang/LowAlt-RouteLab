# LowAlt-RouteLab Algorithm Benchmark v1.0.0

## Scope

The benchmark compares route planning behavior across five low-altitude scenarios:

- `simple_open_area`
- `risk_avoidance_area`
- `dense_obstacle_area`
- `narrow_corridor_area`
- `long_distance_patrol`

Compared cases:

- Dijkstra
- A*
- Theta*
- A* with risk penalty
- Theta* with risk penalty

## Metrics

- Path Length
- Turn Count
- Risk Cells Passed
- Risk Score
- Energy Cost
- Planning Time
- Success Rate
- TimeSlot Count

## Run

```bat
cd /d E:\javacode\LowAlt-RouteLab\algorithm-service
.\.venv\Scripts\python.exe scripts\run_benchmark.py
```

The script calls the FastAPI app through `TestClient`, so it does not require a running uvicorn process.

## Output

```text
algorithm-service/benchmarks/results/benchmark-summary.json
algorithm-service/benchmarks/results/benchmark-summary.csv
```

## 2026-06-18 Summary

| Algorithm | Success Rate | Avg Path Length | Avg Turn Count | Avg Risk Score | Avg Energy Cost | Avg Planning Time ms | Avg TimeSlot Count |
|---|---:|---:|---:|---:|---:|---:|---:|
| A_STAR | 1.0 | 1759.655 | 1.2 | 0.1994 | 10.918 | 8.8 | 15.2 |
| A_STAR_RISK_PENALTY | 1.0 | 1759.655 | 1.2 | 0.1984 | 10.918 | 9.0 | 15.2 |
| DIJKSTRA | 1.0 | 1759.655 | 1.2 | 0.1984 | 10.918 | 105.8 | 15.2 |
| THETA_STAR | 1.0 | 1706.536 | 0.6 | 0.2356 | 10.419 | 8.8 | 2.6 |
| THETA_STAR_RISK_PENALTY | 1.0 | 1706.536 | 0.6 | 0.2356 | 10.419 | 8.4 | 2.6 |

Generated diagrams:

```text
assets/diagrams/algorithm-comparison.png
assets/diagrams/risk-score-comparison.png
assets/diagrams/energy-cost-comparison.png
assets/diagrams/timeslot-comparison.png
```

## Notes

The benchmark reports demo-scale behavior on `demo-city-20x20`. It is intended for engineering comparison and release evidence, not for claiming real-world UAV performance.
