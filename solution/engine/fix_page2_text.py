path = r'solution/docs/part1_weighing_concept_3page.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '5 mm S355 STEEL CONTAINER WALLS' in l:
        lines[i] = '        <text x="375" y="24" fill="#CBD5E1" font-size="7.2" font-weight="bold" text-anchor="middle">5 mm S355 STEEL CONTAINER WALLS (Acts as Closed RF Waveguide Cavity &mdash; Zero External Leakage)</text>\n'
    if '15 mm Chamfered UHMW-PE' in l and '<text' in l:
        lines[i] = '        <text x="375" y="36" fill="#38BDF8" font-size="7" font-weight="bold" text-anchor="middle">&uarr; 15 mm Chamfered UHMW-PE Wear Rail (Tags Recessed Flush Inside) &uarr;</text>\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Page 2 text position adjusted!")
