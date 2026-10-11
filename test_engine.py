from __future__ import annotations

import math

from dks_model.engine import run_model
from dks_model.io import load_inputs


def test_base_model_reconciles() -> None:
    inputs = load_inputs("inputs")
    outputs = run_model(inputs, scenario="base")
    consolidated = outputs.tables["integrated_financials"]

    assert outputs.audit_status == "PASS"
    assert len(consolidated) == 5
    assert (consolidated["revenue"] > 0).all()
    assert (consolidated["total_assets"] - consolidated["total_liabilities_plus_equity"]).abs().max() < 0.01


def test_scenarios_produce_distinct_values() -> None:
    inputs = load_inputs("inputs")
    bull = run_model(inputs, scenario="bull").tables["valuation"]
    bear = run_model(inputs, scenario="bear").tables["valuation"]
    bull_price = float(bull.loc[bull["method"] == "DCF", "price_per_share"].iloc[0])
    bear_price = float(bear.loc[bear["method"] == "DCF", "price_per_share"].iloc[0])

    assert bull_price > bear_price


def test_quarterly_reconciles_to_annual() -> None:
    inputs = load_inputs("inputs")
    outputs = run_model(inputs, scenario="base")
    quarterly = outputs.tables["quarterly_forecast"]
    annual = outputs.tables["integrated_financials"]

    for year in inputs.periods.quarterly_years:
        assert math.isclose(
            quarterly.loc[quarterly["fiscal_year"] == year, "revenue"].sum(),
            annual.loc[year, "revenue"],
            abs_tol=0.01,
        )


def test_reverse_dcf_has_expected_columns() -> None:
    inputs = load_inputs("inputs")
    outputs = run_model(inputs, scenario="base")
    reverse = outputs.tables["reverse_dcf"]

    assert "required_foot_locker_terminal_operating_margin" in reverse.columns
    assert reverse.loc[0, "solve_status"] in {"solved", "not bracketed"}


def test_probabilistic_valuation_is_reproducible_and_ordered() -> None:
    inputs = load_inputs("inputs")
    first = run_model(inputs, scenario="base").tables["probabilistic_valuation"]
    second = run_model(inputs, scenario="base").tables["probabilistic_valuation"]

    assert first.loc[0, "status"] == "enabled"
    assert first.loc[0, "mean_price"] == second.loc[0, "mean_price"]
    assert first.loc[0, "p10_price"] <= first.loc[0, "median_price"] <= first.loc[0, "p90_price"]
    assert 0 <= first.loc[0, "probability_positive_return"] <= 1
    assert 0 <= first.loc[0, "probability_capital_loss"] <= 1


def test_catalyst_status_classification() -> None:
    inputs = load_inputs("inputs")
    catalysts = run_model(inputs, scenario="base").tables["catalyst_monitoring"]

    statuses = set(catalysts["status"])
    assert {"bullish", "bearish", "neutral", "pending"}.issubset(statuses)


def test_forecast_variance_math() -> None:
    inputs = load_inputs("inputs")
    variance = run_model(inputs, scenario="base").tables["forecast_variance"]
    revenue = variance.loc[variance["metric"] == "revenue"].iloc[0]

    assert math.isclose(revenue["variance"], revenue["actual"] - revenue["prior_forecast"], abs_tol=0.001)
    assert math.isclose(revenue["variance_pct"], revenue["variance"] / abs(revenue["prior_forecast"]), abs_tol=0.000001)


def test_phase2_disabled_inputs_do_not_break_model() -> None:
    inputs = load_inputs("inputs")
    disabled = inputs.model_copy(deep=True)
    disabled.probabilistic_valuation.enabled = False
    disabled.thesis_catalysts = []
    disabled.forecast_variance = []

    outputs = run_model(disabled, scenario="base")

    assert outputs.tables["probabilistic_valuation"].loc[0, "status"] == "disabled"
    assert outputs.tables["catalyst_monitoring"].loc[0, "status"] == "not configured"
    assert outputs.tables["forecast_variance"].loc[0, "status"] == "not configured"
