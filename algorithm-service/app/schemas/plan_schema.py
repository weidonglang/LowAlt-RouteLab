from enum import Enum

from pydantic import BaseModel, Field


class AlgorithmName(str, Enum):
    DIJKSTRA = "DIJKSTRA"
    A_STAR = "A_STAR"
    THETA_STAR = "THETA_STAR"


class TaskType(str, Enum):
    LOGISTICS_DELIVERY = "LOGISTICS_DELIVERY"
    POWER_LINE_INSPECTION = "POWER_LINE_INSPECTION"
    EMERGENCY_RESCUE = "EMERGENCY_RESCUE"


class PlanRequest(BaseModel):
    mapId: str = "demo-city-20x20"
    taskType: TaskType | None = None
    startGrid: str
    endGrid: str
    level: str
    algorithm: AlgorithmName = AlgorithmName.A_STAR
    avoidRisk: bool = True
    allowDiagonal: bool = True


class PlanResult(BaseModel):
    success: bool
    algorithm: AlgorithmName
    path: list[str] = Field(default_factory=list)
    distance: float = 0.0
    estimatedTimeSeconds: int = 0
    turnCount: int = 0
    planningTimeMs: int = 0
    visitedCount: int = 0
    riskScore: float = 0.0
    riskLevel: str = "LOW"
    riskFactors: list[str] = Field(default_factory=list)
    estimatedBatteryUsage: float = 0.0
    batteryLimit: float = 80.0
    energySafe: bool = True
    error: str | None = None


class PlanCompareRequest(BaseModel):
    mapId: str = "demo-city-20x20"
    taskType: TaskType | None = None
    startGrid: str
    endGrid: str
    level: str
    algorithms: list[AlgorithmName] = Field(
        default_factory=lambda: [
            AlgorithmName.DIJKSTRA,
            AlgorithmName.A_STAR,
            AlgorithmName.THETA_STAR,
        ]
    )
    avoidRisk: bool = True
    allowDiagonal: bool = True


class PlanCompareResult(BaseModel):
    results: list[PlanResult]
