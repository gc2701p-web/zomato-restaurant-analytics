"""
=============================================================
  Zomato Restaurant & Cuisine Analysis
  College Project — Interactive Streamlit Dashboard
=============================================================
  Author  : Your Name
  Tech    : Python · Streamlit · Pandas · Plotly
=============================================================
"""

import os
import math
import warnings

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore")

# ──────────────────────────────────────────────────────────
# PAGE CONFIG  (must be the very first Streamlit call)
# ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Zomato Restaurant Analytics",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────────────────
# CUSTOM CSS
# ──────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ── Google Font ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Dark background ── */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
        color: #e8eaed;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a0a2e 0%, #16213e 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }
    section[data-testid="stSidebar"] .stRadio label {
        color: #ccc !important;
        font-size: 0.95rem;
        font-weight: 500;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        padding: 0.4rem 0.6rem;
        border-radius: 8px;
        transition: background 0.2s;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover {
        background: rgba(255,75,75,0.15);
    }

    /* ── Metric cards ── */
    div[data-testid="metric-container"] {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 1rem 1.2rem;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
        transition: transform 0.2s, box-shadow 0.2s;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(255,75,75,0.18);
    }
    div[data-testid="metric-container"] label {
        color: #a0aec0 !important;
        font-size: 0.82rem !important;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: #ff6b6b !important;
        font-size: 1.9rem !important;
        font-weight: 700;
    }

    /* ── Section headers ── */
    .section-header {
        font-size: 1.65rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.3rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #ff4b4b;
        display: inline-block;
    }
    .section-sub {
        font-size: 0.95rem;
        color: #a0aec0;
        margin-bottom: 1.5rem;
    }

    /* ── Chart containers ── */
    .chart-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 16px;
        padding: 1rem;
        margin-bottom: 1rem;
    }

    /* ── Tables ── */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ── Selectbox / Multiselect labels ── */
    .stSelectbox label, .stMultiSelect label, .stSlider label,
    .stTextInput label, .stNumberInput label {
        color: #cbd5e0 !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
    }

    /* ── Divider ── */
    hr {
        border-color: rgba(255,255,255,0.08);
    }

    /* ── Info / Warning boxes ── */
    .stAlert {
        border-radius: 10px;
    }

    /* ── Page hero banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #ff4b4b 0%, #e53e3e 40%, #c53030 100%);
        border-radius: 18px;
        padding: 2rem 2.5rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 40px rgba(255,75,75,0.3);
    }
    .hero-banner h1 {
        color: #fff;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
        line-height: 1.2;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.85);
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }

    /* ── About cards ── */
    .about-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-left: 4px solid #ff4b4b;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    .about-card h3 {
        color: #ff6b6b;
        margin-top: 0;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
    }
    .about-card p, .about-card li {
        color: #cbd5e0;
        font-size: 0.92rem;
        line-height: 1.6;
    }
    .about-card ul {
        padding-left: 1.2rem;
        margin: 0.4rem 0 0 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────
DATA_PATH = os.path.join("data", "processed", "cleaned_restaurants.csv")

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#cbd5e0", family="Inter"),
    title_font=dict(color="#ffffff", size=16, family="Inter"),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#cbd5e0")),
    margin=dict(t=50, b=40, l=40, r=20),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="#a0aec0"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.06)",
        zerolinecolor="rgba(255,255,255,0.1)",
        tickfont=dict(color="#a0aec0"),
    ),
)

COLOR_SEQ = px.colors.sequential.Reds_r
ACCENT = "#ff4b4b"


# ──────────────────────────────────────────────────────────
# DATA LOADING
# ──────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Loading dataset...")
def load_data(path: str) -> pd.DataFrame:
    """Load and pre-process the cleaned restaurants CSV."""
    df = pd.read_csv(path, encoding="latin1")

    # Numeric coercions
    df["aggregate_rating"] = pd.to_numeric(df["aggregate_rating"], errors="coerce")
    df["average_cost_for_two"] = pd.to_numeric(df["average_cost_for_two"], errors="coerce")
    df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    df["price_range"] = pd.to_numeric(df["price_range"], errors="coerce")

    # Clean string columns
    for col in ["city", "country", "cuisines", "currency", "rating_text", "restaurant_name"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", pd.NA)

    return df


# ──────────────────────────────────────────────────────────
# LOAD DATA  (with graceful error)
# ──────────────────────────────────────────────────────────
if not os.path.exists(DATA_PATH):
    st.error(
        f"**Dataset not found at `{DATA_PATH}`.**\n\n"
        "Please make sure `cleaned_restaurants.csv` exists inside `data/processed/`. "
        "Run your `src/clean_data.py` script first to generate the cleaned dataset."
    )
    st.stop()

df = load_data(DATA_PATH)

# ──────────────────────────────────────────────────────────
# SIDEBAR NAVIGATION
# ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style='text-align:center; padding: 1.2rem 0 1rem 0;'>
            <div style='font-size:2.6rem;'>&#127869;&#65039;</div>
            <div style='font-weight:800; font-size:1.1rem; color:#ff6b6b; line-height:1.3;'>
                Zomato Analytics
            </div>
            <div style='font-size:0.75rem; color:#718096; margin-top:0.2rem;'>
                Restaurant &amp; Cuisine Analysis
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()

    page = st.radio(
        "Navigate to",
        options=[
            "Overview",
            "Restaurant Explorer",
            "City Analysis",
            "Cuisine Analysis",
            "Rating Analysis",
            "Cost Analysis",
            "About Project",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown(
        "<div style='font-size:0.75rem; color:#4a5568; text-align:center; padding:0.5rem 0;'>"
        "Dataset: Zomato Restaurants<br>"
        f"<b style='color:#718096;'>{len(df):,} records loaded</b>"
        "</div>",
        unsafe_allow_html=True,
    )


# ──────────────────────────────────────────────────────────
# HELPER: section header
# ──────────────────────────────────────────────────────────
def section_header(title: str, subtitle: str = "") -> None:
    st.markdown(f"<div class='section-header'>{title}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div class='section-sub'>{subtitle}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════
#  PAGE 1 — OVERVIEW
# ══════════════════════════════════════════════════════════
if page == "Overview":

    st.markdown(
        """
        <div class='hero-banner'>
            <h1>&#127869;&#65039; Zomato Restaurant &amp; Cuisine Analysis</h1>
            <p>Explore restaurant trends, ratings, costs, and cuisines across cities worldwide.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KPI metrics ──────────────────────────────────────
    total_records = len(df)
    unique_ids = df["restaurant_id"].nunique()
    rated = df[df["aggregate_rating"] > 0]["aggregate_rating"]
    avg_rating = rated.mean() if len(rated) > 0 else 0
    avg_cost = df["average_cost_for_two"].dropna().mean()
    total_cities = df["city"].dropna().nunique()
    total_cuisines = (
        df["cuisines"]
        .dropna()
        .str.split(",")
        .explode()
        .str.strip()
        .nunique()
    )

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Records", f"{total_records:,}")
    c2.metric("Unique Restaurants", f"{unique_ids:,}")
    c3.metric("Avg Rating", f"{avg_rating:.2f} ⭐")
    c4.metric("Avg Cost for Two", f"{avg_cost:,.0f}")
    c5.metric("Cities", f"{total_cities:,}")
    c6.metric("Cuisine Types", f"{total_cuisines:,}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Row 1 charts ──────────────────────────────────────
    col1, col2 = st.columns(2)

    with col1:
        top_cities = (
            df.groupby("city", dropna=True)
            .size()
            .reset_index(name="count")
            .sort_values("count", ascending=False)
            .head(15)
        )
        fig = px.bar(
            top_cities,
            x="count",
            y="city",
            orientation="h",
            title="Top 15 Cities by Restaurant Count",
            color="count",
            color_continuous_scale=COLOR_SEQ,
            labels={"count": "Restaurants", "city": "City"},
        )
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=450)
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        rating_data = df[df["aggregate_rating"] > 0]["aggregate_rating"].dropna()
        fig2 = px.histogram(
            rating_data,
            nbins=30,
            title="Rating Distribution (Rated Restaurants)",
            labels={"value": "Rating", "count": "Count"},
            color_discrete_sequence=[ACCENT],
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=450, showlegend=False)
        fig2.update_traces(opacity=0.85)
        st.plotly_chart(fig2, use_container_width=True)

    # ── Row 2 charts ──────────────────────────────────────
    col3, col4 = st.columns(2)

    with col3:
        pr_labels = {1: "Budget (1)", 2: "Affordable (2)", 3: "Mid-Range (3)", 4: "Fine Dining (4)"}
        pr_counts = (
            df["price_range"]
            .dropna()
            .astype(int)
            .map(pr_labels)
            .value_counts()
            .reset_index()
        )
        pr_counts.columns = ["Price Range", "Count"]
        fig3 = px.pie(
            pr_counts,
            names="Price Range",
            values="Count",
            title="Restaurant Distribution by Price Range",
            color_discrete_sequence=px.colors.sequential.Reds,
            hole=0.45,
        )
        fig3.update_layout(**PLOTLY_LAYOUT, height=400)
        fig3.update_traces(textinfo="percent+label", textfont_color="#ffffff")
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        online_del = df["has_online_delivery"].value_counts().reset_index()
        online_del.columns = ["Status", "Count"]
        table_bk = df["has_table_booking"].value_counts().reset_index()
        table_bk.columns = ["Status", "Count"]

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            name="Online Delivery",
            x=online_del["Status"].astype(str),
            y=online_del["Count"],
            marker_color=ACCENT,
            opacity=0.85,
        ))
        fig4.add_trace(go.Bar(
            name="Table Booking",
            x=table_bk["Status"].astype(str),
            y=table_bk["Count"],
            marker_color="#4299e1",
            opacity=0.85,
        ))
        fig4.update_layout(
            **PLOTLY_LAYOUT,
            title="Online Delivery vs Table Booking",
            barmode="group",
            height=400,
        )
        st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════
#  PAGE 2 — RESTAURANT EXPLORER
# ══════════════════════════════════════════════════════════
elif page == "Restaurant Explorer":

    section_header(
        "🔍 Restaurant Explorer",
        "Search and filter through the complete restaurant database.",
    )

    # ── Filters ──────────────────────────────────────────
    with st.expander("🎛️ Filters", expanded=True):
        fc1, fc2 = st.columns(2)
        with fc1:
            search_name = st.text_input("Search by Restaurant Name", placeholder="e.g. Pizza Hut")
        with fc2:
            all_cities = sorted(df["city"].dropna().unique().tolist())
            selected_cities = st.multiselect("Filter by City", all_cities, placeholder="All cities")

        fc3, fc4, fc5 = st.columns(3)
        with fc3:
            all_cuisines = sorted(
                df["cuisines"].dropna().str.split(",").explode().str.strip().dropna().unique().tolist()
            )
            selected_cuisines = st.multiselect(
                "Filter by Cuisine", all_cuisines, placeholder="All cuisines"
            )
        with fc4:
            rating_min, rating_max = st.slider(
                "Min / Max Rating", min_value=0.0, max_value=5.0, value=(0.0, 5.0), step=0.1
            )
        with fc5:
            pr_map = {1: "Budget", 2: "Affordable", 3: "Mid-Range", 4: "Fine Dining"}
            pr_options = ["All"] + [f"{k} — {v}" for k, v in pr_map.items()]
            selected_pr = st.selectbox("Price Range", pr_options)

    # ── Apply filters ─────────────────────────────────────
    filtered = df.copy()

    if search_name:
        filtered = filtered[
            filtered["restaurant_name"].str.contains(search_name, case=False, na=False)
        ]

    if selected_cities:
        filtered = filtered[filtered["city"].isin(selected_cities)]

    if selected_cuisines:
        mask = filtered["cuisines"].apply(
            lambda x: any(c in str(x) for c in selected_cuisines) if pd.notna(x) else False
        )
        filtered = filtered[mask]

    rated_mask = (
        (filtered["aggregate_rating"] >= rating_min) &
        (filtered["aggregate_rating"] <= rating_max)
    )
    if rating_min == 0.0:
        rated_mask = rated_mask | filtered["aggregate_rating"].isna()
    filtered = filtered[rated_mask]

    if selected_pr != "All":
        pr_num = int(selected_pr.split("—")[0].strip())
        filtered = filtered[filtered["price_range"] == pr_num]

    # ── Display ───────────────────────────────────────────
    st.markdown(f"**{len(filtered):,}** restaurants match your filters.")

    PAGE_SIZE = 50
    total_pages = max(1, math.ceil(len(filtered) / PAGE_SIZE))
    pg_col1, pg_col2, pg_col3 = st.columns([1, 2, 1])
    with pg_col2:
        current_page = st.number_input(
            f"Page (1 to {total_pages})",
            min_value=1,
            max_value=total_pages,
            value=1,
            step=1,
        )

    start_idx = (current_page - 1) * PAGE_SIZE
    end_idx = start_idx + PAGE_SIZE
    page_data = filtered.iloc[start_idx:end_idx]

    display_cols = [
        "restaurant_name", "city", "cuisines",
        "aggregate_rating", "votes", "average_cost_for_two",
        "currency", "price_range", "has_online_delivery", "has_table_booking",
    ]
    existing_cols = [c for c in display_cols if c in page_data.columns]
    rename_map = {
        "restaurant_name": "Restaurant",
        "city": "City",
        "cuisines": "Cuisines",
        "aggregate_rating": "Rating",
        "votes": "Votes",
        "average_cost_for_two": "Cost for Two",
        "currency": "Currency",
        "price_range": "Price Range",
        "has_online_delivery": "Online Delivery",
        "has_table_booking": "Table Booking",
    }

    display_df = page_data[existing_cols].rename(columns=rename_map).reset_index(drop=True)
    display_df.index += 1

    st.dataframe(
        display_df.style.format({"Rating": "{:.1f}", "Cost for Two": "{:,.0f}"}),
        use_container_width=True,
        height=520,
    )
    st.caption(f"Showing rows {start_idx + 1}–{min(end_idx, len(filtered))} of {len(filtered):,}")


# ══════════════════════════════════════════════════════════
#  PAGE 3 — CITY ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "City Analysis":

    section_header(
        "🏙️ City Analysis",
        "Explore how restaurants are distributed across cities and compare average ratings.",
    )

    st.markdown("### Top 10 Cities by Restaurant Count")
    top10_count = (
        df.groupby("city", dropna=True)
        .size()
        .reset_index(name="Restaurant Count")
        .sort_values("Restaurant Count", ascending=False)
        .head(10)
    )
    fig = px.bar(
        top10_count,
        x="city",
        y="Restaurant Count",
        title="Top 10 Cities — Number of Restaurants",
        color="Restaurant Count",
        color_continuous_scale=COLOR_SEQ,
        text="Restaurant Count",
        labels={"city": "City"},
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=420)
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### Average Rating by City")
    min_rest_city = st.slider(
        "Minimum restaurants required per city", 2, 50, 5, key="city_min"
    )

    city_rating = (
        df[df["aggregate_rating"] > 0]
        .groupby("city", dropna=True)
        .agg(avg_rating=("aggregate_rating", "mean"), restaurant_count=("restaurant_id", "size"))
        .reset_index()
        .query(f"restaurant_count >= {min_rest_city}")
        .sort_values("avg_rating", ascending=False)
        .head(20)
    )

    fig2 = px.bar(
        city_rating,
        x="city",
        y="avg_rating",
        title=f"Top 20 Cities — Average Restaurant Rating (min {min_rest_city} restaurants)",
        color="avg_rating",
        color_continuous_scale="RdYlGn",
        text=city_rating["avg_rating"].round(2),
        hover_data={"restaurant_count": True},
        labels={"city": "City", "avg_rating": "Avg Rating", "restaurant_count": "Count"},
    )
    fig2.update_traces(texttemplate="%{text}", textposition="outside")
    fig2.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True, height=420, yaxis_range=[0, 5.5])
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("### City Overview — Count vs Average Rating")
    city_overview = (
        df[df["aggregate_rating"] > 0]
        .groupby("city", dropna=True)
        .agg(
            avg_rating=("aggregate_rating", "mean"),
            restaurant_count=("restaurant_id", "size"),
        )
        .reset_index()
        .query("restaurant_count >= 3")
    )

    fig3 = px.scatter(
        city_overview,
        x="restaurant_count",
        y="avg_rating",
        size="restaurant_count",
        color="avg_rating",
        hover_name="city",
        color_continuous_scale="RdYlGn",
        title="Cities — Restaurant Count vs Average Rating",
        labels={"restaurant_count": "Number of Restaurants", "avg_rating": "Average Rating"},
        size_max=50,
    )
    fig3.update_layout(**PLOTLY_LAYOUT, height=480)
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════
#  PAGE 4 — CUISINE ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "Cuisine Analysis":

    section_header(
        "🍜 Cuisine Analysis",
        "Discover popular cuisine types, their restaurant counts, and ratings.",
    )

    @st.cache_data(show_spinner=False)
    def build_cuisine_df(raw: pd.DataFrame) -> pd.DataFrame:
        exploded = raw.dropna(subset=["cuisines"]).copy()
        exploded["cuisine"] = exploded["cuisines"].str.split(",")
        exploded = exploded.explode("cuisine")
        exploded["cuisine"] = exploded["cuisine"].str.strip()
        exploded = exploded[exploded["cuisine"].notna() & (exploded["cuisine"] != "")]
        return exploded

    cuisine_df = build_cuisine_df(df)

    st.markdown("### Top Cuisines by Restaurant Count")
    top_n = st.slider("Number of cuisines to display", 5, 30, 20, key="cuisine_topn")

    cuisine_count = (
        cuisine_df.groupby("cuisine")
        .size()
        .reset_index(name="Restaurant Count")
        .sort_values("Restaurant Count", ascending=False)
        .head(top_n)
    )

    fig = px.bar(
        cuisine_count,
        x="Restaurant Count",
        y="cuisine",
        orientation="h",
        title=f"Top {top_n} Cuisines by Number of Restaurants",
        color="Restaurant Count",
        color_continuous_scale=COLOR_SEQ,
        text="Restaurant Count",
        labels={"cuisine": "Cuisine"},
    )
    fig.update_traces(texttemplate="%{text:,}", textposition="outside")
    fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=max(420, top_n * 24))
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### Top Cuisines by Average Rating")
    min_rest_cuis = st.slider("Min restaurants to qualify", 2, 50, 10, key="cuisine_minrest")

    cuisine_rating = (
        cuisine_df[cuisine_df["aggregate_rating"] > 0]
        .groupby("cuisine")
        .agg(avg_rating=("aggregate_rating", "mean"), restaurant_count=("restaurant_id", "size"))
        .reset_index()
        .query(f"restaurant_count >= {min_rest_cuis}")
        .sort_values("avg_rating", ascending=False)
        .head(20)
    )

    fig2 = px.bar(
        cuisine_rating,
        x="cuisine",
        y="avg_rating",
        title=f"Top 20 Cuisines by Average Rating (min {min_rest_cuis} restaurants)",
        color="avg_rating",
        color_continuous_scale="RdYlGn",
        text=cuisine_rating["avg_rating"].round(2),
        hover_data={"restaurant_count": True},
        labels={"cuisine": "Cuisine", "avg_rating": "Avg Rating"},
    )
    fig2.update_traces(texttemplate="%{text}", textposition="outside")
    fig2.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True, height=420, yaxis_range=[0, 5.5])
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("### 🔎 Cuisine Drill-Down")
    all_cuisine_names = sorted(cuisine_df["cuisine"].dropna().unique().tolist())
    selected_cuisine = st.selectbox("Select a Cuisine", all_cuisine_names)

    sub = cuisine_df[cuisine_df["cuisine"] == selected_cuisine]
    rated_sub = sub[sub["aggregate_rating"] > 0]["aggregate_rating"]

    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("Restaurants", f"{len(sub):,}")
    kc2.metric("Avg Rating", f"{rated_sub.mean():.2f} ⭐" if len(rated_sub) > 0 else "N/A")
    kc3.metric("Total Votes", f"{sub['votes'].sum():,}")
    kc4.metric("Cities Present In", f"{sub['city'].nunique():,}")

    top_cities_cuisine = (
        sub.groupby("city", dropna=True)
        .size()
        .reset_index(name="Count")
        .sort_values("Count", ascending=False)
        .head(10)
    )
    fig3 = px.bar(
        top_cities_cuisine,
        x="Count",
        y="city",
        orientation="h",
        title=f"Top Cities Serving '{selected_cuisine}'",
        color="Count",
        color_continuous_scale=COLOR_SEQ,
        labels={"city": "City", "Count": "Restaurants"},
    )
    fig3.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=350)
    fig3.update_yaxes(autorange="reversed")
    st.plotly_chart(fig3, use_container_width=True)


# ══════════════════════════════════════════════════════════
#  PAGE 5 — RATING ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "Rating Analysis":

    section_header(
        "⭐ Rating Analysis",
        "Deep dive into restaurant ratings across cities, cuisines, and rating categories.",
    )

    st.markdown("### Rating Category Breakdown")

    rating_cat = df["rating_text"].value_counts().reset_index()
    rating_cat.columns = ["Rating Category", "Count"]

    cat_color_map = {
        "Excellent": "#48bb78",
        "Very Good": "#68d391",
        "Good": "#f6e05e",
        "Average": "#f6ad55",
        "Poor": "#fc8181",
        "Not rated": "#a0aec0",
    }

    fig = px.pie(
        rating_cat,
        names="Rating Category",
        values="Count",
        title="Distribution of Rating Categories",
        color="Rating Category",
        color_discrete_map=cat_color_map,
        hole=0.42,
    )
    fig.update_layout(**PLOTLY_LAYOUT, height=420)
    fig.update_traces(textinfo="percent+label", textfont_color="#ffffff")
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("### Numeric Rating Distribution")
    col1, col2 = st.columns(2)

    with col1:
        rated_only = df[df["aggregate_rating"] > 0]["aggregate_rating"].dropna()
        fig2 = px.histogram(
            rated_only,
            nbins=25,
            title="Rated Restaurants (rating > 0)",
            color_discrete_sequence=[ACCENT],
            labels={"value": "Rating"},
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=360, showlegend=False)
        fig2.update_traces(opacity=0.85)
        st.plotly_chart(fig2, use_container_width=True)

    with col2:
        unrated_count = int((df["aggregate_rating"] == 0).sum()) + int(df["aggregate_rating"].isna().sum())
        rated_count = int((df["aggregate_rating"] > 0).sum())
        fig3 = go.Figure(go.Pie(
            labels=["Rated (> 0)", "Unrated / Missing"],
            values=[rated_count, unrated_count],
            hole=0.5,
            marker_colors=["#48bb78", "#4a5568"],
            textinfo="percent+label",
            textfont_color="#ffffff",
        ))
        fig3.update_layout(**PLOTLY_LAYOUT, title="Rated vs Unrated Restaurants", height=360)
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    st.markdown("### Average Rating by City (Top 15)")
    city_avg = (
        df[df["aggregate_rating"] > 0]
        .groupby("city", dropna=True)["aggregate_rating"]
        .agg(["mean", "count"])
        .reset_index()
        .rename(columns={"mean": "Avg Rating", "count": "Count"})
        .query("Count >= 5")
        .sort_values("Avg Rating", ascending=False)
        .head(15)
    )

    fig4 = px.bar(
        city_avg,
        x="city",
        y="Avg Rating",
        title="Top 15 Cities — Average Rating (min 5 restaurants)",
        color="Avg Rating",
        color_continuous_scale="RdYlGn",
        text=city_avg["Avg Rating"].round(2),
        hover_data={"Count": True},
        labels={"city": "City"},
    )
    fig4.update_traces(texttemplate="%{text}", textposition="outside")
    fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=True, height=420, yaxis_range=[0, 5.5])
    st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    st.markdown("### Rating Score Spread by Category")
    order = ["Excellent", "Very Good", "Good", "Average", "Poor"]
    box_data = df[df["aggregate_rating"] > 0].dropna(subset=["rating_text"])
    box_data = box_data[box_data["rating_text"].isin(order)]

    fig5 = px.box(
        box_data,
        x="rating_text",
        y="aggregate_rating",
        category_orders={"rating_text": order},
        title="Rating Score Distribution per Category",
        color="rating_text",
        color_discrete_map=cat_color_map,
        labels={"rating_text": "Category", "aggregate_rating": "Rating Score"},
    )
    fig5.update_layout(**PLOTLY_LAYOUT, height=400, showlegend=False)
    st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════
#  PAGE 6 — COST ANALYSIS
# ══════════════════════════════════════════════════════════
elif page == "Cost Analysis":

    section_header(
        "💰 Cost Analysis",
        "Analyse average restaurant costs by price range and explore the cost-rating relationship. "
        "Costs are grouped by currency to ensure meaningful comparisons.",
    )

    # Currency selector (costs must not be mixed across currencies)
    all_currencies = sorted(df["currency"].dropna().unique().tolist())
    selected_currency = st.selectbox(
        "Select Currency  (costs are NOT comparable across currencies)",
        all_currencies,
        index=0,
    )

    cur_df = df[df["currency"] == selected_currency].copy()

    if cur_df.empty:
        st.warning("No data available for the selected currency.")
        st.stop()

    kc1, kc2, kc3 = st.columns(3)
    kc1.metric("Restaurants", f"{len(cur_df):,}")
    kc2.metric(
        "Avg Cost for Two",
        f"{cur_df['average_cost_for_two'].mean():,.0f} ({selected_currency})"
        if cur_df["average_cost_for_two"].notna().any() else "N/A"
    )
    kc3.metric(
        "Avg Rating",
        f"{cur_df[cur_df['aggregate_rating'] > 0]['aggregate_rating'].mean():.2f} ⭐"
        if cur_df[cur_df["aggregate_rating"] > 0]["aggregate_rating"].count() > 0 else "N/A"
    )

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Avg Cost for Two by Price Range")
        pr_labels_map = {1: "1 - Budget", 2: "2 - Affordable", 3: "3 - Mid-Range", 4: "4 - Fine Dining"}
        cost_pr = cur_df.dropna(subset=["price_range", "average_cost_for_two"]).copy()
        cost_pr["Price Range Label"] = cost_pr["price_range"].astype(int).map(pr_labels_map)
        cost_pr_agg = (
            cost_pr.groupby("Price Range Label")["average_cost_for_two"]
            .mean()
            .reset_index()
            .rename(columns={"average_cost_for_two": "Avg Cost"})
            .sort_values("Price Range Label")
        )

        fig = px.bar(
            cost_pr_agg,
            x="Price Range Label",
            y="Avg Cost",
            title=f"Avg Cost for Two by Price Range ({selected_currency})",
            color="Avg Cost",
            color_continuous_scale=COLOR_SEQ,
            text=cost_pr_agg["Avg Cost"].round(0),
            labels={"Price Range Label": "Price Range", "Avg Cost": f"Avg Cost ({selected_currency})"},
        )
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
        fig.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=380)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Cost Distribution by Price Range")
        box_cost = cur_df.dropna(subset=["price_range", "average_cost_for_two"]).copy()
        box_cost["Price Range Label"] = box_cost["price_range"].astype(int).map(pr_labels_map)
        order_pr = ["1 - Budget", "2 - Affordable", "3 - Mid-Range", "4 - Fine Dining"]

        fig2 = px.box(
            box_cost,
            x="Price Range Label",
            y="average_cost_for_two",
            category_orders={"Price Range Label": order_pr},
            title=f"Cost Distribution by Price Range ({selected_currency})",
            color="Price Range Label",
            color_discrete_sequence=px.colors.sequential.Reds,
            labels={"average_cost_for_two": f"Cost for Two ({selected_currency})", "Price Range Label": ""},
        )
        fig2.update_layout(**PLOTLY_LAYOUT, height=380, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    st.markdown("#### Cost vs Rating Scatter Plot")
    scatter_df = cur_df[cur_df["aggregate_rating"] > 0].dropna(
        subset=["average_cost_for_two", "aggregate_rating"]
    ).copy()

    if scatter_df.empty:
        st.info("Not enough rated restaurants in the selected currency to plot.")
    else:
        cost_cap = scatter_df["average_cost_for_two"].quantile(0.99)
        scatter_df = scatter_df[scatter_df["average_cost_for_two"] <= cost_cap]

        fig3 = px.scatter(
            scatter_df,
            x="average_cost_for_two",
            y="aggregate_rating",
            color="rating_text",
            size="votes",
            hover_name="restaurant_name",
            hover_data={"city": True, "cuisines": True, "votes": True},
            title=f"Cost for Two vs Rating ({selected_currency}) — bubble size = votes",
            labels={
                "average_cost_for_two": f"Cost for Two ({selected_currency})",
                "aggregate_rating": "Rating",
                "rating_text": "Category",
            },
            color_discrete_sequence=px.colors.qualitative.Set2,
            opacity=0.7,
            size_max=25,
        )
        fig3.update_layout(**PLOTLY_LAYOUT, height=500)
        st.plotly_chart(fig3, use_container_width=True)

        corr = scatter_df[["average_cost_for_two", "aggregate_rating"]].corr().iloc[0, 1]
        st.info(
            f"📊 **Pearson correlation** between cost and rating for *{selected_currency}* "
            f"restaurants: **{corr:.3f}**  \n"
            "*(values closer to +1 mean higher cost tends to associate with higher ratings)*"
        )

    st.divider()

    st.markdown("#### Avg Cost for Two by City (Top 15)")
    city_cost = (
        cur_df.dropna(subset=["city", "average_cost_for_two"])
        .groupby("city")["average_cost_for_two"]
        .mean()
        .reset_index()
        .rename(columns={"average_cost_for_two": "Avg Cost"})
        .sort_values("Avg Cost", ascending=False)
        .head(15)
    )

    fig4 = px.bar(
        city_cost,
        x="city",
        y="Avg Cost",
        title=f"Top 15 Cities — Avg Cost for Two ({selected_currency})",
        color="Avg Cost",
        color_continuous_scale=COLOR_SEQ,
        text=city_cost["Avg Cost"].round(0),
        labels={"city": "City", "Avg Cost": f"Avg Cost ({selected_currency})"},
    )
    fig4.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig4.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, height=380)
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════
#  PAGE 7 — ABOUT PROJECT
# ══════════════════════════════════════════════════════════
elif page == "About Project":

    st.markdown(
        """
        <div class='hero-banner'>
            <h1>📄 About This Project</h1>
            <p>Zomato Restaurant &amp; Cuisine Analysis Using Python and Power BI</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown("""
        <div class='about-card'>
            <h3>🎯 Project Introduction</h3>
            <p>
                This project presents an in-depth analysis of restaurant data sourced from
                the Zomato platform. The goal is to uncover meaningful patterns in restaurant
                distribution, cuisine popularity, customer ratings, and pricing across multiple
                cities and countries.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='about-card'>
            <h3>❓ Problem Statement</h3>
            <p>
                With thousands of restaurants listed across diverse geographies, it is
                difficult for stakeholders — customers, food-tech companies, and restaurant
                owners — to quickly identify trends in ratings, popular cuisines, and
                pricing. This project addresses those challenges through systematic data
                analysis and interactive visualisations.
            </p>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='about-card'>
            <h3>🎯 Objectives</h3>
            <ul>
                <li>Perform exploratory data analysis (EDA) on the Zomato dataset.</li>
                <li>Identify the top cities and cuisines by restaurant count and ratings.</li>
                <li>Analyse the relationship between cost and customer ratings.</li>
                <li>Examine online delivery and table booking availability trends.</li>
                <li>Build interactive visualisations using Plotly and a Power BI dashboard.</li>
                <li>Deploy findings through a professional Streamlit web application.</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class='about-card'>
            <h3>🛠️ Technologies Used</h3>
            <ul>
                <li><b>Python 3.x</b> — core language for data processing and analysis</li>
                <li><b>Pandas</b> — data wrangling and transformation</li>
                <li><b>Plotly</b> — interactive, publication-quality charts</li>
                <li><b>Streamlit</b> — rapid deployment of the web dashboard</li>
                <li><b>Power BI</b> — business intelligence dashboard (.pbix)</li>
                <li><b>NumPy</b> — numerical operations</li>
                <li><b>Matplotlib / Seaborn</b> — static exploratory plots</li>
            </ul>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='about-card'>
            <h3>🔬 Methodology</h3>
            <ul>
                <li><b>Data Collection</b> — Raw Zomato dataset (zomato1.csv)</li>
                <li><b>Data Cleaning</b> — Handled missing values, standardised column types,
                    removed duplicates (src/clean_data.py)</li>
                <li><b>Exploration</b> — Univariate and bivariate analysis
                    (src/explore_data.py)</li>
                <li><b>Analysis</b> — City, cuisine, cost, and rating insights
                    (src/analyze_data.py)</li>
                <li><b>Visualisation</b> — Plotly interactive charts embedded in Streamlit</li>
                <li><b>Dashboard</b> — Power BI report for executive summary</li>
            </ul>
        </div>""", unsafe_allow_html=True)

        st.markdown("""
        <div class='about-card'>
            <h3>✅ Testing and Expected Outcomes</h3>
            <ul>
                <li>All filters in the Restaurant Explorer produce correct, consistent results.</li>
                <li>Charts render with real data — no placeholder or synthetic values.</li>
                <li>Cost comparisons are always scoped to a single currency.</li>
                <li>Missing or unrated restaurants are clearly identified, not omitted silently.</li>
                <li>Expected outcome: actionable insights into restaurant quality, pricing
                    strategies, and cuisine trends for business or academic use.</li>
            </ul>
        </div>""", unsafe_allow_html=True)

    st.divider()

    st.markdown("### 📊 Dataset at a Glance")
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Total Rows", f"{len(df):,}")
    d2.metric("Unique Restaurants", f"{df['restaurant_id'].nunique():,}")
    d3.metric("Countries", f"{df['country'].nunique()}")
    d4.metric("Cities", f"{df['city'].nunique():,}")
    d5.metric("Columns", f"{len(df.columns)}")

    st.markdown("#### Column Reference")
    col_info = {
        "restaurant_id": "Unique numeric identifier for each restaurant listing",
        "restaurant_name": "Name of the restaurant",
        "country": "Country where the restaurant is located",
        "city": "City where the restaurant is located",
        "address": "Full street address",
        "locality": "Neighbourhood / locality name",
        "locality_verbose": "Extended locality description",
        "longitude": "Geographic longitude coordinate",
        "latitude": "Geographic latitude coordinate",
        "cuisines": "Comma-separated list of cuisines served",
        "average_cost_for_two": "Average dining cost for two people (in local currency)",
        "currency": "Currency applicable to the cost figure",
        "has_table_booking": "Whether table booking is available (Yes/No)",
        "has_online_delivery": "Whether online delivery is available (Yes/No)",
        "is_delivering_now": "Real-time delivery availability flag",
        "switch_to_order_menu": "Flag to switch to order menu",
        "price_range": "Price tier (1=Budget, 2=Affordable, 3=Mid-Range, 4=Fine Dining)",
        "aggregate_rating": "Aggregate customer rating (0-5 scale; 0 = unrated)",
        "rating_color": "Colour code associated with the rating",
        "rating_text": "Textual label for the rating (e.g. Excellent, Good, Average)",
        "votes": "Total number of customer votes/reviews",
    }
    col_df = pd.DataFrame([{"Column": k, "Description": v} for k, v in col_info.items()])
    st.dataframe(col_df, use_container_width=True, hide_index=True, height=500)
