from fastapi import APIRouter, HTTPException

from app.schemas.common import success_response
from app.schemas.timeslot_schema import TimeSlotConvertRequest
from app.timeslot.timeslot_converter import convert_path_to_timeslots


router = APIRouter(prefix="/api/timeslot", tags=["timeslot"])


@router.post("/convert")
def convert_timeslot(request: TimeSlotConvertRequest):
    try:
        result = convert_path_to_timeslots(
            path=request.path,
            level=request.level,
            start_time=request.startTime,
            speed=request.speed,
            grid_size_meters=request.gridSizeMeters,
            slot_minutes=request.slotMinutes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return success_response("timeslot converted successfully", result)
