from datetime import datetime

import pytest

from app.timeslot.timeslot_converter import convert_path_to_timeslots, floor_to_slot


def test_floor_to_slot_uses_slot_minutes():
    value = datetime(2026, 6, 8, 10, 7, 31)

    assert floor_to_slot(value, 5) == datetime(2026, 6, 8, 10, 5, 0)


def test_floor_to_slot_handles_cross_hour_slot_size():
    value = datetime(2026, 6, 8, 10, 50, 0)

    assert floor_to_slot(value, 90) == datetime(2026, 6, 8, 10, 30, 0)


def test_convert_path_to_timeslots_groups_by_five_minutes():
    result = convert_path_to_timeslots(
        path=["G-01-01", "G-01-02", "G-02-03"],
        level="L120",
        start_time=datetime(2026, 6, 8, 10, 0, 0),
        speed=10.0,
        grid_size_meters=100.0,
        slot_minutes=5,
    )

    assert len(result.occupancyUnits) == 3
    assert all(unit.slotStart == datetime(2026, 6, 8, 10, 0, 0) for unit in result.occupancyUnits)
    assert all(unit.slotEnd == datetime(2026, 6, 8, 10, 5, 0) for unit in result.occupancyUnits)
    assert [unit.sequenceNo for unit in result.occupancyUnits] == [1, 2, 3]


def test_convert_path_to_timeslots_handles_diagonal_distance():
    result = convert_path_to_timeslots(
        path=["G-01-01", "G-02-02"],
        level="L120",
        start_time=datetime(2026, 6, 8, 10, 0, 0),
        speed=1.0,
        grid_size_meters=100.0,
        slot_minutes=2,
    )

    assert result.occupancyUnits[0].slotStart == datetime(2026, 6, 8, 10, 0, 0)
    assert result.occupancyUnits[1].slotStart == datetime(2026, 6, 8, 10, 2, 0)


def test_convert_path_to_timeslots_deduplicates_same_grid_same_slot():
    result = convert_path_to_timeslots(
        path=["G-01-01", "G-01-02", "G-01-01"],
        level="L120",
        start_time=datetime(2026, 6, 8, 10, 0, 0),
        speed=100.0,
        grid_size_meters=100.0,
        slot_minutes=5,
    )

    assert [unit.gridId for unit in result.occupancyUnits] == ["G-01-01", "G-01-02"]


def test_convert_path_to_timeslots_rejects_invalid_grid_id():
    with pytest.raises(ValueError):
        convert_path_to_timeslots(
            path=["bad"],
            level="L120",
            start_time=datetime(2026, 6, 8, 10, 0, 0),
            speed=10.0,
            grid_size_meters=100.0,
            slot_minutes=5,
        )


def test_convert_path_to_timeslots_rejects_invalid_speed():
    with pytest.raises(ValueError):
        convert_path_to_timeslots(
            path=["G-01-01"],
            level="L120",
            start_time=datetime(2026, 6, 8, 10, 0, 0),
            speed=0,
            grid_size_meters=100.0,
            slot_minutes=5,
        )
