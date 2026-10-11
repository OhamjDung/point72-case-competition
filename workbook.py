from __future__ import annotations

from pathlib import Path

import pandas as pd

from dks_model.schemas import ModelInputs, ModelOutputs


SHEET_ORDER = [
    "Investment Summary",
    "Model Control Panel",
    "Historical Financials",
    "Historical Segment Recon",
    "Assumptions & Sources",
    "Legacy DICK'S Operating Model",
    "Foot Locker Operating Model",
    "Foot Locker Store Cohorts",
    "Acquisition & Synergy",
    "Consolidated Income Statement",
    "Working Capital Schedule",
    "Capex & Depreciation",
    "Debt Interest Lease",
    "Share Count Capital Alloc",
    "Consolidated Balance Sheet",
    "Consolidated Cash Flow",
    "Financial Ratios & ROIC",
    "Wall Street Consensus",
    "Consensus Variant Bridge",
    "Discounted Cash Flow",
    "SOTP Valuation",
    "Relative Valuation",
    "Reverse DCF",
    "Scenarios & Sensitivities",
    "Probabilistic Valuation",
    "Alternative Data & Backtesting",
    "Thesis Catalysts Monitoring",
    "Forecast Variance Analysis",
    "Model Audit & Quality Checks",
]


def export_workbook(outputs: ModelOutputs, inputs: ModelInputs, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(path, engine="xlsxwriter") as writer:
        workbook = writer.book
        formats = _formats(workbook)

        for sheet_name in SHEET_ORDER:
            worksheet = workbook.add_worksheet(sheet_name)
            writer.sheets[sheet_name] = worksheet
            worksheet.set_tab_color("#4472C4" if sheet_name in {"Investment Summary", "Model Audit & Quality Checks"} else "#A5A5A5")
            worksheet.freeze_panes(1, 1)
            worksheet.set_landscape()
            worksheet.fit_to_pages(1, 0)
            worksheet.set_margins(left=0.25, right=0.25, top=0.5, bottom=0.5)
            _write_title(worksheet, sheet_name, formats)

        _write_investment_summary(writer, outputs, inputs, formats)
        _write_control_panel(writer, inputs, outputs, formats)
        _write_dataframe(writer, outputs.tables["historical_financials"].reset_index(), "Historical Financials", 2, 0, formats)
        _write_placeholder(writer, "Historical Segment Recon", "Manual pro forma and post-acquisition reconciliation inputs tie here.")
        _write_dataframe(writer, outputs.tables["sources"], "Assumptions & Sources", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["legacy_operating_model"].reset_index(), "Legacy DICK'S Operating Model", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["foot_locker_operating_model"].reset_index(), "Foot Locker Operating Model", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["foot_locker_store_cohorts"], "Foot Locker Store Cohorts", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["synergy_waterfall"], "Acquisition & Synergy", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["revenue", "legacy_operating_income", "foot_locker_operating_income", "synergy_benefit", "corporate_expense", "integration_cost", "ebit", "interest_expense", "taxes", "net_income", "eps"]), "Consolidated Income Statement", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["operating_nwc", "change_nwc"]), "Working Capital Schedule", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["capex", "depreciation", "ppe"]), "Capex & Depreciation", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["debt", "debt_issuance", "debt_repayment", "interest_expense", "lease_liabilities", "net_debt"]), "Debt Interest Lease", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["diluted_shares", "dividends", "share_repurchases", "eps"]), "Share Count Capital Alloc", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["cash", "operating_nwc", "ppe", "goodwill_and_intangibles", "total_assets", "debt", "lease_liabilities", "other_liabilities", "shareholders_equity", "total_liabilities_plus_equity"]), "Consolidated Balance Sheet", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["net_income", "depreciation", "change_nwc", "operating_cash_flow", "capex", "debt_issuance", "debt_repayment", "fcff", "fcf_to_equity_before_capital_return"]), "Consolidated Cash Flow", 2, 0, formats)
        _write_dataframe(writer, _select(outputs, ["nopat", "invested_capital", "roic", "economic_profit"]), "Financial Ratios & ROIC", 2, 0, formats)
        _write_placeholder(writer, "Wall Street Consensus", "Consensus estimates are intentionally manual placeholders until a licensed source is supplied.")
        _write_placeholder(writer, "Consensus Variant Bridge", "Bridge our revenue, EBIT, EPS, and FCF against consensus once consensus inputs are populated.")
        _write_dataframe(writer, outputs.tables["valuation"].loc[outputs.tables["valuation"]["method"] == "DCF"], "Discounted Cash Flow", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["valuation"].loc[outputs.tables["valuation"]["method"] == "SOTP"], "SOTP Valuation", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["valuation"].loc[outputs.tables["valuation"]["method"].str.contains("Relative", na=False)], "Relative Valuation", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["reverse_dcf"], "Reverse DCF", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["scenario_summary"], "Scenarios & Sensitivities", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["sensitivities"], "Scenarios & Sensitivities", 10, 0, formats)
        _write_dataframe(writer, outputs.tables["probabilistic_valuation"], "Probabilistic Valuation", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["monte_carlo_trials"], "Probabilistic Valuation", 7, 0, formats)
        _write_placeholder(writer, "Alternative Data & Backtesting", "Reserved for future alternative-data collection and validation.")
        _write_dataframe(writer, outputs.tables["catalyst_monitoring"], "Thesis Catalysts Monitoring", 2, 0, formats)
        _write_dataframe(writer, outputs.tables["forecast_variance"], "Forecast Variance Analysis", 2, 0, formats)
        _write_audit(writer, outputs, formats)


def _formats(workbook):
    return {
        "title": workbook.add_format({"bold": True, "font_size": 14, "bg_color": "#1F4E78", "font_color": "#FFFFFF"}),
        "header": workbook.add_format({"bold": True, "bg_color": "#D9EAF7", "border": 1}),
        "input": workbook.add_format({"font_color": "#0000FF"}),
        "formula": workbook.add_format({"font_color": "#000000"}),
        "link": workbook.add_format({"font_color": "#008000"}),
        "money": workbook.add_format({"num_format": "$#,##0.0;($#,##0.0)", "border": 1}),
        "number": workbook.add_format({"num_format": "#,##0.0", "border": 1}),
        "percent": workbook.add_format({"num_format": "0.0%", "border": 1}),
        "text": workbook.add_format({"border": 1}),
        "pass": workbook.add_format({"bg_color": "#C6EFCE", "font_color": "#006100", "border": 1}),
        "warning": workbook.add_format({"bg_color": "#FFEB9C", "font_color": "#9C6500", "border": 1}),
        "error": workbook.add_format({"bg_color": "#FFC7CE", "font_color": "#9C0006", "border": 1}),
    }


def _write_title(worksheet, title: str, formats) -> None:
    worksheet.write(0, 0, title, formats["title"])
    worksheet.set_column(0, 0, 28)
    worksheet.set_column(1, 20, 16)


def _write_dataframe(writer, df: pd.DataFrame, sheet_name: str, startrow: int, startcol: int, formats) -> None:
    df.to_excel(writer, sheet_name=sheet_name, startrow=startrow, startcol=startcol, index=False)
    worksheet = writer.sheets[sheet_name]
    for col_num, value in enumerate(df.columns, startcol):
        worksheet.write(startrow, col_num, value, formats["header"])
    for col_num, column in enumerate(df.columns, startcol):
        width = min(max(len(str(column)) + 2, 12), 28)
        worksheet.set_column(col_num, col_num, width)


def _write_investment_summary(writer, outputs: ModelOutputs, inputs: ModelInputs, formats) -> None:
    ws = writer.sheets["Investment Summary"]
    valuation = outputs.tables["valuation"]
    dcf_price = float(valuation.loc[valuation["method"] == "DCF", "price_per_share"].iloc[0])
    sotp_price = float(valuation.loc[valuation["method"] == "SOTP", "price_per_share"].iloc[0])
    weighted = float(valuation.loc[valuation["method"] == "Scenario-weighted DCF", "price_per_share"].iloc[0])
    recommendation = "Long" if weighted > inputs.control.reference_share_price else "Short / Avoid"
    rows = [
        ("Company", inputs.control.company_name),
        ("Ticker", inputs.control.ticker),
        ("Valuation date", str(inputs.control.valuation_date)),
        ("Reference share price", inputs.control.reference_share_price),
        ("Recommendation", recommendation),
        ("DCF price target", dcf_price),
        ("SOTP value", sotp_price),
        ("Scenario-weighted value", weighted),
        ("Expected upside/downside", weighted / inputs.control.reference_share_price - 1),
        ("Audit status", outputs.audit_status),
    ]
    for row_idx, (label, value) in enumerate(rows, start=2):
        ws.write(row_idx, 0, label, formats["header"])
        if isinstance(value, float) and "upside" in label.lower():
            ws.write(row_idx, 1, value, formats["percent"])
        elif isinstance(value, float):
            ws.write(row_idx, 1, value, formats["money"])
        else:
            fmt = formats["error"] if value == "ERROR" else formats["warning"] if value == "WARNING" else formats["text"]
            ws.write(row_idx, 1, value, fmt)
    ws.write(14, 0, "Three critical assumptions", formats["header"])
    ws.write(15, 0, "Foot Locker normalized operating margin", formats["text"])
    ws.write(16, 0, "Legacy DICK'S sustainable comp growth", formats["text"])
    ws.write(17, 0, "Foot Locker inventory normalization and cash conversion", formats["text"])


def _write_control_panel(writer, inputs: ModelInputs, outputs: ModelOutputs, formats) -> None:
    ws = writer.sheets["Model Control Panel"]
    rows = [
        ("Selected scenario", outputs.scenario),
        ("Forecast version", inputs.control.forecast_version),
        ("Data cutoff", str(inputs.control.data_cutoff)),
        ("Last reported quarter", inputs.control.last_reported_quarter),
        ("Risk-free rate", inputs.control.risk_free_rate),
        ("Market risk premium", inputs.control.market_risk_premium),
        ("WACC", inputs.control.wacc),
        ("Terminal growth", inputs.control.terminal_growth),
        ("Tax rate", inputs.control.tax_rate),
    ]
    for row_idx, (label, value) in enumerate(rows, start=2):
        ws.write(row_idx, 0, label, formats["header"])
        if isinstance(value, float):
            ws.write(row_idx, 1, value, formats["percent"])
        else:
            ws.write(row_idx, 1, value, formats["input"])


def _write_audit(writer, outputs: ModelOutputs, formats) -> None:
    ws = writer.sheets["Model Audit & Quality Checks"]
    df = pd.DataFrame([finding.model_dump() for finding in outputs.audit_findings])
    _write_dataframe(writer, df, "Model Audit & Quality Checks", 2, 0, formats)
    for row_idx, status in enumerate(df["status"], start=3):
        fmt = formats["pass"] if status == "PASS" else formats["warning"] if status == "WARNING" else formats["error"]
        ws.write(row_idx, 1, status, fmt)
    ws.write(1, 0, "Overall status", formats["header"])
    overall_format = formats["pass"] if outputs.audit_status == "PASS" else formats["warning"] if outputs.audit_status == "WARNING" else formats["error"]
    ws.write(1, 1, outputs.audit_status, overall_format)


def _write_placeholder(writer, sheet_name: str, message: str) -> None:
    ws = writer.sheets[sheet_name]
    ws.write(2, 0, message)


def _select(outputs: ModelOutputs, columns: list[str]) -> pd.DataFrame:
    return outputs.tables["integrated_financials"][columns].reset_index()
