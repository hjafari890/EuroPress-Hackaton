# Europress SMART Material Value Engine â€” Weigh at Source, Create Value

**Since AI Hackathon 2026 â€” Complete Submission Package (`Deliverables 1, 2 & 3`)**

> **Role Boundary & Synthetic Data Notice:** All data, prices, tariffs, and material credits in this repository are synthetic illustrations from the official `Europress_SMART_Material_Value_Engine_v1.0.1` dataset (`447` public devices, `52` customers, `20,934` collection events). Europress Group Oy is currently not a party to waste transport or treatment contracts. All automated recommendations require human review and approval.

---

## 1. Map of Required Hackathon Deliverables

| Deliverable | Weight | File / Location | Summary |
| :--- | :---: | :--- | :--- |
| **Deliverable `(1)`: Short Illustrated Weighing Concept** | `25%` | [`solution/docs/weighing_concept.md`](docs/weighing_concept.md) &amp; [`combi_duo_schematics.svg`](frontend/public/diagrams/combi_duo_schematics.svg) | 6-option sensor trade-off matrix, 2-Tier Universal Modular Architecture (`Tier 1 Lite` `â‚¬74` BOM `Â±4.5%`; `Tier 2 Verify` `â‚¬192` BOM `Â±2.6%`), `COMBI` (`â‰¤22 mÂ³`) rear shear-pins, `DUO` (`â‰¤30 mÂ³`) stationary rail pads + locking-hook clevis pins (zero container wires), 2-stage auto-calibration, error budget, and 1-day Kerava factory test plan. |
| **Deliverable `(2)`: Working Software Demo &amp; Analytics Engine** | `35%` (`20%` + `15%`) | [`solution/frontend/index.html`](frontend/index.html), [`solution/backend/app.py`](backend/app.py), [`solution/engine/smart_value_engine.py`](engine/smart_value_engine.py) | Interactive **Europress SMART Web Cockpit** + physics-aware solvers for Tasks `A`, `B`, `B2`, `C`, `C2`, `"Empty Only When Truly Full"` Bulk-Density &amp; Lead-Time Optimizer (`S39`/`S40`), Day-0 Source-Weight Receipt Ledger, and Human-in-the-Loop Approval Queue. |
| **Deliverable `(3)`: Customer Value &amp; Business Case Report** | `40%` (`25%` + `10%` + `5%`) | [`solution/docs/business_case_report.md`](docs/business_case_report.md) &amp; [`team_business_params.yaml`](configs/team_business_params.yaml) | Quantified portfolio value (`â‚¬1,196,422/yr` identified, `â‚¬815,914/yr` realisable across `52` customers), lightweight 2-stage commercial model, SMART productisation pathway, 100% permissive OSS license table, and explicit assumptions/limitations. |

---

## 2. Quick-Start Setup & Running the Demo (`< 30 seconds`)

### Prerequisites
- Python `3.11+` (tested on Python `3.13`, Windows PowerShell)
- Dependencies installed via:
  ```powershell
  pip install -e "provided data from company/Europress_SMART_Material_Value_Engine_v1.0.1_PARTICIPANTS (3)/Europress_SMART_Material_Value_Engine_v1.0.1[dev]" fastapi uvicorn httpx
  ```

### Launch the Interactive Web Cockpit
Run our one-click PowerShell launcher from the repository root:
```powershell
.\solution\run_demo.ps1
```
Or start `uvicorn` directly:
```powershell
python -m uvicorn solution.backend.app:app --host 127.0.0.1 --port 8000
```
Then open **`http://localhost:8000`** in your browser.

---

## 3. Reproducing All Benchmark Scores & Predictions (`Tasks A, B, B2, C, C2`)

To re-run our upgraded solvers against the official starter kit baselines (`B1`â€“`B6`) and score every task with `europress_data.evaluate`:
```powershell
python solution\engine\run_benchmark_suite.py
```
This outputs CSV predictions to `solution/predictions/` and writes the official score comparison to `solution/backend/data/benchmark_scores.json`:

| Task | Metric | Official Baseline | SMART Value Engine (Ours) |
| :--- | :--- | :---: | :---: |
| **Task A** | Net Material Contribution Exact-to-Cent | `96.35%` (`B1`) | **`99.37%`** |
| **Task B** | Anomaly Macro-F1 / False-Positive Traps | `0.7309` (`117` FPs) | **`0.7638` (`52` FPs)** |
| **Task B** | `PREMATURE_UNJUSTIFIED` / `CONTAMINATION` F1 | `0.7164` / `0.7634` | **`0.8650` / `0.9971`** |
| **Task B2** | Operator Scorecard (`0â€“100`) | `67.75` (`B5`) | **`77.28`** |
| **Task C** | Acceptable Share / Impermissible Share | `58.11%` / `10.27%` (`B3`) | **`67.92%` / `1.71%`** |
| **Task C2** | Mean Regret (`â‚¬`) / Value Capture Share | `â‚¬240.07` / `77.43%` (`B6`) | **`â‚¬3.46` / `99.68%`** |

### Re-running Compliance & API Verification
```powershell
python solution\engine\verify_compliance.py
```

