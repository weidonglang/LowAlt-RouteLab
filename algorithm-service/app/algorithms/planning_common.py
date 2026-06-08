from time import perf_counter

from app.algorithms.path_utils import count_turns, path_distance_meters
from app.core.graph_builder import is_traversable
from app.core.map_loader import MapIndex
from app.energy.energy_estimator import estimate_energy_usage
from app.risk.risk_evaluator import evaluate_path_risk
from app.schemas.plan_schema import AlgorithmName, PlanResult


DEFAULT_SPEED_MPS = 10.0


def validate_plan_request(
    map_index: MapIndex,
    start_grid: str,
    end_grid: str,
    level: str,
) -> str | None:
    if level not in map_index.map_data["levels"]:
        return f"level not found: {level}"

    for label, grid_id in (("startGrid", start_grid), ("endGrid", end_grid)):
        try:
            map_index.get_grid(grid_id)
        except ValueError:
            return f"{label} is invalid: {grid_id}"

        if not is_traversable(map_index, grid_id, level):
            return f"{label} is not traversable at {level}: {grid_id}"

    return None


def reconstruct_path(came_from: dict[str, str], end_grid: str) -> list[str]:
    path = [end_grid]
    current = end_grid
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path


def reconstruct_state_path(
    came_from: dict[tuple[str, int | None], tuple[str, int | None]],
    end_state: tuple[str, int | None],
) -> list[str]:
    states = [end_state]
    current = end_state
    while current in came_from:
        current = came_from[current]
        states.append(current)
    states.reverse()
    return [grid_id for grid_id, _ in states]


def build_success_result(
    algorithm: AlgorithmName,
    path: list[str],
    visited_count: int,
    started_at: float,
    map_index: MapIndex,
    level: str,
) -> PlanResult:
    grid_size_meters = float(map_index.map_data["gridSizeMeters"])
    distance = path_distance_meters(path, grid_size_meters)
    turn_count = count_turns(path)
    risk_evaluation = evaluate_path_risk(path, map_index, level)
    energy_estimate = estimate_energy_usage(
        distance_meters=distance,
        turn_count=turn_count,
        risk_grid_count=risk_evaluation.risk_grid_count,
    )

    return PlanResult(
        success=True,
        algorithm=algorithm,
        path=path,
        distance=round(distance, 3),
        estimatedTimeSeconds=round(distance / DEFAULT_SPEED_MPS),
        turnCount=turn_count,
        planningTimeMs=round((perf_counter() - started_at) * 1000),
        visitedCount=visited_count,
        riskScore=risk_evaluation.risk_score,
        riskLevel=risk_evaluation.risk_level,
        riskFactors=risk_evaluation.main_factors,
        estimatedBatteryUsage=energy_estimate.estimated_battery_usage,
        batteryLimit=energy_estimate.battery_limit,
        energySafe=energy_estimate.energy_safe,
    )


def build_failure_result(
    algorithm: AlgorithmName,
    error: str,
    started_at: float,
    visited_count: int = 0,
) -> PlanResult:
    return PlanResult(
        success=False,
        algorithm=algorithm,
        planningTimeMs=round((perf_counter() - started_at) * 1000),
        visitedCount=visited_count,
        error=error,
    )


def clone_failure_result(algorithm: AlgorithmName, result: PlanResult) -> PlanResult:
    return PlanResult(
        success=False,
        algorithm=algorithm,
        planningTimeMs=result.planningTimeMs,
        visitedCount=result.visitedCount,
        error=result.error,
    )
