# System Architecture & Single Source of Truth (SSOT)
## RIZM Agentic Energy OS — Henkel Düsseldorf Pilot

---

### 1. Executive Context & Ground-Truth Facility Profile
* **Target Facility**: Henkel AG & Co. KGaA — Global Headquarters & Manufacturing Site, Düsseldorf-Holthausen.
* **Annual Output**: ~400,000 metric tons of Laundry & Home Care / Adhesive / Industrial products.
* **Primary Generation Asset**: On-site 84 MW gas-fired Combined Heat & Power (CHP) power station.
* **Thermal Infrastructure**: Spray-drying towers (heavy constant baseload), plus a 700 m² waste-heat recovery center connected to a 3.6 km district heating pipeline supplying municipal heat to Garath, Benrath, and Holthausen (cooperation with Stadtwerke Düsseldorf & Bilfinger).
* **Sustainability & Emissions**: CO2 reduction commitment of ~6,500 tons/yr via district heat integration; goal of net-zero production impact.

---

### 2. Physical & Mathematical Parameters (Model SSOT)

| Parameter Name | Symbol | Value | Unit | Description / Constraint |
|---|---|---|---|---|
| **Annual Production** | $Q_{\text{annual}}$ | 400,000 | metric tons/yr | Facility product volume baseline |
| **Daily Production** | $Q_{\text{daily}}$ | 1,095.89 | metric tons/day | $400,000 / 365$ |
| **CHP Max Electrical** | $P_{\text{chp, max}}$ | 84.0 | MW | Maximum electrical power output of gas CHP turbine |
| **CHP Min Stable Load** | $P_{\text{chp, min}}$ | 20.0 | MW | Minimum operational turn-down capacity |
| **Heat-to-Power Ratio** | $\eta_{\text{htp}}$ | 1.20 | MWt / MWe | Thermal output per MW of electrical output |
| **Gas Electrical Efficiency**| $\eta_{\text{elec}}$ | 0.42 | - | Electrical conversion efficiency |
| **Gas Thermal Efficiency** | $\eta_{\text{therm}}$ | 0.504 | - | Thermal conversion efficiency ($0.42 \times 1.2$) |
| **Electrical Demand** | $D_{\text{elec}}$ | 45.0 | MW | Constant Spray-drying & Plant electrical load ($\pm 2.0$ MW stochastic) |
| **Thermal Demand** | $D_{\text{therm}}$ | 60.0 | MWt | Industrial process thermal demand |
| **District Heat Export Cap** | $H_{\text{dh, max}}$ | 30.0 | MWt | Max thermal feed capacity to Garath/Benrath grid |
| **Natural Gas Price** | $C_{\text{gas}}$ | 40.0 | EUR/MWh (therm) | Wholesale baseline gas price |
| **Auxiliary Boiler Price** | $C_{\text{boiler}}$ | 55.0 | EUR/MWh (therm) | Marginal cost of backup peak boiler |
| **District Heat Tariff** | $R_{\text{dh}}$ | 28.0 | EUR/MWh (therm) | Commercial feed-in revenue offset |
| **Carbon Intensity Gas** | $\sigma_{\text{gas}}$ | 0.202 | tCO2e / MWh (therm) | Natural gas emission factor |
| **Carbon Penalty / EUA** | $C_{\text{co2}}$ | 85.0 | EUR / tCO2e | European Union Allowance carbon shadow price |

---

### 3. Mathematical Optimization Formulation (MILP)

#### Time Discretization
$\Delta t = 0.25 \text{ hours}$ (15-minute intervals), $T = 96 \text{ intervals}$ (24-hour horizon).

#### Decision Variables (for each $t \in [1, T]$)
* $P_{\text{chp}}(t) \ge 0$: Electrical output of CHP plant (MW).
* $P_{\text{grid}}(t) \ge 0$: Grid electricity imported (MW).
* $u_{\text{chp}}(t) \in \{0, 1\}$: Binary status of CHP (1 = On, 0 = Off).
* $H_{\text{chp}}(t) = \eta_{\text{htp}} \times P_{\text{chp}}(t)$: Thermal output of CHP (MWt).
* $H_{\text{dh}}(t) \ge 0$: Heat exported to district heating network (MWt).
* $H_{\text{boiler}}(t) \ge 0$: Thermal output of auxiliary gas boiler (MWt).
* $F_{\text{gas}}(t) = P_{\text{chp}}(t) / \eta_{\text{elec}}$: Gas consumed by CHP (MWh thermal per hour).
* $F_{\text{boiler}}(t) = H_{\text{boiler}}(t) / 0.90$: Gas consumed by aux boiler (MWh thermal per hour).

#### Constraint Equations
1. **CHP Turn-down Limit**:
   $$u_{\text{chp}}(t) \cdot P_{\text{chp, min}} \le P_{\text{chp}}(t) \le u_{\text{chp}}(t) \cdot P_{\text{chp, max}}$$
2. **Electrical Demand Conservation**:
   $$P_{\text{chp}}(t) + P_{\text{grid}}(t) = D_{\text{elec}}(t)$$
3. **Thermal Demand Conservation**:
   $$H_{\text{chp}}(t) + H_{\text{boiler}}(t) = D_{\text{therm}}(t) + H_{\text{dh}}(t)$$
4. **District Heating Export Capacity**:
   $$0 \le H_{\text{dh}}(t) \le H_{\text{dh, max}}$$

#### Objective Function
Minimize total 24-hour operational expenditure:
$$\text{Minimize } Z = \sum_{t=1}^{T} \left[ F_{\text{gas}}(t) \cdot C_{\text{gas}} \cdot \Delta t + F_{\text{boiler}}(t) \cdot C_{\text{boiler}} \cdot \Delta t + P_{\text{grid}}(t) \cdot C_{\text{spot}}(t) \cdot \Delta t - H_{\text{dh}}(t) \cdot R_{\text{dh}} \cdot \Delta t + \text{CarbonPenalty}(t) \right]$$

Where:
$$\text{CarbonPenalty}(t) = \left( F_{\text{gas}}(t) + F_{\text{boiler}}(t) \right) \cdot \sigma_{\text{gas}} \cdot C_{\text{co2}} \cdot \Delta t$$

#### Key Performance Indicator (€/ton)
$$\Delta \text{Cost per ton} = \frac{Z_{\text{baseline}} - Z_{\text{optimized}}}{Q_{\text{daily}}}$$

---

### 4. Multi-Agent System Architecture & Verification Checkpoints

```
                   +---------------------------------------+
                   |      SYSTEM_ARCHITECTURE.md (SSOT)    |
                   +---------------------------------------+
                                       |
        +------------------------------+------------------------------+
        |                              |                              |
        v                              v                              v
[Data Analyst Agent]         [OR Optimization Agent]       [Strategic & UI Agent]
(Synthetic 96-interval data)   (MILP PuLP Solver engine)    (Streamlit + Executive Report)
        |                              |                              |
        v                              v                              v
industrial_energy_profile.csv      optimizer.py + test_suite.py     app.py + SUBMISSION_REPORT.md
        |                              |                              |
        +------------------------------+------------------------------+
                                       |
                                       v
                     [Checkpoint & Automated Test Suite]
                         (pytest test_suite.py GREEN)
```

#### Checkpoints to Prevent Hallucinations & Drift:
1. **Data Integrity Checkpoint**: `data_generator.py` must output exactly 96 rows, non-null, with negative EPEX prices during solar hours and peak pricing in morning/evening.
2. **Energy Conservation Checkpoint**: `test_suite.py` asserts that $P_{\text{chp}} + P_{\text{grid}} \equiv D_{\text{elec}}$ and $H_{\text{chp}} + H_{\text{boiler}} \equiv D_{\text{therm}} + H_{\text{dh}}$ for every single interval.
3. **Financial Logic Checkpoint**: `optimizer.py` must prove $Z_{\text{optimized}} < Z_{\text{baseline}}$ and calculate exact normalized €/ton detergent saved.
4. **Git Versioning Checkpoint**: Commit state cleanly at each completed milestone.
