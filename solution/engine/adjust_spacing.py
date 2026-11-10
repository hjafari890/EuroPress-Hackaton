path = r'solution/docs/part1_weighing_concept_3page.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Let's adjust the y positions in Fig 2.1 Panel A:
c = c.replace(
    '<text x="16" y="19" fill="#F8FAFC" font-size="8.8" font-weight="bold">A. LONGITUDINAL CUTAWAY — READER IN PRESS THROAT LOOKING INTO STEEL CONTAINER</text>',
    '<text x="16" y="16" fill="#F8FAFC" font-size="8.4" font-weight="bold">A. LONGITUDINAL CUTAWAY — READER IN PRESS THROAT LOOKING INTO STEEL CONTAINER</text>'
)
c = c.replace(
    '<text x="375" y="24" fill="#CBD5E1" font-size="7.2" font-weight="bold" text-anchor="middle">5 mm S355 STEEL CONTAINER WALLS (Acts as Closed RF Waveguide Cavity &mdash; Zero External Leakage)</text>',
    '<text x="375" y="27" fill="#CBD5E1" font-size="7" font-weight="bold" text-anchor="middle">5 mm S355 STEEL CONTAINER WALLS (Acts as Closed RF Waveguide Cavity &mdash; Zero External Leakage)</text>'
)
c = c.replace(
    '<text x="375" y="36" fill="#38BDF8" font-size="7" font-weight="bold" text-anchor="middle">&uarr; 15 mm Chamfered UHMW-PE Wear Rail (Tags Recessed Flush Inside) &uarr;</text>',
    '<text x="375" y="38" fill="#38BDF8" font-size="6.8" font-weight="bold" text-anchor="middle">&uarr; 15 mm Chamfered UHMW-PE Wear Rail (Tags Recessed Flush Inside) &uarr;</text>'
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Adjusted Page 2 header spacing')
