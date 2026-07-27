"""
Automated Test Suite for Sample Energy OS — Henkel Düsseldorf Site Pilot.
Verifies system architecture constraints, data schemas, energy balances, and solver convergence.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_generator import generate_energy_profile
from src.optimizer import optimize_chp_dispatch, calculate_baseline, DEFAULT_PARAMS

def test_data_generation():
    """Verify data generator produces exactly 96 non-null intervals with expected columns."""
    df = generate_energy_profile(output_file="data/test_profile.csv")
    assert len(df) == 96, f"Expected 96 intervals, got {len(df)}"
    assert not df.isnull().values.any(), "Generated data contains null values"
    
    expected_cols = [
        "Timestamp", "Spot_Price_EUR_MWh", "Electrical_Demand_MW", 
        "Thermal_Demand_MWt", "District_Heating_Capacity_MWt"
    ]
    for col in expected_cols:
        assert col in df.columns, f"Missing required column: {col}"
        
    # Verify presence of solar negative price depression
    min_price = df["Spot_Price_EUR_MWh"].min()
    assert min_price < 20.0, f"Expected solar depression in spot prices, min price was {min_price}"

def test_baseline_calculation():
    """Verify baseline energy calculation consistency."""
    df = generate_energy_profile(output_file="data/test_profile.csv")
    baseline_cost, baseline_co2, df_base = calculate_baseline(df)
    
    assert baseline_cost > 0, "Baseline cost must be positive"
    assert baseline_co2 > 0, "Baseline CO2 emissions must be positive"
    assert (df_base["H_dh"] == 0).all(), "Baseline must not export district heat"

def test_milp_solver_convergence():
    """Verify PuLP solver converges to optimal solution and respects physics constraints."""
    df = generate_energy_profile(output_file="data/test_profile.csv")
    summary, res_df = optimize_chp_dispatch(df)
    
    # 1. Financial Sanity
    assert summary["Daily_Savings_EUR"] > 0, "Optimization must yield cost savings"
    assert summary["Savings_EUR_per_Ton"] > 0, "Savings per ton metric must be strictly positive"
    assert summary["Savings_Percent"] > 0, "Savings percentage must be strictly positive"
    
    # 2. Electrical Energy Balance Check: P_chp + P_grid == Electrical_Demand
    elec_diff = np.abs((res_df["P_chp"] + res_df["P_grid"]) - res_df["Electrical_Demand_MW"])
    assert (elec_diff < 1e-4).all(), f"Electrical balance violated! Max diff: {elec_diff.max()}"
    
    # 3. Thermal Energy Balance Check: H_chp + H_boiler == Thermal_Demand + H_dh
    therm_lhs = res_df["H_chp"] + res_df["H_boiler"]
    therm_rhs = res_df["Thermal_Demand_MWt"] + res_df["H_dh"]
    therm_diff = np.abs(therm_lhs - therm_rhs)
    assert (therm_diff < 1e-4).all(), f"Thermal balance violated! Max diff: {therm_diff.max()}"
    
    # 4. Physical Asset Limits
    assert (res_df["P_chp"] <= DEFAULT_PARAMS["P_chp_max"] + 1e-4).all(), "CHP max capacity exceeded"
    assert (res_df["H_dh"] <= res_df["District_Heating_Capacity_MWt"] + 1e-4).all(), "District heat cap exceeded"

if __name__ == "__main__":
    pytest.main(["-v", "tests/test_suite.py"])
