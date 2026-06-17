from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from statistics import mean
from time import perf_counter

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from app.main import app  # noqa: E402


SCENARIO_DIR = ROOT / "benchmarks" / "scenarios"
RESULT_DIR = ROOT / "benchmarks" / "results"
ALGORITHM_CASES = [
    ("DIJKSTRA", "DIJKSTRA", False),
    ("A_STAR", "A_STAR", False),
    ("THETA_STAR", "THETA_STAR", False),
    ("A_STAR_RISK_PENALTY", "A_STAR", True),
    ("THETA_STAR_RISK_PENALTY", "THETA_STAR", True),
]


def load_scenarios() -> list[dict]:
    scenarios = []
    for path in sorted(SCENARIO_DIR.glob("*.json")):
        scenarios.append(json.loads(path.read_text(encoding="utf-8")))
    if not scenarios:
        raise SystemExit(f"no benchmark scenarios found in {SCENARIO_DIR}")
    return scenarios


def load_risk_cells(client: TestClient, map_id: str) -> set[str]:
    response = client.get(f"/api/maps/{map_id}")
    response.raise_for_status()
    grids = response.json()["data"]["grids"]
    return {
        grid["gridId"]
        for grid in grids
        if str(grid.get("status", "")).upper() == "RISK"
    }


def convert_timeslots(client: TestClient, path: list[str], level: str) -> int:
    if not path:
        return 0
    response = client.post(
        "/api/timeslot/convert",
        json={
            "path": path,
            "level": level,
            "startTime": "2026-06-15T10:00:00",
            "speed": 10.0,
            "gridSizeMeters": 100,
            "slotMinutes": 5,
        },
    )
    response.raise_for_status()
    return len(response.json()["data"]["occupancyUnits"])


def run_case(client: TestClient, scenario: dict, label: str, algorithm: str, force_avoid_risk: bool) -> dict:
    request = {
        "mapId": scenario["mapId"],
        "taskType": scenario.get("taskType"),
        "startGrid": scenario["startGrid"],
        "endGrid": scenario["endGrid"],
        "level": scenario["level"],
        "algorithm": algorithm,
        "avoidRisk": force_avoid_risk or bool(scenario.get("avoidRisk", False)),
        "allowDiagonal": bool(scenario.get("allowDiagonal", True)),
    }
    started = perf_counter()
    response = client.post("/api/plan", json=request)
    elapsed_ms = round((perf_counter() - started) * 1000, 3)
    response.raise_for_status()
    result = response.json()["data"]
    path = result.get("path", [])
    risk_cells = load_risk_cells(client, scenario["mapId"])
    risk_cells_passed = sum(1 for grid in path if grid in risk_cells)
    timeslot_count = convert_timeslots(client, path, scenario["level"])
    return {
        "scenarioId": scenario["scenarioId"],
        "algorithm": label,
        "success": bool(result["success"]),
        "pathLength": result["distance"],
        "turnCount": result["turnCount"],
        "riskCellsPassed": risk_cells_passed,
        "riskScore": result["riskScore"],
        "energyCost": result["estimatedBatteryUsage"],
        "planningTimeMs": result["planningTimeMs"],
        "wallTimeMs": elapsed_ms,
        "visitedCount": result["visitedCount"],
        "timeSlotCount": timeslot_count,
    }


def summarize(rows: list[dict]) -> list[dict]:
    summary = []
    for algorithm in sorted({row["algorithm"] for row in rows}):
        subset = [row for row in rows if row["algorithm"] == algorithm]
        success = [row for row in subset if row["success"]]
        summary.append(
            {
                "algorithm": algorithm,
                "scenarioCount": len(subset),
                "successRate": round(len(success) / len(subset), 4),
                "avgPathLength": round(mean(row["pathLength"] for row in success), 3) if success else 0,
                "avgTurnCount": round(mean(row["turnCount"] for row in success), 3) if success else 0,
                "avgRiskScore": round(mean(row["riskScore"] for row in success), 4) if success else 0,
                "avgEnergyCost": round(mean(row["energyCost"] for row in success), 4) if success else 0,
                "avgPlanningTimeMs": round(mean(row["planningTimeMs"] for row in success), 3) if success else 0,
                "avgTimeSlotCount": round(mean(row["timeSlotCount"] for row in success), 3) if success else 0,
            }
        )
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    RESULT_DIR.mkdir(parents=True, exist_ok=True)
    client = TestClient(app)
    rows = []
    for scenario in load_scenarios():
        for label, algorithm, force_avoid_risk in ALGORITHM_CASES:
            rows.append(run_case(client, scenario, label, algorithm, force_avoid_risk))

    payload = {
        "scenarioCount": len(load_scenarios()),
        "caseCount": len(rows),
        "summary": summarize(rows),
        "rows": rows,
    }
    (RESULT_DIR / "benchmark-summary.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_csv(RESULT_DIR / "benchmark-summary.csv", rows)
    print(f"Benchmark completed: {len(rows)} cases")
    print(f"JSON: {RESULT_DIR / 'benchmark-summary.json'}")
    print(f"CSV: {RESULT_DIR / 'benchmark-summary.csv'}")


if __name__ == "__main__":
    main()
