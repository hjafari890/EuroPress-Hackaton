import os
import subprocess
import fitz
import re

os.makedirs('solution/latex/figures', exist_ok=True)

with open('solution/engine/build_updated_2page_html.py', encoding='utf-8') as f:
    text2 = f.read()

with open('solution/docs/part1_weighing_concept_4page.html', encoding='utf-8') as f:
    text4 = f.read()

m1 = re.search(r'(<svg viewBox="0 0 380 160".*?</svg>)', text2, re.DOTALL)
m2 = re.search(r'(<svg viewBox="0 0 920 180".*?</svg>)', text2, re.DOTALL)
m3 = re.search(r'(<svg viewBox="0 0 920 220".*?</svg>)', text2, re.DOTALL)
m4 = re.search(r'(<svg viewBox="0 0 920 186".*?</svg>)', text4, re.DOTALL)

svgs = [
    ('fig1_hydraulic_signature', m1.group(1), 380, 160),
    ('fig2_cad_subframe_elevation', m2.group(1), 920, 180),
    ('fig3_rfid_aperture_tomography', m3.group(1), 920, 220),
    ('fig4_master_subframe_plan', m4.group(1), 920, 186),
]

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

for name, svg_code, w, h in svgs:
    html_content = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  @page {{ size: {w}px {h}px; margin: 0; }}
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ background: #0F172A; width: {w}px; height: {h}px; overflow: hidden; }}
  svg {{ width: 100%; height: 100%; display: block; }}
</style>
</head>
<body>
{svg_code}
</body>
</html>
"""
    tmp_html = f"solution/latex/figures/{name}_tmp.html"
    tmp_pdf = f"solution/latex/figures/{name}.pdf"
    png_out = f"solution/latex/figures/{name}.png"
    
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    abs_html = f"file:///{os.path.abspath(tmp_html).replace(os.sep, '/')}"
    abs_pdf = os.path.abspath(tmp_pdf)
    
    cmd = [
        edge_path,
        '--headless=new',
        '--disable-gpu',
        '--no-pdf-header-footer',
        f'--print-to-pdf={abs_pdf}',
        abs_html
    ]
    subprocess.run(cmd, check=True)
    
    # Render PDF to 300 DPI PNG using PyMuPDF
    doc = fitz.open(abs_pdf)
    page = doc[0]
    # Calculate scale factor for crisp rendering (target ~1800 px wide)
    scale = max(2.0, 1800.0 / w)
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    pix.save(png_out)
    doc.close()
    
    # Clean up temp html
    if os.path.exists(tmp_html):
        os.remove(tmp_html)
        
    print(f"Generated {png_out} and {tmp_pdf} ({pix.width}x{pix.height})")

print("All figures successfully exported!")
