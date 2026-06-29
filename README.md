# Movie Recommendation System

A professional content-based movie recommendation engine built with Python. Uses TF-IDF vectorization and cosine similarity to recommend top 10 similar movies. Features TMDB API integration for posters, fuzzy search, and an interactive Streamlit dashboard with analytics.

---

## ✨ Features

- **Content-Based Recommendations** - TF-IDF Vectorization + Cosine Similarity
- **Top 10 Predictions** - Ranked by similarity score
- **Fuzzy Search** - Intelligent movie name matching
- **Movie Posters** - TMDB API integration with dynamic loading
- **Analytics Dashboard** - Interactive Plotly visualizations
- **Professional UI** - Dark mode with metallic/grey theme
- **Error Handling** - Graceful API & data fallbacks

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-Learn |
| Web Framework | Streamlit |
| Visualizations | Plotly |
| Fuzzy Matching | RapidFuzz |
| API Integration | Requests, python-dotenv |

---

## 📊 Dataset

**Source:** [MovieLens Latest Dataset](https://grouplens.org/datasets/movielens/latest/)
- 9,000+ movies
- 100,000+ user ratings
- Features: Title, Genre, Cast, Overview, Rating

If the MovieLens files are not downloaded yet, the app still runs using a built-in demo dataset so you can test the full UI immediately.

---

## 🚀 Getting Started

### 1. Clone Repository

```bash
git clone https://github.com/Deepesh-Dey/movie-recommendation-system.git
cd movie-recommendation-system
```

### 2. Setup Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your TMDB_API_KEY from https://www.themoviedb.org/settings/api
```

### 5. Download Dataset

- Visit [MovieLens](https://grouplens.org/datasets/movielens/latest/)
- Download the latest dataset
- Extract CSV files to `data/raw/`

### 6. Run Application

```bash
streamlit run app.py
```

Open browser: `http://localhost:8501`

---

## 📁 Project Structure

```
movie-recommendation-system/
│
├── data/
│   ├── raw/              # Original MovieLens CSV
│   └── processed/        # Cleaned & processed data
│
├── src/
│   ├── recommender/      # Core recommendation engine
│   ├── utils/           # Helpers (fuzzy search, TMDB API, config)
│   └── dashboard/       # Analytics dashboard components
│
├── notebooks/           # Jupyter exploration notebooks
├── reports/            # Analysis & documentation
├── assets/             # Screenshots, logos
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
└── README.md           # This file
```

---

## 🔧 Configuration

Edit `.env` file:

```env
TMDB_API_KEY=your_api_key_here
DEBUG=False
MAX_RECOMMENDATIONS=10
FUZZY_THRESHOLD=80
```

**Get TMDB API Key:** https://www.themoviedb.org/settings/api

---

## 📋 Development Roadmap

- [x] Project structure & repository setup
- [ ] Step 1: Data pipeline & preprocessing
- [ ] Step 2: TF-IDF vectorization & recommendation engine
- [ ] Step 3: Fuzzy search implementation
- [ ] Step 4: TMDB API integration
- [ ] Step 5: Analytics dashboard
- [ ] Step 6: Streamlit web application
- [ ] Step 7: UI/UX enhancement
- [ ] Step 8: Deployment configuration
- [ ] Step 9: Final documentation & report

---

## 📚 Resources

- [Scikit-Learn TF-IDF](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- [Streamlit Docs](https://docs.streamlit.io/)
- [Plotly Docs](https://plotly.com/python/)
- [TMDB API](https://developer.themoviedb.org/docs)
- [RapidFuzz](https://rapidfuzz.github.io/RapidFuzz/)
- [MovieLens Dataset](https://grouplens.org/datasets/movielens/latest/)

---

**Author:** Deepesh Dey  
**Status:** In Development 🔨  
**Updated:** June 1, 2026
A content-based Movie Recommendation System built using Python, Scikit-Learn, TF-IDF Vectorization, Cosine Similarity, Streamlit, TMDB API, and Fuzzy Search.
