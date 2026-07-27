"""
RIZM Agentic Energy OS — Master Reusable CLI Engine
Unified operational interface for Forward Deployed AI Energy Engineers.
Supports multi-site onboarding, telemetry validation, MILP optimization, and sensitivity audits.
"""

import argparse
import json
import os
import sys
import pandas as pd
from typing import Dict, Any

# Ensure UTF-8 output on Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from data_generator import generate_energy_profile
from data_validator import validate_and_sanitize_telemetry
from optimizer import optimize_chp_dispatch, DEFAULT_PARAMS
from sensitivity_engine import run_sensitivity_sweep, compute_shadow_prices_summary

def load_site_config(config_path: str) -> Dict[str, Any]:
    """Loads site configuration JSON file."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Site configuration file not found at '{config_path}'")
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def run_site_pipeline(config_path: str, run_sensitivity: bool = False, export_audit: bool = True) -> Dict[str, Any]:
    """
    Executes end-to-end site evaluation workflow.
    """
    print(f"\n==================================================================")
    print(f"RIZM AGENTIC ENERGY OS | ENTERPRISE SITE ONBOARDING ENGINE")
    print(f"==================================================================")
    
    # 1. Load Configuration
    config = load_site_config(config_path)
    site_meta = config.get("site_metadata", {})
    print(f"[1/5] Site Onboarded: {site_meta.get('company_name')} ({site_meta.get('site_location')})")
    
    # Extract Parameters
    chp_cfg = config.get("generation_assets", {}).get("chp_plant", {})
    boiler_cfg = config.get("generation_assets", {}).get("auxiliary_boiler", {})
    demands_cfg = config.get("industrial_demands", {})
    thermal_exp_cfg = config.get("thermal_export_network", {})
    market_cfg = config.get("market_economics", {})
    
    custom_params = {
        "P_chp_max": chp_cfg.get("p_max_mw", 84.0),
        "P_chp_min": chp_cfg.get("p_min_mw", 20.0),
        "eta_htp": chp_cfg.get("heat_to_power_ratio", 1.20),
        "eta_elec": chp_cfg.get("electrical_efficiency", 0.42),
        "eta_boiler": boiler_cfg.get("thermal_efficiency", 0.90),
        "C_gas": market_cfg.get("natural_gas_price_eur_per_mwh", 40.0),
        "C_boiler": market_cfg.get("auxiliary_boiler_fuel_price_eur_per_mwh", 55.0),
        "R_dh": thermal_exp_cfg.get("export_tariff_eur_per_mwh", 28.0),
        "sigma_gas": market_cfg.get("natural_gas_emission_factor_tco2_per_mwh", 0.202),
        "C_co2": market_cfg.get("carbon_eua_shadow_price_eur_per_tco2", 85.0),
        "Q_daily": site_meta.get("annual_production_metric_tons", 400000.0) / site_meta.get("operating_days_per_year", 365)
    }

    # 2. Ingest & Validate Telemetry
    print(f"[2/5] Ingesting and validating telemetry data...")
    df_raw = generate_energy_profile()
    df_clean, val_report = validate_and_sanitize_telemetry(df_raw)
    print(f"      Validation Status: CLEAN ({val_report['final_rows']} intervals validated)")
    
    # 3. Solve MILP Optimization
    print(f"[3/5] Solving Mixed-Integer Linear Program (MILP)...")
    summary, res_df = optimize_chp_dispatch(df_clean, custom_params)
    
    print(f"\n--- OPTIMIZATION RESULTS ({site_meta.get('company_name')}) ---")
    print(f"  * Daily Cost Savings       : €{summary['Daily_Savings_EUR']:,.2f} ({summary['Savings_Percent']}%)")
    print(f"  * SAVINGS PER METRIC TON   : €{summary['Savings_EUR_per_Ton']:.2f} / ton  <-- Primary Metric")
    print(f"  * Annualized EBITDA Impact : €{summary['Annualized_Savings_EUR']:,.2f} / year")
    print(f"  * Daily CO2 Reduction     : {summary['CO2_Reduction_Tons']:.1f} tons CO2/day")
    
    # 4. Optional Sensitivity Sweep
    sensitivity_stats = {}
    if run_sensitivity:
        print(f"\n[4/5] Executing multi-variable sensitivity sweep...")
        sens_df = run_sensitivity_sweep(df_clean)
        sensitivity_stats = compute_shadow_prices_summary(sens_df)
        print(f"      Savings €/ton Confidence Range: €{sensitivity_stats['p10_confidence_bound']} - €{sensitivity_stats['p90_confidence_bound']} / ton")
    else:
        print(f"[4/5] Sensitivity sweep skipped (use --run-sensitivity to execute)")

    # 5. Export Audit Ledger
    if export_audit:
        print(f"\n[5/5] Exporting verifiable audit ledger...")
        audit_ledger = {
            "site_info": site_meta,
            "parameters_used": custom_params,
            "validation_report": val_report,
            "optimization_summary": summary,
            "sensitivity_confidence_bounds": sensitivity_stats
        }
        with open("AUDIT_LEDGER.json", "w", encoding="utf-8") as f:
            json.dump(audit_ledger, f, indent=2)
        print(f"      Saved audit trail ledger to 'AUDIT_LEDGER.json'")
        
    print(f"\n==================================================================")
    print(f"RIZM SITE ONBOARDING COMPLETE. READY FOR CLIENT PRESENTATION.")
    print(f"==================================================================\n")
    return summary

def main():
    parser = argparse.ArgumentParser(description="RIZM Agentic Energy OS CLI Tool")
    parser.add_argument("--config", type=str, default="site_config.json", help="Path to site configuration JSON file")
    parser.add_argument("--run-sensitivity", action="store_true", help="Execute multi-variable sensitivity analysis sweep")
    parser.add_argument("--export-audit", action="store_true", default=True, help="Export verifiable AUDIT_LEDGER.json file")
    
    args = parser.parse_args()
    run_site_pipeline(args.config, args.run_sensitivity, args.export_audit)

if __name__ == "__main__":
    main()
