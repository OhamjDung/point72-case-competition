# FTAI Aviation (NASDAQ: FTAI): Investment Thesis v1.0

**Date:** 2026-10-06
**Recommendation:** **SHORT**
**12-month price target:** **~$145**, which is **−19%** from $179.44 (close on 10/6/26)
**Model:** `model/FTAI_Model.xlsx` (v1.1; 88/88 checks pass)
**Earlier drafts:** `thesis_v0_archive.md`

**Market data (10/6/26):**
- Market cap $18.43B, EV $21.59B, 102.7M shares ([stockanalysis](https://stockanalysis.com/stocks/ftai/statistics/))
- Short interest about 5.9% of float
- Dividend $0.50 per quarter, about a 1.1% yield

**Street view:**
- Every analyst rates it Buy or Strong Buy.
- The mean of the dated post-June price targets is about $330 (median $325). Source: `phase2/data/consensus.csv`.
- Consensus FY27 EPS is about $8.87. This is derived from the 20.2x forward P/E at $179.44, using a single aggregator.

---

## 1. Thesis in one paragraph

The market prices FTAI as a high-growth aftermarket franchise that will deliver management's 2027 guide of $2.3B Adjusted EBITDA. Our model values full delivery of that guide at about $183, so **today's $179 already assumes it.**

The filings show two things the price ignores:
1. **A large share of the 2025–26 cash came from a one-time balance-sheet sell-down that is ending.** FTAI's own 10-Q calls these sales non-recurring.
2. **Growth increasingly runs through three affiliate channels that FTAI does not control.** FTAI books revenue and EBITDA when it sells into them, before end-customer cash arrives.

Our base case puts 2027 EBITDA at $1.92B, 17% below the guide, and FY27 EPS at $7.88. At peer multiples for a business with FTAI's cash conversion, that is worth about $145.

**What's different from the January 2025 Muddy Waters and Snowcap reports.** They already made the "engine trader, falling margins, CFO classification" arguments. We do not pitch those as new. Everything in our two insights post-dates their reports.

---

## 2. Insight 1: the cash engine was partly a one-time sell-down, and it is ending

| Evidence | Figure | Source |
|---|---|---|
| Seed aircraft sold to the 2025 Partnership | Q2'26: 6 sold (gain $2.5M) vs Q2'25: 33 (gain $34.6M). 1H26: 15 vs 1H25: 37 | Q2'26 10-Q |
| Company's own characterization | The sales "were non-recurring in nature and not considered part of the Company's ordinary activities" | Q2'26 10-Q, [EDGAR 0001628280-26-051412](https://www.sec.gov/Archives/edgar/data/1590364/000162828026051412/ftai-20260630.htm) |
| 1H26 CFO + CFI | −$265.3M + $515.7M = **$250.4M** | Q2'26 10-Q |
| …of which seed-sale proceeds | $175.7M | same |
| …of which Russia insurance proceeds | $48.3M | same |
| Remainder after one-offs | **about $26M**, after an inventory build of about $351M | derived |
| FY26 Adj. FCF guide | $878M (cut from $915M on 7/29/26). 1H26 actual was $255M, so **2H26 needs about $623M** against a Q2 run-rate of about $95M | Q2'26 release and call |
| FY25 Adj. FCF | $724M vs CFO+CFI of $412.6M. The CFO named $252M of Q4 add-backs: $52M SCI, $150M Power turbines, $50M hot-section parts. The remaining ~$59M is **inferred** to be acquisitions plus a JV item | [Q4'25 call](https://www.fool.com/earnings/call-transcripts/2026/02/26/ftai-ftai-q4-2025-earnings-call-transcript/), FY25 10-K |
| Gains on sale as a share of Adj. EBITDA | 44% in FY24, 40% in FY25, 40% in 1H26 | 10-K, 10-Q, releases |
| Leasing guide | 2026 cut from $575M to $475M. The leasing book fell from $1,546M to $1,146M in six months | Q2'26 release |

**How to frame the inventory point fairly.** Do not claim that recurring FCF is $26M. The point is that the 2H26 ramp depends on the roughly $351M inventory build turning into cash, and the seed-sale cushion is gone.

---

## 3. Insight 2: growth runs through three affiliate channels FTAI does not control

**Channel 1: aircraft sold to SCI (the 2025 Partnership).**
- FTAI owns about 19% (equity method) and acts as servicer.
- The 10-K describes the partnership as the "primary buyer of all future on-lease 737NG/A320ceo aircraft."

**Channel 2: engines and modules sold to SCI.**
- The MRE contract is exclusive "for the life of the partnership."
- These sales were $335.8M in FY25 (17.3% of Aerospace revenue) and $404.0M in 1H26 (25.0%).
- Q2'26 Aerospace revenue rose $113.2M, "primarily due to an increase in engine and module sales made to the 2025 Partnership."
- Intra-entity profit eliminated in 1H26 was $16.6M.

**Channel 3: turbines sold to the J&F Power JV.**
- Jereh's 1H26 report calls J&F a 控股子公司 (controlled subsidiary) and consolidates it.
- CFO McAleese on the Q2 call (secondary transcript): "when FTAI sells the turbine to the JV… revenue and cost of goods sold" are booked. Equity earnings follow when the JV sells to the hyperscaler.
- The $1.465B purchase order sits with J&F.
- Not disclosed: the ownership %, the unit price and EBITDA per unit (management calls these "commercially sensitive"). See `phase2/G1_power_jv.md`.

**How SCI shows up in EBITDA vs cash**
- Adj. EBITDA includes the "pro-rata share of Adjusted EBITDA from unconsolidated entities."
- In Q2'26 that added $28.0M, against GAAP equity earnings of $16.6M.
- The Leasing segment's "$35M of SPV fees and co-investment returns" breaks down as $7.0M of servicing fees plus $28.0M of pro-rata EBITDA ([Q2'26 release reconciliation](https://www.sec.gov/Archives/edgar/data/1590364/000162828026050622/ftai6302026earningsrelease.htm)).

**SCI's debt sits outside FTAI's EV** *(inferred: partnership financing is not disclosed in FTAI's filings, and no FTAI guarantee was found)*
- Company-cited figures put SCI I at about $6.0B of total capital on $2.0B of equity, which implies roughly $4B of debt.
- FTAI's 19% proportional share is therefore about $760M.
- FTAI counts 19% of SCI's EBITDA in its own Adj. EBITDA, but none of that debt is in FTAI's net debt.
- Adding it would raise FTAI's EV by about 3.5%.

**Why it matters.** FTAI recognizes revenue and EBITDA when it sells into entities whose demand it partly funds and does not control. That is lower-quality growth than third-party aftermarket sales, and it argues against a franchise multiple.

---

## 4. Supporting evidence (not a core insight)

**Feedstock tightness**
- FTAI bought 10 whole off-lease 737-700s from WestJet "to support its Aerospace Products business" ([finviz, 9/28/26](https://finviz.com/news/395776/ftai-acquires-27-boeing-737-700-aircraft-from-westjet)).
- GE calls used-serviceable-material availability "limited."
- Inventory runs about 222 days and has grown 3.8× since FY23, against 2.7× growth in cost of sales.
- Aerospace margin fell from 35.9% to 28.5%. Management now guides about 30%.
- Caveat: the exchange model returns a core with each swap, so gross retirement math overstates the constraint.

**Governance and flow red flags**
- The CFO resigned in March 2026.
- KPMG is a first-year auditor.
- Director Tuchman sold about $61.5M of stock at about $241 in May 2026. There has been **no insider buying** since: the four Form 4s filed 9/17 are routine $0 director grants.
- SDNY class action 25-cv-00541 is pending and not named in the 10-K.

---

## 5. Valuation (see the model's Valuation and Bridge tabs)

**Peer multiples** (stockanalysis, 10/6/26)

| Company | EV/EBITDA TTM | Forward P/E |
|---|---|---|
| HEICO | 30.2x | 44.0x |
| AAR | 13.8x | 17.7x |
| StandardAero | 11.7x | 15.9x |
| AerSale | 17.4x | 18.1x |
| AerCap | 12.4x | 8.5x |
| **FTAI** | **21.7x** | **20.2x** |

**Method.** The blended value weights SOTP 40%, forward P/E 30% and DCF 30%. The SOTP:
- values Aerospace at an MRO multiple (11.7x / 13x / 16x)
- values Power at 8x / 10x / 12x of FTAI's pro-rata EBITDA
- values Leasing at book of about $1.5B, because the book is being sold down and its EBITDA is gain-heavy
- capitalizes corporate costs of about $160M
- deducts net debt of about $3.16B and the preferred

| Scenario | 2027 EBITDA | FY27 EPS | SOTP | P/E | DCF | **Blended** | vs $179 |
|---|---|---|---|---|---|---|---|
| Mgmt Guide | $2,300M | $10.12 | $185 | $172 | $191 | **$183** | +2% |
| **Base** | **$1,920M** | **$7.88** | **$152** | **$134** | **$143** | **$144** | **−20%** |
| Bear | $1,470M | $5.07 | $97 | $86 | $87 | **$91** | −49% |
| Bull | $2,480M | $11.24 | $256 | $191 | $200 | **$220** | +22% |

Probability-weighted (25/50/25) value is about **$150 (−17%)**. **The price target is about $145.**

**Bridge from consensus to our price target (forward P/E leg)**

| Step | Value per share |
|---|---|
| Price today: consensus FY27 EPS $8.87 × 20.2x | $179 |
| **EPS leg:** our FY27 EPS of $7.88 (−11% vs consensus) at the same 20.2x | about $159 (−$20) |
| **Multiple leg:** 20.2x compressing to the 17x MRO peer forward P/E | about $134 (−$25) |

Why the multiple should compress:
- 3-year CFO/EBITDA is −14% for FTAI, against 69% for HEICO and 25% for StandardAero.
- About 40% of EBITDA is gains.
- The share of revenue sold to affiliates is rising.

**Bridge from management's guide to our base (2027 EBITDA).** $2,300M falls to $1,920M: Aerospace −$170M, Power −$120M, Leasing −$90M. See the model's Bridge tab.

**Key assumptions, flagged in the model**
1. **2027 Aerospace EBITDA.** Base case is 1,500 modules × about $0.82M EBITDA per module = $1,230M, against the $1,400M guide.
2. **2H26 conversion of inventory into FCF.** About $623M is needed. Q3 on 10/28 is the first test.
3. **Power.** Base case is 44 units recognized in 2027 × $7.5M = $330M, against the $450M guide. Per-unit economics are undisclosed, and the 75% cash conversion is an **assumption**.

---

## 6. Catalysts

- **Q3'26 results, 10/28/26, after the close.**
  - Consensus: EPS $1.54, revenue $905M.
  - It tests the 2H FCF ramp, the seed-sale count, J&F disclosure and the timing of the first Mod-1 delivery.
  - It lands after the 10/12 submission but before the 11/9 finalist resubmission.
- **Investor meeting, 12/10/26** (reported, not verified). Long-term targets are expected.
- **FY26 results and 10-K, late Feb 2027.** FY26 FCF against the $878M guide, a re-test of the 2027 guide, and SCI II's first full year.
- **First Mod-1 deliveries.** Management now calls them "prudent to expect" in 2027. They were originally guided for Q4'26.

---

## 7. Risks: the strongest case against us

- **Power proves real and larger.** The 2027 guide range is $450–750M, prepayments have been received, and data-center demand for aeroderivatives is strong. **The bull case is about $220 (+22%).**
- **SCI becomes a captive, recurring demand channel.** SCI I has about $6.0B of capital across more than 300 aircraft, all of which buy modules exclusively from FTAI. SCI II targets $6B.
- **CFM56 demand stays strong through 2028–29.** GE expects about 2,400 shop visits a year, Safran's civil spares were up 27.9%, and shops are "oversubscribed."
- **Technicals specific to a short.**
  - A $500M buyback was announced 9/15/26 and runs to 9/30/29. It is funded "from balance-sheet cash," which was $337M, and equals about 2.7% of market cap.
  - Shorts pay the roughly 1.1% dividend.
  - Short interest is 5.9%.
  - The stock rose about 9% on 10/6 on the Q3 date, the investor meeting and the WestJet deal.
- **Take-private or strategic interest.** Air Lease went private in 2026.

---

## 8. Outstanding diligence

1. J&F ownership % and intercompany elimination (Jereh cninfo notices; Q3 10-Q).
2. The FY25 Adj. FCF residual of about $59M (investor deck, which timed out).
3. SCI fee, promote and carry terms, plus partnership-level debt (KBRA ABS pre-sale reports; SCI II marketing).
4. Net core need under the exchange model (modules consumed per shop visit).
5. The 52-week high, to settle "down 21%" vs "down 44%."

---

## 9. Corrections log (for honesty and the GenAI appendix)

1. **Short-seller identity.** The prompt hint named "Hunterbrook" as the January 2025 short seller. It was actually Muddy Waters and Snowcap; an agent caught the error.
2. **FY25 FCF gap.** The orchestrator first said the $311M gap "matches the SCI investment," which was **wrong**. It then said the gap "closes" fully, which was also **wrong**: about $59M is still inferred.
3. **First-pass insight.** "Engine trader" repeated Muddy Waters' Jan 2025 slide 22, so the insight was refocused on what is new.
4. **Valuation v0.1.** It used an unsupported 10x "trader" multiple (AerSale actually trades at 17.4x) and capitalized gain-heavy Leasing EBITDA. Both were fixed.
5. **Model spec.** The spec left about $160M a year of corporate costs out of the SOTP. Fixed in v1.1, which moved the base case from $172 to $152.
6. **SCI net cash.** The figure "SCI net cash −$80M vs $48M EBITDA" was **retracted**, because it subtracted FTAI's own capital call, which is an investment. It was replaced by the proportional-debt point in section 3.
7. **DKS and NBIS screens.** The DKS screen's "+$61M prior-year inventory build" was wrong; the correct figure is +$184M. The NBIS prompt's "6-year depreciation" was wrong: NBIS uses 5 years, and 6 is CoreWeave's.
