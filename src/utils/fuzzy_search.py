"""Fuzzy matching helpers for movie title lookup."""

from __future__ import annotations

from difflib import get_close_matches

try:
    from rapidfuzz import fuzz, process
except Exception:  # pragma: no cover - fallback if rapidfuzz is unavailable
    fuzz = None
    process = None


def normalize_text(value: str) -> str:
    """Normalize text for matching."""

    return " ".join(value.lower().strip().split())


def find_best_match(query: str, choices: list[str], threshold: int = 80) -> str | None:
    """Find the closest matching movie title."""

    if not query or not choices:
        return None

    normalized_query = normalize_text(query)
    normalized_choices = {normalize_text(choice): choice for choice in choices}

    if normalized_query in normalized_choices:
        return normalized_choices[normalized_query]

    if process is not None and fuzz is not None:
        match = process.extractOne(
            normalized_query,
            list(normalized_choices.keys()),
            scorer=fuzz.WRatio,
        )
        if match and match[1] >= threshold:
            return normalized_choices[match[0]]

    match_list = get_close_matches(normalized_query, list(normalized_choices.keys()), n=1, cutoff=threshold / 100)
    if match_list:
        return normalized_choices[match_list[0]]

    return None


def suggest_title(query: str, choices: list[str], threshold: int = 80) -> str | None:
    """Return a user-friendly suggestion string if a close match exists."""

    match = find_best_match(query, choices, threshold=threshold)
    if match and normalize_text(match) != normalize_text(query):
        return match
    return None
