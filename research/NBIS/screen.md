# NBIS (Nebius Group N.V.) Screen

Prepared 2026-10-06 for the Point72 Academy stock pitch screen. All facts are public. Items I could not confirm in a primary source are marked [UNVERIFIED]. Companion CSVs sit in this folder: dilution_as_converted, guidance_bridge, unit_economics_per_MW, cash_flow_quality, contracts_and_backlog, rpo_conversion, site_tracker, insider_form4_summary_aug_oct2026, external_datasets.

Filing regime, verified: Nebius is a foreign private issuer. It files an annual report on Form 20-F (FY2025 20-F filed 2026-04-30) and quarterly results on Form 6-K, not 10-K/10-Q. CIK 0001513845 (formerly Yandex N.V.). Source: https://data.sec.gov/submissions/CIK0001513845.json, pulled 2026-10-06. 20-F: https://www.sec.gov/Archives/edgar/data/1513845/000110465926052948/nbis-20251231x20f.htm

## 1. Snapshot (as of 2026-10-06 unless stated)

Price and valuation. The stock closed near $249.87 on 2026-10-06 (stockanalysis.com; another feed reported $251.99). Market cap is about $68.5B on the 274.1M share count shown by stockanalysis, but about $77B if the NVIDIA warrant and the August exchange shares are counted (see below). 52-week range is $73.52 to $299.86. The stock traded at $116.33 on 2026-03-17, when the March converts were priced, so it has roughly doubled in under seven months. Source: https://stockanalysis.com/stocks/nbis/ and the 6-K at https://www.sec.gov/Archives/edgar/data/1513845/000110465926029863/tm268409d3_ex99-1.htm

Balance sheet, 30 June 2026 (Q2 6-K financials, https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d2.htm):
- Cash and equivalents $8,042M, plus $1,056M restricted.
- Debt $8,546M carrying value, all convertible notes (principal outstanding $10,042M measured at accreted maturity value). Original principal about $8.7B.
- Operating lease liabilities $1,510M. A further $12,054M of undiscounted lease payments are signed but not yet commenced (terms up to 12 years); $612M has already been prepaid.
- Deferred revenue $5,975M ($979M current, $4,996M non-current). This is customer prepayment cash and is a liability.
- Property and equipment, net $13,045M. Non-marketable equity investments $1,607M (mainly ClickHouse, marked on its Jan 2026 round at about $15B). Equity $10.34B.

Subsequent events that matter for EV:
- 2026-07-17: $775M first secured facility, SOFR+250bp, matures 2030-10-31, backed by deployed GPUs and an investment-grade customer contract (https://www.sec.gov/Archives/edgar/data/1513845/000110465926084452/tm2620683d1_ex99-1.htm).
- 2026-08-19/24: $5.75B of new converts. $3.45B at 0.50% due 2030 (conversion $313.46, accretes to 110%) and $2.3B at 4.50% due 2034 (conversion $324.65, accretes to 125%). Net proceeds about $5.68B. Concurrently about $800M of the 2029 and 2031 converts (conversion $51.45) were exchanged for about 15.8M Class A shares. Sources: https://www.sec.gov/Archives/edgar/data/1513845/000110465926098924/tm2623617d1_ex99-1.htm and https://www.sec.gov/Archives/edgar/data/1513845/000110465926100347/tm2623863d1_ex99-1.htm
- Pro forma (before any Q3 capex burn, which I cannot observe): original convert principal about $13.45B plus $0.775B secured, against cash of roughly $14.5B (8.04 + 5.68 + 0.775). Counting the NVIDIA warrant and the August exchange shares as outstanding (economic basic of about 309M shares, about $77B at $249.87, versus the $68.5B on the reported 274M count), pro forma enterprise value is about $78B including $1.5B of lease liabilities. That is about 26x the June ARR of $3.0B and about 9.8x the midpoint of the YE26 ARR guide ($8B). This is my arithmetic.

Shares and dilution. Basic shares outstanding were 271,855,218 at 30 June 2026 (238.4M Class A, 33.5M Class B, excluding 50.2M treasury). Weighted basic shares rose from 238.5M in Q2 2025 to 280.4M in Q2 2026. Sources of dilution in H1 2026: ATM sales of 12.7M shares at $223.6 for about $2.85B (May and June), and an NVIDIA pre-funded warrant for 21,065,396 shares for $2.0B (about $95 a share, exercise price $0.0001). Economically outstanding shares are about 309M (basic plus the 15.8M exchange shares plus the 21.1M NVIDIA warrant shares). Adding every convert as-converted gives about 377M fully diluted (about +39% versus reported basic, about $94B at $249.87). This excludes options, RSUs and any ATM use since 30 June. The March 2026 notes can be settled in cash, shares or a mix, so net-share settlement would lower this. See dilution_as_converted.csv.

Short interest. 46.78M shares, 18.49% of float, 3.6 days to cover on 2026-09-15; it peaked at 60.2M (23.8%) on 2026-07-31. Source: https://www.marketbeat.com/stocks/NASDAQ/NBIS/short-interest/

Consensus. Buy rating, average price target $283.58 (low $84, high $415) from 19 analysts per stockanalysis (a different page of the same site said 9 analysts), data dated 2026-09-25 and 2026-09-30. FY2026 revenue consensus $3.34B (low $3.0B, high $3.59B, 20 analysts; top end of the $3.0B to $3.4B guidance) and FY2026 GAAP EPS -$2.28 (8 analysts). FY2027 revenue consensus $12.3B (low $8.81B, high $17.99B, 21 analysts) and FY2027 GAAP EPS -$5.64. Source: Yahoo Finance analysis page, https://finance.yahoo.com/quote/NBIS/analysis/ , early October 2026 (no explicit as-of date shown); also https://stockanalysis.com/stocks/nbis/forecast/. A news summary attributes to BNP Paribas a view that ARR could approach $22B by end-2027 [UNVERIFIED, secondary].

Insiders (Form 4s, EDGAR): director Ophir Nave sold 500,000 shares at an average of about $235 (about $118M) on 2026-10-05; director Charles Ryan sold 50,000 shares at $263 to $270 on 2026-08-14; the CEO and two other officers sold 14k to 38k shares each on 2026-10-01 at $234.16, which may be tax-related [UNVERIFIED]. See insider_form4_summary_aug_oct2026.csv.

Next earnings: 2026-11-10 per stockanalysis [UNVERIFIED; not confirmed by the company].

## 2. How it makes money, unit economics, last two quarters, catalysts

Business. About 98% of revenue is Nebius AI cloud: dedicated GPU capacity (Nvidia) sold on reserved contracts and on demand, plus storage, networking and a growing software and inference layer (Token Factory, plus Tavily, Eigen AI, Clarifai and Inferize acquisitions). Avride (autonomous vehicles and delivery robots, adjusted EBITDA loss of $40M in Q2) and TripleTen (edtech, $10M revenue) are small. Stakes in ClickHouse and Toloka are carried as investments.

Last two quarters (Q2 6-K and letter: https://www.sec.gov/Archives/edgar/data/1513845/000110465926094568/tm2622968d1_ex99-1.htm):

| | Q1 2026 | Q2 2026 |
|---|---|---|
| Group revenue | $399.0M (derived from H1 less Q2) | $582.3M (+454% y/y) |
| AI cloud adjusted EBITDA margin | 45% | 50% ($285.7M) |
| Group adjusted EBITDA | $129.5M | $236.2M (41%) |
| D&A | $212M | $259.7M |
| Capex (cash) | $2,473M | $5,657M |
| Reported operating cash flow | $2,258M | $2,246M |
| ARR (last month x12) | $1.9B | $3.0B |

Quality of operating cash flow (cash_flow_quality.csv, my arithmetic from the 6-K): in Q2, reported operating cash flow of $2,246M included a $1,197M rise in deferred revenue (customer prepayments) and a $1,187M fall in receivables. Strip those out and operating cash flow was about -$138M. For H1, $4,504M reported versus about -$319M excluding prepayments and receivables. The business is financing growth with customer cash, converts and equity, not with self-generated cash.

Contracts (contracts_and_backlog.csv). Microsoft, signed 2025-09-08: up to $17,393M over 5 years at the Vineland, NJ site, nine tranches in 2025 and 2026, with about $6,958M paid upfront (40%) and the rest monthly through October 2031, take-or-pay regardless of usage. Meta #1 (2025-11-01): about $2,881M over 5 years. Meta #2 (2026-03-16): about $12B over 5 years of Vera Rubin capacity starting early 2027, plus a Meta commitment to buy up to $15B more capacity that Nebius intends to resell, with Meta taking any remainder. Remaining performance obligations were $37,491M at 30 June 2026: 36% (about $13.5B) to be recognised in the 24 months to June 2028, 40% in months 25 to 48, 24% after. RPO excludes anything of one year or less.

Unit economics per MW, from company disclosures (letter: https://assets.nebius.com/assets/a6ecfd85-a6cb-4967-8ef7-9a25bd261f9c/SHLQ226.pdf):
- Annual contract value per MW: about $12M for the "2026 base" of capacity coming online through 2027, above $20M for Q2 deals ($20M to $25M), above $40M for short-term capacity deals signed in Q3. Cross-check: the Microsoft contract is $17.39B over 5 years on a 300 to 315 MW campus (MW from secondary sources), which is $11.0M to $11.6M per MW per year, matching the $12M base.
- Management says prepayments cover 50% to 60% of capex on Q2 deals, and payback on capex plus related operating costs is 1 year 10 months (revenue basis, excluding prepayments, including capacity not yet built).
- My derivation: payback of 22 months at $22.5M a MW implies cumulative capex plus opex of about $41M per MW, so capex of roughly $30M to $36M per MW depending on opex [UNVERIFIED; management does not disclose capex per MW]. At 5-year depreciation that is about $6M to $7M per MW per year, or 25% to 32% of ACV. For the $12M base contracts the same capex would give a 3 to 4 year simple payback. Scenarios are in unit_economics_per_MW.csv.
- The Microsoft contract itself gives a second, independent hint: if prepayments of $6.96B cover 50% to 60% of its capex (the ratio stated for Q2 deals, not verified for Microsoft), capex is $11.6B to $13.9B, or $39M to $46M per MW [UNVERIFIED].
- Depreciation life: GPUs moved from 4 to 5 years effective 1 January 2026. The 20-F estimated a $167.6M FY26 reduction in depreciation; the Q2 6-K reports a $43.0M reduction in Q2 and $86.1M in H1 (net income effect $34.1M and $75.7M). That is real but small beside a $190M Q2 net loss and has no cash effect. Comparison: CoreWeave's useful-life policy was not confirmed in my sources [UNVERIFIED].
- Spot pricing: Ornn H100 SXM index $2.86 per GPU-hour on 2026-10-06 (3-month range $2.46 to $3.17); B200 $7.56 (https://data.ornn.com/markets/h100-sxm). Nebius's own list price, which is above these indices, rises on 2026-10-01: H100 $3.85 to $4.50, H200 $4.50 to $5.40, B200 $7.15 to $8.50, B300 $7.85 to $9.50 (https://nebius.com/prices, fetched 2026-10-06). Committed rates are up to 35% below on-demand.

Guidance (reaffirmed 2026-08-12): FY26 revenue $3.0B to $3.4B; YE26 ARR $7B to $9B; adjusted EBITDA margin about 40%; capex $20B to $25B; contracted power 5 GW by YE26 (raised from more than 4 GW in May); connected power 800 MW to 1 GW by YE26; over 1 GW per year of new capacity from 2027; more than $9B of customer prepayments in 2026; about $40B of customer commitments available to finance against. Competitor comp (from search summaries, not fetched in full [UNVERIFIED]): CoreWeave Q2 2026 revenue $2.6B, 1.5 GW active, 4.2 GW contracted, $104.2B backlog, FY26 capex $35B to $39B.

Dated catalysts, next 12 months:
- 2026-10 to 11: Vineland follow-through (NJDEP permit decision, stop-work orders lifted, Bloom fuel cell commissioning). Status of stop-work orders not found as of 2026-10-06.
- 2026-11-10 (approx): Q3 results; first test of the ARR path from $3.0B and the signed "capacity deployed late in Q2 contributing in Q3".
- Late 2026: formal 2027 guidance (management deferred it), further asset-backed financings on the $40B of backlog, the Q3 short-term capacity deal going live, ongoing ATM use.
- 2026-12-31: the 5 GW contracted, 800 MW to 1 GW connected and $7B to $9B ARR tests.
- Early 2027: Meta #2 Vera Rubin delivery; Q4 results; Independence, MO Phase 1 target of Q2 2027 and Butler Twp, PA 260 MW target of October 2027 (the site pages conflict on Independence timing).
- Not before late 2026: Nvidia Vera Rubin volume shipments (Nebius has early NVL72 units in test).

## 3. The obvious narrative

Consensus and a first-pass answer say: pure-play AI neocloud with Microsoft and Meta anchoring about $40B of backlog, revenue up 454%, adjusted EBITDA margin about 50% in the cloud segment, power pipeline of 5 GW contracted, pricing rising (Q2 deals above $20M per MW, list prices up 17% to 21% on October 1), Nvidia as a shareholder, ClickHouse worth about $15B as a hidden asset, and Buy ratings with average target near $284. The typical bear case is GPU depreciation life, financing needs and dilution, competition from CoreWeave and hyperscalers, and AI-demand cyclicality. Almost all of that is already in the price: the stock is up more than 100% since March.

## 4. The live debates and the public data that could settle them

1. Is contracted power demand or optionality? The 5 GW is land and power commitments. Contracted customer revenue (RPO) is $37.5B. At roughly $12M per MW per year over 5 years, $37.5B is about 600 to 700 MW of customer-contracted capacity. Settle with: quarterly RPO in the 6-K notes, TCV of new deals, connected MW disclosures.
2. Can ARR reach $7B to $9B at year end? See guidance_bridge.csv. With H1 revenue of $981M and FY guide of $3.0B to $3.4B, H2 revenue is $2.0B to $2.4B. If Q3 is $0.8B to $0.9B, Q4 is $1.1B to $1.5B. A December monthly run rate of $583M to $750M (ARR of $7B to $9B) would then represent 38% to 49% of all Q4 revenue, meaning Oct and Nov average only $320M to $470M a month versus $250M in June. The guide is therefore a December-loaded step function dependent on tranche delivery. A secondary-source summary of the Q2 call says connected power monetises across H1 2027 and not Q4 2026 [UNVERIFIED]. Settle with: Q3 revenue (Nov), Microsoft tranche delivery language, MW connected.
3. Are the hyperscaler contracts good business? $12M per MW against an implied $30M to $45M capex suggests a thin unlevered return that depends on financing spreads (SOFR+250bp) and on GPU residual value. Settle with: contract disclosures, asset-backed facility terms, Q3 capex versus MW added.
4. Execution and permitting at Vineland, the only site carrying the $17.4B Microsoft contract. See hypothesis 3 and the trail.
5. Funding gap and dilution. Capex guide $20B to $25B; H1 capex was $8.1B; cash plus pro forma raises about $14.5B plus >$9B expected prepayments. Settle with: Q3 6-K cash flow, ATM disclosures, 6-K announcements.
6. GPU price direction and useful life. Spot H100 is flat to lower within a $2.46 to $3.17 range; Nebius has raised list prices. Public indices (Ornn, Silicon Data) can track the spread between Nebius list and market. Depreciation life is a smaller issue than the market thinks given payback under 2 years on new deals (but see hypothesis 2 for the other tail).
7. Customer concentration. 2025: two customers were 25% and 15% of revenue. Q2 2026: three customers were 24%, 21% and 14% (59% combined); none of A and B from 2025 exceeded 10% in H1 2026. The names are not disclosed.

## 5. Variant hypotheses

### H1. Contracted revenue, not contracted power, sets the 2027 numbers, and RPO supports far less revenue than the stock implies

Claim. RPO of $37.5B converts at only 36% in the 24 months to June 2028 (about $13.5B). Subtracting an assumed $1.2B to $2.0B for H2 2026 and spreading the rest over 2027 and H1 2028 with a back-weighted ramp (55% to 65% landing in calendar 2027), the 30 June RPO supports about $6.3B to $8.0B of 2027 revenue. Consensus FY2027 revenue is $12.3B (Yahoo; range $8.8B to $18.0B). So roughly 35% to 49% of consensus 2027 revenue (about $4B to $6B) must come from bookings not in the 30 June RPO: new deals, on-demand and sub-one-year contracts, which RPO excludes. The allocation split is my assumption; the RPO total and its 36/40/24 split are filed data. Separately, the market is capitalising 5 GW of contracted power (which needs well over $150B of capex at $30M+ per MW) as if it were demand.

Why it matters. At about $78B EV and about 377M fully diluted shares, each year of delay or each 10% shortfall in conversion changes the required equity raise by billions, and the funding comes at an ever-higher share count.

Test datasets. Each 6-K RPO footnote (quarterly: Q3 on about 2026-11-10 shows the RPO change after new bookings, and the 24-month bucket); Q3 6-K deferred revenue and prepayments; new-deal TCV disclosures; Microsoft and Meta tranche delivery notices; EDGAR XBRL.

Evidence for. RPO bucket data above; Meta #2 revenue only starts early 2027; the YE26 guide is December-loaded; Q2 deals only averaged about $1B each, so four of them are about $4B+ of $37.5B.
Evidence against. RPO excludes sub-1-year deals, and the new short-term deals priced above $40M per MW; Q2 TCV grew 4x quarter on quarter; $40B of commitments is mentioned as available to finance; Palantir partnership (2026-09-08) and the asset-light partner model could add capacity without Nebius capex. RPO growth of $15B+ per quarter would invalidate this.

### H2. Two-tier economics: the anchor hyperscaler contracts are close to financing arbitrage; the equity value rests on short-dated, above-$20M-per-MW deals with young AI labs

Claim. Anchor Microsoft and Meta capacity earns about $11M to $12M of ACV per MW on capex I estimate at $30M to $45M per MW, so unlevered payback is roughly the full 5-year term, and the return is mostly a spread over 6% to 7% secured funding. The headline "1 year 10 month payback" belongs to new 1-to-3-year deals, signed with counterparties like Reflection and Cohere, that are repriced to market again before a 5-year depreciation life ends. So the real exposure is re-contracting and counterparty credit, not the 4-vs-5-year accounting life.

Why it matters. This decides terminal margin. At $22.5M ACV and about $32M capex, 5-year depreciation is 28% of revenue and EBIT margin about 50%; at $12M it is 53% of revenue and EBIT margin about 25%. A mix shift to the second kind of contract is the whole bull case.

Test datasets. Ornn and Silicon Data indices versus Nebius list prices (weekly scrape of nebius.com/prices); quarterly ACV per MW disclosures; secured-facility terms; capex per MW from the Q3 and Q4 letters (capex divided by MW added); counterparties' own funding news.

Evidence for. The 12-versus-20-versus-40 chart in the letter; Microsoft ACV matches $12M; the sub-$3 H100 index versus Nebius $3.85 list suggests Nebius's own price power depends on its supply constraint.
Evidence against. Capex per MW is my inference, not disclosed; the 50% to 60% prepayment funding means customers carry the capex; list prices rose 17% to 21% on October 1 and an auction cleared 15% above prior Blackwell prices, which suggests scarcity pricing is real.

### H3. Delivery risk at the Microsoft site is under-disclosed and is a dated, observable catalyst

Claim. The only site carrying the $17.4B Microsoft contract ran with local and state permit failures that were not mentioned on the 12 August earnings call: two city stop-work orders (6 and 10 August), a state air-permit application withdrawn in May after deficiencies, 62 gas generators (about 123 MW, 45 seen operating) with no air permit and a $1.07M NJDEP fine on 22 September, against a Bloom fuel-cell plan of 328 MW promised as operational "this year" (2026-05-20 press release) while another page says 2027. The Microsoft contract has liquidated damages and tranche termination rights for delay. Management said "we are on track with our delivery" two days after the second stop-work order.

Why it matters. About 40% to 50% of YE26 ARR (my estimate: $3.5B a year of Microsoft revenue at full deployment versus $7B to $9B ARR) depends on this one site. A sharper cut: Customer C was 24% of Q2 revenue (about $140M) and 83% of receivables at December 2025, which fits an upfront Microsoft invoice, but the filing does not name it [inference, UNVERIFIED]. If C is Microsoft, only about $0.56B a year of a roughly $3.5B full run-rate was live in Q2, so about $3B of the $4B to $6B ARR step from $3.0B to $7B to $9B depends on Vineland tranches 3 to 9 arriving in H2. That turns a permit story into a guided-ARR story. A termination right on even one tranche is a multi-hundred-million-dollar revenue event, and the $775M secured facility rests on an investment-grade customer's cash flows.

Test datasets. NJDEP air-permit database and enforcement notices; Vineland planning board and construction code records; Bloom Energy filings (https://fuelcellsworks.com/2026/07/29/electrolyzer/bloom-energy-reports-record-second-quarter-2026-financial-results-and-raises-full-year-2026-guidance for Q2); Nebius 6-K tranche language; Q3 revenue versus the guidance bridge.

Evidence for. Sources in the trail below (Hunterbrook, WHYY, NJDEP-related reporting, Floodlight drone survey).
Evidence against. Phase 2 was approved 9-1 on 17 August; the generators are described as interim construction power; the 17 July 6-K says the latest tranche was delivered on schedule; DataOne says it does not expect a delay to timeline; the fine was only $1.07M; no evidence yet that Microsoft has used a termination right. Liquidated-damage rates are redacted in the exhibit [DEAD END].

### H5 (earnings quality). Part of future adjusted EBITDA will be non-cash accretion on customer prepayments

Claim. Q2 interest expense was $119.1M, but interest on the debt note was only $67.3M net of $40.2M capitalised. The MD&A and 20-F say interest expense also includes accretion for significant financing components on customer prepayments. The residual of about $51.8M is my inference for that item (the 6-K does not give the amount; for FY2025 the 20-F gave only $4.5M). Under the accounting model this accretion is expensed now and added back to revenue when the prepaid service is delivered, so adjusted EBITDA (which excludes interest) will later include non-cash revenue. The effect is not in Q2 EBITDA yet (revenue recognised from opening deferred revenue was only $130.8M in Q2) but it grows as deferred revenue goes from $6.0B toward more than $9B of 2026 prepayments, at roughly 5% to 6% implied.

Why it matters. It makes the 40% margin guide less comparable to peers and means free cash flow, not EBITDA, is the right metric. The direction of the revenue add-back is my reading of the standard; the filings do not quantify it [UNVERIFIED].
Test datasets. Q3 and Q4 6-K interest-expense table versus the debt-note interest table (the gap), revenue-recognition footnote, deferred revenue roll-forward.
Evidence for. The definitions in the MD&A (https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d1.htm) and the $51.8M gap. Evidence against. The gap could include other items such as lease interest; Nebius does not report it.

### H4 (weaker). Financing mix is moving from cheap converts to expensive equity-like capital, and the dilution is bigger than basic share counts suggest

Claim. Reported basic shares are up 14% in a year, but the stack of in-the-money converts, the NVIDIA warrant and the August exchange adds up to about 377M fully diluted shares. The cost has risen: the Aug 2034 notes carry 4.50% coupon plus 25% accretion (an effective yield of about 7.5%), versus 1.0% to 3.0% in 2025; the secured loan is SOFR+250bp.

Why it matters. It is the swing factor between "revenue growth" and "per-share value".
Test datasets. 6-K debt notes, Form 4s, 13F (NVIDIA), ATM disclosures.
Evidence for. Dilution_as_converted.csv; ATM at $224; 20-F and 6-K debt notes. Evidence against. Convert conversion premia are 40% to 80%, signalling that Nebius is selling stock dear; cash settlement options on the 2026 notes; high prepayments reduce external funding needs.

## 6. Catalog of free external datasets

See external_datasets.csv for the full list with verification status. Highlights, all returning HTTP 200 on 2026-10-06 unless noted:
- GPU rental price indices: Ornn OCPI https://data.ornn.com/markets/h100-sxm ; Silicon Data https://www.silicondata.com/products/silicon-index/h100 ; list-price panel https://getdeploying.com/gpu-price-index ; Nebius list prices https://nebius.com/prices
- SEC: submissions API https://data.sec.gov/submissions/CIK0001513845.json ; XBRL companyfacts https://data.sec.gov/api/xbrl/companyfacts/CIK0001513845.json ; Form 4 browse https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=1513845&type=4 ; 13F datasets https://www.sec.gov/data-research/sec-markets-data/form-13f-data-sets
- FINRA short interest https://www.finra.org/finra-data/browse-catalog/equity-short-interest/data
- Power and permits: EIA https://www.eia.gov/electricity/data/browser/ (API needs a key; api.eia.gov returned 403) ; PJM queues https://pjm.com/planning/service-requests/interconnection-queues ; NJDEP https://www.njdeponline.com/ ; City of Vineland https://www.vinelandcity.org ; Cumberland County https://www.cumberlandcountynj.gov ; Federal Register https://www.federalregister.gov
- Comps: CoreWeave IR https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx (from search summary; not fetched). Bloom Energy results (link in H3).
- Dead ends: Internet Archive Wayback was offline on 2026-10-06 (blocked a historical Nebius price series). Google Trends returned HTTP 429 to scripts; use it by hand. Job postings: not tested [UNVERIFIED].

## 7. Modelability

Drivers and what is observable:
- MW online: only year-end 2025 active power (about 170 MW, 20-F) and partial site data are public; connected-MW by quarter is not in the 6-K [data gap]. Guidance is 800 MW to 1 GW connected at YE26.
- ARR per MW: ARR/active MW is about $7M at YE25 [UNVERIFIED, depends on a Dec-25 ARR I did not source] and company ACV per MW is $12M base, above $20M new.
- GPUs and $/GPU-hour: contracts are priced per GPU-hour but rates are redacted; list prices are public; GPU counts are not.
- Utilisation: the company says it is sold out; no number.
- Capex per MW: not disclosed; derived $30M to $46M [UNVERIFIED].
- Depreciation: 5 years (from 4); data center shells likely longer.
- Funding: prepayment percent, convert terms, ATM sizes and the secured facility are all public, so the funding side can be modelled well.
Main gaps: connected MW by site and date, GPU counts and mix, capex per MW, contract rates, who customers C, D and E are, and the 2027 guidance (not yet issued).
Overall: a funding and capacity-ramp model is feasible from filings. A per-GPU-hour model is not.

## 8. Key risks

- Financing: capex of $20B to $25B this year, reliance on markets staying open; the 52-week range is $73.52 to $299.86 and the stock was $116 as recently as March, so the funding window is stock-price dependent.
- Delivery: permits, Vineland, grid and fuel cells; US greenfield sites (Independence moratorium on new projects, Butler Twp still needs final plan approval).
- Customer concentration and credit: top three customers 59% of Q2 revenue; AI-lab counterparties on short contracts; Meta's resale commitment is a backstop whose terms are redacted.
- Pricing: spot H100 index $2.46 to $3.17 over three months; Nebius list is above market.
- Technology: Vera Rubin transition and 5-year useful life.
- Dilution and leverage: about 40% fully diluted uplift; Q2 interest expense of $119M is half of group adjusted EBITDA of $236M (and $40M more was capitalised); stock-based compensation was $102M in Q2; goodwill of $606M from acquisitions.
- Governance: dual-class shares (Class B has 10 votes), insider selling at $231 to $243 on 5 October.
- Short interest of 18% to 24% of float makes the tape volatile in both directions.

## 9. Investigation Trail

1. Searched EDGAR submissions for CIK 0001513845 → found Nebius files 20-F and 6-K, not 10-K/10-Q (https://data.sec.gov/submissions/CIK0001513845.json), plus a flood of Form 4 and 144 filings in Aug to Oct 2026 and four 6-Ks on financing in July to October → raised question: what changed since the model-memory hints? → opened the Q2 6-K (2026-08-12) and its financial statements. CLOSED (filing regime).
2. Q2 6-K showed operating cash flow of +$2.2B against a loss → checked the cash-flow statement → deferred revenue +$1.2B and receivables -$1.2B explain it; underlying about -$0.14B → changed my view: reported OCF overstates self-funding; the business is customer-prepayment funded (cash_flow_quality.csv). CLOSED.
3. Thread A (unit economics, 4 levels). Level 1: Q2 letter chart shows ACV per MW $12M base, >$20M Q2 deals, >$40M short-term, payback 1y10m. Level 2: asked where $12M comes from → Microsoft $17.39B/5 yrs on a ~300 MW campus equals $11.6M per MW, a match (20-F note and Exhibit 4.4). Level 3: asked what capex that implies → payback arithmetic gives $30M to $36M per MW, and Microsoft's 40% prepayment against 50% to 60% capex coverage gives $39M to $46M [both UNVERIFIED] → implies anchor contracts are thin on unlevered returns, and the headline payback applies only to new 1-to-3-year deals (hypothesis H2). Level 4: asked if pricing is real → Nebius list prices rise 17% to 21% on 2026-10-01 (nebius.com/prices) but the Ornn H100 spot index is $2.86 and falling over 30 days (-6.8%) → mixed. Door: Wayback to build a history of Nebius list prices → DEAD END (Internet Archive offline). OPEN: weekly scrape of list prices and capex per MW from Q3/Q4 data.
4. Thread B (delivery, 4 levels). Level 1: Microsoft contract has nine tranches in 2025 to 2026 (20-F). Level 2: 17 July 6-K says latest tranche delivered and on track; the Q2 call summary says Vineland hearing adjourned and "on track". Level 3: searched local news → two stop-work orders (6 and 10 August, per Hunterbrook and WHYY), two days before the earnings call. Level 4: asked why fuel cells were involved → DataOne withdrew a state air-permit application in May after NJDEP found deficiencies, then 62 unpermitted gas generators (about 123 MW) were found running and NJDEP fined DataOne $1.07M on 2026-09-22 (secondary reporting). → changed my view: Vineland's power was never the permanent fuel-cell plan on the schedule Nebius implied; a timeline discrepancy exists between "328 MW operational this year" (2026-05-20 press release) and "by 2027" on the Vineland page. Branches: (a) liquidated damages rate in Exhibit 4.4 → DEAD END, redacted; (b) Planning Board Phase 2 approval 9-1 on 17 August → CLOSED, positive; (c) stop-work orders lifted? → OPEN, not found; (d) Bloom Q2 results and MW delivered for Nebius → OPEN (Bloom Q2 revenue $1.065B; no Nebius MW found); (e) Microsoft use of termination or credits → OPEN.
5. Other sites checked for delay or permit issues: Independence MO (broke ground 2026-05-13; city passed a six-month moratorium on new data centers in July but not on Nebius; Phase 1 timing conflicts between Q2 2027 and Oct 2027) → CLOSED for 2026 (not a 2026 revenue source); Butler Twp PA (ordinance 2-1, final plan still pending, 260 MW target Oct 2027) → OPEN. Implication: YE26 connected power of 800 MW to 1 GW cannot come from owned US greenfield sites; it must come from colocation and Vineland, and I could not build a site-by-site MW sum from public data [data gap, OPEN].
6. Thread C (financing and dilution, 4 levels). Level 1: converts count in H1 and August. Level 2: read conversion prices: $51.45, $138.75, $183.22/$180.31, $313.46/$324.65; the 2025 and early 2026 notes are in the money at $250. Level 3: August exchange of $800M (of $1.0B) of the $51.45 notes for 15.8M shares plus an NVIDIA warrant at about $95 (21.1M shares) → about 309M economic shares and about 377M fully diluted, +39% vs reported basic (dilution_as_converted.csv). Level 4: effective cost: the 4.50% 2034 notes accrete 25%, an effective yield of about 7.5%; secured debt SOFR+250bp → financing cost is rising from 1% to 3% coupons. CLOSED for the structure; OPEN for Q3 ATM usage (not disclosed until 6-K).
7. Customer concentration: 20-F showed customers A (25%) and B (15%) in 2025 → Q2 6-K shows A and B gone and C 24%, D 21%, E 14% in Q2 → names not disclosed, though Microsoft and Meta tranches began Nov 2025 to Feb 2026 → DEAD END on identity; concentration conclusion CLOSED (three customers at 59%).
8. Searched for RPO → found $37.49B with a 36%/40%/24% conversion split in the 6-K notes → compared with the ARR guide and FY27 consensus revenue of $12.3B (Yahoo; 21 analysts) → built guidance_bridge.csv and rpo_conversion.csv → H1: 35% to 49% of consensus FY27 revenue is not in the June RPO. The bridge shows the YE26 ARR guide implies a December step function. OPEN: Q3 6-K on 2026-11-10.
9. Depreciation debate: 20-F says 4 to 5 years from 2026, -$167.6M FY26; Q2 6-K says -$43.0M in Q2 → compared with $190M Q2 loss → modest; changed my view by lowering this debate's importance relative to contract tenor. CLOSED. Comparison to CoreWeave's policy → DEAD END within time (not verified).
10. Market data: price $249.87, market cap $68.5B, consensus Buy, targets $84 to $415, short interest 18.49% → CLOSED. Insider Form 4s: a director sold 500,000 shares on 2026-10-05 → CLOSED, minor signal.
11. Contract exhibits (20-F Exhibits 4.2 to 4.4) read: terms are priced per GPU-hour with take-or-pay, LDs, and a Microsoft right of first offer on future capacity at the same site; effectiveness conditioned on Nebius obtaining financing → CLOSED. Rates, GPU counts and LD formula redacted → DEAD END.
12. Google Trends and job postings → DEAD END (429 and untested, respectively); EIA power prices → OPEN, not pulled because Nebius's Vineland power is behind-the-meter fuel cell/gas, so grid prices are a weak driver there.

## Scorecard (1 to 5)

(a) Settleable debate with public data: 4. RPO, tranche delivery, permits and Q3 revenue are all observable within six weeks.
(b) Original-data potential: 4. Guidance bridge, RPO conversion, as-converted dilution, permit trail and list-price scraping are all original, though capex per MW is not observable.
(c) Modelability: 3. Funding and ramp are modelable; connected MW, GPU counts and contract rates are not public.
(d) Dated 12-month catalyst: 5. Q3 results on about 2026-11-10, year-end guidance tests, Meta delivery in early 2027, Vineland permits.
(e) Un-crowdedness: 2. Heavily covered, 19 analysts, high retail and short interest; the permit and RPO angles are less crowded.
Total: 18 out of 25.
13. Interest-expense gap (advisor-prompted): $119.1M reported versus $67.3M in the debt-interest table → MD&A and 20-F define the residual as accretion on customer-prepayment financing components → amount not disclosed in the 6-K; $51.8M is my inference → became H5. OPEN: Q3 6-K.
14. FY2027 consensus (Yahoo analysis page): $12.3B revenue → compared with RPO-implied 2027 revenue → sharpened H1. CLOSED for consensus; OPEN for the allocation assumption.
