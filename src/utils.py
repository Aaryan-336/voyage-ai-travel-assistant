import re
import string
from src.config import CITY_ALIASES, KNOWN_CITIES


def normalize_city(raw: str) -> str:
    cleaned = raw.lower().strip()
    cleaned = cleaned.translate(str.maketrans("", "", string.punctuation))
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if cleaned in CITY_ALIASES:
        return CITY_ALIASES[cleaned]
    for alias, canonical in CITY_ALIASES.items():
        if alias in cleaned:
            return canonical
    return cleaned


def extract_city_from_query(query: str) -> str:
    query_lower = query.lower().strip()
    for alias, canonical in CITY_ALIASES.items():
        if alias in query_lower:
            return canonical
    for city in KNOWN_CITIES:
        if city in query_lower:
            return city
    patterns = [
        r"(?:about|in|visit|to|for|explore)\s+([a-z\s]+?)(?:\s*[\?\.\!]|$)",
        r"tell me about\s+([a-z\s]+?)(?:\s*[\?\.\!]|$)",
    ]
    for pattern in patterns:
        match = re.search(pattern, query_lower)
        if match:
            candidate = match.group(1).strip()
            normalized = normalize_city(candidate)
            if len(normalized) > 1:
                return normalized
    words = query.split()
    capitalized = [w for w in words if w[0].isupper() and len(w) > 2] if words else []
    if capitalized:
        return normalize_city(" ".join(capitalized))
    return normalize_city(query)


def is_followup_query(query: str) -> bool:
    followup_patterns = [
        "what about next", "show me the forecast", "more images",
        "again", "the same", "same city", "tell me more",
        "what else", "forecast again", "more about",
    ]
    return any(p in query.lower() for p in followup_patterns)


def city_in_store(city: str) -> bool:
    return normalize_city(city) in KNOWN_CITIES
