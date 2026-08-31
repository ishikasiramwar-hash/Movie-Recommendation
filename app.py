import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.set_page_config(
    page_title="Movie Analytics",
    page_icon="🎬",
    layout="wide"
)

# --------------------------------------------------
# CLEAN CSS
# --------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #f7f7f7;
}

.main {
    background-color: #f7f7f7;
}

.dashboard-title {
    background: #1f1f2e;
    padding: 25px;
    border-radius: 15px;
    text-align: center;
    margin-bottom: 25px;
}

.dashboard-title h1 {
    color: white;
    margin: 0;
    font-size: 34px;
}

.dashboard-title p {
    color: #cccccc;
    margin: 8px 0 0 0;
    font-size: 15px;
}

/* KPI */

.kpi {
    background: white;
    padding: 20px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
}

.kpi-title {
    font-size: 14px;
    color: #777777;
}

.kpi-value {
    font-size: 28px;
    font-weight: bold;
    color: #222222;
    margin-top: 8px;
}

/* Section */

.section {
    background: white;
    padding: 18px;
    border-radius: 14px;
    margin-top: 20px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.06);
}

.section-title {
    font-size: 20px;
    font-weight: bold;
    color: #222222;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    try:
        return pd.read_csv("movies.csv")

    except:

        try:
            return pd.read_excel("movies.xlsx")

        except:

            return pd.DataFrame()


df = load_data()


if df.empty:

    st.error(
        "Movie dataset not found. "
        "Place movies.csv or movies.xlsx in the same folder."
    )

    st.stop()


# --------------------------------------------------
# CLEAN COLUMN NAMES
# --------------------------------------------------

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# --------------------------------------------------
# FIND COLUMNS
# --------------------------------------------------

def get_column(names):

    for name in names:

        if name in df.columns:
            return name

    return None


title_col = get_column([
    "movie_name",
    "movie",
    "title",
    "movie_title",
    "name"
])

genre_col = get_column([
    "genre",
    "genres"
])

rating_col = get_column([
    "rating",
    "imdb_rating",
    "average_rating"
])

director_col = get_column([
    "director",
    "director_name"
])

music_col = get_column([
    "music_director",
    "music_director_name",
    "music"
])

year_col = get_column([
    "year",
    "release_year",
    "released_year"
])


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.markdown("""
<div class="dashboard-title">

<h1>🎬 MOVIE ANALYTICS</h1>

<p>
Movie Trends • Ratings • Genres • Directors
</p>

</div>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.title("🎞️ FILTERS")

filtered_df = df.copy()


# Genre filter

if genre_col:

    genres = sorted(
        df[genre_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_genre = st.sidebar.multiselect(
        "Genre",
        genres
    )

    if selected_genre:

        filtered_df = filtered_df[
            filtered_df[genre_col]
            .astype(str)
            .isin(selected_genre)
        ]


# Rating filter

if rating_col:

    filtered_df[rating_col] = pd.to_numeric(
        filtered_df[rating_col],
        errors="coerce"
    )

    min_rating = float(
        df[rating_col].min()
    )

    max_rating = float(
        df[rating_col].max()
    )

    rating = st.sidebar.slider(
        "Rating",
        min_rating,
        max_rating,
        (min_rating, max_rating),
        0.1
    )

    filtered_df = filtered_df[
        filtered_df[rating_col].between(
            rating[0],
            rating[1]
        )
    ]


# Director filter

if director_col:

    directors = sorted(
        df[director_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_director = st.sidebar.multiselect(
        "Director",
        directors
    )

    if selected_director:

        filtered_df = filtered_df[
            filtered_df[director_col]
            .astype(str)
            .isin(selected_director)
        ]


# Music Director

if music_col:

    music_directors = sorted(
        df[music_col]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_music = st.sidebar.multiselect(
        "Music Director",
        music_directors
    )

    if selected_music:

        filtered_df = filtered_df[
            filtered_df[music_col]
            .astype(str)
            .isin(selected_music)
        ]


# --------------------------------------------------
# KPI
# --------------------------------------------------

total_movies = len(filtered_df)

if rating_col:

    avg_rating = filtered_df[rating_col].mean()

else:

    avg_rating = 0


if genre_col:

    total_genres = filtered_df[genre_col].nunique()

else:

    total_genres = 0


if director_col:

    total_directors = filtered_df[director_col].nunique()

else:

    total_directors = 0


st.markdown(
    "### 📌 Overview"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-title">
            🎬 TOTAL MOVIES
        </div>

        <div class="kpi-value">
            {total_movies:,}
        </div>

    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-title">
            ⭐ AVERAGE RATING
        </div>

        <div class="kpi-value">
            {avg_rating:.2f}
        </div>

    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-title">
            🎭 GENRES
        </div>

        <div class="kpi-value">
            {total_genres}
        </div>

    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="kpi">

        <div class="kpi-title">
            🎥 DIRECTORS
        </div>

        <div class="kpi-value">
            {total_directors}
        </div>

    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# GENRE + RATING
# --------------------------------------------------

col1, col2 = st.columns(2)


# --------------------------------------------------
# GENRE
# --------------------------------------------------

with col1:

    st.markdown(
        '<div class="section-title">🎭 Movies by Genre</div>',
        unsafe_allow_html=True
    )

    if genre_col:

        genre_data = (
            filtered_df[genre_col]
            .value_counts()
            .head(10)
            .reset_index()
        )

        genre_data.columns = [
            "Genre",
            "Movies"
        ]

        fig = px.bar(
            genre_data,
            x="Movies",
            y="Genre",
            orientation="h"
        )

        fig.update_layout(
            height=400,
            template="simple_white",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            showlegend=False
        )

        fig.update_traces(
            text=genre_data["Movies"],
            textposition="outside"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# RATING
# --------------------------------------------------

with col2:

    st.markdown(
        '<div class="section-title">⭐ Rating Distribution</div>',
        unsafe_allow_html=True
    )

    if rating_col:

        fig = px.histogram(
            filtered_df,
            x=rating_col,
            nbins=10
        )

        fig.update_layout(
            height=400,
            template="simple_white",
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            ),
            xaxis_title="Rating",
            yaxis_title="Movies"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# --------------------------------------------------
# RELEASE TREND
# --------------------------------------------------

if year_col:

    st.markdown(
        '<div class="section-title">📅 Movies Released Over Time</div>',
        unsafe_allow_html=True
    )

    temp = filtered_df.copy()

    temp["release_year"] = pd.to_numeric(
        temp[year_col],
        errors="coerce"
    )

    year_data = (
        temp
        .dropna(subset=["release_year"])
        .groupby("release_year")
        .size()
        .reset_index(name="Movies")
    )

    year_data = year_data.sort_values(
        "release_year"
    )

    fig = px.line(
        year_data,
        x="release_year",
        y="Movies",
        markers=True
    )

    fig.update_layout(
        height=380,
        template="simple_white",
        xaxis_title="Year",
        yaxis_title="Number of Movies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# --------------------------------------------------
# TOP 5 MOVIES
# --------------------------------------------------

if title_col and rating_col:

    st.markdown(
        '<div class="section-title">🏆 Top 5 Rated Movies</div>',
        unsafe_allow_html=True
    )

    top_movies = (
        filtered_df[
            [title_col, rating_col]
        ]
        .dropna()
        .sort_values(
            rating_col,
            ascending=False
        )
        .head(5)
        .reset_index(drop=True)
    )

    top_movies.insert(
        0,
        "Rank",
        ["🥇", "🥈", "🥉", "4", "5"]
    )

    top_movies.columns = [
        "Rank",
        "Movie",
        "Rating"
    ]

    top_movies["Rating"] = top_movies[
        "Rating"
    ].round(2)

    st.dataframe(
        top_movies,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("""
<br>

<div style="
text-align:center;
color:#777;
padding:15px;
">

🎬 Movie Analytics Dashboard
<br>
<small>Interactive Data Analysis</small>

</div>
""", unsafe_allow_html=True)
