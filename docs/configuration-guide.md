# LowAlt-RouteLab Configuration Guide

## Modes

LowAlt route-adapter-service supports two SkyGrid modes:

```text
skygrid.mode=mock
skygrid.mode=real
```

Mock mode is the default and does not require SkyGrid.

Real mode requires:

```text
skygrid.base-url=http://127.0.0.1:8080
skygrid.token=<dev token>
skygrid.timeout-ms=5000
```

## SkyGrid Demo Mapping

The v0.2.0 real integration path maps LowAlt altitude labels into SkyGrid's current demo seed levels:

```text
L90  -> levelId 2
L120 -> levelId 2
L150 -> levelId 3
```

If SkyGrid seed data changes, update the route-adapter-service `skygrid.default-level-id` fallback and the mapping tests before running the real demo.

## Environment Variables

```text
ADAPTER_ALGORITHM_SERVICE_BASE_URL
SKYGRID_MODE
SKYGRID_BASE_URL
SKYGRID_TOKEN
SKYGRID_TIMEOUT_MS
```

## Local Files Ignored by Git

```text
.env
*.log
algorithm-service/.venv/
frontend/node_modules/
frontend/dist/
route-adapter-service/target/
```

## Public Repository Rule

Do not commit real SkyGrid tokens, API keys, private URLs, or production credentials.
