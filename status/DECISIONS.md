# Decisions log

Times are Central time on 2026-10-12. "P2 agent default" means the human left it unspecified and the agent picked a default; Arjun (P2) can overrule any of them.

| Time | Decision | Owner | Reason |
|---|---|---|---|
| 19:33 | Python: a venv at `.venv` made with `py -3.10 -m venv .venv`; nothing installed system-wide. Code targets Python 3.10+ and must run on Colab. | P2 (Arjun) | Python 3.11 is not installed on Arjun's machine; Colab compatibility. |
| 19:33 | Local project folder is `C:\Users\Arjun\Downloads\dks_laya`. | P2 agent default | The instruction gave an unfilled `[LOCAL_PATH]` placeholder; Downloads holds the other project folders. |
| 19:33 | Built on top of the existing `origin/main` history instead of a fresh repository. No force push. | P2 agent default | `main` already had 3 commits (FTAI research, Damien's Excel model); a fresh `git init` push would be rejected. |
| 19:40 | Existing FTAI `README.md` kept in full; a short DKS x Laya block added at the top pointing to CONTEXT.md. `.gitignore` extended, not replaced. | P2 agent default | Do not delete a teammate's work. The FTAI README is stale for the DKS pitch; the team decides whether to archive it. |
| 19:40 | `comp_pct` = DICK'S Business comparable sales %, equal to the headline consolidated comp before the Foot Locker acquisition. `comp_fl_pct` = Foot Locker business comp when reported, else empty. | P2 (Arjun) | P1 pulls the real numbers and the first Foot Locker quarter from filings. |
| 19:40 | Mock data only: Foot Locker comps first appear in FY2025Q3. Mock period dates are computed (13/13/13/rest weeks), not from filings. | P2 (Arjun) | Placeholder until P1's table lands. |
| 19:40 | Fiscal year named for the calendar year it starts in; FY2026Q3 ends around late October 2026 and is partial. | P2 (Arjun) | DKS's own convention. |
| 19:40 | Index, shock, backtest, and nowcast formulas written into CONTRACT.md files 4 to 6 exactly as given. A shock is an index minus its own recent average, not a model error. | P2 (Arjun) | Pre-registration. |
| 19:40 | `volume_log` is always filled, even when n_effective < 15 empties the four indices. | P2 agent default | It measures volume, not opinion, and CONTEXT.md keeps volume separate from the indices. |
| 19:40 | Nowcast interval = delta_comp_bp plus or minus 1.2816 x beta_se x abs(shock_current) x 100. Verdict uses that interval. | P2 agent default | Follows answer 5 wording ("that interval"). tasks/P2.md says "the 80% interval for b"; the two agree only when delta = b x shock x 100. Arjun to confirm before the 9:45 freeze. |
| 19:40 | `backtest.csv` holds two row blocks, `signal_used` = intent_shock (primary) then stockout_shock (secondary). `metrics.csv` reports the secondary as model `ar_laya_stockout`. | P2 agent default | Gives `signal_used` a meaning and keeps the secondary signal "reported separately" as tasks/P2.md asks. |
| 19:40 | `pred_ar_stars` is empty unless at least 6 training quarters have stars_shock and the forecast quarter has it. | P2 agent default | Same minimum window as the main models. |
| 19:40 | `n_beats_ar` counts strict wins (smaller absolute error); it is 0 for `ar`. | P2 agent default | Definition needed for file 7. |
| 19:40 | `leadlag.csv`: lag k pairs signal(q) with comp(q + k); lag +1 means the signal leads. Completed quarters only; corr empty if n < 3. | P2 agent default | Definition needed for file 8. |
| 19:40 | `agreement.json`: questions relevant, topic, stockout, intent (the hand-label columns). Laya says "yes" at probability 0.5 or more; topic and intent take the top option. | P2 agent default | Definition needed for file 9. |
| 19:40 | `item_id` = source + "_" + first 16 hex characters of SHA-256 of url + newline + text. | P2 agent default | tasks/P1.md asks for "a stable hash" without naming one. P1 may object via status/P1.md Requests. |
| 19:40 | Item banner = top `p_banner_*` (ties go to the first in list order); the `all` row includes every item; coverage uses the latest `scraped_at` date. | P2 agent default | Needed to make file 4 exact. |
| 19:40 | Banners: all, dicks, house_of_sport, golf_galaxy, foot_locker, other. | P2 (Arjun) | Confirmed. |
| 19:40 | `requirements.txt` with minimum versions; five stub modules; no `__init__.py`; `.gitkeep` in every empty folder. `.gitignore` uses `data/raw/*` plus `!data/raw/.gitkeep` so the empty folder is tracked but its contents never are. `model/` gets no `.gitkeep` because it already has files. | P2 (Arjun), details P2 agent default | Teammates need the folder tree. |
| 19:40 | Added mock files `MOCK_items.csv`, `MOCK_metrics.csv`, `MOCK_leadlag.csv`, `MOCK_agreement.json` (CONTRACT.md files 1, 7, 8, 9). | P2 (Arjun) | Joins and P3's figures need them. |
| 19:42 | Contract check run once on the MOCK_ files; all 9 pass. The second-run hash comparison was skipped. | P2 (Arjun) | Deadline. |
