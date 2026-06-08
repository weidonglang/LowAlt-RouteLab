import pytest

from app.utils.grid_id import is_valid_grid_id, parse_grid_id, to_grid_id


def test_to_grid_id_formats_coordinates():
    assert to_grid_id(1, 1) == "G-01-01"
    assert to_grid_id(20, 20) == "G-20-20"


def test_to_grid_id_rejects_non_positive_coordinates():
    with pytest.raises(ValueError):
        to_grid_id(0, 1)


def test_parse_grid_id_returns_coordinates():
    assert parse_grid_id("G-03-15") == (3, 15)


def test_parse_grid_id_rejects_invalid_format():
    with pytest.raises(ValueError):
        parse_grid_id("G-3-15")


def test_is_valid_grid_id_checks_bounds():
    assert is_valid_grid_id("G-20-20", 20, 20)
    assert not is_valid_grid_id("G-21-20", 20, 20)
    assert not is_valid_grid_id("bad", 20, 20)

