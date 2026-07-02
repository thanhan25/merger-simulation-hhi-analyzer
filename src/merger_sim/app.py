"""
Streamlit Web Dashboard for the Merger Simulation Toolkit.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from merger_sim.simulation import simulate_merger

st.set_page_config(page_title="Antitrust Simulator", page_icon="⚖️", layout="wide")

st.title("⚖️ Merger Simulation & Market Concentration Analyzer")
st.markdown(
    "Upload market data to simulate horizontal mergers and calculate HHI antitrust metrics based on U.S. DOJ guidelines."
)

col1, col2 = st.columns([1, 2])

with col1:
    st.header("1. Input Data")
    uploaded_file = st.file_uploader("Upload Market Data (CSV)", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df, use_container_width=True)

        firms = df["Firm"].tolist()
        st.header("2. Simulation Parameters")
        acquirer = st.selectbox("Select Acquiring Firm", firms)
        target = st.selectbox("Select Target Firm", [f for f in firms if f != acquirer])

        simulate_btn = st.button(
            "Run Simulation", type="primary", use_container_width=True
        )

with col2:
    if uploaded_file is not None and simulate_btn:
        st.header("3. Regulatory Impact Analysis")

        try:
            results = simulate_merger(df, "Firm", "Market_Share", acquirer, target)

            # Metric Cards
            m1, m2, m3 = st.columns(3)
            m1.metric(label="Pre-Merger HHI", value=f"{results['hhi_pre']:,.2f}")
            m2.metric(
                label="Post-Merger HHI",
                value=f"{results['hhi_post']:,.2f}",
                delta=f"+{results['delta']:,.2f}",
                delta_color="inverse",
            )
            m3.metric(label="Concentration Level", value=results["concentration_level"])

            if "High Risk" in results["regulatory_risk"]:
                st.error(f"🚨 **Regulatory Alert:** {results['regulatory_risk']}")
            else:
                st.success(f"✅ **Safe Harbor:** {results['regulatory_risk']}")

            # Visualizations
            st.subheader("Market Share Transition")

            # Prepare data for plotting
            plot_df = df.copy()
            plot_df["Status"] = "Pre-Merger"

            post_df = df.copy()
            post_df.loc[post_df["Firm"] == acquirer, "Market_Share"] += post_df.loc[
                post_df["Firm"] == target, "Market_Share"
            ].values[0]
            post_df = post_df[post_df["Firm"] != target]
            post_df["Firm"] = post_df["Firm"].replace(
                {acquirer: f"{acquirer} + {target}"}
            )
            post_df["Status"] = "Post-Merger"

            combined_df = pd.concat([plot_df, post_df])

            fig = px.bar(
                combined_df,
                x="Status",
                y="Market_Share",
                color="Firm",
                title="Market Concentration Shift",
                barmode="stack",
                text="Firm",
            )
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error during simulation: {e}")
    elif uploaded_file is None:
        st.info("👈 Please upload a CSV file on the left to begin the analysis.")
