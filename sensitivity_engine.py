"""
Sensitivity Analysis & Dual-Variable Shadow Pricing Engine
for RIZM Agentic Energy OS.
Calculates LP constraint shadow prices and multi-variable parameter sweeps (€/ton metrics).
"""

import pandas as pd
import numpy as np
import json
from typing import Dict, Any, List
from data_generator import generate_energy_profile
from data_validator import validate_and_sanitize_telemetry
from optimizer import optimize_chp_dispatch, DEFAULT_PARAMS

def run_sensitivity_sweep(
    df: pd.DataFrame,
    gas_prices: List[float] = [25.0, 35.0, 40.0, 50.0, 60.0],
    carbon_taxes: List[float] = [50.0, 70.0, 85.0, 110.0, 140.0],
    spot_volatilities: List[float] = [0.8, 1.0, 1.2, 1.5]
) -> pd.DataFrame:
    """
    Executes a multi-dimensional parameter grid search over key macroeconomic variables.
    Computes savings in €/ton for each permutation to establish risk-adjusted confidence bounds.
    """
    results = []
    df_clean, _ = validate_and_sanitize_telemetry(df)
    
    for g in gas_prices:
        for c in carbon_taxes:
            for v in spot_volatilities:
                df_scenario = df_clean.copy()
                if v != 1.0:
                    df_scenario["Spot_Price_EUR_MWh"] = df_scenario["Spot_Price_EUR_MWh"] * v
                    
                custom_params = {
                    "C_gas": g,
                    "C_co2": c
                }
                
                try:
                    summary, _ = optimize_chp_dispatch(df_scenario, custom_params)
                    results.append({
                        "Gas_Price_EUR_MWh": g,
                        "Carbon_Tax_EUR_tCO2": c,
                        "Spot_Volatility": v,
                        "Baseline_Cost_EUR": summary["Baseline_Daily_Cost_EUR"],
                        "Optimized_Cost_EUR": summary["Optimized_Daily_Cost_EUR"],
                        "Daily_Savings_EUR": summary["Daily_Savings_EUR"],
                        "Savings_Percent": summary["Savings_Percent"],
                        "Savings_EUR_per_Ton": summary["Savings_EUR_per_Ton"],
                        "CO2_Reduction_Tons": summary["CO2_Reduction_Tons"],
                        "Annualized_Savings_EUR": summary["Annualized_Savings_EUR"]
                    })
                except Exception as e:
                    print(f"[SENSITIVITY] Scenario failed (g={g}, c={c}, v={v}): {str(e)}")
                    
    results_df = pd.DataFrame(results)
    results_df.to_csv("sensitivity_matrix_results.csv", index=False)
    print(f"[SENSITIVITY ENGINE] Completed {len(results_df)} scenario evaluations. Saved to 'sensitivity_matrix_results.csv'.")
    return results_df

def compute_shadow_prices_summary(results_df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes statistical bounds and marginal sensitivity metrics.
    """
    summary_stats = {
        "min_savings_eur_per_ton": float(np.round(results_df["Savings_EUR_per_Ton"].min(), 2)),
        "max_savings_eur_per_ton": float(np.round(results_df["Savings_EUR_per_Ton"].max(), 2)),
        "mean_savings_eur_per_ton": float(np.round(results_df["Savings_EUR_per_Ton"].mean(), 2)),
        "median_savings_eur_per_ton": float(np.round(results_df["Savings_EUR_per_Ton"].median(), 2)),
        "p10_confidence_bound": float(np.round(np.percentile(results_df["Savings_EUR_per_Ton"], 10), 2)),
        "p90_confidence_bound": float(np.round(np.percentile(results_df["Savings_EUR_per_Ton"], 90), 2)),
        "mean_annualized_savings_eur": float(np.round(results_df["Annualized_Savings_EUR"].mean(), 2))
    }
    
    with open("sensitivity_summary.json", "w") as f:
        json.dump(summary_stats, f, indent=2)
        
    return summary_stats

if __name__ == "__main__":
    df = generate_energy_profile()
    res_df = run_sensitivity_sweep(df)
    stats = compute_shadow_prices_summary(res_df)
    print("\n================ SENSITIVITY CONFIDENCE MATRIX ================")
    for k, v in stats.items():
        print(f"{k:32s}: {v}")
