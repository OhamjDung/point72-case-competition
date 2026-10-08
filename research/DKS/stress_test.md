# DKS Stress Test: Foot Locker Short (T1), Core Value Long (T2), House of Sport (T3)

Prepared 2026-10-06 for the Point72 Academy pitch (due 2026-10-12). Builds on screen.md in this folder. Price $134.88, market cap about $12.0B, 88.93M shares (stockanalysis.com/stocks/dks/statistics, 2026-10-06). Items I could not confirm in a primary source are marked [UNVERIFIED]. Scenario values and probabilities are my judgment, not sourced.

## Part 1. Smoke tests

**1. Foot Locker inventory derivation: PASS on the level, FAIL on the base-year comparison.**
The 10-Q has no segment inventory table: "Assets by reportable segment are not currently utilized by the CODM ... and thus are not disclosed" (10-Q 8/1/26, sec.gov/Archives/edgar/data/1089063/000108906326000036/dks-20260801.htm, read 2026-10-06). The split is in the Q2 release footnote 4: "Inventories, net as of August 1, 2026 includes $3.6 billion for the DICK'S Business and $2.0 billion for the Foot Locker Business. Inventory increased 6% for the DICK'S Business as compared to August 2, 2025" (sec.gov/Archives/edgar/data/1089063/000108906326000033/dks-2026801xex991earningsr.htm). Total inventory $5,565.3M (XBRL companyfacts CIK 1089063, accn 0001089063-26-000036) less $3,403.9M x 1.06 = $3,608M leaves about $1.96B, consistent with the company's $2.0B. Year-ago Foot Locker inventory was $1,709M at 2025-08-02 (XBRL CIK 850209, accn 0001437749-25-028146), so +14-15% y/y holds; error band about +/-$20M from rounding.
**Correction to T1:** the "+$61M last year" build is wrong. $1,648M was the August 2024 balance. Foot Locker's 2025-02-01 inventory was $1,525M (same XBRL), so the prior-year Feb-to-Aug build was +$184M (+12%). Earlier years: +$188M (FY23: 1,643 to 1,831) and +$139M (FY24: 1,509 to 1,648). This year is about +$430M (1.53B to 1.96B). That is about 2.4x the normal seasonal build, but the January base was depressed by a deliberate $217.9M "write-down and liquidate Foot Locker inventory" charge (10-K FY25, sec.gov/Archives/edgar/data/1089063/000108906326000007/dks-20260131.htm). January 2026 ($1.53B) is flat on January 2025 ($1.525B), so the y/y overhang appears only in the summer.

**2. Q2 call on inventory quality: PARTIAL, FAIL for Foot Locker specifically.**
Quotes: "The industry is carrying too much inventory and the consumer has been even more cautious than expected"; "The inventory built up across the industry supply chains ... led to an increasingly aggressive promotional environment"; "the launches we did see performed below industry and our expectations" (transcript 2026-09-01, fool.com/earnings/call-transcripts/2026/09/01/dicks-sporting-goods-dks-q2-2026-earnings-call-transcript/, obtained through a summarising fetch tool, so exact wording is [UNVERIFIED]). I found no Foot Locker-specific statement that its inventory is clean or aged. The 10-K (March 2026) said "we believe the Foot Locker inventory is well-positioned entering fiscal 2026", which the August cut contradicts. That helps T1 on credibility but is not proof of aged stock.

**3. DKS core segment EBIT and guide: PASS.**
FY26 DICK'S Business segment profit guide "$1.54 billion to 1.60 billion", down from $1.60-1.68B; margin 10.6-10.9% (Q2 release 8/25/26; call: "Operating margins in the range of 10.6% to 10.9% compared to our prior expectation of 11% to 11.4%"). H1 segment profit $846.2M (Q1 $361.0M, Q2 $485.2M; footlocker_segment_trajectory.csv). Reconciliation: consolidated non-GAAP operating income $1.46-1.56B (mid $1.51B) equals core $1.57B plus Foot Locker -$0.06B plus roughly zero corporate.

**4. Peer multiples from free sources: PASS, with a basis caveat.**
All from stockanalysis.com/stocks/<ticker>/statistics, 2026-10-06 (EV/EBIT, fwd P/E): ASO 8.52, 7.68; Best Buy 10.79, 12.39; Shoe Station Group (formerly Shoe Carnival) 12.75, 11.44; Boot Barn 14.57, 13.90; Tractor Supply 16.26, 15.96; Ulta 15.93, 17.79; Genesco 36.49 (distorted), 11.64; DKS 12.82, 11.30. These are trailing and lease-inclusive, so they are not comparable to an ex-lease EV. I value on forward P/E instead. Peer median fwd P/E is 11.6x (ASO, SHOE, GCO, BOOT, BBY) or 12.4x including TSCO and ULTA. DKS at 11.3x is already at the peer median, with a 7.7x floor (ASO) and a 14-16x ceiling. Single source, single date: strength 3.

**5. Foot Locker standalone profit history: PASS.**
GAAP operating income (XBRL CIK 850209, 10-Ks): FY21 $860M (restated $870M), FY22 $581M, FY23 $142M, FY24 $103M; sales $8.97B, $8.76B, $8.17B, $7.99B. Under DKS: segment profit Q3 FY25 -$46.3M, Q4 -$5.9M, Q1 +$17.5M, Q2 -$31.9M; FY26 guide -$80M to -$40M. It was a shrinking, nearly break-even business (1.3% margin at FY24) before the deal, so "temporary loss" requires a return to about the FY24 level.

**6. Census MARTS 451 for Jul-Aug 2026: PASS, with caveats.**
The retail table is at the 3-digit level, NAICS 451 (sporting goods, hobby, musical instrument, book stores). Sub-series 4511 and 45111 are in the Excel file used in screen.md. Advance report for August 2026 (CB26-153, released 2026-09-16, census.gov/retail/marts/www/marts_current.pdf): NAICS 451 +0.2% m/m and +10.0% y/y seasonally adjusted (my reading of garbled table columns), not-adjusted August sales $9,768M. For 45111 (screen.md CSV): July 2026 $5,559M, +7.4% y/y (preliminary); June +13.4%; May +10.1%. The report says it was superseded by revised estimates released 2026-09-28, which I did not retrieve [UNVERIFIED revision]. The series includes books, hobby and trading cards and is not DKS-specific. Category growth of about 10% against DKS Q2 comp of +4.9% is weak evidence for share loss and positive for the demand backdrop.

**Smoke summary:** T1 inventory level PASS, base-year claim FAIL (corrected above). T2 inputs PASS. T3 has no testable primary data (2024 Placer.ai article only) and is excluded from valuation.

## Part 2. Ablation and sum-of-the-parts

**Core earnings.** Core EBIT $1.57B (guide mid). Core EPS = guide EPS mid $11.50 plus Foot Locker loss added back ($60M x 0.71 / 88.93M = $0.48) = **$11.98**. Net debt ex-leases is $1,906M debt less $914M cash = $0.99B (10-Q). The $1.0B notes of 9/22 add equal cash and debt (8-K sec.gov/Archives/edgar/data/1089063/000114036126037715/ef20082695_8k.htm), so P/E on core EPS needs no separate net debt subtraction.

**What the price implies for Foot Locker** (= $134.88 less core EPS x multiple):

| Core fwd P/E | Core value/share | Implied Foot Locker/share | Implied FL $B |
|---|---|---|---|
| 7.7x (ASO) | $92 | +$43 | +3.8 |
| 10.0x | $120 | +$15 | +1.3 |
| 11.6x (peer median) | $139 | -$4 | -0.4 |
| 12.4x (broad peer median) | $149 | -$14 | -1.2 |
| 13.0x | $156 | -$21 | -1.9 |
| 14.0x (about DKS pre-cut) | $168 | -$33 | -2.9 |

At the peer median multiple the market values Foot Locker at about minus $0.4B, roughly zero to slightly negative, so T2's framing holds, but the answer depends entirely on the multiple chosen. The pre-cut stock at about $195 on $14 EPS was about 14x [my derivation]; against that, the market is charging about -$2.9B for Foot Locker. The stock is cheap versus its own history, not versus peers.

**Foot Locker scenarios (per share, my assumptions).** Bear: loss persists plus $0.3B further cash burn, -$11 (about -$1.0B). Zero: $0. Base: EBIT recovers to about $100M (FY24 level plus part of the $100-125M claimed synergies), after-tax $71M x 10x less $0.3B one-time cash: +$4.5. Bull: EBIT $250M x 11.6x less $0.3B: +$15 to +$20.

**SOTP base:** $11.98 x 11.6 + $4.5 = **$143.5 (+6.4%)**. Bear = core 10x on EPS cut by $0.88 (core EBIT -$110M) plus FL -$11 = $100 (-26%). Bull = 13x x $11.98 + $15 = $171 (+27%). Weights 25/50/25 give $139 (+3%).

**Ablation table** (ablation_table.csv; base $143.5):

| Pillar | With | Without | Delta | Evidence 1-5 |
|---|---|---|---|---|
| Core at peer-median 11.6x P/E (vs ASO 7.7x) | 143.5 | 96.7 | -46.8 | 3 |
| Core EBIT at guide (vs -$110M miss) | 143.5 | 133.3 | -10.2 | 3 |
| Foot Locker base +$4.5 (vs bear -$11) | 143.5 | 128.0 | -15.5 | 2 |
| T1: inventory-driven Q3 cut (-$100M, capitalised at 11.3x) | 143.5 | 134.5 | -9.0 | 3 |
| $1.0B notes fund buybacks | 148.9 | 143.5 | +5.4 | 2 |
| FY27 store closures (+$30M EBIT) [UNVERIFIED] | 146.3 | 143.5 | +2.8 | 2 |
| GameChanger at 2x sales [UNVERIFIED] | 146.8 | 143.5 | +3.4 | 1 |
| Insider buying (bear prob 25% to 20%) | 145.7 | 143.5 | +2.2 | 2 |
| T3 House of Sport | n/a | n/a | n/a | 1 |

Notes. Buyback: retiring about 7.4M shares with the full $1.0B lifts EPS from $11.50 to about $11.97 (+4%) after about $47M of after-tax interest; but the 8-K says only "general corporate purposes", and H1 buybacks were $141M against near-zero free cash flow after dividends (H1 CFO $792M, XBRL). Store closures: 110 Foot Locker closures in H1 (store_counts.csv), savings undisclosed. GameChanger: about 10M users and "nearly $150M" revenue (10-K FY25), profit undisclosed, likely already in core EBIT. T1 mechanics: a 10-20% markdown on $2.0B of inventory is $200-400M pre-tax ($1.6-3.2/share after tax), but the market capitalised the 8/25 cut at about the full multiple, hence -$9.0. House of Sport: 2024 Placer.ai figures ($35M sales, 35% cash-on-cash on $18.5M; placer.ai/blog/dicks-sporting-goods-new-store-formats-driving-visit-outperformance, 2024-03-15) cannot be checked now, and cannibalization data is not public.

**Does either thesis give a 20%+ gap with strength 3 or more? No.**
- T2: base gap +6.4%. The 20%+ case (bull $171, +27%) needs a 13x core re-rating (strength 3) and a Foot Locker recovery (strength 2); joint strength 2.
- T1: the strength-3 mechanisms give -$9 (-7%, to $134.5), or about -10% ($121) if the market also keeps 11.3x on EPS cut by $0.80. A 20%+ gap (bear $100, -26%) needs a core miss, a de-rating and a Foot Locker bear case together (strength 2), partly priced after a -42% 52-week move.

## Part 3. Counter-case to the best thesis (T2 Long)

1. **No multiple gap.** 11.3x is already the peer median (11.6x) and above ASO (7.7x). The argument needs 13-14x, i.e. the pre-cut rating. Mean sell-side PT is $157.96 (stockanalysis.com/stocks/dks/forecast, 2026-10-01), so +17% is consensus, not variant.
2. **Cash.** FY25 CFO $1.54B vs gross capex $1.14B and dividends about $0.45B leaves almost nothing for buybacks. FY26 net capex guide is $1.4B and H1 CFO $792M, so FCF after dividends is negative this year. The $1.0B notes at 6.2% and 6.9% cost about $66M a year (about $0.53/share after tax, screen.md). The $3.0B buyback is authorization, not cash.
3. **Guide is not a floor.** Implied H2 core comp is -0.2% to +2.7% vs H1 +5.4%; implied Foot Locker H2 loss $26-66M. Each 100 bps of core margin is $146M, about $1.2/share, about $14 at 11.6x.
4. **Foot Locker is a loss business.** 1.3% margin at FY24, gross margin 25.7% vs 28.9%, goodwill $591M against a $2.5B price and a segment guided to a loss: impairment likely at Q4. Class-action lead-plaintiff deadline 2026-11-03.
5. **Skew.** Bear $100 (-26%, 25%), base $143.5 (50%), bull $171 (+27%, 25%): symmetric, not favourable.
6. **Against T1 (short).** Short interest 8.01M shares at 2026-09-15 (about 9% of shares, 13.3% of float), about $5.6M insider buying including the CFO's $1.0M at $129.75, $3.0B authorization and a deliberately conservative guide (Foot Locker profit cut $190M at midpoint) make a squeeze to $155-160 (+15-19%) plausible.

## Verdict

- **Best thesis:** T2 Long (core at peer-median multiple, Foot Locker priced at zero to negative). T1 second; T3 untestable.
- **Viable? N** under the 20%-gap, strength-3 test. Base-case gap is +6.4%.
- **Direction:** Long, weak; prefer entry after Q3 (2026-11-24, [UNVERIFIED] date).
- **PT range and gap:** $144 (base) to $171 (bull) = +6% to +27%; midpoint $157 = +16%, identical to consensus. Downside tail $100 (-26%).
- **P(right):** 40% to reach about $155 or higher (judgment).
- **Expected alpha** = P x gap - (1-P) x adverse = 0.40 x 16% - 0.60 x 20% = **-5.6%** (adverse = drift to $108). With the full bear $100 as adverse: -8.6%. T1 for comparison (short, PT $111, gap 18%, P 30%, adverse +20%): -8.6%.
- **Carrying pillar:** core multiple at or above 11.6x. At ASO's 7.7x the stock is worth $97; core EBIT holding at $1.57B is second.
- **Kill criteria (Long):** Q3 core comp below 0% or segment margin below 9.5%; a further Foot Locker guide cut beyond $100M; Q3 buybacks under $200M despite the new notes; negative FCF after dividends continuing. **(Short):** Q3 Foot Locker segment loss narrower than -$25M with gross margin above 26%, or the stock above $155.
- **Crowdedness:** the long is consensus (mean PT $158; 13 of 27 ratings Buy or Strong Buy, 12 Hold, 2 Sell or Strong Sell). The Foot Locker bear is crowded too: -31% day, class-action notices, short interest near its six-month high (8.0M vs about 4.6M six months earlier). Neither view is variant. The least crowded evidence is the corrected inventory derivation and the lease-neutral P/E comparison.

## Sources (all retrieved 2026-10-06 unless dated)

sec.gov DKS 10-Q, 10-K, 8-K and Q2 release (URLs above); data.sec.gov XBRL companyfacts CIK 1089063 and 850209 (User-Agent "UniResearch research@example.edu"); stockanalysis.com statistics pages for DKS, ASO, BBY, SHOE, BOOT, TSCO, ULTA, GCO; fool.com Q2 transcript (2026-09-01); census.gov marts_current.pdf (released 2026-09-16); placer.ai blog (2024-03-15). Companion file: ablation_table.csv.
