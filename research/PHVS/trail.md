# PHVS (Pharvaris) - Lead-Following Investigation Trail

Prepared 2026-10-06 for the Point72 Academy stock pitch (12-month Long/Short, deadline 2026-10-12). Public sources only (SEC EDGAR, company IR, CMS, ClinicalTrials.gov, reputable news). No one was contacted. Every number carries a source and an as-of date; anything I could not pin to a primary source is tagged **[UNVERIFIED]**. Prices come from Yahoo Finance's public chart endpoint (daily closes, pulled 2026-10-06). Working files are saved next to this memo as CSVs.

**Bottom line up front.** My lean is Long with low conviction (2 of 5). Three things changed my view of the screen. First, the Ekterly "slowdown" is real but smaller and different from how the screen framed it: the oral on-demand pool appears to be mostly swapping generic icatibant for Ekterly at a much higher price, not growing. Second, the insider selling is not mostly a 10b5-1 story: 88% of the shares sold were not flagged as plan sales, and 600K of them went out in one block at exactly $35.00 through one broker. Third, the whole post-data pop has been given back and the HAE complex has de-rated together, which points at a sector re-pricing rather than a PHVS-specific problem. The prophylaxis data (87% in HAE type 1/2) is better than anything oral on the market and is the real value driver. Financing and the Intellia decision are the two main risks.

---

## (A) Investigation Trail

### Thread 1: Ekterly (KalVista) launch, "is it slowing, and what does it say about oral on-demand?"

1. **Searched KalVista's XBRL and filings for the revenue series the screen quoted ($13.7M, ~$35M, $40.9M).** Found that the $40.9M is *total* revenue. Net *product* revenue in Q1 CY26 was $39.165M, and $1.698M was partnership revenue from a Kaken shipment and deferred-revenue amortization ([10-Q for 3/31/26](https://www.sec.gov/Archives/edgar/data/1348911/000119312526223976/kalv-20260331.htm), filed 2026-05-14). Q3 CY25 product revenue was $13.692M ([10-Q](https://www.sec.gov/Archives/edgar/data/1348911/000119312525274442/kalv-20250930.htm)). The eight-month transition period to 12/31/25 was $49.1M ([10-KT](https://www.sec.gov/Archives/edgar/data/1348911/000119312526124232/kalv-20251231.htm)), so Q4 was about $35.4M. That makes the like-for-like sequence $13.7M, $35.4M, $39.2M. Q1 grew about +11% q/q, not the +16-18% in the screen. **This changed my view slightly**: the revenue is lower than the headline suggests, but the deceleration is also less abrupt than +158% to +16%, because Q4 included launch stocking and refill ramp. Q4 and Q1 both include small German sales that the filings do not separate.
2. **Raised the question: was Q4 inflated?** Checked KalVista's 2026-01-08 release ([8-K ex 99.1](https://www.sec.gov/Archives/edgar/data/1348911/000119312526007801/d11988dex991.htm)). It says refills surpassed initial prescriptions in Q4, "with some activity potentially reflecting demand pulled forward ahead of the holidays." So the Q4 base was flattered, and Q1's +11% is on a pulled-forward base. Door: partially CLOSED (see item 4 for what CMS adds).
3. **Checked patient start forms.** Cumulative US start forms were 460 (2025-08-29), 937 (2025-10-31), 1,318 (2025-12-31) and 1,702 (2026-02-28), with prescribers going 253, 423, 580, 724 (sources in `ekterly_launch_metrics.csv`; [3/25/26 release](https://www.sec.gov/Archives/edgar/data/1348911/000119312526122784/d127514dex991.htm)). New-form adds per week went about 57, 53, 44, 44. That is a plateau, not growth, and it is on a base where start forms include free Quickstart supply (the Sept 2025 release said all 460 forms had Quickstart access; I saw that only in a search summary, so treat it as secondary). 1,702 forms is "almost 20%" of the US patient population per KalVista, which implies about 8,500-9,000 diagnosed US patients (my arithmetic from their statement). **This is the most important driver finding**: new-patient adds have flattened while the cumulative pool is only 20% penetrated by *forms*, and paid patients are fewer than forms.
4. **Cross-checked with government data (Door 7, level 2).** CMS Part D quarterly spending shows Ekterly at 228 claims / $17.1M gross for all of 2025 and 175 claims / 91 beneficiaries / $12.8M gross in Q1 2026 alone ([CMS Quarterly Part D Spending by Drug, release 2026-07](https://data.cms.gov/sites/default/files/2026-07/QDD_PTD_RQ2603_P01_V10_DQT2601_20260708.csv)). Medicaid State Drug Utilization Data (national "XX" rows, FFS+managed care) shows Ekterly prescriptions rising from 56 (Q4 25) to 120 (Q1 26), $2.68M to $6.75M ([Medicaid SDUD 2025/2026](https://data.medicaid.gov/)). In the same data, icatibant prescriptions (Firazyr + generics + Sajazir) fell from 454 (Q1 25) to 366 (Q1 26) in Medicaid, a drop of 88 against Ekterly's +120. In Part D, icatibant claims were 968 per quarter on average in 2025 and 851 in Q1 26, while Ekterly added 175. So combined on-demand claims are up only about 6-7% in either program, and Ekterly's gain is roughly three quarters offset by lost icatibant claims. **This changed my view**: the oral on-demand "pie" looks flat; Ekterly is mostly a share-take from generic icatibant, with some net addition. Caveats: Q1 is seasonally soft, SDUD omits suppressed small cells, and Part D/Medicaid are about a quarter to a third of volume. Door: CLOSED on direction, OPEN on magnitude.
5. **Followed that into price.** A Medicaid unit (one 300 mg tablet) was reimbursed at about $8,440, versus about $751 for a generic icatibant syringe (Q1 2026 SDUD national totals). KalVista's state price filings show a WAC of $35,614 per 4-tablet carton as of May 2026, up from $33,440 in July 2025 ([KalVista Colorado WAC disclosure](https://www.kalvista.com/wp-content/uploads/2026/05/Colorado-WAC-Disclosure-Ekterly-updated-20260504.pdf), search-result snippet; I did not open the PDF itself **[UNVERIFIED]**). If an attack uses two tablets (KONFIDENT tested 300 mg and 600 mg; confirm the label dose **[UNVERIFIED]**), Ekterly costs about $16-18K per attack against well under $1K to $3K for icatibant, and Part D gross cost per claim is about $73-75K for Ekterly against about $13-15K for generic icatibant. That is a 5-20x per-attack premium depending on program. That explains the payer behavior: KalVista said coverage was mostly via medical exception and some payers required step-through of generic icatibant (Q1 FY26 call summary, secondary source). **This is the core payer lesson for PHVS's April 2027 label and price.**
6. **Gross-to-net.** KalVista does not disclose it. The 10-KT lists the deductions (government rebates, copay assistance, prompt-pay discounts, distribution fees, returns) but gives no percentages. The only quantitative hint is the "product revenue related reserves" accrual of $6.96M at 3/31/26 versus $4.75M at 12/31/25 (10-Q Note 6), which is not enough to back out a rate. Door: DEAD END for a hard number. For modeling I would use an assumed range of 25-40% **[assumption, not sourced]**.
7. **Read the SC 14D9 for the long-range forecast** ([SC 14D9, filed 2026-05-13](https://www.sec.gov/Archives/edgar/data/0001348911/000114036126021078/ny20073033x1_sc14d9.htm)). Management projections (updated after Q1) are net revenue of $185M in 2026, $279M in 2027, $350M in 2028, $446M in 2029, $601M in 2030, a plateau around $590-710M through 2038 (peak $705M), and loss of exclusivity in 2039 (US) and 2037 (EU). The footnote says the 2026 figure was moved from $183M to $185M after Q1. **This changed my view of the screen's framing**: the "$185M case" is not a stale pre-launch curve that Q1 missed. Management saw Q1 and still expected Q2-Q4 of about $144M (about $48M per quarter, +18% over Q1 total revenue of $40.9M). Whether that was achieved is unknown, because Chiesi closed the deal on 2026-06-11 and KalVista stopped filing, so there is no Q2 print. Discount rate 11.5-13.5%; Centerview's DCF is the $19.50-$21.70/share the screen cites **[from screen; I did not re-derive]**.
8. **Chiesi integration timing.** Searched for any post-close Ekterly disclosure. Found none: Chiesi is private, and KalVista's last periodic filing is the 5/14 10-Q. Door: DEAD END (no Q2/Q3 data). Next best proxy is Part D/Medicaid Q2 data when CMS posts it (expected about Oct-Nov 2026 for Part D quarterly) and Google Trends.
9. **A branch with a real read-through: the sale process.** The 14D9 background names at least four interested parties: the winner (Chiesi), plus Party A (a global pharma that had been in contact since Nov 2023), Party B (which bid in the mid-to-high $20s) and Party D. Management told bidders a deal would be in the "high $20s." The price paid, $27 (a 36% premium to the 4/28 close, per [Pharmaceutical Technology](https://www.pharmaceutical-technology.com/newsletters/chiesi-widens-rare-disease-portfolio-with-1-9bn-kalvista-buyout)), shows that several strategics value an *on-demand-only* oral at about $1.9B. That is the strongest bull argument for PHVS (M&A floor, and a pool of at least three disappointed bidders), and it undercuts the Short case. Door: CLOSED, flagged as a floor argument.
10. **How does an oral on-demand HAE market size up?** Using only sourced inputs: about 8,500-9,000 diagnosed US patients (derived above); a per-attack WAC of about $17.8K; an assumed GTN of 25-40%, so about $11-13K net per attack. KalVista's $705M peak US+EU net revenue implies roughly 50-60K attacks treated per year in total at those prices, or about 6 attacks per diagnosed US patient if all of it were US and every patient used it. That is plainly a ceiling, and it suggests the management peak assumes almost universal switching or heavy ex-US sales. Note that this is my arithmetic from stated inputs, and the ex-US share of KalVista's peak is not split in the 14D9. Door: OPEN for refinement in Phase 2.

### Thread 2: Prophylaxis market, growth or rotation? (Door 2)

11. **Pulled each drug's latest revenue.** Orladeyo (BioCryst): Q1 25 $134.2M, Q2 $156.8M, Q3 $159.1M, Q4 about $151.7M (derived from FY25 $601.8M), Q1 26 $148.3M, Q2 26 $158.2M ([Q2 26 release](https://www.sec.gov/Archives/edgar/data/882796/000117184326005223/exh_991.htm), 2026-08-05). BioCryst sold its European business on 2025-10-01, so reported growth is distorted. Management's like-for-like growth is +43% for FY25, +21% in Q1 26 and **+10% in Q2 26**, with the FY26 guide at $625-645M. Dawnzera (Ionis): Q1 26 about $16M (derived), Q2 26 $26M (+63% q/q), FY26 guide $110-120M ([Ionis Q2 release](https://www.sec.gov/Archives/edgar/data/0000874015/000114036126029960/ef20078953_ex99-1.htm)). Andembry (CSL): $240M in FY26 (July 2025 to June 2026), its first full year ([CSL FY26 results](https://investors.csl.com/pdf/80148cbc-d117-4b5c-9213-628b0d1de681/Platform/ListPage/CSL-FY2026-Results.pdf)); no quarterly split. Takhzyro (Takeda): reported at JPY 59.9B for April-June 2026, **-2.2% at constant exchange rates** per a search summary of Takeda's release; Takeda's own press release text did not contain the product line, so tag **[UNVERIFIED]** until I read the data book.
12. **Cross-checked with CMS.** Medicaid Takhzyro prescriptions were 712 in Q1 26 versus 798 in Q1 25 (-11%) and $31.4M versus $35.8M (-12%); Orladeyo 366 versus 341 (+7%) and $17.4M versus $14.7M (+18%); Andembry 102 to 159 and Dawnzera 44 in its first Medicaid quarter. In Part D, Takhzyro Q1 26 gross spend was $58.5M versus a 2025 quarterly average of $67.3M (-13%), Orladeyo $49.8M versus $45.1M (+10%). Gross Part D cost per beneficiary is about $450K per year for both Takhzyro ($269.2M / 596) and Orladeyo ($180.3M / 405), which is the price anchor for any XR launch. **This changed my view**: Takhzyro, the largest drug, has stopped growing in two independent public datasets plus Takeda's own report, Orladeyo's growth is decelerating fast, and the new entrants (Andembry about $240M/yr, Dawnzera about $100M/yr run-rate) are the growth. That reads as share rotation with modest net market growth, not an expanding pie. Caveat: Q1 is seasonally weak in Part D and the 2025 Part D out-of-pocket redesign confounds the 2024-to-2025 jump (Orladeyo gross Part D spend roughly 2.3x); I do not splice the annual and quarterly files.
13. **Pivotal data comparison (cross-trial caveats).** CHAPTER-3 (n=85, 2:1, XR 40 mg daily, 24 weeks) showed an 83% reduction overall and 87% in type 1/2 (n=80) ([HCPLive](https://www.hcplive.com/view/deucrictibant-xr-meets-primary-endpoint-hae-prophylaxis); [Pharvaris 6-K 2026-09-08](https://www.sec.gov/Archives/edgar/data/1830487/000119312526384339/6-k_september_8_2026.htm)). Comparators: HELP, lanadelumab 300 mg q2w: 87%; VANGUARD, garadacimab: about 87-89% (sources conflict at 87 versus 89.2 depending on adjustment); OASIS-HAE, donidalorsen: 81% (q4w) and 55% (q8w), weeks 1-25 ([Ionis](https://ir.ionis.com/node/31276)); APeX-2, berotralstat 150 mg: 1.31 versus 2.35 attacks per month, i.e. about 44%. HAELO, lonvo-z (type 1/2 only): 87%, with 0.26 versus 2.10 attacks per month ([Intellia Q2 release via BioSpace](https://www.biospace.com/press-releases/intellia-therapeutics-announces-second-quarter-2026-financial-results-and-business-updates)). Caveats: different baselines, run-in rules, endpoints (weeks 1-25 versus 5-28), populations (CHAPTER-3 includes normal C1-INH HAE, the others do not), sample sizes (30 placebo patients here), and 24 weeks of follow-up. **Takeaway: on an apples-to-apples type 1/2 basis, an oral at 87% is injectable-class and roughly double Orladeyo's 44%.** That is the strongest piece of evidence for the Long case, and RBC's downgrade of BioCryst to Sector Perform on this data (PT $13 to $11) is the market agreeing ([StockTwits summary of RBC note](https://stocktwits.com/news-articles/markets/equity/bcrx-stock-heads-for-fifth-straight-day-in-the-red-rbc-capital-says-bio-cryst-faces-a-challenging-near-term-outlook/cZtaLEXRJ67), secondary).
14. **Cross-trial sanity check on on-demand speed.** RAPIDe-3 median time to symptom relief was 1.28 hours (screen; [HCPLive](https://www.hcplive.com/view/pharvaris-deucrictibant-provides-rapid-relief-hae-phase-3-rapide-3-trial)). KONFIDENT sebetralstat median time to beginning of symptom relief was 1.61 hours (300 mg) and 1.79 hours (600 mg) against 6.72 hours placebo, per KalVista's 10-Q. Different endpoint definitions and placebo behavior (placebo exceeded 12 hours in RAPIDe-3), so a roughly 0.3-0.5 hour edge is not a clean win. Door: CLOSED as "weak differentiation on speed, not decisive."

### Thread 3: Intellia's one-time therapy (Door 3)

15. **Pivotal data.** HAELO (n=80, single 50 mg infusion, 2:1): 87% fewer attacks than placebo (weeks 5-28), mean 0.26 versus 2.10 per month; 62% attack-free and therapy-free versus 11%; 91% reduction in moderate/severe attacks; no serious adverse events in the lonvo-z arm; all events Grade 1-2 ([Intellia Q2 release](https://www.biospace.com/press-releases/intellia-therapeutics-announces-second-quarter-2026-financial-results-and-business-updates); [10-Q for 6/30/26](https://www.sec.gov/Archives/edgar/data/0001652130/000119312526337952/ntla-20260630.htm); NEJM publication June 2026). BLA accepted with Priority Review, **PDUFA 2027-03-10**, no advisory committee planned, launch planned 1H 2027 ([Intellia 8-K, 2026-09-08](https://www.sec.gov/Archives/edgar/data/0001652130/000119312526385194/ntla-20260908.htm)).
16. **Searched for safety signals (liver).** Found the sister program, nex-z, had a Grade 4 liver transaminase and bilirubin event in the MAGNITUDE trial, an FDA clinical hold on 2025-10-29, and a patient death on 2025-11-05 (septic shock after a perforated duodenal ulcer, with acute liver injury and steroid treatment in the course). Holds were lifted in January 2026 (MAGNITUDE-2) and March 2026 (MAGNITUDE). In August 2026 Intellia and Regeneron reported that the highest liver enzyme elevations clustered in carriers of one HLA allele, based on more than 600 samples, and the company is discussing that with FDA ([10-Q](https://www.sec.gov/Archives/edgar/data/0001652130/000119312526337952/ntla-20260630.htm)). Lonvo-z uses the same lipid-nanoparticle platform but had no serious or liver events in HAELO (a search summary said "no liver abnormalities"; I did not find that in a primary document **[UNVERIFIED]**). **Question raised**: could an HLA-linked liver label constraint also hit lonvo-z? I found no evidence it does. Door: OPEN (read the HAELO NEJM supplement and the eventual label).
17. **Price.** No price has been disclosed. Intellia says payers are "very constructive," often benchmark one-time therapies as a multiple of annual cost, and that aggressive pricing risks step edits (Q4 25 call summary, secondary). Annual cost of chronic prophylaxis is about $450K per patient in Part D gross data (item 12). Gene-therapy precedents are in the $2-3.5M range **[from memory, UNVERIFIED]**. My working assumption is $2-3M, i.e. 4-7 years of chronic therapy at gross prices. Door: OPEN until the FDA decision and launch.
18. **How many prophylaxis patients could it take?** No primary-source figure exists. With about 8,500-9,000 diagnosed US patients, one infusion procedure that is irreversible, ages 16 and up, type 1/2 only, and cash of $628.4M with runway "into 2028," a launch of a few hundred patients in year one is plausible. My scenario (explicitly an assumption, **[UNVERIFIED]**): 1-3% of diagnosed patients in year 1 (roughly 85-260) and 5-10% cumulative by year 3. The main brakes are payer step edits, patients stable on current therapy, and caution about an irreversible edit with five-plus years of follow-up at most. Implication for PHVS: lonvo-z competes mainly for the prophylaxis pool that XR targets, but capacity and uptake limit the near-term effect; the stock effect is therefore sentiment and label-driven around 2027-03-10.

### Thread 4: Insider selling (Door 4)

19. **Pulled the EDGAR submissions JSON for CIK 1830487 and parsed every Form 144 and Form 4 since 2026-08-01** ([submissions](https://data.sec.gov/submissions/CIK0001830487.json); files in `form144_notices.csv`, `form4_transactions.csv`). Sixteen Form 144 notices were filed 9/8-9/23, covering **857,210 shares**; summing the executed Form 4 sales gives exactly 857,210 (557,210 coded S plus Schoodic's 300,000, see item 21), worth about $30.8M. Every notice was executed. There were no open-market purchases (no code P anywhere in the August-September Form 4s). Only one gift (500 shares by the CFO) besides sales.
20. **10b5-1 question.** Form 144 shows a plan adoption date for only two filers: Peng Lu (2025-08-19) and CEO Modig's RSU sales (2025-12-15). The Form 4 checkbox for Rule 10b5-1 is ticked only for transactions filed through 9/17, covering Lu's 15K-share weekly pairs, Glassman, Lesage, Souverijns and Modig's small RSU sells: **105,048 shares, 12%**. The other **752,162 shares, 88%**, were not flagged as plan sales. A cross-check of Lu's own Form 4 text: "This is a scheduled exercise and sale from 10b5-1 trading plan" for 9/8, but his 9/17 sale of 100,000 shares is un-flagged. Door on "were they 10b5-1": CLOSED. Mostly no.
21. **The block.** On 2026-09-17, three insiders sold **600,000 shares at exactly $35.00**: Schoodic Management BV (CEO Modig's vehicle) 300,000, director Johannes Schikan 200,000, Lu 100,000. That day PHVS closed at $38.00 with a low of $37.60, so $35.00 was about 8% below the market, and the Form 144 values were already a flat $35.00 when filed. All three Form 144s name the same broker (Morgan Stanley Smith Barney LLC Executive Financial Services). This is a negotiated block, not trickle selling. Modig's Form 4 codes the Schoodic disposal as "M" with a disposal flag (a mis-coding; Schoodic's holdings fall from 950,000 to 650,000 per the 20-F and the Form 4). Other sales that week were at $37.80-$38.60 on the open market. **This changed my view**: the screen read it as clustered discretionary selling after a pop; the record shows a single negotiated discount block of 600K shares (about 0.9% of shares outstanding) plus about 257K of routine option-exercise sales. A block of that size is typically placed with an institution, which is mildly supportive of institutional demand at $35, but the stock has since fallen below that price, so whoever bought it is under water. I could not identify the buyer; no new 13D/13G has appeared (latest 13G/As were 7/31 and 8/14). Door: OPEN on the buyer, CLOSED on structure.
22. **Size versus holdings (20-F beneficial ownership at 2026-03-17, [20-F](https://www.sec.gov/Archives/edgar/data/1830487/000183048726000013/phvs-20251231.htm)).** Modig sold 300K+ of 1,684,167 (about 18%); Schikan 200.8K of 487,355 (41%); Lu 130K of 518,122 (25%); Glassman 31.2K of 107,355 (29%); Lesage 50K of 500,467 (10%); Souverijns 26.1K of 288,824 (9%); Bjork exercised and sold 52.5K and ended with 15,167 shares; CFO Nassif 6K. The beneficial totals include options, so percentages of *shares owned* are higher for the exercisers. CEO and CFO still hold large positions (Modig holds about 650K through Schoodic plus about 128K directly after sales). Also, Schikan has a 144/A on 9/22 amending a 6/30/26 sale, so he sold in June too. Net: heavy proportional selling by a director and the President, none by the CEO beyond the block; no buying. It is a negative sentiment signal but not a thesis driver, and 857K shares is about 1.2% of shares outstanding.

### Thread 5: Why did the stock fall? (Door 5)

23. **Looked at the tape.** PHVS closed $35.25 on 9/4 (the last pre-data close), traded to $43.25 intraday on 9/8 on 6.3M shares, and closed $37.84. It then drifted to $31.12 on 10/6 ([daily closes, Yahoo Finance](https://query1.finance.yahoo.com/v8/finance/chart/PHVS), `phvs_price_window.csv`). **Correction to the screen: the stock is about 12% below its pre-data close, not just 25% below a post-data peak. The entire data reaction has been erased.**
24. **Checked for an equity offering.** None. EDGAR shows no 424B, no S-3/F-3 and no ATM since the 2026-05-08 424B5 ($29.68, $115M base, $132.3M with option). Door: CLOSED.
25. **Checked the Chiesi/KalVista read-through.** The deal closed 2026-06-11; no new news in September. Not the cause. Door: CLOSED.
26. **Checked peers and the sector for the same window (9/4 to 10/6).** XBI fell from $163.81 to $150.90 (-7.9%). BioCryst fell $9.96 to $7.95 (-20%), Ionis $58.09 to $44.00 (-24%), Intellia roughly flat ($12.74 to $12.37, -3%). PHVS fell 11.7%. So the HAE-related names fell roughly together after 9/8, with BCRX falling on the day of the data. **This changed my view**: PHVS is not uniquely weak; it is in a group that is de-rating, and the market may be pricing a smaller HAE profit pool (Ionis's decline, notably, began the week after the data and I did not find its cause **[UNVERIFIED]**). Other contributors I could document: the insider block at $35 on 9/17 and the 9/23 down day (-6.1%, no company news found; the Form 4s from 9/17 hit the tape 9/21-9/25). Door: mostly CLOSED; residual cause is sell-the-news plus sector.

### Thread 6: Pricing, runway, dilution (Door 6)

27. **Balance sheet.** Cash EUR 318.3M at 2026-06-30 (about $359M at 1.1269), no borrowings seen; Q2 operating loss EUR 47.8M (R&D 35.0M, G&A 15.8M); H1 operating cash outflow EUR 86.6M ([Q2 6-K](https://www.sec.gov/Archives/edgar/data/1830487/000119312526345702/phvs-ex99_1.htm), 2026-08-12). Company guides to runway "into 2028." The May raise added 7.6% to the share count versus year-end 65.2M.
28. **Stress-test the runway.** KalVista's first launch quarter SG&A was about $45M, and its SG&A reached $48.8M in Q1 26 against $12.4M of R&D (10-Q). If PHVS's G&A/SG&A steps from about $16M a quarter to $35-45M by 2027 while R&D stays near $35M, quarterly burn rises to about EUR 70-80M, and cash of EUR 318M less Q3-Q4 26 burn of about EUR 110M leaves about EUR 205M entering 2027, i.e. roughly 2.5-3 quarters. The company's "into 2028" therefore probably assumes slower spending or milestone income; an equity raise around IR approval (April 2027) or XR submission (1H 2027) is likely. Illustrative assumption, not a company forecast. A 10-15% raise at about $30 would be consistent with the last two raises. Door: OPEN (model burn explicitly in Phase 2).
29. **Pricing and gross-to-net analogs.** Ekterly WAC about $17.8K per attack (item 5); the chronic prophylaxis analogs are Orladeyo (about $1,695 per capsule Medicaid-reimbursed, roughly $600K+/year annualized) and Takhzyro (about $13.4K per unit, about $350K/year at q2w, Medicaid-reimbursed). Part D gross cost per beneficiary of about $450K supports an XR price near $450-600K gross. Pharvaris has given no pricing guidance (screen). GTN assumption of 25-40%, not sourced. Door: OPEN.

### Thread 7: CMS utilization data (Door 7)

30. **Located the datasets.** Medicaid SDUD annual files on data.medicaid.gov (2025 and 2026 posted; updated 2026-07-13) and CMS Part D Spending by Drug, both annual (DY24, posted 2026-06) and quarterly (through Q1 2026, release 2026-07-23). Pulled national "XX" state rows, which cover FFS plus managed-care utilization. Findings summarized in section C. **Takeaways:** (i) icatibant is shrinking in both programs while Ekterly grows; (ii) Takhzyro volume is declining in Medicaid and Part D; (iii) Orladeyo grows but more slowly in Q1 26 than in 2025; (iv) new entrants are small but growing. Door: CLOSED on direction; OPEN on Q2 26 data (not yet posted).

---

## (B) Revised variant hypotheses

**H1 (revised): Oral on-demand is a payer-constrained share-swap, not a growing pie; the Street is right on 2027 revenue, wrong if it gives on-demand a big terminal value.**
- For: combined icatibant+Ekterly claims up only about 6-7% in Part D and Medicaid; new-patient start forms flat at about 44/week; 5-20x per-attack price premium with step-through-icatibant edits; Q4 flattered by pull-forward; KalVista's own $705M peak implies near-universal switching.
- Against: management raised 2026 *after* seeing Q1; Ekterly Medicaid prescriptions doubled q/q; four bidders paid about $1.9B for on-demand-only; 2027 consensus for PHVS of about $32M is a low bar that does not depend on this.
- Status: supports "do not underwrite on-demand terminal value," not a standalone Short.

**H2 (revised): The prophylaxis opportunity is the thesis, and the March 10 Intellia decision is the sentiment pivot.**
- For: 87% in HAE type 1/2 is injectable-class and about twice Orladeyo's 44%; BCRX -20% and RBC's downgrade show the market sees Orladeyo share at risk; Orladeyo like-for-like growth already slowed from +43% to +10%; Takhzyro is flat to down, so share is available; XR NDA planned 1H 2027.
- Against: n=85 and 24 weeks; no head-to-head; five-plus competitors; Andembry (monthly) and Dawnzera are ramping; lonvo-z at 87% with 62% attack-free and a one-time infusion competes for exactly these patients; payers can step through generics and cheaper chronic drugs; XR is not yet filed so launch is no earlier than 2028.

**H3 (revised): The insider selling is a financing/liquidity signal, not a plan-driven routine; it is a weak negative with no purchases.**
- For: 88% not flagged as 10b5-1; 600K shares in a single $35.00 block through one broker at a roughly 8% discount; 41% of Schikan's and 25% of Lu's beneficial stake sold; no buys; the stock has fallen since.
- Against: 857K shares is 1.2% of shares outstanding; CEO and CFO retain large positions; many sales are option exercises (some expiring); block placed with an institution suggests demand; the market already knew (filings public).

**H4 (new): The post-data drift is sector de-rating plus supply, so the entry point is better than at the screen date.**
- For: price is 12% below the pre-data close with strong data in hand; no offering; group peers down 20-24%; PDUFA on IR is 2027-04-23, a low-risk approval.
- Against: no catalyst until about November Q3 results, Intellia on 3/10/27 and the PDUFA; a raise near approval is probable.

**H5 (new): Financing is the main medium-term risk to a Long: a raise of 10-15% around the IR approval is likely, and that is more likely than not before launch.**
- For: EUR 318M cash against a launch build modeled at EUR 70-80M a quarter by 2027; two raises in nine months; the company is on conferences; insiders sold.
- Against: company says runway into 2028; ex-US/royalty deals could lessen need; M&A could preempt a raise.

**Net view: Long, conviction 2/5.** The Short case in the screen (H1 and H3) is weaker than it looked, because the Ekterly "deceleration" is overstated and the insider pattern is a block, not a trend. The Long case rests on XR efficacy versus Orladeyo and a lower entry price, but is hampered by financing and a crowded prophylaxis field. A cleaner pitch would be a pair: Long PHVS, Short BCRX, which isolates the XR-versus-Orladeyo read. I have not tested that pair.

---

## (C) Data tables

All CSVs are in `C:\Users\Hi\Projects - Coding\Point72\research\PHVS\`.

### C1. HAE drug revenue by quarter ($M unless noted) - `hae_drug_revenue_by_quarter.csv`

| Period | Orladeyo (BioCryst) | Ekterly net product (KalVista) | Dawnzera (Ionis) | Andembry (CSL) | Takhzyro (Takeda) |
|---|---|---|---|---|---|
| Q4 2024 | 124.2 | - | - | - | n/a |
| Q1 2025 | 134.2 | - | - | - | n/a |
| Q2 2025 | 156.8 | - | - | - | n/a |
| Q3 2025 | 159.1 | 13.7 (launch 7/7/25) | - | - | n/a |
| Q4 2025 | 151.7 (derived) | 35.4 (derived; includes holiday pull-forward) | n/a | - | n/a |
| Q1 2026 | 148.3 (+21% ex-Europe) | 39.2 (+1.7 partnership) | 16 (derived) | - | n/a |
| Q2 2026 | 158.2 (+10% ex-Europe) | not public (acquired by Chiesi 6/11) | 26 (+63% q/q) | - | JPY 59.9B, -2.2% CER [UNVERIFIED] |
| FY2026 / guide | 625-645 (guide) | 185 total-revenue mgmt plan (14D9) | 110-120 (guide) | 240 (Jul 25-Jun 26 actual, first full year) | n/a |

Orladeyo Q1 25 to Q3 25 include European revenue (sold 2025-10-01), so y/y reported growth understates the US. Sources are in the CSV.

### C2. Ekterly launch metrics - `ekterly_launch_metrics.csv`

| As of | Cumulative US start forms | Unique prescribers | Adds per week since prior |
|---|---|---|---|
| 2025-08-29 | 460 | 253 | about 57 |
| 2025-10-31 | 937 | 423 | about 53 |
| 2025-12-31 | 1,318 | 580 | about 44 |
| 2026-02-28 | 1,702 | 724 | about 44 |

### C3. Form 144 notices (9/8-9/23; 16 notices, 857,210 shares) - `form144_notices.csv`

| Filed | Filer | Shares | Agg. value ($) | 10b5-1 plan date on Form 144 | Form 4 executed |
|---|---|---|---|---|---|
| 9/8 | Peng Lu (President) | 30,000 | 1,057,500 | 2025-08-19 | 15K at $40.68 (9/8) + 15K at $40.13 (9/11); 10b5-1 box ticked |
| 9/9 | R. Glassman (dir.) | 8,000 | 300,396 | none | 8,000 at $37.55; box ticked |
| 9/10 | A. Lesage | 30,000 | 1,149,084 | none | 30,000 at $38.30; box ticked |
| 9/14 | B. Modig (RSUs) | 2,291 | 87,104 | 2025-12-15 | 2,291 at $39.40; box ticked |
| 9/14 | W. Souverijns (CCO) | 26,090 | 1,023,583 | none | 20,000 at $39.31 + 6,090 at $38.99; box ticked |
| 9/15 | R. Glassman | 8,667 | 331,716 | none | 8,667 at $38.27; box ticked |
| 9/15 | S. Abele (CTO) | 46,400 | 1,771,125 | none | 45,000 at $38.14 + 1,400 at $39.24; box not ticked |
| 9/17 | R. Glassman | 14,493 | 558,812 | none | 14,493 at $38.56; box not ticked |
| 9/17 | GrayMatters (Lesage) | 20,000 | 765,466 | none | 20,000 at $38.27; box not ticked |
| 9/17 | E. Bjork (dir.) | 52,500 | 1,989,409 | none | 52,500 at $37.89; box not ticked |
| 9/17 | Schoodic Mgmt BV (Modig) | 300,000 | 10,500,000 | none | 300,000 at $35.00; mis-coded "M" |
| 9/17 | J. Schikan (dir.) | 200,000 | 7,000,000 | none | 200,000 at $35.00; box not ticked |
| 9/17 | Peng Lu | 100,000 | 3,500,000 | none | 100,000 at $35.00; box not ticked |
| 9/21 | D. Nassif (CFO) | 6,000 | 218,801 | none | 6,000 at $36.47; box not ticked |
| 9/22 | J. Schikan | 800 | 28,952 | none | 800 at $36.19; box not ticked |
| 9/23 | V. Monges (dir.) | 11,969 | 395,524 | none | 11,969 at $33.05; box not ticked |

Totals: 857,210 shares (about $30.8M) executed; 105,048 shares (12%) flagged 10b5-1; 752,162 (88%) not flagged; 600,000 in the $35.00 block (70%). Purchases: none. Brokers: Morgan Stanley Smith Barney LLC Executive Financial Services on the 9/8 and 9/17 notices I checked. Also note the screen's reconciliation question: the 9/8 144 value implies $35.25/share (a pre-trade estimate); the executed price was $40.68.

Holdings context (20-F, 2026-03-17 beneficial incl. options): Modig 1,684,167 (Schoodic 950,000); Lu 518,122; Schikan 487,355; Lesage 500,467; Souverijns 288,824; Glassman 107,355. Full Form 4 lines in `form4_transactions.csv`.

### C4. CMS Part D (gross drug spend, all plans) - `cms_partd_hae_drugs.csv`

| Drug | 2022 | 2023 | 2024 | 2025 (full year) | Q1 2026 | 2025 quarterly avg |
|---|---|---|---|---|---|---|
| Takhzyro | $192.1M / 4,189 claims | $194.4M / 4,162 | $223.0M / 4,752 / 512 benes | $269.2M / 5,607 / 596 | $58.5M / 1,249 / 476 | $67.3M |
| Orladeyo | $47.9M / 1,236 | $52.3M / 1,293 | $77.9M / 1,835 / 221 | $180.3M / 4,056 / 405 | $49.8M / 1,031 / 349 | $45.1M |
| Icatibant (generic) | $44.1M / 2,134 | $43.5M / 1,971 | $32.5M / 2,447 | $37.6M / 2,819 | $9.4M / 624 | $9.4M |
| Firazyr (brand icatibant) | $61.6M / 1,101 | $56.4M / 920 | $43.7M / 719 | $32.1M / 682 | $6.4M / 144 | $8.0M |
| Sajazir | $1.0M / 61 | $2.9M / 148 | $2.0M / 150 | $9.8M / 371 | $2.5M / 83 | $2.5M |
| Ekterly | - | - | - | $17.1M / 228 / 115 | $12.8M / 175 / 91 | n/a |
| Andembry | - | - | - | $23.2M / 309 / 99 | $19.3M / 308 / 124 | n/a |
| Dawnzera | - | - | - | $1.8M / 32 / 14 | $4.3M / 74 / 32 | n/a |

Caveats: annual (DY24) and quarterly files differ in vintage; I do not splice them. The 2025 out-of-pocket cap redesign inflates 2025 versus 2024. Q1 is seasonally soft. Spend is gross of manufacturer rebates. Source: [CMS Part D Spending by Drug (annual, 2026-06)](https://data.cms.gov/sites/default/files/2026-06/98218f98-166c-4723-8438-c344a4ef96a6/DSD_PTD_RY26_P04_V10_DY24_BGM.csv) and [Quarterly (2026-07)](https://data.cms.gov/sites/default/files/2026-07/QDD_PTD_RQ2603_P01_V10_DQT2601_20260708.csv).

### C5. Medicaid SDUD, national (FFS + managed care, unsuppressed rows only) - `cms_medicaid_sdud_national_quarterly.csv`

| Quarter | Takhzyro Rx / $M | Orladeyo Rx / $M | Icatibant family Rx / $M | Ekterly Rx / $M | Andembry Rx / $M | Dawnzera Rx / $M |
|---|---|---|---|---|---|---|
| Q1 2024 | 769 / 32.8 | 268 / 11.2 | 368 / 5.9 | - | - | - |
| Q1 2025 | 798 / 35.8 | 341 / 14.7 | 454 / 5.8 | - | - | - |
| Q2 2025 | 849 / 37.5 | 400 / 17.4 | 442 / 6.7 | - | - | - |
| Q3 2025 | 923 / 41.0 | 439 / 19.1 | 485 / 7.1 | not shown (suppressed) | - | - |
| Q4 2025 | 840 / 36.6 | 402 / 17.6 | 421 / 5.4 | 56 / 2.7 | 102 / 7.1 | - |
| Q1 2026 | 712 / 31.4 | 366 / 17.4 | 366 / 4.6 | 120 / 6.8 | 159 / 9.6 | 44 / 2.5 |

Q1 26 versus Q1 25: Takhzyro -11% Rx and -12% dollars; Orladeyo +7% Rx and +18% dollars; icatibant family -19% Rx and -22% dollars. Unit prices (Q1 26, Medicaid reimbursed): Ekterly about $8,441 per tablet; generic icatibant about $751 per syringe; Firazyr about $3,619; Orladeyo about $1,695 per capsule; Takhzyro 300 mg about $13,371 per unit. Source: [data.medicaid.gov State Drug Utilization Data 2024-2026](https://data.medicaid.gov/), queried 2026-10-06 using state = "XX" national totals. Suppressed small cells are omitted so some quarters are understated; Medicaid is a small share of volume.

### C6. PHVS price window - `phvs_price_window.csv`

| Date | Close | Note |
|---|---|---|
| 2026-09-04 | $35.25 | last pre-data close |
| 2026-09-08 | $37.84 | intraday high $43.25, 6.3M shares |
| 2026-09-17 | $38.00 | $35.00 block day |
| 2026-09-23 | $33.07 | -6.1% on the day |
| 2026-10-06 | $31.12 | about -12% versus 9/4 |

---

## (D) Phase-2 To-Do List

1. **Model the launch and the burn.** Build the quarterly cash model from the Q2 6-K: R&D, G&A, a launch SG&A ramp benchmarked to KalVista ($45M first quarter, $48.8M in Q1 26), and test whether "into 2028" survives. Size a raise as a function of the April 2027 approval and XR filing.
2. **Pull the real Takhzyro number.** Read Takeda's FY26 Q1 data book for Takhzyro revenue by region and growth; replace the [UNVERIFIED] search-summary figure. Get Andembry and Dawnzera quarterly splits (Ionis Q3/Q4 25 releases; CSL half-year release).
3. **Identify the 600K-share block buyer.** Watch for 13D/G and Q3 13F filings (due mid-November). Check the Form 4 footnotes and the 9/22 144/A. Confirm Schikan's June sale and whether a lock-up or underwriter relationship (Morgan Stanley led the May deal) explains the broker.
4. **Open the primary documents I only saw as snippets.** KalVista WAC PDF and the Ekterly label (dose, tablets per attack); BioCryst's and KalVista's gross-to-net disclosures; the Dawnzera and Andembry labels (attack rates in the label, not press releases); the HAELO NEJM supplement for liver enzyme details and exclusion criteria.
5. **Refresh CMS when posted.** Part D Q2 2026 and SDUD Q2 2026 (check data.medicaid.gov and data.cms.gov in late October and November). Specifically test whether Ekterly claims kept growing in Q2 and whether icatibant continued to fall. Add SDUD 2022-2023 NDC-level splits to separate brand versus generic icatibant and to adjust for suppression.
6. **Build a patient-based market model.** Diagnosed US patients (about 8,500-9,000, reconcile with HAEA and HAE International data), on-demand versus prophylaxis split, attacks per year, treated-attack fraction. Run sensitivity of PHVS IR and XR peak sales to share and price, and compare to the $1.8B EV.
7. **Intellia scenario work.** Wait for the 2027-03-10 FDA outcome and the label (price, HLA or liver language, age range). Build scenarios: approved on time and priced at about $2-3M, delayed, or label-limited. Test the sensitivity of PHVS XR share to each.
8. **Look for the cause of the Ionis and BioCryst declines** (9/8-10/6), including any non-HAE news, to see how much of the group move is HAE-specific. Also check short interest (FINRA, bimonthly) and options skew for PHVS; the screen's short-interest figure is stale **[UNVERIFIED]**.
9. **Test a pair trade**: Long PHVS versus Short BCRX, using Orladeyo's FY26 guide ($625-645M) and navenibart timing (top-line Q3 2027). Also review BioCryst's Astria acquisition (navenibart) as a competing long-acting injectable.
10. **Catalyst calendar**: Q3 results (about 2026-11-11, estimated), ACAAI (November; date unverified), CREAATE data (Q1 2027), Intellia PDUFA 2027-03-10, PHVS IR PDUFA 2027-04-23, XR filings 1H 2027, ex-US MAA decision (mid-2027, unverified).
11. **Check ClinicalTrials.gov** for competitor trials (navenibart, other plasma kallikrein and factor XII programs) and CHAPTER-4 enrollment, to see if any readout lands before 2027-10.

## Door status summary

| Door | Status | Reason |
|---|---|---|
| 1a Q1 revenue reconciliation | CLOSED | Product $39.2M; total $40.9M; Q4 derived $35.4M |
| 1b New-patient trend | CLOSED | Start-form adds plateau at about 44/week |
| 1c Payer / step edits | OPEN | Secondary-source only; read primary payer policies |
| 1d Gross-to-net | DEAD END | Not disclosed; assumption needed |
| 1e Switching from icatibant | CLOSED (direction) / OPEN (size) | CMS shows share swap; magnitude needs Q2 data |
| 1f Chiesi integration | DEAD END | Private; no filings after 6/11 |
| 1g 14D9 forecast | CLOSED | $185M (2026) to $705M (2038) |
| 2 Prophylaxis trends and data | CLOSED | Rotation plus modest growth; XR 87% type 1/2 |
| 3 Intellia | OPEN | Price and capacity unknown; HLA/liver label risk unresolved |
| 4a 10b5-1 status | CLOSED | 12% flagged; 88% not |
| 4b Block buyer | OPEN | Not identifiable yet |
| 5 Stock decline | CLOSED (mostly) | No offering; sector de-rating plus block |
| 6 Pricing / runway / dilution | OPEN | Needs explicit burn model |
| 7 CMS data | CLOSED (direction) / OPEN (Q2) | Q2 26 not yet posted |
