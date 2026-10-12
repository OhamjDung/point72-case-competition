"""Import a Google Maps reviews export Tom produced with Apify. Never scrapes anything."""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any

from scraping.places import Banner, match_banner
from scraping.reviews import parse_rfc3339
from scraping.schema import Document, Store
from scraping.store import get_store, upsert_document, upsert_store
from scraping.text import author_hash, state_code, tag_companies

FIELD_MAP: dict[str, tuple[str, ...]] = {
    "review_id": ("reviewId",),
    "place_id": ("placeId",),
    "place_name": ("title",),
    "text": ("text",),
    "stars": ("stars",),
    "published": ("publishedAtDate",),
    "reviewer": ("name",),
    "url": ("reviewUrl", "url"),
}


def _field(row: dict, key: str) -> Any:
    for name in FIELD_MAP[key]:
        if row.get(name) not in (None, ""):
            return row[name]
    return None


def import_apify(
    conn: sqlite3.Connection, rows: list[dict], banners: list[Banner],
    collected_at: datetime, salt: str,
) -> dict[str, int]:
    counts = dict.fromkeys(
        ("inserted", "updated", "unchanged", "deleted", "skipped_missing_fields",
         "skipped_unknown_store", "stores_created"),
        0,
    )
    for row in rows:
        place_id, review_id = _field(row, "place_id"), _field(row, "review_id")
        published = _field(row, "published")
        if not (place_id and review_id and published):
            counts["skipped_missing_fields"] += 1
            continue
        store = get_store(conn, place_id)
        if store is None:
            name = _field(row, "place_name") or ""
            banner = match_banner(name, banners)
            if banner is None:
                counts["skipped_unknown_store"] += 1
                continue
            store = Store(
                store_id=place_id, banner=banner.banner, company=banner.company,
                cohort=banner.cohort, priority=banner.priority, name=name,
                address=row.get("address"), city=row.get("city"),
                state=state_code(row.get("state")), postal_code=row.get("postalCode"),
                lat=None, lng=None, discovery_query="apify_import", discovered_at=collected_at,
            )
            upsert_store(conn, store)
            counts["stores_created"] += 1
        text = _field(row, "text")
        counts[upsert_document(conn, Document(
            doc_id=f"apify_gmaps:{review_id}", platform="apify_google_maps", doc_type="review",
            cohort=store.cohort, store_id=store.store_id, body=text, rating=_field(row, "stars"),
            created_at=parse_rfc3339(published), collected_at=collected_at,
            author_hash=author_hash(_field(row, "reviewer"), salt), url=_field(row, "url"),
            company_mentions=tag_companies(text or ""), source_listings=["apify_import"],
        ))] += 1
    conn.commit()
    return counts
