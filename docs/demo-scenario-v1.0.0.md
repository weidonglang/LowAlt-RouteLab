# LowAlt-RouteLab v1.0.0 Demo Scenario

## Scenario

Urban east-district inspection:

```text
Start: G-02-03
End: G-16-14
Level: L120
Algorithm: A*
Mode: mock by default, real when SkyGrid is running
```

## Flow

```text
Load scenario
  -> Generate route
  -> Evaluate risk
  -> Estimate energy
  -> Convert to TimeSlot occupancy
  -> Check SkyGrid conflict
  -> Submit SkyGrid booking
  -> Read conflict suggestions or booking status
```

## Commands

Algorithm and benchmark:

```bat
cd algorithm-service
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_benchmark.py
```

Adapter:

```bat
cd route-adapter-service
mvn test
```

Frontend:

```bat
cd frontend
npm.cmd run build
```

Real SkyGrid demo:

```bat
scripts\run-real-skygrid-demo.bat
```

## Evidence

Benchmark summaries:

```text
algorithm-service/benchmarks/results/benchmark-summary.json
algorithm-service/benchmarks/results/benchmark-summary.csv
```

Visualization assets:

```text
assets/diagrams/algorithm-comparison.png
assets/diagrams/risk-score-comparison.png
assets/diagrams/energy-cost-comparison.png
```

## Limitations

- The benchmark uses demo-scale `demo-city-20x20` scenarios.
- Real SkyGrid mode requires SkyGrid to be started separately.
