import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Movie Analytics Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = Path("Data for repository.csv")

    if not file_path.exists():
        return None

    df = pd.read_csv(file_path)

    df.columns = df.columns.str.strip()

    return df


df = load_data()


# =========================================================
# CHECK FILE
# =========================================================

if df is None:

    st.error("❌ Data file not found.")

    st.info(
        "Please keep 'Data for repository.csv' "
        "in the same folder as app.py."
    )

    st.stop()


# =========================================================
# CLEAN DATA
# =========================================================

text_columns = [
    "Movie Name",
    "Release Period",
    "Whether Remake",
    "Whether Franchise",
    "Genre",
    "New Actor",
    "New Director",
    "New Music Director",
    "Lead Star",
    "Director",
    "Music Director"
]

for col in text_columns:

    if col in df.columns:

        df[col] = (
            df[col]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


numeric_columns = [
    "Number of Screens",
    "Revenue(INR)",
    "Budget(INR)"
]

for col in numeric_columns:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        ).fillna(0)


# =========================================================
# TITLE
# =========================================================

st.title("🎬 Movie Analytics Dashboard")

st.caption(
    "Explore movie trends, revenue, budget, genres and performance"
)

st.divider()


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🎞️ Movie Filters")

st.sidebar.divider()


# Genre Filter

selected_genre = st.sidebar.multiselect(
    "🎭 Genre",
    sorted(df["Genre"].unique())
)


# Release Period Filter

selected_period = st.sidebar.multiselect(
    "📅 Release Period",
    sorted(df["Release Period"].unique())
)


# Remake Filter

selected_remake = st.sidebar.multiselect(
    "🔁 Remake",
    sorted(df["Whether Remake"].unique())
)


# Franchise Filter

selected_franchise = st.sidebar.multiselect(
    "🎞️ Franchise",
    sorted(df["Whether Franchise"].unique())
)


# Director Filter

selected_director = st.sidebar.multiselect(
    "🎥 Director",
    sorted(df["Director"].unique())
)


# Music Director Filter

selected_music = st.sidebar.multiselect(
    "🎵 Music Director",
    sorted(df["Music Director"].unique())
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_genre:

    filtered_df = filtered_df[
        filtered_df["Genre"].isin(selected_genre)
    ]


if selected_period:

    filtered_df = filtered_df[
        filtered_df["Release Period"].isin(selected_period)
    ]


if selected_remake:

    filtered_df = filtered_df[
        filtered_df["Whether Remake"].isin(selected_remake)
    ]


if selected_franchise:

    filtered_df = filtered_df[
        filtered_df["Whether Franchise"].isin(selected_franchise)
    ]


if selected_director:

    filtered_df = filtered_df[
        filtered_df["Director"].isin(selected_director)
    ]


if selected_music:

    filtered_df = filtered_df[
        filtered_df["Music Director"].isin(selected_music)
    ]


# =========================================================
# CURRENCY FUNCTION
# =========================================================

def crore(value):

    return value / 10000000


# =========================================================
# OVERVIEW
# =========================================================

st.header("📌 Overview")


total_movies = len(filtered_df)

total_revenue = filtered_df["Revenue(INR)"].sum()

total_budget = filtered_df["Budget(INR)"].sum()

total_screens = filtered_df["Number of Screens"].sum()


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "🎬 Total Movies",
        f"{total_movies:,}"
    )


with col2:

    st.metric(
        "💰 Total Revenue",
        f"₹{crore(total_revenue):,.1f} Cr"
    )


with col3:

    st.metric(
        "💵 Total Budget",
        f"₹{crore(total_budget):,.1f} Cr"
    )


with col4:

    st.metric(
        "🖥️ Total Screens",
        f"{total_screens:,.0f}"
    )


st.divider()


# =========================================================
# CHART 1 — GENRE
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🎭 Movies by Genre")

    genre_data = (
        filtered_df["Genre"]
        .value_counts()
        .reset_index()
    )

    genre_data.columns = [
        "Genre",
        "Movies"
    ]

    genre_data = genre_data.sort_values(
        "Movies",
        ascending=True
    )

    fig = px.bar(
        genre_data,
        x="Movies",
        y="Genre",
        orientation="h",
        text="Movies"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(
            l=10,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CHART 2 — RELEASE PERIOD
# =========================================================

with col2:

    st.subheader("📅 Movies by Release Period")

    period_data = (
        filtered_df["Release Period"]
        .value_counts()
        .reset_index()
    )

    period_data.columns = [
        "Release Period",
        "Movies"
    ]

    fig = px.bar(
        period_data,
        x="Release Period",
        y="Movies",
        text="Movies"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CHART 3 — REMAKE
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🔁 Original vs Remake")

    remake_data = (
        filtered_df["Whether Remake"]
        .value_counts()
        .reset_index()
    )

    remake_data.columns = [
        "Type",
        "Movies"
    ]

    fig = px.pie(
        remake_data,
        names="Type",
        values="Movies",
        hole=0.5
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# CHART 4 — FRANCHISE
# =========================================================

with col2:

    st.subheader("🎞️ Franchise vs Non-Franchise")

    franchise_data = (
        filtered_df["Whether Franchise"]
        .value_counts()
        .reset_index()
    )

    franchise_data.columns = [
        "Type",
        "Movies"
    ]

    fig = px.pie(
        franchise_data,
        names="Type",
        values="Movies",
        hole=0.5
    )

    fig.update_layout(
        height=400
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# REVENUE VS BUDGET
# =========================================================

st.subheader("💰 Revenue vs Budget — Top Movies")


money_data = filtered_df[
    [
        "Movie Name",
        "Revenue(INR)",
        "Budget(INR)"
    ]
].copy()


money_data = money_data.sort_values(
    "Revenue(INR)",
    ascending=False
).head(15)


fig = px.bar(
    money_data,
    x="Movie Name",
    y=[
        "Revenue(INR)",
        "Budget(INR)"
    ],
    barmode="group"
)


fig.update_layout(
    height=480,
    xaxis_title="Movie",
    yaxis_title="Amount (INR)",
    margin=dict(
        l=20,
        r=20,
        t=20,
        b=100
    )
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# TOP MOVIES
# =========================================================

col1, col2 = st.columns(2)


# TOP REVENUE

with col1:

    st.subheader("🏆 Top 10 Movies by Revenue")

    top_revenue = filtered_df[
        [
            "Movie Name",
            "Revenue(INR)"
        ]
    ].sort_values(
        "Revenue(INR)",
        ascending=False
    ).head(10).copy()


    top_revenue["Revenue (₹ Cr)"] = (
        top_revenue["Revenue(INR)"] /
        10000000
    ).round(2)


    top_revenue = top_revenue[
        [
            "Movie Name",
            "Revenue (₹ Cr)"
        ]
    ]


    st.dataframe(
        top_revenue,
        use_container_width=True,
        hide_index=True
    )


# TOP BUDGET

with col2:

    st.subheader("💎 Top 10 Movies by Budget")

    top_budget = filtered_df[
        [
            "Movie Name",
            "Budget(INR)"
        ]
    ].sort_values(
        "Budget(INR)",
        ascending=False
    ).head(10).copy()


    top_budget["Budget (₹ Cr)"] = (
        top_budget["Budget(INR)"] /
        10000000
    ).round(2)


    top_budget = top_budget[
        [
            "Movie Name",
            "Budget (₹ Cr)"
        ]
    ]


    st.dataframe(
        top_budget,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DIRECTOR ANALYSIS
# =========================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("🎥 Top Directors")

    director_data = (
        filtered_df["Director"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    director_data.columns = [
        "Director",
        "Movies"
    ]

    director_data = director_data.sort_values(
        "Movies",
        ascending=True
    )

    fig = px.bar(
        director_data,
        x="Movies",
        y="Director",
        orientation="h",
        text="Movies"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


with col2:

    st.subheader("🎵 Top Music Directors")

    music_data = (
        filtered_df["Music Director"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    music_data.columns = [
        "Music Director",
        "Movies"
    ]

    music_data = music_data.sort_values(
        "Movies",
        ascending=True
    )

    fig = px.bar(
        music_data,
        x="Movies",
        y="Music Director",
        orientation="h",
        text="Movies"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        height=430,
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =========================================================
# QUICK INSIGHTS
# =========================================================

st.header("💡 Quick Insights")


if len(filtered_df) > 0:

    most_common_genre = (
        filtered_df["Genre"]
        .value_counts()
        .idxmax()
    )

    most_common_period = (
        filtered_df["Release Period"]
        .value_counts()
        .idxmax()
    )

    highest_revenue_row = filtered_df.loc[
        filtered_df["Revenue(INR)"].idxmax()
    ]

    highest_budget_row = filtered_df.loc[
        filtered_df["Budget(INR)"].idxmax()
    ]


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "🎭 Most Common Genre",
            most_common_genre
        )


    with col2:

        st.metric(
            "📅 Most Common Period",
            most_common_period
        )


    with col3:

        st.metric(
            "🏆 Highest Revenue Movie",
            highest_revenue_row["Movie Name"]
        )


    with col4:

        st.metric(
            "💎 Highest Budget Movie",
            highest_budget_row["Movie Name"]
        )


else:

    st.warning(
        "No movies match the selected filters."
    )


# =========================================================
# END
# =========================================================

st.divider()

st.caption(
    "🎬 Movie Analytics Dashboard | Interactive Data Visualization"
)
