# FTAI Aviation (FTAI): Lead-Following Investigation Trail

Prepared 2026-10-06 for the Point72 Academy pitch (deadline 2026-10-12). Public sources only. SEC filings were pulled directly from EDGAR (CIK 1590364); accession numbers are given so every figure can be re-pulled. Price context from the screen: $179.44 on 2026-10-06 (stockanalysis.com).

Conventions. "UNVERIFIED" marks items I could not tie to a primary source. "Secondary" marks earnings-call text I only saw through third-party transcript sites or AI-summarised fetches; verify against the audio or a full transcript before quoting in the pitch. Dollar amounts are in $M unless noted. Quarterly cash-flow figures are derived by differencing year-to-date statements; this method reproduces the Q2-25 release exactly (CFO -110.3, CFI +523.8).

Source key (all EDGAR, CIK 1590364):
- 10-K FY25: https://www.sec.gov/Archives/edgar/data/1590364/000162828026012940/ftai-20251231.htm (filed 2026-02-27)
- 10-Q Q2-26: https://www.sec.gov/Archives/edgar/data/1590364/000162828026051412/ftai-20260630.htm (filed 2026-07-31)
- 10-Q Q1-26: .../000162828026029335/ftai-20260331.htm; 10-Q Q3-25: .../000159036425000041/ftai-20250930.htm
- Q2-26 release: .../000162828026050622/ftai6302026earningsrelease.htm; Q1-26: .../000162828026028390/ftai3312026earningsrelease.htm; Q4-25: .../000162828026011685/ftai123125earningsrelease.htm; Q3-25: .../000159036425000038/ftai93025earningsrelease.htm; Q2-25: .../000114036125027877/ef20052914_ex99-1.htm; Q4-24: .../000114036125006099/ef20044380_ex99-1.htm
- XBRL: https://data.sec.gov/api/xbrl/companyfacts/CIK0001590364.json (pulled 2026-10-06)

Correction to the screen: the screen lists "Fwd P/E ~20x". At $179.44 and consensus 2026 EPS of $5.83 (screen's stockanalysis figure), the multiple is about 31x. Using the 2026 segment EBITDA guide ($1,525M) and the aggregator EV of $21.59B, EV/EBITDA is about 14x 2026 and 9x the 2027 guide ($2.3B). The screen's "21x trailing" is the only multiple that survives, and it is on trailing EBITDA. Consensus PT of $364 versus a $179 price is inconsistent and should be treated as stale until verified.

---

## (A) Investigation Trail

### Door 1. Cash conversion and "Adjusted FCF" — CLOSED on classification; OPEN on one definitional gap

1. Searched the 10-K, 10-Qs and the six earnings releases for "free cash flow" → found the term only as a risk-factor phrase in the 10-K/10-Q, and as a reconciled metric in exactly one release, Q2-25 (footnote: Adjusted FCF = net cash used in operating activities $(110.3)M + net cash provided by investing $523.8M + a $10.0M adjustment for the 50% QuickTurn Europe JV investment = about $423.5M). The Q3-25, Q4-25, Q1-26 and Q2-26 releases contain no reconciliation (grep for "free cash", "net cash", "comprised of" returns nothing relevant). Raised question: if Adjusted FCF is simply CFO + CFI, why did the company stop reconciling it in its 8-Ks? Result: the figures management quotes ($724M for 2025, $158M Q1-26, $255M 1H26, $878M 2026 guide) are only in decks and calls that are not on EDGAR; the 2026 numbers do tie (below), the 2025 one does not.
2. Checked whether CFO + CFI reproduces the quoted numbers → Q1-26: -160.1 + 317.0 = 156.9 (company: $158M). 1H26: -265.3 + 515.7 = 250.4 (company: $255M per call, secondary). So in 2026 Adjusted FCF is essentially CFO + CFI, i.e. pre-financing cash flow including all asset-sale proceeds and the SCI equity cheques. But FY25: -310.7 + 723.3 = 412.6, versus the $724M reported (sources: Q4-25 call summaries on fool.com and investing.com, secondary; the figure does not appear in the Q4-25 8-K exhibit I read). This changed my view because a $311M unexplained gap is the size of the entire negative CFO.
3. Hunted for the bridge. Two arithmetic reconstructions both land on about $724M, and I cannot separate them without the IR deck: (a) CFO + CFI + net investment in unconsolidated entities (328.5 - 27.1 = 301.4) + 10.0 QuickTurn = 724.0; (b) CFO + CFI + the Q4 "growth investments" management named on the Q4 call (SCI co-invest $52M, Power inventory $150M, hot-section parts $50M = $252M) + 10.0 QuickTurn + acquisition of business 49.1 = 723.7. Either way the 2025 metric added back growth spend that the 1H26 metric (which management said "included funding the final $95M capital call") did not. Status: OPEN, hypothesis only. A metric whose definition moves between periods is a pitch-worthy flag, but I cannot call it proven.
4. Chased the second sub-question: where do sale proceeds and inventory purchases land? The 10-K Note 2 "Cash Flow Presentation" (pp. 63, repeated in each 10-Q) answers it, and it is the most important accounting finding of the investigation:
   - Purchases of engines/aircraft where the expected predominant source of inflow is sale, third-party inventory purchases and manufacturing costs go through operating (CFO).
   - Sales of rebuilt whole engines go through investing (CFI) because the rebuilt engine is first transferred from inventory to leasing equipment. FY25: $1,059.0M of such proceeds in CFI versus $779.4M of manufacturing outflows and $325.1M of engine/aircraft inventory purchases in CFO. 1H26: $538.4M in CFI versus $511.2M and $356.7M in CFO. FY24: $436.2M versus $345.8M and $8.3M.
   - Sales to the SCI vehicle land in two places: seed-aircraft sales in investing ("Proceeds from sale of assets to the 2025 Partnership": $530.0M FY25, $175.7M 1H26; the gain is stripped out of CFO), and MRE engine/module sales to it in operating (MRE Contract revenue, receivable from the Partnership $25.5M at 6/30/26).
   So the answer to the screen's question is "both, and mismatched": costs sit in CFO, a large slice of the matching proceeds sits in CFI. Negative CFO is therefore largely a presentation artifact and cannot carry a short thesis by itself.
5. Re-based the bridge for that artifact → Adding the inventory-sourced CFI proceeds back to CFO gives +$748M in FY25 (63% of $1,191M Adjusted EBITDA), +$248M in FY24 (29%), +$273M in 1H26 (44%). The 63% matches management's "60-70% of EBITDA, in line with aerospace peers" (Q2-26 call, secondary: Investing.com). But CFO + CFI, which is what the company's own metric is, gives 35% (FY25) and 41% (1H26), and just 32% in Q2-26 ($93.5M on $291.4M EBITDA). The honest conversion range is 35-63% depending on whether you credit the leasing-asset disposals that the old model relied on. Table in section C.
6. Followed the money to see how it was financed → found that the negative-CFO story does not mean debt-funded growth. Debt was $3,440M at end-2024, $3,449M at end-2025 and $3,453M at 6/30/26 (net of costs); the revolver was drawn and repaid in full ($480M in 2025, $625M in 1H26). The funding source was disposal of the balance sheet: leasing equipment net fell from $1,546M (12/31/25) to $1,146M (6/30/26), and asset-sale proceeds in CFI were $1.7B in 2025 and $793M in 1H26. This changed my view: the earlier H1 ("growth financed by debt") is wrong on the facts; the sharper claim is that conversion depends on liquidating a leasing book that is shrinking and being deliberately replaced by an asset-light model.
7. Branch: the quality of the EBITDA numerator. The CFO statement strips non-cash gains: gain on sale of assets $377.5M (FY25) and $177.9M (1H26), gain on sales to the Partnership $46.4M and $17.6M, and Russian insurance recoveries $54.3M (FY25) and $49.5M (1H26, with $48.3M cash in CFI). Adjusted EBITDA (definition in the release) does not back out any of these. Together they are 40% of FY25 and 40% of 1H26 Adjusted EBITDA (53% in 1H25). The insurance recoveries alone are 8% of 1H26 EBITDA and non-recurring. Segment attribution of the sale gains is not disclosed, so the "gain share of Aerospace EBITDA" is an upper bound: 99% (FY24), 56% (FY25), 38% (1H26). That declining trend is the strongest evidence against the Muddy Waters "80%" claim (see Door 7), but also shows a one-time component in headline EBITDA.
8. Branch: the guide. The 2026 Adjusted FCF guide was cut from $915M to $878M. With 1H26 at about $250-255M, 2H26 needs about $625M, against a Q2 run-rate of about $94-97M and a 2H weighting not explained in any filing I found. Q3-26 (late Oct/early Nov, date UNVERIFIED) is therefore the first real test. Status of Door 1: CLOSED on classification and on the 2026 definition; OPEN on the 2025 $724M bridge and on the 2H26 back-end loading.

### Door 2. Inventory composition and the Power core-feedstock question — DEAD END on composition; OPEN on feedstock competition

9. Searched the 10-K and 10-Q for an inventory footnote → there is none. Note 2 says only that inventory is "aircraft engines, engine modules, spare parts and used material" carried at lower of cost or net realizable value, and the balance sheet shows one line ($551.2M at 12/31/24; $1,193.8M at 12/31/25; $1,544.6M at 6/30/26). No split by engines/modules/PMA/Power. DEAD END on composition: it is simply not disclosed. KPMG (new auditor, see Door 7) did not make inventory a critical audit matter; its sole CAM is maintenance revenue on aircraft leases (10-K, auditor's report).
10. Built a proxy roll-forward instead. The cash-flow note gives "cash paid for engine and aircraft inventory" in CFO: $8.3M (FY24), $325.1M (FY25), $356.7M (1H26). Against the 1H26 CFO inventory outflow of $453.1M and a balance-sheet increase of $350.8M, third-party engine and aircraft purchases account for essentially all of the 1H26 inventory growth (79% of the CFO outflow; 50% in FY25). This changed my view: the growth is mostly bought whole engines, not trapped work-in-process. Combined with the Q4-25 call (secondary: fool.com 2026-02-26) naming $150M of Power inventory and $50M of hot-section parts added in Q4, roughly two thirds of the $296.6M Q4-25 inventory build was Power and parts. Cumulative Power inventory to date is not disclosed (Phase 2).
11. Tested days inventory: Q2-26 inventory $1,544.6M on quarterly cost of sales $635.8M is about 221 days, versus 186 days in Q2-25 on $369.3M. Turns slowed about 19% while volume rose 61%. Not alarming, but it is the direction Snowcap warned about.
12. Is Power competing with Aerospace for scarce cores? Evidence assembled:
   - GE Aerospace's own Bernstein conference deck (2026-05-27, https://www.geaerospace.com/sites/default/files/geaerospace_bernstein_strategic_decisions_conference_presentation_052726.pdf, p.8): "CFM56: stable outlook, limited risk from retirements and workscopes", "new material needed as used serviceable material availability remains limited", "~80% of volume from engines less than 20 years old", and "Aeroderivatives provide a new offset to retirements". So the OEM sees aeroderivative conversion as a sink for retiring cores, and sees used serviceable material as scarce.
   - Aviation Week (GE commentary, article dated 2026-09-22 per fetch, date UNVERIFIED): retirements "somewhere between 1.5% to 2%", shop visits about 2,400 for 2026 and 2027, removals "up double digits" in 1H27.
   - FTAI Q4-25 call (secondary): global retirements 2-3% of a roughly 20,000-engine fleet, "about 400 engines annually". Power's 100-unit 2027 goal is therefore about a quarter of all retiring engines, against 1,200 modules per year in Aerospace (about 400 engine-equivalents at three modules per engine). Fleet counts differ by source (about 14,200 active per Aviation Week/Safefly vs 20,000 in FTAI's framing), which at 1.75% retirement gives 250-350 engines a year. On this arithmetic, Power and the module factory together need more engines than retire.
   - Prices, however, do not yet show the squeeze: IBA (2026-03-24, https://www.iba.aero/about/news/aircraft-engine-values-2026/) reports CFM56-5B/-7B values at "no value adjustments" in H1-26 and "signs we are past the peak seen over the past 18 months". IBA's CFM56-7B24 value moved $5.2M (H1-25) to $5.7M (H2-25); -7B27 $6.8M to $6.4M (via search snippet, IBA update page, UNVERIFIED in detail). Safefly (a vendor page, low quality) quotes core/teardown input of $1.2-1.8M for -5B.
   Conclusion: feedstock scarcity is real in the OEM's words but is not yet visible in traded engine values. I could not find a public time series of CFM56 core prices (Phase 2: paid sources are off-limits, so use Form 4/10-Q purchases per engine, FAA registry deregistrations, and Cirium/ch-aviation retirement counts). Status: composition DEAD END; feedstock competition OPEN.

### Door 3. Module margin — CLOSED (mix is real, but the target was walked back and dollars per module are not rising)

13. Searched management's own words. Q2-26 call (secondary: Investing.com transcript): the compression comes "from the mix", with the example that a 6,000-cycle engine sold for about $6M earns about $2.5M (about 40%) while a 10,000-cycle engine sold for about $12M earns about $3M (about 25%); "for what we classified as the near term, which I would say is probably 1-2 years, we expect margins to be around 30%." The Q4-25 call (secondary: fool.com) had said Q4 achieved 35% and management targeted 40% in 2026. That is a roughly 10-point walk-back in five months, which is the credibility point for H2.
14. Checked the mix claim with the numbers. Aerospace segment margin by quarter (Adjusted EBITDA / products + MRE revenue): Q1-25 35.9%, Q2-25 33.6%, Q3-25 34.8%, Q4-25 34.6%, Q1-26 29.9%, Q2-26 28.5% (table in C). Derived EBITDA per module is $0.90M in Q2-25 (184 modules, derived from "+61%") and $0.84M in Q2-26 (296 modules): down about 6% while revenue per module rose about 11% ($2.66M to $2.96M). So "similar dollars per engine" is roughly right to slightly optimistic, and growth is volume-driven.
15. Branch: is it competition or pricing? Management named no competitor price action (secondary). Safran's H1-26 release (https://www.safran-group.com/pressroom/safran-reports-its-first-half-2026-results-2026-07-28; direct fetch returned HTTP 403, figures via Leeham/search summary) says CFM56 "benefited from a favorable workscope mix", spare parts were up 28% in USD, and the fleet has "a low level of retirement". GE (Q2-26, Leeham 2026-07-16) says CFM56 turnaround is about 90 days with spare-parts delinquency; the supply side is tight for the OEM too. I found no public evidence of price competition from AerSale or StandardAero in module exchanges; absence of evidence is not proof, and I did not retrieve their filings (Phase 2).
16. Branch: related-party revenue mix. MRE Contract revenue (engines and modules sold to, and exchanged with, the SCI "2025 Partnership", in which FTAI holds 19%) was $335.8M in FY25 and $404.0M in 1H26: 30% of Aerospace segment revenue in Q1-26 and 21% in Q2-26 (25% in 1H26). Margin on this contractual revenue is not disclosed; CFO commentary says it varies with exchange scope. Since the MRE share fell from Q1 to Q2 while margin also fell, MRE mix alone does not explain the move. Status: CLOSED as a mix story with the walk-back and the per-module data as the real flags; the unknown margin on related-party revenue goes to Phase 2.
17. Branch: Total Adjusted EBITDA is flat. 1H26 total Adjusted EBITDA was $617.0M versus $616.4M in 1H25; Q2-26 was $291.4M versus $347.8M, down 16%, because Leasing/Corporate fell while Aerospace rose 51%. Net income attributable was $251.8M versus $251.6M. The "40% growth" narrative is currently an Aerospace-only phenomenon, with Corporate and Other operating expense (which carries FTAI Power costs) at $44.8M in Q2-26.

### Door 4. FTAI Power — OPEN (high impact, most unverified)

18. Searched the $1.465B order → the primary source (GlobeNewswire/finviz release 2026-07-22) states: initial purchase order of $1.465B placed with J&F Power Systems, FTAI's joint venture with Jereh Group, by "a leading international cloud service provider"; delivery "in batches through November 2027"; milestone payments beginning with an advance payment at signing; a five-year master agreement allowing more POs; and a performance adjustment mechanism with downward adjustments capped at 10% of equipment value. Customer is unnamed (the call called it "a leading U.S. hyperscaler", secondary). Units and MW are not disclosed.
19. Raised the question "whose revenue is this?" → the order is placed with the JV, not FTAI. Jereh's own exchange-listed disclosure, reported by Yicai (https://www.yicaiglobal.com/news/chinas-jereh-jumps-by-limit-on-usd15-billion-gas-turbine-generator-order-from-cloud-service-provider), describes it as "Jereh's joint venture with FTAI" and says the equity split is not disclosed; it is Jereh's seventh such order since November 2025 and cumulative business from this customer is $1.72B. The Q2-26 10-Q (filed nine days after the PO) does not mention Jereh or J&F at all: Power is not a reportable segment but sits inside "Corporate and Other" (expenses only), the 10-Q lists two reportable segments, and customer deposits and advances were only $29.4M at 6/30/26 (the PO was signed after quarter-end). This changed my view: whether J&F is consolidated or equity-accounted decides whether the hyperscaler prepayment ever hits FTAI's cash flow, and whether "Power EBITDA $450M" is 100% or FTAI's share. Not answerable from public filings today. Next test: Q3-26 10-Q (customer deposits, equity-method note, segment note).
20. Implied unit math. The $1.465B PO alone, divided by an assumed 25 MW unit (the Mod-1 is a 25 MW unit, about 35-40% efficiency, about 9,000 heat rate; Q4-25 call, secondary) at various $/MW: $1.0M/MW gives about 59 units (1.47 GW); $1.2M/MW about 49 units (1.22 GW); $1.5M/MW about 39 units (0.98 GW) (power_implied_units.csv). Management has reportedly framed Mod-1 economics as about $25M revenue and $7-8M Adjusted EBITDA per unit (a Substack summarising the Q4-25 call; UNVERIFIED), and on the Q2 call declined to restate unit economics as "commercially sensitive". At $7.5M per unit, $450M of 2027 EBITDA is 60 units, which is close to the PO-implied 59 units at $1.0M/MW. So the "$450M, materially fewer than 100 units" guide is roughly equal to this one PO and is not obviously conservative relative to firm orders; the "conservative" upside to $750M (from the call, secondary) requires new customers beyond this PO. This is the key revision of the screen's H3 (see section B).
21. Competitors and market durability. GE Vernova sold 29 LM2500XPRESS (about 35 MW each) packages to Crusoe, nearly 1 GW (GE Vernova release); ProEnergy sells PE6000 units built on CF6-80C2 cores (about 48 MW; 21 turbines for two data-centre projects exceeding 1 GW; delivery in 2027), via DCD and eepower reports; Siemens Energy's backlog is near 70 GW with slots into 2030-31 and GE Vernova's gas backlog was reported at 116 GW in Q2-26 (Energy News Beat / trade press, secondary). Wood Mackenzie, via Power Engineering, puts heavy-duty prices heading to about $600/kW by end-2027, up about 195% from 2019; aeroderivative pricing of about $1.2M/MW, up 70% in a year, is from an interview on InPractise (UNVERIFIED). The structural reason FTAI sells at all is lead-time: large OEMs are sold out, and Mod-1 is "mobile... installed in less than two weeks" (Q2 call, secondary). Durability: demand is real while the AI power shortage lasts, but the pricing power rests on shortage, and the stock sold off on AI-infrastructure fears in late September (cause UNVERIFIED; search found no FTAI-specific article). ProEnergy's use of older CF6 cores shows the aeroderivative-from-retired-engine playbook is not proprietary.
22. Political and supply-chain branch. Jereh is a Shenzhen-listed company (GenSystems Power Solutions is its US subsidiary). US lawmakers are drafting limits on Chinese-sourced data-centre equipment, reported by Reuters via asiae.co.kr and others (Aug-Sep 2026); those proposals target defense-related data centres and I found nothing naming the J&F JV. Tariffs and sanctions on a Chinese-owned packaging partner are an unquantified risk; the 10-K risk factors cite tariffs and sanctions generically. Status: OPEN. Best next source: Jereh's Shenzhen announcement (stock code 002353, on cninfo.com.cn) for the JV split and unit count.

### Door 5. Leverage, maturities and SCI structure — CLOSED on debt (no near-term refinancing catalyst); SCI economics PARTLY CLOSED

23. Debt. 10-Q Note 6 and the 8-K of 2026-04-30: $3,496.4M face, all unsecured senior notes: $1,000M 5.50% due 2028-05-01; $500M 7.875% due 2030-12-01; $700M 7.00% due 2031-05-01; $800M 7.00% due 2032-06-15; $500M 5.875% due 2033-04-15. Nothing is due within one year; the first maturity is May 2028. The revolver was amended and restated on 2026-04-24 to $2.025B, matures 2031-04-24, is undrawn, and is now secured by a first lien on substantially all non-aircraft assets including inventory, receivables and IP (leasing equipment and aircraft excluded). Financial covenants: minimum interest coverage 3.0x, maximum debt/EBITDA 4.0x. Cash interest is about $228.8M a year (10-K). On trailing four-quarter Adjusted EBITDA of about $1,192M, gross debt/EBITDA is about 2.9x (about 2.7x net of $337M cash) and EBITDA/interest about 4.8x on $247.8M of 2025 interest expense. So the screen's "$3.45B on $404M of book equity" is true but understates solvency: book equity is thin because of buybacks of preferred, dividends and the $300M internalization fee in 2024, not because of leverage on the cash flow. The cost of the new secured revolver is that inventory is now pledged; for a company whose inventory has tripled, that is a real, if modest, change in creditor position. Door closed: no refinancing event inside the 12-month window.
24. SCI structure. 10-K Note and 10-Q Note 4: the 2025 Partnership is accounted for under the equity method; FTAI is servicer (GP) and holds a 19% limited partner interest; carrying value $365.5M at 6/30/26 (FTAI invested $291.5M in 2025 and $95.1M in 1H26, and received $19.2M of distributions). It is therefore off-balance-sheet: FTAI consolidates none of its debt. My search for the exact phrases "variable interest entity" in the 10-K and 10-Q returned nothing, so no maximum-exposure disclosure is given. The seed assets (about $700M net purchase price for the committed on-lease 737NG/A320ceo aircraft) were sold to it under ASC 610-20, and FTAI records: (i) a gain on sale ($17.6M in 1H26, $46.4M in FY25), (ii) servicing fees in Other revenue ($7.0M Q2-26; $12.8M 1H26; $2.1M Q2-25), (iii) MRE Contract revenue for engines and modules supplied to the Partnership for its life ($335.8M FY25; $404.0M 1H26), with profit eliminated only for FTAI's 19% share ($22.8M FY25, $16.6M 1H26) and "recognized over time as the 2025 Partnership generates income", and (iv) equity in earnings (including a share of profit-sharing). On 2026-01-22 the company adopted a Strategic Capital Profit Participation Plan (8-K, https://www.sec.gov/Archives/edgar/data/1590364/000114036126002691/ef20064098_8k.htm), a carried-interest plan for employees paid out of "profit participation" distributions to the servicer, which confirms that a carry exists; its rate and hurdle are not disclosed. Management and servicing fee percentages are described only as "customary, market-based compensation". Q4-25 call (secondary): Q4 Leasing EBITDA included "$20 million from SCI management fees and co-investment returns"; Q2-26 call (secondary, equibles): "$35 million from 2025 SPV management fees and co-investment returns" in Q2 Leasing EBITDA; 2026 SPV launched with a 15% FTAI commitment; the first ABS ($612M, MRE 2026) closed in Q2 with a July special distribution. DEAD END on fee and promote percentages: not in the 10-K, 10-Q, or any 8-K I read; the Limited Partnership agreement is not public. Key analytic point: about a quarter of Aerospace revenue is sold to an affiliate in which FTAI owns 19%, financed in part by FTAI's own capital calls ($386.6M cumulative), and 81% of that profit is recognized immediately. That is lawful under the stated accounting, but it is exactly the circularity short sellers will cite, and it is where the 2026-27 Leasing guide ($450M in 2027) depends on fee income that is $7M a quarter today.

### Door 6. CFM56 demand durability — CLOSED (supportive through 2027-28; limited peak risk inside the 12-month window)

25. Safran and GE. GE (2026-05-27 deck, p.8): "stable outlook", about two thirds of the fleet has not had a second shop visit, "majority of retirements occur above 20 years", "LEAP profit $ equal to CFM56 profit by 2030". GE's CFO (via Aviation Week, 2026-09-22 per fetch): about 2,400 CFM56 shop visits this year and next; removals "up double digits" in 1H27; actual retirements 1.5-2%, versus earlier guidance of 3-4%, then 2-3%. Safran H1-26 (via Leeham, search summary): LEAP deliveries 1,030 (+41%), spare parts +28% in dollars, CFM56 benefited from "a fleet benefiting from a low level of retirement" and "very strong demand". A Visual Approach paywalled summary headline says CFM56/V2500 "reach peak in first shop-visits in 2027" (UNVERIFIED; title only). 
26. LEAP durability and the retirement feedback loop. GE says LEAP-1A is at CFM56 levels of time-on-wing (deck p.7), LEAP shop-visit turnaround is about 100 days and LEAP-grounded aircraft are "nearly none" (Leeham, Q2-26): this means LEAP problems are no longer forcing airlines to keep older CFM56 aircraft flying, removing one pillar of the "LEAP durability keeps CFM56 alive" narrative. Offsetting, GE says CFM56 retirements are at historic lows and new-engine supply remains the constraint. On the 12-month horizon the shop-visit curve is up, not peaking. The peak question matters for 2028+ and for the valuation duration, not for the pitch window. Dead end avoided: I did not model the FAA registry (the screen's suggestion) because GE and Safran already disclose fleet-wide age and retirement data; FAA covers US-registered aircraft only.

### Door 7. Short reports — CLOSED on the main claims; two threads OPEN

27. Primary reports: not retrieved. The Muddy Waters site did not resolve from this environment and no archived copy was available; claims below are from secondary press (Hagens Berman via AccessNewswire, Barron's via itiger, Seeking Alpha, Benzinga) and from FTAI's own response; Snowcap claims from AccessNewswire/Benzinga summaries. Treat the allegation wording as indicative. Note also that scratchpad files left over from earlier work (`mw.txt`, `sc.txt`) were Nebius pricing pages, not short reports, and were not used.

| # | Claim (secondary sources) | Company response | What later filings show |
|---|---|---|---|
| 1 | About 80% of Aerospace Products Adjusted EBITDA derives from gains on sales, mainly engine sales (Muddy Waters, 2025-01-15) | CEO RBC remarks 2025-01-21 (8-K Ex 99.1): "baseless and nonsensical"; Audit Committee review by independent legal and forensic accountants found allegations "without merit" (8-K 2025-02-20) | Not reproducible from consolidated data: gain on sale of assets in the cash-flow statement was 99% of Aerospace EBITDA in FY24 (upper bound, mixed segments), 56% in FY25 and 38% in 1H26; Aerospace revenue is recognized as ASC 606 product revenue with $1.24B of cost of sales in FY25 (segment table, 10-K). But total gains (sale + SCI + insurance) were 40% of company EBITDA in FY25 and 1H26. PARTLY DISPROVED on trend; segment attribution still undisclosed |
| 2 | Engine sales are relabelled as recurring MRO / one engine sale counted as three modules (MW) | Counter: three modules equal one engine, and customers choose 1, 2 or 3 modules (CEO remarks). Citi analyst called the point "a little hard to understand" (Barron's) | FY25 10-K splits "Aerospace products revenue" ($1,600.5M) from "MRE Contract revenue" ($335.8M, to the affiliated SCI vehicle); 10-Q now discloses engine/module sales. Presentation improved; the underlying "sales, not services" point stands. INCONCLUSIVE |
| 3 | Depreciation on leased engines too slow; leasing returns inflated (MW) | Policy unchanged since 2015; residuals about 50% of cost; 2-6 year lives; ROGA about 10% | 10-K policy unchanged (aircraft engines 2-6 years; residual equals core salvage plus life-limited parts). No restatement. Leasing book is now being sold down. NOT PROVEN |
| 4 | Fortress sold stock in the May 2024 secondary at an inflated valuation (MW) | None specific | Internalization completed May 2024 ($300M fee, paid in shares); no later filing changes the facts. UNTESTED |
| 5 | Inventories "egregiously overvalued", older engines taken as payment marked up; EBITDA "meaningless", underlying cash flow much lower than claimed (Snowcap, 2025-01-29) | Covered by the Audit Committee's blanket finding (no inventory-specific statement found) | Inventory grew 2.8x with no write-down disclosed and no inventory CAM from KPMG; but CFO was -$311M (FY25) and -$265M (1H26), CFO + CFI conversion was 35-41%, and inventory days lengthened. The cash-flow half of the claim is PARTLY SUPPORTED, with the caveat that classification explains much of the CFO shortfall (Door 1) |
| 6 | Iran: FTAI-packaged CFM56 equipment at Sorena Turbine, Tehran (Muddy Waters, early March 2025, via Asianet/Benzinga) | I found no response | No sanctions matter disclosed in the 10-K, 10-Qs or Item 3 ("not expected to have a material adverse effect"). OPEN: no regulator action found, no disproof either |
| 7 | Auditor and governance flags (not in the reports, but follow-on) | EY dismissed 2025-06-17, KPMG hired, "no disagreements" (8-K Item 4.01, 2025-06-24) | KPMG's FY25 opinion is clean. CFO Eun Nam resigned 2026-03-03, five days after the 10-K (8-K 2026-03-06), succeeded by a 36-year-old FP&A head. Both are disclosed as unrelated to accounting disagreements. Neutral to mildly negative |

28. Litigation. The FY25 10-K Item 3 does not mention the January 2025 securities class actions that plaintiff firms advertised (Kaplan Fox, Glancy Prongay, Hagens Berman). I could not confirm status through court dockets (PACER is not publicly searchable without account). OPEN.

---

## (B) Revised variant hypotheses

The screen's H1 was "EBITDA is not cash; growth is financed by debt and SCI proceeds." The trail shows the first clause is half right and the second is wrong. Revised hypotheses:

**H1-revised (Short, primary): "Reported conversion hides a funding model that is running out, on a definition that moves."**
Statement: Cash conversion measured as CFO + CFI is 35% of EBITDA for FY25 and 41% for 1H26 (32% in Q2-26), versus management's "60-70%"; the 2026 FCF guide needs about $625M in 2H26 versus about $95M in Q2; the cash has been supplied by selling the leasing book (which fell $400M in six months and is being replaced by 19%-owned affiliate structures), while the FY25 headline ($724M) cannot be reconciled to CFO + CFI without a roughly $311M add-back that 2026 does not use.
- For: 10-K Note 2 cash-flow presentation; bridge in section C; Q2-26 1H EBITDA flat at $617M; 2H26 FCF back-loading; 40% of EBITDA from gains/insurance (Door 1, step 7); company stopped reconciling Adjusted FCF in releases after Q2-25; CFO departure; revolver now secured by inventory.
- Against: debt is flat at $3.45B, 2.9x leverage with no maturity before May 2028 and a $2.0B undrawn revolver; if you give credit for inventory-sourced CFI proceeds, conversion is 63% (FY25), in line with peers; the 2026 definition does tie; negative CFO is largely a classification effect; Q1-Q3 timing can swing.
- Needed to confirm: Q3-26 FCF versus the implied ramp; the IR-deck reconciliation of $724M.

**H2-revised (Short, secondary): "Aerospace growth is volume, margins are walking down, and related-party revenue flatters the volume."**
- For: margin 35.9% (Q1-25) to 28.5% (Q2-26); EBITDA per module down about 6% y/y while revenue per module up about 11%; the 40% 2026 target became "around 30% for 1-2 years"; MRE sales to the 19%-owned SCI vehicle were 25% of segment revenue in 1H26 with 81% of that profit recognized at once; inventory days up from 186 to 221.
- Against: mix explanation is plausible and documented (performance-restoration work earns lower percentage but similar dollars); Aerospace EBITDA is still +51% y/y; GE says the used-material shortage persists; share gain from 12% to 14% (secondary).
- Needed: margin on MRE contract revenue; Q3 module count and EBITDA per module.

**H3-revised (Neutral/Long option, not a Short driver): "The Power guide is largely the one PO; the upside is unpriced only if you believe a second customer."**
- For (long): the $1.465B PO is milestone-based with an advance payment; hyperscaler and lead-time scarcity (GE Vernova backlog 116 GW; Siemens near 70 GW); $450-750M range; implied about 59 units at $1.0M/MW means $450M is roughly this PO.
- Against: the PO sits in a JV with Chinese-listed Jereh, FTAI's economics unknown; first unit not yet delivered (Q4-26 target); possible policy risk; customer unnamed; ProEnergy and GE Vernova compete for the same customers; GE itself sees aeroderivatives as a sink for CFM56 retirements, which implies feedstock competition with FTAI's own Aerospace business (about 100 Power cores plus 400 engine-equivalents of modules against 250-400 retirements a year).
- Because the Power risk can reprice the stock upward in the 12-month window, it is the main threat to the Short, and is why conviction is capped.

**H4-revised (Dropped as a driver): "CFM56 peak shop-visit timing."** GE and Safran both indicate elevated shop visits through 2027-28; LEAP is no longer propping up the CFM56 fleet through problems; nothing in the next 12 months. Use as a risk, not a catalyst.

**H5 (New, Event-driven): "The Q3-26 10-Q is a double test."** (i) Customer deposits and J&F accounting after the PO; (ii) 2H26 FCF ramp versus guide; (iii) any change in how Adjusted FCF is defined. These can be read directly from filings once published (date UNVERIFIED, expected late Oct/early Nov 2026, i.e. possibly after the competition deadline).

Net view: Short, conviction 2 of 5 (capped by Power upside and by balance-sheet strength). The defensible pitch is the specific "conversion 35-41% versus 60-70% claimed, moving FCF definition, back-loaded guide, margin walk-back, related-party revenue" and not "negative CFO".

---

## (C) Data tables

All sources: EDGAR statements of cash flows (10-K FY25, 10-Q Q1-25, Q2-25 [via XBRL], Q3-25, Q1-26, Q2-26) and the "Cash Flow Presentation" note. $M. Quarterly values are differences of year-to-date values. CSVs saved alongside.

### C1. CFO and Adjusted-FCF bridge by quarter (cfo_fcf_bridge_quarterly.csv)

| Quarter | CFO | CFI | CFO+CFI | Adj. EBITDA | CFO+CFI % EBITDA | Inventory-sourced sale proceeds in CFI | CFO + that | % EBITDA | Engine/aircraft inventory purchases (in CFO) |
|---|---|---|---|---|---|---|---|---|---|
| Q1-25 | -26.0 | -27.6 | -53.6 | 268.6 | -20% | 145.4 | 119.5 | 44% | 15.8 |
| Q2-25 | -110.3 | 523.8 | 413.5 | 347.8 | 119% | 270.0 | 159.6 | 46% | 9.9 |
| Q3-25 | 4.6 | 226.5 | 231.1 | 297.4 | 78% | 220.4 | 225.1 | 76% | 101.5 |
| Q4-25 | -179.1 | 0.6 | -178.4 | 277.2 | -64% | 423.1 | 244.0 | 88% | 197.8 |
| Q1-26 | -160.1 | 317.0 | 156.9 | 325.6 | 48% | 280.7 | 120.6 | 37% | 156.3 |
| Q2-26 | -105.2 | 198.7 | 93.5 | 291.4 | 32% | 257.8 | 152.5 | 52% | 200.3 |

Company-quoted Adjusted FCF for comparison: Q2-25 about $423.5M (reconciled in release: CFO -110.3 + CFI 523.8 + JV 10.0); Q1-26 $158M; 1H26 $255M (call, secondary); FY25 $724M (call, secondary; reconciliation not found).

### C2. Annual and 1H26 view (cfo_fcf_bridge_annual.csv)

| Period | CFO | CFI | CFO+CFI | Adj. EBITDA | % | Inventory-sourced sale proceeds in CFI | CFO + that | % | Total asset-sale proceeds in CFI | Acquisition of leasing equipment |
|---|---|---|---|---|---|---|---|---|---|---|
| 2023 | 129.0 | -373.3 | -244.4 | 597.3 | -41% | 79.5 | 208.5 | 35% | 477.9 | 749.8 |
| 2024 | -188.0 | -469.5 | -657.5 | 862.1 | -76% | 436.2 | 248.3 | 29% | 969.3 | 1,147.3 |
| 2025 | -310.7 | 723.3 | 412.6 | 1,190.9 | 35% | 1,059.0 | 748.2 | 63% | 1,712.5 | 658.8 |
| 1H26 | -265.3 | 515.7 | 250.4 | 617.0 | 41% | 538.4 | 273.1 | 44% | 793.0 | 163.1 |

Reconciliation of the FY25 gap: reported $724M less CFO + CFI $412.6M = $311.4M. Reconstruction (a): net investment in unconsolidated entities 301.4 + QuickTurn Europe 10.0 = 311.4. Reconstruction (b): Q4 growth items 252 + QuickTurn 10.0 + business acquisition 49.1 = 311.1. Neither is confirmed.

### C3. Where the cash lines land (FY25 10-K, Note 2 "Cash Flow Presentation")

| Item | FY23 | FY24 | FY25 | 1H25 | 1H26 | Cash-flow section |
|---|---|---|---|---|---|---|
| Manufacturing outflows (new inventory, capitalized labor) | -138.0 | -345.8 | -779.4 | -314.0 | -511.2 | Operating |
| Engine and aircraft inventory purchased from third parties | 0 | -8.3 | -325.1 | -25.7 | -356.7 | Operating |
| Cash from assets sold sourced from leasing equipment | 94.2 | 76.2 | 61.5 | 43.0 | 18.9 | Operating |
| Sales of leasing equipment containing components from inventory | 79.5 | 436.2 | 1,059.0 | 415.4 | 538.4 | Investing |
| Sales of seed aircraft to 2025 Partnership | 0 | 0 | 530.0 | 397.1 | 175.7 | Investing |
| Acquisition of leasing equipment | -749.8 | -1,147.3 | -658.8 | -412.1 | -163.1 | Investing |
| Investment in unconsolidated entities (SCI etc.) | -19.5 | 0 | -328.5 | -118.7 | -99.3 | Investing |
| Insurance proceeds (Russia) | 0 | 0 | 54.3 | 54.3 | 48.3 | Investing |
| Gain on sale of assets (deducted in CFO) | -160.7 | -377.9 | -377.5 | -226.1 | -177.9 | Operating (non-cash adjustment) |

### C4. Gains versus EBITDA (gains_vs_ebitda.csv)

| Period | Gain on sale of assets | Gain on sale to Partnership | Insurance gain | Total as % of total Adj. EBITDA | Gain on sale of assets as % of Aerospace EBITDA (upper bound) |
|---|---|---|---|---|---|
| FY24 | 377.9 | 0 | 0 | 44% | 99% |
| FY25 | 377.5 | 46.4 | 54.3 | 40% | 56% |
| 1H25 | 226.1 | 45.5 | 54.3 | 53% | 76% |
| 1H26 | 177.9 | 17.6 | 49.5 | 40% | 38% |

### C5. Inventory (inventory_composition.csv)

| Quarter end | Inventory, net | QoQ change | CFO inventory outflow (quarter) | Of which engine/aircraft purchases | Paid-engine share |
|---|---|---|---|---|---|
| 2024-12-31 | 551.2 | | | | |
| 2025-03-31 | 645.2 | +94.0 | 127.2 | 15.8 | 12% |
| 2025-06-30 | 752.9 | +107.7 | 141.6 | 9.9 | 7% |
| 2025-09-30 | 897.2 | +144.4 | 123.1 | 101.5 | 82% |
| 2025-12-31 | 1,193.8 | +296.6 | 253.6 | 197.8 | 78% |
| 2026-03-31 | 1,364.3 | +170.5 | 186.9 | 156.3 | 84% |
| 2026-06-30 | 1,544.6 | +180.3 | 266.2 | 200.3 | 75% |

Composition by category (engines / modules / PMA parts / Power units): not disclosed in the 10-K or 10-Qs (DEAD END). Management-cited fragments (secondary): Q4-25 additions included about $150M Power inventory and $50M hot-section parts. Other signals: prepaid expenses including prepayments for maintenance not yet incurred rose from $79.8M (12/31/25) to $196.6M (6/30/26) in other current assets, and the balance sheet shows leasing equipment net down $399M over the same period.

### C6. Aerospace margin and mix (aerospace_margin_quarterly.csv)

| Quarter | Segment revenue | Products | MRE (to 19%-owned SCI) | MRE % | Adj. EBITDA | Margin | Modules | EBITDA / module ($M) |
|---|---|---|---|---|---|---|---|---|
| Q1-25 | 365.0 | 264.4 | 100.6 | 27.6% | 131.0 | 35.9% | n/a | n/a |
| Q2-25 | 490.3 | 420.7 | 69.6 | 14.2% | 164.9 | 33.6% | 184 (derived) | 0.90 |
| Q3-25 | 517.9 | 459.2 | 58.7 | 11.3% | 180.4 | 34.8% | n/a | n/a |
| Q4-25 | 563.0 | 456.1 | 106.9 | 19.0% | 195.0 | 34.6% | 228 | 0.86 |
| Q1-26 | 743.8 | 522.6 | 221.2 | 29.7% | 222.6 | 29.9% | n/a | n/a |
| Q2-26 | 875.0 | 692.2 | 182.8 | 20.9% | 249.7 | 28.5% | 296 | 0.84 |

### C7. Debt maturities (debt_schedule.csv)

| Instrument | Face $M | Coupon | Maturity | Annual interest $M |
|---|---|---|---|---|
| Revolver ($2.025B, undrawn; first lien on non-aircraft assets) | 0 | SOFR + 1.25-2.00% | 2031-04-24 | commitment fee 0.15-0.30% |
| Senior Notes 2028 | 1,000 | 5.50% | 2028-05-01 | 55.0 |
| Senior Notes 2030 | 500 | 7.875% | 2030-12-01 | 39.4 |
| Senior Notes 2031 | 700 | 7.00% | 2031-05-01 | 49.0 |
| Senior Notes 2032 | 800 | 7.00% | 2032-06-15 | 56.0 |
| Senior Notes 2033 | 500 | 5.875% | 2033-04-15 | 29.4 |
| Total | 3,500 | about 6.5% | | 228.8 (10-K) |

Covenants: interest coverage at least 3.0x; debt/EBITDA at most 4.0x (8-K 2026-04-30). Equity $404.0M; cash $337.2M (6/30/26).

### C8. Power implied units (power_implied_units.csv; assumptions UNVERIFIED)

| $M per MW (assumed) | MW per unit | Implied units from $1.465B | Implied GW | At $7.5M EBITDA per unit |
|---|---|---|---|---|
| 1.0 | 25 | 58.6 | 1.47 | $440M |
| 1.2 | 25 | 48.8 | 1.22 | $366M |
| 1.5 | 25 | 39.1 | 0.98 | $293M |

---

## (D) Phase-2 to-do list

Highest value first.

1. Obtain the Q4-25 and Q2-26 earnings presentations (company IR page, https://ir.ftaiaviation.com/ or the Investor Center; the site timed out from this environment) and find the Adjusted FCF reconciliation. Resolve the $311M FY25 gap and confirm whether the metric adds back SCI equity.
2. Read Jereh's Shenzhen exchange announcement (stock code 002353; cninfo.com.cn) and Jereh's annual or interim report for the J&F Power Systems ownership split, consolidation method, unit count and delivery schedule. Check whether J&F is equity-accounted in FTAI's books once the Q3-26 10-Q is filed.
3. Wait for and read the Q3-26 10-Q (due late Oct or early Nov 2026, date not verified): customer deposits/advances, any Note on J&F, segment note for FTAI Power, inventory roll-forward, Adjusted FCF versus the $625M 2H26 requirement.
4. Pull the full text of the Q2-26 and Q4-25 calls from a free full-transcript source and confirm the quotes used here (module margin example, "around 30% for 1-2 years", 60-70% conversion, Power unit economics, $35M SCI fees). Everything marked secondary needs this.
5. Obtain the primary Muddy Waters (2025-01-15) and Snowcap (2025-01-29) reports from the firms' sites or archive.org, list each claim verbatim, and test the "80% from gains" claim using FTAI's FY24 10-K segment note.
6. Find the Limited Partnership terms of the 2025 SPV (any exhibit in an S-4/prospectus for the 2026 ABS "MRE 2026" bond issue, or Form ADV if any) for management fee, servicing fee, promote hurdle and FTAI's share of carry; test whether the $35M quarterly SCI line implies a fee rate on SPV AUM.
7. Peer comparison of CFO/EBITDA and CFO+CFI/EBITDA: HEICO, AAR, Willis Lease, AerSale, StandardAero (EDGAR 10-Ks). Ask whether any peer books engine-sale proceeds in investing.
8. Estimate global CFM56 core availability: FAA registry (US only), airline 10-K fleet tables, plus public retirement counts, to size Power plus Aerospace demand against supply; check the Aviation Week (Sep 22, 2026) piece for date and numbers.
9. Check the status of the January 2025 securities class actions (court docket search via free sources such as CourtListener) and any SEC or DOJ inquiries; confirm whether the 10-K should disclose them.
10. Verify the Iran allegation follow-up (any OFAC or BIS action; FTAI response in 10-Q risk factors).
11. Confirm the price, 52-week range and share count from a primary exchange feed; resolve the P/E discrepancy; pull FINRA short interest.
12. Test aerospace margin pricing: AerSale and StandardAero 10-Q commentary on CFM56 module and used serviceable material pricing; GE Aerospace and Safran spare-parts price commentary.
13. Model: three-statement scenario bridge to the 2027 guide ($1.4B Aerospace, $450M Power, $450M Leasing) with a CFO + CFI line, tying 2H26 FCF to the guide, and a Power case with and without the JV share.
