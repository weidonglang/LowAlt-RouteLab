from dataclasses import dataclass


@dataclass(frozen=True)
class RiskComponents:
    risk_zone_grid_count: int
    high_risk_grid_count: int
    turn_count: int
    nearest_no_fly_distance: int | None
    nearest_obstacle_distance: int | None


def explain_risk(components: RiskComponents) -> list[str]:
    factors: list[str] = []

    if components.risk_zone_grid_count:
        factors.append(f"path passes through {components.risk_zone_grid_count} risk-zone grids")
    else:
        factors.append("no risk-zone grid detected on current path")

    if components.nearest_no_fly_distance is not None and components.nearest_no_fly_distance <= 1:
        factors.append("path is within 1 grid of a no-fly zone")

    if (
        components.nearest_obstacle_distance is not None
        and components.nearest_obstacle_distance <= 1
    ):
        factors.append("path is within 1 grid of a level-blocking obstacle")

    if components.turn_count:
        factors.append(f"current route has {components.turn_count} turns")
    else:
        factors.append("current route has no turns")

    return factors

