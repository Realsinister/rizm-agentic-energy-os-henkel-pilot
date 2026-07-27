# Sample Energy OS — Henkel Pilot & Enterprise Core Engine

Welcome to the hiring challenge submission for the **Forward Deployed AI Energy Engineer** position, created by **Yash G.**

This repository presents a complete, data-driven, and algorithmically grounded pilot strategy for onboarding **Henkel's flagship headquarters plant in Düsseldorf-Holthausen**, alongside an enterprise-grade, fail-proof **Industrial Energy Optimization Core Engine** (`src/sample_energy_os.py`) structured for future DAX-40 client deployments.

---

## 🌐 Live Interactive Process & Commercial Pitch Deck (GitHub Pages)

👉 **[Launch Interactive Web Infographic & Pitch Deck (index.html)](file:///d:/RIZM_Challenge/index.html)**

*(When pushed to GitHub, enable GitHub Pages under Repository Settings -> Pages to serve `index.html` as a live shareable website link for recruiters and executives!)*

---

## 📌 Executive Navigation & Key Entry Points

1. **🌐 [index.html (Interactive Infographic & Pitch Deck)](file:///d:/RIZM_Challenge/index.html)**: Interactive visual flowchart, OSINT asset map, live ROI simulator, and commercial FDE strategy.
2. **📄 [SUBMISSION_REPORT.md](file:///d:/RIZM_Challenge/SUBMISSION_REPORT.md)**: **THE CORE DELIVERABLE**. Contains the executive write-up addressing:
   - Grounded business use cases in **€ / metric ton** of detergent produced.
   - The single most load-bearing data request and single key stakeholder meeting strategy.
   - Multi-variable sensitivity analysis (€/ton confidence matrix: P10 to P90 bounds).
   - Methodological trade-offs, MILP shadow pricing, and explicit toolchain disclosure.
3. **🏗️ [SYSTEM_ARCHITECTURE.md](file:///d:/RIZM_Challenge/SYSTEM_ARCHITECTURE.md)**: **SINGLE SOURCE OF TRUTH (SSOT)** detailing 84 MW CHP parameters, thermal load limits, district heat links, MILP formulation, and agent verification checkpoints.
4. **⚡ [Sample Energy OS.bat](file:///d:/RIZM_Challenge/Sample%20Energy%20OS.bat)**: **1-CLICK LAUNCHER**. Instantly installs dependencies and opens the interactive Streamlit dashboard.
5. **💻 [src/sample_energy_os.py](file:///d:/RIZM_Challenge/src/sample_energy_os.py)**: Reusable CLI Engine for Forward Deployed AI Energy Engineers.
6. **🔄 [src/run_full_pipeline.py](file:///d:/RIZM_Challenge/src/run_full_pipeline.py)**: Automated end-to-end master pipeline execution script.

---

## 🏆 Key Challenge Results & Summary Metrics (Exact MILP Optimizer Output)

* **Target Facility**: Henkel AG & Co. KGaA (Düsseldorf-Holthausen site, 400,000 t/a production volume, 84 MW captive gas CHP plant, Stadtwerke Düsseldorf district heating export link).
* **Primary Optimization Metric**: **€ / metric ton of product saved**.

| Financial / Operational Metric | Base Case Scenario (Default) | P10 (Pessimistic) | P90 (Optimistic) |
|---|---|---|---|
| **Daily Net Cost Savings (€)** | **€5,981.71 / day** (3.77%) | €1,621.92 / day | €24,252.05 / day |
| **SAVINGS PER METRIC TON (€/ton)** | **€5.46 / metric ton** | **€1.48 / ton** | **€22.13 / ton** |
| **Annualized EBITDA Impact (€/yr)** | **€2.18 Million / year** | €0.59 Million / yr | €8.85 Million / yr |
| **Daily CO2 Avoidance (tCO2e)** | **38.12 tons CO2 / day** | 18.5 tons / day | 52.4 tons / day |

---

## 📁 Clean Enterprise Repository Structure

```
RIZM_Challenge/
├── index.html                     # Interactive Web Infographic & Pitch Deck (GitHub Pages)
├── README.md                      # Primary entry point & reviewer guide
├── SUBMISSION_REPORT.md           # Executive report, €/ton use cases & sensitivity
├── SYSTEM_ARCHITECTURE.md         # Single Source of Truth (SSOT) system specs
├── site_config.json               # Modular site configuration schema
├── Sample Energy OS.bat           # 1-Click Windows Batch Launcher for Dashboard
├── requirements.txt               # Dependencies
├── .gitignore                     # Git ignore rules
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # GitHub Actions CI/CD pipeline
│
├── src/                           # Core Python source package
│   ├── __init__.py
│   ├── sample_energy_os.py        # Reusable CLI site onboarding engine
│   ├── optimizer.py               # PuLP MILP deterministic solver
│   ├── data_generator.py          # 15-min profile dataset synthesizer
│   ├── data_validator.py          # Telemetry sanitation & quality validator
│   ├── sensitivity_engine.py      # Monte Carlo & shadow pricing engine
│   ├── run_full_pipeline.py       # Master pipeline orchestrator
│   └── app.py                     # Streamlit executive dashboard UI
│
├── tests/                         # Automated unit test suite
│   ├── __init__.py
│   └── test_suite.py              # Pytest verification suite
│
├── data/                          # Generated datasets & audit ledgers
│   ├── industrial_energy_profile.csv
│   ├── sensitivity_matrix_results.csv
│   ├── sensitivity_summary.json
│   └── AUDIT_LEDGER.json
│
└── docs/                          # Reference challenge documentation & GitHub Pages
    ├── index.html                 # Copy of interactive web infographic for /docs deploy
    ├── RIZM Challenge Case.md
    └── RIZM Challenge Deep Research.md
```

---

## 🛠️ Installation & Running Instructions

### 🚀 Option A: 1-Click Dashboard Launch (Recommended for Windows)
Simply double-click **`Sample Energy OS.bat`** (or run `.\Sample Energy OS.bat` in your terminal). It will automatically check Python dependencies, install any missing packages, and open the interactive Streamlit dashboard in your default browser at `http://localhost:8501`.

---

### 💻 Option B: Manual CLI Execution

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Launch Interactive Streamlit Web Dashboard
```bash
streamlit run src/app.py
```

#### 3. Run Automated Full Pipeline Orchestrator (CLI)
Executes data validation, MILP optimization, sensitivity sweeps, unit testing, and exports `data/AUDIT_LEDGER.json`:
```bash
python src/run_full_pipeline.py
```

#### 4. Run Automated Pytest Verification Suite
```bash
pytest tests/test_suite.py -v
```

---

## 🛠️ Toolchain & Methodology Transparency

In compliance with scorecard evaluation criteria:
* **AI Model & Reasoning**: Gemini 3.6 Flash (High) via Antigravity Agentic AI.
* **Optimization Engine**: Mixed-Integer Linear Programming (MILP) formulated in Python using `PuLP` (CBC solver).
* **Telemetry Sanitation**: `src/data_validator.py` with missing value linear interpolation and load bound clipping.
* **Sensitivity Engine**: `src/sensitivity_engine.py` performing 100-point Monte Carlo grid search across gas, carbon tax, and spot price volatility.
* **Visualization & UX**: `Streamlit` and `Plotly` dark-mode interface (`src/app.py`).
* **CI/CD & Version Control**: `Git` with structured commit logging and GitHub Actions workflow automation (`.github/workflows/ci.yml`).
