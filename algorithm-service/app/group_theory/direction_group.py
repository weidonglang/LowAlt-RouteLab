from app.utils.grid_id import parse_grid_id


N = 0
NE = 1
E = 2
SE = 3
S = 4
SW = 5
W = 6
NW = 7


_VECTOR_TO_DIRECTION = {
    (0, -1): N,
    (1, -1): NE,
    (1, 0): E,
    (1, 1): SE,
    (0, 1): S,
    (-1, 1): SW,
    (-1, 0): W,
    (-1, -1): NW,
}


def direction_between(a: tuple[int, int], b: tuple[int, int]) -> int:
    dx = _normalize_step(b[0] - a[0])
    dy = _normalize_step(b[1] - a[1])
    try:
        return _VECTOR_TO_DIRECTION[(dx, dy)]
    except KeyError as exc:
        raise ValueError(f"points do not define a C8 direction: {a} -> {b}") from exc


def direction_between_grid_ids(a_grid_id: str, b_grid_id: str) -> int:
    return direction_between(parse_grid_id(a_grid_id), parse_grid_id(b_grid_id))


def turn_steps(d1: int, d2: int) -> int:
    _validate_direction(d1)
    _validate_direction(d2)
    delta = abs(d2 - d1)
    return min(delta, 8 - delta)


def turn_angle_degrees(d1: int, d2: int) -> int:
    return turn_steps(d1, d2) * 45


def turn_cost(d1: int, d2: int, weight: float = 1.0) -> float:
    return turn_steps(d1, d2) * weight


def _normalize_step(delta: int) -> int:
    if delta > 0:
        return 1
    if delta < 0:
        return -1
    return 0


def _validate_direction(direction: int) -> None:
    if not 0 <= direction <= 7:
        raise ValueError(f"invalid C8 direction: {direction}")

