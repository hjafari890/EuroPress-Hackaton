import os
import subprocess
import shutil
import fitz  # PyMuPDF

html_path = os.path.abspath('solution/docs/part1_weighing_concept_3page.html')
pdf_root_path = os.path.abspath('Europress_Part1_Weighing_Concept_3Page.pdf')
pdf_docs_path = os.path.abspath('solution/docs/Europress_Part1_Weighing_Concept_3Page.pdf')

edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
if not os.path.exists(edge_bin):
    edge_bin = 'msedge.exe'

cmd = [
    edge_bin,
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_root_path}',
    html_path
]

print('Running Edge headless CLI...')
res = subprocess.run(cmd, capture_output=True, text=True)
print('Edge exit code:', res.returncode)

if not os.path.exists(pdf_root_path):
    raise FileNotFoundError(f'Failed to generate {pdf_root_path}')

shutil.copyfile(pdf_root_path, pdf_docs_path)
print(f'Copied PDF to {pdf_docs_path}')

# Check page count and render PNGs
doc = fitz.open(pdf_root_path)
print(f'Total pages in generated PDF: {len(doc)}')

os.makedirs('solution/docs/photos', exist_ok=True)

# Render at 3x scale (~216 DPI)
matrix = fitz.Matrix(3.0, 3.0)

for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    root_png = f'Europress_Part1_Weighing_Concept_Page_{i+1}.png'
    doc_png = f'solution/docs/photos/page_{i+1}.png'
    pix.save(root_png)
    pix.save(doc_png)
    print(f'Rendered Page {i+1}: {pix.width}x{pix.height}px -> {root_png} & {doc_png}')

print('Artifact rendering completed successfully!')
