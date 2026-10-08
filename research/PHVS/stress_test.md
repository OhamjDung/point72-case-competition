# PHVS (Pharvaris) - Stress Test of the Long and Short Theses

Prepared 2026-10-06 for the Point72 Academy pitch (due 2026-10-12). Public sources only; no one was contacted. This memo builds on `trail.md` and does not redo it. Every number carries a source and date. Items I could not tie to a primary document are marked **[UNVERIFIED]**. Inputs that are my own assumptions are labelled "assumption".

Starting point: about $31 per share, about 71M shares, about $2.2B market cap, cash of EUR 318.3M (about $359M at 1.1269), so EV of about $1.84B.

---

## Part 1 - Smoke tests

### 1A. Size of the prophylaxis market - PASS on three of four drugs, FAIL on Takhzyro's calendar-2025 figure

| Drug | Figure | Primary source and quote | Result |
|---|---|---|---|
| Takhzyro (Takeda) | JPY 59.9B in April-June 2026 (Q1 FY26), -2.2% at constant exchange rates | Takeda Q1 FY2026 earnings report, 2026-07-30 ([PDF](https://assets-dam.takeda.com/image/upload/v1785376940/Global/Investor/Financial-Results/FY2026/Q1/qr2026_q1_er_en.pdf)): "Sales of TAKHZYRO (for hereditary angioedema) were JPY 59.9 billion ... -2.2% CER. The increase was primarily due to favorable foreign exchange rates, partially offset by a sales decline in the U.S. due to increased competition." Presentation slide: "TAKHZYRO maintains U.S. market leadership position despite an increasingly competitive HAE market." | PASS for the latest quarter. This replaces the [UNVERIFIED] tag in trail.md. |
| Takhzyro calendar 2025 | Not found | Takeda's FY2025 release (businesswire) returned HTTP 403 and the Q1 earnings PDF holds only the quarter. A search summary says FY2025 Takhzyro was "roughly flat". | FAIL, **[UNVERIFIED]**. I annualize the latest quarter instead: JPY 59.9B x 4 = about JPY 240B, or about $1.6B at an assumed JPY 150 per dollar (FX is my assumption). This is global, not US-only. |
| Orladeyo (BioCryst) | 2025: $601.8M (trail.md item 11). 1H26: $306.5M (Q1 $148.3M, Q2 $158.2M) | BioCryst Q2 2026 release, 2026-08-05 ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/05/3339185/0/en/BioCryst-Reports-Second-Quarter-2026-Financial-Results.html)): Q2 "$158.2 million (+1% y-o-y; +10% y-o-y on a comparable basis)"; guide "$625 million to $645 million". The 10-Q shows $306,549K for six months ([10-Q](https://www.sec.gov/Archives/edgar/data/0000882796/000162828026053300/bcrx-20260630.htm); seen through a search summary, not opened). | PASS |
| Andembry (CSL) | $240M in FY26 (July 2025 to June 2026) | CSL FY2026 results ([PDF](https://investors.csl.com/pdf/80148cbc-d117-4b5c-9213-628b0d1de681/Platform/ListPage/CSL-FY2026-Results.pdf)): "In the Hereditary Angioedema segment, ANDEMBRY achieved sales of $240 million in its first full year in market". No calendar split. | PASS |
| Dawnzera (Ionis) | Q2 26 $26M; 1H26 $42M | Ionis Q2 2026 release ([SEC](https://www.sec.gov/Archives/edgar/data/0000874015/000114036126029960/ef20078953_ex99-1.htm)): "U.S. net product sales of $26 million and $42 million in the second quarter and first half of 2026"; Q2 up 63% on Q1; guide $110-120M. | PASS |

**Market size conclusion.** The four modern prophylactics run at about $2.6B annualized worldwide (Takhzyro about $1.6B, Orladeyo about $0.62B, Andembry $0.24B, Dawnzera about $0.11B at the guide midpoint). Excluding plasma products and ex-US Takhzyro, a US pool of roughly $2.0B is a fair working number (my estimate). The pool is rotating rather than expanding: Takhzyro is declining in the US, Orladeyo's comparable growth slowed to +10%, and the two new entrants are the growth. Andembry reaching $240M in its first full year shows a new entrant can take about 10% of the pool inside a year, which supports a double-digit share assumption for an oral with 87% efficacy.

### 1B. CHAPTER-3 safety and dropouts - PASS on headline safety, open on detail

Source: Pharvaris press release 2026-09-08, read through the [Finviz mirror](https://finviz.com/news/389353/pharvaris-announces-positive-topline-data-from-chapter-3-pivotal-study-of-deucrictibant-xr-for-prophylaxis-of-hae-attacks). The SEC 6-K [cover](https://www.sec.gov/Archives/edgar/data/1830487/000119312526384339/6-k_september_8_2026.htm) points to Exhibit 99.1, which I did not open.
- "deucrictibant XR was well tolerated with most treatment-emergent adverse events being mild or moderate."
- "There were no treatment-related serious adverse events reported."
- "One participant in each group discontinued treatment due to an adverse event." That is 1 of 55 on drug and 1 of 30 on placebo.
- n=85 from 21 countries, 55 versus 30, 24 weeks; 83% attack reduction overall (p<0.0001), 87% in type 1/2.
- Not disclosed in the release: liver enzymes, headache rate, total completion. The headline is clean, but I cannot call the liver profile clean until full data appear (ACAAI in November; date unverified).

### 1C. Lonvo-z durability, safety, price - PASS on durability and safety, FAIL on price

- Durability: Intellia Q2 2026 release ([BioSpace](https://www.biospace.com/press-releases/intellia-therapeutics-announces-second-quarter-2026-financial-results-and-business-updates)): "All patients who received lonvo-z at baseline in crossover after week 28 remained free from long-term prophylaxis therapy" through the 2026-02-10 cutoff. Phase 1 follow-up to three years: all 10 patients attack-free and treatment-free for a median of nearly two years, 98% mean reduction ([EAACI June 2025 summary](https://crisprmedicinenews.com/news/intellia-reports-positive-three-year-follow-up-data-from-phase-1-crispr-trial-in-hereditary-angioede)). That is only 10 patients.
- Safety: "All TEAEs reported were mild or moderate (Grade 1 or Grade 2), and there were no serious adverse events observed in the lonvo-z arm." The sister program nex-z had a liver event and a death (trail.md item 16); the release is silent on liver for lonvo-z, so liver label risk remains open.
- Price: not disclosed; Intellia says it is still finalizing contracting and price. I found no citable analyst figure. My $2-3M per patient is **[UNVERIFIED]**; Part 2 shows it barely moves PHVS value.
- Timing: PDUFA 2027-03-10; launch 1H 2027; cash $628.4M, funded "at least into 2028" (same release).

### 1D. PHVS runway and dilution - PASS on guidance, PARTIAL on "dilution likely"

- Q2 2026 release, 2026-08-12 ([6-K ex 99.1](https://www.sec.gov/Archives/edgar/data/1830487/000119312526345702/phvs-ex99_1.htm)): "The financing we completed in May extends our cash runway into 2028." Cash EUR 318M at 6/30/26 versus EUR 292M at year-end; Q2 loss EUR 47.8M; $132M offering in May 2026.
- My inference (trail.md item 28, assumption): launch SG&A of $35-45M a quarter would leave 2.5-3 quarters of cash entering 2027. That contradicts "into 2028" only if spending steps up faster than the company plans, and I cannot verify its plan. "A raise around approval is likely" is therefore a judgement, not a fact. The May raise priced at $29.68, so a new raise near $31 would be close to flat versus the last deal.
- Result: runway guidance verified; dilution claim unverified, and its dollar effect is small (Part 2).

**Smoke summary.** Market size PASS (Takhzyro CY2025 FAIL, annualized quarter used). CHAPTER-3 safety PASS on headline; liver and completion not disclosed. Lonvo-z durability and safety PASS, price FAIL. Runway PASS; dilution PARTIAL.

---

## Part 2 - Ablation (rNPV)

The model is in `rnpv_model.py` and the table is in `ablation_table.csv`, both in this folder. All structural inputs below are my assumptions unless a source is given; they are chosen from the evidence in trail.md and Part 1, not tuned to the share price.

### 2A. Model structure

| Input | Value | Basis |
|---|---|---|
| Diagnosed US patients | 8,500 | trail.md item 3 (KalVista: 1,702 forms is "almost 20%") |
| US on-demand: oral-brand penetration | 40% of diagnosed patients at peak | Assumption; Ekterly has about 1,700 start forms after 8 months |
| Deucrictibant IR share of oral-brand pool | 45% | Assumption; second entrant, speed edge of only 0.3-0.5 hours (trail.md item 14) |
| Treated attacks per patient-year and net per attack | 10 and $12K | Ekterly WAC about $17.8K per attack, gross-to-net 30% (trail.md items 5-6; GTN unsourced). Check: Ekterly's Q1 product revenue of $39.2M annualizes to about $157M |
| US chronic prophylaxis pool at peak (2033) | 7,500 patients | About $2.0B US pool today at about $330K net per patient is about 6,000 patients, plus modest growth |
| XR share of pool, net price | 18%, $330K per patient-year | Part D gross about $450K per beneficiary (trail.md item 12) less about 27% gross-to-net (assumption). Andembry took about 10% in year one |
| Intellia | 8% of diagnosed patients (680) leave the chronic pool by 2033 | Assumption; trail.md item 18 scenario of 5-10% cumulative by year 3 |
| Ex-US uplift | +35% | Assumption |
| Probability of approval | IR 90% (PDUFA 2027-04-23); XR 70% (filing 1H27; 24-week data, n=85) | Assumption |
| Launch and ramp | IR 2027, XR 2028, 5-year ramp, plateau to 2040, erosion after | Assumption |
| Margin and tax | 55% operating margin at steady state, 20% tax | Assumption |
| Pre-peak overhead | $300M present value of unallocated spend | Assumption |
| Discount rate | 11% (10% and 12% shown) | Task range 10-12% |
| Cash and shares | $359M; 71M shares | Q2 6-K; market cap / price |

### 2B. Base-case output

- IR peak (unrisked, US plus ex-US): $248M. XR peak: $547M.
- rNPV: IR $599M plus XR $893M, less $300M overhead gives EV $1,192M; plus cash gives equity value of about $1.55B, or **$21.5 per share** versus $31.
- Discount rate: $22.9 at 10%, $20.2 at 12%.
- Scenarios: bear $9.2 (XR 8%, IR 30%, Intellia 12%, price -21%, XR approval 55%, $350M raise at 15% discount); base $21.5; bull $42.5 (XR 28%, IR 55%, Intellia 3%, price $360K, XR approval 85%, ex-US +50%). With weights of 30%, 45% and 25% the expected value is **$23.1**, which is 25% below the price.
- Model risk: moving margin to 65% and ex-US to +50% lifts the base to $28.1. The conclusion is sensitive to those two inputs, and I have no source for either.

### 2C. Reverse DCF - what the $1.84B EV implies

Scaling both shares by the same factor until the model returns the current EV gives a factor of 1.44 times base: IR peak $356M plus XR peak $785M, **about $1.14B unrisked peak sales (US plus ex-US), or about $870M probability-weighted**. That is roughly an XR share of 26% and an IR share of 65% of the oral pool.

Two checks on the thesis framing:
- If the market priced PHVS as an on-demand story only, the IR peak would have to be about $886M unrisked. KalVista's own management peak, for the on-demand market leader, was $705M across US and EU ([SC 14D9, 2026-05-13](https://www.sec.gov/Archives/edgar/data/0001348911/000114036126021078/ny20073033x1_sc14d9.htm)), and Chiesi paid about $1.9B for it. A second entrant cannot reasonably be valued at more than the leader's plan on on-demand alone, so **the market is already paying for prophylaxis.**
- Prophylaxis alone would need an XR peak of about $1.3B, about 2.4 times my base. The price therefore embeds a mix of both, with prophylaxis the larger part.

### 2D. Ablation table (value per share, base $21.5; price $31)

| Pillar | Value/share with | Without | Delta | Evidence 1-5 | Flex range (low / high) | Why this score |
|---|---|---|---|---|---|---|
| Prophylaxis share (18% vs 0%) | 21.5 | 9.0 | +12.5 | 2 | 14.5 (8%) / 28.5 (28%) | Cross-trial 87% equals the injectables, not better; n=85; 24 weeks; no head-to-head |
| On-demand share (45% of oral pool vs 0%) | 21.5 | 13.1 | +8.4 | 3 | 17.8 (25%) / 24.3 (60%) | CMS Part D and Medicaid show share-taking from icatibant; flat start forms; $1.9B buyout as a floor signal |
| Intellia penetration (8% vs 0%) | 21.5 | 22.8 | -1.3 | 2 | 20.4 (15%) / 22.8 (0%) | No price, no label, 80-patient pivotal, liver label risk unresolved |
| Net price (-30% vs base) | 21.5 | 15.2 | +6.3 | 3 | 17.2 / 24.5 | Part D gross anchor of about $450K is solid; gross-to-net is not disclosed |
| Dilution ($250M at 10% discount vs none) | 21.5 | 21.8 | -0.3 | 3 | 20.8 ($400M at 20% discount) / 21.8 | Raise size is my burn model; the May deal priced at $29.68 |

Reading the table: prophylaxis share is the biggest value pillar but has the weakest evidence. Intellia and dilution barely move value per share, so they are headline risks and not value drivers. A raise at $31, above my base value, would actually add value per share.

### 2E. Gap test (at least 20% gap with evidence at least 3)

| Thesis | Gap versus $31 | Pillar carrying the gap | Evidence | Passes? |
|---|---|---|---|---|
| T1 Long: prophylaxis is mispriced | Base $21.5 (-31%); probability-weighted $23.1 (-25%); only the bull case ($42.5, +37%) clears +20% | XR share (evidence 2) | 2 | **FAIL.** The premise that the market ignores prophylaxis is contradicted by the reverse DCF (2C). Even 28% XR share with 55% IR share and 3% Intellia only reaches $42.5 when approval odds and ex-US are also raised. |
| T2 Short or avoid: on-demand is a share swap, Intellia, dilution, insiders | -25% to -31% gap on my base | Mostly XR share being below what the price needs (evidence 2); on-demand share has evidence 3 but cannot close the $9.5 base gap by itself | 2 on the main driver | **FAIL on evidence.** The size of the gap passes; the strength fails. Of T2's four legs, Intellia (-$1.3 at most) and dilution (-$0.3) are too small to matter, and insider selling (857K shares, 1.2% of shares outstanding, trail.md item 22) is a sentiment signal and not a value driver. |

---

## Part 3 - Quantifying the counter-case

The counter-case is whatever hurts the position I end up with. Because the gap test favors a Short or Avoid view (Part 2), I quantify the case against that view first, then against a Long.

### 3A. Scenarios for the 12-month horizon

| State | Probability | PHVS value (model) | Return to a Short | What would have to be true |
|---|---|---|---|---|
| Bear | 27% | $9.2 | +70% | XR share about 8%, Intellia takes 12% of the pool, price 21% lower, XR approval odds 55% |
| Base | 40% | $21.5 | +31% | Share and price per the Part 2 table |
| Bull | 23% | $42.5 | -37% | XR share 28%, IR 55%, ex-US +50%, XR approval 85% |
| Takeout | 10% | about $45 | -45% | A strategic bid. Chiesi paid $27 for KalVista, a 36% premium, and the 14D9 names at least three other interested parties (trail.md item 9) |

The probabilities are my judgement and the takeout probability is the least certain; I know of no live rumour. Probability-weighted value is about $25.4 including the takeout (about $23.1 excluding it), which is 18-25% below $31.

Why a model value of $21.5 does not translate to a 12-month price target of $21.5. Value converges to the model slowly, and three scheduled events can push the price the other way before then: the Intellia decision on 2027-03-10, the IR approval on 2027-04-23, and full CHAPTER-3 data at ACAAI. A clean approval usually helps the stock, and my model already assumes 90% approval odds, so approval itself is not upside to my numbers but it will likely be a positive price event. I therefore use a 12-month price range of **$22-27** (midpoint $24.5), which is a 13-29% decline from $31.

### 3B. Specific counter-arguments and their size

| Counter-argument | Source | Effect on the Short |
|---|---|---|
| Takeout optionality | KalVista sale at $27, 36% premium to the 4/28 close ([Pharmaceutical Technology](https://www.pharmaceutical-technology.com/newsletters/chiesi-widens-rare-disease-portfolio-with-1-9bn-kalvista-buyout)); trail.md item 9 | Largest single risk: a loss of 35-45% on 10% of outcomes. This alone costs a Short about 4 points of expected return. |
| Modeled value is sensitive to two unsourced inputs | Part 2B | Margin 65% and ex-US +50% lift the base to $28.1, which is 9% below price. The gap shrinks from 31% to 9%. |
| The stock is already below its pre-data close | trail.md item 23: $31.12 versus $35.25 on 9/4 | The data pop is erased, so the easy part of a Short has already happened. |
| Sector de-rating is not PHVS-specific | trail.md item 26: BCRX -20%, IONS -24%, PHVS -12% | A Short on PHVS is partly a sector bet; Short interest and borrow cost are not verified **[UNVERIFIED]**. |
| Dilution is not value-destructive at these prices | Part 2D | A raise at or above about $27 is value-neutral to accretive, so a Short thesis cannot lean on it. |
| Insider selling | trail.md items 19-22: 857K shares, 1.2% of shares outstanding, 600K in one negotiated block at $35.00 | Sentiment only. Prior research found no purchases, but the CEO and CFO retain large holdings. |

### 3C. Counter-case against a Long

Probability-weighted value of $23.1-25.4 is below the price, so a Long has negative expected value on my numbers. The Long's best argument is the takeout floor plus a bull case of $42.5 (+37%). Its main weaknesses are cross-trial efficacy only, n=85 over 24 weeks, no price guidance, and an XR launch no earlier than 2028.

---

## Verdict

| Item | Answer |
|---|---|
| Best thesis | A narrowed T2: **"The price already embeds prophylaxis success; avoid or underweight."** The Intellia, dilution and insider legs of T2 are too small to carry it. T1 is rejected because its premise (the market prices PHVS as on-demand only) is contradicted by the reverse DCF. |
| Viable? | **N.** The gap is 25-31% against the model, which clears 20%, but the evidence on the carrying pillar is 2 of 5, and expected alpha is negative. |
| Direction | Avoid, or at most a small Short; not a Long. A pair (Long PHVS / Short BCRX) is untested. |
| PT range and gap | **$22-27**, a gap of **-13% to -29% (midpoint -21%)** against $31. Model base $21.5; probability-weighted $23-25. |
| P(right) | **0.55** (price at or below $27 in 12 months). My scenario weights give 67% for bear plus base, which I cut to 55% because the model's evidence is weak. |
| Expected alpha | 0.55 x 21% - 0.45 x 35% = **-4.2%** (adverse move +35%, the blend of the bull and takeout states). Break-even P(right) is about 63%. Without the haircut, the unadjusted scenario weights (67%) give a positive number, but that rests on assumptions I cannot source. |
| Carrying pillar | XR (prophylaxis) share at peak: the price needs about 26% (1.44 times my base of 18%); evidence 2 of 5. |
| Kill criteria (for the Short or Avoid view) | (1) A takeout bid or credible report. (2) CMS Q2 2026 data (expected late October to November) showing combined oral plus icatibant claims growing sharply, which would mean the on-demand pool is expanding and not swapping. (3) Pharvaris guidance of net price at or above $450K per patient-year. (4) Full CHAPTER-3 data (ACAAI) showing clean liver data and attack-free rates above the injectables. (5) A close above $38 without news (data pop recovered). (6) Lonvo-z CRL or a narrow label on 2027-03-10 (it raises the share available to XR). Kill criteria for a Long: a raise below $25; an IR CRL on 2027-04-23; Takhzyro and Andembry prices cut with step-through rules that favor injectables. |
| Q&A defensibility (team with no biology) | **Moderate (3 of 5).** The strongest slide is the reverse DCF: "The market is paying $1.84B, which needs about $1.1B of peak sales. The company we compare it to, KalVista, was sold for $1.9B on a $705M plan." That needs no biology. The weak point is the share assumptions, which are opinions; a judge will ask "why 18%?" and the honest answer is "a new entrant took 10% in a year (Andembry), and an oral may take more." The team should also be ready for "what if someone buys it?", which the 10% takeout state answers, and should avoid claiming the Short is high-conviction. |

**Caveats.** (1) Evidence on XR share is a cross-trial comparison, not a head-to-head. (2) Takhzyro 2025 revenue and dilution intent are not verified. (3) Several sources were read through search summaries or mirrors, as marked. (4) The rNPV outputs shift materially with margin and ex-US inputs. (5) Per the project rule I did not run `graphify update` since no code in the project was changed, only research files were added.
