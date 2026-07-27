"""
Deterministic Mixed-Integer Linear Programming (MILP) Optimization Engine
for RIZM Energy OS — Henkel Düsseldorf Site Pilot.
Formulated using PuLP based on SYSTEM_ARCHITECTURE.md SSOT.
"""

import pandas as pd
import numpy as np
import pulp
from typing import Dict, Any, Tuple

# SSOT Facility & Economic Parameters
DEFAULT_PARAMS = {
    "P_chp_max": 84.0,         # MW electrical max capacity
    "P_chp_min": 20.0,         # MW electrical min turn-down
    "eta_htp": 1.20,           # Heat-to-power ratio (MWt / MWe)
    "eta_elec": 0.42,          # Electrical efficiency of gas CHP
    "eta_boiler": 0.90,        # Auxiliary boiler thermal efficiency
    "C_gas": 40.0,             # EUR/MWh thermal (natural gas baseline)
    "C_boiler": 55.0,          # EUR/MWh thermal (auxiliary boiler fuel cost)
    "R_dh": 28.0,              # EUR/MWh thermal (district heat export tariff)
    "sigma_gas": 0.202,        # tCO2e / MWh thermal
    "C_co2": 85.0,             # EUR / tCO2e (EUA carbon penalty shadow price)
    "Q_daily": 1095.89,        # Metric tons of detergent produced per day (400,000 / 365)
    "delta_t": 0.25            # 15-minute time intervals (hours)
}

def calculate_baseline(df: pd.DataFrame, custom_params: Dict[str, Any] = None) -> Tuple[float, float, pd.DataFrame]:
    """
    Calculates the unoptimized baseline operation:
    CHP runs strictly at flat 45 MW to match electrical demand, aux boiler supplies thermal deficit,
    zero grid import arbitrage, zero district heat export.
    """
    params = DEFAULT_PARAMS.copy()
    if custom_params:
        params.update(custom_params)
        
    dt = params["delta_t"]
    df_base = df.copy()
    
    # Flat CHP dispatch matching electrical demand
    df_base["P_chp"] = np.minimum(df_base["Electrical_Demand_MW"], params["P_chp_max"])
    df_base["P_grid"] = np.maximum(0.0, df_base["Electrical_Demand_MW"] - df_base["P_chp"])
    df_base["H_chp"] = df_base["P_chp"] * params["eta_htp"]
    
    # Auxiliary boiler supplies thermal deficit
    df_base["H_boiler"] = np.maximum(0.0, df_base["Thermal_Demand_MWt"] - df_base["H_chp"])
    df_base["H_dh"] = 0.0  # Unoptimized: no heat export to city
    
    # Fuel consumption
    df_base["F_gas_chp"] = df_base["P_chp"] / params["eta_elec"]
    df_base["F_gas_boiler"] = df_base["H_boiler"] / params["eta_boiler"]
    df_base["Total_Gas_MWh"] = (df_base["F_gas_chp"] + df_base["F_gas_boiler"]) * dt
    
    # Financial costs per interval
    chp_fuel_cost = df_base["F_gas_chp"] * params["C_gas"] * dt
    boiler_fuel_cost = df_base["F_gas_boiler"] * params["C_boiler"] * dt
    grid_cost = df_base["P_grid"] * df_base["Spot_Price_EUR_MWh"] * dt
    carbon_emissions = (df_base["F_gas_chp"] + df_base["F_gas_boiler"]) * params["sigma_gas"] * dt
    carbon_cost = carbon_emissions * params["C_co2"]
    
    df_base["Interval_Cost_EUR"] = chp_fuel_cost + boiler_fuel_cost + grid_cost + carbon_cost
    df_base["CO2_Tons"] = carbon_emissions
    
    total_cost = df_base["Interval_Cost_EUR"].sum()
    total_co2 = df_base["CO2_Tons"].sum()
    
    return total_cost, total_co2, df_base

def optimize_chp_dispatch(
    df: pd.DataFrame, 
    custom_params: Dict[str, Any] = None
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Solves the Mixed-Integer Linear Program (MILP) for optimal CHP dispatch,
    grid power purchasing, and district heat export arbitrage.
    """
    params = DEFAULT_PARAMS.copy()
    if custom_params:
        params.update(custom_params)
        
    dt = params["delta_t"]
    N = len(df)
    
    # Initialize PuLP Problem
    prob = pulp.LpProblem("RIZM_Henkel_Energy_Optimization", pulp.LpMinimize)
    
    # Decision Variables per 15-minute interval
    P_chp = [pulp.LpVariable(f"P_chp_{t}", lowBound=0, upBound=params["P_chp_max"]) for t in range(N)]
    u_chp = [pulp.LpVariable(f"u_chp_{t}", cat=pulp.LpBinary) for t in range(N)]
    P_grid = [pulp.LpVariable(f"P_grid_{t}", lowBound=0) for t in range(N)]
    H_dh = [pulp.LpVariable(f"H_dh_{t}", lowBound=0) for t in range(N)]
    H_boiler = [pulp.LpVariable(f"H_boiler_{t}", lowBound=0) for t in range(N)]
    
    # Constraints and Objective Formulation
    cost_terms = []
    co2_terms = []
    
    for t in range(N):
        D_elec = df.loc[t, "Electrical_Demand_MW"]
        D_therm = df.loc[t, "Thermal_Demand_MWt"]
        DH_cap = df.loc[t, "District_Heating_Capacity_MWt"]
        spot_price = df.loc[t, "Spot_Price_EUR_MWh"]
        
        # 1. CHP Turn-down constraints
        prob += P_chp[t] >= u_chp[t] * params["P_chp_min"]
        prob += P_chp[t] <= u_chp[t] * params["P_chp_max"]
        
        # 2. Electrical Demand Conservation
        prob += P_chp[t] + P_grid[t] == D_elec
        
        # 3. Thermal Demand Conservation & District Heat Export
        H_chp_t = P_chp[t] * params["eta_htp"]
        prob += H_chp_t + H_boiler[t] == D_therm + H_dh[t]
        
        # 4. District Heating Export Cap
        prob += H_dh[t] <= DH_cap
        
        # Fuel & Financial terms
        F_gas_chp_t = P_chp[t] / params["eta_elec"]
        F_boiler_t = H_boiler[t] / params["eta_boiler"]
        
        interval_fuel_cost = (F_gas_chp_t * params["C_gas"] + F_boiler_t * params["C_boiler"]) * dt
        interval_grid_cost = P_grid[t] * spot_price * dt
        interval_dh_revenue = H_dh[t] * params["R_dh"] * dt
        
        interval_co2 = (F_gas_chp_t + F_boiler_t) * params["sigma_gas"] * dt
        interval_co2_cost = interval_co2 * params["C_co2"]
        
        cost_terms.append(interval_fuel_cost + interval_grid_cost + interval_co2_cost - interval_dh_revenue)
        co2_terms.append(interval_co2)
        
    prob += pulp.lpSum(cost_terms)
    
    # Solve MILP
    solver = pulp.PULP_CBC_CMD(msg=False)
    prob.solve(solver)
    
    if pulp.LpStatus[prob.status] != 'Optimal':
        raise RuntimeError(f"MILP Solver failed to reach optimal solution. Status: {pulp.LpStatus[prob.status]}")
        
    # Extract Optimized Time Series Data
    res_df = df.copy()
    res_df["P_chp"] = [P_chp[t].varValue for t in range(N)]
    res_df["u_chp"] = [u_chp[t].varValue for t in range(N)]
    res_df["P_grid"] = [P_grid[t].varValue for t in range(N)]
    res_df["H_chp"] = res_df["P_chp"] * params["eta_htp"]
    res_df["H_boiler"] = [H_boiler[t].varValue for t in range(N)]
    res_df["H_dh"] = [H_dh[t].varValue for t in range(N)]
    
    res_df["F_gas_chp"] = res_df["P_chp"] / params["eta_elec"]
    res_df["F_gas_boiler"] = res_df["H_boiler"] / params["eta_boiler"]
    
    chp_fuel_cost = res_df["F_gas_chp"] * params["C_gas"] * dt
    boiler_fuel_cost = res_df["F_gas_boiler"] * params["C_boiler"] * dt
    grid_cost = res_df["P_grid"] * res_df["Spot_Price_EUR_MWh"] * dt
    dh_revenue = res_df["H_dh"] * params["R_dh"] * dt
    carbon_emissions = (res_df["F_gas_chp"] + res_df["F_gas_boiler"]) * params["sigma_gas"] * dt
    carbon_cost = carbon_emissions * params["C_co2"]
    
    res_df["Interval_Cost_EUR"] = chp_fuel_cost + boiler_fuel_cost + grid_cost + carbon_cost - dh_revenue
    res_df["CO2_Tons"] = carbon_emissions
    
    # Calculate Summary Metrics
    baseline_cost, baseline_co2, df_baseline = calculate_baseline(df, params)
    optimized_cost = res_df["Interval_Cost_EUR"].sum()
    optimized_co2 = res_df["CO2_Tons"].sum()
    
    daily_savings_eur = baseline_cost - optimized_cost
    savings_pct = (daily_savings_eur / baseline_cost) * 100.0
    
    # Key challenge metric: € / ton of detergent produced saved
    savings_per_ton = daily_savings_eur / params["Q_daily"]
    co2_saved_tons = baseline_co2 - optimized_co2
    
    summary = {
        "Baseline_Daily_Cost_EUR": np.round(baseline_cost, 2),
        "Optimized_Daily_Cost_EUR": np.round(optimized_cost, 2),
        "Daily_Savings_EUR": np.round(daily_savings_eur, 2),
        "Savings_Percent": np.round(savings_pct, 2),
        "Savings_EUR_per_Ton": np.round(savings_per_ton, 2),
        "Baseline_CO2_Tons": np.round(baseline_co2, 2),
        "Optimized_CO2_Tons": np.round(optimized_co2, 2),
        "CO2_Reduction_Tons": np.round(co2_saved_tons, 2),
        "Annualized_Savings_EUR": np.round(daily_savings_eur * 365, 2)
    }
    
    return summary, res_df

if __name__ == "__main__":
    from src.data_generator import generate_energy_profile
    df = generate_energy_profile()
    summary, res_df = optimize_chp_dispatch(df)
    print("\n================ RIZM OPTIMIZATION SUMMARY ================")
    for k, v in summary.items():
        print(f"{k:30s}: {v}")
