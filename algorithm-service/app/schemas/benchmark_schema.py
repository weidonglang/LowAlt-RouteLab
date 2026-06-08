from pydantic import BaseModel, Field

from app.group_theory.symmetry_transformer import TRANSFORMS
from app.schemas.plan_schema import AlgorithmName


class SymmetryBenchmarkRequest(BaseModel):
    mapId: str = "demo-city-20x20"
    benchmarkTaskFile: str = "benchmark_tasks.json"
    algorithms: list[AlgorithmName] = Field(
        default_factory=lambda: [
            AlgorithmName.DIJKSTRA,
            AlgorithmName.A_STAR,
            AlgorithmName.THETA_STAR,
        ]
    )
    transforms: list[str] = Field(default_factory=lambda: list(TRANSFORMS))


class SymmetryAlgorithmStats(BaseModel):
    algorithm: AlgorithmName
    successRate: float
    avgDistance: float
    avgPlanningTimeMs: float
    avgRiskScore: float
    distanceVarianceUnderD4: float


class SymmetryBenchmarkResult(BaseModel):
    taskCount: int
    augmentedTaskCount: int
    algorithms: list[SymmetryAlgorithmStats]

