"""Lightweight TMDB client with safe fallbacks."""

from __future__ import annotations

import logging
from functools import lru_cache

import requests


logger = logging.getLogger(__name__)


class TMDBClient:
    """Client for fetching movie metadata and posters from TMDB."""

    def __init__(self, api_key: str | None, base_url: str = "https://api.themoviedb.org/3") -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def is_available(self) -> bool:
        return bool(self.api_key)

    @lru_cache(maxsize=256)
    def search_movie(self, title: str) -> dict | None:
        if not self.api_key:
            return None

        try:
            response = requests.get(
                f"{self.base_url}/search/movie",
                params={"api_key": self.api_key, "query": title, "include_adult": "false"},
                timeout=10,
            )
            response.raise_for_status()
            payload = response.json()
            results = payload.get("results") or []
            return results[0] if results else None
        except Exception as exc:  # pragma: no cover - network dependent
            logger.warning("TMDB search failed for %s: %s", title, exc)
            return None

    def get_poster_url(self, title: str) -> str | None:
        movie = self.search_movie(title)
        if not movie:
            return None

        poster_path = movie.get("poster_path")
        if not poster_path:
            return None

        return f"https://image.tmdb.org/t/p/w500{poster_path}"

    def get_movie_overview(self, title: str) -> str | None:
        movie = self.search_movie(title)
        return movie.get("overview") if movie else None

    def get_movie_rating(self, title: str) -> float | None:
        movie = self.search_movie(title)
        rating = movie.get("vote_average") if movie else None
        return float(rating) if rating is not None else None
