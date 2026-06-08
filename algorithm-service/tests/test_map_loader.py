from app.core.map_loader import load_map


def test_load_demo_map():
    map_index = load_map("demo-city-20x20")

    assert map_index.width == 20
    assert map_index.height == 20
    assert len(map_index.grids_by_id) == 400


def test_query_no_fly_zone():
    map_index = load_map("demo-city-20x20")

    assert map_index.is_no_fly("G-08-08")
    assert not map_index.is_no_fly("G-01-01")


def test_query_obstacle_by_level():
    map_index = load_map("demo-city-20x20")

    assert map_index.is_obstacle("G-04-05", "L60")
    assert map_index.is_obstacle("G-04-05", "L120")
    assert not map_index.is_obstacle("G-04-05", "L150")


def test_query_risk_weight():
    map_index = load_map("demo-city-20x20")

    assert map_index.risk_weight("G-10-11") == 0.65
    assert map_index.risk_weight("G-01-01") == 0.1

