from fastapi import APIRouter, HTTPException

from app.core.map_loader import load_map
from app.group_theory.symmetry_benchmark import (
    load_benchmark_tasks,
    run_symmetry_benchmark,
)
from app.group_theory.symmetry_transformer import TRANSFORMS
from app.schemas.benchmark_schema import SymmetryBenchmarkRequest
from app.schemas.common import success_response


router = APIRouter(prefix="/api/benchmark", tags=["benchmark"])


@router.post("/symmetry")
def run_symmetry(request: SymmetryBenchmarkRequest):
    unknown_transforms = [transform for transform in request.transforms if transform not in TRANSFORMS]
    if unknown_transforms:
        raise HTTPException(
            status_code=400,
            detail=f"unsupported D4 transforms: {', '.join(unknown_transforms)}",
        )
    if not request.algorithms:
        raise HTTPException(status_code=400, detail="algorithms must not be empty")

    try:
        map_index = load_map(request.mapId)
        tasks = load_benchmark_tasks(request.benchmarkTaskFile)
        result = run_symmetry_benchmark(map_index, tasks, request.algorithms, request.transforms)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return success_response("symmetry benchmark completed", result)

