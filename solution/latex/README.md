# Europress SMART-Weight — Part 1 Source Weighing LaTeX Package

This package contains the complete, compilable LaTeX project for Deliverable (1) of the Europress "SMART Material Value Engine" hackathon challenge.

## Package Contents:
- `main.tex`: Master LaTeX document (4-page executive summary + engineering appendix)
- `main.pdf`: Compiled 4-page publication-grade PDF
- `figures/`: Vector PDF and high-res PNG diagrams:
  - `fig1_hydraulic_signature.pdf` (Option 1: Compaction work & decompression relaxation curve)
  - `fig2_cad_subframe_elevation.pdf` (Option 2: COMBI & DUO sensor placement CAD blueprint)
  - `fig3_rfid_aperture_tomography.pdf` (Option 3: 16-tag on-metal PIFA RFID aperture tomography)
  - `fig4_master_subframe_plan.pdf` (Top-down subframe blueprint & edge-to-cloud comms architecture)
- `previews/`: PNG preview images of all 4 rendered pages

## How to Compile:
### Option A: Local Command Line (MiKTeX / TeX Live)
```bash
pdflatex main.tex
```

### Option B: Overleaf / Cloud LaTeX
1. Upload this `.zip` file directly to Overleaf (`New Project` -> `Upload Project`).
2. Set compiler to `pdfLaTeX` (default).
3. Click `Recompile`.
