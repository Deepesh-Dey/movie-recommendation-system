"""Central configuration for the movie recommendation project."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"


@dataclass(frozen=True)
class AppConfig:
    """Application-level settings loaded from environment variables."""

    tmdb_api_key: str | None
    tmdb_base_url: str
    max_recommendations: int
    fuzzy_threshold: int
    debug: bool


def load_config() -> AppConfig:
    """Load configuration from environment variables and defaults."""

    return AppConfig(
        tmdb_api_key=os.getenv("TMDB_API_KEY") or None,
        tmdb_base_url=os.getenv("TMDB_BASE_URL", "https://api.themoviedb.org/3"),
        max_recommendations=int(os.getenv("MAX_RECOMMENDATIONS", "10")),
        fuzzy_threshold=int(os.getenv("FUZZY_THRESHOLD", "80")),
        debug=os.getenv("DEBUG", "False").lower() in {"1", "true", "yes"},
    )
