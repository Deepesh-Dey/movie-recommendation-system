"""Dataset loading and fallback demo data for the app."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR


DEMO_MOVIES: list[dict[str, object]] = [
    {
        "movie_id": 1,
        "title": "Interstellar",
        "genres": "Adventure|Drama|Sci-Fi",
        "overview": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
        "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
        "keywords": "space, wormhole, time dilation, survival",
        "vote_average": 8.6,
    },
    {
        "movie_id": 2,
        "title": "Inception",
        "genres": "Action|Adventure|Sci-Fi",
        "overview": "A thief who steals corporate secrets through dream-sharing technology is given a chance at redemption.",
        "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "keywords": "dream, heist, subconscious, mind-bending",
        "vote_average": 8.8,
    },
    {
        "movie_id": 3,
        "title": "The Dark Knight",
        "genres": "Action|Crime|Drama",
        "overview": "Batman faces the Joker, a criminal mastermind who plunges Gotham into chaos.",
        "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
        "keywords": "gotham, vigilante, joker, crime",
        "vote_average": 9.0,
    },
    {
        "movie_id": 4,
        "title": "The Matrix",
        "genres": "Action|Sci-Fi",
        "overview": "A hacker discovers the reality he lives in is a simulated construct called the Matrix.",
        "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
        "keywords": "simulation, hacker, artificial reality, resistance",
        "vote_average": 8.7,
    },
    {
        "movie_id": 5,
        "title": "Avengers: Endgame",
        "genres": "Action|Adventure|Drama",
        "overview": "The Avengers assemble once more to reverse the damage caused by Thanos.",
        "cast": "Robert Downey Jr., Chris Evans, Scarlett Johansson",
        "keywords": "superhero, infinity stone, team, battle",
        "vote_average": 8.4,
    },
    {
        "movie_id": 6,
        "title": "The Shawshank Redemption",
        "genres": "Drama",
        "overview": "Two imprisoned men bond over years, finding hope and redemption.",
        "cast": "Tim Robbins, Morgan Freeman, Bob Gunton",
        "keywords": "prison, hope, friendship, escape",
        "vote_average": 9.3,
    },
    {
        "movie_id": 7,
        "title": "Forrest Gump",
        "genres": "Drama|Romance",
        "overview": "The life story of a simple man whose innocence leads him through historic events.",
        "cast": "Tom Hanks, Robin Wright, Gary Sinise",
        "keywords": "life story, love, history, perseverance",
        "vote_average": 8.8,
    },
    {
        "movie_id": 8,
        "title": "Fight Club",
        "genres": "Drama|Thriller",
        "overview": "An insomniac office worker and a soap maker form an underground fight club.",
        "cast": "Brad Pitt, Edward Norton, Helena Bonham Carter",
        "keywords": "identity, rebellion, underground, psychology",
        "vote_average": 8.8,
    },
    {
        "movie_id": 9,
        "title": "Gladiator",
        "genres": "Action|Drama|Adventure",
        "overview": "A former Roman general seeks revenge against the corrupt emperor who murdered his family.",
        "cast": "Russell Crowe, Joaquin Phoenix, Connie Nielsen",
        "keywords": "rome, revenge, arena, empire",
        "vote_average": 8.5,
    },
    {
        "movie_id": 10,
        "title": "Titanic",
        "genres": "Drama|Romance",
        "overview": "A love story unfolds aboard the ill-fated RMS Titanic.",
        "cast": "Leonardo DiCaprio, Kate Winslet, Billy Zane",
        "keywords": "ship, romance, disaster, love",
        "vote_average": 7.9,
    },
    {
        "movie_id": 11,
        "title": "Dune",
        "genres": "Adventure|Drama|Sci-Fi",
        "overview": "A noble family becomes embroiled in a war for a desert planet with vast resources.",
        "cast": "Timothee Chalamet, Zendaya, Rebecca Ferguson",
        "keywords": "desert, spice, empire, destiny",
        "vote_average": 8.2,
    },
    {
        "movie_id": 12,
        "title": "John Wick",
        "genres": "Action|Thriller",
        "overview": "A retired assassin returns to the underworld after losing the last thing he loved.",
        "cast": "Keanu Reeves, Ian McShane, Halle Berry",
        "keywords": "assassin, revenge, underworld, guns",
        "vote_average": 7.9,
    },
    {
        "movie_id": 13,
        "title": "Parasite",
        "genres": "Drama|Thriller",
        "overview": "A poor family schemes to become employed by a wealthy household.",
        "cast": "Song Kang-ho, Lee Sun-kyun, Cho Yeo-jeong",
        "keywords": "class, family, deception, social divide",
        "vote_average": 8.6,
    },
    {
        "movie_id": 14,
        "title": "Toy Story",
        "genres": "Animation|Adventure|Comedy",
        "overview": "A group of toys come to life when humans are not present.",
        "cast": "Tom Hanks, Tim Allen, Annie Potts",
        "keywords": "toys, friendship, animation, adventure",
        "vote_average": 8.3,
    },
    {
        "movie_id": 15,
        "title": "The Lion King",
        "genres": "Animation|Adventure|Drama",
        "overview": "A young lion prince flees his kingdom after a family tragedy.",
        "cast": "Matthew Broderick, James Earl Jones, Jeremy Irons",
        "keywords": "lion, kingdom, coming of age, family",
        "vote_average": 8.5,
    },
    {
        "movie_id": 16,
        "title": "The Godfather",
        "genres": "Crime|Drama",
        "overview": "The aging patriarch of an organized crime dynasty transfers control to his reluctant son.",
        "cast": "Marlon Brando, Al Pacino, James Caan",
        "keywords": "mafia, family, crime, power",
        "vote_average": 9.2,
    },
]


def _normalize_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
    frame = dataframe.copy()
    frame.columns = [column.strip().lower() for column in frame.columns]
    rename_map = {
        "movieid": "movie_id",
        "movie id": "movie_id",
        "name": "title",
        "movie_title": "title",
        "genre": "genres",
        "plot": "overview",
    }
    return frame.rename(columns={column: rename_map.get(column, column) for column in frame.columns})


def load_raw_movies() -> pd.DataFrame:
    """Load raw movie data or return the built-in demo dataset."""

    candidates = [
        RAW_DATA_DIR / "movies.csv",
        RAW_DATA_DIR / "ratings.csv",
        PROCESSED_DATA_DIR / "cleaned_movies.csv",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.suffix == ".csv":
            try:
                return _normalize_columns(pd.read_csv(candidate))
            except Exception:
                continue
    return pd.DataFrame(DEMO_MOVIES)


def _combined_text(row: pd.Series) -> str:
    parts = [
        str(row.get("title", "")),
        str(row.get("genres", "")),
        str(row.get("overview", "")),
        str(row.get("cast", "")),
        str(row.get("keywords", "")),
    ]
    return " ".join(part for part in parts if part and part != "nan").strip()


def build_movie_frame(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich the movie dataset for recommendation use."""

    frame = _normalize_columns(dataframe)
    if "title" not in frame.columns:
        raise ValueError("Input dataset must contain a title column.")

    if "movie_id" not in frame.columns:
        frame["movie_id"] = range(1, len(frame) + 1)

    for column in ["genres", "overview", "cast", "keywords", "poster_path", "vote_average"]:
        if column not in frame.columns:
            frame[column] = "" if column != "vote_average" else 0.0

    frame["title"] = frame["title"].astype(str).str.strip()
    frame["genres"] = frame["genres"].fillna("").astype(str).str.strip()
    frame["overview"] = frame["overview"].fillna("").astype(str).str.strip()
    frame["cast"] = frame["cast"].fillna("").astype(str).str.strip()
    frame["keywords"] = frame["keywords"].fillna("").astype(str).str.strip()
    frame["poster_path"] = frame["poster_path"].fillna("").astype(str).str.strip()
    frame["vote_average"] = pd.to_numeric(frame["vote_average"], errors="coerce").fillna(0.0)

    frame = frame.drop_duplicates(subset=["title"]).reset_index(drop=True)
    frame["combined_text"] = frame.apply(_combined_text, axis=1)
    return frame


def load_movie_dataset() -> pd.DataFrame:
    """Load a cleaned dataset if it exists, otherwise build one from source."""

    cleaned_path = PROCESSED_DATA_DIR / "cleaned_movies.csv"
    if cleaned_path.exists():
        try:
            return build_movie_frame(pd.read_csv(cleaned_path))
        except Exception:
            pass

    return build_movie_frame(load_raw_movies())


def save_cleaned_dataset(dataframe: pd.DataFrame, path: Path | None = None) -> Path:
    """Save the cleaned dataset to disk and return the saved path."""

    target_path = path or (PROCESSED_DATA_DIR / "cleaned_movies.csv")
    target_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(target_path, index=False)
    return target_path


def get_available_titles(dataframe: pd.DataFrame) -> list[str]:
    """Return a list of movie titles for UI selection."""

    return sorted(title for title in dataframe["title"].dropna().astype(str).tolist())
