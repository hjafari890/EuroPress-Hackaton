path = r'solution/docs/part1_weighing_concept_3page.html'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line 638 (0-indexed 637) is the UHMW-PE text at y=96
# We can put it right inside the strip at y=55 or change y from 96 to 55, and height of rect to 15!
for i, l in enumerate(lines):
    if '<rect x="157" y="45" width="436" height="14"' in l:
        lines[i] = '        <rect x="157" y="44" width="436" height="15" fill="#082F49" stroke="#38BDF8" stroke-width="1.2"/>\n'
    if 'y="96" fill="#38BDF8" font-size="7"' in l:
        lines[i] = '        <text x="375" y="55" fill="#BAE6FD" font-size="6.8" font-weight="bold" text-anchor="middle">15 mm Chamfered UHMW-PE Protective Wear Rail (Protects Recessed Tags from Sliding Trash)</text>\n'
    if 'Tag #5 (Air Zone)' in l and 'y="84"' in l:
        lines[i] = lines[i].replace('y="84"', 'y="68"')
    if 'Forward work' in l and 'relaxation' in l and '<td>' in l:
        lines[i] = '            <td>Compaction Energy (Forward Stroke) + Pressure Rebound Timing</td>\n'

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Direct line replacement complete")
