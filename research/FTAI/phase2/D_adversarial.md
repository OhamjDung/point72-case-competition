# FTAI Aviation (FTAI): Adversarial Review of the "Engine-Trading Business" Insight

Prepared 2026-10-06 for the Point72 Academy pitch (due 2026-10-12). Public sources only; SEC requests used the header "UniResearch research@example.edu". Price context: $179.44 on 2026-10-06 (stockanalysis.com, per stress_test.md) against a 52-week high of $323.51 on 2026-02-26 (Weiss Ratings alert, 2026-08-20). Items marked [UNVERIFIED] could not be tied to a primary source. Companion file: `short_report_claims.csv`.

Insight under test: the market prices FTAI as a premium aftermarket franchise, but the filings show an engine-trading business (gains about 40% of Adjusted EBITDA; about 25% of Aerospace revenue sold to the 19%-owned SCI partnership; negative GAAP CFO with inventory up 2.8x; Adjusted FCF adding back growth purchases; Aerospace margin 35.9% to 28.5%).

---

## 1. Investigation Trail

Narrative log of doors opened, in order. "L1/L2/L3" mark how deep each chain went.

**Thread 1: the January 2025 short reports**

- L1. Went for the primary Muddy Waters (MW) report. The site did not resolve through the fetch tool, so a search surfaced the PDF address and I downloaded it directly (https://muddywatersresearch.com/wp-content/uploads/2025/01/MW_01152025.pdf, dated 2025-01-15, 59 slides, "Financial Engineering and Accounting Manipulation in the MRO Business"). This corrects trail.md, which relied on secondary summaries and said the primary was not retrievable. MW's second report on Iran (2025-03-03) is at https://muddywatersresearch.com/research/2025/ftai-violating-us-sanctions/ (found, not read in full; claim taken from its headline and TipRanks/Stocktwits summaries).
- L2. Read the MW slides for the exact claims and numbers. Key finding: MW's "80%" is a ratio of total cash-flow-statement gains on sale, less leasing-segment gains, to Aerospace Products adjusted EBITDA for Q1-Q3 2024 (73%, 82%, 83%; slide 6). It is a 2024 pre-SCI number. Compared against our later ratios (99% FY24 upper bound, 56% FY25, 38% 1H26) the claim was roughly right for 2024 and has since faded as module volume grew.
- L2. Checked whether MW had already seen our cash-flow point. It had: slide 22 is titled "New Cash Flow Statement Disclosure Supports our View of the Materiality of Whole Engine Sales". So the classification of whole-engine sale proceeds in investing is not new. What is new is the link to Adjusted FCF (Thread 1, section 6).
- L3. Followed MW's "channel stuffing" door (Dec 2023 sale of two A320s to Aerolease, resold to Setna iO in June 2024). Searched FY25 10-K and Q2-26 10-Q for follow-up: nothing. Dead end: no later filing, comment letter or auditor matter touches it.
- L3. Followed the company's rebuttal. The only formal rebuttal is an Audit Committee review by "independent legal and forensic accounting advisors" concluding the allegations "are without merit" (8-K Item 8.01, 2025-02-20, https://www.sec.gov/Archives/edgar/data/1590364/000114036125005179/ef20043996_8k.htm). It does not rebut any claim line by line. FY24 10-K was filed on time (2025-03-03).
- L1. Snowcap (2025-01-29): primary report not found. Used AccessNewswire/TipRanks summaries (claims: up to 50% of Aerospace profit is repackaged COVID leasing gains; inventory "egregiously overvalued"; EBITDA "at best meaningless"; former executive says third-party module swaps are "not really" happening; 87x book). Treat wording as indicative.
- L2. Followed the class-action branch. Shannahan v. FTAI Aviation Ltd., No. 25-cv-00541 (S.D.N.Y.): defendants moved to dismiss the amended complaint on 2025-11-20; fully briefed; undecided (law-firm releases, accessnewswire/ktmc.com; I could not check the docket). Note the FY25 10-K Item 3 gives only boilerplate and does not name the case (checked by text search of the 10-K).
- L2. Followed SEC comments. EDGAR lists CORRESP/UPLOAD letters from Nov 2024 to Jan 2025 on the FY23 10-K (e.g. https://www.sec.gov/Archives/edgar/data/1590364/000114036125001365/filename1.htm, 2025-01-17). The content is balance-sheet presentation only (separate accounts payable, disclose total current assets and liabilities, Reg S-X 5-02 components). Nothing on non-GAAP, inventory or revenue. Dead end as a red flag. It is a mild positive that the SEC staff reviewed the 10-K and raised only presentation points, though that is not a clearance.

**Thread 2: SCI structure**

- L1. 10-K FY25 (https://www.sec.gov/Archives/edgar/data/1590364/000162828026012940/ftai-20251231.htm) and 10-Q Q2-26 (.../000162828026051412/ftai-20260630.htm), pulled directly, searched for the SCI terms. Found: equity method, 19% LP interest, FTAI is "Servicer" (GP), "customary, market-based compensation", exclusive MRE supply "for the life of the partnership", profit participation to FTAI's servicer subsidiary.
- L2. Fees and promote: no percentages anywhere in the 10-K, 10-Q or the 8-Ks I read. Went to the numbers instead. Servicing fees were $7M in Q2-26 and co-investment returns $28M (Q2-26 slides, https://www.investing.com/news/company-news/ftai-aviation-q2-2026-slides-power-contract-production-surge-amid-earnings-miss-93CH-4824813). Annualised servicing fee $28M on about $5.9B of capital closed or under LOI (Q1-26 supplement) is roughly 0.5%, an estimate of mine.
- L3. Pricing test via the profit elimination. FTAI eliminates its 19% share of profit on engines and modules sold to the partnership: $22.8M FY25 (trail.md), $16.6M 1H26 (10-Q). If elimination = 19% of profit, implied profit on MRE contract revenue is about $120M on $335.8M in FY25 (36%) and $87M on $404.0M in 1H26 (22%): Q1-26 24%, Q2-26 19%. This is a derived estimate, not a disclosed margin [UNVERIFIED mechanics]. This is intra-entity gross profit, not EBITDA, so it is not comparable with the 28.5% segment margin, and the elimination may be net of releases. At face value it says related-party modules are not obviously priced above third-party work, but it is equally consistent with value moving into a vehicle where FTAI (and its employees through the profit-participation plan) earn the promote. Inconclusive on arm's length.
- L3. Retained risk. The 10-K reports ASC 460 guarantees on certain aircraft sales on lease at fair value $12.0M (12/31/25) and $8.9M (12/31/24) in other non-current liabilities, with changes recorded in Asset sales revenue; the disclosure does not say these relate to SCI [UNVERIFIED link]. Searches for "first loss", "residual value guarantee" and "variable interest" found nothing relating to SCI. Maximum-exposure language is absent. Dead end on a first-loss piece; exposure is the carrying value ($365.5M), unfunded commitments, and the exclusivity obligation.
- L2. SCI II. Q4-25 call (https://www.fool.com/earnings/call-transcripts/2026/02/26/ftai-ftai-q4-2025-earnings-call-transcript/, 2026-02-26): "anchor equity commitment" received, matches SCI I's $6B target. Q2-26 call (Investing.com, 2026-07-30): 2026 SPV launched, $6B target, FTAI 15% commitment, capital-call facility "will bridge a substantial portion" of FTAI's funding into 2027. Searches for a first-close announcement or named investors found nothing public. Note a search snippet that gave "$2.0B equity commitments including $380M from the FTAI balance sheet" describes SCI I (19% of $2.0B = $380M), not SCI II.
- L3. Third-party investors. Public news names One Investment Management as partner in the "inaugural" vehicle (TipRanks/The Fly, 2025-03-25). Debt: $2.5B asset-level financing from ATLAS SP Partners (Apollo-majority structured products business) and Deutsche Bank (AviTrader/SFNet, 2025-02-27; Clifford Chance, 2025-05), upsized to a $3.5B warehouse (Q1-26 supplement). The first ABS, FTAI MRE 2026-1: $612M notes on 48 aircraft with appraised value about $825.6M (about 74% advance), rated by Fitch/KBRA, closing 2026-06-04, with "affiliates of FTAI" retaining the equity (KBRA release, https://www.kbra.com/publications/CMcsLXPK). Other LPs are not named in public sources.
- L3. Employee carry. 8-K 2026-01-22 adopts a Strategic Capital Profit Participation Plan (cited in trail.md; https://www.sec.gov/Archives/edgar/data/1590364/000114036126002691/ef20064098_8k.htm), so part of the promote leaks to employees; rate and hurdle undisclosed.

**Thread 3: bull case.** Benchmarked gains against a pure lessor, tested inventory against orders, and tested seasonality (details in section 4).

**Thread 4: ownership.** Parsed every Form 4 filed in 2026 from EDGAR XML (script in scratchpad). Pulled MarketBeat short-interest history. Reconciled the late-September drop (section 5). Dead end: 13F quarter-over-quarter change by holder (aggregator pages rate-limited or gave price changes, not share changes).

**Thread 5: auditor/controls.** KPMG since 2025 (10-K audit report), EY since 2016, replaced after a "comprehensive, competitive auditor selection process" (8-K Item 4.01, 2025-06-24, https://www.sec.gov/Archives/edgar/data/1590364/000114036125023499/ef20050905_8k.htm). This is a competitive rotation, not a dismissal for cause. Clean ICFR opinion for FY25; Item 9 "None".

---

## 2. Short-Report Claim Table

Full table with evidence and sources in `short_report_claims.csv`. Condensed:

| # | Claim (source) | Company rebuttal | Status | Overlap with us |
|---|---|---|---|---|
| MW1 | ~80% of Aerospace Products adj. EBITDA is gain on sale (MW, 2025-01-15, slide 6) | Audit Committee: "without merit" (8-K 2025-02-20) | Right for 2024; now an upper bound of 56% (FY25) and 38% (1H26); segment attribution undisclosed | High on theme, but our number is 40% of company EBITDA |
| MW2 | Whole engines counted as 3 modules; 70-80% of "module sales" | "Three modules is one engine" (CEO, Citi) | Unresolved; revenue per module $2.96M Q2-26 is far above MW's $0.7-1.5M off-the-rack price | Medium |
| MW3 | Over-depreciation in Leasing flatters Aerospace margin (~36% vs peers ~20%) | Policy unchanged since 2015; MS "not egregious" | Partly supported: margin now 28.5%, guided ~30% | Low-medium |
| MW4 | Dec 2023 A320 sales to Aerolease booked via note (channel stuffing) | None specific | Unresolved; no later disclosure | None |
| MW5 | Core module margin falling about 600bp ex-USM | Not addressed | Proven in direction (35.9% to 28.5%) | High |
| MW6 | Aerospace is capital intensive; reliant on third-party engine purchases | Not addressed | Proven: engine/aircraft inventory purchases $325M FY25 and $357M 1H26 | High |
| MW7 | New cash-flow disclosure shows whole-engine sales (slide 22) | Not addressed | Proven (presentation) | High, a rehash of the classification point |
| MW8 | Fortress selling in May 2024 | None | Untested | None |
| MW9 | Sorena/Iran (2025-03-03) | None found | Unresolved; no OFAC/BIS action found | None |
| SC1 | Up to 50% of Aerospace profit is repackaged leasing gains (Snowcap, 2025-01-29) | Audit Committee | Unresolved, eroding | Medium |
| SC2 | Inventory "egregiously overvalued" | Audit Committee | Unresolved; 2.8x growth, no write-down, no KPMG inventory CAM; composition undisclosed | High |
| SC3 | EBITDA "meaningless", cash flow far lower | Audit Committee | Partly supported: CFO+CFI 35-41% of EBITDA | High |
| SC4 | Third-party module swaps "not really" happening | Not addressed | Weakly disproven by +77% products revenue | Low |

**What is new in our insight (precise).**

1. SCI circularity. Both reports predate the revenue; MRE contract revenue to the partnership was $335.8M in FY25 and $404.0M in 1H26 (25% of Aerospace revenue), with $530M and $176M of seed-aircraft sales and gains ($46.4M, $17.6M) on top. Nobody could have said it in January 2025. Caveat from Thread 2: the implied margin on those sales is not above the segment.
2. Adjusted FCF as a metric: FY25 headline $724M vs CFO+CFI $413M (gap $311M unreconciled), and the company stopped giving a reconciliation in 8-Ks after the Q2-25 release (trail.md). Snowcap said cash flow was weak; neither said management's own FCF number is unreconcilable.
3. The 2H26 ramp (about $623M = $878M guide less $255M in 1H) must be built with the SCI I seed-aircraft pipeline exhausted: Note 10 of the Q2-26 10-Q says "As of June 30, 2026, the Company sold all committed aircraft to the 2025 Partnership". Seed-aircraft proceeds were $175.7M of 1H26 CFO+CFI of $250.4M, so ex-seed 1H26 was only about $75M. The raw 2H25 vs 1H25 comparison ($53M vs $360M) is mostly seed timing ($397.1M of seed proceeds in 1H25, about $133M in 2H25); ex-seed, 1H25 was about -$37M and 2H25 about -$80M, so there is no usable seasonality evidence either way.
4. Inventory growth is mostly purchased engines (79% of the 1H26 CFO inventory outflow) and Power feedstock, a business that did not exist when MW wrote.
5. Composition of gains: 40% is not only engine trading; it includes $46.4M SCI seed gain (FY25) and $54.3M (FY25) and $49.5M (1H26) of Russia insurance recoveries, which are non-recurring. This is a more careful number than MW's 80%.

**What is NOT new.** "Engine trading dressed as MRO", falling margins, gains-heavy EBITDA, and weak cash conversion are all MW and Snowcap themes. If the pitch leads with those it is a rehash, and judges will know the January 2025 reports. MW's 80% was also partly wrong going forward, so we should not lean on their credibility.

---

## 3. SCI Terms

| Item | Finding | Source |
|---|---|---|
| FTAI ownership | 19% LP interest in the 2025 Partnership (SCI I); equity method; carrying value $365.5M at 6/30/26; invested $291.5M by 12/31/25 plus $95.1M 1H26; distributions received $19.2M in 1H26 | 10-Q Q2-26 Note 4 |
| Equity raised | $2.0B equity commitments, fundraise completed Oct 2025; 19% implies about $380M FTAI commitment (cumulative $386.6M funded per trail.md) | 10-K FY25; Q4-25 call |
| Management/servicing fee | Percentage not disclosed ("customary, market-based"). Servicing fees $7M in Q2-26; $12.8M 1H26 (trail.md). About 0.5% of capital, my estimate | 10-K; Q2-26 slides |
| Promote/carry | "Profit participation" distributions paid to FTAI's servicer subsidiary; rate and hurdle undisclosed; employees share via the Strategic Capital Profit Participation Plan (8-K 2026-01-22) | 10-K FY25; 8-K |
| Module supply exclusivity | MRE business "exclusively provides replacement aircraft engines and modules for the life of the partnership"; 2026 SPV also requires engine exclusivity with FTAI | 10-K; Q1-26 / One IM release 2025-03-25 |
| Arm's length? | Company says "contractual and customary market-based". Implied gross profit on MRE contract revenue about 36% FY25, about 21% 1H26 (derived from the 19% elimination; not comparable with segment EBITDA margin; inconclusive). Management says SCI builds mirror third-party scope, with low-cycle builds earning more and heavier builds "below" 40% (Q2-26 call). Direct margin by customer not disclosed | 10-Q; call |
| Accounting | Equity method; seed aircraft sold under ASC 610-20 (non-ordinary), gain recognised ($17.6M 1H26; $46.4M FY25); MRE sales recognised as ASC 606 revenue at a point in time, with only the 19% share of profit eliminated and released as the partnership earns | 10-Q Notes 2, 4, 10 |
| Gain on sales into a partly owned vehicle | Yes: gain recognised in full on the seed assets (no 19% elimination on the aircraft gain disclosed; the elimination described applies to MRE sales). Cash lands in investing | 10-Q |
| Retained risk | Equity exposure $365.5M; unfunded commitments (15% of a $6B SPV target for SCI II, bridged by a capital-call facility into 2027); ASC 460 sale guarantees $12.0M (not shown to be SCI); exclusivity performance obligation; servicer role. No first-loss tranche or debt guarantee found in public text | 10-K; Q2-26 call |
| Debt | $2.5B ATLAS (Apollo) and Deutsche Bank commitment, upsized to $3.5B warehouse; ABS MRE 2026-1 $612M on about $825.6M assets, FTAI affiliates retain the equity | AviTrader 2025-02-27; Q1-26 supplement; KBRA |
| Third-party investors | One Investment Management named (2025-03-25); other LPs not public | TipRanks/The Fly |
| SCI II | Launched, $6B target (incl. leverage), anchor equity commitment unnamed, FTAI 15%, no first-close announcement found by 2026-10-06 | Q4-25 and Q2-26 calls |

The 25% related-party share is an observation, not an accusation: the filings disclose it and the auditor did not flag it. Whether pricing is arm's length cannot be resolved from public data.

---

## 4. Strongest Bull Case, Quantified

**(a) Gains as a recurring business.** The right comparator is a lessor. Willis Lease booked gains on sale of $54.0M in 2025 against Adjusted EBITDA of $459.1M, about 12% (Q4-25 release, https://www.sec.gov/Archives/edgar/data/1018164/000101816426000030/q42025ex991.htm). FTAI at 40% is more than 3x that. Only the portion excluding insurance and SCI seed gains (32% in 1H26 per stress_test.md) is plausibly recurring, and it is shrinking as a share (44% FY24 to 32%). The bull framing: FTAI has migrated from leasing-asset sales toward product sales, and its remaining sale gains come from converting a large, maturing leasing book into SCI fees. That story ends when the book is gone: leasing equipment fell $399M in six months.

**(b) Inventory against booked demand.** Evidence for: $1.465B Power PO (2026-07-22) with an advance payment and milestones, delivery through Nov 2027; 2026 module guide raised to 1,200 (from 1,050), 2027 target 1,700; GE says used serviceable material is scarce (GE Bernstein deck, 2026-05-27, via trail.md). Against: Power inventory is not disclosed. If Power inventory were $300-400M [UNVERIFIED illustration, from $150M in Q4-25 plus 2026 working capital], the PO would cover it 3.7-4.9x, but the PO sits in the J&F JV and FTAI's share is unknown. Module inventory against module backlog is undisclosed. Days inventory 221 vs 186.

**(c) FCF inflection in 2H26.** Need about $623M against $255M in 1H26. Prior-year seasonality is not usable: the raw 2H25 ($53M) vs 1H25 ($360M) split is a seed-timing artefact (ex-seed about -$80M vs -$37M). More important, the SCI I seed pipeline is exhausted (Note 10: all committed aircraft sold by 6/30/26), so 2H26 has no seed proceeds. Ex-seed 1H26 CFO+CFI was about $75M ($250.4M less $175.7M); Q2-26 held about $70M of seed (6 of 15 aircraft in 1H26, my estimate), so the ex-seed Q2 run-rate is about $20-25M, not $94M. Items, illustrative only, tagged R (recurring) or O (one-off): (i) ex-seed run-rate of about $25M a quarter, $50M for 2H (R), leaving about $573M to find; (ii) a Power advance at signing; if it is 10-20% of $1.465B that is $147-293M [UNVERIFIED, size undisclosed] (O, then milestones); (iii) no further SCI equity call after the final $95M in 1H26, because the 2026 SPV capital-call facility defers funding to 2027 (McAleese, Q2-26 call), worth up to about $95M versus 1H (R through 2026, then reverses in 2027); (iv) the July special distribution from the first ABS (size undisclosed, O). With midpoint Power advance ($220M) plus no SCI call ($95M) plus ex-seed run-rate ($50M) the sum is about $365M, so roughly $250M short of the guide before the ABS distribution and any asset sales. The guide was already cut from $915M to $878M. The gap closes only if the Power advance is at the top of the range and the ABS distribution and inventory sell-through are large. This is a one-quarter test, Q3-26 on 2026-10-28 (EarningsWhispers via stress_test.md), and on this arithmetic it points against the guide.

**(d) Valuation cushion.** 9.4x 2027 guided EBITDA ($2.3B; stress_test.md); the stock is down 44% from the $323.51 February high; short interest is only about 6%; consensus target about $368 (10 analysts). The stress_test.md break-even on Power probability for a short is about 8%.

---

## 5. Ownership, Flows and Controls

**Insiders (Form 4, EDGAR, all 2026 filings parsed).**
- Buying: President David Moreno bought 2,475 shares at $201.27 (open-market code P, trade 2026-07-31, filed 2026-08-03), about $0.5M, the day after the Q2 call. Small but the only open-market buy in 2026.
- Selling: director Martin Tuchman sold 254,260 shares across 2026-05-01 and 2026-05-04 at about $241-242, roughly $61.5M (Forms 4 filed 2026-05-05). Director Paul Goodwin sold 10,000 shares at $303.35 (2026-02-27, about $3.0M); director Judith Hannaway sold 255 shares at $253.89 (2026-05-27). Executive transactions otherwise are tax-withholding (code F) and awards (code A); CEO Adams exercised 12,448 options at $25.44 on 2026-05-11 and had shares withheld for tax. No executive open-market sales found.
- Reading: a $61M director sale near $242 is a flag, though price was well above today's; the buy at $201 is a mild positive. CFO Eun Nam resigned 2026-03-03 (8-K 2026-03-06, per trail.md), five days after the 10-K; the new CFO is Nicholas McAleese.

**13F.** Largest holders as of the latest quarter aggregated by InsiderSet (https://www.insiderset.com/stocks/FTAI/institutional-ownership): Capital International Investors 12.4M shares, Capital World Investors 11.4M, BlackRock 8.6M, Vanguard Capital Management 4.6M, Vanguard Portfolio Management 4.1M, FMR 3.6M, DZ Bank 3.1M, State Street 3.1M, Rubric Capital 3.0M, Westfield 2.9M. Changes: BlackRock +31.5% in Q1-26 (HoldingsIntel via search); Vanguard -1.99% in Q4-25; across funds 36 added and 19 trimmed in the latest quarter (search summary). I could not retrieve a clean two-quarter change per holder (dead end; the "-38%" shown on aggregator pages is the price change since filing, not a position change). Concentration risk: Capital Group entities together hold about 26.7M shares, about 26% of 102.7M shares. [Aggregator figures, UNVERIFIED against primary 13F-HR.]

**Short interest, reconciled.** MarketBeat (https://www.marketbeat.com/stocks/NASDAQ/FTAI/short-interest): 6.02M shares, 5.94% of float, 4.4 days to cover on 2026-09-15, down 10% from 2026-08-31 (6.71M, 6.6%); 6.1% on 2026-06-30. A search summary quoted 10.4% of float for mid-September; I could not trace it to a primary page [UNVERIFIED], and it conflicts with MarketBeat's series. The 4-10% range is explained by different dates and float definitions; the best-supported figure is about 6%. FINRA/exchange primary files were not pulled. Low short interest means no squeeze risk but also that the market has not taken the short side in size.

**Late-September decline.** Price evidence: -6.2% on 2026-09-24 to $174.53 and -4.5% on 2026-09-28 to $167.10 (GuruFocus, per stress_test.md). The AI-infrastructure sell-off commonly cited for FTAI traces to a WSJ analysis of about $3 trillion of tech off-balance-sheet commitments; Weiss Ratings dates that drop to 2026-08-20 (-5.96% to $198.34, with GE Vernova, Vertiv and Caterpillar also lower). So the August catalyst is documented, but the late-September leg has no company-specific cause that I could find [UNVERIFIED]; it looks like sector beta to AI-power names. The fall has been about 45% from the February high. Note the Aug 20 note also records the Q2 EPS miss ($1.13 vs $1.32) and the Aviation Leasing guide cut from $575M to $475M EBITDA.

**Auditor and controls.** KPMG (first year FY25, clean opinion and clean ICFR opinion; sole CAM is lease maintenance revenue, not inventory); previous auditor EY (2016-2024), replaced by a competitive process (8-K 2025-06-24). No material weakness, no restatement. SEC comment letters (Nov 2024 to Jan 2025) were presentation-only. Class action pending (S.D.N.Y. 25-cv-00541, MTD fully briefed). Flags: first-year auditor, CFO turnover, and a 10-K that does not name the class action.

---

## 6. Verdict

**Does the insight survive?** Partly, and in a narrower form. As a description it is accurate: gains and insurance are about 40% of Adjusted EBITDA, and the Aerospace margin has dropped 7.4 points. But three things weaken it as a trade:

1. Most of the "engine trading" framing is MW and Snowcap's theme, so it is not differentiated, and MW's 80% number has faded.
2. The SCI circularity is real but the pricing question is inconclusive: the implied gross profit on related-party modules (about 21% in 1H26) is not evidently inflated, though promote economics sit with FTAI, and no first-loss piece or guarantee turned up in public text. We cannot argue mispricing from public data.
3. The stock has already de-rated: -44% from peak, 9.4x 2027 EBITDA, ~6% short interest.

**The 1-2 things that would change it.**
1. Q3-26 results and 10-Q (2026-10-28): 2H26 FCF tracking toward $878M, together with whether Adjusted FCF is reconciled and the FY25 $724M gap is explained. This decides the cash-conversion pillar.
2. How the J&F Power JV is accounted for and the size of the advance payment (customer deposits and the equity-method note): this decides both the 2H26 FCF and whether the Power EBITDA is 100% or FTAI's share.

SCI II first close (or its absence) is the third watch item: a closed raise with named third-party LPs and a disclosed fee schedule would remove the related-party objection.

**Differentiated angle.** Do not pitch "FTAI is an engine trader"; pitch "FTAI's headline cash metric and 2H guide are untested, and the quality of earnings turns on one 10-Q." If forced to call a direction, the evidence in this file points Long, small conviction, because the valuation already discounts most of the adversarial points. Direction of the catalysts: the Q3-26 FCF test points against the guide (seed pipeline exhausted, ex-seed 1H26 only about $75M), which is the bear's best card; the Power advance and J&F accounting point up; SCI II close points up. The Long lean therefore rests on valuation and Power, not on cash flow.

**Lean: Long, conviction 2 of 5.** Consistent with stress_test.md (short P(right) about 30%).

**Best open doors:** (0) does SCI II carry a seed-asset purchase from FTAI's leasing book (would refill 2H seed proceeds)? (1) Q3-26 10-Q on 2026-10-28 (customer deposits, J&F note, Adjusted FCF); (2) Jereh Shenzhen filing (002353) for the J&F split and unit count; (3) SCI II first-close announcement and LPA terms via the MRE 2026-1 pre-sale report (fee and promote percentages); (4) CourtListener docket for 25-cv-00541 (motion-to-dismiss ruling); (5) FINRA short-interest file and 13F-HR primaries (Capital Group, BlackRock, Rubric) for two-quarter changes; (6) IR deck footnote reconciling the FY25 $724M Adjusted FCF.
