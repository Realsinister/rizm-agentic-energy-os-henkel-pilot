"""
RIZM Agentic Energy OS — Henkel Düsseldorf Site Pilot
Executive Presentation & Interactive Web Dashboard (app.py)
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from data_generator import generate_energy_profile
from optimizer import optimize_chp_dispatch, calculate_baseline, DEFAULT_PARAMS

# Page Configuration
st.set_page_config(
    page_title="RIZM Agentic OS | Henkel Executive Dashboard",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Executive Dark Mode & Modern Cards)
st.markdown("""
<style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 800;
        background: linear-gradient(90deg, #00E676, #29B6F6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.1rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #CFD8DC;
        margin-bottom: 1.2rem;
    }
    .metric-card {
        background-color: #1A2129;
        border-radius: 12px;
        padding: 16px;
        border-left: 5px solid #00E676;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 800;
        color: #FFFFFF;
    }
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: #90A4AE;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .metric-subtext {
        font-size: 0.8rem;
        margin-top: 4px;
    }
    .callout-box {
        background-color: #1E2732;
        border-radius: 10px;
        padding: 18px;
        border-left: 4px solid #29B6F6;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Controls & Reload Mechanism ---
st.sidebar.header("🎛️ Executive Scenario Controls")
st.sidebar.markdown("Modulate market parameters to evaluate real-time EBITDA and **€/ton** sensitivities.")

# Session State Initialization for Parameters
if "gas_price_slider" not in st.session_state:
    st.session_state["gas_price_slider"] = 40.0
if "carbon_tax_slider" not in st.session_state:
    st.session_state["carbon_tax_slider"] = 85.0
if "dh_tariff_slider" not in st.session_state:
    st.session_state["dh_tariff_slider"] = 28.0
if "spot_volatility_slider" not in st.session_state:
    st.session_state["spot_volatility_slider"] = 1.0

def reset_parameters():
    st.session_state["gas_price_slider"] = 40.0
    st.session_state["carbon_tax_slider"] = 85.0
    st.session_state["dh_tariff_slider"] = 28.0
    st.session_state["spot_volatility_slider"] = 1.0

# 🔄 Reload / Reset Parameters Button
st.sidebar.button("🔄 Reset to Default Parameters", on_click=reset_parameters, use_container_width=True)

gas_price = st.sidebar.slider(
    "Natural Gas Price (€/MWh therm)", 
    min_value=20.0, max_value=80.0, step=2.5, key="gas_price_slider"
)
carbon_tax = st.sidebar.slider(
    "EUA Carbon Penalty (€/tCO2e)", 
    min_value=30.0, max_value=150.0, step=5.0, key="carbon_tax_slider"
)
dh_tariff = st.sidebar.slider(
    "District Heat Export Revenue (€/MWh)", 
    min_value=10.0, max_value=50.0, step=1.0, key="dh_tariff_slider"
)
spot_volatility = st.sidebar.slider(
    "EPEX Spot Price Volatility Multiplier", 
    min_value=0.5, max_value=2.5, step=0.1, key="spot_volatility_slider"
)

st.sidebar.markdown("---")
st.sidebar.caption("🏢 **Facility**: Henkel Düsseldorf-Holthausen\n🏭 **Capacity**: 400,000 metric tons/yr\n⚡ **Primary Asset**: 84 MW Gas CHP Turbine")

# --- Application Header ---
st.markdown('<div class="main-header">⚡ RIZM Agentic Energy OS</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Executive Onboarding Dashboard | Henkel Flagship Plant (Düsseldorf-Holthausen)</div>', unsafe_allow_html=True)

# Ingest & Solve Data
@st.cache_data
def get_base_data():
    return generate_energy_profile()

df_raw = get_base_data().copy()
if spot_volatility != 1.0:
    df_raw["Spot_Price_EUR_MWh"] = df_raw["Spot_Price_EUR_MWh"] * spot_volatility

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
            <div class="metric-label">SAVINGS PER METRIC TON</div>
            <div class="metric-value">€{summary['Savings_EUR_per_Ton']:.2f} / t</div>
            <div class="metric-subtext" style="color: #00E676;">🎯 Core KPI Challenge Metric</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #29B6F6;">
            <div class="metric-label">DAILY COST SAVINGS</div>
            <div class="metric-value">€{summary['Daily_Savings_EUR']:,.2f}</div>
            <div class="metric-subtext" style="color: #29B6F6;">📉 {summary['Savings_Percent']}% OpEx Reduction</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #AB47BC;">
            <div class="metric-label">ANNUALIZED EBITDA GAIN</div>
            <div class="metric-value">€{summary['Annualized_Savings_EUR']/1e6:.2f} M</div>
            <div class="metric-subtext" style="color: #AB47BC;">💼 Projected Annual Yield</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #FFA726;">
            <div class="metric-label">CO2 EMISSIONS AVOIDED</div>
            <div class="metric-value">{summary['CO2_Reduction_Tons']:.1f} t/day</div>
            <div class="metric-subtext" style="color: #FFA726;">🌱 Decarbonization Impact</div>
        </div>
        """, unsafe_allow_html=True)

    with col5:
        st.markdown(f"""
        <div class="metric-card" style="border-left-color: #FF7043;">
            <div class="metric-label">OPTIMIZED DAILY OPEX</div>
            <div class="metric-value">€{summary['Optimized_Daily_Cost_EUR']:,.0f}</div>
            <div class="metric-subtext" style="color: #FF7043;">Base: €{summary['Baseline_Daily_Cost_EUR']:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Executive Tabbed Presentation Navigation ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Executive ROI & Business Case", 
        "⚡ Use Case #1: Solar Price Arbitrage", 
        "🔥 Use Case #2: District Heat Integration", 
        "📈 Financial Profile & Data Export"
    ])

    # === TAB 1: EXECUTIVE ROI SUMMARY ===
    with tab1:
        st.subheader("💡 Business Case Rationale for Henkel Leadership")
        
        col_b1, col_b2 = st.columns([3, 2])
        
        with col_b1:
            st.markdown("""
            <div class="callout-box">
                <h4 style="color: #00E676; margin-top:0;">Why Deploy RIZM Agentic Energy OS at Düsseldorf-Holthausen?</h4>
                <p>Henkel’s global headquarters site produces <b>400,000 metric tons</b> of Laundry & Home Care and Industrial Adhesives annually. Historically, the plant ran its <b>84 MW captive gas-fired CHP turbine</b> at a static, unoptimized rate to meet constant spray-drying process heat loads.</p>
                <p>RIZM Agentic Energy OS transforms this physical infrastructure into an <b>algorithmically traded flexibility asset</b>:</p>
                <ul>
                    <li><b>Dynamic Grid Power Arbitrage</b>: Automatically throttles CHP output during mid-day solar price crashes to import cheap/negative grid power.</li>
                    <li><b>District Heat Export Arbitrage</b>: Routes excess CHP thermal output into the 700 m² Stadtwerke Düsseldorf waste-heat network supplying Garath, Benrath, and Holthausen.</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col_b2:
            st.markdown(f"""
            <div style="background-color: #1A2129; border-radius: 10px; padding: 20px; border: 1px solid #37474F;">
                <h4 style="color: #29B6F6; margin-top:0;">Normalized Savings Formula</h4>
                <p style="font-size: 0.9rem; color: #B0BEC5;">Primary challenge evaluation metric (€/ton):</p>
                <div style="font-size: 1.2rem; font-weight: 700; color: #FFFFFF; background-color: #101418; padding: 12px; border-radius: 8px; text-align: center;">
                    €/ton = <span style="color: #00E676;">€{summary['Daily_Savings_EUR']:,.2f} Daily Savings</span> / <span style="color: #29B6F6;">1,095.89 Daily Tons</span>
                </div>
                <h3 style="color: #00E676; text-align: center; margin-top: 15px;">= €{summary['Savings_EUR_per_Ton']:.2f} / metric ton saved</h3>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### 📋 Executive Business Case Summary Table")
        summary_table_data = {
            "Optimization Dimension": ["Daily Operating Expenditure (€/day)", "Normalized Cost Metric (€/ton)", "Annualized Operating Impact (€/year)", "Daily CO2 Footprint (tCO2e/day)"],
            "Unoptimized Baseline": [f"€{summary['Baseline_Daily_Cost_EUR']:,.2f}", f"€{summary['Baseline_Daily_Cost_EUR']/1095.89:.2f} / ton", f"€{summary['Baseline_Daily_Cost_EUR']*365/1e6:.2f} M / yr", f"{summary['Baseline_CO2_Tons']:.1f} tons/day"],
            "RIZM Agentic OS Optimized": [f"€{summary['Optimized_Daily_Cost_EUR']:,.2f}", f"€{summary['Optimized_Daily_Cost_EUR']/1095.89:.2f} / ton", f"€{summary['Optimized_Daily_Cost_EUR']*365/1e6:.2f} M / yr", f"{summary['Optimized_CO2_Tons']:.1f} tons/day"],
            "Net Customer Benefit": [f"€{summary['Daily_Savings_EUR']:,.2f} / day", f"€{summary['Savings_EUR_per_Ton']:.2f} / ton saved", f"€{summary['Annualized_Savings_EUR']/1e6:.2f} M / year", f"{summary['CO2_Reduction_Tons']:.1f} tons CO2/day avoided"]
        }
        st.table(pd.DataFrame(summary_table_data))

    # === TAB 2: ELECTRICAL ARBITRAGE ===
    with tab2:
        st.subheader("⚡ 1. Dynamic Electrical Dispatch & EPEX Spot Price Arbitrage")
        st.caption("Demonstrates how RIZM automatically throttles CHP generation during mid-day solar price drops to purchase cheap grid power, and ramps CHP output during peak price windows.")

        fig_elec = make_subplots(specs=[[{"secondary_y": True}]])
        fig_elec.add_trace(
            go.Bar(x=res_df["Timestamp"], y=res_df["P_chp"], name="84 MW CHP Output (MW)", marker_color="#00E676"),
            secondary_y=False
        )
        fig_elec.add_trace(
            go.Bar(x=res_df["Timestamp"], y=res_df["P_grid"], name="Grid Power Import (MW)", marker_color="#29B6F6"),
            secondary_y=False
        )
        fig_elec.add_trace(
            go.Scatter(x=res_df["Timestamp"], y=res_df["Spot_Price_EUR_MWh"], name="EPEX Spot Price (€/MWh)", line=dict(color="#FFEA00", width=3)),
            secondary_y=True
        )
        
        fig_elec.update_layout(
            barmode="stack",
            template="plotly_dark",
            height=460,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_elec.update_xaxes(title_text="Time (15-min Intervals)")
        fig_elec.update_yaxes(title_text="Electrical Power (MW)", secondary_y=False)
        fig_elec.update_yaxes(title_text="EPEX Spot Price (€/MWh)", secondary_y=True)

        st.plotly_chart(fig_elec, use_container_width=True)

        st.info("💡 **Executive Takeaway**: Notice the mid-day window (11:30–15:30) where EPEX spot prices crash due to solar PV over-generation. RIZM automatically throttles the CHP down to its 20 MW min load and imports cheap grid power, eliminating natural gas burn when electricity is cheap.")

    # === TAB 3: THERMAL DISPATCH ===
    with tab3:
        st.subheader("🔥 2. Thermal Dispatch & District Heat Integration")
        st.caption("Couples spray-drying process heat demand with thermal export to Garath/Benrath municipal district heating network (Stadtwerke Düsseldorf cooperation).")

        fig_therm = go.Figure()
        fig_therm.add_trace(go.Bar(x=res_df["Timestamp"], y=res_df["H_chp"], name="CHP Thermal Output (MWt)", marker_color="#FF7043"))
        fig_therm.add_trace(go.Bar(x=res_df["Timestamp"], y=res_df["H_boiler"], name="Aux Boiler Output (MWt)", marker_color="#AB47BC"))
        fig_therm.add_trace(go.Scatter(x=res_df["Timestamp"], y=res_df["H_dh"], name="District Heat Export (MWt)", line=dict(color="#00E676", width=2, dash="dash")))

        fig_therm.update_layout(
            barmode="stack",
            template="plotly_dark",
            height=460,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_therm, use_container_width=True)

        st.success("🔥 **Executive Takeaway**: During peak electricity price windows, RIZM ramps the CHP to max electrical capacity. The excess thermal output is exported via the 700 m² energy center into Stadtwerke Düsseldorf’s heating grid, generating €28/MWh in feed-in revenue.")

    # === TAB 4: FINANCIAL SAVINGS & DATA EXPORT ===
    with tab4:
        st.subheader("📈 3. Interval Operational Savings & Telemetry Data Ledger")
        
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

        st.subheader("📋 4. Full 96-Interval Telemetry Ledger")
        st.dataframe(res_df[["Timestamp", "Spot_Price_EUR_MWh", "Electrical_Demand_MW", "P_chp", "P_grid", "Thermal_Demand_MWt", "H_chp", "H_dh", "Interval_Cost_EUR"]], use_container_width=True)
        
        csv_bytes = res_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Full 96-Interval Optimization CSV", data=csv_bytes, file_name="henkel_dusseldorf_rizm_optimization.csv", mime="text/csv")

except Exception as e:
    st.error(f"Optimization Execution Error: {str(e)}")
