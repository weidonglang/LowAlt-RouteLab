from dataclasses import dataclass
from time import perf_counter

from app.algorithms.astar import AStarOptions, plan_astar
from app.algorithms.planning_common import (
    build_success_result,
    clone_failure_result,
)
from app.core.graph_builder import is_traversable
from app.core.map_loader import MapIndex
from app.schemas.plan_schema import AlgorithmName, PlanResult
from app.utils.grid_id import parse_grid_id, to_grid_id


@dataclass(frozen=True)
class ThetaStarOptions:
    task_type: str | None = None
    avoid_risk: bool = True
    allow_diagonal: bool = True


def plan_theta_star(
    map_index: MapIndex,
    start_grid: str,
    end_grid: str,
    level: str,
    options: ThetaStarOptions | None = None,
) -> PlanResult:
    options = options or ThetaStarOptions()
    started_at = perf_counter()

    astar_result = plan_astar(
        map_index,
        start_grid,
        end_grid,
        level,
        AStarOptions(
            task_type=options.task_type,
            avoid_risk=options.avoid_risk,
            allow_diagonal=options.allow_diagonal,
        ),
    )

    if not astar_result.success:
        return clone_failure_result(AlgorithmName.THETA_STAR, astar_result)

    smoothed_path = smooth_path(astar_result.path, map_index, level)
    return build_success_result(
        AlgorithmName.THETA_STAR,
        smoothed_path,
        astar_result.visitedCount,
        started_at,
        map_index,
        level,
    )


def smooth_path(path: list[str], map_index: MapIndex, level: str) -> list[str]:
    if len(path) <= 2:
        return path[:]

    smoothed = [path[0]]
    anchor_index = 0

    while anchor_index < len(path) - 1:
        next_index = len(path) - 1
        while next_index > anchor_index + 1:
            if has_line_of_sight(map_index, path[anchor_index], path[next_index], level):
                break
            next_index -= 1

        smoothed.append(path[next_index])
        anchor_index = next_index

    return smoothed


def has_line_of_sight(
    map_index: MapIndex,
    start_grid: str,
    end_grid: str,
    level: str,
) -> bool:
    for grid_id in _bresenham_grid_ids(start_grid, end_grid):
        if not is_traversable(map_index, grid_id, level):
            return False
    return True


def _bresenham_grid_ids(start_grid: str, end_grid: str) -> list[str]:
    x0, y0 = parse_grid_id(start_grid)
    x1, y1 = parse_grid_id(end_grid)

    points: list[str] = []
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x = x0
    y = y0
    while True:
        points.append(to_grid_id(x, y))
        if x == x1 and y == y1:
            break
        double_error = 2 * err
        if double_error > -dy:
            err -= dy
            x += sx
        if double_error < dx:
            err += dx
            y += sy

    return points
