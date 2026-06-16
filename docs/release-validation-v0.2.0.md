# LowAlt-RouteLab v0.2.0 Validation

## Date

2026-06-16, Asia/Shanghai

## Environment

- OS: Windows 11 amd64
- JDK: Eclipse Temurin 17.0.18
- Maven: 3.9.10
- Node.js: 24.15.0
- npm: 11.12.1
- Python: 3.12.13 from `algorithm-service\.venv`

## Commands

```bat
cd /d E:\javacode\LowAlt-RouteLab

cd algorithm-service
.\.venv\Scripts\python.exe -m pytest -q
cd ..

cd route-adapter-service
mvn test
cd ..

cd frontend
npm.cmd run build
cd ..

scripts\run-real-skygrid-demo.bat
```

## Results

| Command | Result | Notes |
|---|---|---|
| `algorithm-service pytest -q` | Passed | 59 tests passed. Pytest reported a local cache write warning under `.pytest_cache`, but tests completed successfully. |
| `route-adapter-service mvn test` | Passed | 13 tests passed, covering mock client, real client config, factory, HTTP mapping, route task flow, route-to-booking mapping, and the `L120 -> levelId 2` SkyGrid mapping. |
| `frontend npm.cmd run build` | Passed | Vue type check and Vite build completed. Vite reported existing pure annotation and large chunk warnings. |
| `scripts\run-real-skygrid-demo.bat` | Failed due to environment | route-adapter-service was not running at `127.0.0.1:8081`, so the script stopped before creating the route task. |

## Verified v0.2.0 Changes

- Added `skygrid.mode=mock|real` configuration.
- Kept mock mode as the default path.
- Added `RealSkyGridClient` for SkyGrid Gateway calls.
- Added clear real-mode errors for unavailable Gateway, missing token, conflict responses, service errors, and request failures.
- Added `SkyGridBookingRequest`, `SkyGridOccupancySlot`, `TimeSlotOccupancyMapper`, and `RoutePlanToSkyGridBookingMapper`.
- Aligned LowAlt altitude labels with SkyGrid demo seed levels for the first real integration path: `L90` and `L120` map to level id `2`, and `L150` maps to level id `3`.
- Updated `RouteTaskService` to map route plans into a booking request before conflict check and submit.
- Added the East District inspection demo scenario.
- Added real SkyGrid integration demo scripts.

## Known Limitations

- The real integration demo was not executed end-to-end because local LowAlt and SkyGrid services were not running.
- SkyGrid v0.2.0 still accepts bookings through its existing route-template based API, so LowAlt maps route occupancy into that contract and stores richer route metadata in the description field.
- Real integration tests do not run against a live SkyGrid by default; HTTP behavior is covered by `MockRestServiceServer` unit tests.
