import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.utils.grid_id import is_valid_grid_id, to_grid_id


DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "maps"


@dataclass(frozen=True)
class MapIndex:
    map_data: dict[str, Any]
    grids_by_id: dict[str, dict[str, Any]]
    no_fly_grid_ids: frozenset[str]
    obstacle_levels_by_grid: dict[str, frozenset[str]]
    risk_weight_by_grid: dict[str, float]

    @property
    def width(self) -> int:
        return int(self.map_data["width"])

    @property
    def height(self) -> int:
        return int(self.map_data["height"])

    def get_grid(self, grid_id: str) -> dict[str, Any]:
        try:
            return self.grids_by_id[grid_id]
        except KeyError as exc:
            raise ValueError(f"grid id not found: {grid_id}") from exc

    def is_no_fly(self, grid_id: str) -> bool:
        self.get_grid(grid_id)
        return grid_id in self.no_fly_grid_ids

    def is_obstacle(self, grid_id: str, level: str) -> bool:
        self.get_grid(grid_id)
        return level in self.obstacle_levels_by_grid.get(grid_id, frozenset())

    def risk_weight(self, grid_id: str) -> float:
        grid = self.get_grid(grid_id)
        return max(float(grid.get("riskBase", 0.0)), self.risk_weight_by_grid.get(grid_id, 0.0))


def load_map(map_id: str) -> MapIndex:
    return _load_map_cached(map_id)


def build_map_index(map_data: dict[str, Any]) -> MapIndex:
    return _build_index(map_data)


@lru_cache(maxsize=16)
def _load_map_cached(map_id: str) -> MapIndex:
    path = DATA_DIR / f"{map_id}.json"
    if not path.exists():
        raise FileNotFoundError(f"map file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        map_data = json.load(file)

    _validate_map(map_data, map_id)
    return _build_index(map_data)


def _validate_map(map_data: dict[str, Any], expected_map_id: str) -> None:
    if map_data.get("mapId") != expected_map_id:
        raise ValueError(f"mapId mismatch: expected {expected_map_id}")

    width = int(map_data["width"])
    height = int(map_data["height"])
    grids = map_data.get("grids", [])

    if len(grids) != width * height:
        raise ValueError(f"grid count mismatch: expected {width * height}, got {len(grids)}")

    seen: set[str] = set()
    for grid in grids:
        grid_id = grid.get("gridId")
        x = int(grid.get("x"))
        y = int(grid.get("y"))
        if grid_id != to_grid_id(x, y):
            raise ValueError(f"grid id does not match coordinates: {grid_id}")
        if not is_valid_grid_id(grid_id, width, height):
            raise ValueError(f"grid id out of bounds: {grid_id}")
        if grid_id in seen:
            raise ValueError(f"duplicated grid id: {grid_id}")
        seen.add(grid_id)

    for section in ("noFlyZones", "obstacles", "riskZones"):
        for item in map_data.get(section, []):
            for grid_id in item.get("gridIds", []):
                if grid_id not in seen:
                    raise ValueError(f"{section} references unknown grid id: {grid_id}")


def _build_index(map_data: dict[str, Any]) -> MapIndex:
    grids_by_id = {grid["gridId"]: grid for grid in map_data["grids"]}

    no_fly_grid_ids = {
        grid_id
        for zone in map_data.get("noFlyZones", [])
        for grid_id in zone.get("gridIds", [])
    }

    obstacle_levels: dict[str, set[str]] = {}
    for obstacle in map_data.get("obstacles", []):
        levels = set(obstacle.get("blockedLevels", []))
        for grid_id in obstacle.get("gridIds", []):
            obstacle_levels.setdefault(grid_id, set()).update(levels)

    risk_weight_by_grid: dict[str, float] = {}
    for zone in map_data.get("riskZones", []):
        weight = float(zone.get("riskWeight", 0.0))
        for grid_id in zone.get("gridIds", []):
            risk_weight_by_grid[grid_id] = max(risk_weight_by_grid.get(grid_id, 0.0), weight)

    return MapIndex(
        map_data=map_data,
        grids_by_id=grids_by_id,
        no_fly_grid_ids=frozenset(no_fly_grid_ids),
        obstacle_levels_by_grid={
            grid_id: frozenset(levels) for grid_id, levels in obstacle_levels.items()
        },
        risk_weight_by_grid=risk_weight_by_grid,
    )
