import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


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

    /* MAIN PAGE */
    .stApp {
        background-color: #f5f6f8;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* SIDEBAR */
    section[data-testid="stSidebar"] {
        background-color: #20202b;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p {
        color: white !important;
    }


    /* HEADER */
    .dashboard-header {
        background: linear-gradient(
            135deg,
            #181820,
            #34234f
        );

        padding: 30px 25px;
        border-radius: 18px;

        text-align: center;

        box-shadow:
            0 8px 25px rgba(0,0,0,0.12);

        margin-bottom: 25px;
    }

    .dashboard-header h1 {
        color: white;
        font-size: 34px;
        font-weight: 800;
        margin: 0;
    }

    .dashboard-header p {
        color: #dddddf;
        font-size: 15px;
        margin-top: 10px;
        margin-bottom: 0;
    }


    /* SECTION TITLE */
    .section-title {
        font-size: 22px;
        font-weight: 750;
        color: #222222;

        margin-top: 22px;
        margin-bottom: 12px;
    }


    /* KPI CARDS */
    .kpi-card {
        background: white;

        border-radius: 16px;

        padding: 20px;

        min-height: 130px;

        text-align: center;

        box-shadow:
            0 4px 15px rgba(0,0,0,0.07);

        border: 1px solid #eeeeee;
    }

    .kpi-icon {
        font-size: 28px;
        margin-bottom: 5px;
    }

    .kpi-title {
        font-size: 12px;
        color: #777777;

        font-weight: 600;

        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 25px;

        font-weight: 800;

        color: #222222;

        margin-top: 7px;
    }


    /* INSIGHT CARDS */
    .insight-card {
        background: white;

        border-radius: 14px;

        padding: 18px;

        min-height: 95px;

        box-shadow:
            0 3px 12px rgba(0,0,0,0.06);

        border: 1px solid #eeeeee;
    }

    .insight-label {
        font-size: 12px;
        color: #777777;
        font-weight: 600;
    }

    .insight-value {
        font-size: 17px;
        font-weight: 700;
        color: #222222;
        margin-top: 7px;
    }


    /* INFO BOX */
    .info-box {
        background: #eeeaf5;
        border-left: 5px solid #604080;

        padding: 15px;

        border-radius: 10px;

        color: #333333;

        margin-top: 10px;
    }

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = Path("Data for repository.csv")

    if not file_path.exists():
        return None

    data = pd.read_csv(file_path)

    return data


df = load_data()


# =========================================================
# CHECK FILE
# =========================================================

if df is None:

    st.error(
        "❌ Data for repository.csv was not found."
    )

    st.info(
        "Put Data for repository.csv in the same folder as app.py."
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = (
    df.columns
    .str.strip()
)


# =========================================================
# CLEAN TEXT DATA
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

for column in text_columns:

    if column in df.columns:

        df[column] = (
            df[column]
            .fillna("Unknown")
            .astype(str)
            .str.strip()
        )


# =========================================================
# CLEAN NUMERIC DATA
# =========================================================

numeric_columns = [
    "Number of Screens",
    "Revenue(INR)",
    "Budget(INR)"
]

for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        ).fillna(0)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="dashboard-header">

    <h1>🎬 MOVIE ANALYTICS DASHBOARD</h1>

    <p>
        Explore Movie Trends, Revenue, Budget, Genres & Performance
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.markdown("# 🎞️ MOVIE FILTERS")

st.sidebar.markdown("---")


# =========================================================
# GENRE FILTER
# =========================================================

genres = sorted(
    df["Genre"].unique()
)

selected_genres = st.sidebar.multiselect(
    "🎭 Genre",
    genres,
    placeholder="Select genre"
)


# =========================================================
# RELEASE PERIOD FILTER
# =========================================================

release_periods = sorted(
    df["Release Period"].unique()
)

selected_periods = st.sidebar.multiselect(
    "📅 Release Period",
    release_periods,
    placeholder="Select period"
)


# =========================================================
# REMAKE FILTER
# =========================================================

remake_options = sorted(
    df["Whether Remake"].unique()
)

selected_remake = st.sidebar.multiselect(
    "🔁 Remake",
    remake_options,
    placeholder="Select option"
)


# =========================================================
# FRANCHISE FILTER
# =========================================================

franchise_options = sorted(
    df["Whether Franchise"].unique()
)

selected_franchise = st.sidebar.multiselect(
    "🎞️ Franchise",
    franchise_options,
    placeholder="Select option"
)


# =========================================================
# DIRECTOR FILTER
# =========================================================

director_options = sorted(
    df["Director"].unique()
)

selected_director = st.sidebar.multiselect(
    "🎥 Director",
    director_options,
    placeholder="Select director"
)


# =========================================================
# MUSIC DIRECTOR FILTER
# =========================================================

music_options = sorted(
    df["Music Director"].unique()
)

selected_music = st.sidebar.multiselect(
    "🎵 Music Director",
    music_options,
    placeholder="Select music director"
)


# =========================================================
# RESET BUTTON
# =========================================================

if st.sidebar.button(
    "🔄 Reset Filters",
    use_container_width=True
):

    st.rerun()


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_genres:

    filtered_df = filtered_df[
        filtered_df["Genre"].isin(selected_genres)
    ]


if selected_periods:

    filtered_df = filtered_df[
        filtered_df["Release Period"].isin(selected_periods)
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
# KPI CALCULATIONS
# =========================================================

total_movies = len(filtered_df)

total_revenue = filtered_df[
    "Revenue(INR)"
].sum()

total_budget = filtered_df[
    "Budget(INR)"
].sum()

total_screens = filtered_df[
    "Number of Screens"
].sum()


# =========================================================
# CURRENCY FORMAT
# =========================================================

def format_crore(value):

    crore = value / 10000000

    if crore >= 1000:

        return f"₹{crore / 1000:.1f}K Cr"

    return f"₹{crore:.1f} Cr"


# =========================================================
# OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📌 Overview</div>',
    unsafe_allow_html=True
)


k1, k2, k3, k4 = st.columns(4)


# =========================================================
# KPI 1
# =========================================================

with k1:

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


# =========================================================
# KPI 2
# =========================================================

with k2:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">💰</div>

        <div class="kpi-title">
            TOTAL REVENUE
        </div>

        <div class="kpi-value">
            {format_crore(total_revenue)}
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# KPI 3
# =========================================================

with k3:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">💵</div>

        <div class="kpi-title">
            TOTAL BUDGET
        </div>

        <div class="kpi-value">
            {format_crore(total_budget)}
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# KPI 4
# =========================================================

with k4:

    st.markdown(f"""
    <div class="kpi-card">

        <div class="kpi-icon">🖥️</div>

        <div class="kpi-title">
            TOTAL SCREENS
        </div>

        <div class="kpi-value">
            {total_screens:,.0f}
        </div>

    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ROW 1
# =========================================================

col1, col2 = st.columns(2)


# =========================================================
# MOVIES BY GENRE
# =========================================================

with col1:

    st.markdown(
        '<div class="section-title">🎭 Movies by Genre</div>',
        unsafe_allow_html=True
    )

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

    fig_genre = px.bar(
        genre_data,
        x="Movies",
        y="Genre",
        orientation="h",
        text="Movies"
    )

    fig_genre.update_traces(
        textposition="outside"
    )

    fig_genre.update_layout(
        height=420,
        template="simple_white",
        margin=dict(
            l=10,
            r=30,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )


# =========================================================
# RELEASE PERIOD
# =========================================================

with col2:

    st.markdown(
        '<div class="section-title">📅 Movies by Release Period</div>',
        unsafe_allow_html=True
    )

    release_data = (
        filtered_df["Release Period"]
        .value_counts()
        .reset_index()
    )

    release_data.columns = [
        "Release Period",
        "Movies"
    ]

    fig_release = px.bar(
        release_data,
        x="Release Period",
        y="Movies",
        text="Movies"
    )

    fig_release.update_traces(
        textposition="outside"
    )

    fig_release.update_layout(
        height=420,
        template="simple_white",
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig_release,
        use_container_width=True
    )


# =========================================================
# ROW 2
# =========================================================

col3, col4 = st.columns(2)


# =========================================================
# ORIGINAL VS REMAKE
# =========================================================

with col3:

    st.markdown(
        '<div class="section-title">🔁 Original vs Remake</div>',
        unsafe_allow_html=True
    )

    remake_data = (
        filtered_df["Whether Remake"]
        .value_counts()
        .reset_index()
    )

    remake_data.columns = [
        "Type",
        "Movies"
    ]

    fig_remake = px.pie(
        remake_data,
        names="Type",
        values="Movies",
        hole=0.55
    )

    fig_remake.update_layout(
        height=400,
        template="simple_white",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_remake,
        use_container_width=True
    )


# =========================================================
# FRANCHISE
# =========================================================

with col4:

    st.markdown(
        '<div class="section-title">🎞️ Franchise vs Non-Franchise</div>',
        unsafe_allow_html=True
    )

    franchise_data = (
        filtered_df["Whether Franchise"]
        .value_counts()
        .reset_index()
    )

    franchise_data.columns = [
        "Type",
        "Movies"
    ]

    fig_franchise = px.pie(
        franchise_data,
        names="Type",
        values="Movies",
        hole=0.55
    )

    fig_franchise.update_layout(
        height=400,
        template="simple_white",
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=20
        )
    )

    st.plotly_chart(
        fig_franchise,
        use_container_width=True
    )


# =========================================================
# REVENUE VS BUDGET
# =========================================================

st.markdown(
    '<div class="section-title">💰 Revenue vs Budget — Top Movies</div>',
    unsafe_allow_html=True
)


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


fig_money = px.bar(
    money_data,
    x="Movie Name",
    y=[
        "Revenue(INR)",
        "Budget(INR)"
    ],
    barmode="group"
)


fig_money.update_layout(
    height=470,
    template="simple_white",
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
    fig_money,
    use_container_width=True
)


# =========================================================
# TOP 10 MOVIES
# =========================================================

top_revenue_col, top_budget_col = st.columns(2)


# =========================================================
# TOP REVENUE
# =========================================================

with top_revenue_col:

    st.markdown(
        '<div class="section-title">🏆 Top 10 Movies by Revenue</div>',
        unsafe_allow_html=True
    )

    top_revenue = (
        filtered_df[
            [
                "Movie Name",
                "Revenue(INR)"
            ]
        ]
        .sort_values(
            "Revenue(INR)",
            ascending=False
        )
        .head(10)
        .copy()
    )

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

    top_revenue.columns = [
        "Movie",
        "Revenue (₹ Cr)"
    ]

    st.dataframe(
        top_revenue,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# TOP BUDGET
# =========================================================

with top_budget_col:

    st.markdown(
        '<div class="section-title">💎 Top 10 Movies by Budget</div>',
        unsafe_allow_html=True
    )

    top_budget = (
        filtered_df[
            [
                "Movie Name",
                "Budget(INR)"
            ]
        ]
        .sort_values(
            "Budget(INR)",
            ascending=False
        )
        .head(10)
        .copy()
    )

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

    top_budget.columns = [
        "Movie",
        "Budget (₹ Cr)"
    ]

    st.dataframe(
        top_budget,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# DIRECTOR ANALYSIS
# =========================================================

director_col, music_col = st.columns(2)


# =========================================================
# DIRECTORS
# =========================================================

with director_col:

    st.markdown(
        '<div class="section-title">🎥 Top Directors</div>',
        unsafe_allow_html=True
    )

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

    fig_director = px.bar(
        director_data,
        x="Movies",
        y="Director",
        orientation="h",
        text="Movies"
    )

    fig_director.update_traces(
        textposition="outside"
    )

    fig_director.update_layout(
        height=430,
        template="simple_white",
        showlegend=False
    )

    st.plotly_chart(
        fig_director,
        use_container_width=True
    )


# =========================================================
# MUSIC DIRECTORS
# =========================================================

with music_col:

    st.markdown(
        '<div class="section-title">🎵 Top Music Directors</div>',
        unsafe_allow_html=True
    )

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

    fig_music = px.bar(
        music_data,
        x="Movies",
        y="Music Director",
        orientation="h",
        text="Movies"
    )

    fig_music.update_traces(
        textposition="outside"
    )

    fig_music.update_layout(
        height=430,
        template="simple_white",
        showlegend=False
    )

    st.plotly_chart(
        fig_music,
        use_container_width=True
    )


# =========================================================
# QUICK INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">💡 Quick Insights</div>',
    unsafe_allow_html=True
)


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

    highest_revenue_index = (
        filtered_df["Revenue(INR)"].idxmax()
    )

    highest_budget_index = (
        filtered_df["Budget(INR)"].idxmax()
    )

    highest_revenue_movie = filtered_df.loc[
        highest_revenue_index,
        "Movie Name"
    ]

    highest_budget_movie = filtered_df.loc[
        highest_budget_index,
        "Movie Name"
    ]


    i1, i2, i3, i4 = st.columns(4)


    with i1:

        st.markdown(f"""
        <div class="insight-card">

            <div class="insight-label">
                🎭 MOST COMMON GENRE
            </div>

            <div class="insight-value">
                {most_common_genre}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with i2:

        st.markdown(f"""
        <div class="insight-card">

            <div class="insight-label">
                📅 MOST COMMON PERIOD
            </div>

            <div class="insight-value">
                {most_common_period}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with i3:

        st.markdown(f"""
        <div class="insight-card">

            <div class="insight-label">
                🏆 HIGHEST REVENUE
            </div>

            <div class="insight-value">
                {highest_revenue_movie}
            </div>

        </div>
        """, unsafe_allow_html=True)


    with i4:

        st.markdown(f"""
        <div class="insight-card">

            <div class="insight-label">
                💎 HIGHEST BUDGET
            </div>

            <div class="insight-value">
                {highest_budget_movie}
            </div>

        </div>
        """, unsafe_allow_html=True)


else:

    st.warning(
        "No movies match the selected filters."
    )


# =========================================================
# DATA PREVIEW
# =========================================================

with st.expander("📋 View Movie Dataset"):

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<br>

<div style="
    text-align:center;
    padding:20px;
    color:#777;
">

    🎬 <b>Movie Analytics Dashboard</b>
    <br>
    <small>
        Interactive Movie Data Analysis
    </small>

</div>
""", unsafe_allow_html=True)
