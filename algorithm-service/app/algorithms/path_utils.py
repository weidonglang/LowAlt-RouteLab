from math import sqrt

from app.utils.grid_id import parse_grid_id


def segment_distance_meters(a_grid_id: str, b_grid_id: str, grid_size_meters: float) -> float:
    ax, ay = parse_grid_id(a_grid_id)
    bx, by = parse_grid_id(b_grid_id)
    dx = abs(ax - bx)
    dy = abs(ay - by)
    return sqrt(dx * dx + dy * dy) * grid_size_meters


def path_distance_meters(path: list[str], grid_size_meters: float) -> float:
    if len(path) < 2:
        return 0.0
    return sum(
        segment_distance_meters(current, next_grid, grid_size_meters)
        for current, next_grid in zip(path, path[1:])
    )


def count_turns(path: list[str]) -> int:
    if len(path) < 3:
        return 0

    turns = 0
    previous_direction: tuple[int, int] | None = None
    for first, second in zip(path, path[1:]):
        ax, ay = parse_grid_id(first)
        bx, by = parse_grid_id(second)
        direction = (bx - ax, by - ay)
        if previous_direction is not None and direction != previous_direction:
            turns += 1
        previous_direction = direction
    return turns
