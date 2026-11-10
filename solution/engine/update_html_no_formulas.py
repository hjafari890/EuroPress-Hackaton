import os

path = r'solution/docs/part1_weighing_concept_3page.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace formula-box in Concept 1
old_formula_box = '''        <div class="formula-box">
          <strong>Work:</strong> <i>W</i><sub>total</sub> = &Sigma;<sub><i>k</i>=1..<i>N</i></sub> <i>A</i><sub>cyl</sub> &int; <i>P<sub>k</sub></i>(<i>t</i>)&middot;<i>v</i><sub>ram</sub> d<i>t</i> &nbsp;&nbsp;|&nbsp;&nbsp;
          <strong>Relaxation [1]:</strong> (<i>P</i><sub>0</sub>&middot;<i>t</i>) / (<i>P</i><sub>0</sub> &minus; <i>P</i>(<i>t</i>)) = <i>k</i><sub>1</sub> + <i>k</i><sub>2</sub>&middot;<i>t</i> &nbsp;&rArr;&nbsp;
          <strong>Mass:</strong> <i>m&#770;</i> = <i>V</i><sub>SMART</sub> &middot; <i>&rho;&#770;</i>(<i>W</i><sub>total</sub>, <i>&tau;</i><sub>rel</sub>, <i>k</i><sub>1</sub>, <i>k</i><sub>2</sub>)
        </div>'''

new_formula_box = '''        <div class="formula-box" style="font-family: inherit; font-size: 7.5pt; background: #EFF6FF; border-left: 3px solid #0284C7; color: #1E3A8A; padding: 4px 8px;">
          <strong>Measurement Principle Summary:</strong> Total Mechanical Work (during forward ram stroke) + Viscoelastic Rebound Speed (during ram retraction) &rarr; Material Bulk Density (kg/m&sup3;) &rarr; Multiplied by known container volume (m&sup3;) to calculate net waste payload (kg).
        </div>'''

c = c.replace(old_formula_box, new_formula_box)

# 2. In Concept 1 text, simplify mentions of tau_rel, Peleg, etc.
c = c.replace('(<em>&tau;<sub>rel</sub></em>)', '(Rebound Time)')
c = c.replace('(short <em>&tau;<sub>rel</sub></em>)', '(fast pressure drop)')
c = c.replace('(long <em>&tau;<sub>rel</sub></em>, high asymptotic modulus <em>1/k<sub>2</sub></em>)', '(prolonged slow relaxation)')
c = c.replace('tuning material constants (<i>k</i><sub>1</sub>, <i>k</i><sub>2</sub>)', 'tuning material compression curves')
c = c.replace('constants \\((k_1, k_2)\\)', 'calibration curves')

# 3. In Fig 1.1 SVG
c = c.replace('W = &int; P(t)&middot;A&middot;v dt', 'Total Stroke Energy Area')
c = c.replace('Slow plastic decay (Long &tau;_rel, high 1/k&#8322;)', 'Slow plastic decay (Dense waste)')
c = c.replace('Fast elastic spring-back (Short &tau;_rel)', 'Fast elastic rebound (Springy waste)')
c = c.replace('&larr; Decompression Window &Delta;t_rel &rarr;', '&larr; Pressure Rebound Window &rarr;')

# 4. In Fig 1.2 SVG
c = c.replace('m&middot;g&middot;cos(&theta;) + &Delta;F_z,Slope', 'Gravity Vector (Slope Compensated)')
c = c.replace('Equilibrium: m = (F_z,front + F_z,rear) / (g &middot; cos &theta;_pitch &middot; cos &theta;_roll)', 'Weight Calculation: Front Support Force + Rear Axle Force (Corrected for Ground Slope)')
c = c.replace('DUO Equilibrium: m = (F_z,HookPins + F_z,RailPads) / (g &middot; cos &theta;_IMU)', 'DUO Weight Calculation: Press Locking Hook Force + Rear Wheel Pad Force (Zero Box Wires)')

# 5. In Concept 2 text
c = c.replace('(<i>x</i><sub>cog</sub>: 0.35<i>L</i> &rarr; 0.62<i>L</i>)', '(shifts from front press toward rear door)')
c = c.replace('4-point summation + IMU cos(<i>&theta;<sub>p</sub></i>)cos(<i>&theta;<sub>r</sub></i>) eliminates lever-arm &amp; slope errors (<code>&plusmn;1.3% 1&sigma;</code>)', '4-point summation + IMU tilt angle compensation eliminates center-of-gravity shifts and slope errors (accuracy &plusmn;1.3% 1-sigma)')

# 6. In Concept 3 text (Page 2)
c = c.replace('Since <strong>Weight = Known Volume (<i>V</i><sub>SMART</sub>) &times; Density (<i>&rho;</i>)</strong>', 'Since <strong>Weight = Known Volume &times; Material Density</strong>')
c = c.replace('Phase Delay (&Delta;&phi;):', 'Wave Speed Delay:')
c = c.replace('(<i>&epsilon;\'</i> &approx; 2.2) slows wave speed &rArr; <strong>Dry Density (<i>&rho;</i><sub>dry</sub>)</strong>.', 'Packed dry material slows down radio waves &rarr; Measures <strong>Dry Recyclable Density</strong>.')
c = c.replace('Signal Drop (&Delta;RSSI):', 'Signal Energy Absorption:')
c = c.replace('(<i>&epsilon;\'</i> &approx; 80, <i>&epsilon;\'\'</i> &approx; 12) absorbs RF energy &rArr; <strong>Water Density (<i>&rho;</i><sub>water</sub>)</strong>.', 'Water strongly absorbs radio wave energy &rarr; Measures <strong>Moisture / Water Weight</strong>.')
c = c.replace('verify &Delta;&phi; &times; <i>V</i><sub>SMART</sub> mass', 'verify measured mass vs. reference scale')

# 7. In Fig 2.1 SVG
c = c.replace('RF Wave Measures Bulk Permittivity &epsilon;* &rarr; Dry Density &rho;_dry + Water &rho;_water', 'Radio Waves Measure Material Density + Moisture Absorption Across Compactor Length')
c = c.replace('Backscatter Return: Phase Shift &Delta;&phi; (Slow Wave = High Density) + RSSI Drop &Delta;P (Attenuation = Water)', 'Signal Feedback: Wave Delay indicates Density &middot; Signal Absorption indicates Water Content')
c = c.replace('Total Mass: m_total = V_SMART &times; (&rho;_dry + &rho;_water) &nbsp;|&nbsp; Dry Credit Mass: m_dry = V_SMART &times; &rho;_dry', 'System Output: Total Payload Weight (kg) + Dry Recyclable Fibre Mass (kg) + Moisture Content (%)')
c = c.replace('Permittivity &epsilon;* = &epsilon;\' &minus; j&epsilon;\'\'', 'Material Density &amp; Moisture')
c = c.replace('Couples into PIFA Near-Field', 'Couples into Antenna Field')

# 8. In Master Blueprint Fig 3.1 & Page 3 Table
c = c.replace('Phase &Delta;&phi; + RSSI + Container ID', 'Wave Delay + Absorption + Container ID')
c = c.replace('Forward work &int;<i>P&middot;v</i> d<i>t</i> + Peleg&ndash;Moreyra relaxation <i>&tau;</i><sub>rel</sub>', 'Compaction Energy + Pressure Rebound Timing')
c = c.replace('868 MHz phase (&Delta;&phi;) + RSSI (&Delta;<i>P</i>) over known <i>V</i><sub>SMART</sub>', '868 MHz Wave Delay (Density) + Absorption (Moisture)')
c = c.replace('4-point vertical summation (&Sigma; <i>F<sub>z,i</sub></i>)', '4-Point full structural force summation')
c = c.replace('3-axis IMU cos(<i>&theta;<sub>p</sub></i>)cos(<i>&theta;<sub>r</sub></i>) + weight transfer', '3-Axis IMU pitch/roll ground slope correction')
c = c.replace('relaxation curve <i>&tau;</i><sub>rel</sub> tracks density', 'pressure rebound timing tracks density')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Updated HTML successfully!')
