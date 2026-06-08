from app.energy.energy_estimator import estimate_energy_usage


def test_estimate_energy_usage_uses_distance_turn_and_risk_penalty():
    estimate = estimate_energy_usage(
        distance_meters=1000,
        turn_count=2,
        risk_grid_count=3,
    )

    assert estimate.estimated_battery_usage == 7.2
    assert estimate.battery_limit == 80.0
    assert estimate.energy_safe


def test_estimate_energy_usage_marks_unsafe_when_over_limit():
    estimate = estimate_energy_usage(
        distance_meters=20000,
        turn_count=0,
        risk_grid_count=0,
    )

    assert estimate.estimated_battery_usage == 120.0
    assert not estimate.energy_safe
