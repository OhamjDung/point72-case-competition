# FTAI Aviation: Is the 2027 Adjusted EBITDA Guide of $2.3B Credible?

Prepared 2026-10-06 for the Point72 Academy pitch (due 2026-10-12). Public sources only. This note builds on `trail.md` and `stress_test.md` and does not repeat them. The segment build is in `A_2027_guide_segment_build.csv`. Items marked [UNVERIFIED] could not be tied to a primary source. "Secondary" means a transcript or news summary rather than the filing itself.

Bottom line: the $2.3B guide sits at roughly my bull case. My base case is $1.92B, about 17% below guide, and my bear case is $1.47B. At a $21.6B EV the guide is 9.4x; my base is 11.2x and my bear is 14.7x. Aerospace is the most credible piece, Power is the least verifiable, and Leasing is guided at the top of what the run-rate supports.

---

## (1) Investigation Trail

### Thread 1. FTAI Power ($450M)

**Door 1.1. Who owns J&F Power Systems and who consolidates it. CLOSED on consolidation; OPEN on the percentage split.**

1. I started with Jereh's Shenzhen disclosures (code 002353). The July 2026 contract announcement (Jereh notice 2026-048, reported by 10jqka, cls.cn, Eastmoney and Sina on 2026-07-22) calls J&F Power Systems LLC a "控股子公司" (controlled subsidiary) of Jereh. Example: https://stock.10jqka.com.cn/20260723/c678378497.shtml (2026-07-23). I could not retrieve the cninfo PDF of the notice itself, so this rests on press reproductions that agree with each other.
2. This opened a second door, Jereh's 2026 half-year report (cninfo, filed 2026-08-14, http://static.cninfo.com.cn/finalpage/2026-08-14/1225472540.PDF, which I downloaded and text-searched). It lists "J&F POWER SYSTEM LLC" among subsidiaries newly established in the period, with "no significant impact" on results. It also says Jereh signed a "strategic joint-venture agreement" with "FTAI Power, a well-known US aero-engine company". So Jereh fully consolidates J&F.
3. The FTAI side is the opposite. On the Q2-26 call (Investing.com transcript, 2026-07-30, secondary) management described FTAI as receiving revenue and cost of goods sold "when FTAI sells the turbine to the JV" and earning "unconsolidated earnings and other income" from its equity stake. That is equity-method treatment. FTAI's definition of Adjusted EBITDA (Q2-26 8-K, https://www.sec.gov/Archives/edgar/data/1590364/000162828026050622/ftai6302026earningsrelease.htm, 2026-07-29) adds the pro-rata share of unconsolidated entities' Adjusted EBITDA. It also excludes the profit elimination on sales to affiliates (shown in the 10-Q segment note for the 2025 Partnership). If J&F follows the same pattern, FTAI's Power EBITDA is the margin on turbines sold to the JV plus its pro-rata share of JV EBITDA. That is an inference, not a disclosure.
4. Ownership split. EDGAR full-text search (efts.sec.gov, queried 2026-10-06) finds "Jereh" in only one FTAI filing, the Q1-26 earnings release (2026-04-29), which announces a "strategic packaging and distribution joint venture". "J&F Power" appears in no FTAI filing text, so the Q2-26 10-Q does not describe the JV. The Q2-26 10-Q segment note still carries FTAI Power as an expense line in Corporate and Other. A Yicai summary (2026-07-22) read as "50/50", but the page I could fetch does not state a split, and the earlier trail noted the split as undisclosed. [UNVERIFIED]. Combined facts (Jereh consolidates, FTAI equity-accounts) are consistent with Jereh holding a majority or control rights and FTAI a minority or shared stake. Status: consolidation CLOSED; percentage OPEN until the Q3-26 10-Q equity-method note (expected 2026-10-28, per stress_test.md).

Implication: the hyperscaler's prepayment sits at Jereh's consolidated JV, not on FTAI's balance sheet, so it does not fund FTAI's working capital. Jereh's own report shows contract liabilities of only about RMB 2.06B group-wide at 6/30/26, so the JV prepayment was received after period end.

**Door 1.2. The $1.465B purchase order. CLOSED on terms; OPEN on customer and prepayment size.**

1. FTAI release (GlobeNewswire, 2026-07-22, https://www.globenewswire.com/news-release/2026/07/22/3331360/35538/en/ftai-announces-1-465-billion-gas-turbine-generator-set-order-through-j-f-power-systems.html): initial PO of $1.465B under a five-year master agreement, delivery in batches through November 2027, milestone payments starting with an advance payment at signing, performance adjustment capped at 10% of equipment value (the cap is from trail.md; I did not re-read the release). 10% of $1.465B is $146.5M, roughly a third of the $450M Power guide if it fell straight to EBITDA.
2. Jereh's side adds: contract equals 61.33% of Jereh's 2025 audited revenue; there is a price adjustment mechanism ("设有价格调整机制"); risks named are component procurement, performance and delivery acceptance; Jereh has "received the first advance payment" and the order is "progressing normally" (10jqka/cls.cn, 2026-07-22; Sina 2026-09). Prepayment percentage and milestone schedule are not disclosed by either company. [UNVERIFIED]. Jereh told investors on 2026-07-22 that there is no impact on 2026 results and most deliveries fall in 2027 (10jqka investor-meeting record, http://news.10jqka.com.cn/20260722/c678364742.shtml).
3. Customer. FTAI says "a leading U.S. hyperscaler" (call, secondary); Jereh says an international cloud provider; neither names it. Jereh says it has booked about $1.72B from this customer in the last 12 months (press) and, in the half-year report, more than $3.1B (RMB 20.9B) of data-centre turbine orders since November 2025 across "multiple new top-tier customers". Not all of that is FTAI Mod-1 hardware: Jereh lists Siemens Energy, Baker Hughes, Kawasaki and FTAI as turbine partners, and its other US orders ($182M, $301M, $341M, Yicai/tmtpost, 2026) are sold through its wholly owned GenSystems subsidiary, not J&F. The earlier trail treated "Jereh's seventh order" as part of the FTAI story; I would not. DEAD END on identifying the customer (no public source names it).
4. First delivery. The Q4-25 call (Motley Fool transcript, 2026-02-26) says first delivery "in the fourth quarter of this year". After the Q2 call, summaries say commercial launch is still on track for Q4-26 but "prudent to expect Power deliveries in 2027"; the unit is being tested in Miami after Montreal (search summary of Q2 call, 2026-07-30, secondary). I found no news after July confirming or delaying it. Status: OPEN, with the Q3-26 call (2026-10-28) as the test. Deliveries "through November 2027" leave one month of buffer before year-end.

**Door 1.3. Unit economics. CLOSED on what is public; the price is a DEAD END.**

1. Management declined to give price: "commercially sensitive. We're not going to be providing exact numbers" (Q2 call, secondary). Secondary sources say the reference point is about $1M per MW, so about $25M per 25 MW unit, with $7-8M of EBITDA per unit; I could not trace the $7-8M to a primary transcript. [UNVERIFIED]. The Q4-25 call (Motley Fool, 2026-02-26) says Power margin should be "as good or better than margins in our Aerospace Products business", which at 30-35% on $25M gives $7.5-8.75M. A secondary source says the stated aim is $750M to $1B of EBITDA at 100 units, which is the same $7.5-10M per unit. [UNVERIFIED].
2. Units for $450M. At $7.5M per unit, $450M needs 60 units. The $1.465B PO at $1.0M per MW is 59 units (trail.md, power_implied_units.csv); at $1.2-1.3M per MW it is 45-49 units. Management said the guide "does not assume 100 units; it is materially less" and framed $450M as the "bottom end of a $450M to $750M range" (Q2 call). My reading: $450M is roughly this one PO delivered in full inside calendar 2027, not a cushion. The bottom of the range is therefore only conservative if a second PO arrives.
3. Core cost. Management says only that its input cost is one "no one can match" (Q4-25 call). The earlier trail cites a vendor page at $1.2-1.8M for a -5B core [low quality]. A core of that cost against about $25M revenue per unit is not a binding cost; scarcity matters physically, not economically.

**Door 1.4. Competition and demand durability. CLOSED as supportive through 2027; durability beyond 2028 is a judgement.**

Search (Power Engineering, 2026) reports GE Vernova's heavy-duty lead times at about three years and slots tight to 2030; trail.md already collects GE Vernova (29 LM2500XPRESS units to Crusoe), ProEnergy (PE6000 on CF6 cores, 2027 delivery) and Siemens Energy backlog. I could not find public lead-time figures for LM6000, SGT-A35 or FT8 specifically. DEAD END on model-level lead times. The practical conclusion is that FTAI wins on speed, not on a protected technology, and ProEnergy proves the retired-core-to-turbine playbook is copyable. Demand is durable while the power shortage lasts; an AI-capex pause is the main risk to follow-on POs (the bull case).

**Door 1.5. Does Power compete with Aerospace for CFM56 cores? CLOSED: modest, but visible in allocation.**

At 2027 targets Power needs about 100 cores at most; Aerospace targets 1,700 modules (Q2 call, David Moreno: "module production targets for next year of 1,700"), or about 570 engine-equivalents at three modules per engine. Power is therefore about 15% of core demand, and in the guide scenario (about 50-60 units) about 10%. Management said Power takes priority over Aerospace in the sense of "a deliberate shift in allocation" of modules toward third-party customers away from FTAI's own leasing pool (Q2 call, secondary; the wording is ambiguous, and I read it as feedstock being steered away from the leasing book). Q3 evidence of feedstock tightness: FTAI and its 2026 SPV bought 27 737-700 aircraft from WestJet in September 2026, of which FTAI took 10 off-lease aircraft for Aerospace feedstock (search summary, Sept 2026). FTAI also holds 3,000 modules per year of physical capacity against a 1,700 target. Verdict: not a binding constraint for the 2027 guide, but it adds to the engine-supply risk behind the 1,700-module target.

**Door 1.6. US-China angle. CLOSED for public news (nothing found); OPEN as a tail risk.**

I searched for CFIUS, tariff, export-control and congressional items naming Jereh, GenSystems or J&F. I found only generic items: US lawmaker proposals to keep Chinese data-centre technology out of sensitive government systems (Reuters via Investing.com), a DOJ filing in an xAI turbine suit citing national security (DCD, 2026-06-17, about permitting rather than Chinese equipment), and no action naming the JV. Notably, the hyperscaler signed seven orders with Jereh entities despite this, and Jereh's own risk disclosure names component procurement and acceptance, not regulation. Why it still matters: the J&F packaging happens in Jereh facilities in China, North America and Dubai (Jereh half-year report), so a tariff on Chinese-assembled power equipment would hit the JV's margin, and FTAI shares the hit only through its stake. The performance and price-adjustment clauses are the transmission channel. DEAD END on any filed regulatory matter; OPEN as a risk.

### Thread 2. Leasing ($450M in 2027)

**Door 2.1. Gains versus rent. CLOSED.**

1. The Q2-26 call (Investing.com, 2026-07-30; secondary) gives the Q2 breakdown of Leasing EBITDA: $5M insurance recoveries, $48M "balance sheet leasing and gains on sale", $35M "2025 SPV management fees and co-investment returns", total about $88M (a derived sum). Only the $48M mixes rent and gains, and it is not split further.
2. The 10-Q (https://www.sec.gov/Archives/edgar/data/1590364/000162828026051412/ftai-20260630.htm, 2026-07-31) gives the rent base: lease income of $27.8M in Q2-26 ($67.7M 1H26) versus $62.4M in Q2-25, maintenance revenue $25.8M, asset sales revenue $16.9M. Contracted minimum future lease revenue on the whole book is $221.0M, of which $39.8M remains in 2026 and $63.9M falls in 2027. So contracted rent covers only about 14% of the $450M guide. The rest must come from maintenance-reserve releases, gains on engine and aircraft sales, SCI fees and equity earnings.
3. In 1H26 gain on sale of assets was $177.9M and gain on sales to the 2025 Partnership $17.6M (cash-flow statement); the Leasing segment does not isolate its share, so the gain portion of Leasing EBITDA cannot be measured. Trail.md put gains plus insurance at about 40% of company EBITDA. Closed on disclosure limits; the gain share inside the $48M is a DEAD END.

**Door 2.2. SCI II pipeline and when the book runs out. CLOSED on the mechanics; OPEN on fee rates.**

1. The 10-Q shows the physical book: 22 aircraft (from 47 at 1/1/26, 15 sold, 8 lost to Russia insurance settlement net) and 176 engines (from 243, with 63 transferred to inventory). 19 of 22 aircraft and 93 of 176 engines are on lease; utilization was 68%. Remaining aircraft are few enough that aircraft sales to the SPVs can no longer drive gains; the $48M quarterly figure is mostly engines and run-off.
2. The 2026 SPV is the replacement. Its $2.0B warehouse (with a $1.0B accordion) closed 2026-08-14 and began buying aircraft that month (FTAI release via finviz, 2026-08; bcrpub). In September it bought 17 of 27 WestJet 737-700s in a sale-leaseback; FTAI took the other 10 for parts, not for leasing (search summary). Target size is $6B with FTAI committing 15%, and a capital-call facility will bridge FTAI's equity funding "into 2027" (Q2 call, secondary). The first SPV closed with $2.0B of equity commitments (10-Q) and now generates about $35M per quarter of fees and returns. Servicing fees alone were $7.0M in Q2-26 (10-Q segment note).
3. The book therefore "runs out" as a source of gains within 2026: by 2027 Leasing EBITDA depends on SPV fees, equity earnings and the little remaining rent. Fee percentages and carry remain undisclosed (the SPV agreement is not public). OPEN.

### Thread 3. Aerospace ($1.4B)

**Door 3.1. What the guide implies. CLOSED.**

1. Management guides 2026 Aerospace at $1,050M on 1,200 modules (raised from 1,050, Q2 call), or $0.875M per module. 1H26 Aerospace EBITDA is $472.3M (Q1 $222.6M, Q2 $249.7M, Q2-26 8-K), so 2H26 must reach $578M, about $289M per quarter against $250M in Q2 (+16%).
2. For 2027 the call gave 1,700 modules, so $1.4B implies $0.82M per module, slightly below Q2-26's derived $0.84M and in line with the 28.5-30% margin on about $2.96M of revenue per module. At 1,700 modules and $2.96M revenue per module revenue would be about $5.0B, so $1.4B is a 28% margin. The guide is therefore a volume call (+42% in modules versus 2026) and not a margin call.
3. Consistency with margin. The margin trend (35.9% in Q1-25 to 28.5% in Q2-26) has already been absorbed: management guides "around 30% for the near term". The guide does not need margin recovery. It does need 1,700 modules, which is 57% of the stated 3,000 module physical capacity, and about 570 engine-equivalents of feedstock.
4. PMA ramp. I found no PMA revenue target or ramp in the Q2 call: the only comment was "PMA is one alternative... growth is our number 1 priority". So the $1.4B has no explicit PMA component, and PMA is upside, not support. This weakens the "40% margin in 2026" narrative of the Q4-25 call (which cited PMA), since management has walked that target back to 30%. DEAD END on any quantified PMA contribution.
5. Related-party exposure carries over from stress_test.md: about 25% of 1H26 Aerospace revenue was MRE sales to the 19%-owned 2025 Partnership. If the SPV stops buying as the first vehicle is fully deployed (it was fully committed in Q2), part of the 1,700 modules has to come from third parties. The 2026 SPV helps, but its aircraft deployment starts only in August 2026.

---

## (2) Segment Credibility

| Segment | Guide | Bear | Base | Bull | Credibility of guide |
|---|---|---|---|---|---|
| Aerospace | 1,400 | 1,050 | 1,230 | 1,430 | Moderate to high |
| Power | 450 | 150 | 330 | 600 | Low to moderate (unverifiable) |
| Leasing | 450 | 270 | 360 | 450 | Low to moderate |
| **Total** | **2,300** | **1,470** | **1,920** | **2,480** | |

All figures in $M. Bear, base and bull are my estimates; the segment build in the CSV shows the inputs.

**Aerospace.** Bear $1,050M: 1,350 modules at $0.78M (27-28% margin), meaning the 2026 pace is held near the 2H26 level and heavy-engine mix pulls dollars per module down about 7%. Base $1,230M: 1,500 modules at $0.82M. Bull $1,430M: management's 1,700 modules at $0.84M. Reasoning: 2026 is on a 1,200 module path and Q2-26 produced 296 (4 quarters at that rate is 1,184), so 1,700 requires a further +44% in a year, supported by 3,000 module capacity and GE's view that CFM56 shop visits stay near 2,400 a year in 2026-27 (trail.md). The risk is feedstock, related-party demand, and the 2H26 step-up (needs +16%) in a year when the guide for 2026 was reaffirmed while 1H26 EBITDA was only 45% of it. Credibility is good because the arithmetic is volume at today's dollars per module, but I put 1,500 modules as the base.

**Power.** Bear $150M: first units slip, only about 20 units are recognised in calendar 2027 at $7.5M, and part of the 10% performance adjustment is taken. Base $330M: about 44 units, which is 75% of the PO recognised (acceptance and commissioning lag for batches through November 2027). Bull $600M: the full 59 units plus about 20 more from a second PO under the master agreement, inside management's $450-750M range. Reasoning: the guide equals about 100% of one PO delivered on time, FTAI has not yet delivered a unit, EBITDA per unit and the FTAI stake are undisclosed, the JV is consolidated by a Chinese-listed partner that controls prepayment cash, and the delivery window ends one month before year-end. The favourable points are a signed PO, an advance payment (received per Jereh), a five-year master agreement and a shortage that makes follow-on orders plausible.

**Leasing.** Bear $270M, base $360M, bull $450M (equal to guide). Reasoning: Q2-26 ran at $88M, or $352M annualised; excluding $5M of insurance recoveries the run-rate is $332M. Balance-sheet leasing and gains ($48M a quarter, about $190M annualised) falls as the book of 22 aircraft shrinks and only $64M of contracted rent remains in 2027, while SCI fees and returns ($35M a quarter, $140M annualised) must grow. Base assumes $240M from SCI (the 2025 SPV plus a partial 2026 SPV year) plus $120M from the remaining book. The guide needs about $100M above the Q2 run-rate, nearly all from SCI II. The 2026 guide was already cut from $575M to $475M, a 17% reduction within five months, which is a credibility flag for this segment.

---

## (3) Implied 2027 EBITDA and Multiple at $21.6B EV

| Case | 2027 Adj. EBITDA ($M) | EV/EBITDA at $21.6B | vs guide |
|---|---|---|---|
| Bear | 1,470 | 14.7x | -36% |
| Base | 1,920 | 11.2x | -17% |
| Bull | 2,480 | 8.7x | +8% |
| Management guide | 2,300 | 9.4x | n/a |

Notes. (a) The three cases are not probability-weighted; if I weight 25% bear, 50% base, 25% bull the expected figure is about $1.95B (11.1x). (b) Adjusted EBITDA includes pro-rata EBITDA of unconsolidated entities and excludes profit elimination on affiliate sales (Q2-26 8-K definition), so the multiple is on a measure that is generous relative to cash; stress_test.md showed CFO plus CFI conversion of 35-41%. (c) The EV of $21.59B and net debt of $3.16B come from stockanalysis.com (2026-10-06) per stress_test.md. (d) Pro-rata JV EBITDA is already inside Power and Leasing; I did not add a separate line.

Read-through for Long versus Short: at base, the stock still trades on 11.2x 2027 EBITDA with a shortfall of 17% versus guide already implied by a 9.4x headline. A 17% miss versus guide is not, on its own, a thesis for a 12-month Short, but it removes the idea that the guide is a floor. The upside case requires Power to land at or above the guide, so the pitch should be framed around the Q3-26 print and first Mod-1 delivery.

---

## (4) Open Items

1. J&F ownership percentages and FTAI's accounting (equity method, any guarantees or purchase commitments). Source: Q3-26 10-Q (expected 2026-10-28, per stress_test.md) and the Jereh announcement 2026-048 on cninfo (the PDF text, which I could not retrieve).
2. Whether the first Mod-1 unit shipped in Q4-26, and size and timing of the prepayment (Jereh Q3 report, FTAI Q3 call).
3. Mod-1 unit price, FTAI's transfer price to the JV, and EBITDA per unit (not public). A full Q2-26 call transcript from a primary source to replace secondary quotes ($7-8M per unit, $750M-$1B at 100 units).
4. Gain share inside Leasing's $48M quarterly line and the SCI fee, carry and servicing percentages (SPV agreement not public).
5. 2H26 Aerospace step-up (+16% on Q2), Q3 module count (needs about 325 per quarter for 1,200) and EBITDA per module.
6. Margin on MRE sales to the 19%-owned 2025 Partnership, and share of the 1,700 modules going to the 2026 SPV.
7. Public lead-time figures for LM6000, SGT-A35 and FT8 versus Mod-1; the second hyperscaler PO.
8. Any political action on Jereh-linked power equipment (CFIUS, tariffs, FEOC-type rules); none found.
9. Whether to use Jereh's $3.1B total orders as evidence of demand: only the $1.465B is clearly Mod-1; the rest is Jereh's own packages.

---

## Source Index (all accessed 2026-10-06)

- Jereh half-year report 2026 (cninfo, 2026-08-14): http://static.cninfo.com.cn/finalpage/2026-08-14/1225472540.PDF
- Jereh contract notice coverage: https://stock.10jqka.com.cn/20260723/c678378497.shtml (2026-07-23); https://www.cls.cn/detail/2474994; https://www.sina.cn/news/detail/5323545729305778.html; http://news.10jqka.com.cn/20260722/c678364742.shtml
- Yicai: https://www.yicaiglobal.com/news/chinas-jereh-jumps-by-limit-on-usd15-billion-gas-turbine-generator-order-from-cloud-service-provider (2026-07-22)
- FTAI release: https://www.globenewswire.com/news-release/2026/07/22/3331360/35538/en/ftai-announces-1-465-billion-gas-turbine-generator-set-order-through-j-f-power-systems.html
- FTAI Q1-26 release (Jereh JV announcement): https://www.sec.gov/Archives/edgar/data/1590364/000162828026028390/ftai3312026earningsrelease.htm (2026-04-29)
- FTAI Q2-26 release and 10-Q: URLs above (2026-07-29 and 2026-07-31)
- Q2-26 call transcript (secondary): https://www.investing.com/news/transcripts/earnings-call-transcript-ftai-aviation-q2-2026-eps-miss-clouds-strong-revenue-growth-93CH-4824650 (2026-07-30)
- Q4-25 call transcript (secondary): https://www.fool.com/earnings/call-transcripts/2026/02/26/ftai-ftai-q4-2025-earnings-call-transcript/ (2026-02-26)
- EDGAR full-text search: https://efts.sec.gov/LATEST/search-index (queried with User-Agent "UniResearch research@example.edu")
- Power Engineering on GE Vernova lead times: https://www.power-eng.com/gas/turbines/data-centers-drive-record-surge-in-ge-vernova-power-equipment-orders-as-turbine-slots-tighten-through-2030/
