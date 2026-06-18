# LowAlt-RouteLab SkyGrid Integration Guide

## Modes

LowAlt supports two SkyGrid modes:

```text
mock: default mode, no external SkyGrid dependency
real: call SkyGrid Gateway APIs
```

Configuration:

```yaml
skygrid:
  mode: mock
  base-url: http://127.0.0.1:8080
  token: dev-token
  timeout-ms: 5000
```

## Real Mode Flow

```text
Create route task
  -> Plan route through algorithm-service
  -> Convert path to TimeSlot occupancy
  -> Check SkyGrid conflict
  -> Submit SkyGrid booking
  -> Query booking status
  -> Request conflict suggestions when needed
```

## Demo

```bat
scripts\run-real-skygrid-demo.bat
```

Expected prerequisites:

- SkyGrid Gateway is available at `SKYGRID_BASE_URL`.
- A dev token is configured through `SKYGRID_TOKEN`.
- SkyGrid seed data contains route templates, altitude levels, and TimeSlots compatible with the demo scenario.

## Error Behavior

| Condition | Expected Result |
|---|---|
| Gateway unavailable | Clear message: SkyGrid Gateway is unavailable |
| Token missing | Clear message: SkyGrid dev token is missing |
| Conflict response | Returned as a conflict result and can be mapped to replanning guidance |
| Timeout | User-facing timeout message and mock-mode fallback guidance |

## Validation

Default CI/local tests should keep using mock mode. Real mode is an environment test because it depends on a running SkyGrid stack.
