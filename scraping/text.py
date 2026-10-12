from __future__ import annotations

import hashlib
import re

DELETED_MARKERS = frozenset({"[deleted]", "[removed]"})
_QUOTES = str.maketrans({"’": "'", "‘": "'"})

# "dicks" alone is profanity-ambiguous: require an apostrophe or "sporting goods".
COMPANY_PATTERNS: dict[str, re.Pattern[str]] = {
    "DKS": re.compile(
        r"\bdick'?s sporting goods\b|\bdick's\b(?!\s+(?:last resort|drive))|\bdsg\b"
        r"|\bhouse of sport\b|\bgolf galaxy\b",
        re.I,
    ),
    "FL": re.compile(r"\b(?:kids )?foot ?locker\b|\bchamps sports\b", re.I),
    "ACADEMY": re.compile(r"\bacademy sports\b", re.I),
    "HIBBETT": re.compile(r"\bhibbett\b", re.I),
    "SCHEELS": re.compile(r"\bscheels\b", re.I),
    "WALMART": re.compile(r"\bwal-?mart\b", re.I),
    "TARGET": re.compile(
        r"\btarget (?:store|team members?|employees?)\b|\b(?:at|for) target\b", re.I
    ),
    "COSTCO": re.compile(r"\bcostco\b", re.I),
}

US_STATE_CODES = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    "colorado": "CO", "connecticut": "CT", "delaware": "DE", "district of columbia": "DC",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID", "illinois": "IL",
    "indiana": "IN", "iowa": "IA", "kansas": "KS", "kentucky": "KY", "louisiana": "LA",
    "maine": "ME", "maryland": "MD", "massachusetts": "MA", "michigan": "MI",
    "minnesota": "MN", "mississippi": "MS", "missouri": "MO", "montana": "MT",
    "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ",
    "new mexico": "NM", "new york": "NY", "north carolina": "NC", "north dakota": "ND",
    "ohio": "OH", "oklahoma": "OK", "oregon": "OR", "pennsylvania": "PA",
    "rhode island": "RI", "south carolina": "SC", "south dakota": "SD", "tennessee": "TN",
    "texas": "TX", "utah": "UT", "vermont": "VT", "virginia": "VA", "washington": "WA",
    "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY",
}


def normalize_quotes(text: str) -> str:
    return text.translate(_QUOTES)


def tag_companies(text: str) -> list[str]:
    clean = normalize_quotes(text or "")
    return sorted(name for name, pattern in COMPANY_PATTERNS.items() if pattern.search(clean))


def author_hash(name: str | None, salt: str) -> str | None:
    if not name or name in DELETED_MARKERS:
        return None
    if not salt:
        raise ValueError("author salt required (set SCRAPING_AUTHOR_SALT)")
    return hashlib.sha256(f"{salt}:{name}".encode()).hexdigest()[:16]


def state_code(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if len(value) == 2 and value.upper() in US_STATE_CODES.values():
        return value.upper()
    return US_STATE_CODES.get(value.lower())
