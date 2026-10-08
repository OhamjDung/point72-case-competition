# FTAI Aviation (FTAI) Short: Stress Test

Prepared 2026-10-06 for the Point72 Academy pitch (due 2026-10-12). Public sources only. Prior work is in `trail.md` and the CSVs in this folder and is not repeated. Price $179.44, market cap $18.43B, EV $21.59B, 102.71M shares, net debt $3.16B (stockanalysis.com/stocks/FTAI/statistics, 2026-10-06). Items marked [UNVERIFIED] could not be tied to a primary source.

## Part 1. Smoke tests

**S1. Adjusted FCF definition; does it exclude the SCI investment? FAIL as stated for 2026; the FY25 gap stays open.**
No filing defines Adjusted FCF. The Q2-26 8-K release (https://www.sec.gov/Archives/edgar/data/1590364/000162828026050622/ftai6302026earningsrelease.htm, 2026-07-29) contains no free-cash-flow reconciliation; its only non-GAAP measure is Adjusted EBITDA. The one release that reconciled it (Q2-25, per trail.md) defined it as CFO + CFI plus a $10.0M QuickTurn JV adjustment. On the Q2-26 call (2026-07-30; Investing.com transcript, https://www.investing.com/news/transcripts/earnings-call-transcript-ftai-aviation-q2-2026-eps-miss-clouds-strong-revenue-growth-93CH-4824650) CFO Nicholas McAleese said: "In the first half of the year, we generated $255 million of adjusted free cash flow, which included funding the final $95 million capital call under our 2025 SCI equity commitment." So in 2026 the SCI cheque is deducted and 1H26 CFO+CFI is $250.4M against $255M reported. The "excludes SCI" claim is therefore not supported for 2026. What survives: the FY25 headline of $724M is $311M above CFO+CFI ($412.6M) and no primary source reconciles it; trail.md shows two add-back reconstructions (unconsolidated-entity investment of about $301M, or named growth spend), either of which means the definition moved between years. Further, McAleese said a capital call facility for the 2026 SPV "will bridge a substantial portion of FTAI's equity co-investment funding into 2027", so 2026 SCI II funding is being deferred, not excluded. Company conversion claim: "about 60% to 70% of EBITDA" (same call). CFO+CFI is 35% (FY25) and 41% (1H26) of Adjusted EBITDA (cfo_fcf_bridge_annual.csv).

**S2. Gains in Adjusted EBITDA? PASS.**
The release defines Adjusted EBITDA as net income adjusted for taxes, equity comp, transaction costs, impairments, D&A, interest and similar items, plus pro-rata JV EBITDA; gains on sale are not among the exclusions (same 8-K). Gains (sale of assets + sales to the 2025 Partnership + Russian insurance recoveries) as a share of Adjusted EBITDA: FY24 $377.9M / $862.1M = 44%; FY25 $478.2M / $1,190.9M = 40% ($423.9M, 36% excluding insurance); 1H26 $245.1M / $617.0M = 40% ($195.6M, 32% excluding insurance) (gains_vs_ebitda.csv, from 10-K/10-Q cash flow statements). Share is falling in sale-gain terms, which undercuts the 80% Muddy Waters figure (Jan 2025) but leaves about a third of EBITDA as transaction profit.

**S3. Related-party (2025 Partnership) revenue. PASS, and rising.**
MRE sales to the 19%-owned Partnership: FY25 $335.8M (sum of quarters 100.6/69.6/58.7/106.9), 17.3% of Aerospace segment revenue of $1,936.2M; 1H26 $404.0M, 25.0% of $1,618.8M (aerospace_margin_quarterly.csv from 10-Qs; Q1-26 peak 29.7%). Separately, $530.0M of aircraft sales to it in FY25 and $175.7M in 1H26 sit in investing cash flow with $46.4M and $17.6M of gains, partly eliminated by $16.6M of profit elimination in 1H26 (8-K above).

**S4. Aerospace EBITDA margin trend. PASS.**
35.9% (Q1-25), 33.6%, 34.8%, 34.6%, 29.9% (Q1-26), 28.5% (Q2-26). Management: "for what we classified as the near term, which I would say is probably 1-2 years, we expect margins to be around 30%" (Joe Adams, Q2-26 call). EBITDA per module fell from $0.896M to $0.844M year on year while revenue per module rose (trail.md).

**S5. Anything since Q2 that discloses or refutes the thesis? Nothing decisive.**
Shares fell 6.2% on 2026-09-24 to $174.53 and 4.5% on 2026-09-28 to $167.10 (GuruFocus, https://www.gurufocus.com/news/9100553/is-ftai-aviation-ltd-ftai-a-bargain-after-45-drop-gf-value-says-undervalued); no catalyst identified. Stock then closed at $179.44 on 2026-10-06. The Q3-26 report is expected 2026-10-28 (EarningsWhispers via search result; after the Oct 12 deadline). Consensus 12-month target about $368 (stockanalysis.com, 10 analysts, Strong Buy); BTIG $340 and a Stifel upgrade (Yahoo Finance, Tipranks, dates [UNVERIFIED]). A source showing $217 on NASDAQ conflicts with the $179.44 close and is treated as stale. No new short report found; the only short reports are Muddy Waters (2025-01-15) and Snowcap (2025-01-29). The market is therefore not already pricing the cash conversion issue: analysts are far above the price.

## Part 2. Ablation

**Method.** Valuation on 2027 Adjusted EBITDA guidance of $2.3B (Aerospace Products $1.4B, FTAI Power $450M, Aviation Leasing $450M; Q2-26 8-K, 2026-07-29), a sum-of-the-parts EV/EBITDA blended 50/50 with an FCF-yield value, net debt $3.16B, 102.71M shares (stockanalysis.com, 2026-10-06). Peer TTM EV/EBITDA and FCF yield, stockanalysis.com/stocks/{ticker}/statistics, 2026-10-06: HEICO 30.2x / 2.4%; GE Aerospace 28.9x / 2.6%; AerSale 17.4x / -16.7%; AAR 13.8x / 3.3%; StandardAero 11.7x / 3.2%; Willis Lease 8.2x / -9.6%; GE Vernova (Power reference) 67.7x / 4.5%; FTAI itself 21.7x / -5.2%. Chosen multiples (my judgement, not sourced): Aerospace 18x (between the MRO group at 12-17x and the OEM-parts group at 29-30x), Power 10x, Leasing 8x (Willis Lease), FCF yield 4.5% on equity (peer median about 3%, plus a leverage and Power-risk premium). Thesis inputs: 45% EBITDA-to-FCF conversion (company claims 60-70%; CFO+CFI measure 35-41%); $350M of Aerospace EBITDA being gains valued at 8x; a 30% haircut to the 25% of Aerospace EBITDA tied to the Partnership; Aerospace margin 27% instead of the guided 30%; Power delivered with probability 50%. Model script: not saved to the project; all inputs are above so it can be rebuilt. Full table in `ablation_table.csv`.

| Pillar | With | Without | Delta | Evidence (1-5) | Insight? |
|---|---|---|---|---|---|
| Consensus-style (no pillars) | $308.5 | n/a | n/a | n/a | Reference (sell-side mean target is about $368) |
| Full thesis, Power p=50% | $198.3 | n/a | n/a | n/a | Still 10.5% above the $179.44 price |
| P1 FCF definition gap | 198.3 | 243.2 | +44.9 | 3 | Yes, largest swing; only FY25 gap unproven |
| P2 gains in EBITDA | 198.3 | 215.3 | +17.0 | 4 | Partly; verified, but declining |
| P3 related-party haircut | 198.3 | 207.5 | +9.2 | 3 | No |
| P4 margin compression | 198.3 | 210.5 | +12.3 | 4 | No; guide already about 30% |
| P5 Power (counter) | 198.3 | 220.2 | +21.9 | 2 | Yes; sets break-even |

**Reading.** The central finding is that the thesis does not generate a price below today's. The market already values FTAI at 9.4x 2027 guided EBITDA, so it is discounting guidance heavily; my thesis case, with every pillar on, still gives $198. The pillars overlap (gains and related-party profit are partly the same dollars), so adding the deltas overstates the total. Removing P1 matters most, but P1 is the weakest-evidenced as a valuation input because the 2026 definition ties to CFO+CFI and the FY25 gap may reflect a one-off definition.

## Part 3. Counter-case

Quantified bull items per share: Power at the $450M guide and 10x is $43.8 (at the $750M upside figure, $73.0); a 10% beat on Aerospace guide (CFM56 shop-visit demand, which GE and Safran indicate stays elevated through 2027-28; trail.md Door 6) is $24.5 at 18x; SCI II, a $6B target vehicle with FTAI committing 15% (Q2-26 call), is worth about $7 if it adds $60M of fee EBITDA at 12x (the $60M fee estimate is [UNVERIFIED], my assumption). A full bull case (Aerospace +10%, Power $750M, SCI II fees, 60% conversion) gives about $355, close to the sell-side mean of about $368.

**Break-even Power probability.** With every thesis pillar on, value is $176.4 with Power at zero and rises $10.9 per 25 points of probability. The short breaks even at a Power probability of about 8%. In other words the short works only if Power is almost entirely worthless and every other pillar also holds. Against the evidence: the $1.465B purchase order (J&F Power Systems, FTAI-Jereh joint venture, 2026-07-22 press release) carries an advance payment and milestones, so a 92% chance of fully failing is not credible; the open questions are FTAI's share of the JV and Chinese-ownership policy risk (trail.md Door 4).

## Verdict

- **Viable?** N (as a 12-month standalone short).
- **Direction:** do not pitch an outright short. If the competition requires a call, the data favour Long or No Position; the thesis is better framed as a monitored risk with an event trigger (Q3 10-Q, 2026-10-28).
- **PT range and gap:** short-case price targets $151 (severe bear: Aerospace 12x, Power zero) to $165 (bear: 14x, Power 10%), gap 8-16% below $179.44. Probability-weighted value (10% at $151, 20% at $165, 40% at $243, 30% at $355) is about $252, 40% above the price.
- **P(right):** about 30% for the short.
- **Expected alpha** = P x gap - (1-P) x adverse = 0.30 x 10.6% - 0.70 x 62% = about -40% (adverse move: base case +35%, bull +98%, weighted). Static valuation, no time discount; treat the sign, not the size, as the finding.
- **Carrying pillar:** none carries it. P1 (FCF conversion, 35-41% against a claimed 60-70%) is the strongest argument and would carry a short only if the FY25 $724M cannot be reconciled and 2H26 FCF (needs about $625M against $255M in 1H26) misses.
- **Kill criteria:** cover or abandon if (a) Q3-26 FCF tracks toward the $878M guide, (b) the J&F joint venture is consolidated or customer deposits step up, (c) Aerospace margin stabilises at 30% or above with module count above 296, (d) another Power order or Power guide above $450M, or (e) the company publishes a full Adjusted FCF reconciliation that ties to FY25. Next hard test: Q3-26 report, expected 2026-10-28.
