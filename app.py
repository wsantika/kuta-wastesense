"""
Kuta WasteSense AI — Streamlit Dashboard
From Reactive Cleanup to Predictive Waste Planning
"""

import os, sys, math
from datetime import datetime, timedelta

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Ensure project root is on sys.path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.utils import (
    ZONES, FEATURE_COLS, DAY_TYPES, WEATHER_CONDITIONS,
    EVENT_TYPES, SEASONS, MODEL_PATH, DATASET_PATH,
)
from src.recommender import get_recommendations, generate_executive_summary

# ══════════════════════════════════════════════════════════════════════════════
# Page config
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Kuta WasteSense AI",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# Custom CSS for polished look
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
    /* ── Global ──────────────────────────────────────────────────────────── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── Header area ─────────────────────────────────────────────────────── */
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #00b894, #00cec9, #0984e3);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }
    .hero-tagline {
        font-size: 1.05rem;
        color: #636e72;
        margin-top: -4px;
        margin-bottom: 6px;
    }
    .badge-mvp {
        display: inline-block;
        padding: 4px 14px;
        border-radius: 20px;
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        color: #fff;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* ── Metric cards ────────────────────────────────────────────────────── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #dfe6e9 0%, #f5f6fa 100%);
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    div[data-testid="stMetric"] label {
        font-weight: 600 !important;
        color: #2d3436 !important;
    }

    /* ── Risk badges ─────────────────────────────────────────────────────── */
    .risk-low    { color: #00b894; font-weight: 700; font-size: 1.3rem; }
    .risk-medium { color: #fdcb6e; font-weight: 700; font-size: 1.3rem; }
    .risk-high   { color: #d63031; font-weight: 700; font-size: 1.3rem; }

    /* ── Sidebar ─────────────────────────────────────────────────────────── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0c2340 0%, #163a5f 100%);
    }
    section[data-testid="stSidebar"] * {
        color: #dfe6e9 !important;
    }
    section[data-testid="stSidebar"] .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #00b894, #00cec9);
        color: #fff !important;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        font-size: 1rem;
        padding: 0.6rem 0;
        transition: transform 0.15s;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        transform: scale(1.03);
    }

    /* ── Divider ─────────────────────────────────────────────────────────── */
    .section-divider {
        border: none;
        border-top: 2px solid #b2bec3;
        margin: 1.5rem 0;
    }

    /* ── Summary box ─────────────────────────────────────────────────────── */
    .summary-box {
        background: linear-gradient(135deg, #dfe6e9 0%, #f5f6fa 100%);
        border-left: 5px solid #0984e3;
        border-radius: 10px;
        padding: 18px 22px;
        font-size: 0.97rem;
        line-height: 1.65;
        color: #2d3436;
    }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# Load model & data
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_dataset():
    return pd.read_csv(DATASET_PATH, parse_dates=["date"])


model = load_model()
df = load_dataset()

# ══════════════════════════════════════════════════════════════════════════════
# Header
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<p class="hero-title">♻️ Kuta WasteSense AI</p>', unsafe_allow_html=True)
st.markdown('<p class="hero-tagline">From Reactive Cleanup to Predictive Waste Planning</p>', unsafe_allow_html=True)
st.markdown('<span class="badge-mvp">🏗️ MVP Prototype — Synthetic Data</span>', unsafe_allow_html=True)
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Sidebar – Input form
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("### 📋 Prediction Input")
    st.caption("Configure scenario parameters below")

    zone = st.selectbox("🗺️ Zone", ZONES, index=0)
    pred_date = st.date_input("📅 Prediction Date", value=datetime.today())
    day_type = st.selectbox("📆 Day Type", DAY_TYPES, index=0)
    weather = st.selectbox("🌤️ Weather Condition", WEATHER_CONDITIONS, index=0)
    rainfall = st.slider("🌧️ Rainfall (mm)", 0.0, 80.0, 0.0, 0.5)
    event = st.selectbox("🎪 Event Type", EVENT_TYPES, index=0)
    visitors = st.number_input("👥 Estimated Visitors", 100, 20000, 2000, 100)
    season = st.selectbox("🏖️ Season", SEASONS, index=0)
    bin_avail = st.slider("🗑️ Bin Availability", 5, 40, 18)
    prev_waste = st.number_input("📦 Previous Waste (kg)", 50.0, 8000.0, 500.0, 50.0)

    run = st.button("🚀 Run Prediction", width="stretch")


# ══════════════════════════════════════════════════════════════════════════════
# Prediction logic
# ══════════════════════════════════════════════════════════════════════════════
def predict(zone, pred_date, day_type, weather, rainfall, event, visitors, season, bin_avail, prev_waste):
    dow = pred_date.weekday()
    is_weekend = int(day_type == "Weekend")
    is_holiday = int(day_type == "Public Holiday")

    input_df = pd.DataFrame([{
        "zone": zone,
        "day_of_week": dow,
        "is_weekend": is_weekend,
        "is_holiday": is_holiday,
        "weather_condition": weather,
        "rainfall_mm": rainfall,
        "event_type": event,
        "estimated_visitors": visitors,
        "season": season,
        "bin_availability": bin_avail,
        "previous_waste_kg": prev_waste,
    }])

    predicted = model.predict(input_df[FEATURE_COLS])[0]
    return max(predicted, 0)


if run:
    predicted_kg = predict(zone, pred_date, day_type, weather, rainfall, event, visitors, season, bin_avail, prev_waste)
    rec = get_recommendations(predicted_kg)
    summary = generate_executive_summary(zone, predicted_kg, weather, event, visitors, rec)

    # ── Risk colour helper ────────────────────────────────────────────────
    risk_cls = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high"}
    risk_emoji = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}

    # ── KPI cards ─────────────────────────────────────────────────────────
    st.markdown("## 📊 Prediction Results")
    k1, k2, k3 = st.columns(3)
    k1.metric("🗑️ Predicted Waste", f"{predicted_kg:,.0f} kg")
    k2.markdown(
        f"**Risk Level**<br><span class='{risk_cls[rec['risk_level']]}'>"
        f"{risk_emoji[rec['risk_level']]} {rec['risk_level']}</span>",
        unsafe_allow_html=True,
    )
    k3.metric("📅 Collection Schedule", rec["collection_schedule"])

    r1, r2, r3 = st.columns(3)
    r1.metric("👷 Recommended Staff", rec["recommended_staff"])
    r2.metric("🗑️ Recommended Bins", rec["recommended_bins"])
    r3.metric("🚛 Recommended Trucks", rec["recommended_trucks"])

    # ── Executive summary ─────────────────────────────────────────────────
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
    st.markdown("### 📝 Executive Summary")
    st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)

    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# Analytics section (always visible)
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📈 Waste Analytics")

tab1, tab2, tab3 = st.tabs(["🏖️ By Zone", "📅 7-Day Trend", "🔄 Scenario Comparison"])

# ── Tab 1: Average waste by zone ──────────────────────────────────────────────
with tab1:
    zone_avg = df.groupby("zone")["waste_volume_kg"].mean().reset_index()
    zone_avg.columns = ["Zone", "Avg Waste (kg)"]
    zone_avg = zone_avg.sort_values("Avg Waste (kg)", ascending=True)

    fig_zone = px.bar(
        zone_avg, x="Avg Waste (kg)", y="Zone", orientation="h",
        color="Avg Waste (kg)",
        color_continuous_scale=["#00b894", "#fdcb6e", "#d63031"],
        title="Average Waste Volume by Zone",
    )
    fig_zone.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        height=380,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig_zone, width="stretch")

# ── Tab 2: 7-day trend ──────────────────────────────────────────────────────
with tab2:
    last_7 = df.sort_values("date").groupby("date")["waste_volume_kg"].sum().reset_index().tail(30)
    last_7.columns = ["Date", "Total Waste (kg)"]

    fig_trend = px.area(
        last_7, x="Date", y="Total Waste (kg)",
        title="Daily Total Waste Volume (Last 30 Days)",
        color_discrete_sequence=["#0984e3"],
    )
    fig_trend.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter"),
        height=380,
    )
    fig_trend.update_traces(
        fill="tozeroy",
        fillcolor="rgba(9,132,227,0.15)",
        line=dict(width=2.5),
    )
    st.plotly_chart(fig_trend, width="stretch")

# ── Tab 3: Scenario comparison ────────────────────────────────────────────────
with tab3:
    st.markdown("#### Scenario Comparison Table")
    st.caption("Predictions for Beachwalk Area under three typical scenarios")

    scenarios = [
        {
            "Scenario": "🌤️ Normal Weekday",
            "zone": "Beachwalk Area", "day_type": "Weekday",
            "weather": "Sunny", "rainfall": 0.0, "event": "None",
            "visitors": 1800, "season": "Dry Season",
            "bin_avail": 20, "prev_waste": 500.0,
        },
        {
            "Scenario": "🌧️ Rainy Weekend",
            "zone": "Beachwalk Area", "day_type": "Weekend",
            "weather": "Rainy", "rainfall": 15.0, "event": "None",
            "visitors": 3200, "season": "Wet Season",
            "bin_avail": 15, "prev_waste": 700.0,
        },
        {
            "Scenario": "🎉 Major Event Day",
            "zone": "Beachwalk Area", "day_type": "Public Holiday",
            "weather": "Cloudy", "rainfall": 1.0, "event": "Music Concert",
            "visitors": 8000, "season": "Peak Tourist Season",
            "bin_avail": 10, "prev_waste": 1200.0,
        },
    ]

    rows = []
    for s in scenarios:
        p = predict(
            s["zone"], datetime.today(), s["day_type"],
            s["weather"], s["rainfall"], s["event"],
            s["visitors"], s["season"], s["bin_avail"], s["prev_waste"],
        )
        r = get_recommendations(p)
        rows.append({
            "Scenario": s["Scenario"],
            "Predicted Waste (kg)": f"{p:,.0f}",
            "Risk Level": r["risk_level"],
            "Staff": r["recommended_staff"],
            "Bins": r["recommended_bins"],
            "Trucks": r["recommended_trucks"],
            "Schedule": r["collection_schedule"],
        })

    st.dataframe(pd.DataFrame(rows), width="stretch", hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:#b2bec3; font-size:0.82rem;'>"
    "Kuta WasteSense AI · MVP Prototype · Synthetic Data Only · "
    "Not official DLH/DLHK Badung operational data"
    "</div>",
    unsafe_allow_html=True,
)
