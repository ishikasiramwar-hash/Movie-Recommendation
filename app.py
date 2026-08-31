import streamlit as st
import pandas as pd
import plotly.express as px

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    /* Dashboard title */
    .dashboard-header {
        background: white;
        padding: 28px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.06);
        margin-bottom: 25px;
        text-align: center;
    }

    .dashboard-header h1 {
        color: #111827;
        font-size: 32px;
        margin-bottom: 8px;
    }

    .dashboard-header p {
        color: #6b7280;
        font-size: 16px;
        margin: 0;
    }

    /* KPI cards */
    .kpi-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        min-height: 130px;
        text-align: center;
    }

    .kpi-icon {
        font-size: 25px;
        margin-bottom: 8px;
    }

    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 28px;
        font-weight: 700;
        color: #111827;
        margin-top: 8px;
    }

    /* Section headings */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #111827;
        margin-top: 25px;
        margin-bottom: 15px;
    }

    /* Info box */
    .info-box {
        background: white;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e5e7eb;
        margin-top: 15px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    # Change this filename if your CSV has another name
    file_names = [
        "movies.csv",
        "movie.csv",
        "Movie.csv",
        "movies_metadata.csv"
    ]

    for file in file_names:
        try:
            df = pd.read_csv(file)
            return df
        except:
            pass

    return pd.DataFrame()


df = load_data()


# ============================================================
# IF NO DATASET FOUND
# ============================================================

if df.empty:

    st.markdown("""
    <div class="dashboard-header">
        <h1>🎬 MOVIE ANALYTICS DASHBOARD</h1>
        <p>Explore Movie Trends, Revenue, Budget, Genres & Performance</p>
    </div>
    """, unsafe_allow_html=True)

    st.warning("⚠️ Movie dataset was not found.")

    uploaded_file = st.file_uploader(
        "Upload your movie CSV file",
        type=["csv"]
    )

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
    else:
        st.info(
            "Please upload your CSV file or place movies.csv "
            "in the same folder as app.py."
        )
        st.stop()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# ============================================================
# FIND COLUMNS AUTOMATICALLY
# ============================================================

def find_column(possible_names):

    for name in possible_names:
        if name in df.columns:
            return name

    return None


title_col = find_column([
    "title",
    "movie_title",
    "name",
    "original_title"
])

genre_col = find_column([
    "genre",
    "genres",
    "category"
])

release_col = find_column([
    "release_year",
    "year",
    "release_date",
    "released"
])

budget_col = find_column([
    "budget",
    "production_budget"
])

revenue_col = find_column([
    "revenue",
    "box_office",
    "gross",
    "worldwide_gross"
])

rating_col = find_column([
    "rating",
    "imdb_rating",
    "vote_average",
    "score"
])

director_col = find_column([
    "director",
    "director_name"
])

music_col = find_column([
    "music_director",
    "musicdirector",
    "composer",
    "music_composer"
])

franchise_col = find_column([
    "franchise",
    "collection",
    "series"
])

remake_col = find_column([
    "remake",
    "is_remake"
])


# ============================================================
# DATA PREPROCESSING
# ============================================================

# Numeric columns
for col in [budget_col, revenue_col, rating_col]:
    if col:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )


# Release year
if release_col:

    if df[release_col].dtype == "object":

        if "date" in release_col:
            df["release_year_clean"] = pd.to_datetime(
                df[release_col],
                errors="coerce"
            ).dt.year
        else:
            df["release_year_clean"] = pd.to_numeric(
                df[release_col],
                errors="coerce"
            )

    else:
        df["release_year_clean"] = pd.to_numeric(
            df[release_col],
            errors="coerce"
        )

else:
    df["release_year_clean"] = None


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown("""
<h2>🎬 MOVIE FILTERS</h2>
""", unsafe_allow_html=True)

filtered_df = df.copy()


# ---------------- Genre ----------------

if genre_col:

    genres = (
        filtered_df[genre_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    genres = sorted(genres)

    selected_genre = st.sidebar.selectbox(
        "🎭 Genre",
        ["All Genres"] + genres
    )

    if selected_genre != "All Genres":
        filtered_df = filtered_df[
            filtered_df[genre_col].astype(str) == selected_genre
        ]


# ---------------- Release Period ----------------

if "release_year_clean" in filtered_df.columns:

    years = pd.to_numeric(
        filtered_df["release_year_clean"],
        errors="coerce"
    ).dropna()

    if not years.empty:

        min_year = int(years.min())
        max_year = int(years.max())

        if min_year < max_year:

            selected_years = st.sidebar.slider(
                "📅 Release Period",
                min_value=min_year,
                max_value=max_year,
                value=(min_year, max_year)
            )

            filtered_df = filtered_df[
                (filtered_df["release_year_clean"] >= selected_years[0]) &
                (filtered_df["release_year_clean"] <= selected_years[1])
            ]


# ---------------- Remake ----------------

if remake_col:

    remake_values = (
        df[remake_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(remake_values) > 0:

        selected_remake = st.sidebar.selectbox(
            "🔄 Remake",
            ["All"] + sorted(remake_values)
        )

        if selected_remake != "All":

            filtered_df = filtered_df[
                filtered_df[remake_col].astype(str) == selected_remake
            ]


# ---------------- Franchise ----------------

if franchise_col:

    franchise_values = (
        df[franchise_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(franchise_values) > 0:

        selected_franchise = st.sidebar.selectbox(
            "🎞️ Franchise",
            ["All"] + sorted(franchise_values)
        )

        if selected_franchise != "All":

            filtered_df = filtered_df[
                filtered_df[franchise_col].astype(str)
                == selected_franchise
            ]


# ---------------- Director ----------------

if director_col:

    directors = (
        df[director_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(directors) > 0:

        selected_director = st.sidebar.selectbox(
            "🎥 Director",
            ["All Directors"] + sorted(directors)
        )

        if selected_director != "All Directors":

            filtered_df = filtered_df[
                filtered_df[director_col].astype(str)
                == selected_director
            ]


# ---------------- Music Director ----------------

if music_col:

    music_directors = (
        df[music_col]
        .dropna()
        .astype(str)
        .unique()
        .tolist()
    )

    if len(music_directors) > 0:

        selected_music = st.sidebar.selectbox(
            "🎵 Music Director",
            ["All Music Directors"] + sorted(music_directors)
        )

        if selected_music != "All Music Directors":

            filtered_df = filtered_df[
                filtered_df[music_col].astype(str)
                == selected_music
            ]


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="dashboard-header">
    <h1>🎬 MOVIE ANALYTICS DASHBOARD</h1>
    <p>Explore Movie Trends, Revenue, Budget, Genres & Performance</p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">📌 Overview</div>',
    unsafe_allow_html=True
)


# KPI calculations

total_movies = len(filtered_df)

if revenue_col:
    total_revenue = filtered_df[revenue_col].sum()
else:
    total_revenue = 0

if budget_col:
    total_budget = filtered_df[budget_col].sum()
else:
    total_budget = 0


# Screens count
total_screens = 0

for col in ["screens", "screen_count", "number_of_screens"]:

    if col in filtered_df.columns:

        total_screens = pd.to_numeric(
            filtered_df[col],
            errors="coerce"
        ).sum()

        break


# If no screen column, show N/A
if total_screens == 0:
    screen_display = "N/A"
else:
    screen_display = f"{int(total_screens):,}"


# Revenue display
if total_revenue >= 10000000:
    revenue_display = f"₹{total_revenue / 10000000:.1f} Cr"
elif total_revenue >= 100000:
    revenue_display = f"₹{total_revenue / 100000:.1f} L"
else:
    revenue_display = f"₹{total_revenue:,.0f}"


# Budget display
if total_budget >= 10000000:
    budget_display = f"₹{total_budget / 10000000:.1f} Cr"
elif total_budget >= 100000:
    budget_display = f"₹{total_budget / 100000:.1f} L"
else:
    budget_display = f"₹{total_budget:,.0f}"


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">🎬</div>

        <div class="kpi-title">
            TOTAL MOVIES
        </div>

        <div class="kpi-value">
            {total_movies:,}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col2:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">💰</div>

        <div class="kpi-title">
            TOTAL REVENUE
        </div>

        <div class="kpi-value">
            {revenue_display}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col3:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">💵</div>

        <div class="kpi-title">
            TOTAL BUDGET
        </div>

        <div class="kpi-value">
            {budget_display}
        </div>

    </div>
    """, unsafe_allow_html=True)


with col4:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">🏢</div>

        <div class="kpi-title">
            TOTAL SCREENS
        </div>

        <div class="kpi-value">
            {screen_display}
        </div>

    </div>
    """, unsafe_allow_html=True)


# ============================================================
# CHART 1 — MOVIES BY GENRE
# ============================================================

if genre_col:

    st.markdown(
        '<div class="section-title">🎭 Movies by Genre</div>',
        unsafe_allow_html=True
    )

    genre_data = (
        filtered_df[genre_col]
        .dropna()
        .astype(str)
        .value_counts()
        .reset_index()
    )

    genre_data.columns = ["Genre", "Movies"]

    if not genre_data.empty:

        fig_genre = px.bar(
            genre_data.head(15),
            x="Genre",
            y="Movies",
            title="Number of Movies by Genre",
            text="Movies"
        )

        fig_genre.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Genre",
            yaxis_title="Number of Movies"
        )

        st.plotly_chart(
            fig_genre,
            use_container_width=True
        )


# ============================================================
# CHART 2 — MOVIES BY RELEASE PERIOD
# ============================================================

if "release_year_clean" in filtered_df.columns:

    release_data = filtered_df.dropna(
        subset=["release_year_clean"]
    )

    if not release_data.empty:

        release_data = (
            release_data
            .groupby("release_year_clean")
            .size()
            .reset_index(name="Movies")
        )

        st.markdown(
            '<div class="section-title">📅 Movies by Release Period</div>',
            unsafe_allow_html=True
        )

        fig_release = px.line(
            release_data,
            x="release_year_clean",
            y="Movies",
            markers=True,
            title="Movie Releases Over Time"
        )

        fig_release.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Release Year",
            yaxis_title="Number of Movies"
        )

        st.plotly_chart(
            fig_release,
            use_container_width=True
        )


# ============================================================
# REVENUE VS BUDGET
# ============================================================

if budget_col and revenue_col:

    st.markdown(
        '<div class="section-title">💰 Revenue vs Budget</div>',
        unsafe_allow_html=True
    )

    scatter_df = filtered_df[
        [budget_col, revenue_col]
    ].dropna()

    if not scatter_df.empty:

        fig_scatter = px.scatter(
            scatter_df,
            x=budget_col,
            y=revenue_col,
            title="Budget vs Revenue",
            opacity=0.65
        )

        fig_scatter.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white",
            xaxis_title="Budget",
            yaxis_title="Revenue"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )


# ============================================================
# TOP MOVIES BY REVENUE
# ============================================================

if revenue_col:

    st.markdown(
        '<div class="section-title">🏆 Top Movies by Revenue</div>',
        unsafe_allow_html=True
    )

    top_movies = filtered_df.dropna(
        subset=[revenue_col]
    ).copy()

    if not top_movies.empty:

        top_movies = top_movies.sort_values(
            revenue_col,
            ascending=False
        ).head(10)

        if title_col:

            top_chart = px.bar(
                top_movies,
                x=revenue_col,
                y=title_col,
                orientation="h",
                title="Top 10 Movies by Revenue",
                text=revenue_col
            )

            top_chart.update_layout(
                plot_bgcolor="white",
                paper_bgcolor="white",
                yaxis_title="Movie",
                xaxis_title="Revenue"
            )

            st.plotly_chart(
                top_chart,
                use_container_width=True
            )


# ============================================================
# RATINGS ANALYSIS
# ============================================================

if rating_col:

    st.markdown(
        '<div class="section-title">⭐ Movie Ratings</div>',
        unsafe_allow_html=True
    )

    rating_data = filtered_df[rating_col].dropna()

    if not rating_data.empty:

        col1, col2 = st.columns(2)

        with col1:

            avg_rating = rating_data.mean()

            st.metric(
                "Average Rating",
                f"{avg_rating:.2f}"
            )

        with col2:

            max_rating = rating_data.max()

            st.metric(
                "Highest Rating",
                f"{max_rating:.2f}"
            )


# ============================================================
# TOP DIRECTORS
# ============================================================

if director_col:

    st.markdown(
        '<div class="section-title">🎥 Top Directors</div>',
        unsafe_allow_html=True
    )

    director_data = (
        filtered_df[director_col]
        .dropna()
        .astype(str)
        .value_counts()
        .head(10)
        .reset_index()
    )

    director_data.columns = [
        "Director",
        "Movies"
    ]

    if not director_data.empty:

        fig_director = px.bar(
            director_data,
            x="Movies",
            y="Director",
            orientation="h",
            title="Top 10 Directors by Number of Movies",
            text="Movies"
        )

        fig_director.update_layout(
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(
            fig_director,
            use_container_width=True
        )


# ============================================================
# MOVIE DATA TABLE
# ============================================================

st.markdown(
    '<div class="section-title">📋 Movie Details</div>',
    unsafe_allow_html=True
)

display_df = filtered_df.copy()

# Limit columns for clean display
preferred_columns = []

for col in [
    title_col,
    genre_col,
    release_col,
    budget_col,
    revenue_col,
    rating_col,
    director_col
]:

    if col and col in display_df.columns:
        preferred_columns.append(col)


if preferred_columns:

    display_df = display_df[
        preferred_columns
    ]


st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<br>

<div style="
    text-align:center;
    padding:20px;
    color:#6b7280;
    font-size:14px;
">

🎬 Movie Analytics Dashboard  
<br>
Built with Python • Pandas • Plotly • Streamlit

</div>

""", unsafe_allow_html=True)
