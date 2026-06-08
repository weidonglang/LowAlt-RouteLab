from typing import Generic, TypeVar

from pydantic import BaseModel


T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    code: int = 200
    message: str
    data: T | None = None


class HealthData(BaseModel):
    service: str
    status: str


def success_response(message: str, data: T | None = None) -> ApiResponse[T]:
    return ApiResponse(code=200, message=message, data=data)


def error_response(code: int, message: str) -> ApiResponse[None]:
    return ApiResponse(code=code, message=message, data=None)
