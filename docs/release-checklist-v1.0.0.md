# LowAlt-RouteLab v1.0.0 Release Checklist

## Code

- [x] Algorithm service supports Dijkstra, A*, Theta*, risk scoring, energy estimate, and TimeSlot conversion.
- [x] Route adapter supports mock and real SkyGrid client modes.
- [x] Demo scenarios and benchmark scenarios are included.
- [x] Docker Compose and public configuration examples are included.

## Validation

- [x] `cd algorithm-service && .\.venv\Scripts\python.exe -m pytest -q`
- [x] `cd algorithm-service && .\.venv\Scripts\python.exe scripts\run_benchmark.py`
- [x] `cd route-adapter-service && mvn test`
- [x] `cd frontend && npm.cmd run build`
- [ ] `scripts\run-real-skygrid-demo.bat` - blocked until route-adapter-service and SkyGrid Gateway are running.

## Documentation

- [x] Architecture, risk model, TimeSlot conversion, benchmark, demo scenario, Docker deployment, and SkyGrid integration docs exist.
- [x] Benchmark JSON/CSV result files are committed.
- [x] Generated benchmark diagrams are committed.
- [x] Known limitations are recorded honestly.

## Release Rule

Do not tag `v1.0.0` until the validation commands have been run in the target environment and recorded in `docs/release-validation-v1.0.0.md`.
