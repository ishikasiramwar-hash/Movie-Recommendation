import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# =========================================================
# PAGE SETTINGS
# =========================================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS / UI DESIGN
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #eeeeee;
}

/* ---------- TITLE ---------- */

.dashboard-title {
    background: linear-gradient(
        90deg,
        #bdbdbd,
        #eeeeee,
        #bdbdbd
    );
    border-radius: 18px;
    padding: 18px;
    text-align: center;
    font-size: 32px;
    font-weight: 800;
    color: #111111;
    box-shadow: 0px 5px 12px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

/* ---------- KPI CARD ---------- */

.kpi-card {
    background-color: white;
    border-radius: 18px;
    padding: 18px 10px;
    text-align: center;
    box-shadow: 0px 5px 12px rgba(0,0,0,0.18);
    min-height: 115px;
    border: 1px solid #eeeeee;
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

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background-color: #dddddd;
}

.sidebar-title {
    background-color: white;
    padding: 14px;
    border-radius: 14px;
    text-align: center;
    font-size: 21px;
    font-weight: 800;
    margin-bottom: 18px;
}

/* ---------- CHART CONTAINER ---------- */

.chart-title {
    background-color: white;
    padding: 8px;
    border-radius: 8px;
    font-weight: bold;
}

/* ---------- RECOMMENDATION ---------- */

.recommendation-box {
    background-color: white;
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
}

/* ---------- FOOTER ---------- */

.footer {
    text-align: center;
    color: #555555;
    padding: 15px;
}

/* Hide Streamlit branding */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD CSV
# =========================================================

@st.cache_data
def load_data():

    try:

        data = pd.read_csv(
            "Data for repository.csv"
        )

        return data

    except FileNotFoundError:

        st.error(
            "❌ Data file not found."
        )

        st.info(
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
    .str.replace(" ", "_", regex=False)
)


# =========================================================
# FIND COLUMN FUNCTION
# =========================================================

def find_column(names):

    for name in names:

        if name in df.columns:
            return name

    return None


# =========================================================
# FIND DATASET COLUMNS
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
    "imdb",
    "user_rating"
])

budget_col = find_column([
    "budget",
    "budget_inr",
    "budget_in_$",
    "budget_in_rs",
    "budget_(inr)",
    "budget_in_(inr)"
])

revenue_col = find_column([
    "revenue",
    "revenue_inr",
    "revenue_in_$",
    "box_office",
    "box_office_revenue",
    "total_revenue"
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
    "whether_franchise",
    "is_franchise"
])

remake_col = find_column([
    "remake",
    "whether_remake",
    "is_remake"
])


# =========================================================
# FALLBACK COLUMNS
# =========================================================

if movie_col is None:

    df["movie_name"] = [
        "Movie " + str(i + 1)
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
# NUMBER CLEANING FUNCTION
# =========================================================

def clean_number(value):

    if pd.isna(value):
        return 0.0

    value = str(value).strip().lower()

    # Remove currency symbols
    value = (
        value
        .replace("₹", "")
        .replace("$", "")
        .replace("rs.", "")
        .replace("rs", "")
        .replace(",", "")
    )

    multiplier = 1

    # Billion
    if "bn" in value or "billion" in value:

        multiplier = 1000

        value = (
            value
            .replace("bn", "")
            .replace("billion", "")
        )

    # Crore
    elif "cr" in value or "crore" in value:

        multiplier = 1

        value = (
            value
            .replace("cr", "")
            .replace("crore", "")
        )

    # Million
    elif "m" in value:

        multiplier = 1

        value = value.replace("m", "")

    # Thousand
    elif "k" in value:

        multiplier = 0.001

        value = value.replace("k", "")

    try:

        number = float(value)

        return number * multiplier

    except:

        return 0.0


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================

df[rating_col] = pd.to_numeric(
    df[rating_col],
    errors="coerce"
).fillna(0)


df[budget_col] = df[budget_col].apply(
    clean_number
)


df[revenue_col] = df[revenue_col].apply(
    clean_number
)


# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<div class="dashboard-title">'
    '🎬 🍿 MOVIE ANALYTICS DASHBOARD 🍿 🎬'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown(
    '<div class="sidebar-title">'
    '🎬 MOVIE FILTERS'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# GENRE FILTER
# =========================================================

genre_list = sorted(
    df[genre_col]
    .dropna()
    .astype(str)
    .unique()
)


selected_genre = st.sidebar.multiselect(
    "Genre",
    genre_list
)


# =========================================================
# RATING FILTER
# =========================================================

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


# =========================================================
# MUSIC DIRECTOR FILTER
# =========================================================

music_list = sorted(
    df[music_col]
    .dropna()
    .astype(str)
    .unique()
)


selected_music = st.sidebar.multiselect(
    "Music Director",
    music_list
)


# =========================================================
# RELEASE PERIOD FILTER
# =========================================================

release_list = sorted(
    df[release_col]
    .dropna()
    .astype(str)
    .unique()
)


selected_release = st.sidebar.multiselect(
    "Release Period",
    release_list
)


# =========================================================
# DIRECTOR FILTER
# =========================================================

director_list = sorted(
    df[director_col]
    .dropna()
    .astype(str)
    .unique()
)


selected_director = st.sidebar.multiselect(
    "Director",
    director_list
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_genre:

    filtered_df = filtered_df[
        filtered_df[genre_col]
        .astype(str)
        .isin(selected_genre)
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
# KPI CALCULATIONS
# =========================================================

total_movies = len(filtered_df)


if len(filtered_df) > 0:

    average_rating = (
        filtered_df[rating_col].mean()
    )

    total_budget = (
        filtered_df[budget_col].sum()
    )

    total_revenue = (
        filtered_df[revenue_col].sum()
    )

else:

    average_rating = 0

    total_budget = 0

    total_revenue = 0


# =========================================================
# KPI CARDS
# =========================================================

k1, k2, k3, k4 = st.columns(4)


with k1:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Total Movies</div>'
        f'<div class="kpi-value">{total_movies:,}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k2:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Average Rating</div>'
        f'<div class="kpi-value">{average_rating:.2f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k3:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Total Budget</div>'
        f'<div class="kpi-value">₹{total_budget:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with k4:

    st.markdown(
        f'<div class="kpi-card">'
        f'<div class="kpi-title">Total Revenue</div>'
        f'<div class="kpi-value">₹{total_revenue:,.0f}</div>'
        f'</div>',
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# ROW 1
# =========================================================

c1, c2, c3, c4 = st.columns(4)


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
        hole=0.45,
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
    )

    rating_data.columns = [
        "Genre",
        "Average Rating"
    ]

    rating_data = rating_data.sort_values(
        "Average Rating",
        ascending=False
    )

    fig = px.bar(
        rating_data,
        x="Genre",
        y="Average Rating",
        title="Movies By Rating",
        text_auto=".2f"
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

    budget_revenue = budget_revenue[
        (budget_revenue[budget_col] > 0) |
        (budget_revenue[revenue_col] > 0)
    ]

    if len(budget_revenue) > 0:

        fig = px.scatter(
            budget_revenue,
            x=budget_col,
            y=revenue_col,
            size=revenue_col,
            hover_name=movie_col,
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

    else:

        st.info(
            "Budget and Revenue data not available."
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
# MOVIE RECOMMENDATION
# =========================================================

st.markdown("---")

st.markdown(
    '<div class="dashboard-title">'
    '🍿 MOVIE RECOMMENDATION'
    '</div>',
    unsafe_allow_html=True
)


if len(filtered_df) > 0:

    rec1, rec2 = st.columns([1, 2])


    # -----------------------------------------------------
    # MOVIE SELECTION
    # -----------------------------------------------------

    with rec1:

        movie_options = sorted(
            filtered_df[movie_col]
            .astype(str)
            .unique()
        )

        selected_movie = st.selectbox(
            "Select a Movie",
            movie_options
        )


    # -----------------------------------------------------
    # RECOMMENDATIONS
    # -----------------------------------------------------

    with rec2:

        selected_rows = filtered_df[
            filtered_df[movie_col]
            .astype(str)
            == selected_movie
        ]


        if len(selected_rows) > 0:

            selected_row = selected_rows.iloc[0]

            selected_genre_value = str(
                selected_row[genre_col]
            )

            selected_rating_value = float(
                selected_row[rating_col]
            )


            recommendations = filtered_df[
                (
                    filtered_df[genre_col]
                    .astype(str)
                    == selected_genre_value
                )
                &
                (
                    filtered_df[movie_col]
                    .astype(str)
                    != selected_movie
                )
            ].copy()


            if len(recommendations) > 0:

                recommendations[
                    "Rating Difference"
                ] = abs(
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
                    '<div class="recommendation-box">'
                    '<h3>🎬 Recommended Movies</h3>'
                    f'<p>Based on genre: '
                    f'<b>{selected_genre_value}</b></p>'
                    f'<p>Selected movie: '
                    f'<b>{selected_movie}</b></p>'
                    '</div>',
                    unsafe_allow_html=True
                )


                st.write("")


                for _, row in recommendations.iterrows():

                    st.write(
                        "🎥 "
                        + str(row[movie_col])
                        + " — Rating: "
                        + str(
                            round(
                                float(
                                    row[rating_col]
                                ),
                                2
                            )
                        )
                    )

            else:

                st.info(
                    "No similar movies found."
                )


# =========================================================
# DATASET VIEW
# =========================================================

st.markdown("---")

with st.expander("📊 View Dataset"):

    st.write(
        "Total records:",
        len(filtered_df)
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer">'
    '🎬 Movie Analytics Dashboard '
    '| Built with Streamlit + Plotly'
    '</div>',
    unsafe_allow_html=True
)
