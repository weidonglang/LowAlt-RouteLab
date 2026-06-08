from app.algorithms.theta_star import has_line_of_sight, plan_theta_star, smooth_path
from app.core.map_loader import load_map
from tests.test_astar import make_test_map


def test_line_of_sight_is_clear_on_empty_diagonal():
    map_index = make_test_map(5, 5)

    assert has_line_of_sight(map_index, "G-01-01", "G-05-05", "L120")


def test_line_of_sight_rejects_blocked_grid_on_line():
    map_index = make_test_map(5, 5, no_fly_ids={"G-03-03"})

    assert not has_line_of_sight(map_index, "G-01-01", "G-05-05", "L120")


def test_smooth_path_removes_unnecessary_middle_points():
    map_index = make_test_map(5, 5)
    path = ["G-01-01", "G-02-02", "G-03-03", "G-04-04", "G-05-05"]

    assert smooth_path(path, map_index, "L120") == ["G-01-01", "G-05-05"]


def test_theta_star_returns_smoothed_path_for_demo_map():
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

    result = plan_theta_star(
        map_index,
        "G-03-04",
        "G-10-10",
        "L120",
    )

    assert result.success
    assert result.algorithm == "THETA_STAR"
    assert result.path[0] == "G-03-04"
    assert result.path[-1] == "G-10-10"
    assert not blocked.intersection(result.path)


def test_theta_star_distance_uses_direct_segment_length():
    map_index = make_test_map(5, 5)

    result = plan_theta_star(map_index, "G-01-01", "G-05-05", "L120")

    assert result.success
    assert result.path == ["G-01-01", "G-05-05"]
    assert result.distance == 565.685
