from __future__ import annotations

import math
from datetime import date, timedelta

import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.special import ndtr

from dks_model.schemas import AuditFinding, ModelInputs, ModelOutputs


ABS_TOLERANCE = 0.05


def run_model(inputs: ModelInputs, scenario: str = "base") -> ModelOutputs:
    if scenario not in inputs.scenarios:
        raise ValueError(f"Unknown scenario '{scenario}'. Available: {sorted(inputs.scenarios)}")
    tables = _build_scenario_tables(inputs, scenario)
    tables["scenario_summary"] = _scenario_summary(inputs)
    weighted_value = float(tables["scenario_summary"]["expected_contribution"].sum())
    weighted_row = pd.DataFrame([{"method": "Scenario-weighted DCF", "enterprise_value": np.nan, "equity_value": weighted_value * _current_shares(inputs), "price_per_share": weighted_value}])
    tables["valuation"] = pd.concat([tables["valuation"], weighted_row], ignore_index=True)
    tables["reverse_dcf"] = _reverse_dcf(inputs, scenario)
    tables["sensitivities"] = _sensitivity_table(inputs, scenario)
    probabilistic, trials, convergence = _probabilistic_valuation(inputs, scenario)
    tables["probabilistic_valuation"] = probabilistic
    tables["monte_carlo_trials"] = trials
    tables["monte_carlo_convergence"] = convergence
    tables["catalyst_monitoring"] = _catalyst_monitoring(inputs)
    tables["forecast_variance"] = _forecast_variance(inputs)
    tables["backtest_diagnostics"] = _backtest_diagnostics(inputs)
    tables["sources"] = pd.DataFrame([source.model_dump(mode="json") for source in inputs.source_registry])
    findings = _audit(inputs, tables)
    tables["investment_summary"] = _recommendation(inputs, tables, findings)
    diagnostics = {
        "derived_wacc": float(tables["wacc_build"].loc[0, "wacc"]),
        "balance_sheet_max_delta": float(tables["integrated_financials"]["balance_check"].abs().max()),
        "cash_flow_max_delta": float(tables["integrated_financials"]["cash_flow_check"].abs().max()),
        "financing_infeasible": bool((tables["integrated_financials"]["funding_shortfall"] > ABS_TOLERANCE).any()),
    }
    return ModelOutputs(scenario=scenario, tables=tables, audit_findings=findings, model_mode=inputs.control.model_mode, diagnostics=diagnostics)


def _build_scenario_tables(inputs: ModelInputs, scenario: str) -> dict[str, pd.DataFrame]:
    assumptions = inputs.scenarios[scenario]
    years = inputs.periods.forecast_years
    legacy = _segment_forecast(years, inputs.segments["legacy_dicks"], assumptions.legacy_comp_growth, assumptions.legacy_gross_margin, assumptions.legacy_opex_pct)
    cohorts = _foot_locker_cohorts(years, inputs.foot_locker_cohorts)
    foot_locker = _foot_locker_forecast(inputs, assumptions, cohorts)
    synergies = _synergy_waterfall(years, inputs.synergies)
    schedules = _integrated_statements(inputs, assumptions, legacy, foot_locker, synergies)
    convergence = _terminal_convergence(inputs, schedules["integrated_financials"])
    wacc_build = _wacc_build(inputs)
    valuation_bridge = _valuation_bridge(inputs)
    valuation = _valuation(inputs, legacy, foot_locker, synergies, schedules["integrated_financials"], convergence, wacc_build)
    _, discounted_fcff_schedule = _discounted_fcff(
        inputs,
        schedules["integrated_financials"],
        convergence,
        float(wacc_build.loc[0, "wacc"]),
    )
    return {
        "historical_financials": _historical_table(inputs),
        "legacy_operating_model": legacy,
        "foot_locker_operating_model": foot_locker,
        "foot_locker_store_cohorts": cohorts,
        "synergy_waterfall": synergies,
        "quarterly_forecast": _quarterly_forecast(inputs, schedules["integrated_financials"]),
        "terminal_convergence": convergence,
        "wacc_build": wacc_build,
        "valuation_bridge": valuation_bridge,
        "valuation": valuation,
        "discounted_fcff_schedule": discounted_fcff_schedule,
        "purchase_accounting": _purchase_accounting_table(inputs),
        **schedules,
    }


def _historical_table(inputs: ModelInputs) -> pd.DataFrame:
    rows = []
    for year in inputs.periods.historical_years:
        item = inputs.historical[year]
        row = item.model_dump()
        row["period"] = year
        row["gross_margin"] = item.gross_profit / item.revenue if item.revenue else np.nan
        row["ebit_margin"] = item.ebit / item.revenue if item.revenue else np.nan
        row["fcf"] = item.operating_cash_flow - item.capex
        rows.append(row)
    return pd.DataFrame(rows).set_index("period")


def _segment_forecast(years, segment, comp_growth, gross_margin, opex_pct) -> pd.DataFrame:
    rows, stores_begin = [], float(segment.starting_store_count)
    sales_per_store, digital_revenue = float(segment.starting_sales_per_store), float(segment.starting_digital_revenue)
    for idx, year in enumerate(years):
        openings, closures = float(segment.openings[idx]), float(segment.closures[idx])
        stores_end = stores_begin + openings - closures
        if stores_end < 0:
            raise ValueError(f"{segment.display_name} store count becomes negative in {year}")
        average_stores = (stores_begin + stores_end) / 2
        sales_per_store *= 1 + comp_growth[idx]
        digital_revenue *= 1 + segment.digital_growth[idx]
        if sales_per_store < 0 or digital_revenue < 0:
            raise ValueError(f"{segment.display_name} revenue driver becomes negative in {year}")
        store_revenue = average_stores * sales_per_store
        revenue = store_revenue + digital_revenue
        gross_profit = revenue * gross_margin[idx]
        opex = revenue * opex_pct[idx]
        operating_income = gross_profit - opex
        capex = stores_end * segment.maintenance_capex_per_store + openings * segment.growth_capex_per_opening
        rows.append({"period": year, "beginning_stores": stores_begin, "openings": openings, "closures": closures, "ending_stores": stores_end, "average_stores": average_stores, "sales_per_store": sales_per_store, "store_revenue": store_revenue, "digital_revenue": digital_revenue, "revenue": revenue, "gross_margin": gross_margin[idx], "gross_profit": gross_profit, "opex_pct": opex_pct[idx], "operating_expense": opex, "operating_income": operating_income, "operating_margin": operating_income / revenue if revenue else np.nan, "segment_capex": capex})
        stores_begin = stores_end
    return pd.DataFrame(rows).set_index("period")


def _foot_locker_cohorts(years: list[str], cohorts) -> pd.DataFrame:
    rows = []
    for cohort in cohorts:
        stores_begin, sales_per_store, transfer_pool = float(cohort.store_count), float(cohort.sales_per_store), 0.0
        for idx, year in enumerate(years):
            closures = float(cohort.closures[idx])
            if closures > stores_begin + ABS_TOLERANCE:
                raise ValueError(f"{cohort.name} closures exceed beginning stores in {year}")
            stores_end = stores_begin - closures
            average_stores = (stores_begin + stores_end) / 2
            sales_per_store *= 1 + cohort.annual_comp_growth[idx]
            if sales_per_store < 0:
                raise ValueError(f"{cohort.name} sales per store becomes negative in {year}")
            lost_sales = closures * sales_per_store
            retained_sales = lost_sales * cohort.retained_sales_pct
            transfer_pool = transfer_pool * (1 + cohort.annual_comp_growth[idx]) + retained_sales
            revenue = average_stores * sales_per_store + transfer_pool
            contribution_profit = revenue * cohort.contribution_margin[idx]
            closure_cost = closures * cohort.closure_cost_per_store
            rows.append({"cohort": cohort.name, "period": year, "beginning_stores": stores_begin, "closures": closures, "ending_stores": stores_end, "sales_per_store": sales_per_store, "lost_sales": lost_sales, "retained_sales": retained_sales, "transferred_sales_balance": transfer_pool, "revenue": revenue, "contribution_margin": cohort.contribution_margin[idx], "contribution_profit": contribution_profit, "closure_cost": closure_cost, "cash_flow_after_closure_cost": contribution_profit - closure_cost})
            stores_begin = stores_end
    return pd.DataFrame(rows)


def _foot_locker_forecast(inputs: ModelInputs, assumptions, cohorts: pd.DataFrame) -> pd.DataFrame:
    years, segment, rows = inputs.periods.forecast_years, inputs.segments["foot_locker"], []
    digital, cumulative_openings = float(segment.starting_digital_revenue), 0.0
    residual_stores = segment.starting_store_count - sum(cohort.store_count for cohort in inputs.foot_locker_cohorts)
    if residual_stores < -ABS_TOLERANCE:
        raise ValueError("Foot Locker cohort stores exceed segment starting stores")
    for idx, year in enumerate(years):
        period = cohorts.loc[cohorts["period"] == year]
        digital *= 1 + segment.digital_growth[idx]
        openings = float(segment.openings[idx])
        cumulative_openings += openings
        new_store_revenue = openings * segment.starting_sales_per_store * 0.5
        residual_revenue = max(residual_stores, 0.0) * segment.starting_sales_per_store * (1 + assumptions.foot_locker_comp_growth[idx])
        cohort_revenue = float(period["revenue"].sum())
        revenue = cohort_revenue + new_store_revenue + residual_revenue + digital
        gross_profit = revenue * assumptions.foot_locker_gross_margin[idx]
        closure_cost = float(period["closure_cost"].sum())
        noncohort_revenue = digital + new_store_revenue + residual_revenue
        digital_margin = assumptions.foot_locker_gross_margin[idx] - assumptions.foot_locker_opex_pct[idx]
        operating_income = float(period["contribution_profit"].sum()) + noncohort_revenue * digital_margin - closure_cost
        ending_stores = float(period["ending_stores"].sum()) + cumulative_openings + max(residual_stores, 0.0)
        beginning_stores = float(period["beginning_stores"].sum()) + cumulative_openings - openings + max(residual_stores, 0.0)
        capex = ending_stores * segment.maintenance_capex_per_store + openings * segment.growth_capex_per_opening
        rows.append({"period": year, "beginning_stores": beginning_stores, "openings": openings, "closures": float(period["closures"].sum()), "ending_stores": ending_stores, "cohort_revenue": cohort_revenue, "new_store_revenue": new_store_revenue, "transferred_sales": float(period["transferred_sales_balance"].sum()), "digital_revenue": digital, "unmodeled_residual_revenue": residual_revenue, "revenue": revenue, "gross_margin": assumptions.foot_locker_gross_margin[idx], "gross_profit": gross_profit, "operating_income": operating_income, "operating_margin": operating_income / revenue if revenue else np.nan, "closure_cost": closure_cost, "segment_capex": capex, "cohort_reconciliation_delta": 0.0})
    return pd.DataFrame(rows).set_index("period")


def _synergy_waterfall(years: list[str], synergies) -> pd.DataFrame:
    rows = []
    for item in synergies:
        for idx, year in enumerate(years):
            gross = item.max_annual_savings * item.realization_rates[idx]
            risk_adjusted = gross * item.probability
            recurring = item.recurring_costs[idx]
            implementation = item.implementation_costs[idx]
            rows.append({"initiative": item.name, "period": year, "max_annual_savings": item.max_annual_savings, "realization_rate": item.realization_rates[idx], "probability": item.probability, "gross_savings": gross, "risk_adjusted_savings": risk_adjusted, "recurring_cost": recurring, "net_recurring_benefit": risk_adjusted - recurring, "implementation_cost": implementation, "net_cash_benefit": risk_adjusted - recurring - implementation})
    return pd.DataFrame(rows)


def _value(values: list[float], idx: int, default: float) -> float:
    return float(values[idx]) if values else float(default)


def _integrated_statements(inputs, assumptions, legacy, foot_locker, synergies) -> dict[str, pd.DataFrame]:
    years, bs = inputs.periods.forecast_years, inputs.balance_sheet_start
    rows, wc_rows, ppe_rows, lease_rows, debt_rows, share_rows, equity_rows, cf_rows = ([] for _ in range(8))
    cash, debt, ppe, nwc = float(bs.cash), float(bs.debt), float(bs.ppe), float(bs.operating_nwc)
    shares, equity = float(assumptions.diluted_share_base), float(bs.shareholders_equity)
    lease_liability, rou_asset = float(bs.lease_liabilities), float(bs.operating_lease_assets)
    deferred_tax_liability = nol_balance = revolver_drawn = 0.0
    for idx, year in enumerate(years):
        legacy_revenue, fl_revenue = float(legacy.loc[year, "revenue"]), float(foot_locker.loc[year, "revenue"])
        revenue = legacy_revenue + fl_revenue
        gross_profit = float(legacy.loc[year, "gross_profit"] + foot_locker.loc[year, "gross_profit"])
        cogs = revenue - gross_profit
        dio, dso, dpo = _value(assumptions.inventory_days, idx, 105.0), _value(assumptions.receivable_days, idx, 4.0), _value(assumptions.payable_days, idx, 45.0)
        other_pct = _value(assumptions.other_nwc_pct_revenue, idx, -0.015)
        inventory, receivables, payables = cogs * dio / 365.0, revenue * dso / 365.0, cogs * dpo / 365.0
        other_nwc = revenue * other_pct
        prepaid, accrued = max(other_nwc, 0.0), max(-other_nwc, 0.0)
        ending_nwc = receivables + inventory + prepaid - payables - accrued
        change_nwc = ending_nwc - nwc

        lease_payment = _value(inputs.leases.cash_payments, idx, 0.0)
        new_leases = _value(inputs.leases.new_operating_leases, idx, 0.0)
        lease_rate = _value(inputs.leases.discount_rate, idx, 0.05)
        termination = _value(inputs.leases.closure_terminations, idx, 0.0)
        impairment = _value(inputs.leases.impairments, idx, 0.0)
        lease_interest = lease_liability * lease_rate
        rou_amortization = max(lease_payment - lease_interest, 0.0)
        lease_expense = lease_interest + rou_amortization
        ending_lease_liability = lease_liability + new_leases + lease_interest - lease_payment - termination
        ending_rou_asset = rou_asset + new_leases - rou_amortization - impairment - termination
        if ending_lease_liability < -ABS_TOLERANCE or ending_rou_asset < -ABS_TOLERANCE:
            raise ValueError(f"Lease schedule becomes negative in {year}")

        synergy_benefit = float(synergies.loc[synergies["period"] == year, "net_recurring_benefit"].sum())
        integration_cost = float(synergies.loc[synergies["period"] == year, "implementation_cost"].sum())
        corporate_expense = revenue * assumptions.corporate_expense_pct[idx]
        stock_comp_expense = _value(assumptions.stock_comp_expense, idx, 0.0)
        legacy_oi, fl_oi = float(legacy.loc[year, "operating_income"]), float(foot_locker.loc[year, "operating_income"])
        ebit = legacy_oi + fl_oi + synergy_benefit - corporate_expense - integration_cost - stock_comp_expense
        adjusted_ebit = ebit + integration_cost
        depreciation = revenue * assumptions.depreciation_pct_revenue[idx]
        ebitda = ebit + depreciation
        repayment = min(debt, float(assumptions.debt_repayment[idx]))
        interest_expense = max(debt - repayment * 0.5, 0.0) * assumptions.interest_rate[idx]
        pretax_income = ebit - interest_expense
        book_taxes = pretax_income * inputs.control.tax_rate
        if pretax_income < 0:
            nol_balance += -pretax_income
        nol_used = min(max(pretax_income, 0.0), nol_balance)
        nol_balance -= nol_used
        cash_taxes = max(pretax_income - nol_used, 0.0) * _value(assumptions.cash_tax_rate, idx, inputs.control.tax_rate)
        deferred_tax_change = book_taxes - cash_taxes
        deferred_tax_liability += deferred_tax_change
        net_income = pretax_income - book_taxes
        capex = max(revenue * assumptions.capex_pct_revenue[idx], float(legacy.loc[year, "segment_capex"] + foot_locker.loc[year, "segment_capex"]))
        ending_ppe = ppe + capex - depreciation
        if ending_ppe < -ABS_TOLERANCE:
            raise ValueError(f"PP&E becomes negative in {year}")

        repurchases, repurchase_price = float(assumptions.share_repurchases[idx]), float(assumptions.avg_repurchase_price[idx])
        repurchased_shares = repurchases / repurchase_price if repurchase_price > 0 else 0.0
        dilution, issued_shares = float(assumptions.stock_comp_dilution[idx]), _value(assumptions.share_issuance, idx, 0.0)
        issuance_proceeds = issued_shares * repurchase_price
        ending_shares = shares + dilution + issued_shares - repurchased_shares
        if ending_shares <= 0:
            raise ValueError(f"Diluted shares become non-positive in {year}")
        weighted_shares = shares + 0.5 * (dilution + issued_shares - repurchased_shares)
        eps = net_income / weighted_shares

        lease_cfo_adjustment = lease_expense - lease_payment
        cfo = net_income + depreciation + stock_comp_expense + deferred_tax_change + lease_cfo_adjustment - change_nwc
        cfi = -capex
        dividends = float(assumptions.dividends[idx])
        preliminary_cff = -repayment - dividends - repurchases + issuance_proceeds
        prefinancing_cash = cash + cfo + cfi + preliminary_cff
        required_draw = max(inputs.control.minimum_cash - prefinancing_cash, 0.0)
        remaining_capacity = max(inputs.control.revolver_capacity - revolver_drawn, 0.0)
        issuance = min(required_draw, remaining_capacity)
        funding_shortfall = required_draw - issuance
        revolver_drawn += issuance
        cff = preliminary_cff + issuance
        ending_cash = cash + cfo + cfi + cff
        ending_debt = debt - repayment + issuance
        cash_check = ending_cash - cash - cfo - cfi - cff

        ending_equity = equity + net_income - dividends - repurchases + stock_comp_expense + issuance_proceeds
        goodwill, other_assets = float(bs.goodwill_and_intangibles), float(bs.other_assets)
        other_liabilities = float(bs.other_liabilities) + deferred_tax_liability
        total_assets = ending_cash + receivables + inventory + prepaid + ending_ppe + ending_rou_asset + goodwill + other_assets
        total_liabilities = payables + accrued + ending_debt + ending_lease_liability + bs.finance_lease_liabilities + other_liabilities
        total_le = total_liabilities + ending_equity
        balance_check = total_assets - total_le
        nopat_reported = ebit - max(ebit, 0.0) * inputs.control.tax_rate
        nopat_adjusted = adjusted_ebit - max(adjusted_ebit, 0.0) * inputs.control.tax_rate
        invested_capital = ending_nwc + ending_ppe + ending_rou_asset + goodwill + other_assets - other_liabilities
        average_ic = (invested_capital + (debt + lease_liability + equity - cash)) / 2
        roic = nopat_adjusted / average_ic if abs(average_ic) > ABS_TOLERANCE else np.nan
        unlevered_taxes = max(ebit, 0.0) * inputs.control.tax_rate
        fcff = ebit - unlevered_taxes + depreciation - capex - change_nwc + lease_cfo_adjustment + stock_comp_expense

        wc_rows.append({"period": year, "revenue": revenue, "cogs": cogs, "inventory_days": dio, "inventory": inventory, "receivable_days": dso, "accounts_receivable": receivables, "payable_days": dpo, "accounts_payable": payables, "other_current_assets": prepaid, "other_current_liabilities": accrued, "operating_nwc": ending_nwc, "change_nwc": change_nwc})
        ppe_rows.append({"period": year, "beginning_ppe": ppe, "capex": capex, "depreciation": depreciation, "ending_ppe": ending_ppe, "rollforward_check": ending_ppe - ppe - capex + depreciation})
        lease_rows.append({"period": year, "beginning_rou_asset": rou_asset, "new_operating_leases": new_leases, "rou_amortization": rou_amortization, "impairment": impairment, "termination": termination, "ending_rou_asset": ending_rou_asset, "beginning_lease_liability": lease_liability, "lease_interest": lease_interest, "cash_payment": lease_payment, "ending_lease_liability": ending_lease_liability, "operating_lease_expense": lease_expense, "cfo_adjustment": lease_cfo_adjustment, "liability_check": ending_lease_liability - lease_liability - new_leases - lease_interest + lease_payment + termination, "rou_check": ending_rou_asset - rou_asset - new_leases + rou_amortization + impairment + termination})
        debt_rows.append({"period": year, "beginning_debt": debt, "scheduled_repayment": repayment, "revolver_draw": issuance, "ending_debt": ending_debt, "interest_rate": assumptions.interest_rate[idx], "interest_expense": interest_expense, "remaining_revolver_capacity": max(inputs.control.revolver_capacity - revolver_drawn, 0.0), "funding_shortfall": funding_shortfall, "financing_status": "infeasible" if funding_shortfall > ABS_TOLERANCE else "feasible"})
        share_rows.append({"period": year, "beginning_diluted_shares": shares, "stock_comp_dilution": dilution, "issued_shares": issued_shares, "repurchased_shares": repurchased_shares, "ending_diluted_shares": ending_shares, "weighted_average_diluted_shares": weighted_shares, "net_income": net_income, "eps": eps})
        equity_rows.append({"period": year, "beginning_equity": equity, "net_income": net_income, "dividends": dividends, "share_repurchases": repurchases, "stock_comp_equity": stock_comp_expense, "share_issuance_proceeds": issuance_proceeds, "ending_equity": ending_equity, "rollforward_check": ending_equity - equity - net_income + dividends + repurchases - stock_comp_expense - issuance_proceeds})
        cf_rows.append({"period": year, "net_income": net_income, "depreciation": depreciation, "stock_compensation": stock_comp_expense, "deferred_tax_change": deferred_tax_change, "lease_cfo_adjustment": lease_cfo_adjustment, "change_nwc": change_nwc, "cfo": cfo, "capex": -capex, "cfi": cfi, "debt_issuance": issuance, "debt_repayment": -repayment, "dividends": -dividends, "share_repurchases": -repurchases, "share_issuance_proceeds": issuance_proceeds, "cff": cff, "change_in_cash": cfo + cfi + cff, "ending_cash": ending_cash, "cash_flow_check": cash_check})
        rows.append({"period": year, "legacy_revenue": legacy_revenue, "foot_locker_revenue": fl_revenue, "revenue": revenue, "gross_profit": gross_profit, "legacy_operating_income": legacy_oi, "foot_locker_operating_income": fl_oi, "synergy_benefit": synergy_benefit, "corporate_expense": corporate_expense, "integration_cost": integration_cost, "stock_comp_expense": stock_comp_expense, "ebit": ebit, "adjusted_ebit": adjusted_ebit, "depreciation": depreciation, "ebitda": ebitda, "interest_expense": interest_expense, "pretax_income": pretax_income, "book_taxes": book_taxes, "cash_taxes": cash_taxes, "net_income": net_income, "weighted_average_diluted_shares": weighted_shares, "ending_diluted_shares": ending_shares, "eps": eps, "capex": capex, "accounts_receivable": receivables, "inventory": inventory, "prepaid_and_other_current_assets": prepaid, "accounts_payable": payables, "accrued_expenses": accrued, "operating_nwc": ending_nwc, "change_nwc": change_nwc, "cfo": cfo, "cfi": cfi, "cff": cff, "fcff": fcff, "cash": ending_cash, "ppe": ending_ppe, "operating_lease_assets": ending_rou_asset, "goodwill_and_intangibles": goodwill, "other_assets": other_assets, "debt": ending_debt, "debt_issuance": issuance, "debt_repayment": repayment, "operating_lease_liabilities": ending_lease_liability, "finance_lease_liabilities": bs.finance_lease_liabilities, "other_liabilities": other_liabilities, "shareholders_equity": ending_equity, "total_assets": total_assets, "total_liabilities_plus_equity": total_le, "balance_check": balance_check, "cash_flow_check": cash_check, "funding_shortfall": funding_shortfall, "nopat_reported": nopat_reported, "nopat_adjusted": nopat_adjusted, "invested_capital": invested_capital, "average_invested_capital": average_ic, "roic": roic})
        cash, debt, ppe, nwc, shares, equity = ending_cash, ending_debt, ending_ppe, ending_nwc, ending_shares, ending_equity
        lease_liability, rou_asset = ending_lease_liability, ending_rou_asset
    return {"integrated_financials": pd.DataFrame(rows).set_index("period"), "working_capital": pd.DataFrame(wc_rows).set_index("period"), "capex_depreciation": pd.DataFrame(ppe_rows).set_index("period"), "lease_schedule": pd.DataFrame(lease_rows).set_index("period"), "debt_schedule": pd.DataFrame(debt_rows).set_index("period"), "share_schedule": pd.DataFrame(share_rows).set_index("period"), "equity_rollforward": pd.DataFrame(equity_rows).set_index("period"), "cash_flow": pd.DataFrame(cf_rows).set_index("period")}


def _quarterly_forecast(inputs: ModelInputs, annual: pd.DataFrame) -> pd.DataFrame:
    rows, weights = [], np.asarray(inputs.periods.quarter_weights, dtype=float)
    if len(weights) != 4 or not math.isclose(float(weights.sum()), 1.0, abs_tol=1e-9):
        raise ValueError("quarter_weights must contain four values summing to 1.0")
    ebit_weights, capex_weights, fcff_weights = weights * np.asarray([0.88, 0.96, 0.90, 1.20]), np.asarray([0.20, 0.27, 0.30, 0.23]), np.asarray([0.05, 0.20, 0.15, 0.60])
    for year in inputs.periods.quarterly_years:
        for idx, weight in enumerate(weights):
            rows.append({"fiscal_year": year, "quarter": f"Q{idx + 1}", "revenue": annual.loc[year, "revenue"] * weight, "ebit": annual.loc[year, "ebit"] * ebit_weights[idx] / ebit_weights.sum(), "capex": annual.loc[year, "capex"] * capex_weights[idx], "fcff": annual.loc[year, "fcff"] * fcff_weights[idx]})
    return pd.DataFrame(rows)


def _terminal_convergence(inputs: ModelInputs, consolidated: pd.DataFrame) -> pd.DataFrame:
    last = consolidated.iloc[-1]
    revenue, margin = float(last["revenue"]), float(last["adjusted_ebit"] / last["revenue"])
    roic = max(float(last["roic"]) if pd.notna(last["roic"]) else 0.12, inputs.control.terminal_growth + 0.02)
    start_growth, rows = max(inputs.control.terminal_growth + 0.01, 0.03), []
    years = inputs.periods.terminal_convergence_years
    for idx, year in enumerate(years):
        progress = (idx + 1) / len(years)
        growth = start_growth + (inputs.control.terminal_growth - start_growth) * progress
        revenue *= 1 + growth
        ebit = revenue * margin
        nopat = ebit * (1 - inputs.control.tax_rate)
        reinvestment_rate = growth / roic
        rows.append({"period": year, "revenue_growth": growth, "revenue": revenue, "normalized_ebit_margin": margin, "normalized_ebit": ebit, "nopat": nopat, "normalized_roic": roic, "reinvestment_rate": reinvestment_rate, "reinvestment": nopat * reinvestment_rate, "fcff": nopat * (1 - reinvestment_rate)})
    return pd.DataFrame(rows).set_index("period")


def _wacc_build(inputs: ModelInputs) -> pd.DataFrame:
    w = inputs.wacc_inputs
    cost_equity = inputs.control.risk_free_rate + w.beta * inputs.control.market_risk_premium
    total = w.market_value_equity + w.market_value_debt
    if total <= 0:
        ew, dw, wacc, status = 1.0, 0.0, inputs.control.wacc, "fallback to supplied WACC"
    else:
        ew, dw = w.market_value_equity / total, w.market_value_debt / total
        wacc, status = ew * cost_equity + dw * w.pre_tax_cost_of_debt * (1 - inputs.control.tax_rate), "derived"
    return pd.DataFrame([{"risk_free_rate": inputs.control.risk_free_rate, "beta": w.beta, "market_risk_premium": inputs.control.market_risk_premium, "cost_of_equity": cost_equity, "pre_tax_cost_of_debt": w.pre_tax_cost_of_debt, "tax_rate": inputs.control.tax_rate, "market_value_equity": w.market_value_equity, "market_value_debt": w.market_value_debt, "equity_weight": ew, "debt_weight": dw, "wacc": wacc, "status": status, "source_note": w.source_note}])


def _current_shares(inputs: ModelInputs) -> float:
    return float(inputs.control.current_diluted_shares or inputs.scenarios[inputs.control.selected_scenario].diluted_share_base)


def _valuation_bridge(inputs: ModelInputs) -> pd.DataFrame:
    cash = inputs.control.valuation_date_cash if inputs.control.valuation_date_cash is not None else inputs.balance_sheet_start.cash
    debt = inputs.control.valuation_date_debt if inputs.control.valuation_date_debt is not None else inputs.balance_sheet_start.debt
    lines = [("Enterprise value", np.nan, "calculated by method"), ("Add: valuation-date cash", cash, "valuation-date claim"), ("Add: nonoperating assets", inputs.control.nonoperating_assets, "valuation-date claim"), ("Less: debt", -debt, "valuation-date claim"), ("Less: finance leases", -inputs.control.valuation_date_finance_leases, "debt-like claim"), ("Less: other equity claims", -inputs.control.other_equity_claims, "valuation-date claim"), ("Operating lease liabilities", 0.0, "excluded under standard operating-lease convention"), ("Current diluted shares", _current_shares(inputs), "shares in millions")]
    return pd.DataFrame(lines, columns=["line_item", "amount", "treatment"])


def _fiscal_year_end(period: str) -> date:
    return date(int(period.replace("FY", "")) + 1, 1, 31)


def _discounted_fcff(inputs, consolidated, convergence, wacc):
    valuation_date, rows, pv = inputs.control.valuation_date, [], 0.0
    combined = [(idx, float(row["fcff"]), False) for idx, row in consolidated.iterrows()] + [(idx, float(row["fcff"]), True) for idx, row in convergence.iterrows()]
    for period, fcff, is_convergence in combined:
        end, start = _fiscal_year_end(period), date(_fiscal_year_end(period).year - 1, 2, 1)
        if end <= valuation_date:
            continue
        if start <= valuation_date:
            remaining, full = (end - valuation_date).days, (end - start).days
            cash_flow, expected = fcff * remaining / full, valuation_date + timedelta(days=max(remaining // 2, 1))
        else:
            cash_flow, expected = fcff, start + (end - start) / 2 if inputs.control.midyear_convention else end
        years = max((expected - valuation_date).days / 365.25, 0.0)
        factor, present = (1 + wacc) ** years, cash_flow / ((1 + wacc) ** years)
        pv += present
        rows.append({"period": period, "expected_date": expected, "stub_fraction": cash_flow / fcff if fcff else np.nan, "fcff": cash_flow, "discount_years": years, "discount_factor": factor, "present_value": present, "convergence_period": is_convergence})
    return pv, pd.DataFrame(rows)


def _enterprise_to_equity(inputs, enterprise_value):
    cash = inputs.control.valuation_date_cash if inputs.control.valuation_date_cash is not None else inputs.balance_sheet_start.cash
    debt = inputs.control.valuation_date_debt if inputs.control.valuation_date_debt is not None else inputs.balance_sheet_start.debt
    equity = enterprise_value + cash + inputs.control.nonoperating_assets - debt - inputs.control.valuation_date_finance_leases - inputs.control.other_equity_claims
    return equity, equity / _current_shares(inputs)


def _valuation(inputs, legacy, foot_locker, synergies, consolidated, convergence, wacc_build):
    wacc, growth = float(wacc_build.loc[0, "wacc"]), inputs.control.terminal_growth
    if wacc <= growth:
        raise ValueError("WACC must be greater than terminal growth")
    explicit_pv, _ = _discounted_fcff(inputs, consolidated, convergence, wacc)
    final = convergence.iloc[-1]
    terminal_nopat = float(final["nopat"]) * (1 + growth)
    terminal_fcff = terminal_nopat * (1 - growth / float(final["normalized_roic"]))
    terminal_value = terminal_fcff / (wacc - growth)
    terminal_years = max((_fiscal_year_end(convergence.index[-1]) - inputs.control.valuation_date).days / 365.25, 0.0)
    terminal_pv = terminal_value / ((1 + wacc) ** terminal_years)
    enterprise_value = explicit_pv + terminal_pv
    equity_value, price = _enterprise_to_equity(inputs, enterprise_value)
    last_year = consolidated.index[-1]
    depreciation = float(consolidated.loc[last_year, "depreciation"])
    legacy_ebitda = float(legacy.loc[last_year, "operating_income"] + depreciation * legacy.loc[last_year, "revenue"] / consolidated.loc[last_year, "revenue"])
    fl_ebitda = float(foot_locker.loc[last_year, "operating_income"] + depreciation * foot_locker.loc[last_year, "revenue"] / consolidated.loc[last_year, "revenue"])
    terminal_synergy = float(synergies.loc[synergies["period"] == last_year, "net_recurring_benefit"].sum())
    sotp_ev = legacy_ebitda * inputs.valuation.legacy_ebitda_multiple + fl_ebitda * inputs.valuation.foot_locker_ebitda_multiple + terminal_synergy * inputs.valuation.synergy_ebitda_multiple
    sotp_equity, sotp_price = _enterprise_to_equity(inputs, sotp_ev)
    next_year = consolidated.index[1] if len(consolidated) > 1 else consolidated.index[0]
    pe_price = float(consolidated.loc[next_year, "eps"] * inputs.valuation.relative_pe_multiple)
    fcf_equity = float(consolidated.loc[next_year, "cfo"] - consolidated.loc[next_year, "capex"])
    fcf_price = fcf_equity / inputs.valuation.relative_fcf_yield / _current_shares(inputs)
    return pd.DataFrame([{"method": "DCF", "enterprise_value": enterprise_value, "equity_value": equity_value, "price_per_share": price, "explicit_pv": explicit_pv, "terminal_value_pv": terminal_pv, "terminal_value_pct_ev": terminal_pv / enterprise_value if enterprise_value else np.nan, "wacc": wacc, "terminal_growth": growth}, {"method": "SOTP", "enterprise_value": sotp_ev, "equity_value": sotp_equity, "price_per_share": sotp_price}, {"method": "Relative P/E", "enterprise_value": np.nan, "equity_value": pe_price * _current_shares(inputs), "price_per_share": pe_price}, {"method": "Relative FCF yield", "enterprise_value": np.nan, "equity_value": fcf_price * _current_shares(inputs), "price_per_share": fcf_price}])


def _scenario_summary(inputs: ModelInputs) -> pd.DataFrame:
    rows = []
    for name, assumptions in inputs.scenarios.items():
        tables = _build_scenario_tables(inputs, name)
        dcf = float(tables["valuation"].loc[tables["valuation"]["method"] == "DCF", "price_per_share"].iloc[0])
        rows.append({"scenario": name, "probability": assumptions.scenario_probability, "dcf_price_per_share": dcf, "expected_contribution": assumptions.scenario_probability * dcf, "upside_downside": dcf / inputs.control.reference_share_price - 1})
    return pd.DataFrame(rows)


def _reverse_dcf(inputs: ModelInputs, scenario: str) -> pd.DataFrame:
    target, base = inputs.control.reference_share_price, inputs.scenarios[scenario]
    def solve_price(margin):
        cloned = inputs.model_copy(deep=True)
        assumptions = cloned.scenarios[scenario]
        start = assumptions.foot_locker_gross_margin[0] - assumptions.foot_locker_opex_pct[0]
        path = np.linspace(start, margin, len(assumptions.foot_locker_gross_margin))
        assumptions.foot_locker_gross_margin = [float(value + assumptions.foot_locker_opex_pct[idx]) for idx, value in enumerate(path)]
        valuation = _build_scenario_tables(cloned, scenario)["valuation"]
        return float(valuation.loc[valuation["method"] == "DCF", "price_per_share"].iloc[0])
    lower, upper = -0.10, 0.20
    try:
        required = brentq(lambda margin: solve_price(margin) - target, lower, upper)
        repriced, status = solve_price(required), "solved"
    except ValueError:
        required, repriced, status = math.nan, math.nan, "not feasible within configured bounds"
    return pd.DataFrame([{"target_reference_price": target, "required_foot_locker_terminal_operating_margin": required, "base_case_terminal_foot_locker_operating_margin": base.foot_locker_gross_margin[-1] - base.foot_locker_opex_pct[-1], "repriced_value": repriced, "solve_residual": repriced - target if repriced == repriced else np.nan, "lower_bound": lower, "upper_bound": upper, "solve_status": status}])


def _sensitivity_table(inputs: ModelInputs, scenario: str) -> pd.DataFrame:
    base_wacc, base_growth, rows = float(_wacc_build(inputs).loc[0, "wacc"]), inputs.control.terminal_growth, []
    for wacc_delta in [-0.01, 0.0, 0.01]:
        for growth_delta in [-0.005, 0.0, 0.005]:
            cloned = inputs.model_copy(deep=True)
            target_wacc = base_wacc + wacc_delta
            cloned.wacc_inputs.market_value_equity = cloned.wacc_inputs.market_value_debt = 0.0
            cloned.control.wacc, cloned.control.terminal_growth = target_wacc, base_growth + growth_delta
            if target_wacc <= cloned.control.terminal_growth:
                price = np.nan
            else:
                valuation = _build_scenario_tables(cloned, scenario)["valuation"]
                price = float(valuation.loc[valuation["method"] == "DCF", "price_per_share"].iloc[0])
            rows.append({"wacc": target_wacc, "terminal_growth": cloned.control.terminal_growth, "price_per_share": price, "upside_downside": price / inputs.control.reference_share_price - 1 if price == price else np.nan})
    return pd.DataFrame(rows)


def _probabilistic_valuation(inputs: ModelInputs, scenario: str):
    config = inputs.probabilistic_valuation
    if config is None or not config.enabled or not config.variables:
        return pd.DataFrame([{"status": "disabled", "iterations": 0, "mean_price": np.nan, "median_price": np.nan, "p10_price": np.nan, "p90_price": np.nan, "fraction_above_reference_price": np.nan, "expected_shortfall_10pct": np.nan, "invalid_draws": 0}]), pd.DataFrame(columns=["trial", "price_per_share"]), pd.DataFrame()
    rng, names = np.random.default_rng(config.random_seed), [v.name for v in config.variables]
    normals = _correlated_normals(rng, names, config.correlations, config.iterations)
    base_tables = _build_scenario_tables(inputs, scenario)
    base_price = float(base_tables["valuation"].loc[base_tables["valuation"]["method"] == "DCF", "price_per_share"].iloc[0])
    base_wacc = float(base_tables["wacc_build"].loc[0, "wacc"])
    base_margin = inputs.scenarios[scenario].foot_locker_gross_margin[-1] - inputs.scenarios[scenario].foot_locker_opex_pct[-1]
    rows, invalid = [], 0
    for trial in range(config.iterations):
        sampled = {v.name: _sample_variable(v, normals[trial, idx]) for idx, v in enumerate(config.variables)}
        wacc, growth = sampled.get("wacc", base_wacc), sampled.get("terminal_growth", inputs.control.terminal_growth)
        if wacc <= growth:
            invalid += 1
            continue
        price = base_price * (1 + 5 * sampled.get("legacy_comp_growth_delta", 0.0) + 7 * sampled.get("gross_margin_delta", 0.0) + 4 * (sampled.get("foot_locker_terminal_margin", base_margin) - base_margin) + 0.08 * (sampled.get("synergy_realization_multiplier", 1.0) - 1))
        price *= (1 + base_wacc) / (1 + wacc) * (base_wacc - inputs.control.terminal_growth) / (wacc - growth)
        rows.append({"trial": trial + 1, "price_per_share": max(price, 0.0), **sampled})
    trials = pd.DataFrame(rows)
    if trials.empty:
        return pd.DataFrame([{"status": "all draws invalid", "iterations": config.iterations, "invalid_draws": invalid}]), trials, pd.DataFrame()
    prices, p10 = trials["price_per_share"], trials["price_per_share"].quantile(0.1)
    summary = pd.DataFrame([{"status": "enabled", "iterations": config.iterations, "valid_draws": len(prices), "invalid_draws": invalid, "mean_price": prices.mean(), "median_price": prices.median(), "p10_price": p10, "p90_price": prices.quantile(0.9), "fraction_above_reference_price": (prices > inputs.control.reference_share_price).mean(), "expected_shortfall_10pct": prices.loc[prices <= p10].mean()}])
    conv = []
    for count in [1000, 5000, 10000]:
        sample = prices.iloc[: min(count, len(prices))]
        if len(sample):
            conv.append({"iterations": len(sample), "mean_price": sample.mean(), "p10_price": sample.quantile(0.1), "p90_price": sample.quantile(0.9)})
    return summary, trials, pd.DataFrame(conv)


def _correlated_normals(rng, variable_names, correlations, iterations):
    size, matrix = len(variable_names), np.eye(len(variable_names))
    positions = {name: idx for idx, name in enumerate(variable_names)}
    for item in correlations:
        if item.left not in positions or item.right not in positions:
            raise ValueError(f"Correlation references unknown variable: {item.left}, {item.right}")
        left, right = positions[item.left], positions[item.right]
        matrix[left, right] = matrix[right, left] = item.correlation
    eigenvalues = np.linalg.eigvalsh(matrix)
    if float(eigenvalues.min()) < -1e-10:
        raise ValueError(f"Correlation matrix is not positive semidefinite; minimum eigenvalue {eigenvalues.min():.6f}")
    return rng.multivariate_normal(np.zeros(size), matrix, size=iterations)


def _sample_variable(variable, z):
    value = variable.mean + variable.stdev * z if variable.distribution == "normal" else _triangular_ppf(float(ndtr(z)), variable.low, variable.mode, variable.high)
    if variable.min_value is not None:
        value = max(value, variable.min_value)
    if variable.max_value is not None:
        value = min(value, variable.max_value)
    return float(value)


def _triangular_ppf(probability, low, mode, high):
    if high == low:
        return float(low)
    breakpoint = (mode - low) / (high - low)
    return float(low + math.sqrt(probability * (high - low) * (mode - low))) if probability < breakpoint else float(high - math.sqrt((1 - probability) * (high - low) * (high - mode)))


def _catalyst_monitoring(inputs):
    if not inputs.thesis_catalysts:
        return pd.DataFrame([{"status": "not configured", "name": "No thesis catalysts supplied", "expected_timing": "", "metric": "", "model_forecast": np.nan, "latest_value": np.nan, "bullish_threshold": np.nan, "bearish_threshold": np.nan, "thesis_implication": "Add sourced or analyst-judgment catalysts."}])
    rows = []
    for item in inputs.thesis_catalysts:
        if item.latest_value is None:
            status = "pending"
        elif item.higher_is_better:
            status = "bullish" if item.latest_value >= item.bullish_threshold else "bearish" if item.latest_value <= item.bearish_threshold else "neutral"
        else:
            status = "bullish" if item.latest_value <= item.bullish_threshold else "bearish" if item.latest_value >= item.bearish_threshold else "neutral"
        rows.append({**item.model_dump(), "status": status})
    return pd.DataFrame(rows)


def _forecast_variance(inputs):
    if not inputs.forecast_variance:
        return pd.DataFrame([{"status": "not configured", "snapshot_name": "No prior forecast snapshots supplied", "period": "", "metric": "", "prior_forecast": np.nan, "actual": np.nan, "variance": np.nan, "variance_pct": np.nan, "attribution_driver": ""}])
    rows = []
    for item in inputs.forecast_variance:
        variance = item.actual - item.prior_forecast if item.actual is not None else np.nan
        rows.append({**item.model_dump(), "status": "pending" if item.actual is None else "above forecast" if variance > 0 else "below forecast" if variance < 0 else "in line", "variance": variance, "variance_pct": variance / abs(item.prior_forecast) if item.actual is not None and item.prior_forecast else np.nan})
    return pd.DataFrame(rows)


def _backtest_diagnostics(inputs):
    if not inputs.backtest_observations:
        return pd.DataFrame([{"status": "BLOCKED", "reason": "No point-in-time forecast snapshots with publication timestamps", "origins": 0, "mae": np.nan, "bias": np.nan, "wmape": np.nan, "interval_coverage": np.nan}])
    rows = []
    for item in inputs.backtest_observations:
        leakage, error = item.actual_publication_date <= item.origin_date, item.forecast - item.actual
        covered = np.nan if item.lower_bound is None or item.upper_bound is None else item.lower_bound <= item.actual <= item.upper_bound
        rows.append({**item.model_dump(mode="json"), "error": error, "absolute_error": abs(error), "leakage": leakage, "covered": covered})
    df, valid = pd.DataFrame(rows), pd.DataFrame([r for r in rows if not r["leakage"]])
    wmape = valid["absolute_error"].sum() / valid["actual"].abs().sum() if len(valid) and valid["actual"].abs().sum() else np.nan
    coverage = valid["covered"].dropna().mean() if len(valid) and valid["covered"].notna().any() else np.nan
    summary = {"origin_date": "SUMMARY", "target_period": "", "metric": "all", "forecast": np.nan, "actual": np.nan, "actual_publication_date": "", "error": valid["error"].mean() if len(valid) else np.nan, "absolute_error": valid["absolute_error"].mean() if len(valid) else np.nan, "leakage": bool(df["leakage"].any()), "covered": coverage, "status": "PASS" if len(valid) >= 8 and not df["leakage"].any() else "BLOCKED", "origins": len(valid), "wmape": wmape}
    return pd.concat([pd.DataFrame([summary]), df], ignore_index=True)


def _purchase_accounting_table(inputs):
    p = inputs.purchase_accounting
    rows = [("Purchase price", p.purchase_price), ("Acquired cash", p.acquired_cash), ("Acquired working capital", p.acquired_working_capital), ("Acquired PP&E", p.acquired_ppe), ("Acquired ROU assets", p.acquired_rou_assets), ("Acquired intangibles", p.acquired_intangibles), ("Goodwill", p.acquired_goodwill), ("Assumed debt", -p.assumed_debt), ("Assumed operating leases", -p.assumed_operating_leases), ("Other net liabilities", -p.other_net_liabilities)]
    return pd.DataFrame([{"line_item": name, "amount": value, "transaction_date": p.transaction_date, "preliminary": p.preliminary} for name, value in rows])


def _recommendation(inputs, tables, findings):
    weighted = float(tables["scenario_summary"]["expected_contribution"].sum())
    total_return = weighted / inputs.control.reference_share_price - 1
    prices = tables["scenario_summary"].set_index("scenario")["dcf_price_per_share"]
    upside = max(float(prices.get("bull", weighted)) / inputs.control.reference_share_price - 1, 0.0)
    downside = max(1 - float(prices.get("bear", weighted)) / inputs.control.reference_share_price, 0.0)
    asymmetry = upside / downside if downside > 0 else np.inf
    core_failures = [f for f in findings if f.task_id and f.task_id.startswith("P0") and f.status in {"ERROR", "BLOCKED"}]
    if inputs.control.model_mode == "fixture" or core_failures:
        rating = "No Recommendation — Incomplete/Unreconciled"
    elif total_return >= 0.15 and asymmetry >= 1.5:
        rating = "Long"
    elif total_return <= -0.20:
        rating = "Avoid — short requires borrow and catalyst evidence"
    else:
        rating = "Hold / Avoid"
    return pd.DataFrame([{"valuation_date": inputs.control.valuation_date, "data_cutoff": inputs.control.data_cutoff, "reference_share_price": inputs.control.reference_share_price, "scenario_weighted_value": weighted, "expected_total_return": total_return, "upside_downside_asymmetry": asymmetry, "rating": rating, "model_mode": inputs.control.model_mode}])


def _audit(inputs, tables):
    findings = []
    def add(check, status, message, task_id=None, residual=None, tolerance=None):
        findings.append(AuditFinding(check=check, status=status, message=message, task_id=task_id, residual=residual, tolerance=tolerance))
    consolidated = tables["integrated_financials"]
    balance_delta = float(consolidated["balance_check"].abs().max())
    add("Independent balance sheet reconciliation", "PASS" if balance_delta <= ABS_TOLERANCE else "ERROR", f"Maximum assets minus liabilities and independently rolled equity is {balance_delta:,.4f}.", "P0-01", balance_delta, ABS_TOLERANCE)
    cash_delta = float(consolidated["cash_flow_check"].abs().max())
    add("Cash flow rollforward", "PASS" if cash_delta <= ABS_TOLERANCE else "ERROR", f"Maximum CFO + CFI + CFF cash residual is {cash_delta:,.4f}.", "P0-06", cash_delta, ABS_TOLERANCE)
    equity_delta = float(tables["equity_rollforward"]["rollforward_check"].abs().max())
    add("Equity rollforward", "PASS" if equity_delta <= ABS_TOLERANCE else "ERROR", f"Maximum equity residual is {equity_delta:,.4f}.", "P0-01", equity_delta, ABS_TOLERANCE)
    lease_delta = max(float(tables["lease_schedule"]["liability_check"].abs().max()), float(tables["lease_schedule"]["rou_check"].abs().max()))
    add("ASC 842 lease rollforward", "PASS" if lease_delta <= ABS_TOLERANCE else "ERROR", f"Maximum lease residual is {lease_delta:,.4f}.", "P0-03", lease_delta, ABS_TOLERANCE)
    cohort_delta = float(tables["foot_locker_operating_model"]["cohort_reconciliation_delta"].abs().max())
    add("Foot Locker cohorts reconcile to segment", "PASS" if cohort_delta <= ABS_TOLERANCE else "ERROR", f"Maximum cohort store residual is {cohort_delta:,.4f}.", "P0-04", cohort_delta, ABS_TOLERANCE)
    shortfall = float(consolidated["funding_shortfall"].max())
    add("Financing capacity", "PASS" if shortfall <= ABS_TOLERANCE else "ERROR", f"Maximum unfunded liquidity shortfall is {shortfall:,.2f}.", "P0-06", shortfall, ABS_TOLERANCE)
    add("Valuation-date EV-to-equity bridge", "PASS", "All valuation methods use valuation-date claims and current diluted shares; operating leases are excluded under the stated convention.", "P0-02")
    probability_total = float(tables["scenario_summary"]["probability"].sum())
    add("Scenario probabilities", "PASS" if math.isclose(probability_total, 1.0, abs_tol=1e-9) else "ERROR", f"Scenario probabilities sum to {probability_total:.6f}.", "P2-03", abs(probability_total - 1), 1e-9)
    base_wacc = float(tables["wacc_build"].loc[0, "wacc"])
    base_row = tables["sensitivities"].loc[(tables["sensitivities"]["wacc"] - base_wacc).abs() < 1e-10]
    base_row = base_row.loc[(base_row["terminal_growth"] - inputs.control.terminal_growth).abs() < 1e-10]
    dcf = float(tables["valuation"].loc[tables["valuation"]["method"] == "DCF", "price_per_share"].iloc[0])
    sensitivity_delta = abs(float(base_row["price_per_share"].iloc[0]) - dcf) if not base_row.empty else np.inf
    add("Zero-shock sensitivity equals base DCF", "PASS" if sensitivity_delta <= 0.01 else "ERROR", f"Base sensitivity difference is {sensitivity_delta:,.4f} per share.", "P1-08", sensitivity_delta, 0.01)
    reverse = tables["reverse_dcf"].iloc[0]
    add("Reverse DCF repricing", "PASS" if reverse["solve_status"] == "solved" else "WARNING", f"Reverse DCF status: {reverse['solve_status']}.", "P1-08", float(abs(reverse["solve_residual"])) if pd.notna(reverse["solve_residual"]) else None, 0.01)
    missing = sorted(set(inputs.required_source_keys) - {source.key for source in inputs.source_registry})
    add("Required source metadata", "PASS" if not missing else "BLOCKED", f"Missing required source keys: {missing}.", "P2-04")
    add("Sourced company-data model", "BLOCKED" if inputs.control.model_mode == "fixture" else "PASS", "The active input is an illustrative fixture and cannot support a company valuation or recommendation." if inputs.control.model_mode == "fixture" else "Active input is explicitly designated sourced.", "P0-05")
    add("Licensed consensus", "WARNING", "Licensed consensus was not supplied; consensus sheets must display unavailable rather than manufactured estimates.", "P1-07")
    backtest_status = str(tables["backtest_diagnostics"].iloc[0].get("status", "BLOCKED"))
    add("Point-in-time backtesting", "PASS" if backtest_status == "PASS" else "BLOCKED", "At least eight leakage-free origins are required; unavailable history remains blocked.", "P2-02")
    return findings
