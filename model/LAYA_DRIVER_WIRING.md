# Manual Excel wiring for the Laya comp driver

The competition model must remain the team's own workbook. Type these formulas into the existing workbook manually; do not use this note to generate or replace the workbook.

## Flagged assumptions

Add four yellow input cells on `Assumptions` and name them:

| Name | Initial value | Comment |
|---|---:|---|
| `Laya_dComp_bp` | 0 | `Source: outputs/nowcast.json, delta_comp_bp. Apply only with the recorded verdict.` |
| `Laya_Switch` | 0 | `1 = Laya case; 0 = base case.` |
| `Laya_Decay` | 0.5 | `Share of the FY2026 Q3 comp adjustment carried into FY2026 Q4.` |
| `Laya_Verdict` | `pending` | `Source: outputs/nowcast.json; allowed values: nowcast or scenario.` |

## Comp and financial flow

Keep `Comp_Base` visible next to `Comp_Case`:

- FY2026 Q3: `=Comp_Base + Laya_Switch*Laya_dComp_bp/10000`
- FY2026 Q4: `=Comp_Base + Laya_Switch*Laya_dComp_bp/10000*Laya_Decay`
- Later quarters: `=Comp_Base`

Use the workbook's existing revenue build. The incremental chain should be formula-driven and should not alter any other driver:

`Comp_Case -> comparable revenue -> total revenue -> gross profit -> operating income -> after-tax income -> EPS -> price target`.

From FY2025 Q3 onward, the reported `gross_margin_pct` in the P1 fundamentals handoff is consolidated and includes Foot Locker plus acquisition inventory charges. Do not label it as a standalone DICK'S Business margin. Any Foot Locker comparable-sales figure used in the workbook must be labelled **proforma**, matching DKS's disclosure.

Useful audit rows:

- `Incremental_Revenue = Revenue_Laya - Revenue_Base`
- `Incremental_Gross_Profit = Gross_Profit_Laya - Gross_Profit_Base`
- `Incremental_EBIT = EBIT_Laya - EBIT_Base`
- `Incremental_Net_Income = Incremental_EBIT*(1-Tax_Rate)`
- `Incremental_EPS = Incremental_Net_Income/Diluted_Shares`
- `Incremental_PT = Price_Target_Laya - Price_Target_Base`

## Two-way sensitivity

Put a live link to the selected price-target output in the table's upper-left corner. Put `Laya_dComp_bp` down the first column from -300 to +300 in 100 bp steps. Put gross-margin changes across the first row from -100 to +100 bp. Create an Excel two-variable Data Table using `Laya_dComp_bp` as the column input cell and the model's gross-margin-change assumption as the row input cell.

## Price-target bridge

Build formula-linked rows for base/consensus price target, incremental revenue, gross-profit flow-through, operating leverage, tax, diluted shares, and Laya-informed price target. The final row must equal the model's live price-target output. Label the bridge `scenario` unless `outputs/nowcast.json` records `verdict: nowcast`.
