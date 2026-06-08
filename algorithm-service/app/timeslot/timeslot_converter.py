from datetime import datetime, timedelta

from app.algorithms.path_utils import segment_distance_meters
from app.schemas.timeslot_schema import OccupancyUnit, TimeSlotConvertResult
from app.utils.grid_id import parse_grid_id


def convert_path_to_timeslots(
    path: list[str],
    level: str,
    start_time: datetime,
    speed: float,
    grid_size_meters: float,
    slot_minutes: int,
) -> TimeSlotConvertResult:
    if speed <= 0:
        raise ValueError("speed must be greater than 0")
    if grid_size_meters <= 0:
        raise ValueError("gridSizeMeters must be greater than 0")
    if slot_minutes <= 0:
        raise ValueError("slotMinutes must be greater than 0")

    _validate_path(path)

    elapsed_seconds = 0.0
    seen: set[tuple[str, str, datetime, datetime]] = set()
    units: list[OccupancyUnit] = []

    for index, grid_id in enumerate(path):
        if index > 0:
            elapsed_seconds += (
                segment_distance_meters(path[index - 1], grid_id, grid_size_meters) / speed
            )

        arrival_time = start_time + timedelta(seconds=elapsed_seconds)
        slot_start = floor_to_slot(arrival_time, slot_minutes)
        slot_end = slot_start + timedelta(minutes=slot_minutes)
        key = (grid_id, level, slot_start, slot_end)

        if key in seen:
            continue
        seen.add(key)
        units.append(
            OccupancyUnit(
                gridId=grid_id,
                levelId=level,
                slotStart=slot_start,
                slotEnd=slot_end,
                sequenceNo=len(units) + 1,
            )
        )

    return TimeSlotConvertResult(occupancyUnits=units)


def floor_to_slot(value: datetime, slot_minutes: int) -> datetime:
    if slot_minutes <= 0:
        raise ValueError("slotMinutes must be greater than 0")

    start_of_day = value.replace(hour=0, minute=0, second=0, microsecond=0)
    minutes_since_midnight = value.hour * 60 + value.minute
    floored_minutes = (minutes_since_midnight // slot_minutes) * slot_minutes
    return start_of_day + timedelta(minutes=floored_minutes)


def _validate_path(path: list[str]) -> None:
    for grid_id in path:
        parse_grid_id(grid_id)
