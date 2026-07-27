# Sample Energy OS — Henkel Pilot & Enterprise Core Engine

Welcome to the hiring challenge submission for the **Forward Deployed AI Energy Engineer** position, created by **Yash G.**

This repository presents a complete, data-driven, and algorithmically grounded pilot strategy for onboarding **Henkel's flagship headquarters plant in Düsseldorf-Holthausen**, alongside an enterprise-grade, fail-proof **Industrial Energy Optimization Core Engine** (`sample_energy_os.py`) reusable for future DAX-40 client deployments.

---

## 📌 Executive Navigation & Key Entry Points

1. **📄 [SUBMISSION_REPORT.md](file:///d:/RIZM_Challenge/SUBMISSION_REPORT.md)**: **THE CORE DELIVERABLE**. Contains the executive write-up addressing:
   - Grounded business use cases in **€ / metric ton** of detergent produced.
   - The single most load-bearing data request and single key stakeholder meeting strategy.
   - Multi-variable sensitivity analysis (€/ton confidence matrix: P10 to P90 bounds).
   - Methodological trade-offs, MILP shadow pricing, and explicit toolchain disclosure.
2. **🏗️ [SYSTEM_ARCHITECTURE.md](file:///d:/RIZM_Challenge/SYSTEM_ARCHITECTURE.md)**: **SINGLE SOURCE OF TRUTH (SSOT)** detailing 84 MW CHP parameters, thermal load limits, district heat links, MILP formulation, and agent verification checkpoints.
3. **💻 [sample_energy_os.py](file:///d:/RIZM_Challenge/sample_energy_os.py)**: Reusable CLI Engine for Forward Deployed AI Energy Engineers.
4. **🔄 [run_full_pipeline.py](file:///d:/RIZM_Challenge/run_full_pipeline.py)**: Automated end-to-end master pipeline execution script.
5. **⚡ [app.py](file:///d:/RIZM_Challenge/app.py)**: Interactive Streamlit web application dashboard.

---

## 🏆 Key Challenge Results & Summary Metrics

* **Target Facility**: Henkel AG & Co. KGaA (Düsseldorf-Holthausen site, 400,000 t/a production volume, 84 MW captive gas CHP plant, Stadtwerke Düsseldorf district heating export link).
* **Primary Optimization Metric**: **€ / metric ton of product saved**.

| Financial / Operational Metric | Base Case Scenario | P10 (Pessimistic) | P90 (Optimistic) |
|---|---|---|---|
| **Daily Net Cost Savings (€)** | **€11,860.00 / day** | €4,120.50 / day | €18,450.00 / day |
| **SAVINGS PER METRIC TON (€/ton)** | **€10.82 / metric ton** | **€3.76 / ton** | **€16.84 / ton** |
| **Annualized EBITDA Impact (€/yr)** | **€4.33 Million / year** | €1.50 Million / yr | €6.73 Million / yr |
| **Daily CO2 Avoidance (tCO2e)** | **32.3 tons CO2 / day** | 18.5 tons / day | 45.2 tons / day |

---

## 📁 Enterprise Repository Structure

```
RIZM_Challenge/
├── README.md                     # Primary entry point & reviewer guide
├── SUBMISSION_REPORT.md          # Executive report, €/ton use cases & sensitivity
├── SYSTEM_ARCHITECTURE.md        # Single Source of Truth (SSOT) system specs
├── site_config.json              # Modular site configuration schema
├── sample_energy_os.py           # Reusable CLI engine for site onboarding
├── data_validator.py             # Fail-proof telemetry data quality validator
├── sensitivity_engine.py         # Multi-variable parameter sweep & shadow pricing
├── optimizer.py                  # PuLP MILP deterministic optimization engine
├── data_generator.py             # 96-interval (15-min) EPEX SPOT & load synthesizer
├── run_full_pipeline.py          # Master automated pipeline execution script
├── app.py                        # Interactive Streamlit dashboard
├── test_suite.py                 # Automated pytest unit test suite
├── requirements.txt              # Project Python dependencies
└── .github/workflows/ci.yml      # Automated GitHub Actions CI/CD pipeline
```

---

## 🛠️ Quickstart & Execution Instructions

### 1. Run Automated Full Pipeline Orchestrator (CLI)
Executes data validation, MILP optimization, sensitivity sweeps, unit testing, and exports `AUDIT_LEDGER.json`:
```bash
python run_full_pipeline.py
```

### 2. Run Site Onboarding CLI Directly
Onboard any facility configuration with sensitivity sweeps:
```bash
python sample_energy_os.py --config site_config.json --run-sensitivity --export-audit
```

### 3. Run Automated Pytest Verification Suite
```bash
python -m pytest test_suite.py -v
```

### 4. Launch Interactive Streamlit Web Dashboard
```bash
streamlit run app.py
```

---

## 🛠️ Toolchain & Methodology Transparency

In compliance with scorecard evaluation criteria:
* **AI Model & Reasoning**: Gemini 3.6 Flash (High) via Antigravity Agentic AI.
* **Optimization Engine**: Mixed-Integer Linear Programming (MILP) formulated in Python using `PuLP` (CBC solver).
* **Telemetry Sanitation**: `data_validator.py` with missing value linear interpolation and load bound clipping.
* **Sensitivity Engine**: `sensitivity_engine.py` performing 25-point Monte Carlo grid search across gas, carbon tax, and spot price volatility.
* **Visualization & UX**: `Streamlit` and `Plotly` dark-mode interface (`app.py`).
* **CI/CD & Version Control**: `Git` with structured commit logging and GitHub Actions workflow automation (`.github/workflows/ci.yml`).
