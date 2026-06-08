from fastapi import APIRouter, HTTPException

from app.algorithms.astar import AStarOptions, plan_astar
from app.algorithms.dijkstra import DijkstraOptions, plan_dijkstra
from app.algorithms.theta_star import ThetaStarOptions, plan_theta_star
from app.core.map_loader import MapIndex, load_map
from app.schemas.common import success_response
from app.schemas.plan_schema import (
    AlgorithmName,
    PlanCompareRequest,
    PlanCompareResult,
    PlanRequest,
    PlanResult,
)


router = APIRouter(prefix="/api", tags=["planning"])


@router.post("/plan")
def plan_route(request: PlanRequest):
    try:
        map_index = load_map(request.mapId)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    result = _run_algorithm(
        request.algorithm,
        map_index,
        request.startGrid,
        request.endGrid,
        request.level,
        task_type=request.taskType.value if request.taskType else None,
        avoid_risk=request.avoidRisk,
        allow_diagonal=request.allowDiagonal,
    )

    message = "planned successfully" if result.success else "planning failed"
    return success_response(message, result)


@router.post("/plan/compare")
def compare_routes(request: PlanCompareRequest):
    if not request.algorithms:
        raise HTTPException(status_code=400, detail="algorithms must not be empty")

    try:
        map_index = load_map(request.mapId)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    results = [
        _run_algorithm(
            algorithm,
            map_index,
            request.startGrid,
            request.endGrid,
            request.level,
            task_type=request.taskType.value if request.taskType else None,
            avoid_risk=request.avoidRisk,
            allow_diagonal=request.allowDiagonal,
        )
        for algorithm in request.algorithms
    ]

    return success_response("compared successfully", PlanCompareResult(results=results))


def _run_algorithm(
    algorithm: AlgorithmName,
    map_index: MapIndex,
    start_grid: str,
    end_grid: str,
    level: str,
    task_type: str | None,
    avoid_risk: bool,
    allow_diagonal: bool,
) -> PlanResult:
    if algorithm == AlgorithmName.DIJKSTRA:
        return plan_dijkstra(
            map_index,
            start_grid,
            end_grid,
            level,
            DijkstraOptions(
                task_type=task_type,
                avoid_risk=avoid_risk,
                allow_diagonal=allow_diagonal,
            ),
        )

    if algorithm == AlgorithmName.A_STAR:
        return plan_astar(
            map_index,
            start_grid,
            end_grid,
            level,
            AStarOptions(
                task_type=task_type,
                avoid_risk=avoid_risk,
                allow_diagonal=allow_diagonal,
            ),
        )

    if algorithm == AlgorithmName.THETA_STAR:
        return plan_theta_star(
            map_index,
            start_grid,
            end_grid,
            level,
            ThetaStarOptions(
                task_type=task_type,
                avoid_risk=avoid_risk,
                allow_diagonal=allow_diagonal,
            ),
        )

    raise HTTPException(status_code=400, detail=f"unsupported algorithm: {algorithm}")
