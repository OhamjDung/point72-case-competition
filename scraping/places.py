from __future__ import annotations

import os
import re
import sqlite3
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any

import httpx

from scraping.schema import Cohort, Store
from scraping.store import upsert_store
from scraping.text import normalize_quotes

BASE = "https://places.googleapis.com/v1"
# The field mask sets the billing tier: keep discovery minimal; reviews only in details.
SEARCH_MASK = (
    "places.id,places.displayName,places.formattedAddress,places.location,"
    "places.addressComponents,nextPageToken"
)
DETAILS_MASK = "id,rating,userRatingCount,businessStatus,reviews"
RESULT_CAP = 60  # Text Search returns at most 3 pages of 20
Box = tuple[float, float, float, float]  # low_lat, low_lng, high_lat, high_lng
US_BOXES: list[Box] = [
    (24.4, -125.0, 49.5, -66.9),  # contiguous US
    (51.2, -179.9, 71.5, -129.9),  # Alaska
    (18.9, -160.3, 22.3, -154.8),  # Hawaii
]
RETRY_STATUS = {429, 500, 502, 503, 504}


@dataclass(frozen=True)
class Banner:
    banner: str
    company: str
    cohort: Cohort
    query: str
    name_regex: str
    priority: int


def banners_from_config(config: dict) -> list[Banner]:
    return [Banner(priority=i, **b) for i, b in enumerate(config["places"]["banners"])]


def match_banner(name: str, banners: list[Banner]) -> Banner | None:
    clean = normalize_quotes(name)
    return next((b for b in banners if re.search(b.name_regex, clean, re.IGNORECASE)), None)


class PlacesClient:
    def __init__(
        self, api_key: str | None = None, transport: httpx.BaseTransport | None = None,
        max_retries: int = 3, sleep: Callable[[float], Any] = time.sleep,
    ) -> None:
        key = api_key or os.environ.get("GOOGLE_MAPS_API_KEY")
        if not key:
            raise RuntimeError("missing environment variable: GOOGLE_MAPS_API_KEY")
        self._client = httpx.Client(
            timeout=30, transport=transport, headers={"X-Goog-Api-Key": key}
        )
        self.max_retries = max_retries
        self.sleep = sleep
        self.calls = {"search": 0, "details": 0}

    def _request(self, method: str, url: str, mask: str, **kwargs: Any) -> dict:
        for attempt in range(self.max_retries + 1):
            response = self._client.request(
                method, url, headers={"X-Goog-FieldMask": mask}, **kwargs
            )
            if response.status_code in RETRY_STATUS and attempt < self.max_retries:
                self.sleep(float(response.headers.get("Retry-After", 2**attempt)))
                continue
            response.raise_for_status()
            return response.json()
        raise RuntimeError("retries exhausted")

    def search_text(self, query: str, box: Box) -> list[dict]:
        low_lat, low_lng, high_lat, high_lng = box
        body: dict[str, Any] = {
            "textQuery": query, "pageSize": 20,
            "locationRestriction": {"rectangle": {
                "low": {"latitude": low_lat, "longitude": low_lng},
                "high": {"latitude": high_lat, "longitude": high_lng},
            }},
        }
        places: list[dict] = []
        token = None
        while True:
            payload = body | ({"pageToken": token} if token else {})
            data = self._request("POST", f"{BASE}/places:searchText", SEARCH_MASK, json=payload)
            self.calls["search"] += 1
            places += data.get("places", [])
            token = data.get("nextPageToken")
            if not token or len(places) >= RESULT_CAP:
                return places

    def details(self, place_id: str) -> dict:
        data = self._request("GET", f"{BASE}/places/{place_id}", DETAILS_MASK)
        self.calls["details"] += 1
        return data

    def close(self) -> None:
        self._client.close()


def _split(box: Box) -> list[Box]:
    low_lat, low_lng, high_lat, high_lng = box
    mid_lat, mid_lng = (low_lat + high_lat) / 2, (low_lng + high_lng) / 2
    return [
        (low_lat, low_lng, mid_lat, mid_lng), (low_lat, mid_lng, mid_lat, high_lng),
        (mid_lat, low_lng, high_lat, mid_lng), (mid_lat, mid_lng, high_lat, high_lng),
    ]


def search_tiled(
    client: PlacesClient, query: str, box: Box, max_depth: int, truncated: list[Box],
    depth: int = 0,
) -> dict[str, dict]:
    places = client.search_text(query, box)
    found = {p["id"]: p for p in places}
    if len(places) >= RESULT_CAP:
        if depth >= max_depth:
            truncated.append(box)
        else:
            for child in _split(box):
                found.update(search_tiled(client, query, child, max_depth, truncated, depth + 1))
    return found


def _component(place: dict, kind: str, short: bool = False) -> str | None:
    for comp in place.get("addressComponents", []):
        if kind in comp.get("types", []):
            return comp.get("shortText" if short else "longText")
    return None


def discover_stores(
    client: PlacesClient, conn: sqlite3.Connection, banners: list[Banner], max_depth: int,
    now: datetime | None = None,
) -> dict[str, int]:
    now = now or datetime.now(UTC)
    counts = {"matched": 0, "rejected_name": 0, "truncated_tiles": 0}
    for banner in banners:
        truncated: list[Box] = []
        found: dict[str, dict] = {}
        for box in US_BOXES:
            found.update(search_tiled(client, banner.query, box, max_depth, truncated))
        counts["truncated_tiles"] += len(truncated)
        for place in found.values():
            name = place.get("displayName", {}).get("text", "")
            if match_banner(name, [banner]) is None:
                counts["rejected_name"] += 1
                continue
            location = place.get("location", {})
            upsert_store(conn, Store(
                store_id=place["id"], banner=banner.banner, company=banner.company,
                cohort=banner.cohort, priority=banner.priority, name=normalize_quotes(name),
                address=place.get("formattedAddress"), city=_component(place, "locality"),
                state=_component(place, "administrative_area_level_1", short=True),
                postal_code=_component(place, "postal_code"),
                lat=location.get("latitude"), lng=location.get("longitude"),
                discovery_query=banner.query, discovered_at=now,
            ))
            counts["matched"] += 1
    conn.commit()
    counts.update({f"{kind}_calls": n for kind, n in client.calls.items()})
    return counts
