# LowAlt-RouteLab v0.6.0 Validation

## Date

2026-06-17, Asia/Shanghai

## Environment

- OS: Windows 11 amd64
- Python: project virtualenv
- JDK: Eclipse Temurin 17.0.18
- Maven: 3.9.10
- Node.js: 24.15.0
- npm: 11.12.1

## Commands

```bat
cd /d E:\javacode\LowAlt-RouteLab\algorithm-service
.\.venv\Scripts\python.exe scripts\run_benchmark.py
.\.venv\Scripts\pytest.exe -q

cd /d E:\javacode\LowAlt-RouteLab\route-adapter-service
mvn test

cd /d E:\javacode\LowAlt-RouteLab\frontend
npm.cmd run build
```

## Results

| Command | Result | Notes |
|---|---|---|
| `scripts\run_benchmark.py` | Passed | Generated 25 benchmark cases across 5 scenarios and wrote JSON/CSV summaries. |
| `pytest -q` | Passed | 59 Python tests passed. Pytest emitted a cache-write warning in the sandbox. |
| `mvn test` | Passed | Route adapter service ran 13 tests successfully. |
| `npm.cmd run build` | Passed | Vite build completed with existing large chunk and pure annotation warnings. |

## Verified Changes

- Added benchmark scenarios for simple, risk-avoidance, dense-obstacle, narrow-corridor, and long-distance patrol cases.
- Added a benchmark runner that records success rate, path length, turns, risk, energy, planning time, and time-slot count.
- Added machine-readable benchmark summaries in JSON and CSV.
- Added demo scenarios for risk avoidance, hard conflict replan, and long-distance patrol.
- Added v0.6.0 benchmark and validation documentation.

## Known Limitations

- `simple_open_area` currently reports no path in the benchmark summary, so the aggregate success rate is 0.8 for each algorithm.
- Benchmark scenarios are demo-scale and should be treated as regression evidence, not operational flight-performance evidence.
