# FTAI Aviation model: build notes (2026-10-06)

Files: `model/build_model.py` (reproducible; run `python -I build_model.py`, about 20 seconds), `model/FTAI_Model.xlsx`, `model/scenario_snapshot.json` (fallback copy of the scenario snapshot).
The workbook is built from a blank `Workbook()`. It stores no cached values, so it calculates when opened in Excel (`fullCalcOnLoad` is set). All numbers below come from recalculating the workbook with the Python `formulas` library. Verification passed with 0 error cells in all four scenarios.

## 1. Tab list
| Tab | Content |
|---|---|
| Summary | Formula-driven recommendation, price target by method, scenario table with probability weights, 3 key assumptions, bar chart, 3 thesis bullets |
| Drivers | Scenario selector (dropdown, named `Scenario`) and every driver with Bear / Base / Bull / Mgmt Guide rows plus a "Selected" row. It also holds the parallel scenario engine and the KEY ASSUMPTION panel |
| Historical | FY23-FY25 and Q1'24-Q2'26 typed inputs, a source on every row, KPI formulas |
| Quarterly | Q1'26A, Q2'26A, Q3'26E-Q4'27E: segment build, EPS bridge, cash-flow build, debt/revolver, back-test of the EPS bridge |
| Annual | FY23A-FY25A, FY26E-FY30E. FY26/27 are summed from Quarterly. FY28-30 use growth drivers and a capped margin-scale rule |
| FCF_Quality | The three cash definitions, the SCI EBITDA vs cash gap, the FY25 and 1H26 reconciliations, the 2H26 requirement |
| Valuation | SOTP for all 4 scenarios (live), P/E, DCF, blended price target, peer table, snapshot block |
| Bridge | Mgmt guide to Base EBITDA and per-share value, waterfall chart, Street-PT narrative bridge |
| Sensitivity | 3 explicit formula grids with conditional formatting |
| Checks | 86 formula-driven pass/fail tie-outs (extra tab) |
| Sources | Sources, accessions, inferred/unverified list, GenAI note |

## 2. Driver logic
- **Aerospace.** Modules x revenue per module = segment revenue. Modules x EBITDA per module = EBITDA (KEY #1). MRE share is a memo with a profit elimination of 4.1% of MRE revenue. FY28-30 margin = MIN(cap, prior margin + 0.10 x volume growth), so margin rises with scale up to a scenario cap.
- **Power.** Units x $7.5M EBITDA per unit (KEY #3). Units start in 2027. Turbine working capital is funded one quarter ahead of delivery ($17.5M per unit) and released on delivery.
- **Leasing.** Book roll: beginning book less book sold less depreciation plus acquisitions. EBITDA = yield on the beginning book + gain % x book sold + SCI servicing fee (rate x AUM) + pro-rata SCI EBITDA and co-invest returns. Distributions are 65% of pro-rata EBITDA, so there is a cash gap. The 2027 pro-rata and fee line is calibrated to A's SCI split (190 / 240 / 300).
- **EPS bridge.** Adj. EBITDA less D&A (leasing book rate x beginning book, plus other D&A that grows with the capex base) less interest (coupon schedule + other + revolver) less EBITDA-to-pretax adjustments, then tax, preferred/NCI and diluted shares. The adjustments are the SCI pro-rata EBITDA not converted into equity earnings, other adjustments, and the non-converted share of Power. The bridge is calibrated on 1H26.
- **Cash.** CFO + CFI is built as one line: EBITDA, less gains (proceeds are in CFI), less non-cash pro-rata, plus distributions, less interest and tax, less the inventory build (days-driven, KEY #2), less Power WC, plus book sold, less acquisitions, SCI co-investment and capex. Clean = less seed-sale and insurance proceeds. The company-defined Adjusted FCF adds back SCI co-invest, **net** Power turbine investment (floored at zero) and hot-section parts. The revolver sweeps to a $300M minimum cash.
- **Scenario handling.** The Drivers tab has a Scenario dropdown. SOTP is live for all four scenarios. P/E, DCF and blended are live for the selected scenario. The script runs four full recalculations and stores all four in the Valuation snapshot block, with a live freshness cell. Re-run the script after changing a driver.

## 3. The three key assumptions
1. **KEY #1: 2027 Aerospace EBITDA = modules x EBITDA per module.** Values: Bear 1,050 / Base 1,230 / Bull 1,430 / Mgmt 1,400. The guide is a volume call (1,700 modules, +42% vs the 2026 pace).
2. **KEY #2: inventory conversion % (the 2H26 FCF ramp).** The Mgmt Guide value of 11.3% is back-solved so the FY26 company-defined Adjusted FCF equals $878M. It is not a judgment input. Bear / Base / Bull are 0% / 10% / 25% (judgment).
3. **KEY #3: 2027 Power EBITDA = units x $7.5M.** Values: Bear 150 / Base 330 / Bull 600 / Mgmt 450. The $7.5M per unit is an unverified secondary figure.

## 4. Tie-out results (all PASS in all four scenarios; 86 checks on the Checks tab)
| Category | Result |
|---|---|
| Historical quarters sum to FY, FY24 and FY25 (revenue, cost of sales, D&A, interest, 5 EBITDA lines, CFO, CFI, net income; 24 checks) | PASS. For IS and EBITDA lines this holds by construction, because Q4 is derived as FY less 9M. CFO/CFI quarters are derived from YTD |
| Quarterly sums to Annual, FY26 and FY27 (11 lines x 2) | PASS |
| Mgmt Guide FY27 segment EBITDA = 2,300 (1,400 / 450 / 450) | PASS: 2,299.97 |
| Mgmt Guide FY26 = 1,525 (Aero 1,050, Leasing 475) | PASS: 1,525.06 (Aero 1,050.0, Leasing 475.04) |
| Base FY27 ~ 1,920; Bear ~ 1,470; Bull ~ 2,480 | PASS: 1,920.03 / 1,470.00 / 2,480.06 |
| Engine for selected scenario = Quarterly (no logic drift) | PASS |
| SOTP Base ~172 / Bear ~115 / Bull ~280 | PASS within $2: 171.14 / 114.62 / 279.14 (see deviations) |
| FY25 CFO = -310.7, CFI = +723.3, CFO+CFI = 412.6; 1H26 CFO+CFI = 250.4; seed 175.7; insurance 48.3; clean 26.4 | PASS |
| FY25 $724M less $412.6M less $252M named = $59.4M residual | PASS (flagged INFERRED, not confirmed) |
| Mgmt Guide FY26 Adjusted FCF = 878 | PASS: 878.02 (snapshot, back-solved) |
| EPS bridge back-test on actuals | PASS: Q1'26 1.35 vs 1.29 reported (+0.06), Q2'26 1.06 vs 1.13 (-0.07), 1H26 2.41 vs 2.42 |
| Leasing book never negative (4 scenarios); book sold <= beginning book; net debt reconciliation (3,159 vs 3,160) | PASS |
| Error-cell scan (Quarterly, Annual, Valuation); probability and blend weights = 100% | PASS |

## 5. Scenario outputs
| | Bear | Base | Bull | Mgmt Guide |
|---|---|---|---|---|
| FY26E segment EBITDA ($M) | 1,321 | 1,406 | 1,503 | 1,525 |
| FY27E segment EBITDA ($M) | 1,470 | 1,920 | 2,480 | 2,300 |
| FY27E total Adj. EBITDA, company basis ($M) | 1,274 | 1,720 | 2,275 | 2,094 |
| FY26E EPS | $4.07 | $4.68 | $5.15 | $5.20 |
| FY27E EPS | $5.07 | $7.88 | $11.24 | $10.12 |
| SOTP $/share | $114.62 | $171.14 | $279.14 | $204.33 |
| P/E $/share (17x) | $86.15 | $133.92 | $191.06 | $171.96 |
| DCF $/share | $86.51 | $143.41 | $199.94 | $190.78 |
| Blended $/share (40/30/30) | $97.65 | $151.65 | $228.96 | $190.55 |
| FY26E company-defined Adjusted FCF ($M) | 647 | 753 | 852 | 878 |

- Probability-weighted blended value (25/50/25/0) is **$157.48, or -12.2% vs $179.44**, so the formula gives SHORT, flagged MARGINAL. The probability-weighted SOTP alone is $184.0 (+2.5%).
- **Base FY27 EPS is $7.88 vs about $8.87 consensus-implied (-11%).** Mgmt Guide EPS is $10.12 (+14% above consensus-implied), so the Street's EPS sits between our Base and the guide. Caveat: the $8.87 is derived from a forward P/E that conflicts with stockanalysis's own FY26 EPS.

## 6. How fragile the SHORT call is (judgment calls that matter)
The call is SHORT only through the P/E and DCF legs. The SOTP leg is about +2.5% on a probability-weighted basis, and the call is marginal against a -10% threshold. Two things drive it: the 40/30/30 weights, and the EPS bridge.

EPS bridge sensitivity (re-run recalcs on all four scenarios, only the named driver changed):

| Case | Base FY27 EPS | Mgmt FY27 EPS | Prob-weighted blended |
|---|---|---|---|
| As built (equity-earnings conversion 13.6% on the 1H26 average, Power pre-tax conversion 75%) | $7.88 | $10.12 | $157.5 (-12.2%) |
| Conversion at Q2'26-only rate (35.6%) | $8.25 | $10.62 | $159.0 (-11.4%) |
| Q2-only conversion plus Power pre-tax conversion 100% | $8.90 | $11.51 | $161.5 (-10.0%, at the threshold) |

- On the most generous bridge, Base EPS is about equal to the $8.87 consensus-implied figure and the call is exactly on the threshold.
- Even at guide EBITDA the model's FY26 EPS is $5.20 vs $5.83 consensus (Q3'26 $1.33 vs $1.54). The cause is the bridge's treatment of pro-rata SCI EBITDA. Mgmt's 2H26 Leasing step-up is attributed to SCI (per A), and that EBITDA is non-cash and not in pre-tax income.
- D&A falls from about $181M (FY26) to about $114M (FY27) as the leasing book runs off. That is a tailwind to EPS already in the numbers.
- The DCF terminal value is 81% of EV (Mgmt). WACC 10% and g 3% were fixed before viewing output and were not tuned.

## 7. Key finding for the pitch: the $878M guide on a narrow definition
- The 1H26 company-reported Adjusted FCF ($255M) is only about $4.6M above CFO+CFI ($250.4M). The FY25 add-backs ($252M named) are not consistent with that.
- At guide-level EBITDA (Mgmt Guide scenario) with the FY25-style add-backs, 2H26 needs an 11.3% inventory conversion to produce $623M of Adjusted FCF. In that case 2H26 GAAP CFO+CFI is only **$358M**, and $265M of the $623M is add-backs (SCI co-invest $135M, Power turbines $105M, parts $25M).
- If add-backs stay at the 1H26 level (about $5M), the guide needs about $623M of 2H26 **GAAP** CFO+CFI. That is about $265M more than the model produces. It implies roughly **58% inventory conversion** (11.3% + 265/561, where 561 is the $M of FCF per 100% of conversion), against the 11.3% back-solved on the broader definition.
- Also in the 2H26 requirement: $623M is about 3.2x the Q2'26 Adjusted FCF run-rate of $97M per quarter.

## 8. Deviations from the spec
- **Extra Checks tab** (spec lists 10 tabs).
- **Preferred deducted.** SOTP deducts $65M of preferred at liquidation, and Leasing book is 1,146.4 + 365.5 = $1,511.9M (thesis says about $1.5B). Together these put SOTP $0.5-1.0 below thesis (171.1 vs ~172; 114.6 vs ~115; 279.1 vs ~280). A switch on Drivers turns the deduction off.
- **Rounded inputs.** EBITDA per module (0.7778, 0.82, 0.8412, 0.8235), Bull Power units (80, to land $600M) and the calibrated SCI pro-rata series are chosen to hit A's totals and the 2026/2027 guide. The model's own rounding residual is 0.0 to 0.06.
- **P/E, DCF and blended per scenario are snapshot values.** SOTP is live for all four scenarios. The other three come from the four full-model recalcs the script runs. A freshness cell flags a stale snapshot.
- **FY23/FY24 pretax, tax and net income are blank.** The source CSV is not cleanly parsed for those periods. FY25 and all 2026 quarters are fine.
- **Segment-basis vs company-basis EBITDA.** Spec tie-outs and the SOTP use the segment basis (Aero + Power + Leasing). EPS and FCF use the company basis, which includes Corporate (about -$40M per quarter) and eliminations. Both lines are shown.
- **Corporate costs excluded from SOTP**, per the spec. Memo on the Valuation tab: capitalising 2027 corporate costs (about $160M) at the blended Aero+Power multiple lowers value per share by roughly $17-23 (Base: $151.9 vs $171.1).
- **Insurance** uses CFI proceeds (48.3), not the CFO gain add-back (49.5).
- **Company-defined Adjusted FCF** uses the FY25-style add-backs (SCI co-invest, net Power turbine investment, hot-section parts) for the forecast. The add-back for Power turbines is net of the delivery release (floored at zero). Without that netting, FY27+ Adjusted FCF double-counted.
- Header text keeps the placeholder "[TEAM NAME]" (change `TEAM` at the top of the script).

## 9. Assumptions added (blue inputs with rationale on the Drivers tab, listed on Sources)
All clearly labelled. Highlights:
- **Not in the provided data and unverified:** common dividend $0.30 per share per quarter (it only affects cash and revolver, not valuation); SCI AUM starting at about $6.0B and its growth path; revolver rate 6%; refinancing coupon 7.0% on the 2028 notes; minimum cash $300M.
- **Invented conversions:** Power cash conversion 75% and Power EBITDA-to-pretax conversion 75% (these move Bull EPS materially); pro-rata SCI EBITDA of 28.0 per quarter in Q1'26 (equal to Q2'26).
- **Leasing:** yield 8.5%, gain on sale 15%, seed share 30%, acquisitions 25 per quarter, book-sold paths, FY28-30 growth.
- **Aerospace:** FY28-30 module growth, margin caps (28 / 31 / 33 / 31%), scale elasticity 0.10, MRE share 22%, 2H26 module splits, inventory target days 150, conversion phasing.
- **Other:** tax rate 18%, other D&A $2.5M per quarter, capex $15M per quarter, 10-year life, other EBITDA-to-pretax adjustments calibrated on 1H26, blend weights 40/30/30, scenario probabilities 25/50/25/0, Q1'26 module estimate (265), buyback toggle (OFF).
- Unverified secondary inputs (from the research files): Power $7.5M per unit and about $25M per unit price, the 1,700-module target, module counts from calls, and the $500M buyback.

## Change log
**v1.1 (orchestrator, 2026-10-06)**
- Corporate costs are now included in the SOTP: `corpcap` = 1, so 2027E corporate costs are multiplied by each scenario's blended Aero+Power multiple. v1 had excluded them because of a spec error.
- The SOTP excluding corporate costs is kept as a memo row. Its checks still tie to the thesis v0.2 targets ($115 / $172 / $280).

**Blended outputs ($/share)**

| Scenario | Blended | SOTP |
|---|---|---|
| Bear | 90.6 | 97.1 |
| Base | 144.0 | 151.9 |
| Bull | 219.7 | 256.1 |
| Mgmt Guide | 182.9 | 185.2 |

**Recalc check:** 88 checks, 0 FAIL. The 3 "#" cells are unit labels, not errors.
