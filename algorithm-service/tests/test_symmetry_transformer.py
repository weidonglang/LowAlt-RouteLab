import pytest

from app.core.map_loader import load_map
from app.group_theory.symmetry_transformer import (
    FLIP_HORIZONTAL,
    FLIP_MAIN_DIAGONAL,
    IDENTITY,
    ROTATE_90,
    ROTATE_180,
    transform_grid_id,
    transform_grid_list,
    transform_map,
    transform_point,
    transform_task,
)


def test_transform_point_examples():
    assert transform_point(1, 1, 20, ROTATE_90) == (1, 20)
    assert transform_point(1, 1, 20, ROTATE_180) == (20, 20)
    assert transform_point(3, 5, 20, FLIP_MAIN_DIAGONAL) == (5, 3)


def test_transform_grid_id_examples():
    assert transform_grid_id("G-01-01", 20, ROTATE_90) == "G-01-20"
    assert transform_grid_id("G-01-01", 20, ROTATE_180) == "G-20-20"
    assert transform_grid_id("G-03-05", 20, FLIP_MAIN_DIAGONAL) == "G-05-03"


def test_transform_grid_list_preserves_order():
    assert transform_grid_list(["G-01-01", "G-02-01"], 20, ROTATE_90) == [
        "G-01-20",
        "G-01-19",
    ]


def test_rotate_90_four_times_returns_original_task():
    task = {"startGrid": "G-01-01", "endGrid": "G-18-16"}

    transformed = task
    for _ in range(4):
        transformed = transform_task(transformed, 20, ROTATE_90)

    assert transformed["startGrid"] == task["startGrid"]
    assert transformed["endGrid"] == task["endGrid"]


def test_flip_horizontal_twice_returns_original_task():
    task = {"startGrid": "G-03-05", "endGrid": "G-18-16"}

    transformed = transform_task(transform_task(task, 20, FLIP_HORIZONTAL), 20, FLIP_HORIZONTAL)

    assert transformed["startGrid"] == task["startGrid"]
    assert transformed["endGrid"] == task["endGrid"]


def test_transform_map_syncs_grids_and_zones():
    map_index = load_map("demo-city-20x20")

    transformed = transform_map(map_index.map_data, ROTATE_90)

    assert transformed["mapId"] == "demo-city-20x20__rotate_90"
    assert any(grid["gridId"] == "G-01-20" for grid in transformed["grids"])
    assert "G-08-13" in transformed["noFlyZones"][0]["gridIds"]
    assert "G-05-17" in transformed["obstacles"][0]["gridIds"]
    assert "G-11-11" in transformed["riskZones"][0]["gridIds"]


def test_identity_transform_map_keeps_grid_ids():
    map_index = load_map("demo-city-20x20")

    transformed = transform_map(map_index.map_data, IDENTITY)

    assert {grid["gridId"] for grid in transformed["grids"]} == set(map_index.grids_by_id)


def test_transform_point_rejects_unknown_transform():
    with pytest.raises(ValueError):
        transform_point(1, 1, 20, "BAD")
