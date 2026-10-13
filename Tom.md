# Tom.md — context on the user

## Who
- Tom Pham, university student (UT Dallas), on a Point72 Academy 2026 case-competition team.
- Teammate Damien built the original DKS Excel model and engine branches.
- Team skills: finance/accounting, CS/engineering, consumer/retail. No biology background.

## Projects in this repo
- **FTAI (submission):** SHORT call, PT ~$145. Deck + model due 2026-10-12 11:59 PM ET; finalists 10-26, resubmission 11-09, finals NYC 11-12/13.
- **DKS (side work):** Damien's model, operational-signal pipeline, SEC historical validation (`docs/historical-validation-report.md`).
- **Scraping (built, branch `scraping`):** `scraping/` collects Reddit (PRAW) and Google store reviews for DKS sentiment analysis. Guide: `scraping/README.md`; plan + schema: `docs/superpowers/plans/2026-10-12-scraping.md`.

## Sentiment data: what we have and what classification adds

**Collected now (raw, `scraping/data/scraping.sqlite`, exported to `scraping/data/exports/`):**
- Reddit: r/dickssportinggoods (cohort `dks`, mostly employee voice) plus r/retail, r/TalesFromRetail and r/RantsFromRetail (cohort `general_retail`, the control group). Posts and comments, each with `created_at`, score, flair (an "Employee" hint), retailers mentioned, and a salted author hash (never usernames).
- Google reviews: up to 5 per store for DICK'S banners, DICK'S Foot Locker/Champs and competitors (Academy, Hibbett, Scheels). Each has store, banner, company, city, state, 1–5 stars and date. `store_snapshots` adds each store's overall rating and review count over time.
- **Collected as of 2026-10-12 (local only, gitignored):**

  | Dataset | Volume | Range | Location |
  |---|---|---|---|
  | r/dickssportinggoods | 1,528 posts + 16,033 comments | 2021-01 → 2026-10 | `scraping/data/scraping.sqlite` → `exports/` |
  | r/retail | 1,911 posts + 31,644 comments | 2012 → 2026 | same |
  | r/TalesFromRetail | 2,683 posts + 147,749 comments (partial run) | 2011 → 2026 | same |
  | r/RantsFromRetail | not collected yet | — | — |
  | Google reviews, DICK'S banners | 3,184 reviews, 642 of 670 stores, 48 states | 2016 → 2026 (2,451 from 2026) | `scraping/data/reviews.sqlite` → `exports_reviews/` |

  Review averages by banner: DICK'S 3.51★ (555 stores), House of Sport 3.69★ (45), Golf Galaxy 3.81★ (38); Going, Going, Gone! not fetched. The sampled reviews average 3.5★, but those stores' overall Google rating averages 3.89★ over 261k reviews: Google's "most relevant" sample skews negative. Use `store_snapshots` for rating levels and review text for themes.
- **Pending:** deletion re-check (run before sharing any data); finish r/TalesFromRetail and r/RantsFromRetail; 28 unfetched stores (wait a day, confirm the monthly free allowance first); sentiment classification.
- **Google cost guard:** Tom set Places API (New) quotas to 500 SearchText/day and 900 GetPlace/day. About 645 GetPlace calls were used on 2026-10-12, and the free tier is believed to be ~1,000/month (unverified). Don't run more reviews this month without checking.

**After classification (next step, not built yet). Each document gains:**

| Field | Values | Reddit | Reviews |
|---|---|---|---|
| `sentiment` | −1…1 score + neg/neu/pos label | model output | model output, checked against stars |
| `topic` | existing pipeline taxonomy: `excess_inventory`, `markdowns`, `understaffing`, `reduced_hours`, `shipment_disruption`, `employee_turnover`, `restructuring`, `store_closures`, `sales_pressure`, `positive_performance`, `neutral`, `irrelevant` (multi-label allowed) | operations themes | customer experience themes (stock-outs, staffing on floor, checkout) |
| `severity` | 0–1 | model/LLM | model/LLM |
| `confidence` | 0–1; <0.6 is dropped by the pipeline | model | model |
| `voice` / `employee_role` | customer / employee / manager / former / unknown | from flair + text | always customer |
| `segment` | `legacy_dicks` / `foot_locker` | from company mentions | from store banner |
| `store_scope` | single_store / regional / company_wide / unknown | usually unknown | single_store (exact store) |
| model metadata | model name, version, classified_at | yes | yes |

**Aggregates for the pitch and model:**
- Per fiscal quarter: DKS negative share **minus** general-retail negative share (a relative index, because rant subs are negative by design), volume-weighted.
- Per store / state / banner / quarter: mean stars, negative share, topic shares, plus rating and review-count trend from `store_snapshots`.
- Exportable to the existing `src/dks_model/alternative_data` Observation schema (`post_id, event_id, created_at, available_at, source, company, segment, store_scope, store_id, topic, sentiment, severity, confidence, employee_role, text, is_synthetic=false`) so real data can replace the synthetic mock signals.
- Validation: star ratings plus about 200 hand-labelled docs measure classifier accuracy before any claim.

**Caveats to state:** Reddit history is capped (~1,000 per listing); Google returns only "most relevant" reviews; data was collected retrospectively, not captured in real time; subreddits are self-selected.

## How Tom wants to work
- Token efficiency first. Terse answers; recommendations, not surveys.
- **No subagents** unless Tom explicitly asks for them.
- Free data only (no Bloomberg/FactSet, no paid datasets unless Tom approves). Public information only; never contact companies or people.
- Keep verified vs inferred numbers separate; cite sources.
- Never write Tom's email or other contact details into committed files. Secrets (SEC_USER_AGENT, Reddit/API keys) live in environment variables or a gitignored `.env`.

## Environment
- Windows 11, PowerShell + Git Bash. Python venv at `.venv/`.
- No desktop Excel: workbooks are checked in Excel for the web or Google Sheets.
- AI tools used (must appear in the GenAI appendix): Claude / Claude Code, ChatGPT / Codex, Gemini. Log meaningful AI use in `genai_log/`.
