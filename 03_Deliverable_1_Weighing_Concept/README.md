# 03 Deliverable 1: Weighing Concept Design & Specifications

This folder contains the complete deliverables for **Part 1 (Weighing Concept)** of the Europress Since AI 2026 Challenge.

## Proposed Weighing Architectures

1. **Option 1: Zero-Hardware Virtual Sensor (Compaction & Rebound)**
   - *Hardware BOM:* **€0.00** (100% software upgrade in existing SMART PLC)
   - *Accuracy:* ±4.5% to ±6.0% error on payload mass
   - *Principle:* Computes integral hydraulic ram work \(W = \int P \cdot A \, dx\) and decompressive rebound relaxation rate upon stroke release.
2. **Option 2: Factory-Calibrated Subframe Shear-Beam Load Cell Array**
   - *Hardware BOM:* **~€1,850** (4x IP68 C3 alloy steel shear-beam load cells, summing box, isolation mounts)
   - *Accuracy:* ±0.5% calibrated static accuracy (OIML R60 compliant)
   - *Principle:* True gravimetric payload measurement integrated into the compactor base chassis with mechanical shock absorption.
3. **Option 3: Dynamic RFID Aperture Tomography**
   - *Hardware BOM:* **~€620** (Dual UHF RFID reader modules + 4 phased patch antennas at bin feed aperture)
   - *Accuracy:* ±1.2% density-calibrated tracking with 100% operator tag auditability
   - *Principle:* Continuous volumetric density estimation combined with operator authentication at the loading door.

---

## Directory Organization

```
03_Deliverable_1_Weighing_Concept/
├── Final_Reports_PDF/        # Published publication-ready PDFs
│   ├── Europress_Part1_Weighing_Concept_Master.pdf   # Complete specification report
│   ├── Europress_Part1_Weighing_Concept_2Page.pdf    # Concise 2-page executive summary
│   └── Europress_Part1_Weighing_Concept_3Page.pdf    # 3-page expanded edition
├── Page_Previews_PNG/        # High-resolution page renders
│   ├── Europress_Part1_Weighing_Concept_Page_1.png   # Page 1: Executive Summary & Concepts 1 & 2
│   ├── Europress_Part1_Weighing_Concept_Page_2.png   # Page 2: Concept 3 & Comparative Decision Matrix
│   ├── Europress_Part1_Weighing_Concept_Page_3.png   # Page 3: Engineering Appendix (BOM & Schematics)
│   └── Europress_Part1_Weighing_Concept_Page_4.png   # Page 4: Engineering Appendix (Protocols & Validation)
├── LaTeX_Package/            # LaTeX source bundle
│   └── Europress_Part1_Weighing_Concept_LaTeX.zip    # Complete LaTeX package (tex, figures, styles)
└── Specifications/           # Technical draft and specification markdown
    └── WEIGHING_CONCEPT_DRAFT.md
```

## Additional Resources
For raw LaTeX source files and vector diagrams, visit [`solution/latex/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/latex/).
For interactive HTML versions, visit [`solution/docs/`](file:///d:/Academic%20Resources/Oulu/period%205/EuroPress-Hackaton/solution/docs/).
