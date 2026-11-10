import os
import zipfile

zip_filename = 'Europress_Part1_Weighing_Concept_LaTeX.zip'
latex_dir = 'solution/latex'

# Create a clean README for the zip
readme_content = """# Europress SMART-Weight — Part 1 Source Weighing LaTeX Package

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
"""

with open(os.path.join(latex_dir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(readme_content)

files_to_zip = [
    'main.tex',
    'main.pdf',
    'README.md',
    'figures/fig1_hydraulic_signature.pdf',
    'figures/fig1_hydraulic_signature.png',
    'figures/fig2_cad_subframe_elevation.pdf',
    'figures/fig2_cad_subframe_elevation.png',
    'figures/fig3_rfid_aperture_tomography.pdf',
    'figures/fig3_rfid_aperture_tomography.png',
    'figures/fig4_master_subframe_plan.pdf',
    'figures/fig4_master_subframe_plan.png',
    'previews/latex_page_1.png',
    'previews/latex_page_2.png',
    'previews/latex_page_3.png',
    'previews/latex_page_4.png',
]

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for rel_path in files_to_zip:
        full_path = os.path.join(latex_dir, rel_path)
        if os.path.exists(full_path):
            zipf.write(full_path, arcname=rel_path)
            print(f"Added {rel_path} to zip")

# Also copy zip to solution/docs/
import shutil
shutil.copyfile(zip_filename, os.path.join('solution/docs', zip_filename))

print(f"Successfully created {zip_filename} ({os.path.getsize(zip_filename)} bytes)")
