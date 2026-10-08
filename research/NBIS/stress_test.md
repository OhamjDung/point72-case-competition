# NBIS Stress Test of Candidate Theses (prepared 2026-10-06)

Companion files: screen.md and its CSVs (not redone), stress_test_ablation.csv. Model script: scratchpad model.py (inputs listed in Part 2). Anything I could not confirm in a primary source is marked [UNVERIFIED]. Dollar figures are USD.

## Bottom line

No candidate thesis clears the bar (a gap of 20% or more with evidence strength of 3 or more, and positive expected alpha). T1 (delivery short) comes closest at a 19% gap and strength 3, but its expected alpha is negative once the squeeze-side tail is counted. T2 rests on a mis-stated premise: Nebius depreciates servers over 5 years, not 6. The recommendation is no position; the stock is pricing roughly 2,000 MW of average connected capacity at about $10.5M of revenue per MW over the next twelve months, or a 10x EV/EBITDA multiple on that, and the evidence does not say that is wrong by enough to short against 18% short interest and a doubling since March.

## Part 1. Smoke tests

### T1 (Short): delivery is the binding constraint

| Load-bearing fact | Result | Evidence |
|---|---|---|
| Two Vineland stop-work orders (Aug 6 and Aug 10) | PASS | City orders cite "Installation of a LNG Tank with no prior approvals or permits" and, for the second, "We have no prior approvals, plans, or permits in reference to the Bloom Energy Units" (Hunterbrook, via search summary of https://hntrbrk.com/breaking-news/vineland, retrieved 2026-10-06; NJBIZ confirms the two dates, https://njbiz.com/vineland-dataone-data-center-fine/, 2026-09-23). |
| $1.07M NJDEP fine, 62 unpermitted generators | PASS | "$1.07 million penalty ... largest action ever taken against a data center in New Jersey ... 62 gas generators" of 1,982 kW each, about 123 MW; found at a 29 July inspection (NJBIZ, 2026-09-23). A New Jersey Monitor summary adds a 45-day order to obtain permits or cease operating (https://newjerseymonitor.com/?p=25339, search snippet only; the page returned 403) [UNVERIFIED in full text]. |
| Withdrawn air permit (May) | NOT RE-CHECKED | Carried from screen.md (secondary reporting). Not independently verified today. |
| Link from permit problems to missed ARR | FAIL (not shown) | No source shows a missed tranche, a termination right being used, or a stop order still in force. I found nothing on whether the orders were lifted ("search results do not contain information about the stop work order being lifted"). Phase 2 was approved 9-1 on 17 August; the 17 July 6-K said the latest tranche was delivered on schedule (screen.md). |

Verdict on T1: facts PASS, causal link unproven. The thesis is about timing of a ramp, and the public record shows violations, not delays.

### T2 (Short): depreciation life versus rental price decay

| Load-bearing fact | Result | Evidence |
|---|---|---|
| Nebius uses a 6-year depreciation schedule | FAIL | The Q2 6-K says "the estimated useful lives of such assets should be extended from four to five years," effective 1 January 2026, cutting H1 depreciation by $86.1M (https://www.sec.gov/Archives/edgar/data/1513845/000110465926094844/nbis-20260812xex99d2.htm, read 2026-10-06). Six years is CoreWeave's policy (raised from five to six in 2023; secondary source, https://www.nasdaq.com/articles/michael-burrys-latest-warning-could-be-bad-news-coreweave) [UNVERIFIED against the CoreWeave 10-K]. So Nebius is already shorter-lived than its main peer. |
| GPU rental prices are decaying | FAIL for 2026 | Ornn H100 index is $2.86/GPU-hour on 2026-10-06, up 4.4% in 7 days, down 6.8% in 30 days, 90-day range $2.46 to $3.17 (https://data.ornn.com/markets/h100-sxm). Silicon Data shows $2.82, up 2.5% in 7 days (https://www.silicondata.com/products/silicon-index/h100, 2026-10-06). A secondary source reports H100 rents rose about 40% from October 2025 to March 2026, $1.70 to $2.35 (https://cryptobriefing.com/nvidia-h100-gpu-rental-costs-surge/) [UNVERIFIED]. A 2020-vintage A100 contract running to 2029 is reported for CoreWeave (secondary) [UNVERIFIED]. Old-generation prices are rising, not decaying. |
| Unit returns are thin enough for life to matter | PARTIAL | Derived $12M ACV per MW anchor contracts versus $30M to $46M capex per MW (screen.md, [UNVERIFIED]); but on Q2 deals at $20M to $25M per MW, payback is 1y10m (company letter). |

Verdict on T2: premise wrong; evidence points the other way in 2026.

### T3 (Long): pricing power

| Load-bearing fact | Result | Evidence |
|---|---|---|
| Nebius raised list prices on 1 October | PASS | nebius.com/prices, fetched 2026-10-06: H100 $3.85 to $4.50, H200 $4.50 to $5.40, B200 $7.15 to $8.50, "effective October 1, 2026" (+17% to +21%). B300 showed "contact sales" in today's fetch, so the B300 $7.85 to $9.50 in screen.md is not reproduced [UNVERIFIED]. |
| Uncommitted 2027 capacity sells at spot | UNVERIFIED | Only a press-reported management intention. And spot is below Nebius list: Ornn H100 $2.86 versus list $4.50; Silicon Data $2.82. List price is an asking price, not a clearing price. |
| Peers also raised prices | PARTIAL | A secondary summary says CoreWeave's CFO said in Q1 2026 it was "largely sold out" of 2026 capacity while raising prices across every GPU generation (https://www.spheron.network/blog/coreweave-gpu-pricing-2026, search summary, 2026) [UNVERIFIED primary]. Index data show H100 up in the last week, down over 30 days. |
| Contracted pricing is rising | PASS | Q2 deals at $20M to $25M ACV per MW versus $12M for the base book (Q2 shareholder letter, https://assets.nebius.com/assets/a6ecfd85-a6cb-4967-8ef7-9a25bd261f9c/SHLQ226.pdf). This is the real pricing evidence. |

Verdict on T3: contract-mix pricing PASS; spot and list-hike pillar weak.

### T4 (Either): dilution and financing cost

| Load-bearing fact | Result | Evidence |
|---|---|---|
| Dilution stack | PASS | 271.9M basic at 30 June, about 309M economic, about 377M fully diluted (+39%), from filings (dilution_as_converted.csv; Q2 6-K and 8/19 and 8/24 6-Ks). ATM sold 12.7M shares at $223.6 in May and June. |
| Convert terms and financing cost | PASS | $3.45B 0.50% due 2030 (conversion $313.46) and $2.3B 4.50% due 2034 (conversion $324.65, accretes to 125%); $775M secured at SOFR+250bp (6-K exhibits cited in screen.md). |
| Roughly $52M interest gap | PARTIAL | Q2 interest expense $119.1M versus $67.3M in the debt note: arithmetic holds; the cause (accretion on customer-prepayment financing) is the 6-K's definition but the amount is not disclosed [UNVERIFIED]. Size: $52M is 0.06% of an $84B EV. It is an earnings-quality issue, not a valuation lever. |

Verdict on T4: facts PASS, magnitude small.

### Other premises in the brief

- AIB: binding agreement for 50 MW, initial term 12 years, announced 2026-09-30, CLT-01 in South Carolina, first hall within 10 months, second within 14, revenue from H2 2027, 3% annual escalators (https://investingnews.com/aib-data-centers-signs-contract-with-nebius-for-ai-data-center-capacity/ and https://datacenterdynamics.com/en/news/nebius-signs-50mw-lease-with-aib-data-centers, search summaries). This is a lease Nebius pays, adding supply for H2 2027, not a revenue contract. Confirmed.
- Meta optional capacity: the 20-F describes a further order with "a potential total contract value of up to $15 billion" that Nebius intends to resell, Meta buying any unsold remainder (20-F text, https://www.sec.gov/Archives/edgar/data/1513845/000110465926052948/nbis-20251231x20f.htm). Whether it sits in RPO is not stated; the $37.5B RPO is below $12B plus $15B plus Microsoft's $17.4B, so it is probably excluded [UNVERIFIED].
- FY2027 revenue consensus: $12.30B from 21 analysts (https://stockanalysis.com/stocks/nbis/forecast/, 2026-10-06); Yahoo range $8.81B to $17.99B (screen.md). I could not reproduce a $2.4B figure for 2027 [UNVERIFIED].

## Part 2. Ablation

### Method and inputs

Driver model: revenue = average connected MW over the next twelve months (NTM) at a PT date of October 2027, times realised revenue per MW, times EBITDA margin; EV = multiple times NTM EBITDA; equity = EV minus net debt plus ClickHouse stake ($1.6B book), divided by shares.

| Input | Base | Source |
|---|---|---|
| Connected MW | YE26 900 (guide 800 to 1,000); about 1,500 at Oct 2027; about 2,525 at Sep 2028; NTM average about 2,010 | Guidance in screen.md (reaffirmed 2026-08-12); 2027 pace is my assumption below the "over 1 GW per year" guide |
| Realised revenue per MW | $10.5M | Between $12M base ACV and $20M to $25M Q2 deals, less ramp lag (assumption). Check: 2026 consensus revenue $3.34B on about 535 average MW is $6.2M, ARR $8B on 900 MW is $8.9M |
| EBITDA margin | 52% | Q2 AI cloud 50%; CoreWeave Q2 adjusted EBITDA 59% (https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/) |
| Capex per MW | $34M, 55% covered by prepayments | Derived $30M to $46M, [UNVERIFIED]; prepayment share from company letter |
| Net debt at Oct 2027 | $6.6B, plus $15.3B funding for the NTM build ($34M x 1,000 MW x 45%) = $21.9B | Pro forma cash $14.5B and converts in screen.md; my roll-forward. Deferred revenue ($6.0B) not treated as debt, for comparability with peers |
| Shares | 359.2M as-converted (excludes out-of-the-money August 2026 converts, counted as $6.7B debt) plus 10M ATM and other issuance | dilution_as_converted.csv |

Today's EV at $250 on 359M shares: about $84B (as-converted, net of $14.5B pro forma cash, $6.7B out-of-the-money converts, $0.8B secured, $1.5B leases); screen.md's $78B treats in-the-money converts as debt at par. Both within the $77B to $94B range.

Peers: CoreWeave at $91.72 has market cap $50.6B, EV $96.6B, debt $51.6B, EV/sales 12.8x trailing (https://stockanalysis.com/stocks/crwv/statistics/, 2026-10-06), and consensus revenue of $12.87B for 2026 and $26.26B for 2027 (https://stockanalysis.com/stocks/crwv/forecast/, 2026-10-06). That gives EV/2027 revenue of 3.7x versus 6.8x for NBIS ($84B on $12.3B). Applying about 60% EBITDA margin to CoreWeave's 2027 revenue (my assumption) gives about 6.1x EV/2027 EBITDA. A Loop Capital target is reported to imply 10x 2027 EBITDA (secondary, https://finviz.com/news/174059/loop-capital-starts-coreweave-crwv-coverage-at-buy-sets-165-price-target) [UNVERIFIED]; that was set at a higher share price.

### Reverse engineering the price

At $250, base inputs require a market-implied multiple of 10.3x NTM EBITDA of $11.0B (NTM revenue $21.1B, EV $113B in PT-date terms). Holding the multiple constant and flexing one driver at a time:

| Multiple applied | NTM average MW needed (at $10.5M per MW) | Or revenue per MW needed (at 2,010 MW) |
|---|---|---|
| 10.3x (market-implied) | 2,010 | $10.5M |
| 8x (CoreWeave +30%) | 2,700 | $13.5M |
| 6.1x (CoreWeave) | 3,790 | $17.7M |

Reading: the price needs either CoreWeave-plus multiples on a plan close to guidance, or something like 2.7 GW average connected at 8x. YE26 guide of 800 MW to 1 GW and a 2027 pace of roughly 1 GW per year make 2,010 MW plausible; 2,700 requires beating guidance.

### Ablation table (value per share at the Oct 2027 PT date; multiple held at 10.3x so each row isolates one pillar)

| Pillar | Value/share with pillar true | Without pillar (base) | Delta | Gap vs $250 | Evidence (1-5) |
|---|---|---|---|---|---|
| T1 delivery slips (NTM MW 2,010 to 1,650; build 1,000 to 800 MW) | $204 | $250 | -$46 | -19% | 3 |
| T2 economic life 3.5y vs 5y (50% pass-through of extra depreciation on a $55B base) | $184 | $250 | -$66 | -26% | 2 |
| T3 pricing: 35% of NTM capacity at spot +20% | $289 | $250 | +$39 | +16% | 2 |
| T3 downside: spot -15% on that 35% | $221 | $250 | -$29 | -12% | 2 |
| T4 financing: +20M shares, +150bp on $20B debt | $229 | $250 | -$21 | -8% | 4 |
| Re-rating to 8x (not a thesis) | $183 | $250 | -$67 | -27% | 2 |

Evidence scores: T1 3 (violations verified, link to schedule not); T2 2 (premise wrong at 6 years, indices flat to up in 2026, and the effect applies to peers too, so relative short value is smaller); T3 2 (list hike verified, but spot prices sit below list, and 35% uncommitted share is my assumption); T4 4 (all numbers filed, but small).

Does any thesis give a gap of 20% or more with strength 3 or more? No. T1 is 19% at strength 3. T2 clears 20% only at strength 2 and on a wrong premise. The only 20%+ lever is the multiple, which is a valuation view, not a catalyst-linked thesis, and is not falsifiable inside twelve months.

Scenario values (Part 2 model, PT date Oct 2027): bear $108 (NTM MW 1,650, $9.5M per MW, 7x), base $198 (8.5x), bull $364 (2,300 MW, $12M, 11x). Weights 25% / 45% / 30% give about $225, 10% below the price. The distribution is wide and right-skewed; the mean is below the price but with a 30% chance of +46%.

## Part 3. Counter-case to the best thesis (T1, delivery short)

1. The facts are compliance failures, not a schedule slip. Fine of $1.07M against an $84B EV; interim generators are described as construction power; Phase 2 approved 9-1 on 17 August; DataOne says it does not expect a delay (screen.md, secondary).
2. Capacity does not have to come from Vineland. AIB 50 MW (H2 2027), Independence MO, Butler PA, colocation, and the Palantir partnership add supply; guided YE26 MW (800 to 1,000) is not owned-greenfield capacity (screen.md).
3. Slippage is offset by price. Delayed capacity re-prices at $20M to $45M per MW on later deals; combining T1 (-$46) with the T3 uplift (+$39) leaves about -$7 per share (-3%), so delay alone does not produce a 20% gap.
4. Tape. Price +7.4% today, doubled since March, 18.5% of float short (peak 23.8% on 2026-07-31), average target $283.58. A short has to survive a squeeze through the November 10 Q3 print. Directors are selling (500,000 shares at about $235 on 2026-10-05), which supports the short, but is small relative to market cap.
5. Quantified: probability that T1 is materially true and the stock is at or below $204 in twelve months: 35%. In the other 65% the stock averages about +24% (30% bull at +46%, 35% flat-to-up around +5%).

## Verdict

| Item | Result |
|---|---|
| Best thesis | T1 (delivery constrains ARR), with T3 as its offset |
| Viable? | N |
| Direction | None (pass). If forced, T1 short only as a small hedge, not a standalone call |
| PT range and gap | $185 to $225 (T1 case $204 at 10.3x; ±$20 for ±1x multiple); gap about -19% (range -26% to -10%) |
| P(right) | 35% |
| Expected alpha | 0.35 x 19% - 0.65 x 24% = about -9% |
| Carrying pillar | The multiple (about 10x NTM EBITDA versus 6.1x CoreWeave) and MW on schedule; neither is thesis-specific |
| Kill criteria | Exit or do not enter if: Q3 6-K (about 2026-11-10, [UNVERIFIED date]) shows revenue at or above $0.85B and ARR on a path to $7B or more; Vineland stop-work orders lifted and NJDEP permit issued; RPO up by more than $10B in a quarter; Microsoft tranche delivery language unchanged. Thesis confirmed if: Q3 revenue below $0.75B, a tranche termination or credit disclosed, or YE26 ARR guide cut |

## What would change the answer

- A primary disclosure of connected MW by quarter (not public today) would let T1 be tested properly.
- The 2027 guide, expected late 2026 [UNVERIFIED], would anchor MW and revenue per MW.
- A verified CoreWeave EBITDA and useful-life policy would firm up the peer multiple and T2.

## Investigation notes

- Fetches and searches on 2026-10-06: Ornn, Silicon Data (Ornn and Silicon Data pages are free-tier; history beyond 90 days is paywalled), nebius.com/prices, stockanalysis (NBIS and CRWV), NJBIZ, SEC Q2 6-K financials via the required User-Agent. The New Jersey Monitor page returned 403; Silicon Data and Hunterbrook details are from search summaries.
- Dead ends: Vineland stop-order status (not found), CoreWeave primary 10-K life (not fetched), 2027 consensus of $2.4B (not reproduced), capex per MW (not disclosed).
- Model parameters are my assumptions where marked; they are not company guidance.
