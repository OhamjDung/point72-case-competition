# FTAI Aviation: Draft Investment Thesis (v0.1, 2026-10-06)

**Status:** this is a working draft for the team to review. Direction and price target are provisional until the model is built.

**Price:** $179.44 (close 10/6/26, +8.7% on the day).
**Market cap:** $18.43B. **EV:** $21.59B. **Shares:** 102.7M ([stockanalysis](https://stockanalysis.com/stocks/ftai/statistics/)).

**Street view:**
- All Buy/Strong Buy ratings.
- Dated post-June price targets average about $330 (median $325). See `phase2/data/consensus.csv`.
- FY26 EPS estimate: $5.83.

**Model result (v1.1, 10/6 evening; `model/FTAI_Model.xlsx`, all 88 checks pass):** points to SHORT, with a price target of about $145 (−19%).

Corporate costs (about $160M a year) are now valued in the SOTP. The first version of the spec had left them out.

Blended $/share (SOTP / P/E / DCF at 40/30/30):

| Scenario | Blended $/share | vs $179.44 |
|---|---|---|
| Mgmt Guide | $183 | +2% |
| Base | $144 | −20% |
| Bear | $91 | −49% |
| Bull | $220 | +22% |

The probability-weighted value (25/50/25 across Bear/Base/Bull) is about $150, or −17%.

**Headline: at $179, the stock already prices in full delivery of management's 2027 guide.** Our base case is 17% below that guide on EBITDA and 22% below on EPS ($7.88 vs a guide-implied $10.12). The Street's mean target is about $330.

---

## 1. The differentiated insight

### What is *not* new, so we must not pitch it as new
The "FTAI is an engine trader, not a franchise" framing was already published, along with the falling margins and the CFO-classification point. Muddy Waters covered all three in its January 15, 2025 short report (slide 22). Snowcap also published that month. Our pitch has to go beyond them. See `phase2/D_adversarial.md` and `short_report_claims.csv`.

### Insight 1: A large part of 2025–26 cash came from a one-time balance-sheet sell-down that is now ending
FTAI funded its cash generation partly by selling its leasing book into SCI I (the 2025 Partnership), and FTAI's own 10-Q classes those sales as one-off. The seed-sale stream is shrinking quickly. The 2026 FCF guide still requires a steep second-half ramp.

- **Seed sales are fading.**
  - Q2'26: 6 seed aircraft sold to the 2025 Partnership, for a $2.5M gain.
  - Q2'25: 33 aircraft, for a $34.6M gain.
  - 1H26: 15 aircraft, against 37 in 1H25.
  - The 10-Q says these sales "were non-recurring in nature and not considered part of the Company's ordinary activities" (Q2'26 10-Q, [EDGAR 0001628280-26-051412](https://www.sec.gov/Archives/edgar/data/1590364/000162828026051412/ftai-20260630.htm)).
- **What 1H26 cash looks like without the one-offs.**
  - CFO was −$265.3M and CFI was +$515.7M, so CFO+CFI = $250.4M.
  - That total includes $175.7M of seed-sale proceeds and $48.3M of Russia insurance proceeds.
  - Excluding both leaves about $26M. That figure is *after* a roughly $351M inventory build.
  - The honest framing: the 2H26 ramp requires that inventory to convert to cash. We are not saying recurring FCF is $26M.
- **The FY26 Adjusted FCF guide has already been cut, and the back half carries most of it.**
  - The guide went from $915M to $878M on 7/29/26.
  - With $255M done in 1H26, 2H26 needs about $623M. The Q2'26 run-rate was about $95M.
- **The company's FCF metric adds back working-capital-like spend.**
  - FY25 Adjusted FCF was $724M, against CFO+CFI of $412.6M.
  - On the Q4'25 call the CFO said the figure was "further adjusted for 3 key investments": a $52M increase in SCI co-investment, $150M of Power turbines, and $50M of hot-section parts. That is $252M in total.
  - The remaining gap of about $59M is *probably* acquisitions. This is inferred from the $49.1M acquisition line plus a $10M JV item, and it is not confirmed ([Q4'25 transcript](https://www.fool.com/earnings/call-transcripts/2026/02/26/ftai-ftai-q4-2025-earnings-call-transcript/)).
  - About $200M of the add-backs are inventory-type purchases, which are the same items that drive negative GAAP CFO.
- **New since MW/Snowcap:** the seed program did not exist until SCI launched in December 2024, and it is now running off.

### Insight 2: Growth increasingly runs through affiliates FTAI does not control
- **Aerospace growth comes from selling to the affiliate.**
  - The 10-Q says Aerospace revenue rose $113.2M y/y, "primarily due to an increase in engine and module sales made to the 2025 Partnership."
  - The Partnership bought $335.8M in FY25 (17.3% of Aerospace revenue) and $404.0M in 1H26 (25.0%).
  - FTAI eliminated $16.6M of intra-entity profit in 1H26.
  - The 10-K says FTAI's MRE business "exclusively provides replacement aircraft engines and modules for the life of the partnership."
- **FTAI is on both sides.** FTAI owns about 19% of the vehicle (equity method, carrying value $365.5M), acts as its servicer, and is its exclusive engine supplier. Fee and promote terms are not disclosed. Recurring servicing fees were $7.0M in Q2'26.
- **The Power order sits in a JV that Jereh consolidates.**
  - The $1.465B hyperscaler PO is held by J&F Power Systems. Jereh's 1H26 report (cninfo, 8/14/26) calls J&F a 控股子公司 (controlled subsidiary) and consolidates it.
  - FTAI equity-accounts its stake. This comes from a secondary source, the Q2 call.
  - "Jereh" appears in only one FTAI filing.
  - The ownership split and how FTAI recognizes Power economics are **unverified**.
- **The SCI vehicles now buy aircraft straight from airlines.** SCI II (the 2026 SPV) bought 17 on-lease 737-700s from WestJet in a sale-leaseback. FTAI bought the other 10, off-lease, "to support its Aerospace Products business" ([finviz, 9/28/26](https://finviz.com/news/395776/ftai-acquires-27-boeing-737-700-aircraft-from-westjet)). So SCI II deals do not by default bring back seed proceeds from FTAI's balance sheet.

### Supporting evidence, demoted: feedstock tightness
- FTAI bought 10 whole aircraft from WestJet for parts.
- GE calls used serviceable material availability "limited".
- Inventory runs about 222 days, up 3.8x since FY23 against 2.7x for cost of sales.
- Aerospace margin fell from 35.9% to 28.5%. Management now guides about 30%, below its earlier 40% target.
- **Not pitched as a core insight.** CFM56 retirements are about 420–560 *engines* a year (1.5–2% of about 28,000), but FTAI's exchange model returns a core with each module swap. Gross need therefore overstates the constraint. This goes to outstanding diligence.

---

## 2. Valuation (v0.2, corrected after review; the model will refine it)

### Facts that change the valuation
- **Adjusted EBITDA includes FTAI's "pro-rata share of Adjusted EBITDA from unconsolidated entities"** (definition in the Q2'26 10-Q). Two consequences:
  - FTAI's share of the J&F Power JV is *inside* Adjusted EBITDA, so Power can be valued on EBITDA.
  - About 19% of SCI's lease EBITDA also counts toward FTAI's EBITDA, but cash only reaches FTAI through distributions: $27.1M "return of capital" in FY25. **This is another gap between EBITDA and cash, and it is new since MW.**
- **There is no cheap "trader" peer.** AerSale (ASLE), a negative-FCF used-parts trader, trades at 17.4x TTM. So the earlier 10x "trader multiple" has no anchor and has been dropped.

### Peer multiples
Source: stockanalysis, as of 10/6/26. **FTAI's forward P/E of 20.2x implies FY27 EPS of about $8.87**, which resolves the 20x vs 31x conflict: 31x is on FY26 EPS of $5.83.

| Company | EV/EBITDA TTM | Forward P/E | FCF yield |
|---|---|---|---|
| HEICO | 30.2x | 44.0x | 2.4% |
| AAR | 13.8x | 17.7x | 3.3% |
| StandardAero | 11.7x | 15.9x | 3.2% |
| AerSale | 17.4x | 18.1x | −16.7% |
| AerCap | 12.4x | 8.5x | −1.4% |
| FTAI | 21.7x | 20.2x | n/m |

### Method 1: sum-of-the-parts
For a 12-month target, we apply TTM peer multiples to 2027E EBITDA, because 2027 becomes the trailing year at the target date.

How each piece is valued:
- **Aerospace:** MRO peer range.
- **Power:** FTAI's pro-rata EBITDA × 8–12x.
- **Leasing:** valued at about **book value**, not as a multiple of gain-heavy EBITDA. The book is being sold down. Leasing equipment net is $1,146M and the SCI stake is $365.5M (6/30/26), about $1.5B in total.
- **Net debt** is about $3.16B, and there are 102.7M shares.

| Case | Aero EBITDA × multiple | Power EBITDA × multiple | Leasing | Value / share |
|---|---|---|---|---|
| Bear | 1,050 × 11.7x | 150 × 8x | $1.5B | **~$115** |
| Base | 1,230 × 13x | 330 × 10x | $1.5B | **~$172** |
| Bull | 1,430 × 16x | 600 × 12x | $1.8B (1.2× book) | **~$280** |

**Probability-weighted value.** At 25/50/25 weights the value is about $185. At 30/50/20, which assumes a miss on 2H26 FCF makes the bull case unreachable within 12 months, it is about $177. **Both are roughly in line with the $179 price.**

### Method 2: forward P/E cross-check
- At the MRO forward P/E of 16–18x (AAR, StandardAero, AerSale), **consensus** FY27 EPS of about $8.87 gives **$142–160**.
- Our base case puts 2027 EBITDA about 17% below the guide. With fixed interest and D&A, EPS would fall by more than 17%. *The model must compute this properly.*

### What the numbers actually say
1. **Versus the Street, the variant view is strong.** The Street's mean PT is about $330 (methodology not public), and every analyst rates it a Buy. Both of our methods land at $142–185. The evidence verified against primary sources says the guide and the cash engine are overstated.
2. **Versus the price, a Short is marginal.** The SOTP base is about −4%, the P/E method gives −11% to −21%, and the bull tail is about +56%. The Short depends on two things: (a) the P/E method, where FTAI keeps 20x only if the 2027 guide is fully delivered, and (b) the Q3 FCF test cutting off the bull case.
3. Key Assumption #1 is now **the 2027 EBITDA delivery and the valuation basis** (EBITDA SOTP versus P/E), not a "trader multiple".

**Key Assumption #2: 2H26 FCF conversion.** About $623M is needed in 2H26 against $255M in 1H26. Q3 on 10/28 is the first test.

**Key Assumption #3: the Power ramp.** We assume 44 units in 2027 at about $7.5M of EBITDA per unit. The per-unit figure comes from a secondary source.

### FCF-yield cross-check
On management's definition, the FY26 guide of $878M gives a 4.8% yield, which looks cheap against peers at 2.4–3.3%. The thesis is that this definition flatters FCF, because it adds back turbine and parts purchases and includes seed-sale proceeds. The model must also show FCF yield on CFO+CFI excluding one-offs.

### Checked and ruled out as a counter
The four Form 4s filed 9/17/26 are routine director grants of 118–171 shares at $0, not purchases. There has been **no insider buying** after the 19% drop.

## 3. Catalysts
- **Q3'26 results, 10/28/26 after the close.** This is the test of the 2H FCF ramp, the seed-sale count, the J&F note and the first Mod-1 timing. Consensus: EPS $1.54, revenue $905M. It lands after the 10/12 deadline but before the 11/9 finalist resubmission.
- **Investor meeting, 12/10/26** (reported, not yet verified). Long-term targets will be laid out.
- **FY26 results and the 10-K, late February 2027.** This is the FY26 FCF actual against the $878M guide, and the first full-year look at SCI II.
- **First Mod-1 deliveries.** Management now says it is "prudent to expect" them in 2027. They were originally guided for Q4'26.

## 4. Risks and disconfirming evidence
The strongest case against us:
- **Power is real and larger.** The guide range is $450–750M EBITDA. The PO's prepayments are received (according to Jereh), and data-center demand for aeroderivatives is strong. At the bull case our Short loses about 70%.
- **SCI scales into a captive engine-demand channel.** The SCI I vehicle has about $6.0B of total capital across more than 300 aircraft, all of which must buy modules exclusively from FTAI. SCI II targets $6B. This could look like a recurring franchise rather than a one-off.
- **The stock has already de-rated.** It trades well below its 200-day moving average ($236), and a $500M buyback has reportedly been approved (unverified). The 10/6 rally followed the Q3 date, the investor meeting and the WestJet deal.
- **CFM56 demand is strong through 2028–29.** GE expects about 2,400 shop visits a year, Safran's civil spares rose 27.9%, and shops are "oversubscribed".
- **Takeover or private capital interest.** Air Lease was taken private in 2026.

Other red flags, which support the thesis but are not proof:
- The CFO resigned in March 2026.
- KPMG is a first-year auditor.
- Director Tuchman sold about $61.5M at about $241 in May 2026.
- SDNY class action 25-cv-00541 is not named in the 10-K.
- Short interest is about 5.9% of float.

## 5. Outstanding diligence
1. The J&F ownership split and FTAI's accounting for Power. Sources: Jereh notice 2026-048 (cninfo) and the Q3 10-Q.
2. The FY25 Adjusted FCF residual of about $59M. Source: the investor deck, which timed out.
3. Leasing reconciliation. The Q2 call cites $35M of "SPV management fees and co-investment returns", but the 10-Q shows $7.0M of servicing fees plus $10.0M of equity earnings. We need to explain the difference.
4. Net core need under the exchange model (module consumption per shop visit).
5. Verify the $500M buyback, its date and its funding source. The question is a buyback against negative CFO.
6. SCI fee, promote and carry terms. Possible source: the MRE 2026-1 ABS pre-sale report.

## 6. Corrections log (for honesty and the GenAI appendix)
- The prompt hint named "Hunterbrook" as the January 2025 short seller. It was actually Muddy Waters and Snowcap. Caught by an agent.
- The orchestrator first said the $311M FY25 FCF gap "matches the SCI investment". **Wrong.** The CFO named $252M of Q4 growth investments, and about $59M is probably acquisitions (inferred).
- The orchestrator first said the "$311M gap closes" fully. It is only partly explained. About $59M remains inferred.
- The first-pass insight ("engine trader") was found to repeat Muddy Waters' January 2025 slide 22, so it was re-focused on what is new since then.
- The DKS screen's "+$61M prior-year inventory build" was wrong. The correct figure is +$184M.
- The NBIS prompt's "6-year depreciation" was wrong. Nebius uses 5 years; 6 is CoreWeave's policy.

---

## 7. Gap closure (10/6 late; orchestrator, primary sources)

**1. Leasing "$35M SPV fees and co-investment returns" (Q2'26 call): RESOLVED.**
- The $35M = $7.0M of servicing fees + $28.0M of "pro-rata share of Adjusted EBITDA from unconsolidated entities". The pro-rata piece is essentially all from SCI; the Aerospace segment's pro-rata share is only $0.05M.
- In the Q2'26 release's Adjusted EBITDA reconciliation, FTAI adds back $28.0M of pro-rata EBITDA in place of $16.6M of GAAP equity earnings.
- Source: [Q2'26 release, EDGAR 0001628280-26-050622](https://www.sec.gov/Archives/edgar/data/1590364/000162828026050622/ftai6302026earningsrelease.htm).

**2. SCI: EBITDA counted vs cash received in 1H26 (new evidence for Insight 2).**

| 1H26 item | Amount |
|---|---|
| Pro-rata SCI/unconsolidated EBITDA counted in Adjusted EBITDA | $48.3M |
| Cash distributions received from the 2025 Partnership | $19.2M |
| New investment in unconsolidated entities | $99.3M |

- **Net SCI cash flow to FTAI was about −$80M, while FTAI booked $48M of EBITDA from it.**
- Source: Q2'26 10-Q cash flow statement and Note 10.

**3. $500M buyback: VERIFIED, and it supports the thesis.**
- Announced 9/15/26. Runs to 9/30/2029. To be funded "using cash on its balance sheet" ([finviz](https://finviz.com/news/392391/ftai-aviation-announces-500-million-share-repurchase-program)).
- Cash was $337.2M at 6/30/26, GAAP CFO is negative, and debt is $3.5B.
- So the buyback depends on the 2H26 cash ramp or on more asset sales. The model keeps the buyback toggle OFF in Base.

**4. FY25 Adjusted FCF residual of about $59M: STILL OPEN.**
- 2026 releases contain no FCF reconciliation table.
- Treat it as "inferred: likely acquisitions ($49.1M) plus a JV item of about $10M".

**5. Power JV: partly resolved** (`phase2/G1_power_jv.md`).
- **VERIFIED: FTAI books revenue when it sells turbines *to the JV*.** CFO McAleese said on the Q2'26 call (7/30/26; investing.com transcript, a secondary copy of a primary statement): "when FTAI sells the turbine to the JV... revenue and cost of goods sold". FTAI then books equity earnings when the JV sells to the hyperscaler.
  - So Power is a **third affiliate sales channel**, alongside SCI aircraft sales and MRE module sales to SCI.
  - Revenue is recognized on the sale into a Jereh-controlled JV, *before* delivery to the end customer.
- **NOT DISCLOSED:**
  - J&F ownership %. Jereh calls J&F a 控股子公司, i.e. Jereh controls it.
  - Unit price and EBITDA per unit. Management calls them "commercially sensitive".
  - Unit count in the PO. The PO is $1.465B, delivered in batches through Nov 2027, and the guide says "<100 units".
- **Risk to watch:** the $450M guide probably includes both FTAI's own margin on turbine sales to the JV and its pro-rata share of JV EBITDA. Whether intercompany profit is eliminated is not explicit. [UNVERIFIED]
- **Model:** the Power inputs stay as they are (Base 44 units × $7.5M = $330M). They sit inside the agent's suggested range (bear $180M, base $420M, bull $750M). The 75% cash conversion stays labeled as an **assumption** with no source.
- No US–China regulatory item was found in public news.

### Updated Insight 2 framing (for the deck)
**FTAI recognizes revenue and EBITDA through three affiliate channels it does not control:**
1. Aircraft sold to SCI.
2. Engines and modules sold to SCI under an exclusive MRE contract: 25% of Aerospace revenue in 1H26.
3. Turbines sold to the Jereh-controlled J&F JV.

Its EBITDA also includes pro-rata SCI EBITDA ($48.3M in 1H26), while net cash flow to SCI was about −$80M over the same period.
