"""
Data Generator Module for RIZM Energy OS — Henkel Düsseldorf Site Pilot.
Synthesizes a realistic 96-interval (15-minute, 24-hour) energy profile dataset.
"""

import pandas as pd
import numpy as np

def generate_energy_profile(output_file: str = "industrial_energy_profile.csv", seed: int = 42) -> pd.DataFrame:
    np.random.seed(seed)
    intervals = 96  # 24 hours * 4 intervals/hour
    timestamps = pd.date_range(start="2026-07-27 00:00", periods=intervals, freq="15min")
    
    hours = np.linspace(0, 24, intervals, endpoint=False)
    
    # 1. EPEX SPOT Electricity Price Synthesis (EUR/MWh)
    # Diurnal pattern: Morning peak, Solar mid-day crash (negative pricing), Evening peak
    base_price = 65.0
    morning_peak = 70.0 * np.exp(-((hours - 8.5) ** 2) / 2.5)
    evening_peak = 90.0 * np.exp(-((hours - 19.5) ** 2) / 3.0)
    solar_depression = -85.0 * np.exp(-((hours - 13.5) ** 2) / 3.0)
    
    noise_spot = np.random.normal(0, 4.0, intervals)
    spot_prices = base_price + morning_peak + evening_peak + solar_depression + noise_spot
    
    # 2. Electrical Demand (MW) — Henkel Düsseldorf spray-drying baseload
    base_elec_demand = 45.0
    elec_noise = np.random.normal(0, 1.2, intervals)
    elec_demand = base_elec_demand + elec_noise
    
    # 3. Thermal Process Demand (MWt) — Spray-drying towers process heat
    base_therm_demand = 60.0
    therm_noise = np.random.normal(0, 1.5, intervals)
    therm_demand = base_therm_demand + therm_noise
    
    # 4. District Heating Absorption Capacity (MWt) — Garath/Benrath export link
    # Higher thermal absorption capacity in morning/evening municipal heating windows
    base_dh_cap = 25.0 + 5.0 * np.sin(2 * np.pi * (hours - 6) / 24)
    dh_cap = np.clip(base_dh_cap + np.random.normal(0, 0.8, intervals), 15.0, 30.0)
    
    df = pd.DataFrame({
        "Timestamp": timestamps.strftime("%Y-%m-%d %H:%M:%S"),
        "Spot_Price_EUR_MWh": np.round(spot_prices, 2),
        "Electrical_Demand_MW": np.round(elec_demand, 2),
        "Thermal_Demand_MWt": np.round(therm_demand, 2),
        "District_Heating_Capacity_MWt": np.round(dh_cap, 2)
    })
    
    df.to_csv(output_file, index=False)
    print(f"[DATA GENERATOR] Successfully generated {len(df)} intervals dataset saved to '{output_file}'.")
    return df

if __name__ == "__main__":
    generate_energy_profile()
