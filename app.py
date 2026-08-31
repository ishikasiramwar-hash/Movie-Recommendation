import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path


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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f6f8;
}

/* HEADER */
.header {
    background: linear-gradient(135deg, #171722, #35264f);
    padding: 30px;
    border-radius: 18px;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.12);
}

.header h1 {
    color: white;
    font-size: 36px;
    margin: 0;
    font-weight: 800;
}

.header p {
    color: #d8d8df;
    font-size: 15px;
    margin-top: 8px;
}


/* KPI CARDS */
.kpi-card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    min-height: 125px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.07);
}

.kpi-icon {
    font-size: 25px;
}

.kpi-title {
    color: #777;
    font-size: 13px;
    margin-top: 5px;
}

.kpi-value {
    color: #222;
    font-size: 26px;
    font-weight: 800;
    margin-top: 6px;
}


/* SECTION TITLES */
.section-title {
    font-size: 21px;
    font-weight: 750;
    color: #222;
    margin-top: 25px;
    margin-bottom: 12px;
}


/* INSIGHT CARDS */
.insight-card {
    background: white;
    padding: 18px;
    border-radius: 14px;
    min-height: 90px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.06);
}

.insight-label {
    color: #777;
    font-size: 12px;
}

.insight-value {
    color: #222;
    font-size: 17px;
    font-weight: 700;
    margin-top: 7px;
}


/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #20202b;
}

section[data-testid="stSidebar"] * {
    color: white;
}


/* REMOVE EXTRA TOP SPACE */
.block-container {
    padding-top: 2rem;
}


/* TABLE */
[data-testid="stDataFrame"] {
    border-radius: 12px;
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
        return pd.DataFrame()

    return pd.read_csv(file_path)


df = load_data()


# =========================================================
# CHECK DATA
# =========================================================

if df.empty:

    st.error(
        "❌ Data for repository.csv was not found. "
        "Place the CSV file in the same folder as app.py."
    )

    st.stop()


# =========================================================
# CLEAN COLUMN NAMES
# =========================================================

df.columns = df.columns.str.strip()


# =========================================================
# CONVERT NUMERIC COLUMNS
# =========================================================

df["Revenue(INR)"] = pd.to_numeric(
    df["Revenue(INR)"],
    errors="coerce"
).fillna(0)

df["Budget(INR)"] = pd.to_numeric(
    df["Budget(INR)"],
    errors="coerce"
).fillna(0)

df["Number of Screens"] = pd.to_numeric(
    df["Number of Screens"],
    errors="coerce"
).fillna(0)


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="header">

    <h1>🎬 MOVIE ANALYTICS DASHBOARD</h1>

    <p>
        Explore Movie Trends, Revenue, Budget, Genres & Performance
    </p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR FILTERS
# =========================================================

st.sidebar.markdown("## 🎞️ MOVIE FILTERS")

st.sidebar.markdown("---")


# ---------------------------------------------------------
# GENRE
# ---------------------------------------------------------

genre_list = sorted(
    df["Genre"]
    .dropna()
    .astype(str)
    .unique()
)

selected_genre = st.sidebar.multiselect(
    "🎭 Genre",
    genre_list,
    placeholder="Select genre"
)


# ---------------------------------------------------------
# RELEASE PERIOD
# ---------------------------------------------------------

release_list = sorted(
    df["Release Period"]
    .dropna()
    .astype(str)
    .unique()
)

selected_release = st.sidebar.multiselect(
    "📅 Release Period",
    release_list,
    placeholder="Select period"
)


# ---------------------------------------------------------
# REMAKE
# ---------------------------------------------------------

remake_list = sorted(
    df["Whether Remake"]
    .dropna()
    .astype(str)
    .unique()
)

selected_remake = st.sidebar.multiselect(
    "🔁 Remake",
    remake_list,
    placeholder="Select option"
)


# ---------------------------------------------------------
# FRANCHISE
# ---------------------------------------------------------

franchise_list = sorted(
    df["Whether Franchise"]
    .dropna()
    .astype(str)
    .unique()
)

selected_franchise = st.sidebar.multiselect(
    "🎞️ Franchise",
    franchise_list,
    placeholder="Select option"
)


# ---------------------------------------------------------
# DIRECTOR
# ---------------------------------------------------------

director_list = sorted(
    df["Director"]
    .dropna()
    .astype(str)
    .unique()
)

selected_director = st.sidebar.multiselect(
    "🎥 Director",
    director_list,
    placeholder="Select director"
)


# ---------------------------------------------------------
# MUSIC DIRECTOR
# ---------------------------------------------------------

music_list = sorted(
    df["Music Director"]
    .dropna()
    .astype(str)
    .unique()
)

selected_music = st.sidebar.multiselect(
    "🎵 Music Director",
    music_list,
    placeholder="Select music director"
)


# =========================================================
# APPLY FILTERS
# =========================================================

filtered_df = df.copy()


if selected_genre:

    filtered_df = filtered_df[
        filtered_df["Genre"].isin(selected_genre)
    ]


if selected_release:

    filtered_df = filtered_df[
        filtered_df["Release Period"].isin(selected_release)
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

total_revenue = filtered_df["Revenue(INR)"].sum()

total_budget = filtered_df["Budget(INR)"].sum()

total_screens = filtered_df["Number of Screens"].sum()


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


# ---------------------------------------------------------
# TOTAL MOVIES
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TOTAL REVENUE
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TOTAL BUDGET
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# TOTAL SCREENS
# ---------------------------------------------------------

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
# CHART SECTION 1
# =========================================================

chart1, chart2 = st.columns(2)


# =========================================================
# MOVIES BY GENRE
# =========================================================

with chart1:

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
        template="simple_white",
        height=420,
        margin=dict(
            l=10,
            r=30,
            t=10,
            b=10
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig_genre,
        use_container_width=True
    )


# =========================================================
# MOVIES BY RELEASE PERIOD
# =========================================================

with chart2:

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
        template="simple_white",
        height=420,
        margin=dict(
            l=20,
            r=20,
            t=10,
            b=20
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig_release,
        use_container_width=True
    )


# =========================================================
# CHART SECTION 2
# =========================================================

chart3, chart4 = st.columns(2)


# =========================================================
# ORIGINAL VS REMAKE
# =========================================================

with chart3:

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
        template="simple_white",
        height=400,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
        )
    )

    st.plotly_chart(
        fig_remake,
        use_container_width=True
    )


# =========================================================
# FRANCHISE VS NON-FRANCHISE
# =========================================================

with chart4:

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
        template="simple_white",
        height=400,
        margin=dict(
            l=10,
            r=10,
            t=10,
            b=10
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
    '<div class="section-title">💰 Revenue vs Budget</div>',
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
    template="simple_white",
    height=450,
    xaxis_title="Movie",
    yaxis_title="Amount (INR)",
    margin=dict(
        l=20,
        r=20,
        t=10,
        b=100
    )
)


st.plotly_chart(
    fig_money,
    use_container_width=True
)


# =========================================================
# TOP MOVIES
# =========================================================

top1, top2 = st.columns(2)


# =========================================================
# TOP REVENUE MOVIES
# =========================================================

with top1:

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
# TOP BUDGET MOVIES
# =========================================================

with top2:

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
# DIRECTORS
# =========================================================

director_col, music_col = st.columns(2)


# =========================================================
# TOP DIRECTORS
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

    fig_director.update_layout(
        template="simple_white",
        height=420,
        showlegend=False
    )

    fig_director.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig_director,
        use_container_width=True
    )


# =========================================================
# TOP MUSIC DIRECTORS
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

    fig_music.update_layout(
        template="simple_white",
        height=420,
        showlegend=False
    )

    fig_music.update_traces(
        textposition="outside"
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


# Most common genre
most_common_genre = (
    filtered_df["Genre"]
    .value_counts()
    .idxmax()
)


# Most common release period
most_common_period = (
    filtered_df["Release Period"]
    .value_counts()
    .idxmax()
)


# Highest revenue movie
highest_revenue_row = filtered_df.loc[
    filtered_df["Revenue(INR)"].idxmax()
]

highest_revenue_movie = highest_revenue_row[
    "Movie Name"
]


# Highest budget movie
highest_budget_row = filtered_df.loc[
    filtered_df["Budget(INR)"].idxmax()
]

highest_budget_movie = highest_budget_row[
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


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<br>
<hr>

<div style="
    text-align:center;
    color:#777;
    padding:15px;
">

🎬 <b>Movie Analytics Dashboard</b>
<br>

<small>
Interactive analysis using movie data
</small>

</div>
""", unsafe_allow_html=True)
