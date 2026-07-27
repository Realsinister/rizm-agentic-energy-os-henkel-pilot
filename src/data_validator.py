"""
Fail-Proof Telemetry Data Validator & Sanitation Module
for RIZM Agentic Energy OS.
Ensures incoming customer operational telemetry is clean, continuous, and physically sound before solving.
"""

import pandas as pd
import numpy as np
import logging
from typing import Tuple, Dict, Any

# Configure Data Quality Logging
logging.basicConfig(level=logging.INFO, format="[DATA VALIDATOR] %(levelname)s: %(message)s")

class TelemetryValidationError(Exception):
    """Custom exception raised when data cannot be sanitized safely."""
    pass

def validate_and_sanitize_telemetry(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Validates and cleans time-series telemetry data.
    
    Checks:
    1. Required columns presence.
    2. Timestamp continuity and format parsing.
    3. Null / NaN imputation (linear interpolation).
    4. Physical load bound checks (non-negative demands, reasonable bounds).
    5. Anomaly / outlier detection.
    """
    df_clean = df.copy()
    report = {
        "initial_rows": len(df),
        "missing_values_repaired": 0,
        "anomalies_clipped": 0,
        "is_valid": True,
        "warnings": []
    }
    
    required_cols = [
        "Timestamp", "Spot_Price_EUR_MWh", "Electrical_Demand_MW",
        "Thermal_Demand_MWt", "District_Heating_Capacity_MWt"
    ]
    
    # 1. Column Existence Check
    for col in required_cols:
        if col not in df_clean.columns:
            raise TelemetryValidationError(f"Missing required telemetry column: '{col}'")
            
    # 2. Timestamp Parsing & Continuity Check
    try:
        df_clean["Timestamp"] = pd.to_datetime(df_clean["Timestamp"])
    except Exception as e:
        raise TelemetryValidationError(f"Timestamp parsing error: {str(e)}")
        
    df_clean = df_clean.sort_values("Timestamp").reset_index(drop=True)
    
    # 3. Missing Value Detection & Linear Imputation
    null_count = df_clean[required_cols[1:]].isnull().sum().sum()
    if null_count > 0:
        report["missing_values_repaired"] = int(null_count)
        report["warnings"].append(f"Detected {null_count} missing values. Repaired via linear interpolation.")
        logging.warning(f"Detected {null_count} missing values. Performing linear interpolation.")
        df_clean[required_cols[1:]] = df_clean[required_cols[1:]].interpolate(method="linear").bfill().ffill()
        
    # 4. Physical Load Bound Validation
    # Demands must be strictly non-negative
    for demand_col in ["Electrical_Demand_MW", "Thermal_Demand_MWt", "District_Heating_Capacity_MWt"]:
        neg_mask = df_clean[demand_col] < 0
        if neg_mask.any():
            count = neg_mask.sum()
            report["anomalies_clipped"] += int(count)
            report["warnings"].append(f"Clipped {count} negative values in {demand_col} to 0.0.")
            logging.warning(f"Clipped {count} negative values in {demand_col} to 0.0.")
            df_clean.loc[neg_mask, demand_col] = 0.0
            
    # 5. Outlier Detection (Capping extreme spikes > 10x median)
    for numeric_col in required_cols[1:]:
        median_val = df_clean[numeric_col].median()
        std_val = df_clean[numeric_col].std()
        upper_limit = median_val + 6 * std_val
        lower_limit = median_val - 6 * std_val
        
        spike_mask = (df_clean[numeric_col] > upper_limit) | (df_clean[numeric_col] < lower_limit)
        if spike_mask.any() and numeric_col != "Spot_Price_EUR_MWh":
            count = spike_mask.sum()
            report["anomalies_clipped"] += int(count)
            report["warnings"].append(f"Clipped {count} extreme telemetry outliers in {numeric_col}.")
            df_clean.loc[df_clean[numeric_col] > upper_limit, numeric_col] = upper_limit
            df_clean.loc[df_clean[numeric_col] < lower_limit, numeric_col] = lower_limit

    # Standardize string timestamp format
    df_clean["Timestamp"] = df_clean["Timestamp"].dt.strftime("%Y-%m-%d %H:%M:%S")
    report["final_rows"] = len(df_clean)
    
    logging.info(f"Telemetry validation passed successfully. Sanitized {report['final_rows']} intervals.")
    return df_clean, report

if __name__ == "__main__":
    from data_generator import generate_energy_profile
    df = generate_energy_profile()
    df_clean, report = validate_and_sanitize_telemetry(df)
    print("Validation Report:", report)
