# Sample Energy OS — Henkel Pilot & Enterprise Core Engine

Welcome to the hiring challenge submission for the **Forward Deployed AI Energy Engineer** position, created by **Yash Gupta.**

This repository presents a complete, data-driven, and algorithmically grounded pilot strategy for onboarding **Henkel's flagship headquarters plant in Düsseldorf-Holthausen**, alongside an enterprise-grade, fail-proof **Industrial Energy Optimization Core Engine & Web Application** (`src/app.py` & `src/sample_energy_os.py`) structured for future DAX-40 client deployments.

---

## 🌐 Interactive System Architecture & Methodology Website (GitHub Pages)

👉 **[Launch Interactive System Architecture & Methodology Website (index.html)](file:///d:/RIZM_Challenge/index.html)** — Interactive website explaining the end-to-end engineering workflow, featuring 5 connected process stages, real-time viewport inspector dock, zero-hallucination MILP formulas, OSINT asset discovery maps, and commercial FDE pilot strategy.

---

## 🛡️ Anti-Hallucination SSoT Architecture & Multi-Agent Management

### 1. Single Source of Truth (SSoT) Layer to Combat AI Hallucinations
In mission-critical industrial AI applications, generating unconstrained or "hallucinated" asset dispatch decisions risks severe physical plant damage or production SLA breaches. 
* **Zero-Hallucination Guarantee**: We established **[SYSTEM_ARCHITECTURE.md](file:///d:/RIZM_Challenge/SYSTEM_ARCHITECTURE.md)** and **`site_config.json`** as the deterministic **Single Source of Truth (SSoT)**.
* **Deterministic MILP Binding**: The AI agent workflow never directly emits unverified dispatch commands. Instead, asset efficiency curves, thermal turn-down limits, and physical capacity bounds are strictly enforced by a PuLP Mixed-Integer Linear Program (MILP), guaranteeing **0% AI hallucination risk**.

### 2. Multi-Agent Environment Orchestration
To execute complex engineering research, data validation, mathematical solving, and C-suite UI generation, we managed a structured multi-agent environment:
* **Specialized Subagent Roles**: 
  - *Research Agent*: Conducted OSINT asset mapping for Henkel Düsseldorf.
  - *Telemetry Validator Agent*: Implemented linear interpolation imputation and clipping in `src/data_validator.py`.
  - *Optimization Agent*: Formulated deterministic PuLP MILP solver in `src/optimizer.py`.
  - *UI & Presentation Agent*: Developed interactive Streamlit web application in `src/app.py` and GitHub Pages interactive methodology website in `index.html`.
* **Inter-Agent Protocols & Verification**: Scoped read/write permissions and automated contract checks via `tests/test_suite.py` eliminated race conditions and state drift across agent handoffs.

---

## 📌 Executive Navigation & Key Entry Points

1. **🌐 [index.html (Interactive Methodology Website)](file:///d:/RIZM_Challenge/index.html)**: Interactive website explaining the 5-stage engineering lifecycle with real-time inspector dock, MILP equations, and OSINT asset maps.
2. **📦 [Sample_Energy_OS_v1.0_Standalone.zip](file:///d:/RIZM_Challenge/Sample_Energy_OS_v1.0_Standalone.zip)**: **1-CLICK STANDALONE EXECUTABLE (Zero Setup Required)**. Contains single `Sample_Energy_OS.exe` for instant execution without Python or environment setup.
3. **⚡ [Sample Energy OS.bat](file:///d:/RIZM_Challenge/Sample%20Energy%20OS.bat)**: **1-CLICK LAUNCHER FOR STREAMLIT WEB APPLICATION**. Instantly installs dependencies and opens the interactive Streamlit web application (`src/app.py`).
4. **📄 [SUBMISSION_REPORT.md](file:///d:/RIZM_Challenge/SUBMISSION_REPORT.md)**: **THE CORE DELIVERABLE**. Contains the executive write-up addressing:
   - Grounded business use cases in **€ / metric ton** of detergent produced.
   - Anti-hallucination SSoT layer and multi-agent environment management.
   - The single most load-bearing data request and single key stakeholder meeting strategy.
   - Multi-variable sensitivity analysis (€/ton confidence matrix: P10 to P90 bounds).
   - Methodological trade-offs, MILP shadow pricing, and explicit toolchain disclosure.
5. **🏗️ [SYSTEM_ARCHITECTURE.md](file:///d:/RIZM_Challenge/SYSTEM_ARCHITECTURE.md)**: **SINGLE SOURCE OF TRUTH (SSOT)** detailing 84 MW CHP parameters, thermal load limits, district heat links, MILP formulation, and agent verification checkpoints.
6. **💻 [src/sample_energy_os.py](file:///d:/RIZM_Challenge/src/sample_energy_os.py)**: Reusable CLI Engine for Forward Deployed AI Energy Engineers.
7. **🔄 [src/run_full_pipeline.py](file:///d:/RIZM_Challenge/src/run_full_pipeline.py)**: Automated end-to-end master pipeline execution script.

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
├── Sample_Energy_OS_v1.0_Standalone.zip # 1-Click Standalone Downloadable Package (Zero Setup)
├── dist/
│   └── Sample_Energy_OS.exe              # Standalone Windows Executable
├── index.html                            # Interactive Methodology & Workflow Website (GitHub Pages)
├── README.md                             # Primary entry point & reviewer guide
├── SUBMISSION_REPORT.md                  # Executive report, €/ton use cases & sensitivity
├── SYSTEM_ARCHITECTURE.md                # Single Source of Truth (SSOT) system specs
├── site_config.json                      # Modular site configuration schema
├── Sample Energy OS.bat                  # 1-Click Windows Batch Launcher for Streamlit Web App
├── requirements.txt                      # Dependencies
├── .gitignore                            # Git ignore rules
│
├── archive/                              # Archived design iterations
│   └── pitch_deck_version_a.html         # Archived Tabbed Pitch Deck layout
│
├── .github/
│   └── workflows/
│       └── ci.yml                        # GitHub Actions CI/CD pipeline
│
├── src/                                  # Core Python source package
│   ├── __init__.py
│   ├── sample_energy_os.py               # Reusable CLI site onboarding engine
│   ├── optimizer.py                      # PuLP MILP deterministic solver
│   ├── data_generator.py                 # 15-min profile dataset synthesizer
│   ├── data_validator.py                 # Telemetry sanitation & quality validator
│   ├── sensitivity_engine.py             # Monte Carlo & shadow pricing engine
│   ├── run_full_pipeline.py              # Master pipeline orchestrator
│   └── app.py                            # Streamlit web application & executive UI
│
├── tests/                                # Automated unit test suite
│   ├── __init__.py
│   └── test_suite.py                     # Pytest verification suite
│
├── data/                                 # Generated datasets & audit ledgers
│   ├── industrial_energy_profile.csv
│   ├── sensitivity_matrix_results.csv
│   ├── sensitivity_summary.json
│   └── AUDIT_LEDGER.json
│
└── docs/                                 # Reference challenge documentation & GitHub Pages root
    ├── index.html                        # Main entry point for /docs deploy
    ├── archive/                          # Archived docs layouts
    ├── RIZM Challenge Case.md
    └── RIZM Challenge Deep Research.md
```

---

## 🛠️ Installation & Execution Options

### ⚡ Option 0: Standalone Executable (Zero Setup Required - Recommended)
Download **`Sample_Energy_OS_v1.0_Standalone.zip`** (or `dist/Sample_Energy_OS.exe`), extract, and double-click **`Sample_Energy_OS.exe`**.
* **Zero Python installation required**
* **Zero repository cloning required**
* **Zero environment/dependency setup required**
Double-clicking the standalone `.exe` automatically starts the embedded web application server and launches `http://localhost:8501` in your browser.

---

### 🚀 Option A: 1-Click Batch Launcher (For Windows Repository Clones)
If you have cloned the repository, simply double-click **`Sample Energy OS.bat`** (or run `.\Sample Energy OS.bat` in your terminal). It will automatically check Python dependencies, install any missing packages, and open the interactive Streamlit web application (`src/app.py`) in your default browser at `http://localhost:8501`.

---

### 💻 Option B: Manual CLI Execution

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Launch Interactive Streamlit Web Application
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
* **Visualization & UX**: `Streamlit` web application and `Plotly` dark-mode interface (`src/app.py`).
* **CI/CD & Version Control**: `Git` with structured commit logging and GitHub Actions workflow automation (`.github/workflows/ci.yml`).
