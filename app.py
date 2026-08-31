import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #eeeeee;
}

/* Main title */
.dashboard-title {
    background: linear-gradient(
        90deg,
        #bdbdbd,
        #f5f5f5,
        #bdbdbd
    );

    border-radius: 18px;
    padding: 18px;
    text-align: center;

    font-size: 34px;
    font-weight: 800;

    color: #111111;

    box-shadow:
        0px 5px 12px rgba(0,0,0,0.25);

    margin-bottom: 20px;
}

/* KPI Cards */

.kpi-card {
    background: white;

    border-radius: 18px;

    padding: 18px;

    text-align: center;

    box-shadow:
        0px 5px 12px rgba(0,0,0,0.18);

    min-height: 110px;
}

.kpi-title {
    font-size: 16px;
    color: #555555;
    font-weight: 600;
}

.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #111111;

    margin-top: 10px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background-color: #dddddd;
}

/* Sidebar heading */

.sidebar-title {
    background: #ffffff;

    padding: 12px;

    border-radius: 12px;

    text-align: center;

    font-weight: bold;

    font-size: 20px;

    margin-bottom: 15px;
}

/* Recommendation card */

.recommendation-card {

    background: white;

    padding: 20px;

    border-radius: 15px;

    box-shadow:
        0px 4px 12px rgba(0,0,0,0.15);

    margin-top: 10px;

}

/* Hide Streamlit elements */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATASET
# =========================================================

@st.cache_data
def load_data():

    try:

        df = pd.read_csv(
            "Data for repository.csv"
        )

        return df

    except FileNotFoundError:

        st.error(
            "❌ Data file not found. "
            "Make sure 'Data for repository.csv' "
            "is in the same GitHub folder as app.py."
        )

        st.stop()


df = load_data()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)


# =========================================================
# FUNCTION TO FIND COLUMN
# =========================================================

def find_column(possible_names):

    for name in possible_names:

        if name in df.columns:
            return name

    return None


# =========================================================
# IDENTIFY IMPORTANT COLUMNS
# =========================================================

movie_col = find_column([
    "movie_name",
    "movie_title",
    "title",
    "movie",
    "name"
])

genre_col = find_column([
    "genre",
    "genres",
    "category"
])

rating_col = find_column([
    "rating",
    "ratings",
    "imdb_rating",
    "user_rating"
])

budget_col = find_column([
    "budget",
    "budget_inr",
    "budget_in_$",
    "budget_inr_"
])

revenue_col = find_column([
    "revenue",
    "revenue_inr",
    "box_office",
    "box_office_revenue"
])

director_col = find_column([
    "director",
    "director_name"
])

music_col = find_column([
    "music_director",
    "music_director_name",
    "music"
])

release_col = find_column([
    "release_period",
    "release_type",
    "period"
])

franchise_col = find_column([
    "franchise",
    "whether_franchise"
])

remake_col = find_column([
    "remake",
    "whether_remake",
    "is_remake"
])


# =========================================================
# CREATE FALLBACK COLUMNS
# =========================================================

if movie_col is None:

    df["movie_name"] = [
        f"Movie {i+1}"
        for i in range(len(df))
    ]

    movie_col = "movie_name"


if genre_col is None:

    df["genre"] = "Unknown"

    genre_col = "genre"


if rating_col is None:

    df["rating"] = 3.5

    rating_col = "rating"


if budget_col is None:

    df["budget"] = 0

    budget_col = "budget"


if revenue_col is None:

    df["revenue"] = 0

    revenue_col = "revenue"


if director_col is None:

    df["director"] = "Unknown"

    director_col = "director"


if music_col is None:

    df["music_director"] = "Unknown"

    music_col = "music_director"


if release_col is None:

    df["release_period"] = "Normal"

    release_col = "release_period"


if franchise_col is None:

    df["franchise"] = "No"

    franchise_col = "franchise"


if remake_col is None:

    df["remake"] = "No"

    remake_col = "remake"


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================

df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
)

df[budget_col] = pd.to_numeric(
    df[budget_col],
    errors="coerce"
)

df[revenue_col] = pd.to_numeric(
    df[revenue_col],
    errors="coerce"
)


# Remove invalid rows

df = df.dropna(
    subset=[rating_col]
)

df[rating_col] = df[rating_col].fillna(0)

df[budget_col] = df[budget_col].fillna(0)

df[revenue_col] = df[revenue_col].fillna(0)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    """
    <div class="sidebar-title">
        🎬 MOVIE FILTERS
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Genre Filter
# ---------------------------------------------------------

genre_values = sorted(
    df[genre_col]
    .dropna()
    .astype(str)
    .unique()
)

selected_genres = st.sidebar.multiselect(
    "Genre",
    genre_values
)


# ---------------------------------------------------------
# Rating Filter
# ---------------------------------------------------------

min_rating = float(
    df[rating_col].min()
)

max_rating = float(
    df[rating_col].max()
)

if min_rating == max_rating:

    max_rating = min_rating + 1


selected_rating = st.sidebar.slider(
    "Rating",
    min_value=min_rating,
    max_value=max_rating,
    value=(min_rating, max_rating),
    step=0.1
)


# ---------------------------------------------------------
# Music Director
# ---------------------------------------------------------

music_values = sorted(
    df[music_col]
    .dropna()
    .astype(str)
    .unique()
)

selected_music = st.sidebar.multiselect(
    "Music Director",
    music_values
)


# ---------------------------------------------------------
# Release Period
# ---------------------------------------------------------

release_values = sorted(
    df[release_col]
    .dropna()
    .astype(str)
    .unique()
)

selected_release = st.sidebar.multiselect(
    "Release Period",
    release_values
)


# ---------------------------------------------------------
# Director
# ---------------------------------------------------------

director_values = sorted(
    df[director_col]
    .dropna()
    .astype(str)
    .unique()
)

selected_director = st.sidebar.multiselect(
    "Director",
    director_values
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_genres:

    filtered_df = filtered_df[
        filtered_df[genre_col]
        .astype(str)
        .isin(selected_genres)
    ]


filtered_df = filtered_df[
    (filtered_df[rating_col] >= selected_rating[0]) &
    (filtered_df[rating_col] <= selected_rating[1])
]


if selected_music:

    filtered_df = filtered_df[
        filtered_df[music_col]
        .astype(str)
        .isin(selected_music)
    ]


if selected_release:

    filtered_df = filtered_df[
        filtered_df[release_col]
        .astype(str)
        .isin(selected_release)
    ]


if selected_director:

    filtered_df = filtered_df[
        filtered_df[director_col]
        .astype(str)
        .isin(selected_director)
    ]


# =========================================================
# TITLE
# =========================================================

st.markdown(
    """
    <div class="dashboard-title">
        🎬 🍿 MOVIE ANALYTICS DASHBOARD 🍿 🎬
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# KPI CALCULATIONS
# =========================================================

total_movies = len(filtered_df)


if len(filtered_df) > 0:

    average_rating = filtered_df[rating_col].mean()

    total_budget = filtered_df[budget_col].sum()

    total_revenue = filtered_df[revenue_col].sum()

else:

    average_rating = 0

    total_budget = 0

    total_revenue = 0


# =========================================================
# KPI CARDS
# =========================================================

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                Total Movies
            </div>

            <div class="kpi-value">
                {total_movies:,}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                Average Rating
            </div>

            <div class="kpi-value">
                {average_rating:.2f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                Total Budget
            </div>

            <div class="kpi-value">
                ₹{total_budget:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with col4:

    st.markdown(
        f"""
        <div class="kpi-card">

            <div class="kpi-title">
                Total Revenue
            </div>

            <div class="kpi-value">
                ₹{total_revenue:,.0f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# ROW 1
# =========================================================

c1, c2, c3, c4 = st.columns(
    [1.2, 1.5, 1.3, 1.2]
)


# =========================================================
# REVENUE BY FRANCHISE
# =========================================================

with c1:

    franchise_data = (
        filtered_df[franchise_col]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    franchise_data.columns = [
        "Franchise",
        "Count"
    ]

    fig = px.pie(
        franchise_data,
        names="Franchise",
        values="Count",
        hole=0.4,
        title="Revenue By Franchise"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MOVIES BY GENRE
# =========================================================

with c2:

    genre_data = (
        filtered_df[genre_col]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    genre_data.columns = [
        "Genre",
        "Count"
    ]

    fig = px.pie(
        genre_data,
        names="Genre",
        values="Count",
        hole=0.45,
        title="Movies By Genre"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MOVIES BY RATING
# =========================================================

with c3:

    rating_data = (
        filtered_df
        .groupby(genre_col)[rating_col]
        .mean()
        .reset_index()
        .sort_values(
            rating_col,
            ascending=False
        )
    )

    rating_data[genre_col] = (
        rating_data[genre_col]
        .astype(str)
    )

    fig = px.bar(
        rating_data,
        x=genre_col,
        y=rating_col,
        title="Movies By Rating",
        text_auto=".2f"
    )

    fig.update_layout(
        height=320,
        xaxis_title="Genre",
        yaxis_title="Average Rating",
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# BUDGET VS REVENUE
# =========================================================

with c4:

    budget_revenue = (
        filtered_df
        .groupby(movie_col)[
            [budget_col, revenue_col]
        ]
        .mean()
        .reset_index()
    )

    fig = px.scatter(
        budget_revenue,
        x=budget_col,
        y=revenue_col,
        hover_name=movie_col,
        size=revenue_col,
        title="Budget Vs Revenue"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ROW 2
# =========================================================

c5, c6, c7, c8 = st.columns(4)


# =========================================================
# MOVIES BY RELEASE PERIOD
# =========================================================

with c5:

    period_data = (
        filtered_df[release_col]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    period_data.columns = [
        "Release Period",
        "Count"
    ]

    fig = px.bar(
        period_data,
        x="Release Period",
        y="Count",
        title="Movies By Released Period",
        text="Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TOP 5 MOVIES BY REVENUE
# =========================================================

with c6:

    top_revenue = (
        filtered_df
        .groupby(movie_col)[revenue_col]
        .sum()
        .nlargest(5)
        .reset_index()
    )

    fig = px.bar(
        top_revenue,
        x=movie_col,
        y=revenue_col,
        title="Top 5 Movies By Revenue",
        text_auto=".2s"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# ORIGINAL VS REMAKE
# =========================================================

with c7:

    remake_data = (
        filtered_df[remake_col]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    remake_data.columns = [
        "Remake",
        "Count"
    ]

    fig = px.bar(
        remake_data,
        x="Remake",
        y="Count",
        title="Original Vs Remake Movies",
        text="Count"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# TOP 5 MOVIES BY BUDGET
# =========================================================

with c8:

    top_budget = (
        filtered_df
        .groupby(movie_col)[budget_col]
        .sum()
        .nlargest(5)
        .reset_index()
    )

    fig = px.bar(
        top_budget,
        x=budget_col,
        y=movie_col,
        orientation="h",
        title="Top 5 Movies By Budget",
        text_auto=".2s"
    )

    fig.update_layout(
        height=320,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# MOVIE RECOMMENDATION SECTION
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div class="dashboard-title">
        🍿 Movie Recommendation
    </div>
    """,
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    recommendation_col1, recommendation_col2 = st.columns(
        [1, 2]
    )


    # -----------------------------------------------------
    # SELECT MOVIE
    # -----------------------------------------------------

    with recommendation_col1:

        movie_list = sorted(
            filtered_df[movie_col]
            .astype(str)
            .unique()
        )

        selected_movie = st.selectbox(
            "Select a Movie",
            movie_list
        )


    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    with recommendation_col2:

        selected_row = filtered_df[
            filtered_df[movie_col]
            .astype(str)
            == selected_movie
        ]

        if len(selected_row) > 0:

            selected_genre = str(
                selected_row.iloc[0][genre_col]
            )

            selected_rating_value = float(
                selected_row.iloc[0][rating_col]
            )

            selected_director = str(
                selected_row.iloc[0][director_col]
            )


            recommendations = filtered_df[
                (
                    filtered_df[genre_col]
                    .astype(str)
                    == selected_genre
                )
                &
                (
                    filtered_df[movie_col]
                    .astype(str)
                    != selected_movie
                )
            ].copy()


            if len(recommendations) > 0:

                recommendations["Rating Difference"] = abs(
                    recommendations[rating_col]
                    - selected_rating_value
                )

                recommendations = (
                    recommendations
                    .sort_values(
                        "Rating Difference"
                    )
                    .head(5)
                )


                st.markdown(
                    f"""
                    <div class="recommendation-card">

                    <h3>
                    🎬 Recommended Movies
                    </h3>

                    <p>
                    Based on the genre:
                    <b>{selected_genre}</b>
                    </p>

                    <p>
                    Selected movie:
                    <b>{selected_movie}</b>
                    </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                for i, row in recommendations.iterrows():

                    st.write(
                        "🎥 "
                        + str(row[movie_col])
                        + " — Rating: "
                        + str(round(
                            float(row[rating_col]),
                            2
                        ))
                    )

            else:

                st.info(
                    "No similar movies found."
                )


# =========================================================
# DATASET INFORMATION
# =========================================================

st.markdown("---")

with st.expander("📊 View Dataset"):

    st.write(
        "Number of records:",
        len(filtered_df)
    )

    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="
        text-align:center;
        color:#555555;
        padding:10px;
    ">

    🎬 Movie Analytics Dashboard

    <br>

    Built with ❤️ using Streamlit + Plotly

    </div>
    """,
    unsafe_allow_html=True
)
