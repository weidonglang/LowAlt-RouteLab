from app.algorithms.path_utils import segment_distance_meters
from app.core.map_loader import MapIndex
from app.group_theory.direction_group import direction_between_grid_ids, turn_cost


DEFAULT_COST_WEIGHTS = {
    "distance": 0.50,
    "risk": 0.25,
    "turn": 0.15,
    "energy": 0.05,
    "conflict": 0.05,
}

TASK_TYPE_COST_WEIGHTS = {
    "LOGISTICS_DELIVERY": {
        "distance": 0.55,
        "risk": 0.20,
        "turn": 0.10,
        "energy": 0.10,
        "conflict": 0.05,
    },
    "POWER_LINE_INSPECTION": {
        "distance": 0.30,
        "risk": 0.35,
        "turn": 0.15,
        "energy": 0.10,
        "conflict": 0.10,
    },
    "EMERGENCY_RESCUE": {
        "distance": 0.65,
        "risk": 0.10,
        "turn": 0.10,
        "energy": 0.05,
        "conflict": 0.10,
    },
}


def weights_for_task(task_type: str | None) -> dict[str, float]:
    if not task_type:
        return DEFAULT_COST_WEIGHTS
    return TASK_TYPE_COST_WEIGHTS.get(task_type, DEFAULT_COST_WEIGHTS)


def edge_cost(
    map_index: MapIndex,
    from_grid_id: str,
    to_grid_id: str,
    previous_grid_id: str | None = None,
    previous_direction: int | None = None,
    task_type: str | None = None,
    avoid_risk: bool = True,
) -> float:
    grid_size_meters = float(map_index.map_data["gridSizeMeters"])
    distance_cost = segment_distance_meters(from_grid_id, to_grid_id, grid_size_meters)
    weights = weights_for_task(task_type)
    current_direction = direction_between_grid_ids(from_grid_id, to_grid_id)
    turn_cost_value = 0.0

    if previous_grid_id is not None:
        previous_direction = direction_between_grid_ids(previous_grid_id, from_grid_id)

    if previous_direction is not None:
        turn_cost_value = turn_cost(
            previous_direction,
            current_direction,
            weight=grid_size_meters,
        )

    if not avoid_risk:
        return distance_cost + weights["turn"] * turn_cost_value

    risk_cost = map_index.risk_weight(to_grid_id) * grid_size_meters
    return (
        weights["distance"] * distance_cost
        + weights["risk"] * risk_cost
        + weights["turn"] * turn_cost_value
    )
