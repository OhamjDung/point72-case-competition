from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Platform = Literal["reddit", "google_maps", "apify_google_maps"]
DocType = Literal["post", "comment", "review"]
Cohort = Literal["dks", "general_retail", "competitor"]


def _utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        raise ValueError("timestamps must be timezone-aware")
    return value.astimezone(UTC)


class Document(BaseModel):
    model_config = ConfigDict(extra="forbid")

    doc_id: str = Field(min_length=1)
    platform: Platform
    doc_type: DocType
    cohort: Cohort
    community: str | None = None
    store_id: str | None = None
    thread_id: str | None = None
    parent_id: str | None = None
    title: str | None = None
    body: str | None = None
    rating: float | None = None
    score: int | None = None
    num_comments: int | None = None
    created_at: datetime
    collected_at: datetime
    author_hash: str | None = None
    author_flair: str | None = None
    link_flair: str | None = None
    url: str | None = None
    is_deleted: bool = False
    edited: bool = False
    company_mentions: list[str] = Field(default_factory=list)
    source_listings: list[str] = Field(min_length=1)

    @field_validator("created_at", "collected_at")
    @classmethod
    def aware_utc(cls, value: datetime) -> datetime:
        return _utc(value)


class Store(BaseModel):
    model_config = ConfigDict(extra="forbid")

    store_id: str = Field(min_length=1)
    banner: str
    company: str
    cohort: Cohort
    priority: int
    name: str
    address: str | None
    city: str | None
    state: str | None
    postal_code: str | None
    lat: float | None
    lng: float | None
    discovery_query: str
    discovered_at: datetime

    @field_validator("discovered_at")
    @classmethod
    def aware_utc(cls, value: datetime) -> datetime:
        return _utc(value)


class StoreSnapshot(BaseModel):
    model_config = ConfigDict(extra="forbid")

    store_id: str
    collected_at: datetime
    rating: float | None
    user_rating_count: int | None
    business_status: str | None

    @field_validator("collected_at")
    @classmethod
    def aware_utc(cls, value: datetime) -> datetime:
        return _utc(value)
