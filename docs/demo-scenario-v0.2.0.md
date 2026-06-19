# LowAlt-RouteLab v0.2.0 Real SkyGrid Demo Scenario

## Scenario

- Task: East District UAV Inspection
- Map: `demo-city-20x20`
- Start grid: `G-02-03`
- End grid: `G-16-14`
- Altitude level: `L120`
- Start time: `2026-06-15T10:00:00`
- Algorithm: `A_STAR`
- Risk avoidance: enabled
- SkyGrid mode: `real`

The scenario file is stored at:

```text
algorithm-service/demo_scenarios/east_district_inspection.json
```

## Expected Flow

1. Create a LowAlt route task.
2. Call algorithm-service to generate an A* route.
3. Calculate risk score, energy cost, and TimeSlot occupancy.
4. Map the route plan into `SkyGridBookingRequest`.
5. Call SkyGrid Gateway for conflict pre-check.
6. Submit the booking request to SkyGrid.
7. Return the SkyGrid booking id to LowAlt.

## Run

Start SkyGrid first:

```bat
cd /d E:\javacode\low-altitude-platform
scripts\start-dev-stack.bat
scripts\check-dev-stack.bat
```

Start LowAlt services:

```bat
cd /d E:\javacode\LowAlt-RouteLab
scripts\start-dev.ps1
```

For real mode, route-adapter-service must be started with:

```text
skygrid.mode=real
skygrid.base-url=http://127.0.0.1:8080
skygrid.token=<dev token>
```

Run the demo:

```bat
scripts\run-real-skygrid-demo.bat
```

## Success Output

```text
Route task created: OK
Route planned: OK
Risk evaluated: OK
TimeSlot converted: OK
SkyGrid conflict checked: OK
Booking submitted: OK
Demo completed successfully.
```

## Current Limitation

The v0.2.0 real demo uses SkyGrid's current booking API, which accepts `routeTemplateId`, `levelId`, `bookingDate`, and `timeSlotIds`. LowAlt therefore maps route occupancy metadata into that existing booking contract while preserving richer route metadata in the booking description.
