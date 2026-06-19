# LowAlt-RouteLab v1.0.0 Validation

## Date

2026-06-18, Asia/Shanghai

Live API retest: 2026-06-19, Asia/Shanghai

## Environment

- OS: Windows 11 amd64
- Python: 3.12.13
- JDK: Eclipse Temurin 17.0.18
- Maven: 3.9.10
- Node.js: 24.15.0
- npm: 11.12.1

## Commands

```bat
cd /d E:\javacode\LowAlt-RouteLab\algorithm-service
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_benchmark.py

cd ..\route-adapter-service
mvn test

cd ..\frontend
npm.cmd run build

cd ..
scripts\run-real-skygrid-demo.bat

git grep -n "sk-"
git grep -n -i "password\|secret\|token"
```

## Results

| Command | Result | Notes |
|---|---|---|
| `pytest -q` | Passed | 59 tests passed. Pytest emitted a cache-write warning for `.pytest_cache` permissions. |
| `scripts\run_benchmark.py` | Passed | Generated 25 cases across 5 scenarios. All algorithm summary success rates are 1.0 after correcting `simple_open_area` to use traversable `G-05-04`. |
| `mvn test` | Passed | Route adapter service ran 13 tests covering mock, real client config, real client mapping, task service, factory, and integration mapping. |
| `npm.cmd run build` | Passed | Vue/Vite build completed. Existing pure-annotation and large-chunk warnings remain. |
| `scripts\run-real-skygrid-demo.bat` | Passed | Retested on 2026-06-19 with SkyGrid Gateway, Nacos, Redis, RabbitMQ, local MySQL, algorithm-service, and route-adapter-service running. Demo completed successfully and returned `bookingId=5`. |
| `git grep -n "sk-"` | Reviewed | No OpenAI-style secret key found. Matches were ordinary source/document strings. |
| `git grep -n -i "password\|secret\|token"` | Reviewed | Matches are configuration placeholders, `dev-token` examples, DTO fields, tests, and documentation. No production credential was identified. |

## Benchmark Summary

| Algorithm | Success Rate | Avg Path Length | Avg Risk Score | Avg Energy Cost | Avg Planning Time ms | Avg TimeSlot Count |
|---|---:|---:|---:|---:|---:|---:|
| A_STAR | 1.0 | 1759.655 | 0.1994 | 10.918 | 8.8 | 15.2 |
| A_STAR_RISK_PENALTY | 1.0 | 1759.655 | 0.1984 | 10.918 | 9.0 | 15.2 |
| DIJKSTRA | 1.0 | 1759.655 | 0.1984 | 10.918 | 105.8 | 15.2 |
| THETA_STAR | 1.0 | 1706.536 | 0.2356 | 10.419 | 8.8 | 2.6 |
| THETA_STAR_RISK_PENALTY | 1.0 | 1706.536 | 0.2356 | 10.419 | 8.4 | 2.6 |

## Verified Release Package

- Mock and real SkyGrid client modes are documented.
- Docker deployment, ports, benchmark, performance, demo scenario, release checklist, and validation docs are present.
- Benchmark JSON/CSV and generated PNG diagrams are present.
- Runtime screenshot targets are listed without fake screenshots.
- Real SkyGrid live API demo has been exercised end to end from task creation through booking submission.

## Known Limitations

- Real SkyGrid integration requires algorithm-service, route-adapter-service, and a running SkyGrid Gateway.
- Frontend screenshot capture still requires starting the SkyGrid and LowAlt frontend applications.
- Benchmark scenarios are demo-scale and are not real-world UAV performance claims.
