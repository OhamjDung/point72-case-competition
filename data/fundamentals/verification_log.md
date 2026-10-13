# Verification log: dks_quarters.csv

Run 2026-10-12 by P1 (Claude Code, on Tom's machine). Each source was re-opened from the local SEC download cache (files fetched from sec.gov on 2026-10-12 by the repo's `dks_model data-fetch` pipeline), turned into plain text, and checked automatically:

1. **Period end in release:** the `period_end` date, written out (e.g. "May 1, 2021"), appears in the release.
2. **Release date:** the `report_date`, written out, appears in the release dateline.
3. **Comp:** the `comp_pct` value appears beside "same store sales", "comparable (store) sales" or "comp" in the release. Negatives are written as "(8.4)%" or "declined 8.4%".
4. **FL comp:** the `comp_fl_pct` value matches the "Proforma Foot Locker (3) (4)" row for the 13-week column.
5. **Net sales and gross profit:** re-parsed from the release income statement (thousands); net_sales_musd matches within 0.05 and gross_margin_pct within 0.005.
6. **XBRL cross-check:** quarterly revenue and gross profit from the company's XBRL facts (10-Q, or 10-K for Q4) match the release within $1 thousand.

Result: **0 failures** across 22 reported quarters.

| Quarter | Period end in release | Release date | Comp | FL comp | Net sales | Gross profit | XBRL sales / GP (10-Q/10-K) |
|---|---|---|---|---|---|---|---|
| FY2021Q1 | ok | ok | ok (115.0) | n/a | ok (2,918,719k) | ok (1,088,627k) | ok (2,918,719 / 1,088,627) |
| FY2021Q2 | ok | ok | ok (19.2) | n/a | ok (3,274,842k) | ok (1,307,077k) | ok (3,274,842 / 1,307,077) |
| FY2021Q3 | ok | ok | ok (12.2) | n/a | ok (2,747,647k) | ok (1,056,576k) | ok (2,747,647 / 1,056,576) |
| FY2021Q4 | ok | ok | ok (5.9) | n/a | ok (3,352,160k) | ok (1,259,605k) | ok (3,352,160 / 1,259,606) |
| FY2022Q1 | ok | ok | ok (-8.4) | n/a | ok (2,700,205k) | ok (984,714k) | ok (2,700,205 / 984,714) |
| FY2022Q2 | ok | ok | ok (-5.1) | n/a | ok (3,112,419k) | ok (1,121,382k) | ok (3,112,419 / 1,121,382) |
| FY2022Q3 | ok | ok | ok (6.5) | n/a | ok (2,958,861k) | ok (1,012,423k) | ok (2,958,861 / 1,012,423) |
| FY2022Q4 | ok | ok | ok (5.3) | n/a | ok (3,596,713k) | ok (1,166,039k) | ok (3,596,713 / 1,166,039) |
| FY2023Q1 | ok | ok | ok (3.4) | n/a | ok (2,842,181k) | ok (1,028,617k) | ok (2,842,181 / 1,028,617) |
| FY2023Q2 | ok | ok | ok (1.8) | n/a | ok (3,223,643k) | ok (1,109,476k) | ok (3,223,643 / 1,109,476) |
| FY2023Q3 | ok | ok | ok (1.7) | n/a | ok (3,042,405k) | ok (1,061,463k) | ok (3,042,405 / 1,061,463) |
| FY2023Q4 | ok | ok | ok (2.8) | n/a | ok (3,876,171k) | ok (1,334,179k) | ok (3,876,171 / 1,334,179) |
| FY2024Q1 | ok | ok | ok (5.3) | n/a | ok (3,018,383k) | ok (1,095,293k) | ok (3,018,383 / 1,095,293) |
| FY2024Q2 | ok | ok | ok (4.5) | n/a | ok (3,473,635k) | ok (1,275,700k) | ok (3,473,635 / 1,275,700) |
| FY2024Q3 | ok | ok | ok (4.2) | n/a | ok (3,057,181k) | ok (1,093,444k) | ok (3,057,181 / 1,093,444) |
| FY2024Q4 | ok | ok | ok (6.4) | n/a | ok (3,893,649k) | ok (1,361,258k) | ok (3,893,649 / 1,361,258) |
| FY2025Q1 | ok | ok | ok (4.5) | n/a | ok (3,174,677k) | ok (1,165,086k) | ok (3,174,677 / 1,165,086) |
| FY2025Q2 | ok | ok | ok (5.0) | n/a | ok (3,646,616k) | ok (1,351,272k) | ok (3,646,616 / 1,351,272) |
| FY2025Q3 | ok | ok | ok (5.7) | ok | ok (4,167,773k) | ok (1,380,860k) | ok (4,167,773 / 1,380,860) |
| FY2025Q4 | ok | ok | ok (3.1) | ok | ok (6,226,054k) | ok (1,770,044k) | ok (6,226,054 / 1,770,045) |
| FY2026Q1 | ok | ok | ok (6.0) | ok | ok (5,164,504k) | ok (1,683,262k) | ok (5,164,504 / 1,683,262) |
| FY2026Q2 | ok | ok | ok (4.9) | ok | ok (5,586,815k) | ok (1,943,271k) | ok (5,586,815 / 1,943,271) |
| FY2026Q3 | in progress | n/a | n/a | n/a | n/a | n/a | n/a |

## Differences found (none change a number in the file)

- FY2021Q4 and FY2025Q4 gross profit: XBRL is $1 thousand higher than the release (1,259,606 vs 1,259,605; 1,770,045 vs 1,770,044). The Q4 XBRL value comes from the 10-K and is rounding. The release value is used.
- Restatements and definition changes (FY2022 comp method change, FY2021 restated comps, FY2024Q3/Q4 revised to 4.3%/6.6%): see NOTES.md, "Reporting changes". The file keeps first-reported values.
- Foot Locker close date 2025-09-08: verified in DKS's 8-K Exhibit 99.1 of that date (accession 0001140361-25-034244). The 2025-08-26 8-K had said the deal was "expected to close on September 8, 2025".
- FY2026Q3 period_end (2026-10-31) is computed and report_date is empty. See NOTES.md.

## Manual spot checks (read by eye in the release text)

- FY2022Q1: "Comparable store sales declined 8.4%"; table "Net sales $ 2,700.2 ... Comparable store sales (1) (8.4)%".
- FY2023Q4: "Comparable store sales (13-week basis) 2.8%"; 14 Weeks Ended February 3, 2024.
- FY2025Q3: "Non-GAAP DICK'S Business (2) Comparable sales (3) 5.7% 4.3%"; "Proforma Foot Locker (3) (4) (4.7)%"; "Consolidated GAAP Net sales $ 4,168".
- FY2026Q2: "Delivers 4.9% Comp Sales Growth for the DICK'S Business"; "Proforma comps for the Foot Locker Business (C) declined 3.6%".
