from app.risk.risk_evaluator import evaluate_path_risk
from tests.test_astar import make_test_map


def make_risk_test_map():
    map_index = make_test_map(6, 6, no_fly_ids={"G-03-03"}, obstacle_ids={"G-05-05"})
    map_index.risk_weight_by_grid["G-02-02"] = 0.65
    map_index.risk_weight_by_grid["G-02-03"] = 0.65
    return map_index


def test_path_through_risk_zone_scores_higher_than_clear_path():
    map_index = make_risk_test_map()

    risky = evaluate_path_risk(["G-01-01", "G-02-02", "G-02-03"], map_index, "L120")
    clear = evaluate_path_risk(["G-01-05", "G-02-06", "G-03-06"], map_index, "L120")

    assert risky.risk_score > clear.risk_score
    assert risky.risk_grid_count == 2
    assert "path passes through 2 risk-zone grids" in risky.main_factors


def test_turns_increase_risk_slightly():
    map_index = make_risk_test_map()

    straight = evaluate_path_risk(["G-01-05", "G-02-05", "G-03-05"], map_index, "L120")
    turning = evaluate_path_risk(["G-01-05", "G-02-05", "G-02-06"], map_index, "L120")

    assert turning.risk_score > straight.risk_score
    assert "current route has 1 turns" in turning.main_factors


def test_path_near_no_fly_zone_gets_explanation():
    map_index = make_risk_test_map()

    evaluation = evaluate_path_risk(["G-02-03", "G-02-04", "G-02-05"], map_index, "L120")

    assert "path is within 1 grid of a no-fly zone" in evaluation.main_factors


def test_path_near_level_obstacle_gets_explanation():
    map_index = make_risk_test_map()

    evaluation = evaluate_path_risk(["G-04-05", "G-04-06", "G-05-06"], map_index, "L120")

    assert "path is within 1 grid of a level-blocking obstacle" in evaluation.main_factors

