# ============================================================
# GAMEPULSE
# Video Game Sales & Engagement Intelligence
# Streamlit Dashboard V2
# ============================================================

import os
import sqlite3

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="GAMEPULSE | Video Game Intelligence",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

PROCESSED_DIR = os.path.join(
    BASE_DIR,
    "data",
    "processed"
)

DATABASE_DIR = os.path.join(
    BASE_DIR,
    "database"
)

DB_PATH = os.path.join(
    DATABASE_DIR,
    "video_game_analysis.db"
)

GAMES_PATH = os.path.join(
    PROCESSED_DIR,
    "games_cleaned.csv"
)

SALES_PATH = os.path.join(
    PROCESSED_DIR,
    "vgsales_cleaned.csv"
)

ANNUAL_SALES_PATH = os.path.join(
    PROCESSED_DIR,
    "annual_sales_forecasting.csv"
)

MODEL_COMPARISON_PATH = os.path.join(
    PROCESSED_DIR,
    "forecast_model_comparison.csv"
)

FUTURE_FORECAST_PATH = os.path.join(
    PROCESSED_DIR,
    "future_sales_forecast.csv"
)

ANOMALY_SUMMARY_PATH = os.path.join(
    PROCESSED_DIR,
    "anomaly_summary.csv"
)

SALES_ANOMALIES_PATH = os.path.join(
    PROCESSED_DIR,
    "sales_anomalies.csv"
)

REGIONAL_ANOMALIES_PATH = os.path.join(
    PROCESSED_DIR,
    "regional_sales_anomalies.csv"
)

ENGAGEMENT_ANOMALIES_PATH = os.path.join(
    PROCESSED_DIR,
    "engagement_sales_anomalies.csv"
)


# ============================================================
# DARK THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ======================================================
       GLOBAL APP
       ====================================================== */

    .stApp {
        background: #080d19 !important;
        color: #e8edf7 !important;
    }

    [data-testid="stHeader"] {
        background: #080d19 !important;
    }

    [data-testid="stToolbar"] {
        visibility: hidden;
    }

    .main .block-container,
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1500px;
    }

    /* ======================================================
       GLOBAL TEXT
       ====================================================== */

    .stApp p,
    .stApp label,
    .stApp .stMarkdown,
    .stApp [data-testid="stCaptionContainer"] {
        color: #dce5f4 !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    /* ======================================================
       SIDEBAR
       ====================================================== */

    section[data-testid="stSidebar"] {
        background: #070c17 !important;
        border-right: 1px solid #202b40 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #e8edf7 !important;
    }

    section[data-testid="stSidebar"] .nav-label {
        color: #6f819e !important;
    }

    /* ======================================================
       SIDEBAR REOPEN CONTROL
       Keep Streamlit's sidebar toggle accessible after
       the sidebar has been collapsed.
       ====================================================== */

    div[data-testid="collapsedControl"] {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        position: fixed !important;
        top: 0.75rem !important;
        left: 0.75rem !important;
        z-index: 999999 !important;
    }

    div[data-testid="collapsedControl"] button {
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        align-items: center !important;
        justify-content: center !important;
        min-width: 2.25rem !important;
        min-height: 2.25rem !important;
        border-radius: 8px !important;
        background: #111a2b !important;
        border: 1px solid #2a3952 !important;
        color: #e8edf7 !important;
        z-index: 999999 !important;
    }

    div[data-testid="collapsedControl"] button:hover {
        background: #1b2940 !important;
        border-color: #4da3ff !important;
    }

    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        opacity: 1 !important;
        z-index: 999999 !important;
    }

    /* Radio navigation */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #6f819e !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] label {
        color: #e8edf7 !important;
    }

    /* ======================================================
       BRAND / TYPOGRAPHY
       ====================================================== */

    .brand {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff !important;
        margin-bottom: 0;
    }

    .brand-accent {
        color: #4da3ff !important;
    }

    .brand-subtitle {
        color: #8fa0ba !important;
        font-size: 13px;
        margin-top: 2px;
        margin-bottom: 28px;
    }

    .page-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1px;
        color: #ffffff !important;
        margin-bottom: 5px;
    }

    .page-subtitle {
        color: #91a1ba !important;
        font-size: 14px;
        margin-bottom: 28px;
    }

    .section-title {
        color: #ffffff !important;
        font-size: 21px;
        font-weight: 700;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    /* ======================================================
       KPI / METRIC CARDS
       ====================================================== */

    div[data-testid="stMetric"] {
        background: linear-gradient(
            145deg,
            #131d30 0%,
            #0f1728 100%
        ) !important;

        border: 1px solid #26344c !important;
        border-radius: 14px !important;

        padding: 18px 20px !important;

        min-height: 105px;

        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.20);
    }

    [data-testid="stMetricLabel"] {
        color: #8fa0ba !important;
    }

    [data-testid="stMetricLabel"] p,
    [data-testid="stMetricLabel"] div {
        color: #8fa0ba !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        overflow: visible !important;
        white-space: nowrap !important;
        text-overflow: clip !important;
        min-width: max-content !important;
    }

    [data-testid="stMetricValue"] div {
        color: #ffffff !important;
        font-weight: 800 !important;
        font-size: 27px !important;
        line-height: 1.2 !important;
        overflow: visible !important;
        white-space: nowrap !important;
        text-overflow: clip !important;
        min-width: max-content !important;
    }

    [data-testid="stMetric"] [data-testid="stMetricValue"] *,
    [data-testid="stMetricValue"] [data-testid="stMetricValue"] {
        overflow: visible !important;
        text-overflow: clip !important;
    }

    /* Keep long KPI values readable */
    [data-testid="stMetric"] {
        overflow: visible !important;
    }

    [data-testid="stMetricLabel"] {
        white-space: nowrap !important;
        overflow: visible !important;
    }

    [data-testid="stMetricDelta"] {
        color: #71d6b2 !important;
    }

    /* ======================================================
       PANELS
       ====================================================== */

    .panel {
        background-color: #101725;
        border: 1px solid #202c42;
        border-radius: 14px;
        padding: 20px;
    }

    /* ======================================================
       SELECTBOX / MULTISELECT
       ====================================================== */

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] div {
        color: #a9b7ca !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] {
        background-color: #111a2b !important;
        color: #ffffff !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #111a2b !important;
        border: 1px solid #2a3952 !important;
        color: #ffffff !important;
    }

    div[data-baseweb="select"] span {
        color: #ffffff !important;
    }

    div[data-baseweb="select"] input {
        color: #ffffff !important;
        caret-color: #ffffff !important;
    }

    div[data-baseweb="select"] input::placeholder {
        color: #71819a !important;
        opacity: 1 !important;
    }

    div[data-baseweb="select"] svg {
        fill: #9aabc3 !important;
    }

    /* Dropdown popup */
    div[role="listbox"] {
        background-color: #111a2b !important;
        border: 1px solid #2a3952 !important;
    }

    div[role="option"] {
        background-color: #111a2b !important;
        color: #e8edf7 !important;
    }

    div[role="option"] * {
        color: #e8edf7 !important;
    }

    div[role="option"]:hover {
        background-color: #1b2940 !important;
        color: #ffffff !important;
    }

    div[role="option"][aria-selected="true"] {
        background-color: #1e5fa8 !important;
        color: #ffffff !important;
    }

    /* Multiselect selected tags */
    span[data-baseweb="tag"] {
        background-color: #1e5fa8 !important;
        color: #ffffff !important;
    }

    span[data-baseweb="tag"] span {
        color: #ffffff !important;
    }

    span[data-baseweb="tag"] svg {
        fill: #ffffff !important;
    }

    /* ======================================================
       INPUTS
       ====================================================== */

    div[data-baseweb="input"] > div {
        background-color: #111a2b !important;
        border: 1px solid #2a3952 !important;
    }

    div[data-baseweb="input"] input {
        color: #ffffff !important;
    }

    /* ======================================================
       DATAFRAME
       ====================================================== */

    [data-testid="stDataFrame"] {
        border: 1px solid #202d43 !important;
        border-radius: 10px !important;
    }

    /* ======================================================
       FOOTER
       ====================================================== */

    .footer {
        color: #64748c !important;
        text-align: center;
        font-size: 11px;
        padding-top: 30px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PLOTLY THEME
# ============================================================

PLOT_BG = "#101725"
PAPER_BG = "#101725"
TEXT_COLOR = "#dce5f4"
GRID_COLOR = "#202c42"
ACCENT = "#4da3ff"


def apply_plotly_theme(fig):

    fig.update_layout(
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,

        font=dict(
            color="#dce5f4",
            family="Arial"
        ),

        title=dict(
            font=dict(
                color="#ffffff",
                size=16
            )
        ),

        margin=dict(
            l=35,
            r=25,
            t=55,
            b=40
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#dce5f4",
                size=12
            )
        ),

        hoverlabel=dict(
            bgcolor="#172238",
            bordercolor="#34445f",
            font=dict(
                color="#ffffff"
            )
        )
    )

    fig.update_xaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        color="#9aabc3",
        title_font=dict(
            color="#dce5f4"
        ),
        tickfont=dict(
            color="#9aabc3"
        )
    )

    fig.update_yaxes(
        gridcolor=GRID_COLOR,
        zerolinecolor=GRID_COLOR,
        color="#9aabc3",
        title_font=dict(
            color="#dce5f4"
        ),
        tickfont=dict(
            color="#9aabc3"
        )
    )

    return fig


# ============================================================
# DATA LOADING
# ============================================================

@st.cache_data
def load_games():

    return pd.read_csv(
        GAMES_PATH
    )


@st.cache_data
def load_sales():

    df = pd.read_csv(
        SALES_PATH
    )

    df["Year"] = pd.to_numeric(
        df["Year"],
        errors="coerce"
    )

    df["Global_Sales"] = pd.to_numeric(
        df["Global_Sales"],
        errors="coerce"
    )

    return df


@st.cache_data
def load_annual_sales():

    if not os.path.exists(
        ANNUAL_SALES_PATH
    ):
        return pd.DataFrame()

    return pd.read_csv(
        ANNUAL_SALES_PATH
    )


@st.cache_data
def load_model_comparison():

    if not os.path.exists(
        MODEL_COMPARISON_PATH
    ):
        return pd.DataFrame()

    return pd.read_csv(
        MODEL_COMPARISON_PATH
    )


@st.cache_data
def load_future_forecast():

    if not os.path.exists(
        FUTURE_FORECAST_PATH
    ):
        return pd.DataFrame()

    return pd.read_csv(
        FUTURE_FORECAST_PATH
    )


@st.cache_data
def load_anomaly_summary():

    if not os.path.exists(
        ANOMALY_SUMMARY_PATH
    ):
        return pd.DataFrame()

    return pd.read_csv(
        ANOMALY_SUMMARY_PATH
    )


@st.cache_data
def load_anomaly_file(path):

    if not os.path.exists(path):
        return pd.DataFrame()

    return pd.read_csv(path)


@st.cache_data
def load_database_tables():

    if not os.path.exists(DB_PATH):
        return pd.DataFrame()

    connection = sqlite3.connect(
        DB_PATH
    )

    tables = pd.read_sql_query(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """,
        connection
    )

    connection.close()

    return tables


# ============================================================
# LOAD ALL DATA
# ============================================================

try:

    games = load_games()
    sales = load_sales()
    annual_sales = load_annual_sales()
    model_comparison = load_model_comparison()
    future_forecast = load_future_forecast()
    anomaly_summary = load_anomaly_summary()

    sales_anomalies = load_anomaly_file(
        SALES_ANOMALIES_PATH
    )

    regional_anomalies = load_anomaly_file(
        REGIONAL_ANOMALIES_PATH
    )

    engagement_anomalies = load_anomaly_file(
        ENGAGEMENT_ANOMALIES_PATH
    )

    database_tables = load_database_tables()

except Exception as error:

    st.error(
        f"Unable to load project data: {error}"
    )

    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            🎮 GAME<span class="brand-accent">PULSE</span>
        </div>

        <div class="brand-subtitle">
            VIDEO GAME INTELLIGENCE PLATFORM
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="nav-label">ANALYTICS</div>',
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Sales Analysis",
            "Game & Engagement",
            "Regional Analysis",
            "Forecasting",
            "Anomaly Analysis"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown(
        """
        <div style="
            color:#66738a;
            font-size:11px;
            line-height:1.7;
        ">
        DATA SCIENCE CAPSTONE<br>
        Sales • Engagement • Market Intelligence
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    st.markdown(
        '<div class="page-title">Video Game Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'A consolidated view of game sales, market performance '
        'and player engagement.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    total_games = len(games)

    total_sales = sales[
        "Global_Sales"
    ].sum()

    total_platforms = sales[
        "Platform"
    ].nunique()

    total_genres = sales[
        "Genre"
    ].nunique()

    total_publishers = sales[
        "Publisher"
    ].nunique()

    kpi_cols = st.columns(5)

    kpis = [
        (
            "TOTAL GAMES",
            f"{total_games:,}",
            "Games dataset"
        ),
        (
            "GLOBAL SALES",
            f"{total_sales:,.2f}M",
            "All recorded sales"
        ),
        (
            "PLATFORMS",
            f"{total_platforms}",
            "Gaming platforms"
        ),
        (
            "PUBLISHERS",
            f"{total_publishers}",
            "Recorded publishers"
        ),
        (
            "GENRES",
            f"{total_genres}",
            "Sales genres"
        )
    ]

    for col, data in zip(
        kpi_cols,
        kpis
    ):

        label, value, description = data

        with col:
            st.metric(
                label=label,
                value=value,
                help=description
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------
    # SALES TREND + TOP PLATFORMS
    # --------------------------------------------------------

    left, right = st.columns(
        [1.65, 1]
    )

    with left:

        st.markdown(
            '<div class="section-title">'
            'Global Sales Trend'
            '</div>',
            unsafe_allow_html=True
        )

        if not annual_sales.empty:

            fig = px.area(
                annual_sales,
                x="Year",
                y="Global_Sales",
                title="Global Sales Trend"
            )

            fig.update_traces(
                line_color=ACCENT,
                fillcolor="rgba(77,163,255,0.16)"
            )

            fig.update_layout(
                title_text="Global Sales Trend",
                xaxis_title=None,
                yaxis_title="Sales (Million)"
            )

            fig = apply_plotly_theme(
                fig
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    with right:

        st.markdown(
            '<div class="section-title">'
            'Top Platforms'
            '</div>',
            unsafe_allow_html=True
        )

        platform_sales = (
            sales
            .groupby("Platform")[
                "Global_Sales"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(8)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            platform_sales,
            x="Global_Sales",
            y="Platform",
            orientation="h",
            title="Top Platforms"
        )

        fig.update_traces(
            marker_color=ACCENT
        )

        fig.update_layout(
            title_text="Top Platforms",
            xaxis_title="Sales (Million)",
            yaxis_title=None
        )

        fig = apply_plotly_theme(
            fig
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # GENRE + REGIONAL
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        st.markdown(
            '<div class="section-title">'
            'Genre Performance'
            '</div>',
            unsafe_allow_html=True
        )

        genre_sales = (
            sales
            .groupby("Genre")[
                "Global_Sales"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .reset_index()
        )

        fig = px.bar(
            genre_sales,
            x="Genre",
            y="Global_Sales"
        )

        fig.update_traces(
            marker_color="#6c8cff"
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Sales (Million)"
        )

        fig = apply_plotly_theme(
            fig
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        st.markdown(
            '<div class="section-title">'
            'Regional Sales'
            '</div>',
            unsafe_allow_html=True
        )

        regional = pd.DataFrame({
            "Region": [
                "North America",
                "Europe",
                "Japan",
                "Other"
            ],
            "Sales": [
                sales["NA_Sales"].sum(),
                sales["EU_Sales"].sum(),
                sales["JP_Sales"].sum(),
                sales["Other_Sales"].sum()
            ]
        })

        fig = px.bar(
            regional,
            x="Region",
            y="Sales"
        )

        fig.update_traces(
            marker_color="#55d6be"
        )

        fig.update_layout(
            xaxis_title=None,
            yaxis_title="Sales (Million)"
        )

        fig = apply_plotly_theme(
            fig
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # TOP GAMES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Top Selling Games'
        '</div>',
        unsafe_allow_html=True
    )

    top_games = (
        sales[
            [
                "Name",
                "Platform",
                "Genre",
                "Publisher",
                "Global_Sales"
            ]
        ]
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(10)
        .reset_index(drop=True)
    )

    top_games.index = top_games.index + 1

    st.dataframe(
        top_games,
        use_container_width=True,
        height=380
    )


# ============================================================
# SALES ANALYSIS
# ============================================================

elif page == "Sales Analysis":

    st.markdown(
        '<div class="page-title">Sales Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Explore platform, publisher, genre and yearly sales performance.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # FILTER BAR
    # --------------------------------------------------------

    filter1, filter2 = st.columns(2)

    with filter1:

        selected_platforms = st.multiselect(
            "Platforms",
            sorted(
                sales["Platform"]
                .dropna()
                .unique()
            )
        )

    with filter2:

        selected_genres = st.multiselect(
            "Genres",
            sorted(
                sales["Genre"]
                .dropna()
                .unique()
            )
        )

    filtered = sales.copy()

    if selected_platforms:

        filtered = filtered[
            filtered["Platform"].isin(
                selected_platforms
            )
        ]

    if selected_genres:

        filtered = filtered[
            filtered["Genre"].isin(
                selected_genres
            )
        ]

    # --------------------------------------------------------
    # KPIs
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Records",
        f"{len(filtered):,}"
    )

    c2.metric(
        "Global Sales",
        f"{filtered['Global_Sales'].sum():,.2f}M"
    )

    c3.metric(
        "Average Sales",
        f"{filtered['Global_Sales'].mean():.2f}M"
    )

    c4.metric(
        "Platforms",
        f"{filtered['Platform'].nunique()}"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # PLATFORM + PUBLISHER
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        platform_sales = (
            filtered
            .groupby("Platform")[
                "Global_Sales"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(12)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            platform_sales,
            x="Global_Sales",
            y="Platform",
            orientation="h"
        )

        fig.update_traces(
            marker_color=ACCENT
        )

        fig.update_layout(
            title="Top Platforms",
            xaxis_title="Sales (Million)",
            yaxis_title=None
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        publisher_sales = (
            filtered
            .groupby("Publisher")[
                "Global_Sales"
            ]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(12)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            publisher_sales,
            x="Global_Sales",
            y="Publisher",
            orientation="h"
        )

        fig.update_traces(
            marker_color="#6c8cff"
        )

        fig.update_layout(
            title="Top Publishers",
            xaxis_title="Sales (Million)",
            yaxis_title=None
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # YEARLY SALES
    # --------------------------------------------------------

    yearly = (
        filtered
        .groupby("Year")[
            "Global_Sales"
        ]
        .sum()
        .reset_index()
        .dropna()
    )

    fig = px.line(
        yearly,
        x="Year",
        y="Global_Sales",
        markers=True
    )

    fig.update_traces(
        line_color=ACCENT
    )

    fig.update_layout(
        title="Sales Trend by Year",
        xaxis_title="Year",
        yaxis_title="Global Sales (Million)"
    )

    fig = apply_plotly_theme(fig)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # --------------------------------------------------------
    # TOP GAMES
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        'Best-Selling Games'
        '</div>',
        unsafe_allow_html=True
    )

    best_games = (
        filtered[
            [
                "Name",
                "Platform",
                "Genre",
                "Publisher",
                "Global_Sales"
            ]
        ]
        .sort_values(
            "Global_Sales",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        best_games,
        use_container_width=True,
        height=500
    )


# ============================================================
# GAME & ENGAGEMENT
# ============================================================

elif page == "Game & Engagement":

    st.markdown(
        '<div class="page-title">Game & Engagement</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Understand how players interact with games through ratings, '
        'plays, backlogs and wishlists.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # RATING KPIs
    # --------------------------------------------------------

    ratings = pd.to_numeric(
        games["Rating"],
        errors="coerce"
    ).dropna()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Average Rating",
        f"{ratings.mean():.2f}"
    )

    c2.metric(
        "Median Rating",
        f"{ratings.median():.2f}"
    )

    c3.metric(
        "Rated Games",
        f"{len(ratings):,}"
    )

    st.markdown("---")

    # --------------------------------------------------------
    # RATING DISTRIBUTION
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        fig = px.histogram(
            ratings,
            x=ratings,
            nbins=15
        )

        fig.update_traces(
            marker_color=ACCENT
        )

        fig.update_layout(
            title="Rating Distribution",
            xaxis_title="Rating",
            yaxis_title="Number of Games"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        if "Wishlist" in games.columns:

            wishlist = games[
                [
                    "Title",
                    "Wishlist",
                    "Rating"
                ]
            ].copy()

            wishlist["Wishlist"] = pd.to_numeric(
                wishlist["Wishlist"],
                errors="coerce"
            )

            wishlist = (
                wishlist
                .sort_values(
                    "Wishlist",
                    ascending=False
                )
                .head(10)
            )

            fig = px.bar(
                wishlist.sort_values(
                    "Wishlist"
                ),
                x="Wishlist",
                y="Title",
                orientation="h"
            )

            fig.update_traces(
                marker_color="#55d6be"
            )

            fig.update_layout(
                title="Most Wishlisted Games",
                xaxis_title="Wishlist",
                yaxis_title=None
            )

            fig = apply_plotly_theme(fig)

            st.plotly_chart(
                fig,
                use_container_width=True
            )

    # --------------------------------------------------------
    # ENGAGEMENT BY GENRE
    # --------------------------------------------------------

    engagement_cols = [
        "Plays",
        "Playing",
        "Backlogs",
        "Wishlist"
    ]

    available = [
        col
        for col in engagement_cols
        if col in games.columns
    ]

    if available and "Genres" in games.columns:

        engagement = games.copy()

        for col in available:

            engagement[col] = pd.to_numeric(
                engagement[col],
                errors="coerce"
            ).fillna(0)

        engagement[
            "Total_Engagement"
        ] = engagement[
            available
        ].sum(axis=1)

        genre_data = engagement[
            [
                "Genres",
                "Total_Engagement"
            ]
        ].dropna()

        genre_data["Genres"] = genre_data[
            "Genres"
        ].str.split(",")

        genre_data = genre_data.explode(
            "Genres"
        )

        genre_data["Genres"] = genre_data[
            "Genres"
        ].str.strip()

        genre_engagement = (
            genre_data
            .groupby("Genres")[
                "Total_Engagement"
            ]
            .mean()
            .sort_values(
                ascending=False
            )
            .head(15)
            .sort_values()
            .reset_index()
        )

        fig = px.bar(
            genre_engagement,
            x="Total_Engagement",
            y="Genres",
            orientation="h"
        )

        fig.update_traces(
            marker_color="#8b7cff"
        )

        fig.update_layout(
            title="Average Engagement by Genre",
            xaxis_title="Average Engagement",
            yaxis_title=None
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )


# ============================================================
# REGIONAL ANALYSIS
# ============================================================

elif page == "Regional Analysis":

    st.markdown(
        '<div class="page-title">Regional Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Compare video game sales across major geographic markets.'
        '</div>',
        unsafe_allow_html=True
    )

    regional = pd.DataFrame({
        "Region": [
            "North America",
            "Europe",
            "Japan",
            "Other"
        ],
        "Sales": [
            sales["NA_Sales"].sum(),
            sales["EU_Sales"].sum(),
            sales["JP_Sales"].sum(),
            sales["Other_Sales"].sum()
        ]
    })

    c1, c2, c3, c4 = st.columns(4)

    for col, row in zip(
        [c1, c2, c3, c4],
        regional.itertuples()
    ):

        col.metric(
            row.Region,
            f"{row.Sales:,.2f}M"
        )

    st.markdown("---")

    # --------------------------------------------------------
    # REGIONAL SALES
    # --------------------------------------------------------

    left, right = st.columns(2)

    with left:

        fig = px.bar(
            regional,
            x="Region",
            y="Sales"
        )

        fig.update_traces(
            marker_color=ACCENT
        )

        fig.update_layout(
            title="Sales by Region",
            xaxis_title=None,
            yaxis_title="Sales (Million)"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with right:

        fig = px.pie(
            regional,
            names="Region",
            values="Sales",
            hole=0.55
        )

        fig.update_traces(
            textfont=dict(
                color="#ffffff"
            )
        )

        fig.update_layout(
            title="Regional Sales Share"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # REGIONAL GENRE
    # --------------------------------------------------------

    regional_genre = (
        sales
        .groupby("Genre")[
            [
                "NA_Sales",
                "EU_Sales",
                "JP_Sales",
                "Other_Sales"
            ]
        ]
        .sum()
        .reset_index()
    )

    regional_genre = regional_genre.rename(
        columns={
            "NA_Sales": "North America",
            "EU_Sales": "Europe",
            "JP_Sales": "Japan",
            "Other_Sales": "Other"
        }
    )

    st.markdown(
        '<div class="section-title">'
        'Regional Genre Performance'
        '</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        regional_genre.sort_values(
            "North America",
            ascending=False
        ),
        use_container_width=True,
        height=500
    )


# ============================================================
# FORECASTING
# ============================================================

elif page == "Forecasting":

    st.markdown(
        '<div class="page-title">Sales Forecasting</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Historical sales, model evaluation and dataset-based future projection.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # HISTORICAL TREND
    # --------------------------------------------------------

    if not annual_sales.empty:

        fig = px.area(
            annual_sales,
            x="Year",
            y="Global_Sales"
        )

        fig.update_traces(
            line_color=ACCENT,
            fillcolor="rgba(77,163,255,0.16)"
        )

        fig.update_layout(
            title="Historical Annual Global Sales",
            xaxis_title="Year",
            yaxis_title="Sales (Million)"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # MODEL COMPARISON
    # --------------------------------------------------------

    if not model_comparison.empty:

        st.markdown(
            '<div class="section-title">'
            'Model Evaluation — 2011 to 2015'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            model_comparison,
            use_container_width=True,
            hide_index=True
        )

        fig = go.Figure()

        for metric in [
            "MAE",
            "RMSE"
        ]:

            fig.add_trace(
                go.Bar(
                    name=metric,
                    x=model_comparison["Model"],
                    y=model_comparison[metric]
                )
            )

        fig.update_layout(
            title="Forecasting Error Comparison",
            barmode="group",
            yaxis_title="Error (Million)"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    # --------------------------------------------------------
    # FUTURE FORECAST
    # --------------------------------------------------------

    if (
        not future_forecast.empty
        and not annual_sales.empty
    ):

        st.markdown(
            '<div class="section-title">'
            'Future Dataset-Based Projection'
            '</div>',
            unsafe_allow_html=True
        )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=annual_sales["Year"],
                y=annual_sales["Global_Sales"],
                mode="lines+markers",
                name="Historical",
                line=dict(
                    color=ACCENT,
                    width=3
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=future_forecast["Year"],
                y=future_forecast[
                    "Forecast_Global_Sales"
                ],
                mode="lines+markers",
                name="Forecast",
                line=dict(
                    color="#55d6be",
                    width=3,
                    dash="dash"
                )
            )
        )

        fig.update_layout(
            title="Historical Sales and Future Projection",
            xaxis_title="Year",
            yaxis_title="Sales (Million)"
        )

        fig = apply_plotly_theme(fig)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            future_forecast,
            use_container_width=True,
            hide_index=True
        )

        st.warning(
            "The post-2016 dataset coverage is sparse. "
            "This projection should therefore be interpreted "
            "as a dataset-based baseline rather than a "
            "real-world market forecast."
        )


# ============================================================
# ANOMALY ANALYSIS
# ============================================================

elif page == "Anomaly Analysis":

    st.markdown(
        '<div class="page-title">Anomaly Intelligence</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="page-subtitle">'
        'Explore unusual sales patterns, regional concentration '
        'and engagement-sales relationships.'
        '</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    if not anomaly_summary.empty:

        st.markdown(
            '<div class="section-title">'
            'Detection Summary'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            anomaly_summary,
            use_container_width=True,
            hide_index=True
        )

    st.markdown("---")

    # --------------------------------------------------------
    # SALES ANOMALIES
    # --------------------------------------------------------

    if not sales_anomalies.empty:

        st.markdown(
            '<div class="section-title">'
            'High Global Sales Anomalies'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            sales_anomalies.head(50),
            use_container_width=True,
            height=400
        )

    # --------------------------------------------------------
    # REGIONAL ANOMALIES
    # --------------------------------------------------------

    if not regional_anomalies.empty:

        st.markdown(
            '<div class="section-title">'
            'Regional Concentration'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            regional_anomalies.head(50),
            use_container_width=True,
            height=400
        )

    # --------------------------------------------------------
    # ENGAGEMENT / SALES ANOMALIES
    # --------------------------------------------------------

    if not engagement_anomalies.empty:

        st.markdown(
            '<div class="section-title">'
            'Engagement vs Sales'
            '</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            engagement_anomalies.head(50),
            use_container_width=True,
            height=400
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        GAMEPULSE • Video Game Sales & Engagement Intelligence
        <br>
        Data Science Capstone Project
    </div>
    """,
    unsafe_allow_html=True
)
