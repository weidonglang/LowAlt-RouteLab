from app.core.cost_model import edge_cost
from tests.test_astar import make_test_map


def test_edge_cost_includes_turn_penalty():
    map_index = make_test_map(3, 3)

    straight = edge_cost(
        map_index,
        "G-02-01",
        "G-03-01",
        previous_grid_id="G-01-01",
        avoid_risk=False,
    )
    turning = edge_cost(
        map_index,
        "G-02-01",
        "G-02-02",
        previous_grid_id="G-01-01",
        avoid_risk=False,
    )

    assert turning > straight
