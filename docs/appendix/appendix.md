# GenAI appendix (3 slides): draft for P3

Each slide body is 80 words or fewer (counts in brackets). Placeholders in `{braces}` are filled after the 9:45 freeze from `data/labels/agreement.json`, `outputs/metrics.csv` and `outputs/nowcast.json`. Supporting material for speaker notes and Q&A is under each slide. No em dashes.

---

## Slide A1. GenAI tools and where we used them

**Headline:** We used AI to build and check the pipeline. Our judgment set the thesis, the frozen spec and the model.

**Body [76 words]**
- **Objective:** speed up research, coding and text scoring without letting AI choose the answer.
- **Tools (all publicly offered):** Laya (open source, self-hosted on Google Colab) scores the text; Claude Code (Anthropic) and ChatGPT/Codex (OpenAI) for research, code and reviews; Claude API as a standby scoring fallback.
- **Output:** 17,198 Reddit items scored on 7 frozen questions.
- **Interpretation:** AI did the volume work. We fixed questions and tests before seeing results.
- **Limitation:** AI facts were re-checked against SEC filings.

**Supporting detail**
- Pipeline: scraped Reddit text -> 7 frozen Laya questions -> quarterly indices on DKS fiscal quarters -> expanding-window backtest against an AR(1) baseline -> one flagged comp driver in our own Excel model.
- Laya: package `laya` 0.4.6, checkpoint `convaiinnovations/laya` at a pinned revision (CONTRACT.md file 2), Apache-2.0.
- Claude Code (Opus 5.5) ran the data cleaning, the fundamentals table and the terms check for P1. It also ran the early ticker screen with Claude Sonnet 5.5 research agents (genai_log/01_screening.md).
- ChatGPT/Codex integrated a teammate's model branches and the signal pipeline (genai_log/02, 03).
- The Excel financial model was typed by hand from a blank workbook. AI only explained formulas (competition rule).
- If the Claude fallback is used for scoring, say so here and give its `model_version`. Otherwise delete "standby scoring fallback". **[P2 to confirm which provider scored the real run.]**

**Prompt / response example (P1 data step)**
- Prompt (abridged): "Build data/fundamentals/dks_quarters.csv ... using only DKS quarterly earnings press releases (8-K Exhibit 99.1) and 10-Q/10-K filings ... After the Foot Locker acquisition closed (verify and cite the closing date), use the DICK'S Business comp ... re-open each source and verify every number."
- Response (abridged): 22 quarters from 22 releases. Foot Locker close verified as 2025-09-08 (8-K, accession 0001140361-25-034244). Flagged a comp definition change in FY2022 (relocated stores added; FY2021 Q1 restated from 115% to 117.1%). Automated re-check: 0 mismatches against the releases and the XBRL filings.
- How we used it: kept first-reported comps; recorded every restatement in data/fundamentals/NOTES.md.

---

## Slide A2. Worked example: AI's first idea failed, research changed our question

**Headline:** AI first proposed predicting the stock. Public evidence showed that fails, so we nowcast DICK'S comps instead.

**Body [77 words]**
- **Prompt:** "How can consumer text help a long/short call on DKS?"
- **AI response:** daily stock-price models from social text (StockNet, MAN-SF).
- **Gap found:** we read their code and published results. Such models lose to a "price stays the same" baseline and predict prices, not fundamentals.
- **Further public research:** Okuneva et al. (text nowcasts of German GDP); Huang (2018, JFE): abnormal review sentiment predicts revenue and earnings surprises.
- **Changed conclusion:** nowcast DICK'S FY2026 Q3 comps before the late-November print.

**Supporting detail**
- Why this matters for the pitch: comps are the driver the market reprices on at earnings; the Q3 print (expected around 2026-11-24, inferred from past Q3 timing, not yet announced) is a dated catalyst inside our 12-month horizon.
- We reimplemented the logic in our own Python. We did not copy code from either paper's repository.
- **[Overclaim check]** "lose to a price stays the same baseline" must be backed by the specific results table we inspected. Add the citation (paper, table) or soften to "did not clearly beat". **[Team to confirm source.]**

**Second worked example (data rights), usable in Q&A**
- Prompt: check the current Google Maps and Reddit terms for our collection method.
- Response: Google Maps Platform Terms 3.2.3(a)(iii) prohibit copying and saving user reviews. Reddit's Data API license covers display in an app, not republishing.
- Gap: our first dataset contained 3,104 Google reviews.
- Research: read both official terms pages (dates in docs/compliance.md).
- Changed conclusion: we dropped all Google reviews (and the star-rating baseline that depended on them) and publish only aggregates of Reddit text.

---

## Slide A3. Validation, limits and bias controls

**Headline:** We tested the AI's labels against our own, froze the test in advance, and size claims to the evidence.

**Body [about 70 words once filled]**
- **Method:** 50 items hand-labelled before seeing Laya's answers. Agreement: relevance {pct_rel}% (kappa {k_rel}), topic {pct_topic}%, stockout {pct_stock}%, intent {pct_intent}%.
- **Backtest:** {n} out-of-sample quarters; MAE {mae_laya} bp with text vs {mae_ar} bp without. Verdict: {verdict}.
- **Bias:** Reddit skews to extreme experiences and employees; history is thin before 2023.
- **Controls:** questions and spec frozen first; missing data kept missing; Google reviews excluded under their terms.

**Supporting detail**
- Data collection: official Reddit API (PRAW), read-only, within rate limits; usernames replaced by salted hashes; items deleted on Reddit are purged; only aggregates published. Google reviews were collected through the official Places API but excluded under Google's terms (docs/compliance.md).
- Coverage: 17,198 items, 2021-02-04 to 2026-10-12; 17,191 from r/dickssportinggoods (largely employee voice). Items per year: 2021: 37, 2022: 448, 2023: 643, 2024: 2,764, 2025: 5,316, 2026: 7,990. Early quarters fall below the 15-item threshold, which shortens the backtest.
- FY2026 Q3 signal is partial: data through 2026-10-12 against a quarter ending 2026-10-31 (coverage about {coverage_pct}%).
- Laya's probabilities are used as shipped (no recalibration on our labels), so its over-confidence caveat applies.
- **If verdict = "scenario":** replace the backtest line with "The text signal did not beat the no-text baseline in {n} out-of-sample quarters, so we show it as a scenario, not a forecast."
- **[Overclaim check]** Do not write "predicts" or "leads" comps unless the verdict is "nowcast". With fewer than about 8 out-of-sample quarters, say "early evidence".

---

## Sentences flagged for overclaiming

1. A2: "Such models lose to a 'price stays the same' baseline": needs the specific source (paper and table) or a softer wording.
2. A3: any wording that says the signal "predicts" comps: only if verdict = nowcast, and with n stated.
3. A1: "Claude API as a standby scoring fallback": remove if unused; if it scored the real run, say it was the scorer.
4. A2 supporting: "expected around 2026-11-24": inferred from past Q3 report dates, not announced by DKS. Label it "expected" on the slide.
