# FTAI Financial Model: Build Spec (v1, 2026-10-06)

**Output:** `model/FTAI_Model.xlsx`, produced by the reproducible script `model/build_model.py` (openpyxl).
**Purpose:** decide Long vs Short and the price target for the Point72 Academy pitch, due 10/12/26.

**Competition requirements.** The model must have:
- a Summary tab with the recommendation, price target and valuation
- at least 2 years of history
- 5 years of projections, at least 2 of them quarterly
- company-specific drivers that link to the P&L
- the 2–3 key assumptions flagged
- sensitivity/scenario analysis
- a clear bridge from the base/consensus case to our case
- an easy-to-print layout, with page numbers and the team name on every page

The rules also say it must be the team's own model, built from a blank workbook. That is why the script creates the workbook from nothing and does not copy any external model.

## Inputs, all already sourced
- `research/FTAI/phase2/data/*.csv` covers the historical IS, segment EBITDA, cash flow, balance sheet, related party, debt, consensus and guidance. Every row cites its filing.
- `research/FTAI/phase2/A_2027_guide_segment_build.csv` holds the bear/base/bull 2027 segment builds and their drivers.
- `research/FTAI/thesis.md` holds the thesis, valuation logic, peer multiples and key facts.
- Market data as of 10/6/26: price $179.44, shares 102.71M, market cap $18.43B, EV $21.59B (stockanalysis). Net debt is EV minus market cap, about $3.16B. Use balance-sheet debt and cash where available and show the reconciliation.

## Conventions
- Blue font marks hard-coded inputs. Black marks formulas. Green marks links to other sheets.
- Yellow fill and **bold red labels** mark the 3 KEY ASSUMPTIONS, each with an Excel cell comment explaining it.
- **No hard-coded numbers inside formulas.** Every projection cell is a live formula referencing the Drivers tab. Historicals are inputs with a source note column.
- Every input has a cell comment or an adjacent "Source / rationale" column (filing, accession, URL).
- $ millions, except per-share figures. Fiscal year = calendar year.
- Scenario selector on the Drivers tab, a dropdown named `Scenario` with values Bear / Base / Bull / Mgmt Guide. All projections use `CHOOSE`/`INDEX` on the selected scenario.
- Print setup on every sheet:
  - landscape, fit to 1 page wide
  - header: "[TEAM NAME] | FTAI Aviation (NASDAQ: FTAI) | Short/Long TBD"
  - footer: "Page &P of &N" and the sheet name
  - print area set, gridlines off, frozen panes on labels

## Tabs

### 1. Summary
- Recommendation, which stays a formula-driven text cell.
- Current price, PT under each method (SOTP, P/E, DCF), and the blended PT with its weights as inputs.
- Upside/downside %.
- Scenario table: Bear / Base / Bull / Mgmt with probability weights as inputs, and the probability-weighted value.
- The 3 key assumptions with their values in each scenario.
- A mini chart of value/share by scenario (an openpyxl bar chart).
- 3 bullets summarizing the thesis.

### 2. Drivers (assumptions, with scenario columns Bear / Base / Bull / Mgmt Guide)
**Aerospace**
- modules sold per quarter
- revenue per module
- MRE (SCI) share of Aerospace revenue
- EBITDA margin, or EBITDA per module
- **KEY #1:** 2027 Aerospace EBITDA, which falls out of modules × EBITDA/module

**Power** (pro-rata, equity-accounted J&F JV; Adj. EBITDA includes FTAI's pro-rata share)
- units delivered per quarter, starting 2027 per management's "prudent to expect"
- EBITDA per unit
- **KEY #3:** Power units × EBITDA per unit
- Power working-capital investment

**Leasing**
- leasing book run-off, quarterly, as $ book value sold
- gain on sale as a % of book sold
- lease yield on the remaining book
- SCI servicing fees (Q2'26 actual $7.0M per quarter), with growth tied to SCI AUM
- pro-rata SCI EBITDA included in Adj. EBITDA
- cash distributions from SCI, kept separate because they are not equal to the pro-rata EBITDA

**Corporate and other**
- corporate costs
- D&A, linked to the leasing book plus the Aerospace capex base
- interest, from the debt schedule
- tax rate
- preferred dividends
- share count, with a buyback toggle (a $500M program is reported but unverified, so it defaults to OFF)

**Working capital**
- inventory days on Aerospace cost of sales
- **KEY #2:** inventory conversion, i.e. the 2H26 FCF ramp. This flows into cash flow.

**Valuation inputs**
- peer multiples per segment and per scenario (Aerospace 11.7x / 13x / 16x; Power 8x / 10x / 12x; Leasing at book × 1.0 / 1.0 / 1.2)
- forward P/E range (16–18x MRO peers)
- WACC and terminal growth for the DCF

**Defaults.** Base/bear/bull defaults come from A_2027_guide_segment_build.csv. Mgmt Guide must reproduce the $2.3B 2027 guide (1,400 / 450 / 450) and the 2026 guide (Aero $1,050M, Leasing $475M, total $1,525M; FCF $878M).

### 3. Historical
- FY2023A, FY2024A, FY2025A, plus quarterly Q1'24–Q2'26.
- Income statement, segment revenue (Aerospace products / MRE Contract / lease / maintenance / asset sales), segment Adj. EBITDA, gains on sale (including to the 2025 Partnership), cash flow (CFO and the key CFI lines), and balance sheet (inventory, leasing equipment, SCI investment, debt, equity).
- KPIs computed from those figures:
  - gains as % of Adj. EBITDA
  - MRE share of Aerospace revenue
  - Aerospace margin
  - inventory days
  - CFO/EBITDA
  - (CFO+CFI)/EBITDA
- Source column on every row.

### 4. Quarterly
- Q1'26A, Q2'26A, Q3'26E–Q4'27E, so 8 quarters in total with 2 actual.
- Segment build, then Adj. EBITDA, then the EPS bridge (D&A, interest, tax, preferred), then the cash-flow build.
- Quarters must sum to the annual figures on the Annual tab.

### 5. Annual
- FY2023A–FY2025A, then FY2026E–FY2030E (5 projection years).
- FY26 and FY27 are summed from Quarterly. FY28–FY30 are driven by annual growth and margin drivers.
- Economies of scale should show margin improvement with scale, up to a cap, per the competition tip.

### 6. FCF_Quality (the thesis tab)
Rebuild cash flow three ways, by year:
- (a) the company's "Adjusted FCF" definition, which adds back growth investment (turbines, parts, SCI co-investment), as stated on the Q4'25 call
- (b) GAAP CFO + CFI
- (c) "clean" CFO + CFI excluding seed-sale proceeds and insurance recoveries

Also show:
- the gap between pro-rata SCI EBITDA and cash distributions
- cash conversion ratios
- FY25 reconciliation of the $724M Adj. FCF to the $412.6M CFO+CFI: $252M named by the CFO, plus about $59M inferred acquisitions, flagged "inferred"
- 1H26: $250.4M total, less $175.7M seed proceeds, less $48.3M insurance, leaves about $26M after a roughly $351M inventory build

### 7. Valuation
- **SOTP** per scenario: 2027E segment EBITDA × multiple, plus Leasing at book, minus net debt, divided by shares. Note that TTM peer multiples are applied to 2027E because 2027 is the trailing year at a 12-month horizon.
- **P/E cross-check:** model FY27 EPS × 16–18x, shown alongside consensus FY27 EPS of about $8.87 (implied by the 20.2x forward P/E at $179.44).
- **DCF** on clean FCF for FY26–30, with a terminal value. Keep it simple.
- **Peer table:** HEICO 30.2x / 44.0x P/E; AAR 13.8x / 17.7x; StandardAero 11.7x / 15.9x; AerSale 17.4x / 18.1x; AerCap 12.4x / 8.5x; FTAI 21.7x / 20.2x (stockanalysis, 10/6/26).
- **Blended PT** using input weights.

### 8. Bridge
A waterfall from the **Mgmt Guide 2027 EBITDA ($2,300M)** to **our Base**, by segment: Aerospace Δ, Power Δ, Leasing Δ.

Then the value per share at the guide, minus each segment's value impact, gives our PT. Present it as a table plus an openpyxl bar chart.

Also show a second bridge from the Street mean PT of about $330 (methodology not public) to our PT, as a narrative table.

### 9. Sensitivity
Explicit formula grids. Excel Data Tables don't work from openpyxl, so each cell recomputes value directly.
- Value/share across 2027 Aerospace EBITDA (rows) × Aerospace multiple (columns).
- Value/share across Power units (rows) × EBITDA per unit (columns).
- FY26 clean FCF across inventory conversion % (rows) × Aerospace margin (columns).
- Conditional formatting: green above the current price, red below.

### 10. Sources
- Every source with its URL or accession and date.
- The list of inferred or unverified items.
- A note that the model was built with GenAI assistance (Claude) and verified against filings.

## Verification (required before reporting done)
1. Recalculate with the Python `formulas` library (`formulas.ExcelModel().loads(path).finish(); .calculate()`), or an equivalent, and confirm there are no errors (#REF!, #DIV/0!, #NAME?).
2. Tie-outs:
   - historical quarters sum to FY
   - Quarterly sums to Annual for FY26 and FY27
   - Mgmt Guide scenario yields 2027 EBITDA = $2,300M and 2026 = $1,525M
   - Base 2027 EBITDA ≈ $1,920M (agent A)
   - Base SOTP ≈ $172/share; Bear ≈ $115; Bull ≈ $280 (thesis.md section 2)
   - FY25 CFO = −$310.7M, CFI = +$723.3M, 1H26 CFO+CFI = $250.4M
3. Write `model/model_notes.md` covering the tie-out results, driver logic and any deviations from this spec.
