# CONTEXT.md: DKS x Laya case pipeline

Read this file in full at the start of every session. It is the shared brief for all three teammates and their AI agents. `CONTRACT.md` is the authority on file schemas; this file is the authority on goals, rules, ownership, and the Git protocol.

## 1. What we are building and why

Team entry in the 2026 Point72 Academy Case Competition. Company: Dick's Sporting Goods (DKS). Deliverables: a 12-slide max Long/Short deck (the GenAI appendix counts toward the 12), our own Excel financial model, and a GenAI appendix.

Thesis: a System One decision model (Laya, open source, self-hosted) turns unusable consumer text (Reddit posts, Google reviews) into calibrated, mechanism-specific signals. Those signals become evidence for ONE flagged operating driver (DICK'S comparable-store sales) inside our own Excel model. The text model is an evidence layer. It is NOT the financial model.

Live target: FY2026 Q3 (roughly Aug to Oct 2026), reported around late November 2026. The text signal for that quarter is a pre-earnings nowcast and a dated catalyst inside our 12-month horizon.

Method precedent (cite, do not copy code): Okuneva, Hauber, Carstensen and Bar, "Nowcasting German GDP with Text Data" (text indices into a mixed-frequency ridge/DFM nowcast); Huang (2018, JFE), "The Customer Knows Best" (abnormal consumer-review index predicts revenue and earnings surprises). We reimplement the logic in our own Python. Do not clone or vendor their repositories (no license, legacy stack, and a known scaling leak).

## 2. Architecture

```
data/raw (scraper output, not committed)
  -> src/clean.py         -> data/clean/items.csv          (P1)
  -> src/score.py (Laya)  -> data/labels/item_features.csv (P2)
  -> src/aggregate.py     -> data/indices/quarterly_index.csv (P2)
  -> src/backtest.py      -> outputs/backtest.csv, metrics.csv, leadlag.csv, nowcast.json (P2)
  -> src/figures.py       -> figures/*.png (P3)
  -> Excel model (P3, built by hand)  <- outputs/nowcast.json delta_comp_bp
  -> deck (P3), GenAI appendix (P1)
data/fundamentals/dks_quarters.csv (P1) feeds aggregate.py and backtest.py
```

## 3. Deadline and timeline (Central time)

Hard deadline 10:59 PM CT (11:59 PM ET), Monday Oct 12, 2026. We submit by 10:40 PM CT.

| Time | Gate |
|---|---|
| 7:30 | Google reviews terms-of-service decision (P1 recommends, P2 records in status/DECISIONS.md) |
| 7:50 | Laya smoke test passes, or switch to fallback adapter |
| 8:05 to 8:30 | items.csv committed (P1) |
| 8:30 | Runtime check: subsample if full scoring would exceed 40 minutes |
| 9:45 | DATA FREEZE. Whatever the frozen spec produces is what we report |
| 10:20 | Deck and model final |
| 10:40 | Upload |

## 4. Ownership (edit ONLY your own paths)

| Owner | Paths |
|---|---|
| P1 (data + compliance) | `src/clean.py`, `data/clean/`, `data/fundamentals/`, `docs/appendix/`, `docs/compliance.md`, `status/P1.md` |
| P2 (pipeline lead, Arjun) | `CONTRACT.md`, `CONTEXT.md`, `src/score.py`, `src/aggregate.py`, `src/backtest.py`, `src/mock.py`, `data/labels/`, `data/indices/`, `outputs/`, `status/P2.md`, `status/DECISIONS.md` |
| P3 (Excel + deck) | `src/figures.py`, `figures/`, `docs/deck/`, `model/`, `status/P3.md` |

If you need a change in someone else's file, write the request under "Requests" in your own status file. Do not edit their file.

## 5. Git protocol for agents

At the start of every session and before every step:
1. `git pull --rebase origin main`
2. Read `CONTEXT.md`, `CONTRACT.md`, your `tasks/Px.md`, every file in `status/`, and `git log --oneline -20`.
3. Check what already exists (`ls -R data outputs figures src`). Never redo a step another agent has marked done.

While working:
- Work on `main`. Small commits. Message prefix `[P1]`, `[P2]`, or `[P3]`, e.g. `[P1] add dks_quarters.csv (verified)`.
- Before every push: `git pull --rebase origin main`, then push. On a conflict in a file you do not own, keep the upstream version.
- After each completed step, update your `status/Px.md` and push: Done / Doing / Next / Blockers / Handoffs / Requests.
- Signal a handoff with a line in your status file such as `HANDOFF: data/clean/items.csv ready (N rows) at 8:12`.
- Never force-push. Never rewrite history.

Never commit:
- API keys or tokens (use `.env`, which is gitignored).
- `data/raw/` (may contain usernames). Only cleaned data without author identifiers is committed.
- Files over 50 MB (`data/labels/laya_raw.jsonl` and checkpoints are gitignored).

## 6. Mock-first rule

`src/mock.py` writes `MOCK_`-prefixed versions of every downstream file. Build and test all code against MOCK_ files first. At the 9:45 freeze, switch paths with the `--mock` flag off. Never let a MOCK_ number appear in the deck or the Excel model.

## 7. Pre-registration rules (non-negotiable)

- The 7 Laya questions in `CONTRACT.md` / `src/score.py` are frozen. Do not reword them after seeing outputs.
- The backtest specification in `tasks/P2.md` is frozen: target comp_pct, primary signal intent_shock, secondary stockout_shock, comparison stars_shock, expanding window, AR(1) baselines.
- Do not add variants, change thresholds, or swap signals after seeing results. If the result is null, the verdict is "scenario" and the deck says so.
- Missing data is missing, never neutral. Text volume stays separate from opinion indices.

## 8. Competition rules every agent must respect

- Publicly available information only. No confidential or material non-public information.
- The Excel financial model must be our own, built from a blank workbook. Agents may explain formulas but must not generate or import a prebuilt financial model.
- Only publicly offered GenAI tools. Laya is open source and self-hosted; document it as such.
- Cite sources on every slide (company filings, company website, reputable news, and our documented data collection).
- 12 slides maximum including the GenAI appendix (3 slides max for the appendix).
- No contacting any individuals or companies.

## 9. Facts status

Verified: competition rules above; Okuneva and Huang method summaries (from our research brief).
To verify before use (P1 owns): Foot Locker acquisition closing date and how DKS now reports comps (DICK'S Business vs Foot Locker business); fiscal quarter period dates; FY2026 Q3 report date; current Google and Reddit data terms.

## 10. Writing style for anything that goes in the deck

Plain language first, define any term the first time. No em dashes. Claims sized to the evidence: if out-of-sample quarters are few, say so on the slide.
