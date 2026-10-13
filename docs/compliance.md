# Data terms check (P1, 2026-10-12)

Official pages, read 2026-10-12. Not legal advice.

## Google Maps reviews

Google Maps Platform Terms of Service, https://cloud.google.com/maps-platform/terms ("Last modified August 26, 2026"):

- 3.2.3(a) "Customer will not export, extract, or otherwise scrape Google Maps Content for use outside the Services. For example, Customer will not: (i) pre-fetch, index, store, reshare, or rehost Google Maps Content outside the services; ... (iii) copy and save business names, addresses, or user reviews".
- 3.2.3(b) "Customer will not cache Google Maps Content except as expressly permitted under the Maps Service Specific Terms."

Our method: official Places API (New), up to 5 "most relevant" reviews per store, saved to SQLite and `items.csv`.

Status: **prohibited.** Saving review text is the named example.

**Recommendation: EXCLUDE** (`python src/clean.py --drop-source google`).

## Reddit posts and comments

Data API Terms, https://redditinc.com/policies/data-api-terms ("Last Revised July 20, 2026"); User Agreement, https://redditinc.com/policies/user-agreement ("Effective July 1, 2026"):

- User Agreement: "scraping the Services without Reddit's prior written consent is prohibited". We used the official OAuth API (PRAW), not HTML scraping.
- Data API Terms 2.4: license "to copy and display the User Content using the Data API solely as necessary to ... run your App to your App Users."
- 3.1: commercial use or "research in excess of rate limits" needs a separate agreement. 3.2: no training AI models on User Content; do not "retain any User Content ... beyond your approved use case".

Our method: read-only API within rate limits, usernames replaced by salted hashes, deleted items purged (re-check of all 17,573 in-scope items on 2026-10-12: 0 deleted). Laya only scores the text (no training).

Status: **unclear.** API collection is allowed. Storing the data and republishing raw text publicly go beyond "display".

**Recommendation: USE WITH DISCLOSURE.** Publish aggregates, not raw text.
