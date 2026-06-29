"""Streamlit application for the movie recommendation system."""

from __future__ import annotations

import logging

import pandas as pd
import streamlit as st

from src.config import load_config
from src.dashboard.dashboard import build_dashboard_figures, compute_metrics
from src.data import get_available_titles, load_movie_dataset
from src.preprocessing import prepare_movies_dataset
from src.recommender.recommender import MovieRecommender, build_recommender
from src.utils.tmdb_client import TMDBClient


st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


CONFIG = load_config()
logging.basicConfig(level=logging.INFO if CONFIG.debug else logging.WARNING)


def inject_styles() -> None:
    """Apply a professional dark metallic theme."""

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #0c0c0d 0%, #141416 50%, #0f0f10 100%);
            color: #f5f5f5;
        }
        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }
        .hero {
            background: linear-gradient(135deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 22px;
            padding: 24px;
            box-shadow: 0 14px 40px rgba(0, 0, 0, 0.35);
        }
        .metric-card {
            background: #161618;
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 18px;
            padding: 18px;
            min-height: 110px;
        }
        .movie-card {
            background: #151518;
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 18px;
            padding: 16px;
            height: 100%;
        }
        .movie-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.35rem;
        }
        .movie-meta {
            color: #bbbbbb;
            font-size: 0.9rem;
        }
        .movie-score {
            color: #d9d9d9;
            font-weight: 700;
            margin-top: 0.4rem;
        }
        .section-title {
            font-size: 1.4rem;
            font-weight: 800;
            margin-bottom: 0.5rem;
        }
        .stButton>button {
            background: linear-gradient(135deg, #d1d1d1, #6e6e6e);
            color: #0f0f10;
            border: 0;
            border-radius: 12px;
            font-weight: 700;
        }
        .stButton>button:hover {
            opacity: 0.92;
            border: 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_data(show_spinner=False)
def load_dataset() -> pd.DataFrame:
    """Load the best available dataset for the app."""

    dataset = load_movie_dataset()
    if dataset.empty:
        dataset = prepare_movies_dataset()
    return dataset


@st.cache_resource(show_spinner=False)
def load_recommender(dataframe: pd.DataFrame) -> MovieRecommender:
    """Build the recommender once and reuse it."""

    return build_recommender(dataframe, fuzzy_threshold=CONFIG.fuzzy_threshold)


@st.cache_resource(show_spinner=False)
def load_tmdb_client() -> TMDBClient:
    """Build the TMDB client from configuration."""

    return TMDBClient(api_key=CONFIG.tmdb_api_key, base_url=CONFIG.tmdb_base_url)


def render_metric(label: str, value: object, help_text: str = "") -> None:
    """Render a compact metric card."""

    st.markdown(
        f"""
        <div class="metric-card">
            <div style="color:#bbbbbb;font-size:0.9rem;">{label}</div>
            <div style="color:#ffffff;font-size:2rem;font-weight:800;line-height:1.1;">{value}</div>
            <div style="color:#8c8c8c;font-size:0.85rem;">{help_text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_recommendation_card(movie: dict[str, object], poster_url: str | None = None) -> None:
    """Render a single recommendation card."""

    with st.container():
        st.markdown('<div class="movie-card">', unsafe_allow_html=True)
        columns = st.columns([1, 1.75])
        with columns[0]:
            if poster_url:
                st.image(poster_url, width="stretch")
            else:
                st.markdown(
                    """
                    <div style="height:260px;border-radius:14px;background:linear-gradient(135deg,#252527,#141416);border:1px solid rgba(255,255,255,0.08);
                    display:flex;align-items:center;justify-content:center;color:#cfcfcf;font-size:2rem;font-weight:800;">
                    🎬
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        with columns[1]:
            st.markdown(f"<div class='movie-title'>{movie.get('title', 'Untitled')}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='movie-meta'><strong>Genres:</strong> {movie.get('genres', 'N/A')}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='movie-meta'>{movie.get('overview', 'No overview available.')}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<div class='movie-score'>Similarity: {movie.get('score', 0):.2%}</div>",
                unsafe_allow_html=True,
            )
            rating = movie.get("vote_average", 0.0)
            st.caption(f"TMDB Rating: {rating:.1f}" if isinstance(rating, (int, float)) and rating else "TMDB Rating unavailable")
        st.markdown('</div>', unsafe_allow_html=True)


def render_home(dataframe: pd.DataFrame) -> None:
    """Render the home page content."""

    metrics = compute_metrics(dataframe)
    st.markdown(
        """
        <div class="hero">
            <div style="color:#bfbfbf;font-size:0.9rem;letter-spacing:0.14em;text-transform:uppercase;">Movie Recommendation System</div>
            <h1 style="margin:0.35rem 0 0.6rem 0;color:#ffffff;font-size:2.4rem;">Professional content-based recommendations</h1>
            <p style="margin:0;color:#d7d7d7;max-width:900px;line-height:1.7;">
                Search a movie title, get intelligent fuzzy matching, and explore top recommendations with a metallic dark UI designed for internship and portfolio presentation.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write("")
    metric_cols = st.columns(4)
    with metric_cols[0]:
        render_metric("Total Movies", metrics["total_movies"], "Available in the current dataset")
    with metric_cols[1]:
        render_metric("Total Genres", metrics["total_genres"], "Flattened from genre tags")
    with metric_cols[2]:
        render_metric("Average Rating", metrics["average_rating"], "Based on available metadata")
    with metric_cols[3]:
        render_metric("Dataset Rows", metrics["rating_count"], "Records in the working set")


def render_recommender_tab(dataframe: pd.DataFrame, recommender: MovieRecommender, tmdb_client: TMDBClient) -> None:
    """Render the recommendation workflow."""

    st.markdown('<div class="section-title">Find a Movie</div>', unsafe_allow_html=True)
    titles = get_available_titles(dataframe)
    search_mode = st.radio("Search mode", ["Dropdown", "Free text"], horizontal=True)

    movie_title = ""
    if search_mode == "Dropdown":
        movie_title = st.selectbox("Choose a movie", titles)
    else:
        movie_title = st.text_input("Enter movie title", placeholder="Example: Interstelar")

    if st.button("Recommend movies", width="stretch"):
        with st.spinner("Generating recommendations..."):
            result = recommender.recommend(movie_title, top_n=CONFIG.max_recommendations)

        if result.message:
            st.info(result.message)
        if result.suggestion and result.suggestion.lower() != movie_title.strip().lower():
            st.warning(f"Did you mean **{result.suggestion}**?")

        if not result.recommendations:
            st.error("No recommendations available. Please try a different title.")
            return

        if result.matched_title:
            st.success(f"Showing similar movies for **{result.matched_title}**")

        for index, recommendation in enumerate(result.recommendations, start=1):
            cols = st.columns([0.75, 5])
            with cols[0]:
                st.markdown(
                    f"""
                    <div style="height:60px;width:60px;border-radius:14px;background:linear-gradient(135deg,#2a2a2d,#111113);
                    border:1px solid rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:800;">
                    {index}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with cols[1]:
                poster_url = tmdb_client.get_poster_url(str(recommendation["title"]))
                render_recommendation_card(recommendation, poster_url=poster_url)


def render_dashboard_tab(dataframe: pd.DataFrame) -> None:
    """Render dashboard visuals."""

    metrics = compute_metrics(dataframe)
    figs = build_dashboard_figures(dataframe)
    cols = st.columns(3)
    with cols[0]:
        render_metric("Top Genres", len(metrics["top_genres"]), "Most common labels in the dataset")
    with cols[1]:
        render_metric("Ratings Available", metrics["rating_count"], "Rows usable for analytics")
    with cols[2]:
        render_metric("Average Rating", metrics["average_rating"], "Numeric vote average")

    if "genre_bar" in figs:
        st.plotly_chart(figs["genre_bar"], width="stretch")
    if "rating_hist" in figs:
        st.plotly_chart(figs["rating_hist"], width="stretch")


def render_about() -> None:
    """Render about-page information."""

    st.markdown(
        """
        <div class="hero">
            <h2 style="margin-top:0;color:#ffffff;">About this project</h2>
            <p style="color:#d7d7d7;line-height:1.8;">
                This application demonstrates a clean content-based movie recommendation workflow built with Python, Pandas,
                NumPy, Scikit-Learn, Streamlit, Plotly, Requests, and RapidFuzz. It is designed to work even when the MovieLens
                dataset is not yet available by using a curated demo dataset, so the app remains functional immediately after setup.
            </p>
            <ul style="color:#d7d7d7;line-height:1.8;">
                <li>Professional dark metallic UI</li>
                <li>TF-IDF and cosine similarity recommendations</li>
                <li>Graceful fallback data and TMDB-free execution</li>
                <li>Optional poster enrichment when a TMDB API key is provided</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    """Application entry point."""

    inject_styles()
    dataframe = load_dataset()
    recommender = load_recommender(dataframe)
    tmdb_client = load_tmdb_client()

    st.sidebar.title("Movie Recommender")
    st.sidebar.caption("Content-based recommendations with a mature metallic theme.")
    st.sidebar.success("Functional even without TMDB API key")
    if not tmdb_client.is_available():
        st.sidebar.warning("TMDB API key not configured yet.")

    tab_home, tab_recommend, tab_dashboard, tab_about = st.tabs([
        "Home",
        "Recommendation System",
        "Analytics Dashboard",
        "About Project",
    ])

    with tab_home:
        render_home(dataframe)
    with tab_recommend:
        render_recommender_tab(dataframe, recommender, tmdb_client)
    with tab_dashboard:
        render_dashboard_tab(dataframe)
    with tab_about:
        render_about()


if __name__ == "__main__":
    main()
