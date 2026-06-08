import pytest

from app.group_theory.direction_group import (
    E,
    N,
    NE,
    NW,
    S,
    direction_between,
    direction_between_grid_ids,
    turn_angle_degrees,
    turn_cost,
    turn_steps,
)


def test_direction_between_points():
    assert direction_between((2, 2), (2, 1)) == N
    assert direction_between((2, 2), (3, 1)) == NE
    assert direction_between((2, 2), (3, 2)) == E


def test_direction_between_grid_ids():
    assert direction_between_grid_ids("G-02-02", "G-03-01") == NE


def test_direction_between_rejects_same_point():
    with pytest.raises(ValueError):
        direction_between((2, 2), (2, 2))


def test_turn_steps_from_plan_examples():
    assert turn_steps(N, E) == 2
    assert turn_angle_degrees(N, E) == 90
    assert turn_steps(N, S) == 4
    assert turn_angle_degrees(N, S) == 180
    assert turn_steps(NW, N) == 1
    assert turn_angle_degrees(NW, N) == 45
    assert turn_steps(E, NE) == 1
    assert turn_angle_degrees(E, NE) == 45


def test_turn_cost_uses_weight():
    assert turn_cost(N, E, weight=2.5) == 5.0
