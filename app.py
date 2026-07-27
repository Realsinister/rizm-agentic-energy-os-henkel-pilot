"""
RIZM Agentic Energy OS — Henkel Düsseldorf Site Pilot
Interactive Streamlit Web Dashboard (app.py)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_generator import generate_energy_profile
from optimizer import optimize_chp_dispatch, DEFAULT_PARAMS

# Page Configuration
st.set_page_config(
    page_title="RIZM Energy OS | Henkel Düsseldorf Pilot",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Dark Mode & Premium Aesthetics)
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00E676;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #B0BEC5;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #1E242B;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #00E676;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #90A4AE;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-header">⚡ RIZM Agentic Energy OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">DAX-40 Optimization Pilot | Henkel Headquarters & Production Site (Düsseldorf-Holthausen)</div>', unsafe_allow_html=True)

# Sidebar Control Panel
st.sidebar.header("🎛️ Simulation Control Parameters")
st.sidebar.markdown("Adjust macroeconomic parameters to observe real-time dispatch and **€/ton** financial impacts.")

gas_price = st.sidebar.slider("Natural Gas Price (€/MWh therm)", min_value=20.0, max_value=80.0, value=40.0, step=2.5)
carbon_tax = st.sidebar.slider("EUA Carbon Penalty (€/tCO2e)", min_value=30.0, max_value=150.0, value=85.0, step=5.0)
dh_tariff = st.sidebar.slider("District Heat Export Revenue (€/MWh therm)", min_value=10.0, max_value=50.0, value=28.0, step=1.0)
spot_volatility = st.sidebar.slider("EPEX Spot Price Volatility Multiplier", min_value=0.5, max_value=2.5, value=1.0, step=0.1)

# Cache data generation
@st.cache_data
def get_base_data():
    return generate_energy_profile()

df_raw = get_base_data().copy()
if spot_volatility != 1.0:
    df_raw["Spot_Price_EUR_MWh"] = df_raw["Spot_Price_EUR_MWh"] * spot_volatility

# Run Optimization Solver
custom_params = {
    "C_gas": gas_price,
    "C_co2": carbon_tax,
    "R_dh": dh_tariff
}

try:
    summary, res_df = optimize_chp_dispatch(df_raw, custom_params)
    
    # --- Top KPI Metrics Banner ---
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">SAVINGS PER TON</div>
            <div class="metric-value">€{summary['Savings_EUR_per_Ton']:.2f} / t</div>
            <div style="color: #00E676; font-size: 0.85rem;">Key Challenge Metric</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #29B6F6;">
            <div class="metric-label">DAILY COST SAVINGS</div>
            <div class="metric-value">€{summary['Daily_Savings_EUR']:,.2f}</div>
            <div style="color: #29B6F6; font-size: 0.85rem;">{summary['Savings_Percent']}% Reduction</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #AB47BC;">
            <div class="metric-label">ANNUALIZED SAVINGS</div>
            <div class="metric-value">€{summary['Annualized_Savings_EUR']:,.0f}</div>
            <div style="color: #AB47BC; font-size: 0.85rem;">Projected EBITDA Gain</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #FFA726;">
            <div class="metric-label">CO2 REDUCTION</div>
            <div class="metric-value">{summary['CO2_Reduction_Tons']:.1f} t/day</div>
            <div style="color: #FFA726; font-size: 0.85rem;">Avoided Emissions</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #FF7043;">
            <div class="metric-label">DAILY OPEX (OPTIMIZED)</div>
            <div class="metric-value">€{summary['Optimized_Daily_Cost_EUR']:,.2f}</div>
            <div style="color: #FF7043; font-size: 0.85rem;">Base: €{summary['Baseline_Daily_Cost_EUR']:,.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Section 1: Electrical Dispatch & EPEX Spot Price Arbitrage Chart ---
    st.subheader("⚡ 1. Dynamic Electrical Dispatch Mix vs. EPEX Spot Price Arbitrage")
    st.caption("Demonstrates how RIZM Agentic OS automatically throttles CHP generation during mid-day solar negative pricing to import cheap grid power, and ramps CHP output during peak price windows.")

    fig_elec = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Stacked Bars for Electrical Generation
    fig_elec.add_trace(
        go.Bar(x=res_df["Timestamp"], y=res_df["P_chp"], name="84 MW CHP Output (MW)", marker_color="#00E676"),
        secondary_y=False
    )
    fig_elec.add_trace(
        go.Bar(x=res_df["Timestamp"], y=res_df["P_grid"], name="Grid Power Import (MW)", marker_color="#29B6F6"),
        secondary_y=False
    )
    
    # EPEX Spot Price Line Graph
    fig_elec.add_trace(
        go.Scatter(x=res_df["Timestamp"], y=res_df["Spot_Price_EUR_MWh"], name="EPEX Spot Price (€/MWh)", line=dict(color="#FFEA00", width=3)),
        secondary_y=True
    )
    
    fig_elec.update_layout(
        barmode="stack",
        template="plotly_dark",
        height=450,
        margin=dict(l=20, r=20, t=30, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig_elec.update_xaxes(title_text="Time (15-min Intervals)")
    fig_elec.update_yaxes(title_text="Electrical Generation / Load (MW)", secondary_y=False)
    fig_elec.update_yaxes(title_text="EPEX Spot Price (€/MWh)", secondary_y=True)

    st.plotly_chart(fig_elec, use_container_width=True)

    # --- Section 2: Thermal Dispatch & District Heat Export ---
    col_t1, col_t2 = st.columns(2)

    with col_t1:
        st.subheader("🔥 2. Thermal Dispatch & District Heat Integration")
        st.caption("Couples spray-drying process heat demand with thermal export to Garath/Benrath municipal district heating network (Stadtwerke Düsseldorf cooperation).")

        fig_therm = go.Figure()
        fig_therm.add_trace(go.Bar(x=res_df["Timestamp"], y=res_df["H_chp"], name="CHP Thermal Output (MWt)", marker_color="#FF7043"))
        fig_therm.add_trace(go.Bar(x=res_df["Timestamp"], y=res_df["H_boiler"], name="Aux Boiler Output (MWt)", marker_color="#AB47BC"))
        fig_therm.add_trace(go.Scatter(x=res_df["Timestamp"], y=res_df["H_dh"], name="District Heat Export (MWt)", line=dict(color="#00E676", width=2, dash="dash")))

        fig_therm.update_layout(
            barmode="stack",
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_therm, use_container_width=True)

    with col_t2:
        st.subheader("📉 3. Interval Financial Savings Profile (€)")
        st.caption("Comparison of unoptimized flat-run baseline cost vs RIZM optimized interval operational cost.")

        # Baseline vs Optimized cost per interval
        _, _, df_base = calculate_baseline(df_raw, custom_params)
        
        fig_cost = go.Figure()
        fig_cost.add_trace(go.Scatter(x=res_df["Timestamp"], y=df_base["Interval_Cost_EUR"], name="Baseline Cost (€/15-min)", line=dict(color="#EF5350", width=2)))
        fig_cost.add_trace(go.Scatter(x=res_df["Timestamp"], y=res_df["Interval_Cost_EUR"], name="RIZM Optimized Cost (€/15-min)", line=dict(color="#00E676", width=2)))

        fig_cost.update_layout(
            template="plotly_dark",
            height=380,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_cost, use_container_width=True)

    # --- Section 3: Data Inspection & Download ---
    st.subheader("📋 4. Optimization Time-Series Dataset")
    st.dataframe(res_df[["Timestamp", "Spot_Price_EUR_MWh", "Electrical_Demand_MW", "P_chp", "P_grid", "Thermal_Demand_MWt", "H_chp", "H_dh", "Interval_Cost_EUR"]], use_container_width=True)
    
    csv_bytes = res_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download Full 96-Interval Optimization CSV", data=csv_bytes, file_name="henkel_dusseldorf_rizm_optimization.csv", mime="text/csv")

except Exception as e:
    st.error(f"Optimization Execution Error: {str(e)}")
