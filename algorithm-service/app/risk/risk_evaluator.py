from dataclasses import dataclass

from app.algorithms.path_utils import count_turns
from app.core.map_loader import MapIndex
from app.risk.risk_explainer import RiskComponents, explain_risk
from app.utils.grid_id import parse_grid_id


@dataclass(frozen=True)
class RiskEvaluation:
    risk_score: float
    risk_level: str
    main_factors: list[str]
    risk_grid_count: int


def evaluate_path_risk(path: list[str], map_index: MapIndex, level: str) -> RiskEvaluation:
    if not path:
        return RiskEvaluation(0.0, "LOW", ["empty path has no route risk"], 0)

    risk_zone_weights = [map_index.risk_weight(grid_id) for grid_id in path]
    risk_zone_grid_count = sum(1 for weight in risk_zone_weights if weight >= 0.5)
    high_risk_grid_count = sum(1 for weight in risk_zone_weights if weight >= 0.65)
    turn_count = count_turns(path)
    nearest_no_fly = _nearest_distance_to_any(path, map_index.no_fly_grid_ids)
    nearest_obstacle = _nearest_distance_to_obstacle(path, map_index, level)

    risk_zone_risk = min(sum(risk_zone_weights) / len(path), 1.0)
    turn_risk = min(turn_count / max(len(path) - 2, 1), 1.0) if len(path) >= 3 else 0.0
    no_fly_near_risk = _near_distance_risk(nearest_no_fly)
    obstacle_near_risk = _near_distance_risk(nearest_obstacle)

    risk_score = (
        0.45 * risk_zone_risk
        + 0.20 * turn_risk
        + 0.20 * no_fly_near_risk
        + 0.15 * obstacle_near_risk
    )
    risk_score = round(min(risk_score, 1.0), 3)

    components = RiskComponents(
        risk_zone_grid_count=risk_zone_grid_count,
        high_risk_grid_count=high_risk_grid_count,
        turn_count=turn_count,
        nearest_no_fly_distance=nearest_no_fly,
        nearest_obstacle_distance=nearest_obstacle,
    )

    return RiskEvaluation(
        risk_score=risk_score,
        risk_level=_risk_level(risk_score),
        main_factors=explain_risk(components),
        risk_grid_count=risk_zone_grid_count,
    )


def _risk_level(risk_score: float) -> str:
    if risk_score < 0.25:
        return "LOW"
    if risk_score < 0.50:
        return "MEDIUM"
    if risk_score < 0.75:
        return "HIGH"
    return "DANGEROUS"


def _near_distance_risk(distance: int | None) -> float:
    if distance is None:
        return 0.0
    if distance == 0:
        return 1.0
    if distance == 1:
        return 0.55
    if distance == 2:
        return 0.25
    return 0.0


def _nearest_distance_to_obstacle(
    path: list[str],
    map_index: MapIndex,
    level: str,
) -> int | None:
    obstacle_grid_ids = {
        grid_id
        for grid_id, blocked_levels in map_index.obstacle_levels_by_grid.items()
        if level in blocked_levels
    }
    return _nearest_distance_to_any(path, obstacle_grid_ids)


def _nearest_distance_to_any(path: list[str], target_grid_ids: set[str] | frozenset[str]) -> int | None:
    if not target_grid_ids:
        return None

    path_points = [parse_grid_id(grid_id) for grid_id in path]
    target_points = [parse_grid_id(grid_id) for grid_id in target_grid_ids]

    nearest: int | None = None
    for px, py in path_points:
        for tx, ty in target_points:
            distance = max(abs(px - tx), abs(py - ty))
            if nearest is None or distance < nearest:
                nearest = distance
    return nearest

