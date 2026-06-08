from app.core.map_loader import load_map
from app.group_theory.symmetry_benchmark import (
    load_benchmark_tasks,
    run_symmetry_benchmark,
)
from app.group_theory.symmetry_transformer import IDENTITY, ROTATE_90
from app.schemas.plan_schema import AlgorithmName


def test_load_benchmark_tasks():
    tasks = load_benchmark_tasks("benchmark_tasks.json")

    assert len(tasks) == 5
    assert tasks[0]["startGrid"] == "G-01-01"


def test_run_symmetry_benchmark_returns_stats():
    map_index = load_map("demo-city-20x20")
    tasks = load_benchmark_tasks("benchmark_tasks.json")[:2]

    result = run_symmetry_benchmark(
        map_index,
        tasks,
        [AlgorithmName.A_STAR],
        [IDENTITY, ROTATE_90],
    )

    assert result.taskCount == 2
    assert result.augmentedTaskCount == 4
    assert len(result.algorithms) == 1
    assert result.algorithms[0].algorithm == AlgorithmName.A_STAR
    assert result.algorithms[0].successRate == 1.0
    assert result.algorithms[0].avgDistance > 0
