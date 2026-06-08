from dataclasses import dataclass
from heapq import heappop, heappush
from time import perf_counter

from app.algorithms.planning_common import (
    build_failure_result,
    build_success_result,
    reconstruct_state_path,
    validate_plan_request,
)
from app.core.cost_model import edge_cost, weights_for_task
from app.core.graph_builder import grid_distance_steps, iter_neighbors
from app.core.map_loader import MapIndex
from app.group_theory.direction_group import direction_between_grid_ids
from app.schemas.plan_schema import AlgorithmName, PlanResult


@dataclass(frozen=True)
class AStarOptions:
    task_type: str | None = None
    avoid_risk: bool = True
    allow_diagonal: bool = True


def plan_astar(
    map_index: MapIndex,
    start_grid: str,
    end_grid: str,
    level: str,
    options: AStarOptions | None = None,
) -> PlanResult:
    options = options or AStarOptions()
    started_at = perf_counter()

    validation_error = validate_plan_request(map_index, start_grid, end_grid, level)
    if validation_error:
        return build_failure_result(AlgorithmName.A_STAR, validation_error, started_at)

    if start_grid == end_grid:
        return build_success_result(
            AlgorithmName.A_STAR,
            [start_grid],
            0,
            started_at,
            map_index,
            level,
        )

    grid_size_meters = float(map_index.map_data["gridSizeMeters"])
    start_state = (start_grid, None)
    open_heap: list[tuple[float, int, tuple[str, int | None]]] = []
    sequence = 0
    heappush(open_heap, (0.0, sequence, start_state))

    came_from: dict[tuple[str, int | None], tuple[str, int | None]] = {}
    g_score: dict[tuple[str, int | None], float] = {start_state: 0.0}
    closed: set[tuple[str, int | None]] = set()
    visited_count = 0
    heuristic_distance_weight = (
        weights_for_task(options.task_type)["distance"] if options.avoid_risk else 1.0
    )

    while open_heap:
        _, _, current_state = heappop(open_heap)
        if current_state in closed:
            continue
        closed.add(current_state)
        visited_count += 1
        current, incoming_direction = current_state

        if current == end_grid:
            path = reconstruct_state_path(came_from, current_state)
            return build_success_result(
                AlgorithmName.A_STAR,
                path,
                visited_count,
                started_at,
                map_index,
                level,
            )

        for neighbor in iter_neighbors(map_index, current, level, options.allow_diagonal):
            neighbor_direction = direction_between_grid_ids(current, neighbor)
            neighbor_state = (neighbor, neighbor_direction)
            tentative = g_score[current_state] + edge_cost(
                map_index,
                current,
                neighbor,
                previous_direction=incoming_direction,
                task_type=options.task_type,
                avoid_risk=options.avoid_risk,
            )
            if tentative >= g_score.get(neighbor_state, float("inf")):
                continue

            came_from[neighbor_state] = current_state
            g_score[neighbor_state] = tentative
            heuristic = (
                grid_distance_steps(neighbor, end_grid)
                * grid_size_meters
                * heuristic_distance_weight
            )
            sequence += 1
            heappush(open_heap, (tentative + heuristic, sequence, neighbor_state))

    return build_failure_result(
        AlgorithmName.A_STAR,
        "no path found",
        started_at,
        visited_count,
    )
