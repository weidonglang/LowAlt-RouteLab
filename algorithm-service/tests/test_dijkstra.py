import pytest

from app.algorithms.dijkstra import DijkstraOptions, plan_dijkstra
from app.core.map_loader import load_map
from tests.test_astar import make_test_map


def test_dijkstra_finds_short_path_on_empty_map():
    map_index = make_test_map(3, 3)

    result = plan_dijkstra(map_index, "G-01-01", "G-03-03", "L120")

    assert result.success
    assert result.algorithm == "DIJKSTRA"
    assert result.path[0] == "G-01-01"
    assert result.path[-1] == "G-03-03"
    assert result.distance == pytest.approx(282.843)
    assert result.visitedCount > 0


def test_dijkstra_avoids_demo_blocked_grids():
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

    result = plan_dijkstra(
        map_index,
        "G-03-04",
        "G-10-10",
        "L120",
        DijkstraOptions(task_type="POWER_LINE_INSPECTION", avoid_risk=True),
    )

    assert result.success
    assert not blocked.intersection(result.path)


def test_dijkstra_returns_failure_for_invalid_end():
    map_index = load_map("demo-city-20x20")

    result = plan_dijkstra(map_index, "G-01-01", "G-99-99", "L120")

    assert not result.success
    assert "endGrid is invalid" in result.error


def test_dijkstra_returns_failure_when_no_path_exists():
    map_index = make_test_map(
        3,
        3,
        no_fly_ids={
            "G-01-02",
            "G-02-01",
            "G-02-02",
        },
    )

    result = plan_dijkstra(
        map_index,
        "G-01-01",
        "G-03-03",
        "L120",
        DijkstraOptions(allow_diagonal=False),
    )

    assert not result.success
    assert result.error == "no path found"
