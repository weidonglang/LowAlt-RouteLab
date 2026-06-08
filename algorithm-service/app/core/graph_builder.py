from math import sqrt

from app.core.map_loader import MapIndex
from app.utils.grid_id import parse_grid_id, to_grid_id


FOUR_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (0, -1),
    (1, 0),
    (0, 1),
    (-1, 0),
)

DIAGONAL_DIRECTIONS: tuple[tuple[int, int], ...] = (
    (-1, -1),
    (1, -1),
    (1, 1),
    (-1, 1),
)


def is_traversable(map_index: MapIndex, grid_id: str, level: str) -> bool:
    return not map_index.is_no_fly(grid_id) and not map_index.is_obstacle(grid_id, level)


def iter_neighbors(
    map_index: MapIndex,
    grid_id: str,
    level: str,
    allow_diagonal: bool = True,
) -> list[str]:
    x, y = parse_grid_id(grid_id)
    directions = FOUR_DIRECTIONS + (DIAGONAL_DIRECTIONS if allow_diagonal else ())

    neighbors: list[str] = []
    for dx, dy in directions:
        nx = x + dx
        ny = y + dy
        if not (1 <= nx <= map_index.width and 1 <= ny <= map_index.height):
            continue

        neighbor_id = to_grid_id(nx, ny)
        if not is_traversable(map_index, neighbor_id, level):
            continue

        neighbors.append(neighbor_id)

    return neighbors


def grid_distance_steps(a_grid_id: str, b_grid_id: str) -> float:
    ax, ay = parse_grid_id(a_grid_id)
    bx, by = parse_grid_id(b_grid_id)
    dx = abs(ax - bx)
    dy = abs(ay - by)
    diagonal = min(dx, dy)
    straight = max(dx, dy) - diagonal
    return diagonal * sqrt(2) + straight

