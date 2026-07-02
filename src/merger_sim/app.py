"""
Streamlit Web Dashboard for the Merger Simulation Toolkit.
"""

import streamlit as st
import pandas as pd
from merger_sim.simulation import simulate_merger

st.set_page_config(page_title="HHI Simulator", page_icon="📊", layout="wide")

# Sidebar
with st.sidebar:
    st.header("🧰 Toolkit")
    if st.button("Load AT&T/T-Mobile Case Study"):
        st.session_state["df"] = pd.DataFrame(
            {
                "Firm": ["AT&T", "Verizon", "T-Mobile", "Sprint", "Others"],
                "Market_Share": [29.0, 31.0, 11.0, 16.0, 13.0],
            }
        )
    st.markdown("---")
    st.markdown("**Regulatory Risk Thresholds:**")
    st.markdown("🟩 **Safe:** HHI < 1500 or Delta < 100")
    st.markdown("🟨 **Moderate:** HHI 1500-2500 & Delta > 100")
    st.markdown("🟥 **High Risk:** HHI > 2500 & Delta > 200")
    st.markdown(
        "[View Case Study Notebook](https://github.com/thanhan25/merger-simulation-hhi-analyzer/blob/main/notebooks/historical_case_study.ipynb)"
    )

st.title("📊 Merger Simulation & Concentration Analyzer")

# State Management
if "df" not in st.session_state:
    st.session_state["df"] = None

col1, col2 = st.columns([1, 2])

with col1:
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
    if uploaded_file:
        st.session_state["df"] = pd.read_csv(uploaded_file)

    df = st.session_state["df"]
    if df is not None:
        st.dataframe(df, use_container_width=True)
        firms = df["Firm"].tolist()
        acquirer = st.selectbox("Acquiring Firm", firms)
        target = st.selectbox("Target Firm", [f for f in firms if f != acquirer])
        run_sim = st.button("Run Simulation", type="primary", use_container_width=True)

with col2:
    if df is not None and "run_sim" in locals() and run_sim:
        scenario = simulate_merger(df, "Firm", "Market_Share", acquirer, target)

        m1, m2, m3 = st.columns(3)
        m1.metric("Pre-Merger HHI", f"{scenario.pre_hhi:,.2f}")
        m2.metric(
            "Post-Merger HHI",
            f"{scenario.post_hhi:,.2f}",
            delta=f"+{scenario.delta:,.2f}",
            delta_color="inverse",
        )
        m3.metric("Concentration", scenario.concentration_level)

        if "High Risk" in scenario.regulatory_risk:
            st.error(f"🚨 {scenario.regulatory_risk}")
        else:
            st.success(f"✅ {scenario.regulatory_risk}")
