# FTAI Aviation: Phase 2 input data notes (prepared 2026-10-06)

All files are in `phase2/data/`. Units are USD millions unless stated. Sources are SEC EDGAR filings (CIK 1590364) pulled directly on 2026-10-06, plus the free web pages listed in consensus.csv. Every row carries a source column (accession numbers included for filings). Nothing was copied from any firm's model.

## Files

| File | Content |
|---|---|
| is_quarterly.csv | Long format (period, basis, segment, line_item, value, source). Q1-23 to Q2-26 plus FY23/24/25. Segment columns: Aerospace Products, Aviation Leasing, Corporate and Other, Eliminations (2025 onward), Total. Lines: lease income, maintenance revenue, asset sales revenue, aerospace products revenue, MRE Contract revenue, other revenue, total revenues, cost of sales, opex, G&A, D&A, interest expense (positive = expense), equity in earnings, gain on sale to 2025 Partnership, other income, taxes, net income. Consolidated net income attributable, diluted EPS, diluted shares are in the same file (segment = Total). |
| segment_ebitda.csv | Adjusted EBITDA by Aerospace, Leasing, Corporate, Eliminations, Total, quarterly plus FY. Module counts and company-level gains appended (see caveats). |
| cash_flow.csv | Quarterly CFO, CFI, sale proceeds, proceeds from sale to the 2025 Partnership, acquisition of leasing equipment, investment in unconsolidated entities, PP&E, inventory change, CFS gain add-backs, insurance. Company-reported Adjusted FCF rows with reconciliation. Prior-research inventory-sourced items carried over (labelled). |
| balance_sheet.csv | Quarter-end cash, inventory, leasing equipment, investments, total assets, debt by instrument, issuance costs, liabilities, equity, preferred share count. |
| related_party.csv | 2025 Partnership / SCI: MRE revenue and share of revenue, servicing fees, seed-asset gains, profit elimination, receivables, equity investment. |
| debt_schedule.csv | Each note, coupon, maturity, face, carrying value (6/30/26). |
| consensus.csv | Every free source side by side with date; market data. |
| guidance_history.csv | Every guidance figure with date and revision. |

## Method

- Segment tables parsed from the segment note of each 10-Q/10-K (three-month blocks), taking the LATEST filing that contains each period (so earlier periods are on the recast basis, e.g. V2500 moved into Aerospace Products in Q4-23). Vintage is in the source column.
- Q4 = FY (10-K) minus 9M (Q3 10-Q YTD). Marked `derived_FY_less_9M`. Cash flow quarters beyond Q1 are YTD minus prior YTD, marked DERIVED.
- Adjusted EBITDA by segment: Q1-Q3 from the three-month Adjusted EBITDA reconciliation in the 10-Q (segment note through 2024, MD&A from 2025). Eliminations = total less the three segments (profit elimination on sales to the 2025 Partnership; matches the disclosed elimination: Q1-25 6.950, Q2-25 4.935, Q3-25 3.908, Q1-26 10.000, Q2-26 6.597).

## Tie-out checks (all run in code)

| Check | Result |
|---|---|
| Segment columns sum to Total, every line, every period | 0 mismatches |
| Four quarters sum to FY: revenue, cost of sales, D&A (FY23/24/25) | PASS (exact) |
| Derived Q4 vs Q4 release: revenue Q4-23 312.737, Q4-24 498.819, Q4-25 662.028; cost of sales, D&A, interest Q4-25 | PASS |
| Quarterly net income attributable sums to FY (212.022 / -32.079 / 477.494) | PASS |
| Quarterly segment Adjusted EBITDA sums to FY (all four columns, 3 years) | PASS |
| Q1-25..Q2-26 CFO, CFI, inventory vs prior research CSV | within 0.05 (rounding) |
| Debt by instrument sums to total debt at every quarter end | PASS (no mismatch printed) |
| Total debt 6/30/26 vs 10-Q: 3,496.380 before issuance costs; face 3,500; coupons imply 228.8/yr, equal to the 10-K's 12-month interest due | PASS |
| Balance sheet 12/31/25 and 6/30/26 vs release | PASS |

Failures: none in the filings-based data. One immaterial vintage difference: Q1-25 Aerospace revenue is 365.063 in the Q1-26 10-Q comparative versus 364.994 used in the prior research CSV (0.069 recast between filings; total unchanged).

## Gaps

1. Consensus: Yahoo Finance (load error), Zacks (bot wall) and Nasdaq (timeout) could not be read. No free page shows EBITDA consensus. FY2027 revenue/EPS consensus is behind stockanalysis Pro. The $238 PT from the screen was not reproduced anywhere.
2. Adjusted FCF: only the Q2-25 release reconciles it on EDGAR (423.5 = CFO -110.3 + CFI 523.8 + 10.0 QuickTurn). FY25 $724M, Q1-26 $158M, 1H26 $255M and the $878M/$915M guides come from calls (secondary transcripts). The 3 named investments (52 + 150 + 50 = 252) close only part of the FY25 gap: CFO+CFI is 412.6, so 724 less 412.6 less 252 leaves 59.4 unexplained (candidates: 10.0 QuickTurn and 49.1 acquisition of business; a hypothesis, not confirmed).
3. Gains embedded in Adjusted EBITDA are not disclosed by segment. Only company-level CFS gains exist (FY25 377.5 asset sales + 46.4 to Partnership + 54.3 insurance, about 40% of Adjusted EBITDA). The gain on sale to the Partnership is booked in Aviation Leasing.
4. Modules: Q2-25 (184) is from a release. Q4-25 (228) and Q2-26 (296) are call figures. Q1-25 (about 138) is back-solved from "+33%". Q3-25 and Q1-26 not found. Q4-23 and FY23 are modules SOLD (61 and 178), a different definition.
5. 2025 EBITDA guidance history (1,100-1,150 raised to 1,250-1,300) and the 2025 FCF raise (650 to 750) come from a search summary and the date is ambiguous. The $915M prior 2026 FCF guide date was not confirmed. 2027 modules 1,700 is from a truncated transcript read (first 100k of 111k characters).
6. Receivable from the Partnership at Q1-25 not disclosed in the release footnote. Q4 profit elimination (FY less 9M) was not parsed from the 10-K.
7. Preferred: book value is par only ($26K). 2.6M shares x $25 liquidation preference = $65M at 6/30/26 (6.8M shares, $170M, at 12/31/25). Redemption of 4.2M shares in 1H26 cost $105.5M.
8. Single-value rows in the cash flow parser were assigned to the current year. Return-of-capital figures are carried from prior research rather than re-parsed.

## Caveats and flags

- The pre-2025 segment tables show gains in expenses as negative numbers (Q4-24 -18.705 "Gain on sale of assets, net" expense line) and interest expense as a positive expense. 2025+ tables show interest as negative other expense. is_quarterly.csv normalizes interest expense to positive; other lines keep reported sign.
- 2023-24 "Aerospace Products" revenue was a single line (aerospace products revenue). MRE Contract revenue appears from Q1-25. The Aerospace segment therefore changed meaning when the 2025 Partnership started. MRE contract revenue is essentially all with the Partnership.
- Corporate and Other in 2023-24 contains offshore energy leasing revenue and the 2024 internalization fee (300.0 in Q2-24, producing the Q2-24 loss and EPS of -2.26).
- Q2-24 diluted shares equal basic (loss quarter).
- Consensus numbers are mutually inconsistent. Price targets: stockanalysis 364.10 (low 290, high 600, no per-analyst dates), MarketBeat 315.67 (225-375), unlabeled snippets 321.11 and 377. The 7 dated post-June targets itemized by MarketBeat average 330 (median 325). FY26 EPS consensus: 5.83 (stockanalysis, updated 9/29) vs 6.47 and 6.86 (older vintages).
- Stock fell about 19% after the Q2 print (barchart snippet); the +8.95% move on 10/6 left the price at 179.44 against a 52-week range of 149.50-323.51.
- stockanalysis lists forward P/E 20.2, but its own price and FY26 EPS give 30.8x.
