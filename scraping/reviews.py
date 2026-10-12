from __future__ import annotations

import re
import sqlite3
from datetime import UTC, datetime

from scraping.places import PlacesClient
from scraping.schema import Document, Store, StoreSnapshot
from scraping.store import add_snapshot, stores_for_reviews, upsert_document
from scraping.text import author_hash, tag_companies


def parse_rfc3339(value: str) -> datetime:
    clean = re.sub(r"(\.\d{6})\d+", r"\1", value.replace("Z", "+00:00"))
    return datetime.fromisoformat(clean).astimezone(UTC)


def review_to_doc(
    review: dict, store: Store, collected_at: datetime, salt: str
) -> Document | None:
    published = review.get("publishTime")
    if not published:
        return None
    text = (review.get("text") or review.get("originalText") or {}).get("text")
    return Document(
        doc_id=f"gmaps:{review['name']}", platform="google_maps", doc_type="review",
        cohort=store.cohort, store_id=store.store_id, body=text, rating=review.get("rating"),
        created_at=parse_rfc3339(published), collected_at=collected_at,
        author_hash=author_hash(review.get("authorAttribution", {}).get("displayName"), salt),
        url=review.get("googleMapsUri"), company_mentions=tag_companies(text or ""),
        source_listings=["places_details:most_relevant"],
    )


def fetch_reviews(
    client: PlacesClient, conn: sqlite3.Connection, limit: int, salt: str,
    now: datetime | None = None,
) -> dict[str, int]:
    now = now or datetime.now(UTC)
    counts = dict.fromkeys(
        ("stores", "inserted", "updated", "unchanged", "deleted", "skipped_no_time"), 0
    )
    for store in stores_for_reviews(conn, limit):
        data = client.details(store.store_id)
        add_snapshot(conn, StoreSnapshot(
            store_id=store.store_id, collected_at=now, rating=data.get("rating"),
            user_rating_count=data.get("userRatingCount"),
            business_status=data.get("businessStatus"),
        ))
        for review in data.get("reviews", []):
            doc = review_to_doc(review, store, now, salt)
            if doc is None:
                counts["skipped_no_time"] += 1
                continue
            counts[upsert_document(conn, doc)] += 1
        counts["stores"] += 1
        conn.commit()
    return counts
