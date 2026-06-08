import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "algorithm-service" / "data" / "maps" / "demo-city-20x20.json"


def to_grid_id(x: int, y: int) -> str:
    return f"G-{x:02d}-{y:02d}"


def risk_base_for(x: int, y: int) -> float:
    if 9 <= x <= 12 and 10 <= y <= 13:
        return 0.18
    if 3 <= x <= 6 and 4 <= y <= 7:
        return 0.16
    return 0.1


def terrain_for(x: int, y: int) -> str:
    if 8 <= x <= 12 and 8 <= y <= 12:
        return "CBD"
    if x in (1, 20) or y in (1, 20):
        return "SUBURBAN"
    return "URBAN"


def main() -> None:
    width = 20
    height = 20
    no_fly_ids = {"G-08-08", "G-08-09", "G-09-08", "G-09-09"}
    obstacle_ids = {"G-04-05", "G-04-06", "G-05-05"}

    grids = []
    for x in range(1, width + 1):
        for y in range(1, height + 1):
            grid_id = to_grid_id(x, y)
            grids.append(
                {
                    "gridId": grid_id,
                    "x": x,
                    "y": y,
                    "terrainType": terrain_for(x, y),
                    "riskBase": risk_base_for(x, y),
                    "isNoFly": grid_id in no_fly_ids,
                    "isObstacle": grid_id in obstacle_ids,
                }
            )

    map_data = {
        "mapId": "demo-city-20x20",
        "width": width,
        "height": height,
        "gridSizeMeters": 100,
        "levels": ["L60", "L90", "L120", "L150", "L180"],
        "grids": grids,
        "noFlyZones": [
            {
                "zoneId": "NFZ-001",
                "name": "airport protection area",
                "gridIds": sorted(no_fly_ids),
                "blockedLevels": ["L60", "L90", "L120", "L150", "L180"],
            }
        ],
        "obstacles": [
            {
                "obstacleId": "OBS-001",
                "name": "high-rise building cluster",
                "gridIds": sorted(obstacle_ids),
                "blockedLevels": ["L60", "L90", "L120"],
            }
        ],
        "riskZones": [
            {
                "riskZoneId": "RZ-001",
                "name": "dense population area",
                "gridIds": ["G-10-11", "G-10-12", "G-11-11", "G-11-12"],
                "riskWeight": 0.65,
                "riskType": "DENSE_POPULATION",
            }
        ],
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(map_data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
