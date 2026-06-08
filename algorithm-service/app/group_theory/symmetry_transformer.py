from copy import deepcopy
from typing import Any

from app.utils.grid_id import parse_grid_id, to_grid_id


IDENTITY = "IDENTITY"
ROTATE_90 = "ROTATE_90"
ROTATE_180 = "ROTATE_180"
ROTATE_270 = "ROTATE_270"
FLIP_HORIZONTAL = "FLIP_HORIZONTAL"
FLIP_VERTICAL = "FLIP_VERTICAL"
FLIP_MAIN_DIAGONAL = "FLIP_MAIN_DIAGONAL"
FLIP_ANTI_DIAGONAL = "FLIP_ANTI_DIAGONAL"

TRANSFORMS = (
    IDENTITY,
    ROTATE_90,
    ROTATE_180,
    ROTATE_270,
    FLIP_HORIZONTAL,
    FLIP_VERTICAL,
    FLIP_MAIN_DIAGONAL,
    FLIP_ANTI_DIAGONAL,
)


def transform_point(x: int, y: int, n: int, transform: str) -> tuple[int, int]:
    _validate_transform(transform)
    if not (1 <= x <= n and 1 <= y <= n):
        raise ValueError(f"point out of bounds for {n}x{n} grid: {(x, y)}")

    if transform == IDENTITY:
        return x, y
    if transform == ROTATE_90:
        return y, n + 1 - x
    if transform == ROTATE_180:
        return n + 1 - x, n + 1 - y
    if transform == ROTATE_270:
        return n + 1 - y, x
    if transform == FLIP_HORIZONTAL:
        return x, n + 1 - y
    if transform == FLIP_VERTICAL:
        return n + 1 - x, y
    if transform == FLIP_MAIN_DIAGONAL:
        return y, x
    if transform == FLIP_ANTI_DIAGONAL:
        return n + 1 - y, n + 1 - x

    raise ValueError(f"unsupported D4 transform: {transform}")


def transform_grid_id(grid_id: str, n: int, transform: str) -> str:
    x, y = parse_grid_id(grid_id)
    tx, ty = transform_point(x, y, n, transform)
    return to_grid_id(tx, ty)


def transform_grid_list(grid_ids: list[str], n: int, transform: str) -> list[str]:
    return [transform_grid_id(grid_id, n, transform) for grid_id in grid_ids]


def transform_task(task: dict[str, Any], n: int, transform: str) -> dict[str, Any]:
    transformed = deepcopy(task)
    for key in ("startGrid", "endGrid", "start_grid", "end_grid"):
        if key in transformed and transformed[key] is not None:
            transformed[key] = transform_grid_id(str(transformed[key]), n, transform)

    for key in ("waypoints", "taskPoints", "gridIds"):
        if key in transformed and isinstance(transformed[key], list):
            transformed[key] = transform_grid_list(transformed[key], n, transform)

    transformed["d4Transform"] = transform
    return transformed


def transform_map(map_data: dict[str, Any], transform: str) -> dict[str, Any]:
    _validate_square_map(map_data)
    n = int(map_data["width"])
    transformed = deepcopy(map_data)
    transformed["mapId"] = f"{map_data['mapId']}__{transform.lower()}"

    grids = []
    for grid in map_data.get("grids", []):
        new_grid = deepcopy(grid)
        tx, ty = transform_point(int(grid["x"]), int(grid["y"]), n, transform)
        new_grid["x"] = tx
        new_grid["y"] = ty
        new_grid["gridId"] = to_grid_id(tx, ty)
        grids.append(new_grid)
    transformed["grids"] = sorted(grids, key=lambda item: (item["x"], item["y"]))

    for section in ("noFlyZones", "obstacles", "riskZones"):
        for item in transformed.get(section, []):
            if "gridIds" in item:
                item["gridIds"] = transform_grid_list(item["gridIds"], n, transform)

    transformed["d4Transform"] = transform
    return transformed


def _validate_transform(transform: str) -> None:
    if transform not in TRANSFORMS:
        raise ValueError(f"unsupported D4 transform: {transform}")


def _validate_square_map(map_data: dict[str, Any]) -> None:
    width = int(map_data["width"])
    height = int(map_data["height"])
    if width != height:
        raise ValueError("D4 transform requires a square map")

