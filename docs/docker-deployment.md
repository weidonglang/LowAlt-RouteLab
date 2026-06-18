# LowAlt-RouteLab Docker Deployment

## Development Stack

```bat
scripts\docker-start-dev.bat
```

Services:

- algorithm-service: `http://127.0.0.1:8001`
- route-adapter-service: `http://127.0.0.1:8081`
- frontend: `http://127.0.0.1:5173`

Stop:

```bat
scripts\docker-stop-dev.bat
```

## SkyGrid Modes

Mock mode:

```text
SKYGRID_MODE=mock
```

Real mode:

```text
SKYGRID_MODE=real
SKYGRID_BASE_URL=http://host.docker.internal:8080
SKYGRID_TOKEN=<dev token>
```

## Validation

```bat
cd algorithm-service
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe scripts\run_benchmark.py

cd ..\route-adapter-service
mvn test

cd ..\frontend
npm.cmd run build
```
