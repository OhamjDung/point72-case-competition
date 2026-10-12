# scraping

Collects Reddit posts and comments (PRAW) and store-attributed Google reviews into
`scraping/data/scraping.sqlite`, then exports sentiment-ready CSVs. The data schema and
sentiment guidance are in `docs/superpowers/plans/2026-10-12-scraping.md`.

Stores covered (edit `config.json`; list order = review priority): DICK'S Sporting Goods,
House of Sport, Golf Galaxy, Going Going Gone!, Foot Locker (incl. Kids Foot Locker) and
Champs Sports (DKS-owned since 2025-09-08), plus competitors Academy, Hibbett, Scheels.
US only (contiguous US, Alaska, Hawaii).

## One-time setup

1. `uv --cache-dir .uv-cache pip install --python .venv/Scripts/python.exe praw`
2. Reddit: create a "script" app at https://www.reddit.com/prefs/apps (read-only use).
   Reddit may require approval for new API apps. Apply early.
3. Google: create a Cloud project, enable **Places API (New)**, create an API key
   restricted to that API, and set a **daily request quota** in Cloud Console so usage
   stays inside the free monthly allowance (a billing account is required).
4. Set secrets for the session (PowerShell). Never commit them:

```powershell
$env:REDDIT_CLIENT_ID = "<client id>"
$env:REDDIT_CLIENT_SECRET = "<secret>"
$env:REDDIT_USER_AGENT = "script:point72-dks-research:v0.1 (by u/<your reddit username>)"
$env:GOOGLE_MAPS_API_KEY = "<key>"
$env:SCRAPING_AUTHOR_SALT = "<any long random string; keep it constant>"
```

## Commands

```powershell
.venv/Scripts/python.exe -m scraping reddit                      # all 4 subreddits
.venv/Scripts/python.exe -m scraping reddit --subreddit retail --no-comments
.venv/Scripts/python.exe -m scraping stores-discover             # rarely (monthly)
.venv/Scripts/python.exe -m scraping reviews --max-stores 200    # capped by config
.venv/Scripts/python.exe -m scraping apify-import --input path\to\export.json
.venv/Scripts/python.exe -m scraping status
.venv/Scripts/python.exe -m scraping export                      # -> scraping/data/exports/
```

Cadence: Reddit weekly (coverage grows forward; each listing caps near 1,000 posts),
reviews monthly (5 "most relevant" reviews per store plus a rating/count snapshot).
Schedule with Windows Task Scheduler if needed.

## Limits

- PRAW cannot reach full subreddit history. `status` shows the oldest post per subreddit.
- Google returns at most 5 reviews per store. Use `store_snapshots` for trends.
- Author-deleted Reddit content is purged on the next run that sees the deletion.
- `created_at` is when content was posted; `first_collected_at` is when we saw it.
  Retrospective collection is not point-in-time capture.
