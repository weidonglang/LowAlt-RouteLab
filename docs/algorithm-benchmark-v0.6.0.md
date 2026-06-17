# LowAlt-RouteLab Algorithm Benchmark v0.6.0

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

## 2026-06-17 Summary

| Algorithm | Success Rate | Avg Path Length | Avg Turn Count | Avg Risk Score | Avg Energy Cost | Avg Planning Time ms | Avg TimeSlot Count |
|---|---:|---:|---:|---:|---:|---:|---:|
| A_STAR | 0.8 | 2068.503 | 1.25 | 0.198 | 12.786 | 6.25 | 17.75 |
| A_STAR_RISK_PENALTY | 0.8 | 2068.503 | 1.25 | 0.198 | 12.786 | 6.25 | 17.75 |
| DIJKSTRA | 0.8 | 2068.503 | 1.25 | 0.198 | 12.786 | 84 | 17.75 |
| THETA_STAR | 0.8 | 2008.17 | 0.75 | 0.2592 | 12.2737 | 6.25 | 2.75 |
| THETA_STAR_RISK_PENALTY | 0.8 | 2008.17 | 0.75 | 0.2592 | 12.2737 | 6.5 | 2.75 |

## Notes

The benchmark reports demo-scale behavior on `demo-city-20x20`. It is intended for engineering comparison and release evidence, not for claiming real-world UAV performance.
