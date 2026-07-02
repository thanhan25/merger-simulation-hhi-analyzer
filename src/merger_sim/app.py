"""
Streamlit Web Dashboard for the Merger Simulation Toolkit.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from merger_sim.simulation import simulate_merger

# 1. Page Configuration & Custom CSS
st.set_page_config(
    page_title="Antitrust Simulator",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    /* Clean up the UI by hiding Streamlit branding and tightening padding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}
    /* Enhance metric card visibility */
    div[data-testid="metric-container"] {
        background-color: #1e1e1e;
        border: 1px solid #333;
        padding: 5% 5% 5% 10%;
        border-radius: 5px;
        box-shadow: 0 0.15rem 1.75rem 0 rgba(0, 0, 0, 0.15);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 2. Sidebar Setup
with st.sidebar:
    st.header("🧰 Toolkit")
    if st.button("Load AT&T/T-Mobile Case Study", use_container_width=True):
        st.session_state["df"] = pd.DataFrame(
            {
                "Firm": ["AT&T", "Verizon", "T-Mobile", "Sprint", "Others"],
                "Market_Share": [29.0, 31.0, 11.0, 16.0, 13.0],
            }
        )
    st.markdown("---")
    st.markdown("**DOJ/FTC Regulatory Thresholds:**")
    st.markdown("🟩 **Safe:** HHI < 1500 or $\Delta$ < 100")
    st.markdown("🟨 **Moderate:** HHI 1500-2500 & $\Delta$ > 100")
    st.markdown("🟥 **High Risk:** HHI > 2500 & $\Delta$ > 200")
    st.markdown(
        "[View Full Case Study Notebook](https://github.com/thanhan25/merger-simulation-hhi-analyzer/blob/main/notebooks/historical_case_study.ipynb)"
    )

# 3. Main Header
st.title("⚖️ Merger Simulation & Market Concentration Analyzer")
st.markdown(
    "Upload market data below to instantly simulate horizontal mergers and calculate HHI antitrust metrics based on U.S. DOJ Horizontal Merger Guidelines."
)

if "df" not in st.session_state:
    st.session_state["df"] = None

# 4. Top Input Section (Full Width)
with st.container():
    col_upload, col_params = st.columns([1, 1], gap="large")

    with col_upload:
        uploaded_file = st.file_uploader(
            "Upload Market Data (CSV)",
            type=["csv"],
            help="CSV must contain 'Firm' and 'Market_Share' columns.",
        )
        if uploaded_file:
            st.session_state["df"] = pd.read_csv(uploaded_file)

    df = st.session_state["df"]

    with col_params:
        if df is not None:
            firms = df["Firm"].tolist()
            acquirer = st.selectbox("Select Acquiring Firm", firms)
            target = st.selectbox(
                "Select Target Firm", [f for f in firms if f != acquirer]
            )
            run_sim = st.button(
                "Execute Merger Simulation", type="primary", use_container_width=True
            )
        else:
            st.info(
                "👈 Please upload a CSV file or load the Case Study from the sidebar to begin."
            )

st.divider()

# 5. Output Section
if df is not None and "run_sim" in locals() and run_sim:
    try:
        # Execute Core Engine
        scenario = simulate_merger(df, "Firm", "Market_Share", acquirer, target)

        # --- A. Executive Metric Cards ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Pre-Merger HHI", f"{scenario.pre_hhi:,.1f}")
        m2.metric(
            "Post-Merger HHI",
            f"{scenario.post_hhi:,.1f}",
            delta=f"+{scenario.delta:,.1f}",
            delta_color="inverse",
        )
        m3.metric("Concentration Level", scenario.concentration_level)
        m4.metric("Regulatory Target", f"{target}")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- B. Regulatory Alert Banner ---
        if "High Risk" in scenario.regulatory_risk:
            st.error(f"🚨 **Regulatory Alert:** {scenario.regulatory_risk}")
        elif "Moderate Risk" in scenario.regulatory_risk:
            st.warning(f"⚠️ **Regulatory Warning:** {scenario.regulatory_risk}")
        else:
            st.success(f"✅ **Safe Harbor:** {scenario.regulatory_risk}")

        st.markdown("<br>", unsafe_allow_html=True)

        # --- C. Executive Visualizations ---
        chart_col1, chart_col2 = st.columns([1, 1], gap="large")

        with chart_col1:
            st.subheader("Market Share Consolidation")

            # Prepare data for stacked bar
            pre_df = df.copy()
            pre_df["Scenario"] = "1. Pre-Merger"

            post_df = df.copy()
            acq_idx = post_df[post_df["Firm"] == acquirer].index[0]
            tgt_idx = post_df[post_df["Firm"] == target].index[0]

            post_df.loc[acq_idx, "Market_Share"] += post_df.loc[tgt_idx, "Market_Share"]
            post_df.loc[acq_idx, "Firm"] = f"{acquirer} + {target}"
            post_df = post_df.drop(tgt_idx)
            post_df["Scenario"] = "2. Post-Merger"

            plot_df = pd.concat([pre_df, post_df])
            plot_df = plot_df.sort_values(
                by=["Scenario", "Market_Share"], ascending=[True, False]
            )

            fig_bar = px.bar(
                plot_df,
                x="Scenario",
                y="Market_Share",
                color="Firm",
                text="Market_Share",
                color_discrete_sequence=px.colors.qualitative.Pastel,
            )
            fig_bar.update_traces(texttemplate="%{text:.1f}%", textposition="inside")
            fig_bar.update_layout(
                yaxis_title="Market Share (%)",
                xaxis_title="",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                legend_title_text="",
            )
            st.plotly_chart(fig_bar, use_container_width=True)

        with chart_col2:
            st.subheader("DOJ Regulatory Index (HHI)")

            # Gauge Chart for HHI Limits
            fig_gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number+delta",
                    value=scenario.post_hhi,
                    delta={
                        "reference": scenario.pre_hhi,
                        "position": "top",
                        "valueformat": ".1f",
                    },
                    title={"text": "Post-Merger Index", "font": {"size": 20}},
                    domain={"x": [0, 1], "y": [0, 1]},
                    gauge={
                        "axis": {"range": [None, 6000], "tickwidth": 1},
                        "bar": {"color": "black", "thickness": 0.1},
                        "bgcolor": "white",
                        "borderwidth": 2,
                        "bordercolor": "gray",
                        "steps": [
                            {"range": [0, 1500], "color": "#1f77b4"},  # Blue (Safe)
                            {
                                "range": [1500, 2500],
                                "color": "#ff7f0e",
                            },  # Orange (Moderate)
                            {
                                "range": [2500, 6000],
                                "color": "#d62728",
                            },  # Red (Highly Concentrated)
                        ],
                        "threshold": {
                            "line": {"color": "white", "width": 4},
                            "thickness": 0.75,
                            "value": scenario.post_hhi,
                        },
                    },
                )
            )
            fig_gauge.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=20, t=50, b=20),
            )
            st.plotly_chart(fig_gauge, use_container_width=True)

    except Exception as e:
        st.error(f"Error executing simulation: {e}")
