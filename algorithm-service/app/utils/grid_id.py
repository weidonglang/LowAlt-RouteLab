import re


GRID_ID_PATTERN = re.compile(r"^G-(\d{2})-(\d{2})$")


def to_grid_id(x: int, y: int) -> str:
    if x <= 0 or y <= 0:
        raise ValueError("grid coordinates must be positive")
    return f"G-{x:02d}-{y:02d}"


def parse_grid_id(grid_id: str) -> tuple[int, int]:
    match = GRID_ID_PATTERN.match(grid_id)
    if not match:
        raise ValueError(f"invalid grid id: {grid_id}")
    return int(match.group(1)), int(match.group(2))


def is_valid_grid_id(grid_id: str, width: int, height: int) -> bool:
    try:
        x, y = parse_grid_id(grid_id)
    except ValueError:
        return False
    return 1 <= x <= width and 1 <= y <= height

