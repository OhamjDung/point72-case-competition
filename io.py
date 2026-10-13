from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from dks_model.schemas import ModelInputs


def load_inputs(path: str | Path) -> ModelInputs:
    """Load a model input directory or JSON file."""
    path = Path(path)
    input_file = path / "model_inputs.json" if path.is_dir() else path
    with input_file.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    payload = migrate_legacy_payload(payload)
    return ModelInputs.model_validate(payload)


def migrate_legacy_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Upgrade the v0.1 template to the v2 contract without claiming sourced data.

    The legacy file remains a synthetic fixture. Derived opening-balance-sheet
    detail and lease assumptions are explicitly mechanical compatibility fields,
    not filing-sourced company facts.
    """
    if payload.get("control", {}).get("schema_version") == "2.0":
        return payload

    migrated = json.loads(json.dumps(payload))
    control = migrated.setdefault("control", {})
    control.setdefault("schema_version", "2.0")
    control.setdefault("model_mode", "fixture")
    control.setdefault("units", "USD millions")
    control.setdefault("minimum_cash", 500.0)
    control.setdefault("revolver_capacity", 0.0)

    periods = migrated.get("periods", {})
    years = periods.get("forecast_years", [])
    scenarios = migrated.get("scenarios", {})
    for scenario in scenarios.values():
        scenario.setdefault("inventory_days", [105.0] * len(years))
        scenario.setdefault("receivable_days", [4.0] * len(years))
        scenario.setdefault("payable_days", [45.0] * len(years))
        scenario.setdefault("other_nwc_pct_revenue", [-0.015] * len(years))
        scenario.setdefault("stock_comp_expense", [0.0] * len(years))
        scenario.setdefault("share_issuance", [0.0] * len(years))
        scenario.setdefault("cash_tax_rate", [control.get("tax_rate", 0.0)] * len(years))

    historical = migrated.get("historical", {})
    historical_years = periods.get("historical_years", [])
    last_historical = historical.get(historical_years[-1], {}) if historical_years else {}
    opening = migrated.setdefault("balance_sheet_start", {})
    inventory = float(opening.get("inventory") or last_historical.get("inventory", 0.0))
    operating_nwc = float(opening.get("operating_nwc", 0.0))
    opening.setdefault("inventory", inventory)
    opening.setdefault("accounts_receivable", 0.0)
    opening.setdefault("prepaid_and_other_current_assets", 0.0)
    opening.setdefault("accounts_payable", max(inventory - operating_nwc, 0.0))
    opening.setdefault("accrued_expenses", 0.0)
    opening.setdefault("deferred_revenue", 0.0)
    opening.setdefault("income_taxes_payable", 0.0)
    opening.setdefault("operating_lease_assets", float(opening.get("lease_liabilities", 0.0)))
    opening.setdefault("finance_lease_liabilities", 0.0)
    opening.setdefault("other_assets", 0.0)
    opening.setdefault("common_stock_and_apic", 0.0)
    opening.setdefault("retained_earnings", float(opening.get("shareholders_equity", 0.0)))
    opening.setdefault("accumulated_oci", 0.0)
    opening.setdefault("treasury_stock", 0.0)
    # Grossing up a synthetic ROU asset requires an equal synthetic balancing
    # classification. It is deliberately visible in fixture-mode diagnostics.
    opening["other_liabilities"] = float(opening.get("other_liabilities", 0.0)) + float(
        opening.get("operating_lease_assets", 0.0)
    )

    control.setdefault("current_diluted_shares", scenarios.get("base", {}).get("diluted_share_base"))
    control.setdefault("valuation_date_cash", opening.get("cash", 0.0))
    control.setdefault("valuation_date_debt", opening.get("debt", 0.0))

    if "debt_tranches" not in migrated:
        migrated["debt_tranches"] = [
            {
                "name": "Legacy aggregate debt fixture",
                "opening_balance": opening.get("debt", 0.0),
                "coupon_rate": scenarios.get("base", {}).get("interest_rate", [0.0])[0],
                "maturity_year": years[-1] if years else "Unknown",
                "mandatory_repayments": scenarios.get("base", {}).get("debt_repayment", [0.0] * len(years)),
                "is_revolver": False,
                "capacity": 0.0,
            }
        ]

    lease_liability = float(opening.get("lease_liabilities", 0.0))
    migrated.setdefault(
        "leases",
        {
            "cash_payments": [lease_liability * 0.075] * len(years),
            "new_operating_leases": [lease_liability * 0.075] * len(years),
            "discount_rate": [0.05] * len(years),
            "closure_terminations": [0.0] * len(years),
            "impairments": [0.0] * len(years),
        },
    )

    base_shares = float(control.get("current_diluted_shares") or 0.0)
    migrated.setdefault(
        "wacc_inputs",
        {
            "beta": 1.0,
            "pre_tax_cost_of_debt": scenarios.get("base", {}).get("interest_rate", [0.05])[0],
            "market_value_equity": base_shares * float(control.get("reference_share_price", 0.0)),
            "market_value_debt": float(opening.get("debt", 0.0)),
            "source_note": "Legacy fixture-derived WACC inputs; public-market verification required",
        },
    )

    for source in migrated.get("source_registry", []):
        source.setdefault("source_id", source.get("key"))
        source.setdefault("publisher", source.get("source_name"))
        source.setdefault("as_of_date", source.get("source_date"))
        source.setdefault("locator", "Legacy source anchor; exact locator required")
        source.setdefault("mapped_fields", [])
        if source.get("input_type") == "internal judgment":
            source.setdefault("judgment_reason", "Illustrative fixture assumption")

    migrated.setdefault("purchase_accounting", {})
    migrated.setdefault("backtest_observations", [])
    return migrated
