# GenAI Log 01: Ticker Screening (2026-10-06)

**Tools:** Claude Code (Opus 5.5 orchestrator) running 4 parallel Claude Sonnet 5.5 research agents with web search/fetch.
**Objective:** Screen PHVS, NBIS, DKS and FTAI. For each ticker, find the contested questions about the economics that public data could settle.
**Method:**
- Each ticker used one shared prompt template plus ticker-specific starting hints. Agents were told those hints come from model memory, may be stale, and must be verified live.
- Constraints: public sources only, a source URL and as-of date for every number, and unverified claims flagged.
- Output: a full write-up in `research/<TICKER>/screen.md` and a scorecard of 250 words or less.

**Scorecard dimensions (1–5):**
- debate that public data can settle
- original-data potential
- modelability
- dated 12-month catalyst
- un-crowdedness

**Bias mitigation planned:**
- The orchestrator challenges weak claims.
- Key numbers are re-verified against EDGAR/IR.
- Each agent's "obvious narrative" section is kept as the GenAI baseline that the team's thesis must beat.

## Responses / evaluation

**PHVS screen: 19/25.**
- Ekterly launch is decelerating against KalVista's own 14D9 forecast.
- Intellia's CRISPR PDUFA (3/10/27) comes before PHVS's (4/23/27).
- Form 144 cluster in September.
- Orchestrator note: the team has no bio background, so Q&A defensibility is lower.

**FTAI screen: 16/25.**
- *GenAI error caught.* The orchestrator's prompt hint named "Hunterbrook" as the Jan 2025 short seller. The agent's live search corrected this to **Muddy Waters and Snowcap**. Example of a hallucination in the prompt fixed by primary-source checking.
- *Orchestrator verification (SEC XBRL companyfacts, CIK 0001590364, pulled 2026-10-06):*
  - GAAP CFO: FY24 -$188.0M, FY25 -$310.7M, 1H26 -$265.3M.
  - Inventory: $551M (12/24) → $1,545M (6/26).
  - Stockholders' equity: $404M (6/26).
  - These match the agent's figures.

**FTAI trail.** View: Short, conviction 2/5. Output: `research/FTAI/trail.md` plus CSVs.

What the agent found:
- **Negative CFO is mostly classification.** Proceeds from rebuilt-engine sales are booked in investing CF, while their costs sit in operating CF.
- **Real cash conversion is weak.** CFO+CFI ran 35% of EBITDA in FY25 and 41% in 1H26, against management's "60–70%".
- **FCF does not reconcile.** FY25 "Adjusted FCF" of $724M is $311M higher than CFO+CFI ($413M). Status: OPEN.
- **Related-party revenue.** About 25% of Aerospace revenue is sold to the 19%-owned off-balance-sheet SCI vehicle.
- **Margins are compressing.** Aerospace margin fell from 35.9% to 28.5%.
- **Power PO counterparty.** The $1.465B Power PO sits with the J&F JV (Jereh, 002353.SZ).

Orchestrator verification (XBRL):
- `ProceedsFromSaleOfOtherProductiveAssets` (investing) = $969M in FY24, which confirms the classification mechanism.
- `GainLossOnSaleOfOtherAssets` = $378M in both FY24 and FY25.
- I could not find an FY25 proceeds tag in the standard taxonomy, so the agent's $1.06B is only partially verified.

**DKS screen + trail: 18/25.**
- Agent's findings:
  - 31% one-day drop on 8/25/26 after the FY26 EPS guide was cut to $11–12.
  - Foot Locker segment guide went from +$100–150M to -$80 to -$40M.
  - Derived Foot Locker inventory is about $1.96B, up 14–15% y/y.
  - $1.0B of bonds issued 9/22.
  - Insiders bought about $5.6M of stock after the cut.
- Orchestrator verification (XBRL): consolidated inventory $5,565M (8/1/26) vs $3,404M (8/2/25); 1H CFO $792M.
- Orchestrator view: the bear case is crowded after the crash. The best hypothesis is closer to an estimate call than a business insight.

**NBIS screen + trail: 18/25.**
- Agent's findings:
  - RPO of $37.5B, with 36% recognized within 24 months.
  - On the agent's timing assumption, that supports about $6–8B of 2027 revenue against $12.3B consensus.
  - Vineland, NJ (likely the Microsoft site) has had permit trouble.
- Orchestrator verification: the Q2 6-K exhibit 99.2 states verbatim "unsatisfied RPO was $37,490.6 [M], of which 36% is expected to be recognized as revenue during the 24 months ending June 30, 2028, 40% between months 25 and 48".
- Orchestrator caveats:
  - RPO excludes contracts of 1 year or less, so short-term and on-demand revenue sits outside it.
  - Bookings signed after 6/30 also add to it.
  - The size of the gap therefore depends on the non-RPO revenue run-rate, which is an OPEN question.

**PHVS trail. View flipped from Short/avoid (screen) to Long, conviction 2/5.**

What the trail found:
- **Ekterly revenue was overstated in the screen.** Q1 product revenue was $39.2M; the screen's $40.9M included $1.7M of partnership revenue.
- **Ekterly demand looks flat.** Start-form adds are flat at about 44 a week.
- **The oral drug is taking share, not growing the market.** In CMS Part D and Medicaid data, Ekterly claims rose almost one-for-one as generic icatibant claims fell.
- **Insider selling was mostly not pre-planned.** Only 12% of the 857K shares sold carried the 10b5-1 flag. A 600K-share block went at $35.00 on 9/17.
- **The price drop looks sector-wide.** BCRX fell 20% and IONS 24% over the same window, against XBI down 8%.
- **The real value driver is prophylaxis.** CHAPTER-3 showed 87% attack reduction in type 1/2 patients versus about 44% for Orladeyo (cross-trial comparison).

*Good candidate for the appendix "how conclusion changed" example: the first-pass Short thesis did not survive primary-data checks.*

## Orchestrator tie-break checks (2026-10-06)

### FTAI: what explains the $311M gap between "Adjusted FCF" and CFO+CFI?
Source: FY25 10-K cash flow statement (EDGAR, accession 0001628280-26-012940).

**Cash flow statement, FY25:**
- CFO: -$310.7M
- CFI: +$723.3M
- CFO+CFI: $412.6M, against $724M of reported "Adjusted FCF"

**Investing lines that matter:**
- Investment in unconsolidated entities (the SCI 2025 Partnership): -$328.5M
- Return of capital from that entity: +$27.1M
- Proceeds from sale of assets: $1,182.5M
- Proceeds from sale of assets *to the 2025 Partnership*: $530.0M

**Gains on sale inside net income:**
- $377.5M on sales of assets
- $46.4M on sales to the Partnership

**Inventory build:** -$645.5M

**What the 10-K says about the SCI 2025 Partnership:**
- It is "the primary buyer of all future on-lease 737NG and A320ceo aircraft".
- FTAI's MRE business "exclusively provides replacement aircraft engines and modules for the life of the partnership".
- FTAI holds a minority equity stake and earns management fees.

**Inference.** The gap is about the size of FTAI's cash investment in the vehicle that buys its assets. This is not yet confirmed: the IR deck that defines Adjusted FCF timed out, so the definition is still OPEN.

### NBIS: does the RPO gap thesis hold?
**What weakens it:**
- The Meta deal (3/16/26) is $12B of dedicated capacity *plus up to $15B* of optional additional purchases. The optional part is likely outside RPO.
- News reports say management deliberately keeps 2027 capacity uncommitted so it can sell at spot prices.
- Free "consensus" for 2027 revenue ranges from $2.4B to $12.3B depending on the aggregator, which is too unreliable to anchor a gap.

**What is new:**
- AIB 50MW, 12-year contract (9/30/26).

**Verdict.** An RPO shortfall reflects management's chosen strategy, not a hidden flaw. Thesis downgraded.

**Process issue.** Sending a mid-run method update to running agents triggered API safeguard false positives, and all 4 terminated. The NBIS and DKS screens were lost before saving. Fix: relaunch fresh agents with the method in the original prompt, and save progressively.

**Method change (user direction).** Use a lead-following "investigation trail": search A → find B and C → chase each → narrative log with each door marked CLOSED, DEAD END or OPEN. Trail files are `research/<TICKER>/trail.md`, or section 9 of `screen.md`.

## Stress tests: Phase 1.5 (smoke tests and ablation)

**NBIS: NOT VIABLE.** Best thesis T1 (capacity delivery): PT $185–225, gap -19%, P = 35%, expected alpha about -9%.
- No thesis cleared both bars: a value gap of at least 20% and evidence strength of at least 3.
- Most of the value gap comes from the multiple (NBIS at about 10x EBITDA vs CoreWeave at about 6.1x), not from a business insight.

*GenAI error caught (2nd instance).* The orchestrator's prompt said NBIS depreciates GPUs over 6 years. The agent found the Q2 6-K says servers were "extended from four to five years", effective 1/1/26. The orchestrator re-verified the quote in the 6-K. Six years is CoreWeave's policy, and the prompt had conflated the two peers.

**DKS: NOT VIABLE.** Best thesis T2 (weak Long): PT $144–171, P = 40%, expected alpha about -5.6%. The value comes from the core multiple, and both the Long and the Foot Locker bear case are crowded (mean PT $158).

*Earlier screen claim falsified.* The DKS screen said Foot Locker's inventory build last year was "+$61M". The stress test found Foot Locker's Feb 2025 inventory was $1,525M, which makes the prior-year build +$184M. This year's build of about +$430M also comes off a base reduced by a $218M write-down. The "inventory blowout" signal is much weaker than first reported. This is self-correction across agent passes.

**PHVS: NOT VIABLE.** Best thesis: a narrowed T2 (Avoid or small Short). PT $22–27, P = 55%, expected alpha about -4.2%.

*The stress test reversed the Long view from the trail.*
- A reverse DCF shows the EV already implies about $1.14B of unrisked peak sales.
- On-demand alone would need $886M, which is more than KalVista's own $705M plan for Ekterly.
- So the price already includes prophylaxis success, and T1's premise (that the market prices PHVS as an on-demand-only story) fails.

*Model sensitivity.* Margin and ex-US inputs are unsourced. Changing them moves the base value from $21.5 to $28.1.

**FTAI stress test.** The agent's verdict: not viable as a Short (thesis value $198 vs a $179 price).
- What passed:
  - Gains on sale are 44% / 40% / 40% of Adjusted EBITDA (FY24 / FY25 / 1H26).
  - 2025 Partnership revenue is $335.8M in FY25 (17.3% of Aerospace) and $404.0M in 1H26 (25.0%).
  - Aerospace margin fell from 35.9% to 28.5%.
- What failed: S1, as originally framed (the FCF definition excludes SCI).

**Orchestrator resolution of the FY25 FCF gap.** Source: Q4'25 call transcript (fool.com, 2/26/26).
- The CFO said the $724M was "further adjusted for 3 key investments" made in Q4: a $52M increase in SCI co-investment, $150M of FTAI Power turbines, and $50M of hot-section parts. These total $252M.
- That $252M plus about $59M of acquisitions closes the $311M gap to CFO+CFI. This matches the trail agent's "reconstruction (b)".
- An earlier hypothesis (from the advisor/orchestrator) was that the gap equals the SCI investment. That matched on a nearby number and was WRONG. It was corrected via primary source.
- Sharper finding: management's headline FCF adds back about $200M of inventory-type purchases (turbines and parts), labelled "growth investments". These are the same items that drive negative GAAP CFO.

**Valuation check (orchestrator, approximate; peer multiples still to verify).**
- EV is $21.6B. The 2026 EBITDA guide is about $1,525M (Aerospace $1,050M + Leasing $475M).
- Headline multiple is about 14x. Excluding gains (about 40%), it is about 24x.
- On the 2027 guide of $2.3B (including Power $450M), the multiple is 9.4x.
- The direction therefore hinges on how credible the 2027 guide is.

## Phase 2 (FTAI)

**Agent C: engine economics and comps.**

Market and share:
- CFM56 shop visits plateau at about 2,400 a year through 2027–28 (GE CFO, quoted in Aviation Week, 9/22/26).
- FTAI's 2026 guide of 1,200 modules equals about 400 engine-equivalents, a 14–17% share.

Supply is the binding constraint:
- The constraint is engine cores, not capacity or demand.
- Retirements supply about 210–560 engines a year. FTAI needs about 600, plus about 100 for Power. *Retirement figures still to be verified.*
- Inventory runs about 222 days, and inventory has grown 3.8x since FY23 against 2.7x for cost of sales.
- The PMAs are held by Chromalloy, not FTAI.

Cash conversion and valuation:
- 3-year CFO/EBITDA is -14% for FTAI, against 69% for HEICO and 25% for StandardAero.
- At $179.44, FTAI trades at about 23.6x 2026 EBITDA excluding gains, which is a franchise multiple.
- The peer multiples are revenue-scaled proxies.

**Emerging candidate insight:** FTAI's growth is constrained by feedstock. Aerospace and Power compete for the same retiring CFM56 cores. That would explain both the margin compression and the inventory build.

**Agent A: 2027 guide credibility.** Our 2027 EBITDA estimates, against the $2.3B guide:

| Case | 2027 EBITDA | Implied EV/EBITDA |
|---|---|---|
| Bear | $1.47B | 14.7x |
| Base | $1.92B | 11.2x |
| Bull | $2.48B | 8.7x |

The guide sits near our bull case. Conviction that the guide is a stretch: 3/5.

**FTAI Power structure.**
- Jereh's 1H26 report (cninfo, 8/14/26) calls J&F a "控股子公司" (controlled subsidiary) and consolidates it.
- FTAI equity-accounts J&F (per a secondary source, the Q2 call).
- Jereh appears in only one FTAI filing.
- **Emerging pattern:** both of FTAI's growth engines run through affiliates it does not control. SCI buys aircraft and modules. J&F holds the Power PO. *To verify:* the J&F ownership split and how FTAI books Power revenue.

**Agent D: adversarial review.** Agent's lean: Long, 2/5. The key finding is that the "engine-trading, not franchise" framing **is a rehash**: the Muddy Waters primary PDF (1/15/25, slide 22) already made the trading, margin and CFO-classification points. *An important differentiation check, without which the pitch would have repeated MW.*

What is NEW since MW and Snowcap:
1. **The SCI I seed pipeline is exhausted.** Note 10 says all committed aircraft were sold by 6/30/26. Excluding the seed sales, 1H26 CFO+CFI was about $75M of the $250M. The 2H26 FCF ramp (about $623M needed) has to come without those proceeds.
2. **SCI related-party revenue** started after both short reports.
3. **Core-supply constraint** (from agent C).
4. **The J&F affiliate structure for Power** (from agent A).

Agent D marked the FY25 $724M as unreconciled. The orchestrator had already reconciled it from the Q4 call: $252M of Q4 "growth investments" plus about $59M of acquisitions.

Red flags:
- The CFO resigned in March 2026.
- KPMG is a first-year auditor.
- A director (Tuchman) sold about $61.5M at about $241 in May.
- An SDNY class action (25-cv-00541) is unnamed in the 10-K.

Data conflict: "down 44% from high" (agent D) versus a $227 high in Aug 2026 (screen). Resolve with agent B's price data.

**Orchestrator verification: Q2'26 10-Q** (EDGAR 0001628280-26-051412, filed 7/31/26)

Seed sales to the 2025 Partnership:
- Q2'26: 6 aircraft for a $2.5M gain. 1H26: 15 aircraft for a $17.6M gain.
- Same periods in 2025: 33 aircraft ($34.6M gain) and 37 aircraft ($45.5M gain).
- Filing language: these sales "were non-recurring in nature and not considered part of the Company's ordinary activities."
- The 10-Q does not explicitly state that "all seed sold". The trend shows the program winding down.

Aerospace revenue:
- Up $113.2M, "primarily due to an increase in engine and module sales made to the 2025 Partnership."
- Profit elimination on sales to the Partnership was -$16.6M in 1H26.

1H26 cash flow:
- CFO -$265.3M and CFI +$515.7M, so CFO+CFI = $250.4M.
- That includes $175.7M of seed-sale proceeds and $48.3M of Russia insurance proceeds.
- Excluding both, the remainder is about $26M. The FY26 FCF guide is $878M.

## Thesis v0.2 review (orchestrator + advisor)

**Valuation errors fixed:**
- *Inconsistent multiples:* the bear case used 12x while the "trader" case used 10x.
- *No basis for the 10x:* AerSale actually trades at 17.4x TTM, so the "trader" multiple has no peer support.
- *Leasing capitalized on gains:* Leasing EBITDA, which is mostly gains on sales, had been valued on a multiple. It is now valued at book.

**Verified in the Q2'26 10-Q:**
- Adjusted EBITDA includes FTAI's pro-rata share of EBITDA from unconsolidated entities.
- So Power JV EBITDA and 19% of SCI's lease EBITDA sit inside FTAI's EBITDA. Cash arrives only through distributions ($27.1M in FY25). This point is new relative to the Muddy Waters report.

**Insider check:** the four Form 4s filed 9/17 are routine director grants at $0. No insider buying.

**Result:**
- Street mean PT is about $330. Our range is $142–185, a strong variant view against consensus.
- Against the $179 price, a Short is marginal:
  - SOTP base is about $172. Probability-weighted value is about $177–185.
  - Forward P/E method gives $142–160.
  - The bull tail is about +56%.
- Direction stays UNDECIDED until the model computes EPS under our base case.
- *Appendix lesson:* the first valuation pass "manufactured" downside using an unsupported multiple. A review caught it, and the call was not stretched to fit.

## Model v1 (Sonnet agent) and orchestrator review
- The agent built the model from the spec: 10 tabs, 86 tie-outs passing, built from a blank Workbook().
- The orchestrator found that its own spec had left corporate costs (about $160M a year) out of the SOTP. This was fixed in v1.1.
- Result: the Mgmt Guide scenario is worth about $183, roughly the $179 price. Our base case is $144 (−20%), the bear case $91 and the bull case $220.
- **The call firms to SHORT, PT about $145.**
- Insight for the deck: "the price already embeds full guide delivery".

## Gap closure
- Both gap agents hit the usage limit with nothing saved. For the remaining work, the orchestrator did the EDGAR lookups itself (cheaper) and relaunched only the Power JV agent, with a hard budget of 25 calls and a save after the first 5.
- Resolved items:
  - The Leasing $35M is $7.0M of fees plus $28.0M of pro-rata SCI EBITDA.
  - In 1H26, SCI produced $48.3M of EBITDA counted by FTAI, against $19.2M of cash distributions and $99.3M of new investment.
  - The $500M buyback (9/15/26) is funded "from balance-sheet cash", which was $337M.
- **Power JV agent result:** verified via the CFO's Q2 call quote that FTAI books revenue/COGS on turbine sales *to the JV*. That makes Power a third affiliate channel. Ownership %, unit price and per-unit EBITDA are undisclosed ("commercially sensitive"). The model's Power inputs are kept and labeled as assumptions.

**Retraction (advisor review).**
- The earlier figure "SCI net cash about −$80M vs $48.3M of EBITDA" was misframed. It subtracted FTAI's own $99.3M capital call, which is an investment, not lost cash.
- It is replaced by the proportional-debt point. SCI I has about $6.0B of capital on $2.0B of equity, so about $4B of debt, and FTAI's 19% share is about $760M. That debt is not in FTAI's EV, while 19% of SCI's EBITDA is in FTAI's Adjusted EBITDA. This figure is inferred: the financing is not disclosed in FTAI's filings.
- Thesis rewritten as one consistent document (v1.0). The old draft is archived.
