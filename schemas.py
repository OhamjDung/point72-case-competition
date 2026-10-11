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


class PeriodConfig(BaseModel):
    historical_years: list[str]
    forecast_years: list[str]
    quarterly_years: list[str]
    quarter_weights: list[float]
    fiscal_year_end_month: int = Field(ge=1, le=12)

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
    iterations: int = Field(default=500, ge=1)
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


class ModelInputs(BaseModel):
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

    @model_validator(mode="after")
    def validate_lengths_and_sources(self) -> "ModelInputs":
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

        for cohort in self.foot_locker_cohorts:
            _require_len(f"{cohort.name}.annual_comp_growth", cohort.annual_comp_growth, years)
            _require_len(f"{cohort.name}.contribution_margin", cohort.contribution_margin, years)
            _require_len(f"{cohort.name}.closures", cohort.closures, years)

        for synergy in self.synergies:
            _require_len(f"{synergy.name}.realization_rates", synergy.realization_rates, years)
            _require_len(f"{synergy.name}.implementation_costs", synergy.implementation_costs, years)
            _require_len(f"{synergy.name}.recurring_costs", synergy.recurring_costs, years)

        source_keys = {source.key for source in self.source_registry}
        missing = sorted(set(self.required_source_keys) - source_keys)
        if missing:
            raise ValueError(f"required source keys missing from source_registry: {missing}")
        if self.control.selected_scenario not in self.scenarios:
            raise ValueError("selected_scenario must exist in scenarios")
        return self


class AuditFinding(BaseModel):
    check: str
    status: Literal["PASS", "WARNING", "ERROR"]
    message: str


class ModelOutputs(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    scenario: str
    tables: dict[str, pd.DataFrame]
    audit_findings: list[AuditFinding]

    @property
    def audit_status(self) -> str:
        statuses = [finding.status for finding in self.audit_findings]
        if "ERROR" in statuses:
            return "ERROR"
        if "WARNING" in statuses:
            return "WARNING"
        return "PASS"


def _require_len(name: str, values: list[float], expected: int) -> None:
    if len(values) != expected:
        raise ValueError(f"{name} must contain {expected} values")
