from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr

from dks_model.schemas import AuditFinding, ModelInputs, ModelOutputs


def run_model(inputs: ModelInputs, scenario: str = "base") -> ModelOutputs:
    if scenario not in inputs.scenarios:
        raise ValueError(f"Unknown scenario '{scenario}'. Available: {sorted(inputs.scenarios)}")

    assumptions = inputs.scenarios[scenario]
    years = inputs.periods.forecast_years

    legacy = _segment_forecast(
        years,
        inputs.segments["legacy_dicks"],
        assumptions.legacy_comp_growth,
        assumptions.legacy_gross_margin,
        assumptions.legacy_opex_pct,
    )
    foot_locker = _segment_forecast(
        years,
        inputs.segments["foot_locker"],
        assumptions.foot_locker_comp_growth,
        assumptions.foot_locker_gross_margin,
        assumptions.foot_locker_opex_pct,
    )
    cohorts = _foot_locker_cohorts(years, inputs.foot_locker_cohorts)
    synergies = _synergy_waterfall(years, inputs.synergies)
    consolidated = _integrated_statements(inputs, assumptions, legacy, foot_locker, synergies)
    quarterly = _quarterly_forecast(inputs, consolidated)
    valuation = _valuation(inputs, assumptions, legacy, foot_locker, synergies, consolidated)
    reverse_dcf = _reverse_dcf(inputs, scenario)
    sensitivities = _sensitivity_table(inputs, scenario)
    probabilistic_valuation, monte_carlo_trials = _probabilistic_valuation(inputs, scenario)
    catalyst_monitoring = _catalyst_monitoring(inputs)
    forecast_variance = _forecast_variance(inputs)
    sources = pd.DataFrame([source.model_dump(mode="json") for source in inputs.source_registry])

    tables = {
        "historical_financials": _historical_table(inputs),
        "legacy_operating_model": legacy,
        "foot_locker_operating_model": foot_locker,
        "foot_locker_store_cohorts": cohorts,
        "synergy_waterfall": synergies,
        "integrated_financials": consolidated,
        "quarterly_forecast": quarterly,
        "valuation": valuation,
        "reverse_dcf": reverse_dcf,
        "sensitivities": sensitivities,
        "probabilistic_valuation": probabilistic_valuation,
        "monte_carlo_trials": monte_carlo_trials,
        "catalyst_monitoring": catalyst_monitoring,
        "forecast_variance": forecast_variance,
        "sources": sources,
        "scenario_summary": _scenario_summary(inputs),
    }
    audit_findings = _audit(inputs, tables)
    return ModelOutputs(scenario=scenario, tables=tables, audit_findings=audit_findings)


def _historical_table(inputs: ModelInputs) -> pd.DataFrame:
    rows = []
    for year in inputs.periods.historical_years:
        item = inputs.historical[year]
        row = item.model_dump()
        row["period"] = year
        row["gross_margin"] = item.gross_profit / item.revenue
        row["ebit_margin"] = item.ebit / item.revenue
        row["fcf"] = item.operating_cash_flow - item.capex
        rows.append(row)
    return pd.DataFrame(rows).set_index("period")


def _segment_forecast(
    years: list[str],
    segment,
    comp_growth: list[float],
    gross_margin: list[float],
    opex_pct: list[float],
) -> pd.DataFrame:
    rows = []
    stores_begin = segment.starting_store_count
    sales_per_store = segment.starting_sales_per_store
    digital_revenue = segment.starting_digital_revenue
    for idx, year in enumerate(years):
        openings = segment.openings[idx]
        closures = segment.closures[idx]
        stores_end = max(stores_begin + openings - closures, 0)
        average_stores = (stores_begin + stores_end) / 2
        sales_per_store *= 1 + comp_growth[idx]
        digital_revenue *= 1 + segment.digital_growth[idx]
        store_revenue = average_stores * sales_per_store
        revenue = store_revenue + digital_revenue
        gross_profit = revenue * gross_margin[idx]
        opex = revenue * opex_pct[idx]
        operating_income = gross_profit - opex
        capex = stores_end * segment.maintenance_capex_per_store + openings * segment.growth_capex_per_opening
        rows.append(
            {
                "period": year,
                "beginning_stores": stores_begin,
                "openings": openings,
                "closures": closures,
                "ending_stores": stores_end,
                "average_stores": average_stores,
                "sales_per_store": sales_per_store,
                "store_revenue": store_revenue,
                "digital_revenue": digital_revenue,
                "revenue": revenue,
                "gross_margin": gross_margin[idx],
                "gross_profit": gross_profit,
                "opex_pct": opex_pct[idx],
                "operating_expense": opex,
                "operating_income": operating_income,
                "operating_margin": operating_income / revenue if revenue else np.nan,
                "segment_capex": capex,
            }
        )
        stores_begin = stores_end
    return pd.DataFrame(rows).set_index("period")


def _foot_locker_cohorts(years: list[str], cohorts) -> pd.DataFrame:
    rows = []
    for cohort in cohorts:
        stores_begin = cohort.store_count
        sales_per_store = cohort.sales_per_store
        cumulative_transferred_sales = 0.0
        for idx, year in enumerate(years):
            closures = min(cohort.closures[idx], stores_begin)
            stores_end = max(stores_begin - closures, 0)
            average_stores = (stores_begin + stores_end) / 2
            sales_per_store *= 1 + cohort.annual_comp_growth[idx]
            lost_sales = closures * sales_per_store
            retained_sales = lost_sales * cohort.retained_sales_pct
            cumulative_transferred_sales += retained_sales
            revenue = average_stores * sales_per_store + cumulative_transferred_sales
            contribution_profit = revenue * cohort.contribution_margin[idx]
            closure_cost = closures * cohort.closure_cost_per_store
            rows.append(
                {
                    "cohort": cohort.name,
                    "period": year,
                    "beginning_stores": stores_begin,
                    "closures": closures,
                    "ending_stores": stores_end,
                    "sales_per_store": sales_per_store,
                    "retained_sales": retained_sales,
                    "revenue": revenue,
                    "contribution_margin": cohort.contribution_margin[idx],
                    "contribution_profit": contribution_profit,
                    "closure_cost": closure_cost,
                    "cash_flow_after_closure_cost": contribution_profit - closure_cost,
                }
            )
            stores_begin = stores_end
    return pd.DataFrame(rows)


def _synergy_waterfall(years: list[str], synergies) -> pd.DataFrame:
    rows = []
    for synergy in synergies:
        for idx, year in enumerate(years):
            gross_savings = synergy.max_annual_savings * synergy.realization_rates[idx]
            risk_adjusted_savings = gross_savings * synergy.probability
            recurring_cost = synergy.recurring_costs[idx]
            net_recurring_benefit = risk_adjusted_savings - recurring_cost
            implementation_cost = synergy.implementation_costs[idx]
            rows.append(
                {
                    "initiative": synergy.name,
                    "period": year,
                    "max_annual_savings": synergy.max_annual_savings,
                    "realization_rate": synergy.realization_rates[idx],
                    "probability": synergy.probability,
                    "gross_savings": gross_savings,
                    "risk_adjusted_savings": risk_adjusted_savings,
                    "recurring_cost": recurring_cost,
                    "net_recurring_benefit": net_recurring_benefit,
                    "implementation_cost": implementation_cost,
                    "net_cash_benefit": net_recurring_benefit - implementation_cost,
                }
            )
    return pd.DataFrame(rows)


def _integrated_statements(inputs: ModelInputs, assumptions, legacy: pd.DataFrame, foot_locker: pd.DataFrame, synergies: pd.DataFrame) -> pd.DataFrame:
    rows = []
    years = inputs.periods.forecast_years
    bs = inputs.balance_sheet_start
    beginning_cash = bs.cash
    beginning_debt = bs.debt
    beginning_ppe = bs.ppe
    beginning_nwc = bs.operating_nwc
    beginning_shares = assumptions.diluted_share_base
    beginning_lease_liabilities = bs.lease_liabilities

    for idx, year in enumerate(years):
        total_revenue = legacy.loc[year, "revenue"] + foot_locker.loc[year, "revenue"]
        legacy_oi = legacy.loc[year, "operating_income"]
        fl_oi = foot_locker.loc[year, "operating_income"]
        synergy_benefit = synergies.loc[synergies["period"] == year, "net_recurring_benefit"].sum()
        integration_cost = synergies.loc[synergies["period"] == year, "implementation_cost"].sum()
        corporate_expense = total_revenue * assumptions.corporate_expense_pct[idx]
        ebit = legacy_oi + fl_oi + synergy_benefit - corporate_expense - integration_cost
        depreciation = total_revenue * assumptions.depreciation_pct_revenue[idx]
        ebitda = ebit + depreciation
        interest_expense = beginning_debt * assumptions.interest_rate[idx]
        pretax_income = ebit - interest_expense
        taxes = max(pretax_income, 0) * inputs.control.tax_rate
        net_income = pretax_income - taxes
        capex = max(total_revenue * assumptions.capex_pct_revenue[idx], legacy.loc[year, "segment_capex"] + foot_locker.loc[year, "segment_capex"])
        ending_nwc = total_revenue * assumptions.operating_nwc_pct_revenue[idx]
        change_nwc = ending_nwc - beginning_nwc
        fcff = ebit * (1 - inputs.control.tax_rate) + depreciation - capex - change_nwc
        debt_repayment = min(beginning_debt, assumptions.debt_repayment[idx])
        ending_debt = beginning_debt - debt_repayment
        dividends = assumptions.dividends[idx]
        repurchases = assumptions.share_repurchases[idx]
        repurchased_shares = repurchases / assumptions.avg_repurchase_price[idx] if assumptions.avg_repurchase_price[idx] else 0.0
        diluted_shares = max(beginning_shares + assumptions.stock_comp_dilution[idx] - repurchased_shares, 1.0)
        eps = net_income / diluted_shares
        ending_ppe = max(beginning_ppe + capex - depreciation, 0.0)
        lease_payment = beginning_lease_liabilities * 0.075
        ending_lease_liabilities = max(beginning_lease_liabilities - lease_payment, 0.0)
        operating_cash_flow = net_income + depreciation - change_nwc
        fcf_to_equity_before_capital_return = operating_cash_flow - capex - debt_repayment - lease_payment
        ending_cash = beginning_cash + fcf_to_equity_before_capital_return - dividends - repurchases
        minimum_cash = 500.0
        debt_issuance = max(minimum_cash - ending_cash, 0.0)
        if debt_issuance:
            ending_debt += debt_issuance
            ending_cash = minimum_cash
        total_assets = ending_cash + ending_nwc + ending_ppe + bs.goodwill_and_intangibles
        total_liabilities = ending_debt + ending_lease_liabilities + bs.other_liabilities
        shareholders_equity = total_assets - total_liabilities
        invested_capital = ending_debt + ending_lease_liabilities + shareholders_equity - ending_cash
        nopat = ebit * (1 - inputs.control.tax_rate)
        roic = nopat / invested_capital if invested_capital else np.nan
        economic_profit = nopat - inputs.control.wacc * invested_capital

        rows.append(
            {
                "period": year,
                "legacy_revenue": legacy.loc[year, "revenue"],
                "foot_locker_revenue": foot_locker.loc[year, "revenue"],
                "revenue": total_revenue,
                "legacy_operating_income": legacy_oi,
                "foot_locker_operating_income": fl_oi,
                "synergy_benefit": synergy_benefit,
                "corporate_expense": corporate_expense,
                "integration_cost": integration_cost,
                "ebit": ebit,
                "depreciation": depreciation,
                "ebitda": ebitda,
                "interest_expense": interest_expense,
                "pretax_income": pretax_income,
                "taxes": taxes,
                "net_income": net_income,
                "diluted_shares": diluted_shares,
                "eps": eps,
                "capex": capex,
                "operating_nwc": ending_nwc,
                "change_nwc": change_nwc,
                "operating_cash_flow": operating_cash_flow,
                "fcff": fcff,
                "fcf_to_equity_before_capital_return": fcf_to_equity_before_capital_return,
                "dividends": dividends,
                "share_repurchases": repurchases,
                "cash": ending_cash,
                "ppe": ending_ppe,
                "goodwill_and_intangibles": bs.goodwill_and_intangibles,
                "debt": ending_debt,
                "debt_issuance": debt_issuance,
                "debt_repayment": debt_repayment,
                "lease_liabilities": ending_lease_liabilities,
                "other_liabilities": bs.other_liabilities,
                "shareholders_equity": shareholders_equity,
                "total_assets": total_assets,
                "total_liabilities_plus_equity": total_liabilities + shareholders_equity,
                "net_debt": ending_debt + ending_lease_liabilities - ending_cash,
                "invested_capital": invested_capital,
                "nopat": nopat,
                "roic": roic,
                "economic_profit": economic_profit,
            }
        )
        beginning_cash = ending_cash
        beginning_debt = ending_debt
        beginning_ppe = ending_ppe
        beginning_nwc = ending_nwc
        beginning_shares = diluted_shares
        beginning_lease_liabilities = ending_lease_liabilities

    return pd.DataFrame(rows).set_index("period")


def _quarterly_forecast(inputs: ModelInputs, consolidated: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for year in inputs.periods.quarterly_years:
        annual = consolidated.loc[year]
        for q_idx, weight in enumerate(inputs.periods.quarter_weights, start=1):
            rows.append(
                {
                    "period": f"{year} Q{q_idx}",
                    "fiscal_year": year,
                    "quarter": q_idx,
                    "revenue": annual["revenue"] * weight,
                    "ebit": annual["ebit"] * weight,
                    "net_income": annual["net_income"] * weight,
                    "fcff": annual["fcff"] * weight,
                    "actual_or_forecast": "forecast",
                }
            )
    return pd.DataFrame(rows).set_index("period")


def _valuation(inputs: ModelInputs, assumptions, legacy: pd.DataFrame, foot_locker: pd.DataFrame, synergies: pd.DataFrame, consolidated: pd.DataFrame) -> pd.DataFrame:
    discount_periods = np.arange(1, len(consolidated) + 1)
    fcff = consolidated["fcff"].to_numpy(dtype=float)
    wacc = inputs.control.wacc
    terminal_growth = inputs.control.terminal_growth
    terminal_value = fcff[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    pv_fcff = float(np.sum(fcff / (1 + wacc) ** discount_periods))
    pv_terminal = float(terminal_value / (1 + wacc) ** len(fcff))
    enterprise_value = pv_fcff + pv_terminal
    final = consolidated.iloc[-1]
    equity_value = enterprise_value - final["net_debt"]
    dcf_price = equity_value / final["diluted_shares"]

    legacy_ebitda = legacy.iloc[-1]["operating_income"] + final["depreciation"] * (legacy.iloc[-1]["revenue"] / final["revenue"])
    fl_ebitda = foot_locker.iloc[-1]["operating_income"] + final["depreciation"] * (foot_locker.iloc[-1]["revenue"] / final["revenue"])
    final_synergy = synergies.loc[synergies["period"] == consolidated.index[-1], "net_recurring_benefit"].sum()
    sotp_ev = (
        legacy_ebitda * inputs.valuation.legacy_ebitda_multiple
        + fl_ebitda * inputs.valuation.foot_locker_ebitda_multiple
        + final_synergy * inputs.valuation.synergy_ebitda_multiple
    )
    sotp_price = (sotp_ev - final["net_debt"]) / final["diluted_shares"]
    relative_pe_price = consolidated.iloc[1]["eps"] * inputs.valuation.relative_pe_multiple
    relative_fcf_price = (consolidated.iloc[1]["fcff"] / inputs.valuation.relative_fcf_yield - final["net_debt"]) / final["diluted_shares"]
    scenario_weighted = _scenario_weighted_value(inputs)

    rows = [
        {"method": "DCF", "enterprise_value": enterprise_value, "equity_value": equity_value, "price_per_share": dcf_price},
        {"method": "SOTP", "enterprise_value": sotp_ev, "equity_value": sotp_ev - final["net_debt"], "price_per_share": sotp_price},
        {"method": "Relative P/E", "enterprise_value": np.nan, "equity_value": np.nan, "price_per_share": relative_pe_price},
        {"method": "Relative FCF Yield", "enterprise_value": np.nan, "equity_value": np.nan, "price_per_share": relative_fcf_price},
        {"method": "Scenario-weighted DCF", "enterprise_value": np.nan, "equity_value": np.nan, "price_per_share": scenario_weighted},
    ]
    return pd.DataFrame(rows)


def _scenario_weighted_value(inputs: ModelInputs) -> float:
    weighted = 0.0
    total_probability = 0.0
    for name, scenario in inputs.scenarios.items():
        output = _run_model_no_scenario_weight(inputs, name)
        price = float(output.tables["valuation"].loc[output.tables["valuation"]["method"] == "DCF", "price_per_share"].iloc[0])
        weighted += scenario.scenario_probability * price
        total_probability += scenario.scenario_probability
    return weighted / total_probability if total_probability else np.nan


def _run_model_no_scenario_weight(inputs: ModelInputs, scenario: str) -> ModelOutputs:
    assumptions = inputs.scenarios[scenario]
    years = inputs.periods.forecast_years
    legacy = _segment_forecast(years, inputs.segments["legacy_dicks"], assumptions.legacy_comp_growth, assumptions.legacy_gross_margin, assumptions.legacy_opex_pct)
    foot_locker = _segment_forecast(years, inputs.segments["foot_locker"], assumptions.foot_locker_comp_growth, assumptions.foot_locker_gross_margin, assumptions.foot_locker_opex_pct)
    synergies = _synergy_waterfall(years, inputs.synergies)
    consolidated = _integrated_statements(inputs, assumptions, legacy, foot_locker, synergies)
    valuation = _valuation_without_weighted(inputs, legacy, foot_locker, synergies, consolidated)
    return ModelOutputs(scenario=scenario, tables={"valuation": valuation}, audit_findings=[])


def _valuation_without_weighted(inputs: ModelInputs, legacy: pd.DataFrame, foot_locker: pd.DataFrame, synergies: pd.DataFrame, consolidated: pd.DataFrame) -> pd.DataFrame:
    discount_periods = np.arange(1, len(consolidated) + 1)
    fcff = consolidated["fcff"].to_numpy(dtype=float)
    terminal_value = fcff[-1] * (1 + inputs.control.terminal_growth) / (inputs.control.wacc - inputs.control.terminal_growth)
    enterprise_value = float(np.sum(fcff / (1 + inputs.control.wacc) ** discount_periods) + terminal_value / (1 + inputs.control.wacc) ** len(fcff))
    final = consolidated.iloc[-1]
    equity_value = enterprise_value - final["net_debt"]
    return pd.DataFrame([{"method": "DCF", "enterprise_value": enterprise_value, "equity_value": equity_value, "price_per_share": equity_value / final["diluted_shares"]}])


def _reverse_dcf(inputs: ModelInputs, scenario: str) -> pd.DataFrame:
    target_price = inputs.control.reference_share_price
    base_assumptions = inputs.scenarios[scenario].model_copy(deep=True)

    def solve_price(final_fl_margin: float) -> float:
        adjusted = base_assumptions.model_copy(deep=True)
        start_margin = adjusted.foot_locker_gross_margin[0] - adjusted.foot_locker_opex_pct[0]
        margin_path = np.linspace(start_margin, final_fl_margin, len(adjusted.foot_locker_gross_margin))
        adjusted.foot_locker_gross_margin = [float(m + adjusted.foot_locker_opex_pct[i]) for i, m in enumerate(margin_path)]
        legacy = _segment_forecast(inputs.periods.forecast_years, inputs.segments["legacy_dicks"], adjusted.legacy_comp_growth, adjusted.legacy_gross_margin, adjusted.legacy_opex_pct)
        foot_locker = _segment_forecast(inputs.periods.forecast_years, inputs.segments["foot_locker"], adjusted.foot_locker_comp_growth, adjusted.foot_locker_gross_margin, adjusted.foot_locker_opex_pct)
        synergies = _synergy_waterfall(inputs.periods.forecast_years, inputs.synergies)
        consolidated = _integrated_statements(inputs, adjusted, legacy, foot_locker, synergies)
        valuation = _valuation_without_weighted(inputs, legacy, foot_locker, synergies, consolidated)
        return float(valuation.loc[0, "price_per_share"])

    try:
        required_margin = brentq(lambda margin: solve_price(margin) - target_price, -0.1, 0.18)
        status = "solved"
    except ValueError:
        required_margin = math.nan
        status = "not bracketed"

    return pd.DataFrame(
        [
            {
                "target_reference_price": target_price,
                "required_foot_locker_terminal_operating_margin": required_margin,
                "base_case_terminal_foot_locker_operating_margin": base_assumptions.foot_locker_gross_margin[-1] - base_assumptions.foot_locker_opex_pct[-1],
                "solve_status": status,
            }
        ]
    )


def _sensitivity_table(inputs: ModelInputs, scenario: str) -> pd.DataFrame:
    base_wacc = inputs.control.wacc
    base_growth = inputs.control.terminal_growth
    rows = []
    for wacc_delta in [-0.01, 0.0, 0.01]:
        for growth_delta in [-0.005, 0.0, 0.005]:
            cloned = inputs.model_copy(deep=True)
            cloned.control.wacc = base_wacc + wacc_delta
            cloned.control.terminal_growth = base_growth + growth_delta
            if cloned.control.wacc <= cloned.control.terminal_growth:
                price = np.nan
            else:
                output = _run_model_no_scenario_weight(cloned, scenario)
                price = float(output.tables["valuation"].loc[0, "price_per_share"])
            rows.append(
                {
                    "wacc": cloned.control.wacc,
                    "terminal_growth": cloned.control.terminal_growth,
                    "price_per_share": price,
                    "upside_downside": price / inputs.control.reference_share_price - 1 if price == price else np.nan,
                }
            )
    return pd.DataFrame(rows)


def _probabilistic_valuation(inputs: ModelInputs, scenario: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    config = inputs.probabilistic_valuation
    if config is None or not config.enabled or not config.variables:
        summary = pd.DataFrame(
            [
                {
                    "status": "disabled",
                    "iterations": 0,
                    "mean_price": np.nan,
                    "median_price": np.nan,
                    "p10_price": np.nan,
                    "p90_price": np.nan,
                    "probability_positive_return": np.nan,
                    "probability_capital_loss": np.nan,
                    "downside_tail_valuation": np.nan,
                    "expected_return": np.nan,
                }
            ]
        )
        return summary, pd.DataFrame(columns=["trial", "price_per_share"])

    rng = np.random.default_rng(config.random_seed)
    variable_names = [variable.name for variable in config.variables]
    standard_normals = _correlated_normals(rng, variable_names, config.correlations, config.iterations)
    trial_rows = []

    for trial_idx in range(config.iterations):
        sampled = {
            variable.name: _sample_variable(variable, standard_normals[trial_idx, var_idx])
            for var_idx, variable in enumerate(config.variables)
        }
        trial_inputs = _apply_trial_assumptions(inputs, scenario, sampled)
        valuation = _run_model_no_scenario_weight(trial_inputs, scenario).tables["valuation"]
        price = float(valuation.loc[valuation["method"] == "DCF", "price_per_share"].iloc[0])
        trial_rows.append({"trial": trial_idx + 1, "price_per_share": price, **sampled})

    trials = pd.DataFrame(trial_rows)
    prices = trials["price_per_share"]
    reference_price = inputs.control.reference_share_price
    downside_tail = prices.loc[prices <= prices.quantile(0.1)].mean()
    summary = pd.DataFrame(
        [
            {
                "status": "enabled",
                "iterations": config.iterations,
                "mean_price": prices.mean(),
                "median_price": prices.median(),
                "p10_price": prices.quantile(0.1),
                "p90_price": prices.quantile(0.9),
                "probability_positive_return": (prices > reference_price).mean(),
                "probability_capital_loss": (prices < reference_price).mean(),
                "downside_tail_valuation": downside_tail,
                "expected_return": prices.mean() / reference_price - 1,
            }
        ]
    )
    return summary, trials


def _correlated_normals(rng: np.random.Generator, variable_names: list[str], correlations, iterations: int) -> np.ndarray:
    size = len(variable_names)
    matrix = np.eye(size)
    positions = {name: idx for idx, name in enumerate(variable_names)}
    for item in correlations:
        if item.left in positions and item.right in positions:
            left_idx = positions[item.left]
            right_idx = positions[item.right]
            matrix[left_idx, right_idx] = item.correlation
            matrix[right_idx, left_idx] = item.correlation
    try:
        return rng.multivariate_normal(np.zeros(size), matrix, size=iterations)
    except np.linalg.LinAlgError:
        adjusted = matrix + np.eye(size) * 1e-6
        return rng.multivariate_normal(np.zeros(size), adjusted, size=iterations)


def _sample_variable(variable, standard_normal: float) -> float:
    if variable.distribution == "normal":
        value = variable.mean + variable.stdev * standard_normal
    else:
        value = _triangular_ppf(float(ndtr(standard_normal)), variable.low, variable.mode, variable.high)
    if variable.min_value is not None:
        value = max(value, variable.min_value)
    if variable.max_value is not None:
        value = min(value, variable.max_value)
    return float(value)


def _triangular_ppf(probability: float, low: float, mode: float, high: float) -> float:
    if high == low:
        return float(low)
    breakpoint = (mode - low) / (high - low)
    if probability < breakpoint:
        return float(low + math.sqrt(probability * (high - low) * (mode - low)))
    return float(high - math.sqrt((1 - probability) * (high - low) * (high - mode)))


def _apply_trial_assumptions(inputs: ModelInputs, scenario: str, sampled: dict[str, float]) -> ModelInputs:
    cloned = inputs.model_copy(deep=True)
    assumptions = cloned.scenarios[scenario]

    if "legacy_comp_growth_delta" in sampled:
        assumptions.legacy_comp_growth = [value + sampled["legacy_comp_growth_delta"] for value in assumptions.legacy_comp_growth]
    if "gross_margin_delta" in sampled:
        assumptions.legacy_gross_margin = [value + sampled["gross_margin_delta"] for value in assumptions.legacy_gross_margin]
        assumptions.foot_locker_gross_margin = [value + sampled["gross_margin_delta"] for value in assumptions.foot_locker_gross_margin]
    if "nwc_pct_delta" in sampled:
        assumptions.operating_nwc_pct_revenue = [max(value + sampled["nwc_pct_delta"], 0.0) for value in assumptions.operating_nwc_pct_revenue]
    if "foot_locker_terminal_margin" in sampled:
        start_margin = assumptions.foot_locker_gross_margin[0] - assumptions.foot_locker_opex_pct[0]
        margin_path = np.linspace(start_margin, sampled["foot_locker_terminal_margin"], len(assumptions.foot_locker_gross_margin))
        assumptions.foot_locker_gross_margin = [
            float(margin + assumptions.foot_locker_opex_pct[idx]) for idx, margin in enumerate(margin_path)
        ]
    if "synergy_realization_multiplier" in sampled:
        multiplier = sampled["synergy_realization_multiplier"]
        for synergy in cloned.synergies:
            synergy.realization_rates = [min(max(rate * multiplier, 0.0), 1.0) for rate in synergy.realization_rates]
    if "wacc" in sampled:
        cloned.control.wacc = sampled["wacc"]
    if "terminal_growth" in sampled:
        cloned.control.terminal_growth = sampled["terminal_growth"]
    if cloned.control.wacc <= cloned.control.terminal_growth:
        cloned.control.wacc = cloned.control.terminal_growth + 0.005
    return cloned


def _catalyst_monitoring(inputs: ModelInputs) -> pd.DataFrame:
    if not inputs.thesis_catalysts:
        return pd.DataFrame(
            [
                {
                    "status": "not configured",
                    "name": "No thesis catalysts supplied",
                    "expected_timing": "",
                    "metric": "",
                    "model_forecast": np.nan,
                    "latest_value": np.nan,
                    "bullish_threshold": np.nan,
                    "bearish_threshold": np.nan,
                    "thesis_implication": "Add manual catalysts to model_inputs.json.",
                }
            ]
        )

    rows = []
    for catalyst in inputs.thesis_catalysts:
        if catalyst.latest_value is None:
            status = "pending"
        elif catalyst.higher_is_better:
            if catalyst.latest_value >= catalyst.bullish_threshold:
                status = "bullish"
            elif catalyst.latest_value <= catalyst.bearish_threshold:
                status = "bearish"
            else:
                status = "neutral"
        else:
            if catalyst.latest_value <= catalyst.bullish_threshold:
                status = "bullish"
            elif catalyst.latest_value >= catalyst.bearish_threshold:
                status = "bearish"
            else:
                status = "neutral"
        rows.append(
            {
                "status": status,
                "name": catalyst.name,
                "expected_timing": catalyst.expected_timing,
                "metric": catalyst.metric,
                "model_forecast": catalyst.model_forecast,
                "latest_value": catalyst.latest_value,
                "bullish_threshold": catalyst.bullish_threshold,
                "bearish_threshold": catalyst.bearish_threshold,
                "higher_is_better": catalyst.higher_is_better,
                "thesis_implication": catalyst.thesis_implication,
            }
        )
    return pd.DataFrame(rows)


def _forecast_variance(inputs: ModelInputs) -> pd.DataFrame:
    if not inputs.forecast_variance:
        return pd.DataFrame(
            [
                {
                    "status": "not configured",
                    "snapshot_name": "No prior forecast snapshots supplied",
                    "period": "",
                    "metric": "",
                    "prior_forecast": np.nan,
                    "actual": np.nan,
                    "variance": np.nan,
                    "variance_pct": np.nan,
                    "attribution_driver": "Add manual snapshots to model_inputs.json.",
                }
            ]
        )

    rows = []
    for item in inputs.forecast_variance:
        if item.actual is None:
            variance = np.nan
            variance_pct = np.nan
            status = "pending"
        else:
            variance = item.actual - item.prior_forecast
            variance_pct = variance / abs(item.prior_forecast) if item.prior_forecast else np.nan
            status = "above forecast" if variance > 0 else "below forecast" if variance < 0 else "in line"
        rows.append(
            {
                "status": status,
                "snapshot_name": item.snapshot_name,
                "period": item.period,
                "metric": item.metric,
                "prior_forecast": item.prior_forecast,
                "actual": item.actual,
                "variance": variance,
                "variance_pct": variance_pct,
                "attribution_driver": item.attribution_driver,
            }
        )
    return pd.DataFrame(rows)


def _scenario_summary(inputs: ModelInputs) -> pd.DataFrame:
    rows = []
    for scenario, assumptions in inputs.scenarios.items():
        output = _run_model_no_scenario_weight(inputs, scenario)
        dcf_price = float(output.tables["valuation"].loc[0, "price_per_share"])
        rows.append(
            {
                "scenario": scenario,
                "probability": assumptions.scenario_probability,
                "dcf_price_per_share": dcf_price,
                "expected_contribution": assumptions.scenario_probability * dcf_price,
                "upside_downside": dcf_price / inputs.control.reference_share_price - 1,
            }
        )
    return pd.DataFrame(rows)


def _audit(inputs: ModelInputs, tables: dict[str, pd.DataFrame]) -> list[AuditFinding]:
    findings: list[AuditFinding] = []
    consolidated = tables["integrated_financials"]
    balance_delta = (consolidated["total_assets"] - consolidated["total_liabilities_plus_equity"]).abs().max()
    findings.append(_finding("Balance sheet balances", balance_delta < 0.01, f"Maximum balance delta is {balance_delta:,.4f}."))

    quarterly = tables["quarterly_forecast"]
    annual_quarterly_delta = 0.0
    for year in inputs.periods.quarterly_years:
        quarterly_revenue = quarterly.loc[quarterly["fiscal_year"] == year, "revenue"].sum()
        annual_quarterly_delta = max(annual_quarterly_delta, abs(quarterly_revenue - consolidated.loc[year, "revenue"]))
    findings.append(_finding("Quarterly revenue reconciles to annual", annual_quarterly_delta < 0.01, f"Maximum quarterly annual delta is {annual_quarterly_delta:,.4f}."))

    seg_delta = (
        consolidated["legacy_operating_income"]
        + consolidated["foot_locker_operating_income"]
        + consolidated["synergy_benefit"]
        - consolidated["corporate_expense"]
        - consolidated["integration_cost"]
        - consolidated["ebit"]
    ).abs().max()
    findings.append(_finding("Segment operating income reconciles", seg_delta < 0.01, f"Maximum segment EBIT delta is {seg_delta:,.4f}."))

    required_sources = set(inputs.required_source_keys)
    source_keys = {source.key for source in inputs.source_registry}
    missing_sources = sorted(required_sources - source_keys)
    findings.append(_finding("Required source metadata present", not missing_sources, f"Missing required source keys: {missing_sources}."))

    synergy_by_year = tables["synergy_waterfall"].groupby("period")["net_recurring_benefit"].sum()
    synergy_delta = (consolidated["synergy_benefit"] - synergy_by_year).abs().max()
    findings.append(_finding("Synergy schedule ties to income statement", synergy_delta < 0.01, f"Maximum synergy tie-out delta is {synergy_delta:,.4f}."))

    negative_cash_years = consolidated.index[consolidated["cash"] < 0].tolist()
    if negative_cash_years:
        findings.append(AuditFinding(check="Cash balance remains non-negative", status="WARNING", message=f"Negative cash in {negative_cash_years}; financing policy should be reviewed."))
    else:
        findings.append(AuditFinding(check="Cash balance remains non-negative", status="PASS", message="Projected cash is non-negative in all forecast periods."))

    reverse_status = str(tables["reverse_dcf"].loc[0, "solve_status"])
    if reverse_status != "solved":
        findings.append(AuditFinding(check="Reverse DCF solve", status="WARNING", message="Reference price was not bracketed by the Foot Locker margin solve range."))
    else:
        findings.append(AuditFinding(check="Reverse DCF solve", status="PASS", message="Reverse DCF solved for Foot Locker terminal operating margin."))

    probabilistic = tables["probabilistic_valuation"].iloc[0]
    if probabilistic["status"] == "enabled":
        ordered = probabilistic["p10_price"] <= probabilistic["median_price"] <= probabilistic["p90_price"]
        findings.append(_finding("Monte Carlo percentile ordering", bool(ordered), "Probabilistic valuation percentiles are ordered from downside to upside."))
    else:
        findings.append(AuditFinding(check="Monte Carlo configured", status="WARNING", message="Probabilistic valuation is disabled or has no variables."))

    return findings


def _finding(check: str, passed: bool, message: str) -> AuditFinding:
    return AuditFinding(check=check, status="PASS" if passed else "ERROR", message=message)
