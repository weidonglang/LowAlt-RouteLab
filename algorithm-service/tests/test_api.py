from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "code": 200,
        "message": "algorithm-service is running",
        "data": {
            "service": "LowAlt-RouteLab algorithm-service",
            "status": "UP",
        },
    }


def test_get_demo_map_endpoint():
    response = client.get("/api/maps/demo-city-20x20")

    assert response.status_code == 200
    payload = response.json()
    assert payload["code"] == 200
    assert payload["data"]["mapId"] == "demo-city-20x20"
    assert len(payload["data"]["grids"]) == 400


def test_plan_endpoint_returns_astar_path():
    response = client.post(
        "/api/plan",
        json={
            "mapId": "demo-city-20x20",
            "taskType": "POWER_LINE_INSPECTION",
            "startGrid": "G-01-01",
            "endGrid": "G-18-16",
            "level": "L120",
            "algorithm": "A_STAR",
            "avoidRisk": True,
            "allowDiagonal": True,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    result = payload["data"]
    assert payload["message"] == "planned successfully"
    assert result["success"]
    assert result["path"][0] == "G-01-01"
    assert result["path"][-1] == "G-18-16"
    assert "G-08-08" not in result["path"]
    assert "G-04-05" not in result["path"]
    assert result["estimatedBatteryUsage"] > 0
    assert result["batteryLimit"] == 80.0
    assert result["energySafe"]
    assert result["riskFactors"]


def test_plan_endpoint_supports_dijkstra():
    response = client.post(
        "/api/plan",
        json={
            "mapId": "demo-city-20x20",
            "startGrid": "G-01-01",
            "endGrid": "G-05-04",
            "level": "L120",
            "algorithm": "DIJKSTRA",
            "avoidRisk": True,
            "allowDiagonal": True,
        },
    )

    assert response.status_code == 200
    result = response.json()["data"]
    assert result["success"]
    assert result["algorithm"] == "DIJKSTRA"
    assert result["path"][0] == "G-01-01"
    assert result["path"][-1] == "G-05-04"


def test_plan_compare_endpoint_returns_requested_algorithms():
    response = client.post(
        "/api/plan/compare",
        json={
            "mapId": "demo-city-20x20",
            "startGrid": "G-01-01",
            "endGrid": "G-18-16",
            "level": "L120",
            "algorithms": ["DIJKSTRA", "A_STAR", "THETA_STAR"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    results = payload["data"]["results"]
    assert payload["message"] == "compared successfully"
    assert [result["algorithm"] for result in results] == [
        "DIJKSTRA",
        "A_STAR",
        "THETA_STAR",
    ]
    assert all(result["success"] for result in results)


def test_symmetry_benchmark_endpoint():
    response = client.post(
        "/api/benchmark/symmetry",
        json={
            "mapId": "demo-city-20x20",
            "benchmarkTaskFile": "benchmark_tasks.json",
            "algorithms": ["A_STAR"],
            "transforms": ["IDENTITY", "ROTATE_90"],
        },
    )

    assert response.status_code == 200
    payload = response.json()
    data = payload["data"]
    assert payload["message"] == "symmetry benchmark completed"
    assert data["taskCount"] == 5
    assert data["augmentedTaskCount"] == 10
    assert data["algorithms"][0]["algorithm"] == "A_STAR"
    assert data["algorithms"][0]["successRate"] == 1.0


def test_timeslot_convert_endpoint():
    response = client.post(
        "/api/timeslot/convert",
        json={
            "path": ["G-01-01", "G-01-02", "G-02-03"],
            "level": "L120",
            "startTime": "2026-06-08 10:00:00",
            "speed": 10.0,
            "gridSizeMeters": 100,
            "slotMinutes": 5,
        },
    )

    assert response.status_code == 200
    payload = response.json()
    units = payload["data"]["occupancyUnits"]
    assert payload["message"] == "timeslot converted successfully"
    assert len(units) == 3
    assert units[0]["gridId"] == "G-01-01"
    assert units[0]["levelId"] == "L120"
    assert units[0]["slotStart"] == "2026-06-08T10:00:00"
    assert units[0]["slotEnd"] == "2026-06-08T10:05:00"
    assert units[0]["sequenceNo"] == 1


def test_validation_error_uses_unified_response():
    response = client.post(
        "/api/plan",
        json={
            "mapId": "demo-city-20x20",
            "endGrid": "G-18-16",
            "level": "L120",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "code": 422,
        "message": "request validation failed",
        "data": None,
    }
