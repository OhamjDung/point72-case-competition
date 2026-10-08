# Point72 Academy 2026 Case Competition: FTAI Short

> **For AI assistants reading this file:** this README is the full context for a university team's stock-pitch project. Read all of it before helping.
>
> The competition rules in section 2 are **binding**:
> - Use only public information.
> - Never contact companies or people.
> - Never present other firms' research models as the team's own.
>
> If something here conflicts with a file in `research/`, the newer file wins. Check `research/FTAI/thesis.md` first.

---

## 1. TL;DR

| | |
|---|---|
| **Ticker** | FTAI Aviation Ltd. (NASDAQ: FTAI) |
| **Call** | **SHORT** |
| **12-month price target** | **~$145** (−19% vs $179.44 close on 10/6/26) |
| **Street view** | All Buy / Strong Buy; mean price target ≈ $330 |
| **Deadline** | **Oct 12, 2026, 11:59 PM ET** (deck + model) |
| **Status (Oct 7)** | Research done, model built, team reviewing. Deck not started. |

**Thesis in one paragraph.** The market prices FTAI as a high-growth aftermarket franchise that will deliver management's 2027 guide of $2.3B Adjusted EBITDA. Our model values full guide delivery at about $183, so the $179 share price already assumes it. The filings show two things the price ignores:
1. A large share of 2025–26 cash came from a **one-time sell-down of the balance sheet that is now ending**. FTAI's own 10-Q calls these sales "non-recurring".
2. Growth increasingly runs through **three affiliate channels FTAI does not control**, and FTAI books revenue when it sells into them.

Our base case: 2027 EBITDA of $1.92B (17% below guide), FY27 EPS of $7.88, worth about $145.

---

## 2. The competition (what we must deliver)

**Task.** Pick one of PHVS, NBIS, DKS or FTAI. Make a Long or Short call on a 12-month view, built around one or two *differentiated business insights*. An insight is a conclusion about how the business really works, not a fact. It must go beyond what a first-pass GenAI answer gives. Judges grade the **rationale**, not whether they agree with the call.

**Deliverables (due Oct 12):**
1. **Deck, 12 slides max including the AI appendix** (the cover doesn't count). It must cover:
   - recommendation, price target, horizon and upside/downside
   - the differentiated insight
   - supporting evidence
   - valuation impact versus consensus
   - catalysts
   - risks and disconfirming evidence
   - outstanding diligence

   Cite sources on every slide. Put page numbers and the team name on every page. The cover needs the team name, all member names, the ticker, the price target and Long/Short.
2. **Financial model.**
   - Summary tab
   - 2+ years of history
   - 5 years of projections, at least 2 of them quarterly
   - operating drivers linked to the P&L, with the 2–3 key assumptions flagged
   - sensitivities
   - a bridge from the consensus/base case to our case
   - easy to print
3. **GenAI appendix, 3 slides max** (counted inside the 12). It must cover:
   - every AI tool used
   - the main use cases
   - one worked example: prompt → AI response → gap found → extra public research → how the conclusion changed

**Rules (binding):**
- Public information only. **No confidential or material non-public information, ever.**
- **Do not contact any company or individual.** The project must stay passive.
- The model must be the team's own, started from a blank workbook. No other firm's research model.
- No collaboration with other teams.
- Every team member must be able to defend every part of the pitch in Q&A.
- Upload note: "This project was created exclusively by me; is sourced exclusively to publicly available information; does not contain confidential or material non-public information; and sharing it with Point72 does not breach any duty to any other person or entity."

**Later dates:**
- Finalists announced Oct 26.
- Mentor window closes Nov 6.
- Resubmission due Nov 9.
- Finals in NYC on Nov 12–13.

**Team constraints:**
- Skills: finance/accounting, CS/engineering, consumer/retail. No biology.
- Free data only; no Bloomberg or FactSet.
- Tools: Claude (including Claude Code), ChatGPT and Gemini.

---

## 3. How we got here (process summary)

1. **Screened all 4 tickers** in parallel with Claude research agents, using a lead-following method: search A, find B and C, chase each, and log the trail.
2. **Stress-tested each thesis** with smoke tests (pass/fail checks of load-bearing facts against filings) and ablations (remove each evidence pillar and see how much value moves).

| Ticker | Result | Why dropped / kept |
|---|---|---|
| **NBIS** (Nebius) | Dropped | The value gap was only a multiple call (about 10x vs CoreWeave at 6x), not a business insight. |
| **DKS** (Dick's) | Dropped | Both the Long and the Short were crowded after a 31% one-day drop. |
| **PHVS** (Pharvaris) | Backup | The price already embeds prophylaxis success. Takeover risk, and the team has no bio background. |
| **FTAI** | **Chosen** | Strongest primary-source evidence; fits a finance team. |

3. **FTAI deep dive** with 4 agents:
   - credibility of the 2027 guide
   - clean historical data
   - engine economics and peer comparables
   - devil's advocate
4. **Critical pivot.** The first-pass insight ("FTAI is an engine trader, not a franchise") turned out to **repeat the January 2025 Muddy Waters short report (slide 22)**. We refocused on what is *new since then*. This is the worked example for the GenAI appendix.
5. **Built the model** (Python → Excel) and fixed review findings. Direction firmed to SHORT.

---

## 4. The two insights (new since the Muddy Waters / Snowcap short reports of Jan 2025)

### Insight 1: the cash engine was partly a one-time sell-down, and it's ending

- **Seed aircraft sales are collapsing.** Sales to the SCI "2025 Partnership" fell from 33 in Q2'25 to 6 in Q2'26. The 10-Q says these sales "were non-recurring in nature and not considered part of the Company's ordinary activities."
- **One-offs made up most of 1H26 cash.**
  - Operating plus investing cash flow (CFO + CFI) was **$250.4M**.
  - Of that, $175.7M was seed-sale proceeds and $48.3M was Russia insurance.
  - That leaves **about $26M**, after an inventory build of about $351M.
- **The second half is back-loaded.** The FY26 Adjusted FCF guide is $878M, already cut from $915M. **2H26 needs about $623M**, against a Q2 run-rate of about $95M.
- **Management's FCF definition adds back spending.** FY25 Adjusted FCF of $724M includes $252M of add-backs the CFO named on the Q4 call (turbines, parts and the SCI investment). CFO + CFI was $412.6M.
- **Gains are a big part of EBITDA.** Gains on sale were about **40% of Adjusted EBITDA** (44% in FY24, 40% in FY25, 40% in 1H26).

### Insight 2: growth runs through three affiliate channels FTAI does not control

1. **Aircraft sold to SCI.** FTAI owns about 19%, acts as servicer, and SCI is the "primary buyer of all future on-lease 737NG/A320ceo aircraft".
2. **Engines and modules sold to SCI** under an exclusive contract. These were **25% of Aerospace revenue in 1H26** (17% in FY25). Q2'26 Aerospace revenue growth was "primarily due to" these sales.
3. **Turbines sold to the J&F Power joint venture.** Jereh, a Chinese company, consolidates it as a "controlled subsidiary". The CFO said FTAI books revenue "when FTAI sells the turbine to the JV". The $1.465B hyperscaler order sits there.

**Adjusted EBITDA includes FTAI's pro-rata share of SCI's EBITDA.** That share was $28.0M in Q2'26. SCI's debt (inferred at about $760M for FTAI's 19%) is **not** in FTAI's net debt.

---

## 5. Valuation summary

| Scenario | 2027 EBITDA | FY27 EPS | Blended $/share | vs $179 |
|---|---|---|---|---|
| Management guide | $2,300M | $10.12 | $183 | +2% |
| **Our base** | **$1,920M** | **$7.88** | **$144** | **−20%** |
| Bear | $1,470M | $5.07 | $91 | −49% |
| Bull | $2,480M | $11.24 | $220 | +22% |

- **Blended value** = 40% sum-of-the-parts + 30% forward P/E + 30% DCF.
- **Probability-weighted (25/50/25):** about $150. **Price target about $145.**

**Peer multiples (EV/EBITDA TTM, then forward P/E):**

| Company | EV/EBITDA TTM | Forward P/E |
|---|---|---|
| HEICO | 30.2x | 44.0x |
| AAR | 13.8x | 17.7x |
| StandardAero | 11.7x | 15.9x |
| AerSale | 17.4x | 18.1x |
| AerCap | 12.4x | 8.5x |
| FTAI | 21.7x | 20.2x |

**Bridge from consensus:**
- Price $179 = consensus FY27 EPS ($8.87) × 20.2x.
- **EPS leg:** our $7.88 at the same multiple gives about $159 (−$20).
- **Multiple leg:** compressing to 17x (MRO peers) gives about $134 (−$25).

Why the multiple should compress:
- 3-year CFO/EBITDA is −14% for FTAI, versus 69% for HEICO and 25% for StandardAero.
- About 40% of EBITDA is gains.
- The share of revenue going to affiliates is rising.

**Three key assumptions (flagged yellow in the model):**
1. **2027 Aerospace EBITDA:** base 1,500 modules × about $0.82M per module = $1,230M (guide $1,400M).
2. **2H26 inventory → FCF conversion:** about $623M is needed.
3. **Power:** 44 units × $7.5M = $330M (guide $450M). Per-unit economics are undisclosed.

**Catalysts:**
- **Q3 results on Oct 28, 2026** (after the deadline, before the Nov 9 resubmission)
- investor meeting on Dec 10 (unverified)
- FY26 results in late Feb 2027
- first Mod-1 power unit deliveries

**Strongest risks:**
- Power turns out bigger than guided (bull case +22%).
- SCI becomes a captive recurring demand channel.
- CFM56 demand stays strong through 2028–29.
- A $500M buyback (announced 9/15/26).
- Short holders pay the ~1.1% dividend.
- Take-private interest.

---

## 6. Verified vs inferred (be honest in Q&A)

**Verified in SEC filings or company statements:**
- the 10-Q "non-recurring" quote and the seed-sale counts
- 1H26 and FY25 cash flows
- gains share of EBITDA
- SCI revenue share
- the Adjusted EBITDA definition (includes pro-rata share)
- the Q2 Leasing breakdown ($7.0M fees + $28.0M pro-rata = the "$35M")
- the CFO's turbine-to-JV revenue quote (from a secondary transcript)
- the $500M buyback
- Form 4s show no insider buying

**Inferred or unverified:**
- the ~$59M of FY25 FCF the CFO didn't explain (probably acquisitions)
- SCI partnership debt (~$4B total, ~$760M FTAI share)
- J&F ownership % (not disclosed)
- Power per-unit EBITDA (~$7–8M, secondary source)
- the 75% Power cash conversion (a model assumption)
- the 52-week high
- consensus FY27 EPS of $8.87 (derived from one aggregator)

**Corrections made along the way** (full log in `research/FTAI/thesis.md` §9; useful for the GenAI appendix):
- Wrong short-seller name in the AI's prompt (Hunterbrook → actually Muddy Waters and Snowcap).
- A wrong FCF-gap attribution.
- The first insight repeated Muddy Waters.
- An unsupported 10x multiple.
- Corporate costs left out of the first model valuation.
- A misframed "SCI net cash" figure that was retracted.

---

## 7. File map

```
README.md                          ← you are here
docs/
  research-plan.md                 phases, selection rubric, compliance rules
  model-spec.md                    spec the model was built from
research/FTAI/
  thesis.md                        ★ MAIN DOCUMENT — full thesis v1.0, sourced
  screen.md, trail.md              first screen + lead-following investigation
  stress_test.md                   smoke tests + ablation
  phase2/A_2027_guide.md           2027 guide credibility (bear/base/bull by segment)
  phase2/B_data_notes.md           data notes for the CSVs below
  phase2/C_engine_economics_comps.md  CFM56 market, share, peer comps
  phase2/D_adversarial.md          devil's advocate; Muddy Waters/Snowcap claim table
  phase2/G1_power_jv.md            J&F Power JV findings
  phase2/data/*.csv                clean sourced historicals, consensus, guidance, debt
  thesis_v0_archive.md             superseded draft (don't use)
research/NBIS|DKS|PHVS/            screens + stress tests for the rejected tickers
model/
  FTAI_Model.xlsx                  ★ the model (10 tabs + Checks)
  build_model.py                   rebuilds the workbook from scratch: python -I build_model.py
  model_notes.md                   driver logic, tie-outs, change log
genai_log/01_screening.md          ★ full AI-use trail for the GenAI appendix
```

**Model tabs:**

| Tab | What it holds |
|---|---|
| Summary | |
| Drivers | Scenario dropdown: Bear / Base / Bull / Mgmt Guide |
| Historical | |
| Quarterly | Q1'26–Q4'27 |
| Annual | FY23–FY30 |
| FCF_Quality | The thesis tab |
| Valuation | |
| Bridge | |
| Sensitivity | |
| Checks | 88 checks; all should say PASS |
| Sources | |

- Blue font = input, black = formula.
- The file has no saved calculated values, so open it in **Excel for the web** (via your school Microsoft 365) or Google Sheets. It recalculates on open. Then switch the scenarios and confirm the Checks tab shows 0 FAIL.

---

## 8. What's left (as of Oct 7)

- [ ] Team reviews `thesis.md` and the model, and sends edits.
- [ ] Team name and all member names (needed for the deck cover and the model header, which currently says "[TEAM NAME]").
- [ ] Run the same baseline prompt in **ChatGPT and Gemini** and take screenshots, for the GenAI appendix. Suggested prompt: *"Should I be long or short FTAI Aviation over the next 12 months, and what drives the business?"*
- [ ] Test the model in Excel for the web, then export a PDF print copy.
- [ ] Build the deck: 12 slides including a 3-slide AI appendix, with sources on every slide.
- [ ] Final compliance check and upload with the required note.

**Suggested deck outline (draft):**

| # | Slide |
|---|---|
| 1 | Recommendation and price target |
| 2 | The market's view vs ours ("$179 = full guide delivery") |
| 3 | Insight 1 evidence (seed sales collapsing, cash ex-one-offs) |
| 4 | Insight 1: the 2H26 FCF bar |
| 5 | Insight 2: three affiliate channels |
| 6 | Valuation and scenarios |
| 7 | Bridge from consensus and guide |
| 8 | Catalysts |
| 9 | Risks |
| 10 | Diligence |
| 11–12 | AI appendix (plus one more if needed; the total stays within 12) |

---

## 9. Instructions for an AI helping on this project

- Treat `research/FTAI/thesis.md` as the source of truth. Cite filings (EDGAR accession numbers or URLs are in the files) rather than memory. Model knowledge of FTAI may be stale or wrong: one AI-generated hint in this project named the wrong short seller.
- Don't claim our insights are new if Muddy Waters (Jan 15, 2025) or Snowcap already made them. Check `phase2/D_adversarial.md` and `short_report_claims.csv`.
- Keep "verified" and "inferred" separate (section 6). Don't upgrade an inferred number to a fact.
- Use only public sources: SEC EDGAR, company IR, reputable news, government data. No paywalled, leaked or private content. Never draft outreach to the company, its employees or analysts.
- If you change a model number, edit `model/build_model.py` and rebuild. Don't hand-edit the xlsx, or the rebuild will overwrite your change.
- Log meaningful AI prompts and outputs in `genai_log/` for the appendix.
