from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.routers import benchmark_router, map_router, plan_router, timeslot_router
from app.schemas.common import HealthData, error_response, success_response


app = FastAPI(
    title="LowAlt-RouteLab algorithm-service",
    description="UAV route planning and risk evaluation simulator algorithm service.",
    version="0.1.0",
)

app.include_router(map_router.router)
app.include_router(plan_router.router)
app.include_router(benchmark_router.router)
app.include_router(timeslot_router.router)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(exc.status_code, str(exc.detail)).model_dump(),
    )


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=error_response(422, "request validation failed").model_dump(),
    )


@app.get("/health")
def health():
    return success_response(
        "algorithm-service is running",
        HealthData(service="LowAlt-RouteLab algorithm-service", status="UP"),
    )
