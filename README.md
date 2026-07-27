# RIZM Forward Deployed AI Energy Engineer Challenge — Henkel Pilot

Welcome to the RIZM challenge submission for the **Forward Deployed AI Energy Engineer** position, created by **Yash G.**

This repository presents a complete, data-driven, and algorithmically grounded pilot strategy for onboarding **Henkel's flagship headquarters plant in Düsseldorf-Holthausen** into RIZM's Agentic Energy OS.

---

## 📌 Executive Navigation & Entry Points

1. **📄 [SUBMISSION_REPORT.md](file:///d:/RIZM_Challenge/SUBMISSION_REPORT.md)**: **THE CORE DELIVERABLE**. Contains the complete write-up addressing:
   - Grounded business use cases in **€ / metric ton** of detergent produced.
   - The single most load-bearing data request and single key stakeholder meeting strategy.
   - Methodological trade-offs, back-of-the-envelope math, and toolchain declaration.
2. **🏗️ [SYSTEM_ARCHITECTURE.md](file:///d:/RIZM_Challenge/SYSTEM_ARCHITECTURE.md)**: **SINGLE SOURCE OF TRUTH (SSOT)** detailing the 84 MW CHP parameters, thermal load limits, district heating export links, mathematical MILP formulation, and multi-agent verification checkpoints.
3. **⚡ [app.py](file:///d:/RIZM_Challenge/app.py)**: Interactive Streamlit web application dashboard simulating RIZM's Agentic Energy OS.
4. **🧮 [optimizer.py](file:///d:/RIZM_Challenge/optimizer.py)**: Deterministic Mixed-Integer Linear Programming (MILP) dispatch solver engine using `PuLP`.

---

## 🏆 Key Challenge Results & Summary Metrics

* **Target Facility**: Henkel AG & Co. KGaA (Düsseldorf-Holthausen site, 400,000 t/a production volume, 84 MW captive gas CHP plant, Stadtwerke Düsseldorf district heating export link).
* **Primary Optimization Metric**: **€ / metric ton of product saved**.

| Financial / Operational Metric | Unoptimized Baseline | RIZM Agentic OS | Net Savings / Impact |
|---|---|---|---|
| **Daily Operational Cost (€)** | €74,210.00 / day | €62,350.00 / day | **€11,860.00 / day** (16.0% reduction) |
| **Normalized Cost Metric (€/ton)** | €67.72 / ton | €56.90 / ton | **€10.82 / metric ton saved** |
| **Annualized EBITDA Impact (€/yr)** | €27.08 Million / yr | €22.75 Million / yr | **€4.33 Million / year saved** |
| **Daily CO2 Emissions (tCO2e)** | 240.5 tons / day | 208.2 tons / day | **32.3 tons CO2 / day reduced** |

---

## 📁 Repository Structure

```
RIZM_Challenge/
├── README.md                     # Primary entry point & reviewer guide
├── SUBMISSION_REPORT.md          # Comprehensive executive report & €/ton use cases
├── SYSTEM_ARCHITECTURE.md        # SSOT system parameters & math formulation
├── requirements.txt              # Project Python dependencies
├── data_generator.py             # 96-interval (15-min) EPEX SPOT & load synthesizer
├── optimizer.py                  # PuLP MILP optimization engine
├── app.py                        # Streamlit interactive dashboard UI
├── test_suite.py                 # Automated pytest unit test suite
└── .gitignore                    # Version control exclusions
```

---

## 🛠️ Quickstart & Running Instructions

### 1. Install Dependencies
Ensure Python 3.10+ is installed, then run:
```bash
pip install -r requirements.txt
```

### 2. Run Automated Unit Tests
Verify energy balance equations and solver convergence:
```bash
python -m pytest test_suite.py -v
```

### 3. Run Optimization Engine (CLI Mode)
Generate the profile dataset and compute optimized dispatch:
```bash
python optimizer.py
```

### 4. Launch Interactive Streamlit Dashboard
Launch the web interface to experiment with sliders for gas prices, carbon tax, and spot price volatility:
```bash
streamlit run app.py
```

---

## 🛠️ Toolchain & Methodology Transparency

In compliance with RIZM scorecard evaluation criteria:
* **AI Model & Reasoning**: Gemini 3.6 Flash (High) via Antigravity Agentic AI for deep contextual research, prompt formulation, and architectural design.
* **Optimization Engine**: Mixed-Integer Linear Programming (MILP) formulated in Python using `PuLP` (CBC solver).
* **Data Synthesis**: `pandas` & `numpy` modeling 96 discrete 15-minute intervals reflecting EPEX SPOT solar price depressions and morning/evening demand peaks.
* **Visualization & UX**: `Streamlit` and `Plotly` dark-mode charts.
* **Version Control**: `Git` tracking modular phase development.
