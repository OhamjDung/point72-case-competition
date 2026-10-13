# CONTRACT.md: file schemas for the DKS x Laya pipeline

Owner: P2. This file is the authority on file schemas. If code and this file disagree, this file wins; ask P2 (status/P2.md Requests) before changing it.

Runtime: Python 3.10+ (also runs on Google Colab). Dependencies: `requirements.txt`.

## 0. Rules that apply to every file

**CSV format.** UTF-8 without a byte-order mark, comma separator, one header row, and exactly the columns listed below in the order listed. Text containing commas, quotes, or newlines is quoted the standard way (RFC 4180, which is what pandas `to_csv` does).

**Missing values.** A missing value is an empty field. Never write `NA`, `NaN`, `None`, `null`, or `0` to mean missing. Missing is never neutral: downstream code must skip it, not treat it as zero. In JSON files, missing is `null`.

**Types used in the tables below.**

| Type | Format | Example |
|---|---|---|
| str | text | `dicks` |
| float | decimal point, no thousands separator, no `%` sign | `3.25` |
| int | whole number | `17` |
| bool | `True` or `False` (what pandas writes and reads) | `True` |
| date | ISO 8601 calendar date `YYYY-MM-DD` | `2026-08-01` |
| datetime | ISO 8601 in UTC, `YYYY-MM-DDTHH:MM:SSZ` | `2026-10-11T15:00:00Z` |
| quarter | `FY{YYYY}Q{1-4}` | `FY2024Q3` |

**Units.** A percentage is in percentage points: `3.5` means +3.5%. A probability is between 0 and 1. A basis point (bp) is one hundredth of a percentage point, so 0.25 percentage points = 25 bp.

**Fiscal calendar.** DKS's fiscal year ends on the Saturday closest to January 31. A fiscal year is named for the calendar year it starts in: FY2024 runs from early February 2024 to early February 2025. Use fiscal quarters from `data/fundamentals/dks_quarters.csv` (`period_start`, `period_end`). Never use calendar quarters.

**Coverage.** FY2021Q1 through FY2026Q3. FY2026Q3 (about Aug 2 to Oct 31, 2026) is in progress, so it is partial: it has text data but no reported results.

**Mock files.** `src/mock.py` writes a fake version of every file below, in the same folder, with the same schema, and with the file name prefixed `MOCK_` (for example `data/labels/MOCK_item_features.csv`). Every mock value is invented. In mock files, `source_url` and `model_version` say `MOCK`, and URLs use the reserved domain `example.com`. A `MOCK_` number must never appear in the deck or the Excel model.

| # | Real file | Mock file | Written by |
|---|---|---|---|
| 1 | `data/clean/items.csv` | `data/clean/MOCK_items.csv` | `src/clean.py` (P1) |
| 2 | `data/labels/item_features.csv` | `data/labels/MOCK_item_features.csv` | `src/score.py` (P2) |
| 3 | `data/fundamentals/dks_quarters.csv` | `data/fundamentals/MOCK_dks_quarters.csv` | P1, from filings |
| 4 | `data/indices/quarterly_index.csv` | `data/indices/MOCK_quarterly_index.csv` | `src/aggregate.py` (P2) |
| 5 | `outputs/backtest.csv` | `outputs/MOCK_backtest.csv` | `src/backtest.py` (P2) |
| 6 | `outputs/nowcast.json` | `outputs/MOCK_nowcast.json` | `src/backtest.py` (P2) |
| 7 | `outputs/metrics.csv` | `outputs/MOCK_metrics.csv` | `src/backtest.py` (P2) |
| 8 | `outputs/leadlag.csv` | `outputs/MOCK_leadlag.csv` | `src/backtest.py` (P2) |
| 9 | `data/labels/agreement.json` | `data/labels/MOCK_agreement.json` | `src/score.py` (P2) |

Run `python src/mock.py --check` to test every `MOCK_` file against the column lists in this file.

---

## File 1: `data/clean/items.csv`

One row per text item (a Reddit post or a Google review). No usernames, profile links, or author identifiers of any kind.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `item_id` | str | no | Unique. `{source}_{h}`, where `h` is the first 16 hex characters of the SHA-256 hash of the UTF-8 string `url + "\n" + text`. Pattern `^(reddit\|google)_[0-9a-f]{16}$`. |
| `source` | str | no | One of `reddit`, `google`. |
| `banner_hint` | str | yes | Raw location text, unedited: the subreddit name (or a post flair that names a banner) for Reddit, the store or location name for Google. Empty if none. |
| `text` | str | no | Reddit: title, then two newlines, then body (title only if the body is empty). Google: the review text with any "Edited" prefix removed. Never empty. |
| `stars` | float | yes | Google star rating, 1.0 to 5.0. Always empty for Reddit. |
| `created_exact` | datetime | yes | Exact posting time in UTC (Reddit `created_utc`). Empty for Google. |
| `date_low` | date | no | Earliest date the item could have been written. |
| `date_high` | date | no | Latest date the item could have been written. `date_low <= date_high`. |
| `date_precision` | str | no | One of `exact`, `week`, `month`, `year`. |
| `url` | str | no | Link to the post or review page (no profile links). |
| `scraped_at` | datetime | no | When the item was collected, in UTC. |

Date rules (from tasks/P1.md):

- Reddit: `date_low = date_high = ` the UTC date of `created_exact`; precision `exact`.
- Google relative dates are parsed against `scraped_at` into an interval, never a point:
  - "N days ago": [scraped - (N+1) days, scraped - (N-1) days], precision `week`.
  - "a week ago" / "N weeks ago": [scraped - (N+1)*7 days, scraped - N*7 days], precision `week`.
  - "a month ago" / "N months ago": [scraped - (N+1) months, scraped - N months], precision `month`.
  - "a year ago" / "N years ago": [scraped - (N+1) years, scraped - N years], precision `year`.

## File 2: `data/labels/item_features.csv`

One row per scored item. Every `item_id` must exist in `items.csv`. All `p_` columns are Laya's probabilities, between 0 and 1. Each group marked "sums to 1" must sum to 1 within 0.001.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `item_id` | str | no | Unique; matches `items.csv`. |
| `p_relevant` | float | no | Q1: probability of "yes". |
| `p_banner_dicks` | float | no | Q2 banner group (sums to 1): Dick's Sporting Goods store or website. |
| `p_banner_house_of_sport` | float | no | Q2: a House of Sport store. |
| `p_banner_golf_galaxy` | float | no | Q2: Golf Galaxy. |
| `p_banner_foot_locker` | float | no | Q2: Foot Locker. |
| `p_banner_other` | float | no | Q2: another retailer or unclear. |
| `p_author_customer` | float | no | Q3 author group (sums to 1): a shopper or customer. |
| `p_author_employee` | float | no | Q3: a current or former employee. |
| `p_author_other` | float | no | Q3: neither, or unclear. |
| `p_topic_availability` | float | no | Q4 topic group (sums to 1): items unavailable or hard to find. |
| `p_topic_price_promo` | float | no | Q4: prices, sales, discounts. |
| `p_topic_service_staff` | float | no | Q4: staffing, help, waits, employee behavior. |
| `p_topic_fulfillment_returns` | float | no | Q4: online orders, pickup, shipping, returns. |
| `p_topic_product_quality` | float | no | Q4: quality of products bought. |
| `p_topic_store_experience` | float | no | Q4: layout, cleanliness, events, in-store features. |
| `p_topic_other` | float | no | Q4: anything else. |
| `p_stockout` | float | no | Q5: probability of "yes". |
| `p_intent_up` | float | no | Q6 intent group (sums to 1): more likely to shop here again. |
| `p_intent_flat` | float | no | Q6: no change, or not stated. |
| `p_intent_down` | float | no | Q6: less likely to shop here again. |
| `promo_score_exp` | float | no | Q7 expected level, 1 to 5: sum over levels of level x p(level). |
| `promo_entropy` | float | no | Q7 spread, 0 to ln 5 (about 1.609): -sum p ln p, natural log, with 0 ln 0 = 0. |
| `model_version` | str | no | Laya version or commit, or `fallback:<model name>` for the fallback adapter. |
| `scored_at` | datetime | no | When the item was scored, in UTC. |

### Frozen Laya questions (do not reword; see CONTEXT.md section 7)

Item prompt:

"Source: {source}. Location/community: {banner_hint}. Company context: Dick's Sporting Goods (DKS) operates Dick's Sporting Goods, House of Sport, Golf Galaxy, and Foot Locker stores. Text: {text}"

- Q1 relevant (noul): "Does this text describe a first-hand experience or observation about shopping at, buying from, or working at Dick's Sporting Goods, House of Sport, Golf Galaxy, or Foot Locker?"
- Q2 banner (choice): dicks = "Dick's Sporting Goods store or website"; house_of_sport = "a House of Sport store"; golf_galaxy = "Golf Galaxy"; foot_locker = "Foot Locker"; other = "another retailer or unclear".
- Q3 author (choice): customer = "a shopper or customer"; employee = "a current or former employee"; other = "neither, or unclear".
- Q4 topic (choice, main subject): availability = "products, sizes, or items unavailable or hard to find"; price_promo = "prices, sales, discounts, coupons, markdowns"; service_staff = "staffing levels, help, wait times, employee behavior"; fulfillment_returns = "online orders, store pickup, shipping, returns"; product_quality = "quality of products bought"; store_experience = "store layout, cleanliness, events, in-store features"; other = "anything else".
- Q5 stockout (noul): "Does the text report that a product, size, or item the author wanted was unavailable or out of stock?"
- Q6 intent (choice): up = "the experience makes the author more likely to shop here again"; flat = "no change, or not stated"; down = "the experience makes the author less likely to shop here again".
- Q7 promo (score, 5 levels): 1 = "discounts not mentioned or irrelevant"; 2 = "discounts mentioned in passing"; 3 = "discounts were one reason among several"; 4 = "discounts were the main reason"; 5 = "the purchase or visit happened only because of a discount".

## File 3: `data/fundamentals/dks_quarters.csv`

One row per fiscal quarter, FY2021Q1 to FY2026Q3, sorted oldest first. Built by P1 from DKS earnings releases (8-K Exhibit 99.1) and 10-Q/10-K filings only.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `fiscal_quarter` | quarter | no | Unique, e.g. `FY2024Q3`. |
| `period_start` | date | no | First day of the quarter, taken from the filing (not computed). |
| `period_end` | date | no | Last day of the quarter, taken from the filing. |
| `report_date` | date | yes | Date results were released. Empty if not yet reported and no date announced. |
| `comp_pct` | float | yes | DICK'S Business comparable sales change, %. Before the Foot Locker acquisition this equals the headline consolidated comp. Empty if not yet reported. |
| `comp_fl_pct` | float | yes | Foot Locker business comparable sales change, %, when DKS reports it. Otherwise empty. |
| `net_sales_musd` | float | yes | Consolidated net sales as reported, millions of US dollars. Empty if not yet reported. |
| `gross_margin_pct` | float | yes | Gross margin, %, as reported, or gross profit / net sales x 100 (method noted in `data/fundamentals/NOTES.md`). Empty if not yet reported. |
| `source_url` | str | no | URL of the specific release or filing for that row. |

## File 4: `data/indices/quarterly_index.csv`

One row per fiscal quarter and banner: every quarter in `dks_quarters.csv` times the six banner values `all`, `dicks`, `house_of_sport`, `golf_galaxy`, `foot_locker`, `other`. Sorted by quarter, then banner in that order.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `fiscal_quarter` | quarter | no | From `dks_quarters.csv`. |
| `banner` | str | no | `all` or one of the five banner names. |
| `n_items` | int | no | Number of items in this banner with overlap share s > 0 in this quarter. |
| `n_effective` | float | no | Sum of item weights w in this quarter and banner. |
| `intent_idx` | float | yes | Purchase-intent index, -1 to +1. |
| `stockout_idx` | float | yes | Stockout index, 0 to 1. |
| `promo_idx` | float | yes | Promotion-dependence index, 1 to 5. |
| `stars_idx` | float | yes | Star-rating index, 1 to 5 (non-Laya baseline). |
| `volume_log` | float | no | ln(1 + n_effective). Always filled, including when the indices are empty. |
| `intent_shock` | float | yes | intent_idx minus its recent average (definition below). |
| `stockout_shock` | float | yes | Same for stockout_idx. |
| `promo_shock` | float | yes | Same for promo_idx. |
| `stars_shock` | float | yes | Same for stars_idx. |
| `partial` | bool | no | `True` when the data window ends before the quarter ends (coverage_frac < 1). |
| `coverage_frac` | float | no | Share of the quarter's days covered by the data, 0 to 1. |

Method (pre-registered; implement exactly):

1. **Banner of an item** = the banner with the highest `p_banner_*`. Ties go to the first in the order dicks, house_of_sport, golf_galaxy, foot_locker, other. The `all` row includes every item, whatever its banner.
2. **Overlap share** s(i, q) = the number of days in both the item's interval [date_low, date_high] and the quarter [period_start, period_end], divided by the number of days in the item's interval. Both ends count, so a one-day item has length 1.
3. **Item weight** w(i, q) = p_relevant x s(i, q).
4. **n_effective** = sum of w(i, q) over the items in the quarter and banner.
5. **intent_idx** = weighted mean of (p_intent_up - p_intent_down), weight w x p_author_customer.
6. **stockout_idx** = weighted mean of p_stockout, weight w.
7. **promo_idx** = weighted mean of promo_score_exp, weight w.
8. **stars_idx** = weighted mean of stars over items where stars is present, weight s (overlap share only, no Laya input).
9. **Threshold:** if n_effective < 15, all four `_idx` columns are empty. Missing is never neutral.
10. **Shock:** X_shock(q) = X_idx(q) - mean of the non-missing X_idx over the four quarters before q (same banner). It needs X_idx(q) present and at least 2 non-missing prior quarters; otherwise it is empty.
11. **Coverage:** data_end = the latest `scraped_at` date in `items.csv`. coverage_frac = (min(period_end, data_end) - period_start + 1 day) / (period_end - period_start + 1 day), clipped to [0, 1]. partial = coverage_frac < 1.
12. `--strict` mode drops items whose interval spans a quarter boundary; the output schema is unchanged.

## File 5: `outputs/backtest.csv`

One row per out-of-sample forecast (a forecast for a quarter the model was not fitted on). Rows come in two blocks, `signal_used = intent_shock` (primary) and then `signal_used = stockout_shock` (secondary), each sorted by quarter. Uses the `all` banner of `quarterly_index.csv` joined to `dks_quarters.csv`.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `fiscal_quarter` | quarter | no | The quarter being forecast. |
| `actual` | float | no | comp_pct of that quarter, %. |
| `pred_persist` | float | no | comp_pct of the previous quarter, %. |
| `pred_ar` | float | no | AR forecast, %. |
| `pred_ar_laya` | float | no | AR + signal_used forecast, %. |
| `pred_ar_stars` | float | yes | AR + stars_shock forecast, %. Empty when not computable. |
| `signal_used` | str | no | `intent_shock` or `stockout_shock`: the shock inside pred_ar_laya. |
| `train_end_quarter` | quarter | no | Last quarter in the training sample for this forecast. |

Models (pre-registered; fitted by ordinary least squares (OLS) with an intercept and classical standard errors; no standardization):

- persist: comp(q) = comp(q-1).
- ar: comp(q) = a + r x comp(q-1).
- ar_laya: comp(q) = a + r x comp(q-1) + b x S(q), where S = signal_used.
- ar_stars: comp(q) = a + r x comp(q-1) + b x stars_shock(q).

Expanding window: a quarter is eligible when comp(q), comp(q-1), and S(q) are all present. Sort the eligible quarters E1, E2, ... The first training sample is E1 to E6. For each k from 7 on, fit on E1 to E(k-1) and forecast Ek. `pred_ar` uses the same training quarters as `pred_ar_laya`. `pred_ar_stars` uses the training quarters that also have stars_shock; it is empty if fewer than 6 such quarters exist or stars_shock(Ek) is missing.

## File 6: `outputs/nowcast.json`

One JSON object with exactly these keys. Missing numbers are `null`.

| Key | Type | Meaning |
|---|---|---|
| `target_quarter` | quarter | `FY2026Q3`. |
| `beta` | float | b from ar_laya with intent_shock, fitted on all eligible completed quarters. |
| `beta_se` | float | Classical OLS standard error of b. |
| `shock_current` | float | intent_shock of the target quarter (`all` banner, partial-quarter data). |
| `pred_ar` | float | AR forecast for the target quarter, fitted on the same quarters, %. |
| `pred_ar_laya` | float | ar_laya forecast for the target quarter, %. |
| `delta_comp_bp` | float | (pred_ar_laya - pred_ar) x 100, in bp. |
| `delta_comp_bp_lo80` | float | delta_comp_bp - 1.2816 x beta_se x abs(shock_current) x 100. |
| `delta_comp_bp_hi80` | float | delta_comp_bp + 1.2816 x beta_se x abs(shock_current) x 100. |
| `verdict` | str | `nowcast` if the 80% interval [lo80, hi80] excludes zero AND ar_laya out-of-sample MAE < ar out-of-sample MAE (from metrics.csv); otherwise `scenario`. Also `scenario` if shock_current is missing. |

1.2816 is the normal-distribution multiplier for a central 80% interval. MAE is mean absolute error.

## File 7: `outputs/metrics.csv`

One row per model, in this order: `persist`, `ar`, `ar_laya`, `ar_stars`, `ar_laya_stockout`. The first four come from the `intent_shock` rows of `backtest.csv`. `ar_laya_stockout` is `pred_ar_laya` from the `stockout_shock` rows.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `model` | str | no | Model name (list above). |
| `mae_bp` | float | yes | Mean of abs(pred - actual) x 100 over the model's out-of-sample quarters, bp. Empty if n_oos = 0. |
| `rmse_bp` | float | yes | Root mean squared error x 100, bp. Empty if n_oos = 0. |
| `n_oos` | int | no | Number of out-of-sample quarters with a prediction. |
| `n_beats_ar` | int | no | Quarters where abs(pred - actual) < abs(pred_ar - actual), strictly. 0 for `ar` by definition. |

## File 8: `outputs/leadlag.csv`

Six rows: signal `intent_idx` then `stockout_idx`, each with lag -1, 0, +1. Uses the `all` banner and completed (non-partial) quarters only.

| Column | Type | Missing allowed | Meaning |
|---|---|---|---|
| `signal` | str | no | `intent_idx` or `stockout_idx`. |
| `lag` | int | no | -1, 0, or 1. The correlation pairs signal(q) with comp_pct(q + lag). lag = 1 means the signal leads comps by one quarter. |
| `corr` | float | yes | Pearson correlation. Empty if n < 3. |
| `n` | int | no | Number of quarter pairs with both values present. |

## File 9: `data/labels/agreement.json`

How often Laya agrees with the 50 hand labels in `data/labels/handlabel_50.csv`. One JSON object with these keys:

| Key | Type | Meaning |
|---|---|---|
| `n_items` | int | Number of hand-labelled items. |
| `model_version` | str | Laya version used. |
| `questions` | list | One object per question, in order relevant, topic, stockout, intent. |

Each object in `questions`:

| Key | Type | Meaning |
|---|---|---|
| `question` | str | `relevant`, `topic`, `stockout`, or `intent`. |
| `n` | int | Items with a non-empty human label for this question. |
| `pct_agreement` | float | 100 x (items where Laya's label equals the human label) / n. |
| `cohen_kappa` | float or null | Cohen's kappa (agreement corrected for chance), unweighted. `null` when undefined. |

Laya's label: relevant and stockout are "yes" when the probability is at least 0.5. Topic and intent are the option with the highest probability.
