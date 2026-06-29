"""Content-based movie recommendation engine."""

from __future__ import annotations

from dataclasses import dataclass
import logging

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.utils.fuzzy_search import find_best_match


logger = logging.getLogger(__name__)


@dataclass
class RecommendationResult:
    """Structured recommendation response."""

    query_title: str
    matched_title: str | None
    suggestion: str | None
    recommendations: list[dict[str, object]]
    message: str


class MovieRecommender:
    """Build a TF-IDF based recommender over movie metadata."""

    def __init__(self, dataframe: pd.DataFrame, fuzzy_threshold: int = 80) -> None:
        if dataframe.empty:
            raise ValueError("Movie dataframe cannot be empty.")

        self.dataframe = dataframe.copy().reset_index(drop=True)
        self.fuzzy_threshold = fuzzy_threshold
        self.tfidf_vectorizer = TfidfVectorizer(stop_words="english")
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.dataframe["combined_text"].fillna(""))
        self.cosine_similarities = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        self.indices = pd.Series(self.dataframe.index, index=self.dataframe["title"].str.lower()).drop_duplicates()

    def resolve_title(self, query: str) -> tuple[str | None, str | None]:
        """Resolve a movie title or suggest the closest match."""

        normalized_query = query.strip().lower()
        if normalized_query in self.indices:
            return self.dataframe.loc[self.indices[normalized_query], "title"], None

        title = find_best_match(query, self.dataframe["title"].tolist(), threshold=self.fuzzy_threshold)
        if title:
            return title, title if title.lower() != normalized_query else None
        return None, None

    def recommend(self, movie_title: str, top_n: int = 10) -> RecommendationResult:
        """Return the top-N most similar movies."""

        if not movie_title or not movie_title.strip():
            return RecommendationResult(
                query_title=movie_title,
                matched_title=None,
                suggestion=None,
                recommendations=[],
                message="Please enter a valid movie title.",
            )

        matched_title, suggestion = self.resolve_title(movie_title)
        if matched_title is None:
            return RecommendationResult(
                query_title=movie_title,
                matched_title=None,
                suggestion=None,
                recommendations=[],
                message="Movie not found. Try a different title or use the dropdown.",
            )

        if suggestion and suggestion.lower() != movie_title.strip().lower():
            logger.info("Using fuzzy match '%s' for '%s'", suggestion, movie_title)

        movie_index = int(self.indices[matched_title.lower()])
        similarity_scores = list(enumerate(self.cosine_similarities[movie_index]))
        similarity_scores = sorted(similarity_scores, key=lambda item: item[1], reverse=True)

        recommendations: list[dict[str, object]] = []
        for index, score in similarity_scores[1 : top_n + 1]:
            row = self.dataframe.iloc[index]
            recommendations.append(
                {
                    "title": row.get("title", ""),
                    "genres": row.get("genres", ""),
                    "overview": row.get("overview", ""),
                    "vote_average": float(row.get("vote_average", 0.0)),
                    "poster_path": row.get("poster_path", ""),
                    "score": round(float(score), 4),
                }
            )

        return RecommendationResult(
            query_title=movie_title,
            matched_title=matched_title,
            suggestion=suggestion,
            recommendations=recommendations,
            message=f"Found {len(recommendations)} recommendations for '{matched_title}'.",
        )


def build_recommender(dataframe: pd.DataFrame, fuzzy_threshold: int = 80) -> MovieRecommender:
    """Create a ready-to-use recommender instance."""

    return MovieRecommender(dataframe=dataframe, fuzzy_threshold=fuzzy_threshold)
