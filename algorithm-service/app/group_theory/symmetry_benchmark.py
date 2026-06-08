import json
from pathlib import Path
from statistics import mean, pvariance
from typing import Any

from app.algorithms.astar import AStarOptions, plan_astar
from app.algorithms.dijkstra import DijkstraOptions, plan_dijkstra
from app.algorithms.theta_star import ThetaStarOptions, plan_theta_star
from app.core.map_loader import MapIndex, build_map_index
from app.group_theory.symmetry_transformer import transform_map, transform_task
from app.schemas.benchmark_schema import SymmetryAlgorithmStats, SymmetryBenchmarkResult
from app.schemas.plan_schema import AlgorithmName, PlanResult


BENCHMARK_TASK_DIR = Path(__file__).resolve().parents[2] / "data" / "benchmark_tasks"


def load_benchmark_tasks(file_name: str) -> list[dict[str, Any]]:
    if Path(file_name).name != file_name:
        raise ValueError("benchmarkTaskFile must be a file name, not a path")

    path = BENCHMARK_TASK_DIR / file_name
    if not path.exists():
        raise FileNotFoundError(f"benchmark task file not found: {path}")

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    tasks = data.get("tasks") if isinstance(data, dict) else data
    if not isinstance(tasks, list):
        raise ValueError("benchmark task file must contain a task list")
    return tasks


def run_symmetry_benchmark(
    map_index: MapIndex,
    tasks: list[dict[str, Any]],
    algorithms: list[AlgorithmName],
    transforms: list[str],
) -> SymmetryBenchmarkResult:
    transformed_maps = {
        transform: build_map_index(transform_map(map_index.map_data, transform))
        for transform in transforms
    }

    stats = [
        _run_algorithm_stats(algorithm, map_index, transformed_maps, tasks, transforms)
        for algorithm in algorithms
    ]

    return SymmetryBenchmarkResult(
        taskCount=len(tasks),
        augmentedTaskCount=len(tasks) * len(transforms),
        algorithms=stats,
    )


def _run_algorithm_stats(
    algorithm: AlgorithmName,
    source_map_index: MapIndex,
    transformed_maps: dict[str, MapIndex],
    tasks: list[dict[str, Any]],
    transforms: list[str],
) -> SymmetryAlgorithmStats:
    results: list[PlanResult] = []
    distances_by_task: dict[str, list[float]] = {}

    for task in tasks:
        task_id = str(task.get("taskId", task.get("id", len(distances_by_task) + 1)))
        for transform in transforms:
            transformed_task = transform_task(task, source_map_index.width, transform)
            result = _run_algorithm(
                algorithm,
                transformed_maps[transform],
                transformed_task,
            )
            results.append(result)
            if result.success:
                distances_by_task.setdefault(task_id, []).append(result.distance)

    success_results = [result for result in results if result.success]
    success_rate = len(success_results) / len(results) if results else 0.0

    return SymmetryAlgorithmStats(
        algorithm=algorithm,
        successRate=round(success_rate, 3),
        avgDistance=round(_avg([result.distance for result in success_results]), 3),
        avgPlanningTimeMs=round(_avg([result.planningTimeMs for result in success_results]), 3),
        avgRiskScore=round(_avg([result.riskScore for result in success_results]), 3),
        distanceVarianceUnderD4=round(_avg_normalized_variance(distances_by_task), 6),
    )


def _run_algorithm(
    algorithm: AlgorithmName,
    map_index: MapIndex,
    task: dict[str, Any],
) -> PlanResult:
    task_type = task.get("taskType")
    start_grid = task["startGrid"]
    end_grid = task["endGrid"]
    level = task["level"]
    avoid_risk = bool(task.get("avoidRisk", True))
    allow_diagonal = bool(task.get("allowDiagonal", True))

    if algorithm == AlgorithmName.DIJKSTRA:
        return plan_dijkstra(
            map_index,
            start_grid,
            end_grid,
            level,
            DijkstraOptions(task_type=task_type, avoid_risk=avoid_risk, allow_diagonal=allow_diagonal),
        )
    if algorithm == AlgorithmName.A_STAR:
        return plan_astar(
            map_index,
            start_grid,
            end_grid,
            level,
            AStarOptions(task_type=task_type, avoid_risk=avoid_risk, allow_diagonal=allow_diagonal),
        )
    if algorithm == AlgorithmName.THETA_STAR:
        return plan_theta_star(
            map_index,
            start_grid,
            end_grid,
            level,
            ThetaStarOptions(task_type=task_type, avoid_risk=avoid_risk, allow_diagonal=allow_diagonal),
        )
    raise ValueError(f"unsupported algorithm: {algorithm}")


def _avg(values: list[float | int]) -> float:
    return float(mean(values)) if values else 0.0


def _avg_normalized_variance(distances_by_task: dict[str, list[float]]) -> float:
    normalized_variances: list[float] = []
    for distances in distances_by_task.values():
        if len(distances) < 2:
            continue
        avg_distance = mean(distances)
        if avg_distance == 0:
            normalized_variances.append(0.0)
        else:
            normalized_variances.append(pvariance(distances) / (avg_distance * avg_distance))
    return _avg(normalized_variances)
