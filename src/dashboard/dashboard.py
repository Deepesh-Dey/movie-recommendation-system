"""Analytics helpers for the dashboard tab."""

from __future__ import annotations

from collections import Counter

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def split_genres(dataframe: pd.DataFrame) -> pd.Series:
    """Return a flattened genre series."""

    if "genres" not in dataframe.columns:
        return pd.Series(dtype=str)

    genres = dataframe["genres"].fillna("").astype(str).str.split("|")
    return genres.explode().str.strip().replace("", pd.NA).dropna()


def compute_metrics(dataframe: pd.DataFrame) -> dict[str, object]:
    """Compute high-level dataset metrics."""

    genre_series = split_genres(dataframe)
    genre_counts = Counter(genre_series.tolist())

    return {
        "total_movies": int(dataframe["title"].nunique()) if "title" in dataframe.columns else 0,
        "total_genres": int(len(genre_counts)),
        "top_genres": genre_counts.most_common(10),
        "average_rating": round(float(dataframe.get("vote_average", pd.Series([0.0])).mean()), 2),
        "rating_count": int(len(dataframe)),
    }


def build_dashboard_figures(dataframe: pd.DataFrame) -> dict[str, go.Figure]:
    """Build Plotly figures for the analytics dashboard."""

    genre_series = split_genres(dataframe)
    genre_counts = genre_series.value_counts().head(10).reset_index()
    genre_counts.columns = ["genre", "count"]

    figs: dict[str, go.Figure] = {}
    if not genre_counts.empty:
        figs["genre_bar"] = px.bar(
            genre_counts,
            x="count",
            y="genre",
            orientation="h",
            title="Top 10 Genres",
            color="count",
            color_continuous_scale="Greys",
        )
        figs["genre_bar"].update_layout(template="plotly_dark", paper_bgcolor="#111111", plot_bgcolor="#111111")

    if "vote_average" in dataframe.columns and not dataframe.empty:
        rating_fig = px.histogram(dataframe, x="vote_average", nbins=10, title="Rating Distribution", color_discrete_sequence=["#d9d9d9"])
        rating_fig.update_layout(template="plotly_dark", paper_bgcolor="#111111", plot_bgcolor="#111111")
        figs["rating_hist"] = rating_fig

    return figs
