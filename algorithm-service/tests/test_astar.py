import pytest

from app.algorithms.astar import AStarOptions, plan_astar
from app.core.map_loader import build_map_index, load_map


def make_test_map(
    width: int,
    height: int,
    no_fly_ids: set[str] | None = None,
    obstacle_ids: set[str] | None = None,
):
    no_fly_ids = no_fly_ids or set()
    obstacle_ids = obstacle_ids or set()
    grids = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            grid_id = f"G-{x:02d}-{y:02d}"
            grids.append(
                {
                    "gridId": grid_id,
                    "x": x,
                    "y": y,
                    "terrainType": "TEST",
                    "riskBase": 0.1,
                    "isNoFly": grid_id in no_fly_ids,
                    "isObstacle": grid_id in obstacle_ids,
                }
            )

    return build_map_index(
        {
            "mapId": "test-map",
            "width": width,
            "height": height,
            "gridSizeMeters": 100,
            "levels": ["L120"],
            "grids": grids,
            "noFlyZones": [
                {
                    "zoneId": "NFZ-TEST",
                    "name": "test no-fly zone",
                    "gridIds": sorted(no_fly_ids),
                    "blockedLevels": ["L120"],
                }
            ],
            "obstacles": [
                {
                    "obstacleId": "OBS-TEST",
                    "name": "test obstacle",
                    "gridIds": sorted(obstacle_ids),
                    "blockedLevels": ["L120"],
                }
            ],
            "riskZones": [],
        }
    )


def test_astar_finds_short_path_on_empty_map():
    map_index = make_test_map(3, 3)

    result = plan_astar(map_index, "G-01-01", "G-03-03", "L120")

    assert result.success
    assert result.path == ["G-01-01", "G-02-02", "G-03-03"]
    assert result.distance == pytest.approx(282.843)
    assert result.visitedCount > 0


def test_astar_avoids_no_fly_zone_and_obstacles_on_demo_map():
    map_index = load_map("demo-city-20x20")
    blocked = {
        "G-08-08",
        "G-08-09",
        "G-09-08",
        "G-09-09",
        "G-04-05",
        "G-04-06",
        "G-05-05",
    }

    result = plan_astar(
        map_index,
        "G-03-04",
        "G-10-10",
        "L120",
        AStarOptions(task_type="POWER_LINE_INSPECTION", avoid_risk=True),
    )

    assert result.success
    assert not blocked.intersection(result.path)
    assert result.path[0] == "G-03-04"
    assert result.path[-1] == "G-10-10"


def test_astar_returns_failure_for_blocked_start():
    map_index = load_map("demo-city-20x20")

    result = plan_astar(map_index, "G-08-08", "G-10-10", "L120")

    assert not result.success
    assert "startGrid is not traversable" in result.error


def test_astar_returns_failure_when_no_path_exists():
    map_index = make_test_map(
        3,
        3,
        no_fly_ids={
            "G-01-02",
            "G-02-01",
            "G-02-02",
        },
    )

    result = plan_astar(
        map_index,
        "G-01-01",
        "G-03-03",
        "L120",
        AStarOptions(allow_diagonal=False),
    )

    assert not result.success
    assert result.error == "no path found"
