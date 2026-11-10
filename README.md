# Europress SMART Material Value Engine — Weigh at Source, Create Value

**Since AI Hackathon 2026 (Turku, Finland) — Team Solution & Complete Submission Package**

![Europress COMBI and DUO Universal Modular Weighing Architecture](solution/frontend/public/diagrams/combi_duo_schematics.svg)

> **Role Boundary & Synthetic Data Notice:** All data, prices, tariffs, and material credits in this repository are synthetic illustrations from the official `Europress_SMART_Material_Value_Engine_v1.0.1` dataset (447 public devices, 52 customers, 20,934 collection events). Europress Group Oy is currently not a party to waste transport or treatment contracts. All automated recommendations require human review and approval.

---

## Repository Navigation Map

The repository is organized into dedicated, self-explanatory directories:

```
EuroPress-Hackaton/
│
├── 01_Presentations_and_Pitch/           # Official PowerPoint slide decks
│   ├── Final_Pitch_Deck.pptx             # Final hackathon submission pitch presentation
│   ├── Weight_Measuring_Techniques.pptx  # Technical presentation on sensor & weighing methods
│   └── README.md                         # Presentation overview and guide
│
├── 02_Demo_and_Pitch_Videos/             # Full presentation recordings and demo videos
│   ├── Final_Pitch_Full_Presentation_2m50s.mp4   # Complete pitch presentation (143 MB, 2m50s)
│   ├── SMART_Weight_Concept_Demo_1m30s.mp4       # Video walkthrough of SMART-Weight concept
│   ├── Weight_Measuring_Techniques_Demo_58s.mp4  # Video walkthrough of weighing techniques
│   ├── Hamid_Pitch_Segment_41s.mp4               # Individual presentation recording segment
│   ├── Final_Pitch_Rehearsal_Clip_45s.mp4        # Presentation rehearsal clip
│   ├── Cockpit_Screen_Recording_11s.mp4          # Short UI screen capture of the cockpit
│   └── README.md                                 # Guide to video files, timestamps, and roles
│
├── 03_Deliverable_1_Weighing_Concept/    # Part 1: Weighing system engineering specifications
│   ├── Final_Reports_PDF/                # Publication-ready PDF specifications
│   │   ├── Europress_Part1_Weighing_Concept_Master.pdf   # Complete specification report
│   │   ├── Europress_Part1_Weighing_Concept_2Page.pdf    # Concise 2-page executive summary
│   │   └── Europress_Part1_Weighing_Concept_3Page.pdf    # 3-page expanded edition
│   ├── Page_Previews_PNG/                # High-resolution rendered page images (Pages 1-4)
│   ├── LaTeX_Package/                    # Complete compiled LaTeX package & schematics (.zip)
│   ├── Specifications/                   # Technical draft & architectural notes
│   └── README.md                         # Architecture summary & sensor trade-off matrix
│
├── 04_Competition_Brief_and_Rules/       # Official challenge brief & problem statement
│   ├── Europress_SinceAI_2026_Challenge_Brief.pdf
│   └── README.md                         # Summary of tasks, requirements & evaluation rubrics
│
├── 05_Handoff_and_Development_Notes/     # Multi-agent handoffs, brainstorming & sprint progress
│   ├── ANTIGRAVITY_SESSION_HANDOFF.md    # Multi-agent developer handoff document
│   ├── antigravity_session_handoff.zip   # Backup archive of handoff files
│   ├── BUSINESS_CASE.md                  # Commercial value calculations and ROI assumptions
│   ├── EXPLAINABILITY.md                 # Explainability frameworks for AI decisions
│   ├── PROGRESS.md                       # Sprint progress and milestone tracking
│   ├── task_d_e_brainstorming.md         # Brainstorming notes for Tasks D & E
│   ├── my_params.yaml                    # Custom parameter configuration
│   └── README.md                         # Description of handoff files
│
├── 06_Partner_Repositories/              # Upstream and teammate reference repositories
│   ├── europress_repo/                   # Teammate repository clone (Sharan Sapkota)
│   └── README.md                         # Cross-reference documentation
│
├── solution/                             # Deliverables 2 & 3: Codebase, Models & Cockpit Dashboard
│   ├── backend/                          # FastAPI REST API & audit services
│   ├── frontend/                         # Modern React + Vite interactive dashboard
│   ├── engine/                           # Analytics, simulation, ML models & figure generators
│   ├── predictions/                      # Deliverable 2 submission CSVs (Tasks A, B, B2, C, C2)
│   ├── business_case_out/                # Deliverable 3 scenario outputs & customer ROI tables
│   ├── configs/                          # Scenario parameters and profile configurations
│   ├── docs/                             # Engineering specs, HTML reports & briefings
│   ├── latex/                            # LaTeX build workspace and vector schematics
│   └── README.md                         # Comprehensive architecture documentation
│
├── provided data from company/           # Official starter kit and competition dataset
│   ├── Europress_SMART_Material_Value_Engine_v1.0.1_PARTICIPANTS (3).zip
│   └── Europress_SMART_Material_Value_Engine_v1.0.1_PARTICIPANTS (3)/
│
├── run_cockpit.bat                       # One-click Windows CMD launcher
├── run_cockpit.py                        # Cross-platform Python launcher (auto-port & browser open)
├── run_demo.ps1                          # PowerShell launcher
├── README.md                             # Main repository guide
└── .gitignore                            # Git ignore configuration
```

---

## One-Click Demo Quickstart (< 30 seconds)

You can launch the full interactive **Europress SMART Web Cockpit** with a single click or command directly from the repository root:

### Option A: Windows Batch Launcher (Double-Click)
Double-click [`run_cockpit.bat`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/run_cockpit.bat) in File Explorer or run in CMD:
```cmd
run_cockpit.bat
```

### Option B: Cross-Platform Python Launcher
Automatically detects an available open port (8000, 8001, 8080, etc.), boots the server, and automatically opens your default browser:
```powershell
python run_cockpit.py
```

### Option C: PowerShell Launcher
```powershell
.\run_demo.ps1
```

Once running, navigate to **`http://localhost:8000`** (or the port detected by the launcher).

---

## Hackathon Deliverables Summary

| Deliverable | Weight | Location | Key Highlights |
| :--- | :---: | :--- | :--- |
| **Deliverable 1: Weighing Concept** | **25%** | [`03_Deliverable_1_Weighing_Concept/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/03_Deliverable_1_Weighing_Concept/) | 3-tier modular architecture: **Zero-Hardware Virtual Sensor** (€0 BOM, ±4.5%), **Subframe Shear-Beam Load Cell Array** (~€1,850 BOM, ±0.5%), and **Dynamic RFID Aperture Tomography** (~€620 BOM, ±1.2%). Full LaTeX specifications, OIML R60 compliance, and 1-day factory validation protocol. |
| **Deliverable 2: SMART Value Engine** | **35%** | [`solution/engine/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/engine/) & [`solution/predictions/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/predictions/) | Machine learning & analytical solvers for **Task A** (Fill-level prediction), **Task B** (Invoice anomaly detection), **Task B2** (Operator scorecard), **Task C** (Next-best collection decision), and **Task C2** (Prescriptive operator actions). |
| **Deliverable 3: Interactive Web Cockpit & Business Case** | **40%** | [`solution/frontend/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/frontend/) & [`solution/docs/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/docs/) | Full-featured executive dashboard with real-time fleet overview, interactive invoice dispute resolver, operator performance scorecard, what-if ROI simulator (€815k/yr realisable savings across 52 customers), and human-in-the-loop audit logging. |

---

## Verified Benchmark Scores (`competition` Dataset)

Evaluated using the official competition harness via [`solution/engine/run_benchmark_suite.py`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/engine/run_benchmark_suite.py):

| Task | Metric | Official Baseline (B1–B6) | Our SMART Value Engine | Improvement |
| :--- | :--- | :---: | :---: | :--- |
| **Task A** | Net Material Contribution Exact-to-Cent | `96.35%` (B1) | **`99.37%`** | **83% error reduction** (recovers Grade B credits & de-duplicates mismatch lines) |
| **Task A** | Fabricated €/t where Reference Null | `3` (B1) | **`1`** | Detects zero-net stored-tare invoices on per-tonne contracts |
| **Task B** | Anomaly Macro-F1 / False-Positive Traps | `0.7309` (117 FPs) | **`0.7638` (52 FPs)** | **56% fewer trap false positives**; catches S39 (4h lead) & S40 (bridging) |
| **Task B** | `PREMATURE` / `COST_HIGH` / `CONTAM` F1 | `0.716` / `0.773` / `0.763` | **`0.865` / `0.876` / `0.997`** | Suppresses `MIN_CHARGE_TOPUP` & justified early lifts |
| **Task B2** | Operator Scorecard (0–100) | `67.75` (B5) | **`77.28`** | **`+9.53 pts`** (`weight_bias_pct` score `0.021 -> 0.658`) |
| **Task C** | Acceptable Share / Impermissible Share | `58.11%` / `10.27%` (B3) | **`67.92%` / `1.71%`** | **`+9.81%` acceptable share** & **83% fewer constraint violations** |
| **Task C2** | Mean Regret (€) / Value Capture Share | `€240.07` / `77.43%` (B6) | **`€3.46` / `99.68%`** | **98.6% regret reduction** (99.68% optimal value capture) |

---

## Team & Project Information
- **Event:** Since AI Hackathon 2026 (Turku, Finland)
- **Challenge Sponsor:** Europress Group Oy
- **Challenge:** Weigh at Source, Create Value
