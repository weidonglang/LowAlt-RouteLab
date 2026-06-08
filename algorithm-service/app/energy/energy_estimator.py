from dataclasses import dataclass


@dataclass(frozen=True)
class EnergyEstimate:
    estimated_battery_usage: float
    battery_limit: float
    energy_safe: bool


DEFAULT_ENERGY_PARAMS = {
    "baseCostPerMeter": 0.006,
    "turnCost": 0.3,
    "climbCost": 1.2,
    "riskPenalty": 0.2,
    "batteryLimit": 80.0,
}


def estimate_energy_usage(
    distance_meters: float,
    turn_count: int,
    risk_grid_count: int,
    level_change_count: int = 0,
    params: dict[str, float] | None = None,
) -> EnergyEstimate:
    params = params or DEFAULT_ENERGY_PARAMS
    estimated = (
        params["baseCostPerMeter"] * distance_meters
        + params["turnCost"] * turn_count
        + params["climbCost"] * level_change_count
        + params["riskPenalty"] * risk_grid_count
    )
    estimated = round(estimated, 3)
    battery_limit = float(params["batteryLimit"])

    return EnergyEstimate(
        estimated_battery_usage=estimated,
        battery_limit=battery_limit,
        energy_safe=estimated <= battery_limit,
    )
