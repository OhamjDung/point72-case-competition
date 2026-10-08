# FTAI Aviation: Engine Economics and Peer Comps (Phase 2, Workstream C)

Prepared 2026-10-06. Public sources only. All market data are stockanalysis.com statistics and forecast pages (https://stockanalysis.com/stocks/{ticker}/statistics/ and /forecast/, fetched 2026-10-06) unless stated. Items marked [UNVERIFIED] could not be tied to a primary source. "Secondary" means seen through press or transcript summaries, not the original document. Companion files: `comps.csv`, `shop_visit_market.csv`.

Core question: is FTAI a HEICO-style franchise or an engine trader? Short answer: on cash conversion and earnings mix it behaves like an MRO/trader with lessor-style gain income. The market price ($179.44) is only explained if you apply a franchise multiple to EBITDA that already excludes gains.

## 1. Investigation Trail

1. **Starting point.** trail.md and stress_test.md established EV $21.59B, 2026 EBITDA guide $1,525M, 2027 guide $2.3B, gains about 40% of EBITDA, and CFO+CFI conversion of 35-41%. Stress test: the standalone short does not survive (value $198 even with all pillars). This workstream asks the valuation-regime question instead.
2. **Door: market multiples.** Pulled statistics pages for all 11 names. EV verified: FTAI $21.59B (matches). Dead end: no free source gives forward EV/EBITDA or consensus EBITDA (forecast pages show revenue and EPS only; FY27+ is paywalled). Workaround: proxy CY26E EBITDA = TTM EBITDA scaled by consensus revenue growth (constant margin), NTM = CY26E grown by half of next-year revenue growth. These are my estimates, labelled "proxy" throughout.
3. **Surprise: Air Lease.** The stockanalysis page shows last trade 2026-04-07 at $65.00 and delisting 2026-04-08 on acquisition by a Sumitomo-led group. So AL is a take-private precedent (EV $26.55B), not a live comp. Its EV/EBITDA is not given; my 9.5x is an estimate [UNVERIFIED].
4. **Door: cash conversion.** Pulled SEC XBRL companyfacts (User-Agent per rules) for 3 fiscal years. CFO is clean. EBITDA is built as operating income plus D&A (HEI, TDG, SARO, ASLE, VSEC), or pre-tax income plus interest plus D&A (WLFC), or pre-tax plus D&A for GE (rough). AAR's fiscal-year XBRL did not yield a coherent EBITDA, AerCap files a 20-F with no us-gaap facts, AL is delisted: for those I use TTM CFO/EBITDA from stockanalysis. Lesson: TDG's 47% shows CFO/EBITDA is a levered metric (heavy interest). It is not a pure quality test, so the franchise-vs-trader call rests on the combination of conversion, gains and inventory behaviour.
5. **Door: gains share for peers.** XBRL gain-on-sale tags are empty or near zero for HEI, TDG, SARO, VSEC. Lessors (WLFC, AerCap) report gains in tags I could not isolate: [UNVERIFIED], flagged. Dead end for exact lessor figures; their order of magnitude is mid-single to mid-teens percent of EBITDA from memory of filings, not verified.
6. **Door: CFM56 market.** Aviation Week (2026-09-22) quoting GE's CFO: 2026 and 2027 shop visits about 2,400, retirements down to 1.5-2% (from 3-4% then 2-3% guidance), H1-27 removals up more than 10%. Leeham (2026-07-16) on GE Q2-26: about 28,000 CFM56 in service, about 30% not through a first visit, about two thirds not through a second, demand steady "through at least 2028 or 2029", spares orders +34% with delinquencies +20%, shops "oversubscribed". Safran H1-26 (2026-07-28 release): civil spares +27.9% in USD, "low level of retirement". That raised the question of when the peak is. Older Aviation Week summary says about 2,500 visits peaking around 2025 [UNVERIFIED, search snippet], and a 2030 estimate of about 2,000 visits (more than 4,000 CFM-fleet visits split roughly evenly with LEAP) [UNVERIFIED]. Net: the plateau is 2026-2028, decline after, driven by the LEAP crossover. Visual Approach's headline "peak in first shop visits in 2027" is title-only [UNVERIFIED].
7. **Door: LEAP durability and retirement deferral.** GE (Leeham 2026-07-16): LEAP-1B durability kit certified, more than 40% of LEAP-1A fitted, grounded aircraft "nearly zero", LEAP turnaround about 100 days. So the LEAP problem that deferred CFM56 retirements in 2023-25 is fading. Deferral now comes from new-aircraft delivery shortage and cheap-to-run old fleets, not from LEAP groundings. Implication: the retirement wave (and the end of used-serviceable-material scarcity) shifts to 2028-2030, which is exactly when FTAI's capacity is meant to peak.
8. **Door: GE pushback on PMA/USM.** Searched GE commentary. GE's Bernstein deck (2026-05-27, cited in trail.md) calls USM availability "limited" and says CFM56 has "limited risk from retirements". An Aviation Week summary says GE typically offers service-contract discounts to keep PMA out (secondary, undated). No GE statement naming FTAI. Then the twist: **FTAI signed a multi-year materials agreement with CFM International on 2026-01-22** (OEM replacement parts, performance upgrades, repair support; barchart/finviz press release, https://www.barchart.com/story/news/37173281/ftai-aviation-announces-multi-year-materials-agreement-with-cfm-international-to-further-support-cfm56-engines). The OEM is supplying FTAI, which makes open GE hostility less likely near term but also means FTAI's cost of OEM material is set by a counterparty with pricing power (GE and Safran took high-single-digit spares price rises in August per Aviation Week summary). Dead end: no GE or Safran filing language on FTAI specifically.
9. **Door: PMA status.** Chromalloy (not FTAI) holds the FAA PMAs: CFM56-5B/-7B HPT nozzle guide vane, LPT stage-1 nozzle guide vane, HPT shroud, and the HPT stage-1 blade (eplaneai/Aviation Week). FTAI buys them via an exclusive arrangement, "five FAA-approved PMA hot-section parts at cost, saving up to $2M per shop visit" (Yahoo bull-case article, secondary). I did not query the FAA PMA database (DRS) directly: the site is not scrapeable through this tool. [UNVERIFIED] whether FTAI itself holds any PMA. The Chromalloy JV terms and ownership percentage were not found. This is the main franchise-like asset, and it is third-party owned.
10. **Door: 25% share arithmetic.** See section 2. Conclusion: capacity is more than enough, share is the open variable, feedstock is the binding constraint.
11. **Door: inventory.** XBRL inventory and cost of sales for peers give turns. FTAI is the outlier on both level and growth (section 2).
12. **Door: guide inconsistency.** A search summary says FTAI "raised full-year 2026 Adjusted EBITDA guidance to $1.625B from $1.4B" with Aerospace Products $1.05B and 40% margins. That conflicts with the $1,525M in the task brief and with the 29-30% margin on the Q2-26 call. Likely an older (Q4-25) vintage. I use $1,525M. Open item to confirm against the Q2-26 8-K.
13. **Door: forward P/E conflict.** stockanalysis shows FTAI forward P/E 20.2x today, versus the 31x in trail.md (price over $5.83 EPS). The page's own forecast shows 2026 EPS $5.83, so 20x is probably using a different (2027) EPS. Not resolved; not used in the valuation.

## 2. Shop-visit market and FTAI share analysis

**Market (source: Aviation Week 2026-09-22; Leeham 2026-07-16; see shop_visit_market.csv).**

| Year | CFM56 shop visits | Note |
|---|---|---|
| 2025 | about 2,500 | peak estimate [UNVERIFIED] |
| 2026 | 2,300-2,400, upper end | GE CFO |
| 2027 | about 2,400 | removals up more than 10% in H1-27 |
| 2028-29 | strong, declining pace uncertain | GE: demand steady "through at least 2028 or 2029" |
| 2030 | about 2,000 | LEAP overtakes; [UNVERIFIED] |

Peak timing: the plateau runs 2025-2028 at roughly 2,300-2,500 visits; the peak in first shop visits is 2027 per one paywalled headline [UNVERIFIED]. Inside the 12-month pitch window, the curve is flat to up. V2500 visits are not quantified in any free source I found; I test 0 and about 500 [UNVERIFIED assumption].

**Module-to-shop-visit conversion.** FTAI's convention: 3 modules equal 1 engine. 2026 guide 1,200 modules (Q2-26 call, 296 modules in Q2, +61%, gurufocus summary 2026-07) equals 400 engine-equivalents.

| Metric | Value |
|---|---|
| FTAI 2026 share, CFM56 only (400 / 2,400) | 16.7% |
| Share if market includes about 500 V2500 visits | 13.8% (matches the roughly 14% quoted in trail.md) |
| Capacity 3,000 modules | 1,000 engine-eq = 41.7% of 2,400 visits |
| 25% share requirement | 600 engine-eq = 1,800 modules (2,175 if V2500 included) |
| Utilisation of 3,000 capacity at 25% share | 60-72% |
| Volume growth needed from 2026 | +50% to +81% |
| 25% of a 2030 market of about 2,000 | 500 engine-eq = 1,500 modules |

Caveat: a shop visit often consumes fewer than three FTAI modules, so "engine-equivalent" share understates FTAI's share of work content, and may overstate it if each module replaces a smaller scope. Management's own claim that 3,000 modules "supports 25% share" implies about 1.7x headroom, suggesting they assume a lower module-per-visit ratio or more total visits. That mismatch is an open item.

**Is 25% credible?** Capacity: yes. Demand: the volume is plausible by 2028 (growth was 61% last quarter; peer-leading). Feedstock: this is the binding constraint. Retirements at 1.5-2% give about 420-560 engines a year on GE's 28,000 in-service fleet, or 210-280 on about 14,200 active engines (trail.md, Safefly/Aviation Week). FTAI needs about 600 engine-equivalents for the 25% share plus about 100 cores for Power. Module supply also draws on USM, which GE calls scarce. Prices have not yet shown the squeeze (IBA, 2026-03-24, "no value adjustments" in H1-26). I rate 25% as a stretch target (my range 18-25% by 2028), and a share-gain story that hits a shrinking market in 2029-30.

**Competitors.** GE/CFM own shops and are "oversubscribed" with spares delinquencies +20% (Leeham). That is a demand tailwind for third-party modules. StandardAero (Safran/GE shop mix, 2025 revenue $6.06B), AerSale, Lufthansa Technik, AFI KLM and MTU are all active in CFM56; I found no public pricing action from any of them against FTAI modules. [UNVERIFIED], not tested through filings. The relationship with GE is now partly cooperative (materials agreement, 2026-01-22).

**Inventory turns (10-Ks via XBRL, fiscal year-end inventory over cost of sales).**

| Company | Year-end inventory $M | Cost of sales $M | Days | Turns | Inventory vs COGS growth |
|---|---|---|---|---|---|
| FTAI FY25 | 1,193.8 | 1,349.7 (company-wide) | 323 | 1.1x | inventory +117% vs COGS +63% |
| FTAI 6/30/26 | 1,544.6 | 635.8 (Q2, annualised) | 222 | 1.6x | inventory +29% in six months |
| HEICO FY25 | 1,295.3 | 2,698.6 | 175 | 2.1x | +10.6% vs +14.5% |
| TransDigm FY25 | 2,095 | 3,520 | 217 | 1.7x | +11.7% vs +7.7% |
| AAR FY26 | 979.0 | 2,686.0 | 133 | 2.7x | +21% vs +19% |
| StandardAero FY25 | 827.7 | 5,165.1 | 58 | 6.2x | -2% vs +15% |
| AerSale FY25 | 205.4 | 229.5 | 327 | 1.1x | -9% vs -5% |

FTAI inventory has grown 3.8x since FY23 ($316.6M) against cost of sales up 2.7x. It is building faster than sales, and it is the only name besides TransDigm and AerSale at 200+ days. Defence: HEICO and TDG also carry long inventory days because of parts breadth; for FTAI a large part is bought whole engines (trail.md: engine purchases are 75-84% of recent quarterly inventory growth). Inventory is carried like a franchise parts base (high days) but built like a trader's book (whole-engine purchases).

## 3. Comps table and grouping

Sources: stockanalysis.com statistics and forecast pages, 2026-10-06; CFO and EBITDA from SEC XBRL companyfacts (data.sec.gov, 2026-10-06). CY26E and NTM EBITDA are my revenue-scaled proxies, not consensus. Revenue growth is consensus current fiscal year over last actual. Full table with notes in comps.csv.

| Group | Company | EV $B | EV/EBITDA TTM | CY26E (proxy) | NTM (proxy) | FCF yield | CFO/EBITDA FY23 / 24 / 25 | 3-yr cum | Gains % EBITDA | Rev growth | EBITDA margin |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Franchise | HEICO | 44.7 | 30.2x | 29.2x | 27.6x | 2.4% | 59 / 67 / 77% | 69% | about 0 | 20% | 28.5% |
| Franchise | TransDigm | 91.7 | 18.0x | 17.1x | 16.1x | 3.2% | 43 / 53 / 45% | 47% | about 0 | 19% | 50.9% |
| MRO/trading | AAR | 5.0 | 13.8x | 13.1x | 13.1x | 3.3% | TTM 55% | n/a | about 0 | about 18% | 10.3% |
| MRO/trading | StandardAero | 9.2 | 11.7x | 11.4x | 10.9x | 3.2% | 13 / 13 / 43% | 25% | about 0 | 6.5% | 12.5% |
| MRO/trading | AerSale | 0.4 | 17.4x | 17.4x | 16.9x | -16.7% | neg / 43 / neg | neg | n/a | -3.8% | 7.7% |
| MRO/trading | VSE | 6.3 | 28.7x | 21.2x | 19.1x | 0.0% | neg / neg / 21% | neg | about 0 | 63% (M&A) | 16.3% |
| Lessor | Willis Lease | 3.2 | 8.2x | 8.0x | 7.8x | -9.6% | 97 / 81 / n/a | TTM 68% | [UNVERIFIED] | 7.5% | 52.8% |
| Lessor | AerCap | 63.7 | 12.4x | 12.3x | 12.4x | -1.4% | TTM 109% | n/a | [UNVERIFIED] | 1.0% | 57.4% |
| Lessor | Air Lease (delisted 2026-04-08) | 26.6 | n/a | about 9.5x [UNVERIFIED est.] | n/a | -4.3% | TTM about 64% [UNVERIFIED] | n/a | [UNVERIFIED] | n/a | n/a |
| Reference | GE Aerospace | 331.3 | 28.9x | 29.1x | 27.7x | 2.6% | 46 / 56 / 79% | about 60% | about 0 | 9.7% | 22.7% |
| FTAI | FTAI Aviation | 21.6 | 21.7x (SA) | 14.2x on $1,525M guide | 10.3x | -5.2% | 22 / -22 / -26% | -14% | 40% | 55% FY26E | 32.0% |

FTAI details: NTM EBITDA proxy $2,106M (0.25 x 2026 guide $1,525M-implied path plus 0.75 x 2027 guide $2,300M, linear), giving 10.3x. 9.4x on the 2027 guide. Using adjusted TTM EBITDA of about $1,192M (trail.md) gives 18.1x. CFO plus CFI over EBITDA is 35% (FY25) and 41% (1H26), so with asset-sale proceeds treated as operating cash FTAI sits at 44-63% (trail.md), in the HEICO/TDG range only on the generous measure.

**Which group does FTAI resemble?**
- **Cash conversion:** FTAI's three-year CFO/EBITDA is -14% (22%, -22%, -26%), worse than every peer except AerSale and VSE (neg) and similar in sign to MRO/trading names that carry growing inventory (StandardAero 25%, VSE negative, AerSale negative). It does not resemble HEICO (69%) or TDG (47%, which is depressed by interest, not by inventory) or lessors (68-109%, because depreciation is non-cash and sales are not in CFO).
- **Earnings mix:** 40% of EBITDA is gains on sale (sale of assets, sales to the 19%-owned partnership, Russian insurance). Franchise names have about none. Lessors have gains but at lower share. FTAI's mix is lessor-like with a much higher dependence.
- **Growth and margin:** 55% revenue growth, 32% EBITDA margin and a 3-year revenue CAGR forecast of 47% are unlike any peer. That is the only franchise-like trait, plus the CFM-licensed materials and Chromalloy PMA access.
- **Verdict on group:** MRO/trading on cash and inventory, lessor on earnings mix, franchise only on growth.

## 4. Implied value per share under each peer-group multiple

Formula: (multiple x EBITDA - net debt $3.16B) / 102.71M shares. Net debt and shares from stockanalysis, 2026-10-06. Preferred stock, non-controlling interests and the off-balance-sheet SCI stake are ignored (open item). Group multiples use CY26E proxies (median of members; HEICO/TDG average for franchise because there are only two): franchise 23.2x (range 17.1-29.2x), MRO/trading 15.3x (range 11.4-21.2x), lessor 9.5x (range 8.0-12.3x, includes the AL estimate). Ex-gains EBITDA removes 40% of the 2026 guide ($915M, using the FY25 and 1H26 observed gain share) and 30% of the 2027 guide ($1,610M, my assumption [UNVERIFIED]). Applying CY26E multiples to 2027 EBITDA is a forward-year capitalisation: discount by roughly 10-15% to compare with today.

| Basis | EBITDA $M | Franchise 23.2x (range) | MRO/trading 15.3x (range) | Lessor 9.5x (range) |
|---|---|---|---|---|
| 2026E headline | 1,525 | $314 ($223-403) | $196 ($139-284) | $110 ($88-151) |
| 2026E ex-gains | 915 | $176 ($122-229) | $106 ($71-158) | $54 ($41-78) |
| 2027 guide, headline | 2,300 | $489 | $312 | $182 |
| 2027 guide, ex-gains (30%) | 1,610 | $333 | $209 | $118 |

Current price $179.44. Reading:
- At today's price, FTAI trades at 23.6x 2026 ex-gains EBITDA ($21.59B / $915M), the same as the franchise average. The market is paying a franchise multiple on gain-free earnings, or equivalently a trader multiple on 2027-guided earnings (MRO/trading on the 2027 ex-gains base gives $209, on the headline base $312).
- If the right group is MRO/trading and 2026 ex-gains is the right earnings base, fair value is about $106 (41% below the price). Lessors on ex-gains: about $54.
- The bull case requires the 2027 guide ($2.3B, mostly Aerospace $1.4B and Power $450M) to be delivered and valued at a franchise multiple: $489 headline, $333 ex-gains.
- The decision turns on the earnings base (2026 versus 2027) more than on the multiple group, consistent with stress_test.md ($198 central value).

## 5. Open items

Best doors, in priority order:
1. **Consensus EBITDA.** Replace my revenue-scaled proxies with actual CY26/NTM EBITDA consensus (Bloomberg, FactSet, or company-guided EBITDA from peers' Q2 releases). Biggest accuracy gain for section 3.
2. **FAA PMA database (DRS).** Confirm what PMAs exist on CFM56-5B/-7B and who holds them (Chromalloy, FTAI, others). Obtain the Chromalloy-FTAI agreement terms and any cost-sharing from Chromalloy's side.
3. **V2500 shop-visit count** and a primary-source CFM56 forecast (Safran/GE investor decks, Oliver Wyman, IBA/Cirium) to replace secondary 2030 estimate.
4. **Modules per shop visit.** Test whether 3,000 modules is really "enough for 25%" by finding FTAI's average module consumption per visit (Q2-26 transcript Q&A).
5. **Guide vintage.** $1,525M versus $1,625M 2026 EBITDA guide, and 2027 gains share; check against the Q2-26 8-K.
6. **Lessor gains and AL/AER/WLFC conversion** from the 10-K cash-flow statements (gain on sale of flight equipment, 20-F). AL estimate is a placeholder.
7. **AAR EBITDA** on a fiscal-year basis and VSE/AerSale adjusted EBITDA (company-defined) to replace stockanalysis TTM.
8. **Equity bridge.** Preferred stock, minorities, and value of the 19% SCI stake and J&F Power JV not in net debt.
9. **Q3-26 report (expected 2026-10-28, after deadline)** for inventory, Adjusted FCF and gains share.
10. **Dead ends:** forward EV/EBITDA from free sources; GE statements naming FTAI; FTAI inventory split by engines/modules/PMA (not disclosed).
