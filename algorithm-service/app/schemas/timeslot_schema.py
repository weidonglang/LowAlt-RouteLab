from datetime import datetime

from pydantic import BaseModel, Field


class TimeSlotConvertRequest(BaseModel):
    path: list[str] = Field(min_length=1)
    level: str
    startTime: datetime
    speed: float = Field(gt=0)
    gridSizeMeters: float = Field(gt=0)
    slotMinutes: int = Field(gt=0)


class OccupancyUnit(BaseModel):
    gridId: str
    levelId: str
    slotStart: datetime
    slotEnd: datetime
    sequenceNo: int


class TimeSlotConvertResult(BaseModel):
    occupancyUnits: list[OccupancyUnit]

