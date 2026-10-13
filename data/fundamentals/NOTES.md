# NOTES: data/fundamentals/dks_quarters.csv

Owner: P1. Schema: CONTRACT.md file 3. Every number comes from a DKS quarterly earnings release (8-K Exhibit 99.1 on SEC EDGAR, URL in `source_url`). Net sales and gross profit were also cross-checked against the XBRL values in the matching 10-Q/10-K (see `verification_log.md`).

## Columns

- **period_start, period_end:** from the filings. Q1 to Q3 use the XBRL duration of quarterly net sales in each 10-Q. Q4 starts the day after the Q3 end and ends on the fiscal year end in the 10-K. Every period end also appears in its release ("13 Weeks Ended ..."). FY2023Q4 has 14 weeks (2023-10-29 to 2024-02-03); all other quarters have 13.
- **report_date:** the dateline of the earnings release ("PITTSBURGH, November 25, 2025 - ...").
- **comp_pct:** comparable sales change **as first reported in that quarter's own release**: the number the market saw on report day. Later restatements are listed below and are not applied.
- **comp_fl_pct:** "Proforma Foot Locker" comparable sales from DKS's post-acquisition releases (FY2025Q3 onward). DKS calculates it as if it had owned Foot Locker for the whole period, in constant currency. Empty before the acquisition.
- **net_sales_musd:** consolidated GAAP net sales from the release's income statement, in thousands, divided by 1,000.
- **gross_margin_pct:** consolidated gross profit / consolidated net sales x 100, both from the release's income statement (thousands of dollars), rounded to 2 decimals. Up to FY2024Q4 this equals the "% of Sales" printed beside GROSS PROFIT. From FY2025Q3 it uses "Total gross profit", which includes Foot Locker and the corporate inventory write-downs tied to the acquisition (for example, FY2025Q4 total gross profit is after a $217.9m corporate charge). The low FY2025Q4 margin (28.43%) is mostly that charge plus Foot Locker's lower margin. It is not a like-for-like fall in the DICK'S Business margin.

## Reporting changes

1. **Foot Locker acquisition closed on 2025-09-08**, inside FY2025Q3 (DKS 8-K, Exhibit 99.1, "DICK'S Sporting Goods Completes Acquisition of Foot Locker", accession 0001140361-25-034244, https://www.sec.gov/Archives/edgar/data/1089063/000114036125034244/ef20055283_ex99-1.htm). From FY2025Q3, DKS reports two businesses. `comp_pct` = "DICK'S Business" comparable sales (the "DICK'S Sporting Goods" line of the proforma comparable sales table, also called "Non-GAAP DICK'S Business comparable sales"). Before the acquisition, `comp_pct` = the company's headline comp, which was the same business. Consolidated net sales and gross margin include Foot Locker from 2025-09-08 on, so FY2025Q3 onward is not comparable with earlier quarters for those two columns.
2. **Comp definition changed in FY2022.** "Beginning in fiscal 2022, the Company revised its method for determining its comparable store sales calculations to include relocated store locations" (FY2022Q1 release, footnote 1; details in Exhibit 99.2 of that 8-K). The FY2022 releases restate the FY2021 prior-year comps: Q1 117.1% (first reported 115%), Q2 20.2% (19.2%), Q3 12.8% (12.2%), Q4 6.6% (5.9%). `comp_pct` keeps the first-reported FY2021 values. FY2021 comps lap the 2020 COVID closures (Q1 = +115%), so they are outliers either way.
3. **Name change.** Up to FY2021 DKS said "same store sales"; FY2022 to FY2023 "comparable store sales"; from FY2024 "comparable sales". Same concept.
4. **FY2023Q4 comp is on a 13-week basis** (2.8%), though the quarter had 14 weeks.
5. **Small later revisions in post-acquisition releases:** the prior-year columns show FY2024Q3 as 4.3% (first reported 4.2%) and FY2024Q4 as 6.6% (first reported 6.4%). The releases do not explain why. Not applied.
6. **Prior-year proforma Foot Locker comps** appear in the post-acquisition releases (FY2024Q3 +2.3%, FY2024Q4 +2.3%, FY2025Q1 -2.9%, FY2025Q2 -2.2%). They were not left in `comp_fl_pct`, because DKS did not own or report Foot Locker in those quarters. They are recorded here only.

## FY2026Q3 (in progress)

- `period_start` 2026-08-02 = the day after the FY2026Q2 end in the FY2026Q2 10-Q (accession 0001089063-26-000036; `source_url` points to that filing's index).
- `period_end` 2026-10-31 is **computed, not taken from a filing** (the only exception to the filings-only rule): 13 weeks from 2026-08-02. No filing has stated it yet. It matches the 13-week Q3 pattern of every year above and the Saturday calendar.
- `report_date` is empty: no date announced in any filing as of 2026-10-12. Past Q3 reports came out 23 to 25 days after quarter end (2021-11-23, 2022-11-22, 2023-11-21, 2024-11-26, 2025-11-25), so the expected date is around **2026-11-24**. That is inferred, not announced.
- Guidance known before the print (management guidance, not consensus): the FY2026Q2 release (2026-08-25) kept the full-year DICK'S Business comp outlook at +2.5% to +4.0% and lowered the Foot Locker Business proforma comp outlook to -2.0% to 0.0%.
