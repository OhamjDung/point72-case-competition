from __future__ import annotations

from datetime import date
from typing import Literal

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


Confidence = Literal["low", "medium", "high"]
InputType = Literal[
    "official filing",
    "official company release",
    "management guidance",
    "consensus",
    "market data",
    "internal judgment",
]


AuditStatus = Literal["PASS", "WARNING", "ERROR", "BLOCKED"]
ModelMode = Literal["fixture", "sourced"]


class ControlPanel(BaseModel):
    company_name: str
    ticker: str
    valuation_date: date
    data_cutoff: date
    last_reported_quarter: str
    forecast_version: str
    selected_scenario: str
    reference_share_price: float = Field(gt=0)
    risk_free_rate: float
    market_risk_premium: float
    terminal_growth: float
    wacc: float = Field(gt=0)
    tax_rate: float = Field(ge=0, le=1)
    schema_version: str = "2.0"
    model_mode: ModelMode = "fixture"
    units: str = "USD millions"
    minimum_cash: float = Field(default=500.0, ge=0)
    revolver_capacity: float = Field(default=0.0, ge=0)
    current_diluted_shares: float | None = Field(default=None, gt=0)
    valuation_date_cash: float | None = Field(default=None, ge=0)
    valuation_date_debt: float | None = Field(default=None, ge=0)
    valuation_date_finance_leases: float = Field(default=0.0, ge=0)
    nonoperating_assets: float = 0.0
    other_equity_claims: float = 0.0
    midyear_convention: bool = True


class PeriodConfig(BaseModel):
    historical_years: list[str]
    forecast_years: list[str]
    quarterly_years: list[str]
    quarter_weights: list[float]
    fiscal_year_end_month: int = Field(ge=1, le=12)
    terminal_convergence_years: list[str] = Field(default_factory=lambda: ["FY2031", "FY2032", "FY2033"])

    @field_validator("quarter_weights")
    @classmethod
    def quarter_weights_sum_to_one(cls, values: list[float]) -> list[float]:
        if len(values) != 4:
            raise ValueError("quarter_weights must contain four quarters")
        if abs(sum(values) - 1.0) > 0.0001:
            raise ValueError("quarter_weights must sum to 1.0")
        return values

    @model_validator(mode="after")
    def quarterly_years_are_forecast_years(self) -> "PeriodConfig":
        invalid = set(self.quarterly_years) - set(self.forecast_years)
        if invalid:
            raise ValueError(f"quarterly_years must be forecast years: {sorted(invalid)}")
        return self


class HistoricalFinancials(BaseModel):
    revenue: float
    gross_profit: float
    ebit: float
    net_income: float
    diluted_shares: float
    operating_cash_flow: float
    capex: float
    cash: float
    inventory: float
    debt: float
    lease_liabilities: float
    shareholders_equity: float
    accounts_receivable: float = 0.0
    prepaid_and_other_current_assets: float = 0.0
    accounts_payable: float = 0.0
    accrued_expenses: float = 0.0
    deferred_revenue: float = 0.0
    income_taxes_payable: float = 0.0
    ppe: float = 0.0
    operating_lease_assets: float = 0.0
    goodwill_and_intangibles: float = 0.0
    other_assets: float = 0.0
    other_liabilities: float = 0.0
    publication_date: date | None = None


class SegmentConfig(BaseModel):
    display_name: str
    starting_store_count: float = Field(ge=0)
    starting_sales_per_store: float = Field(ge=0)
    starting_digital_revenue: float = Field(ge=0)
    openings: list[float]
    closures: list[float]
    digital_growth: list[float]
    maintenance_capex_per_store: float = Field(ge=0)
    growth_capex_per_opening: float = Field(ge=0)


class FootLockerCohort(BaseModel):
    name: str
    store_count: float = Field(ge=0)
    sales_per_store: float = Field(ge=0)
    annual_comp_growth: list[float]
    contribution_margin: list[float]
    closures: list[float]
    retained_sales_pct: float = Field(ge=0, le=1)
    closure_cost_per_store: float = Field(ge=0)


class ScenarioAssumptions(BaseModel):
    legacy_comp_growth: list[float]
    legacy_gross_margin: list[float]
    legacy_opex_pct: list[float]
    foot_locker_comp_growth: list[float]
    foot_locker_gross_margin: list[float]
    foot_locker_opex_pct: list[float]
    corporate_expense_pct: list[float]
    capex_pct_revenue: list[float]
    depreciation_pct_revenue: list[float]
    operating_nwc_pct_revenue: list[float]
    interest_rate: list[float]
    debt_repayment: list[float]
    dividends: list[float]
    share_repurchases: list[float]
    avg_repurchase_price: list[float]
    diluted_share_base: float = Field(gt=0)
    stock_comp_dilution: list[float]
    scenario_probability: float = Field(ge=0, le=1)
    valuation_multiple: float = Field(gt=0)
    inventory_days: list[float] = Field(default_factory=list)
    receivable_days: list[float] = Field(default_factory=list)
    payable_days: list[float] = Field(default_factory=list)
    other_nwc_pct_revenue: list[float] = Field(default_factory=list)
    stock_comp_expense: list[float] = Field(default_factory=list)
    share_issuance: list[float] = Field(default_factory=list)
    cash_tax_rate: list[float] = Field(default_factory=list)


class SynergyInitiative(BaseModel):
    name: str
    max_annual_savings: float = Field(ge=0)
    realization_rates: list[float]
    implementation_costs: list[float]
    recurring_costs: list[float]
    probability: float = Field(ge=0, le=1)


class ValuationAssumptions(BaseModel):
    legacy_ebitda_multiple: float = Field(gt=0)
    foot_locker_ebitda_multiple: float = Field(gt=0)
    synergy_ebitda_multiple: float = Field(gt=0)
    relative_pe_multiple: float = Field(gt=0)
    relative_fcf_yield: float = Field(gt=0)


class MonteCarloVariable(BaseModel):
    name: str
    distribution: Literal["normal", "triangular"]
    mean: float | None = None
    stdev: float | None = None
    low: float | None = None
    mode: float | None = None
    high: float | None = None
    min_value: float | None = None
    max_value: float | None = None

    @model_validator(mode="after")
    def validate_distribution_parameters(self) -> "MonteCarloVariable":
        if self.distribution == "normal" and (self.mean is None or self.stdev is None):
            raise ValueError(f"{self.name} normal distribution requires mean and stdev")
        if self.stdev is not None and self.stdev < 0:
            raise ValueError(f"{self.name} standard deviation must be non-negative")
        if self.distribution == "triangular" and (self.low is None or self.mode is None or self.high is None):
            raise ValueError(f"{self.name} triangular distribution requires low, mode, and high")
        if self.distribution == "triangular" and not (self.low <= self.mode <= self.high):
            raise ValueError(f"{self.name} triangular distribution requires low <= mode <= high")
        return self


class CorrelationAssumption(BaseModel):
    left: str
    right: str
    correlation: float = Field(ge=-1, le=1)


class ProbabilisticValuationConfig(BaseModel):
    enabled: bool = True
    iterations: int = Field(default=10_000, ge=1)
    random_seed: int = 72
    variables: list[MonteCarloVariable] = Field(default_factory=list)
    correlations: list[CorrelationAssumption] = Field(default_factory=list)


class ThesisCatalyst(BaseModel):
    name: str
    expected_timing: str
    metric: str
    model_forecast: float
    latest_value: float | None = None
    bullish_threshold: float
    bearish_threshold: float
    higher_is_better: bool = True
    thesis_implication: str


class ForecastVarianceEntry(BaseModel):
    snapshot_name: str
    period: str
    metric: Literal["revenue", "ebit", "eps", "fcff"]
    prior_forecast: float
    actual: float | None = None
    attribution_driver: str = "Unattributed"


class BalanceSheetStart(BaseModel):
    cash: float
    operating_nwc: float
    ppe: float
    goodwill_and_intangibles: float
    debt: float
    lease_liabilities: float
    other_liabilities: float
    shareholders_equity: float
    accounts_receivable: float = 0.0
    inventory: float = 0.0
    prepaid_and_other_current_assets: float = 0.0
    accounts_payable: float = 0.0
    accrued_expenses: float = 0.0
    deferred_revenue: float = 0.0
    income_taxes_payable: float = 0.0
    operating_lease_assets: float = 0.0
    finance_lease_liabilities: float = 0.0
    other_assets: float = 0.0
    common_stock_and_apic: float = 0.0
    retained_earnings: float = 0.0
    accumulated_oci: float = 0.0
    treasury_stock: float = 0.0


class DebtTranche(BaseModel):
    name: str
    opening_balance: float = Field(ge=0)
    coupon_rate: float = Field(ge=0)
    maturity_year: str
    mandatory_repayments: list[float] = Field(default_factory=list)
    is_revolver: bool = False
    capacity: float = Field(default=0.0, ge=0)


class LeaseAssumptions(BaseModel):
    cash_payments: list[float] = Field(default_factory=list)
    new_operating_leases: list[float] = Field(default_factory=list)
    discount_rate: list[float] = Field(default_factory=list)
    closure_terminations: list[float] = Field(default_factory=list)
    impairments: list[float] = Field(default_factory=list)


class PurchaseAccounting(BaseModel):
    transaction_date: date | None = None
    purchase_price: float = Field(default=0.0, ge=0)
    acquired_cash: float = 0.0
    acquired_working_capital: float = 0.0
    acquired_ppe: float = 0.0
    acquired_rou_assets: float = 0.0
    acquired_intangibles: float = 0.0
    acquired_goodwill: float = 0.0
    assumed_debt: float = 0.0
    assumed_operating_leases: float = 0.0
    other_net_liabilities: float = 0.0
    preliminary: bool = True


class WaccInputs(BaseModel):
    beta: float = Field(default=1.0, ge=0)
    pre_tax_cost_of_debt: float = Field(default=0.05, ge=0)
    market_value_equity: float = Field(default=0.0, ge=0)
    market_value_debt: float = Field(default=0.0, ge=0)
    source_note: str = "Analyst input pending dated public-market verification"


class BacktestObservation(BaseModel):
    origin_date: date
    target_period: str
    metric: Literal["revenue", "ebit", "eps", "fcff"]
    forecast: float
    actual: float
    actual_publication_date: date
    lower_bound: float | None = None
    upper_bound: float | None = None


class SourceEntry(BaseModel):
    key: str
    value: str | float
    unit: str
    period: str
    source_name: str
    source_date: date
    access_date: date
    confidence: Confidence
    input_type: InputType
    source_id: str | None = None
    url: str | None = None
    accession: str | None = None
    locator: str | None = None
    publisher: str | None = None
    as_of_date: date | None = None
    transformation: str | None = None
    mapped_fields: list[str] = Field(default_factory=list)
    judgment_reason: str | None = None
    redistributable: bool = True


class ModelInputsV2(BaseModel):
    model_config = ConfigDict(extra="forbid")

    control: ControlPanel
    periods: PeriodConfig
    historical: dict[str, HistoricalFinancials]
    segments: dict[Literal["legacy_dicks", "foot_locker"], SegmentConfig]
    foot_locker_cohorts: list[FootLockerCohort]
    scenarios: dict[str, ScenarioAssumptions]
    synergies: list[SynergyInitiative]
    valuation: ValuationAssumptions
    probabilistic_valuation: ProbabilisticValuationConfig | None = None
    thesis_catalysts: list[ThesisCatalyst] = Field(default_factory=list)
    forecast_variance: list[ForecastVarianceEntry] = Field(default_factory=list)
    balance_sheet_start: BalanceSheetStart
    source_registry: list[SourceEntry]
    required_source_keys: list[str] = Field(default_factory=list)
    debt_tranches: list[DebtTranche] = Field(default_factory=list)
    leases: LeaseAssumptions = Field(default_factory=LeaseAssumptions)
    purchase_accounting: PurchaseAccounting = Field(default_factory=PurchaseAccounting)
    wacc_inputs: WaccInputs = Field(default_factory=WaccInputs)
    backtest_observations: list[BacktestObservation] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_lengths_and_sources(self) -> "ModelInputsV2":
        years = len(self.periods.forecast_years)
        for name, segment in self.segments.items():
            _require_len(f"{name}.openings", segment.openings, years)
            _require_len(f"{name}.closures", segment.closures, years)
            _require_len(f"{name}.digital_growth", segment.digital_growth, years)

        scenario_fields = [
            "legacy_comp_growth",
            "legacy_gross_margin",
            "legacy_opex_pct",
            "foot_locker_comp_growth",
            "foot_locker_gross_margin",
            "foot_locker_opex_pct",
            "corporate_expense_pct",
            "capex_pct_revenue",
            "depreciation_pct_revenue",
            "operating_nwc_pct_revenue",
            "interest_rate",
            "debt_repayment",
            "dividends",
            "share_repurchases",
            "avg_repurchase_price",
            "stock_comp_dilution",
        ]
        for scenario_name, scenario in self.scenarios.items():
            for field_name in scenario_fields:
                _require_len(f"{scenario_name}.{field_name}", getattr(scenario, field_name), years)
            optional_scenario_fields = [
                "inventory_days",
                "receivable_days",
                "payable_days",
                "other_nwc_pct_revenue",
                "stock_comp_expense",
                "share_issuance",
                "cash_tax_rate",
            ]
            for field_name in optional_scenario_fields:
                values = getattr(scenario, field_name)
                if values:
                    _require_len(f"{scenario_name}.{field_name}", values, years)

        for cohort in self.foot_locker_cohorts:
            _require_len(f"{cohort.name}.annual_comp_growth", cohort.annual_comp_growth, years)
            _require_len(f"{cohort.name}.contribution_margin", cohort.contribution_margin, years)
            _require_len(f"{cohort.name}.closures", cohort.closures, years)

        for synergy in self.synergies:
            _require_len(f"{synergy.name}.realization_rates", synergy.realization_rates, years)
            _require_len(f"{synergy.name}.implementation_costs", synergy.implementation_costs, years)
            _require_len(f"{synergy.name}.recurring_costs", synergy.recurring_costs, years)

        for field_name in ["cash_payments", "new_operating_leases", "discount_rate", "closure_terminations", "impairments"]:
            values = getattr(self.leases, field_name)
            if values:
                _require_len(f"leases.{field_name}", values, years)
        for tranche in self.debt_tranches:
            if tranche.mandatory_repayments:
                _require_len(f"debt_tranches.{tranche.name}.mandatory_repayments", tranche.mandatory_repayments, years)

        source_keys = {source.key for source in self.source_registry}
        if len(source_keys) != len(self.source_registry):
            raise ValueError("source_registry keys must be unique")
        missing = sorted(set(self.required_source_keys) - source_keys)
        if missing:
            raise ValueError(f"required source keys missing from source_registry: {missing}")
        if self.control.selected_scenario not in self.scenarios:
            raise ValueError("selected_scenario must exist in scenarios")
        probability_total = sum(item.scenario_probability for item in self.scenarios.values())
        if abs(probability_total - 1.0) > 1e-6:
            raise ValueError(f"scenario probabilities must sum to 1.0; got {probability_total:.6f}")
        if self.control.wacc <= self.control.terminal_growth:
            raise ValueError("WACC must be greater than terminal growth")
        future_sources = [source.key for source in self.source_registry if source.source_date > self.control.data_cutoff]
        if future_sources:
            raise ValueError(f"source dates after data cutoff are not permitted: {sorted(future_sources)}")
        return self


# Backward-compatible public alias. The loader migrates legacy payloads into this
# versioned contract and never upgrades fixture data to sourced status.
ModelInputs = ModelInputsV2


class AuditFinding(BaseModel):
    check: str
    status: AuditStatus
    message: str
    task_id: str | None = None
    residual: float | None = None
    tolerance: float | None = None


class ModelOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    scenario: str
    tables: dict[str, pd.DataFrame]
    audit_findings: list[AuditFinding]
    model_mode: ModelMode = "fixture"
    diagnostics: dict[str, float | str | bool] = Field(default_factory=dict)

    @property
    def audit_status(self) -> str:
        statuses = [finding.status for finding in self.audit_findings]
        if "ERROR" in statuses:
            return "ERROR"
        if "BLOCKED" in statuses:
            return "BLOCKED"
        if "WARNING" in statuses:
            return "WARNING"
        return "PASS"


def _require_len(name: str, values: list[float], expected: int) -> None:
    if len(values) != expected:
        raise ValueError(f"{name} must contain {expected} values")
