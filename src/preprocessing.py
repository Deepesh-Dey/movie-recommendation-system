"""Preprocessing pipeline for the movie recommendation system."""

from __future__ import annotations

import logging

from src.data import build_movie_frame, load_raw_movies, save_cleaned_dataset


logger = logging.getLogger(__name__)


def prepare_movies_dataset():
    """Load, clean, enrich, and save the movie dataset."""

    raw_movies = load_raw_movies()
    logger.info("Raw dataset shape: %s", raw_movies.shape)

    cleaned_movies = build_movie_frame(raw_movies)
    logger.info("Cleaned dataset shape: %s", cleaned_movies.shape)

    save_cleaned_dataset(cleaned_movies)
    return cleaned_movies


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dataset = prepare_movies_dataset()
    print(dataset.head())
