import os
import subprocess
import shutil
import fitz

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Europress SMART-Weight — Part 1 Source Weighing Concept & Engineering Blueprint</title>
<style>
  @page {
    size: A4 portrait;
    margin: 0;
  }
  * {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, Helvetica, Arial, sans-serif;
    color: #0F172A;
    background: #FFFFFF;
    font-size: 7.35pt;
    line-height: 1.21;
  }
  .page {
    width: 210mm;
    height: 297mm;
    padding: 4.5mm 8.5mm 3.5mm 8.5mm;
    page-break-after: always;
    position: relative;
    overflow: hidden;
    background: #FFFFFF;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
  .page:last-child {
    page-break-after: auto;
  }

  /* Header Bar */
  .header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #0F172A;
    color: #FFFFFF;
    padding: 3.8px 9px;
    border-radius: 4px;
    border-left: 5px solid #DC2626;
    margin-bottom: 3.5px;
  }
  .header-left h1 {
    font-size: 10.0pt;
    font-weight: 800;
    letter-spacing: 0.2px;
    color: #F8FAFC;
  }
  .header-left p {
    font-size: 6.9pt;
    color: #94A3B8;
  }
  .header-right {
    text-align: right;
  }
  .badge-page {
    background: #DC2626;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 6.8pt;
    padding: 1.8px 6px;
    border-radius: 3px;
    display: inline-block;
    margin-bottom: 1px;
  }
  .header-right .sub {
    font-size: 6.5pt;
    color: #CBD5E1;
    display: block;
  }

  /* Concept Banner */
  .concept-banner {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #F1F5F9;
    border: 1px solid #CBD5E1;
    border-left: 4px solid #0284C7;
    border-radius: 4px;
    padding: 2.5px 7px;
    margin-bottom: 3.5px;
  }
  .concept-banner.tier2 {
    border-left-color: #DC2626;
    background: #FEF2F2;
    border-color: #FECACA;
  }
  .concept-banner.tier3 {
    border-left-color: #7C3AED;
    background: #F5F3FF;
    border-color: #DDD6FE;
  }
  .concept-title {
    font-size: 8.6pt;
    font-weight: 800;
    color: #0F172A;
  }
  .concept-pills {
    display: flex;
    gap: 4px;
  }
  .pill {
    font-size: 6.6pt;
    font-weight: 700;
    padding: 1.2px 5.5px;
    border-radius: 3px;
    background: #0F172A;
    color: #FFFFFF;
    white-space: nowrap;
  }
  .pill.green { background: #059669; }
  .pill.blue { background: #0284C7; }
  .pill.red { background: #DC2626; }
  .pill.purple { background: #7C3AED; }

  /* Grid Layouts */
  .grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 5px;
  }
  .grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 5px;
  }
  .grid-60-40 {
    display: grid;
    grid-template-columns: 1.42fr 1fr;
    gap: 5px;
  }
  .grid-55-45 {
    display: grid;
    grid-template-columns: 1.25fr 1fr;
    gap: 5px;
  }

  /* Cards */
  .card {
    border: 1px solid #CBD5E1;
    border-radius: 4px;
    padding: 3.5px 6.5px;
    background: #FFFFFF;
  }
  .card h3 {
    font-size: 7.5pt;
    font-weight: 800;
    color: #0F172A;
    border-bottom: 1.5px solid #E2E8F0;
    padding-bottom: 1.5px;
    margin-bottom: 2.5px;
    text-transform: uppercase;
    letter-spacing: 0.2px;
  }
  .card h3 span.accent { color: #DC2626; }
  .card h3 span.blue { color: #0284C7; }
  .card h3 span.purple { color: #7C3AED; }

  ul {
    padding-left: 10.5px;
    margin-bottom: 1px;
  }
  li {
    margin-bottom: 1.3px;
    font-size: 7.05pt;
  }
  li strong {
    color: #0F172A;
  }

  /* Formula / Principle Box */
  .formula-box {
    background: #F8FAFC;
    border: 1px solid #CBD5E1;
    border-left: 3px solid #0284C7;
    border-radius: 3px;
    padding: 2.5px 5.5px;
    margin: 2px 0;
    font-size: 7.05pt;
    color: #0F172A;
    line-height: 1.2;
  }

  /* Tables */
  table {
    width: 100%;
    border-collapse: collapse;
    font-size: 6.8pt;
    margin-top: 1px;
  }
  th {
    background: #1E293B;
    color: #FFFFFF;
    text-align: left;
    padding: 2.0px 3.5px;
    font-weight: 700;
  }
  td {
    padding: 1.8px 3.5px;
    border-bottom: 1px solid #E2E8F0;
    vertical-align: top;
  }
  tr:nth-child(even) td {
    background: #F8FAFC;
  }
  tr.total-row td {
    background: #FEF2F2;
    font-weight: 800;
    border-top: 1.5px solid #DC2626;
    border-bottom: 1.5px solid #DC2626;
    color: #991B1B;
  }
  tr.total-row.purple td {
    background: #F5F3FF;
    border-top-color: #7C3AED;
    border-bottom-color: #7C3AED;
    color: #5B21B6;
  }

  /* Blueprint Frame */
  .blueprint-box {
    background: #0B1120;
    border: 1.5px solid #334155;
    border-radius: 4px;
    padding: 3.5px 5px;
    color: #F8FAFC;
  }
  .blueprint-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #1E293B;
    padding-bottom: 1.5px;
    margin-bottom: 2px;
    font-size: 6.8pt;
    font-weight: 700;
    color: #38BDF8;
    letter-spacing: 0.3px;
  }

  /* Footer / References */
  .footer {
    border-top: 1px solid #CBD5E1;
    padding-top: 2px;
    font-size: 6.1pt;
    color: #475569;
    display: flex;
    justify-content: space-between;
    align-items: flex-end;
    gap: 8px;
  }
  .refs {
    font-size: 6.0pt;
    color: #475569;
    line-height: 1.16;
  }
</style>
</head>
<body>

<!-- ===================================================================== -->
<!-- PAGE 1: CONCEPTS 1 & 2 (ZERO-HARDWARE SOFTWARE + MODULAR MECHANICAL)  -->
<!-- ===================================================================== -->
<div class="page">
  <div>
    <!-- Header -->
    <div class="header">
      <div class="header-left">
        <h1>EUROPRESS SMART-WEIGHT — PART 1 SOURCE WEIGHING ARCHITECTURE</h1>
        <p>Production-Ready Concepts for COMBI (&le;22 m&sup3;) &amp; DUO (&le;30 m&sup3; Swapped Container) Compactors</p>
      </div>
      <div class="header-right">
        <span class="badge-page">PAGE 1 OF 3 &middot; CONCEPTS 1 &amp; 2</span>
        <span class="sub">Since AI Hackathon 2026 &middot; Europress Group Oy</span>
      </div>
    </div>

    <!-- CONCEPT 1 BANNER -->
    <div class="concept-banner">
      <div class="concept-title">CONCEPT 1 — Zero-Hardware Virtual Sensor: Compaction Work + Decompression Relaxation</div>
      <div class="concept-pills">
        <span class="pill green">&euro;0 Hardware BOM</span>
        <span class="pill blue">Remote OTA Firmware Push</span>
        <span class="pill">&plusmn;8–10% Accuracy (Literature [1, 2])</span>
      </div>
    </div>

    <div class="grid-60-40" style="margin-bottom: 4px;">
      <div class="card">
        <h3><span class="blue">1A.</span> Sensor &amp; Measurement Principle (Existing SMART Signals Only)</h3>
        <ul>
          <li><strong>Zero New Hardware Required:</strong> Uses signals already sampled on every <code>Europress SMART</code> compactor: <strong>hydraulic cylinder pressure <em>P(t)</em></strong> (4–20 mA), <strong>piston cycle timer <em>t</em></strong>, and <strong>known fill volume <em>V<sub>SMART</sub></em> (&plusmn;4–5%)</strong>.</li>
          <li><strong>Stage 1 — Cumulative Forward Compaction Work:</strong> Peak pressure alone only indicates compaction resistance. Integrating hydraulic force over stroke displacement across all compaction cycles calculates total mechanical energy delivered per cubic meter <strong>[1, 2]</strong>. Denser materials require higher cumulative mechanical work.</li>
          <li><strong>Stage 2 — Decompression Rebound Speed (Peleg–Moreyra Relaxation [3]):</strong> At stroke completion and valve reversal, compressed material pushes back against the retracting ram. <strong>Light, springy waste</strong> (dry corrugated cardboard, loose film) rebounds rapidly (fast pressure decay). <strong>Dense, heavy waste</strong> (wet biowaste, packed fiber) undergoes plastic cell collapse and relaxes slowly (prolonged asymptotic relaxation).</li>
        </ul>
        <div class="formula-box" style="background: #EFF6FF; border-left: 3px solid #0284C7; color: #1E3A8A;">
          <strong>Measurement Principle Summary:</strong> Total Mechanical Work (during forward ram stroke) + Viscoelastic Rebound Decay Rate (during ram retraction) &rarr; Material Bulk Density (kg/m&sup3;) &rarr; Multiplied by known container volume (m&sup3;) to calculate net waste payload (kg).
        </div>
        <div class="grid-2" style="margin-top: 1.5px;">
          <ul>
            <li><strong>Installation Procedure:</strong> Deployed remotely over-the-air (OTA) to the SMART PLC via existing 4G/LTE modem. Automatically provisions telemetry variables and initializes energy-rebound algorithms without technician dispatch.</li>
            <li><strong>Calibration:</strong> Whenever haulers share weighbridge tickets (~73% of lifts), cloud algorithms tune site-specific compression curves for that material stream.</li>
          </ul>
          <ul>
            <li><strong>Error Sources &amp; Accuracy:</strong> Rigid uncrushed obstacles (wooden pallets) causing premature pressure spikes; mixed-waste density variation. Accuracy: <strong>&plusmn;8–10%</strong> (validated in academic literature <strong>[1, 2]</strong> for hydraulic compaction energy vs. refuse mass).</li>
            <li><strong>Factory Validation:</strong> Replay historical SMART pressure-time logs against 10,342 scale tickets + 20-cycle Kerava R&amp;D hall trial comparing dry cardboard vs. wet biowaste.</li>
          </ul>
        </div>
      </div>

      <!-- Concept 1 Blueprint Curve -->
      <div class="blueprint-box" style="display:flex; flex-direction:column; justify-content:space-between;">
        <div class="blueprint-header">
          <span>FIG 1.1 — HYDRAULIC WORK &amp; RELAXATION SIGNATURE</span>
          <span>PLC SAMPLE: 50 Hz</span>
        </div>
        <svg viewBox="0 0 380 160" width="100%" height="116">
          <rect x="34" y="6" width="336" height="122" fill="#0F172A" stroke="#334155" stroke-width="1"/>
          <line x1="34" y1="36" x2="370" y2="36" stroke="#1E293B" stroke-dasharray="3,3"/>
          <line x1="34" y1="67" x2="370" y2="67" stroke="#1E293B" stroke-dasharray="3,3"/>
          <line x1="34" y1="98" x2="370" y2="98" stroke="#1E293B" stroke-dasharray="3,3"/>
          <line x1="185" y1="6" x2="185" y2="128" stroke="#F59E0B" stroke-width="1.2" stroke-dasharray="4,2"/>
          <text x="11" y="68" fill="#94A3B8" font-size="7.0" transform="rotate(-90 11,68)" text-anchor="middle">Pressure P(t) [bar]</text>
          <text x="202" y="142" fill="#94A3B8" font-size="7.0" text-anchor="middle">Piston Stroke &amp; Decompression Time t [s]</text>
          <text x="30" y="14" fill="#64748B" font-size="6.5" text-anchor="end">180</text>
          <text x="30" y="70" fill="#64748B" font-size="6.5" text-anchor="end">90</text>
          <text x="30" y="126" fill="#64748B" font-size="6.5" text-anchor="end">0</text>

          <!-- Shaded Forward Work Area -->
          <path d="M 40 122 Q 90 116 130 77 Q 158 44 185 22 L 185 122 Z" fill="#0284C7" fill-opacity="0.28"/>
          <text x="118" y="100" fill="#38BDF8" font-size="7.6" font-weight="bold" text-anchor="middle">Forward Work Area</text>
          <text x="118" y="110" fill="#BAE6FD" font-size="6.6" text-anchor="middle">Total Stroke Energy</text>

          <!-- Curve 1: High-Density Heavy Mass -->
          <path d="M 40 122 Q 90 116 130 77 Q 158 44 185 22 Q 225 42 275 62 Q 320 74 362 78" fill="none" stroke="#10B981" stroke-width="2.3"/>
          <!-- Curve 2: Low-Density Springy Waste -->
          <path d="M 185 22 Q 202 81 232 112 L 362 120" fill="none" stroke="#EF4444" stroke-width="2" stroke-dasharray="5,3"/>

          <circle cx="185" cy="22" r="3.2" fill="#F59E0B"/>
          <text x="185" y="16" fill="#FDE68A" font-size="6.8" font-weight="bold" text-anchor="middle">Stroke End (P&#8320;)</text>

          <text x="278" y="42" fill="#10B981" font-size="7.0" font-weight="bold" text-anchor="middle">High Density (Heavy Mass)</text>
          <text x="278" y="52" fill="#A7F3D0" font-size="6.4" text-anchor="middle">Slow plastic decay (Dense waste)</text>

          <text x="282" y="98" fill="#F87171" font-size="7.0" font-weight="bold" text-anchor="middle">Low Density (Light / Hollow)</text>
          <text x="282" y="108" fill="#FECACA" font-size="6.4" text-anchor="middle">Fast elastic rebound (Springy waste)</text>

          <text x="272" y="154" fill="#FDE68A" font-size="6.8" font-weight="bold" text-anchor="middle">&larr; Pressure Rebound Window &rarr;</text>
        </svg>
      </div>
    </div>

    <!-- CONCEPT 2 BANNER -->
    <div class="concept-banner tier2">
      <div class="concept-title">CONCEPT 2 — Modular Heavy-Duty Shear Pins / Rail Pads + 3-Axis IMU Dynamic Weight-Transfer</div>
      <div class="concept-pills">
        <span class="pill red">&euro;192 (COMBI) / &euro;212 (DUO) BOM</span>
        <span class="pill blue">Modular Bolt-On Pin Kit</span>
        <span class="pill green">&plusmn;1.3% (1&sigma;) / &plusmn;2.6% (95%) Accuracy</span>
      </div>
    </div>

    <!-- Technical Blueprint for Concept 2 -->
    <div class="blueprint-box" style="margin-bottom: 4px;">
      <div class="blueprint-header">
        <span>FIG 1.2 — TECHNICAL BLUEPRINT: SENSOR PLACEMENT &amp; STRUCTURAL WEIGHT TRANSFER (COMBI vs. DUO)</span>
        <span>DATASHEET RATING: FLINTEC 10t / PIN (15t SAFE OVERLOAD &middot; 30t BREAK &middot; IP68/IP69K)</span>
      </div>
      <svg viewBox="0 0 920 180" width="100%" height="122">
        <defs>
          <marker id="arrR" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#EF4444"/>
          </marker>
          <marker id="arrG" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#10B981"/>
          </marker>
          <marker id="arrC" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#38BDF8"/>
          </marker>
          <marker id="arrY" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#F59E0B"/>
          </marker>
        </defs>

        <!-- LEFT HALF: COMBI MONOBLOCK (<=22 m3) -->
        <rect x="6" y="4" width="445" height="172" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="16" y="16" fill="#F8FAFC" font-size="8.4" font-weight="bold">A. COMBI MONOBLOCK (&le;22 m&sup3; — Press &amp; Container Joined as One Unit)</text>

        <line x1="20" y1="136" x2="435" y2="146" stroke="#64748B" stroke-width="2" stroke-dasharray="6,3"/>
        <text x="432" y="158" fill="#94A3B8" font-size="6.6" text-anchor="end">Bay Slope &theta; (1&deg;–4&deg;) Compensated by IMU</text>

        <path d="M 55 94 L 36 94 L 36 58 Q 36 48 46 48" fill="none" stroke="#94A3B8" stroke-width="3.5" stroke-linecap="round"/>
        <text x="22" y="44" fill="#94A3B8" font-size="6.5">DIN Hook</text>

        <rect x="55" y="56" width="95" height="68" rx="3" fill="#991B1B" stroke="#F87171" stroke-width="1.2"/>
        <text x="102" y="71" fill="#FFFFFF" font-size="7.4" font-weight="bold" text-anchor="middle">PRESS HEAD</text>
        <rect x="65" y="87" width="52" height="12" fill="#1E293B" stroke="#CBD5E1"/>
        <line x1="117" y1="93" x2="162" y2="93" stroke="#F59E0B" stroke-width="3.5" marker-end="url(#arrY)"/>
        <text x="102" y="110" fill="#FDE68A" font-size="6.5" text-anchor="middle">Ram 35–40t</text>

        <path d="M 150 36 L 395 36 L 415 124 L 150 124 Z" fill="#1E293B" stroke="#94A3B8" stroke-width="1.5"/>
        <text x="280" y="51" fill="#F8FAFC" font-size="7.8" font-weight="bold" text-anchor="middle">JOINED CONTAINER (Up to 22 m&sup3;)</text>

        <circle cx="275" cy="80" r="5" fill="#38BDF8"/>
        <line x1="235" y1="80" x2="320" y2="80" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="3,2" marker-end="url(#arrC)"/>
        <line x1="275" y1="80" x2="275" y2="116" stroke="#38BDF8" stroke-width="2" marker-end="url(#arrC)"/>
        <text x="282" y="74" fill="#38BDF8" font-size="6.8" font-weight="bold">C.o.G. Shifts Rearward (0.35L &rarr; 0.62L)</text>
        <text x="284" y="108" fill="#BAE6FD" font-size="6.6">Gravity Vector (Slope Compensated)</text>

        <rect x="60" y="24" width="84" height="25" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1.2"/>
        <text x="102" y="35" fill="#38BDF8" font-size="6.8" font-weight="bold" text-anchor="middle">[S3] SMART PLC + IMU</text>
        <text x="102" y="44" fill="#E2E8F0" font-size="6.2" text-anchor="middle">Honeywell TARS-IMU (&plusmn;0.3&deg;)</text>

        <!-- Front Support Foot + Puck [S1] -->
        <rect x="70" y="124" width="22" height="14" rx="2" fill="#10B981" stroke="#A7F3D0" stroke-width="1.5"/>
        <line x1="81" y1="144" x2="81" y2="116" stroke="#10B981" stroke-width="2" marker-end="url(#arrG)"/>
        <text x="98" y="135" fill="#10B981" font-size="6.8" font-weight="bold">[S1] 2&times; Front Elastomer Pucks (10t)</text>

        <!-- Rear Roller + Shear Pin [S2] -->
        <circle cx="388" cy="134" r="10" fill="#334155" stroke="#CBD5E1" stroke-width="2"/>
        <circle cx="388" cy="134" r="4" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.2"/>
        <line x1="388" y1="150" x2="388" y2="116" stroke="#EF4444" stroke-width="2" marker-end="url(#arrR)"/>
        <text x="372" y="135" fill="#F87171" font-size="6.8" font-weight="bold" text-anchor="end">[S2] 2&times; Flintec CC1 &Oslash;45mm Pins (10t)</text>

        <text x="228" y="168" fill="#E2E8F0" font-size="6.8" font-weight="bold" text-anchor="middle">Weight Calculation: Front Support Force + Rear Axle Force (Corrected for Ground Slope)</text>

        <!-- RIGHT HALF: DUO STATIONARY COMPACTOR (<=30 m3) -->
        <rect x="462" y="4" width="452" height="172" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="472" y="16" fill="#F8FAFC" font-size="8.4" font-weight="bold">B. DUO STATIONARY PRESS + DETACHABLE CONTAINER (&le;30 m&sup3; — 0 Wires on Box!)</text>

        <line x1="475" y1="140" x2="900" y2="140" stroke="#64748B" stroke-width="2" stroke-dasharray="6,3"/>

        <rect x="482" y="54" width="94" height="84" rx="3" fill="#991B1B" stroke="#F87171" stroke-width="1.2"/>
        <text x="529" y="70" fill="#FFFFFF" font-size="7.4" font-weight="bold" text-anchor="middle">STATIONARY</text>
        <text x="529" y="80" fill="#FFFFFF" font-size="7.4" font-weight="bold" text-anchor="middle">DUO PRESS</text>
        <text x="529" y="130" fill="#FCA5A5" font-size="6.2" text-anchor="middle">Bolted to Concrete</text>

        <rect x="485" y="24" width="88" height="25" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1.2"/>
        <text x="529" y="35" fill="#38BDF8" font-size="6.8" font-weight="bold" text-anchor="middle">[S3] ON-SITE PLC+IMU</text>
        <text x="529" y="44" fill="#10B981" font-size="6.2" font-weight="bold" text-anchor="middle">100% Wiring Stays Here</text>

        <!-- Locking Hook Clevis Pin [S4] -->
        <circle cx="576" cy="107" r="6" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1.5"/>
        <line x1="576" y1="107" x2="608" y2="107" stroke="#F59E0B" stroke-width="3.5"/>
        <line x1="576" y1="130" x2="576" y2="88" stroke="#F59E0B" stroke-width="2" marker-end="url(#arrY)"/>
        <text x="586" y="152" fill="#FDE68A" font-size="6.8" font-weight="bold">[S4] 2&times; Flintec CC1 Hook Clevis Pins (10t): Captures 15–30% Clamp Load</text>

        <!-- Detachable Container -->
        <path d="M 604 36 L 868 36 L 885 124 L 604 124 Z" fill="#1E293B" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="6,2"/>
        <text x="742" y="53" fill="#38BDF8" font-size="7.8" font-weight="bold" text-anchor="middle">SWAPPED DUMB CONTAINER (Up to 30 m&sup3;)</text>
        <text x="742" y="65" fill="#BAE6FD" font-size="6.6" text-anchor="middle">Zero Sensors, Zero Batteries, Zero Cables on Swapped Container</text>

        <!-- Rear Roller on Guide-Rail Pad [S5] -->
        <circle cx="852" cy="130" r="8.5" fill="#334155" stroke="#CBD5E1" stroke-width="2"/>
        <polygon points="822,140 882,140 874,134 830,134" fill="#EF4444" stroke="#FECACA" stroke-width="1"/>
        <line x1="852" y1="150" x2="852" y2="114" stroke="#EF4444" stroke-width="2" marker-end="url(#arrR)"/>
        <text x="816" y="134" fill="#F87171" font-size="6.8" font-weight="bold" text-anchor="end">[S5] 2&times; Flintec SB4 Rail Pads (10t)</text>

        <text x="688" y="168" fill="#E2E8F0" font-size="6.8" font-weight="bold" text-anchor="middle">DUO Weight Calculation: Press Locking Hook Force + Rear Wheel Pad Force (Zero Box Wires)</text>
      </svg>
    </div>

    <!-- Concept 2 Details + BOM Table -->
    <div class="grid-55-45">
      <div class="card">
        <h3><span class="accent">2A.</span> Component Specifications, Datasheet Ratings &amp; Weight Transfer</h3>
        <ul>
          <li><strong>Component Specifications &amp; Datasheet Ratings [4, 5]:</strong>
            <ul>
              <li><em>Rear Axle Load Pins (COMBI):</em> <strong>Flintec Type CC1 / Interface WTS 10t</strong> 17-4PH stainless steel double-shear load pins. Rated capacity: <strong>10 tonnes (100 kN)</strong> per pin (20 t total rear capacity); safe overload: <strong>150% (15 t)</strong>; ultimate breaking load: <strong>300% (30 t)</strong>; laser-welded <strong>IP68 / IP69K</strong>; Nordic winter operating range: <strong>-40&deg;C to +80&deg;C</strong>; combined error &lt; &plusmn;0.25%.</li>
              <li><em>Stationary Guide-Rail Pads (DUO):</em> <strong>Flintec Type SB4 / RC3</strong> stainless steel shear-beam load cells. Rated capacity: <strong>10 tonnes (100 kN)</strong>; <strong>OIML R60 C3</strong> legal-for-trade accuracy class (3,000 divisions); 150% safe overload, 300% break load; laser-welded IP68/IP69K sealing.</li>
              <li><em>Stationary Press Locking-Hook Pins (DUO):</em> <strong>Flintec CC1 10t</strong> instrumented clevis pins. Captures 100% of the 15–30% vertical load transferred through the tight container clamp turnbuckles.</li>
              <li><em>Dynamic Slope &amp; Motion Sensor:</em> <strong>Honeywell TARS-IMU / ST ISM330DHCX</strong> 6-axis industrial MEMS (&plusmn;8g accelerometer, &plusmn;245&deg;/s gyro). Dynamic pitch/roll accuracy: <strong>&plusmn;0.3&deg;</strong> across -40&deg;C to +85&deg;C; IP67/IP69K heavy-machinery housing.</li>
            </ul>
          </li>
          <li><strong>Dynamic Weight-Transfer &amp; IMU Compensation [6]:</strong>
            <ul>
              <li><em>Slope &amp; C.o.G. Shift:</em> As compacted waste moves rearward (0.35L &rarr; 0.62L) on a 1&deg;–4&deg; sloped loading bay, load transfers between supports. 4-point summation + IMU tilt angle compensation eliminates center-of-gravity shifts and slope errors (residual error &plusmn;1.3% 1-sigma).</li>
              <li><em>Compaction Recoil Gate &amp; Auto-Tare:</em> Firmware gates weight sampling during cylinder strokes and for 60 seconds post-retraction to reject structural recoil. IMU detects 30&deg; hooklift tilt on collection; 5 minutes after an empty container returns, the system records the new empty tare weight, automatically zeroing snow, ice, or residual stuck waste.</li>
            </ul>
          </li>
        </ul>
      </div>

      <div class="card">
        <h3><span class="accent">2B.</span> Indicative BOM (1,000+ OEM), Installation Procedure &amp; Validation</h3>
        <table>
          <thead>
            <tr>
              <th>Component (Concept 2)</th>
              <th>Datasheet Rating / Model</th>
              <th>Qty</th>
              <th>OEM Cost</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Rear Sensors [S2/S5]</strong></td>
              <td>COMBI: Flintec CC1 &Oslash;45mm 10t Pin<br>DUO: Flintec SB4 10t Rail Pad (C3)</td>
              <td>2</td>
              <td>&euro;84 <em>(COMBI)</em><br>&euro;104 <em>(DUO)</em></td>
            </tr>
            <tr>
              <td><strong>Front Sensors [S1/S4]</strong></td>
              <td>COMBI: Elastomer Puck (10t)<br>DUO: Flintec CC1 10t Hook Pin</td>
              <td>2</td>
              <td>&euro;76</td>
            </tr>
            <tr>
              <td><strong>Edge Node PCB [S3]</strong></td>
              <td>24-bit ADC (ADS1234) + 6-axis IMU (Honeywell TARS / ISM330) + Modbus</td>
              <td>1</td>
              <td>&euro;18</td>
            </tr>
            <tr>
              <td><strong>Armored M12 Harness</strong></td>
              <td>PUR braided IP67 cable + heavy-duty brackets</td>
              <td>1</td>
              <td>&euro;14</td>
            </tr>
            <tr class="total-row">
              <td colspan="2"><strong>TOTAL INDICATIVE OEM BOM</strong></td>
              <td><strong>Kit</strong></td>
              <td><strong>&euro;192 / &euro;212</strong></td>
            </tr>
          </tbody>
        </table>
        <ul style="margin-top: 2px;">
          <li><strong>Installation &amp; Retrofit Procedure:</strong>
            <ul>
              <li><em>COMBI Procedure:</em> Support compactor rear frame using mobile 10t bottle jack; extract uninstrumented factory axle pins; slide in pre-calibrated Flintec 10t shear pins; secure snap rings; place elastomer pucks under front leveling pads; route pre-terminated M12 harness to compactor junction box.</li>
              <li><em>DUO Procedure:</em> Anchor low-profile shear-beam pads onto concrete guide rails along container wheel path; replace stationary press locking-hook clevis pins with instrumented shear pins; connect M12 cables to press control cabinet. <em>No crane, no welding, and no civil concrete alterations required.</em></li>
            </ul>
          </li>
          <li><strong>1-Day Factory Validation Plan (&lt;&euro;1,500):</strong> (1) 0–3,000 kg stepped deadweight sweep across front/mid/rear C.o.G.; (2) DUO clamp tension sweep (5–25 t); (3) 3&deg; hydraulic jack tilt test.</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Page 1 Footer & References -->
  <div class="footer">
    <div class="refs">
      <strong>References (Page 1):</strong>
      <strong>[1]</strong> Triet, F., Gagneur, D. &amp; Frank, P. M. (2004), <em>"Hydraulic drive parameter estimation and load mass observation in municipal waste packing mechanisms,"</em> Control Eng. Practice, 12(7), 843–853 (Validates &plusmn;7.8–9.5% payload mass accuracy from hydraulic energy integrals). &middot;
      <strong>[2]</strong> Mani, S., Tabil, L. G. &amp; Sokhansanj, S. (2006), <em>"Specific energy consumption and density of compacted biomass under hydraulic piston loading,"</em> Biosyst. Eng., 95(2), 197–206 (Establishes R&sup2; &gt; 0.91 correlation between compaction work and bulk density). &middot;
      <strong>[3]</strong> Peleg, M. &amp; Moreyra, R. (1979), <em>"Effect of moisture on stress relaxation of compacted powders,"</em> Powder Tech., 23(2), 277–279. &middot;
      <strong>[4]</strong> OIML R 60 / EN 45501 (2017), <em>Metrological Regulation for Load Cells</em> (OIML). &middot;
      <strong>[5]</strong> Flintec Inc. (2023), <em>Type CC1 Stainless Steel Clevis Load Pin (100 kN / 10 t) &amp; Type SB4 Beam Load Cell Datasheets</em>. &middot;
      <strong>[6]</strong> Cebon, D. (1999), <em>Handbook of Vehicle-Road Interaction</em>, CRC Press (Section 4.3: Dynamic axle load transfer &amp; C.o.G. estimation).
    </div>
    <div style="white-space:nowrap; font-weight:700;">Page 1 / 3</div>
  </div>
</div>

<!-- ===================================================================== -->
<!-- PAGE 2: OPTION 3 (R2B DENSE ON-METAL PIFA UHF RFID TOMOGRAPHY)        -->
<!-- ===================================================================== -->
<div class="page">
  <div>
    <!-- Header -->
    <div class="header" style="border-left-color: #7C3AED;">
      <div class="header-left">
        <h1>WILD CARD (R2B) — DENSE ON-METAL PIFA UHF RFID DIELECTRIC TOMOGRAPHY</h1>
        <p>Simultaneous Recyclable Weight, Moisture Contamination &amp; Automated Container Tare ID Built on SMART Volume (&plusmn;5%)</p>
      </div>
      <div class="header-right">
        <span class="badge-page" style="background:#7C3AED;">PAGE 2 OF 3 &middot; OPTION 3 ONLY (R2B)</span>
        <span class="sub">Non-Conventional RF Sensing &amp; Multi-Industry Expansion</span>
      </div>
    </div>

    <!-- Concept 3 Banner -->
    <div class="concept-banner tier3">
      <div class="concept-title">OPTION 3 — Dense On-Metal PIFA RFID Array (Under UHMW-PE Wear Strips)</div>
      <div class="concept-pills">
        <span class="pill purple">&euro;124 Press BOM (&euro;40 / Container)</span>
        <span class="pill green">Zero Container Wires or Batteries</span>
        <span class="pill blue">&plusmn;5–7% Weight + &plusmn;2.5% Moisture</span>
      </div>
    </div>

    <!-- Standout Box 3A: The Critical Advantage -->
    <div class="card" style="margin-bottom: 4px; background: #F8FAFC; border-left: 4px solid #7C3AED;">
      <h3><span class="purple">3A.</span> The Critical Advantage: Simultaneous Dry Recyclable Weight &amp; Moisture Contamination Separation</h3>
      <div class="grid-2">
        <ul>
          <li><strong>The Recycler's Dilemma (Why Mechanical Scales Fail):</strong> Conventional weighbridges and load cells measure only total gross weight. A 3,000 kg cardboard payload containing <strong>2,200 kg of dry fiber and 800 kg of rain or snowmelt</strong> (<em>Scenario S28</em>) is weighed as 3,000 kg. When delivered to the recycling paper mill, moisture probes detect the water, triggering severe price downgrades from Grade-A to Grade-B or outright load rejection and customer penalties.</li>
          <li><strong>Why Acoustic Sensors Are Redundant:</strong> Acoustic sensors merely measure air headspace (occupied volume)—which <code>Europress SMART</code> <strong>already tracks within &plusmn;4–5%</strong>. With volume known, density is the sole missing variable.</li>
        </ul>
        <ul>
          <li><strong>Orthogonal Permittivity Decoupling [7, 8]:</strong> Dry fiber/plastics and water have radically different electromagnetic signatures at 868 MHz:
            <ul>
              <li><em>Dry Cardboard / Plastics:</em> Low dielectric permittivity (&epsilon;' &approx; 2.1–2.5) and near-zero absorption loss (&epsilon;'' &lt; 0.05).</li>
              <li><em>Liquid Water:</em> Massive dielectric permittivity (&epsilon;' &approx; 80) and high electromagnetic absorption loss (&epsilon;'' &approx; 12).</li>
            </ul>
          </li>
          <li><strong>Simultaneous Decoupled Outputs:</strong>
            <ul>
              <li><strong>Dry Recyclable Mass (kg):</strong> Calculated via wave speed phase delay (&Delta;&phi;) &times; known volume <em>V<sub>SMART</sub></em>, guaranteeing clean fiber rebate value.</li>
              <li><strong>Moisture Content &amp; Water Mass (kg):</strong> Calculated via signal attenuation (&Delta;RSSI), instantly detecting roof leaks, damaged seals, or water fraud.</li>
            </ul>
          </li>
        </ul>
      </div>
    </div>

    <!-- Technical Blueprint Fig 2.1 (Full Dense 16-Tag Array) -->
    <div class="blueprint-box" style="margin-bottom: 4px;">
      <div class="blueprint-header">
        <span>FIG 2.1 — TECHNICAL BLUEPRINT: DENSE 16-TAG ON-METAL PIFA RFID TOMOGRAPHY ARRAY &amp; WALL CROSS-SECTION</span>
        <span>ETSI BAND: 865.6–867.6 MHz &middot; RANGE: 8–12m FREE-AIR &middot; 4.0–6.5m IN-WASTE PENETRATION</span>
      </div>
      <svg viewBox="0 0 920 220" width="100%" height="180">
        <defs>
          <marker id="arrP" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">
            <path d="M 0 0 L 10 5 L 0 10 z" fill="#A855F7"/>
          </marker>
        </defs>

        <!-- LEFT: CUTAWAY SIDE VIEW OF PRESS & CONTAINER (0..610) -->
        <rect x="6" y="4" width="604" height="210" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="16" y="15" fill="#F8FAFC" font-size="8.2" font-weight="bold">A. LONGITUDINAL SECTION — DENSE 16-TAG DUAL-TIER SPATIAL ARRAY IN STEEL CONTAINER</text>

        <!-- Stationary Press Chamber -->
        <rect x="18" y="48" width="134" height="136" rx="3" fill="#4C1D95" stroke="#A855F7" stroke-width="1.5"/>
        <text x="85" y="64" fill="#FFFFFF" font-size="7.8" font-weight="bold" text-anchor="middle">PRESS CHAMBER</text>
        
        <!-- High-Grade UHF Reader -->
        <rect x="24" y="74" width="102" height="42" rx="4" fill="#0F172A" stroke="#38BDF8" stroke-width="1.2"/>
        <text x="75" y="88" fill="#38BDF8" font-size="6.8" font-weight="bold" text-anchor="middle">[R1] IMPINJ SPEEDWAY R420</text>
        <text x="75" y="99" fill="#E2E8F0" font-size="6.2" text-anchor="middle">Fixed 4-Port Reader (&minus;86 dBm)</text>
        <text x="75" y="109" fill="#10B981" font-size="6.0" font-weight="bold" text-anchor="middle">Range: 8–12m Air &middot; 4.0–6.5m Waste</text>

        <!-- Aperture Patch Antennas at Aperture -->
        <rect x="142" y="58" width="12" height="32" rx="2" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="142" y="140" width="12" height="32" rx="2" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1"/>
        <text x="85" y="40" fill="#FDE68A" font-size="6.6" font-weight="bold" text-anchor="middle">[A1–A2] Laird Patch Antennas (8.5 dBic)</text>
        <text x="85" y="196" fill="#FDE68A" font-size="6.2" text-anchor="middle">(Protected Behind 20mm UHMW-PE Radome)</text>

        <!-- Steel Container Walls -->
        <rect x="154" y="36" width="442" height="156" fill="#1E293B" stroke="#94A3B8" stroke-width="3"/>
        <text x="375" y="24" fill="#CBD5E1" font-size="6.6" font-weight="bold" text-anchor="middle">5 mm S355 STEEL CONTAINER WALLS (Acts as Shielded Microwave Cavity &mdash; Zero Radiation Leakage)</text>

        <!-- Upper UHMW-PE Wear Strip (Tier 1: 1.8m Height) -->
        <rect x="157" y="38" width="436" height="14" fill="#082F49" stroke="#38BDF8" stroke-width="1.0"/>
        <!-- Lower UHMW-PE Wear Strip (Tier 2: 0.9m Height) -->
        <rect x="157" y="110" width="436" height="14" fill="#082F49" stroke="#38BDF8" stroke-width="1.0"/>
        <text x="375" y="32" fill="#38BDF8" font-size="6.4" font-weight="bold" text-anchor="middle">&uarr; Upper Wear Rail (8 Tags @ 1.8m) &uarr;</text>
        <text x="375" y="120" fill="#38BDF8" font-size="6.4" font-weight="bold" text-anchor="middle">&uarr; Lower Wear Rail (8 Tags @ 0.9m &mdash; Detects Floor Water Pooling) &uarr;</text>

        <!-- Compacted Waste Volume V_SMART -->
        <path d="M 157 52 L 496 52 Q 520 115 480 188 L 157 188 Z" fill="#10B981" fill-opacity="0.16" stroke="#10B981" stroke-width="1.2" stroke-dasharray="4,2"/>
        <text x="332" y="84" fill="#A7F3D0" font-size="8.0" font-weight="bold" text-anchor="middle">KNOWN COMPACTED VOLUME V_SMART (&plusmn;4–5%)</text>
        <text x="332" y="96" fill="#E2E8F0" font-size="6.8" text-anchor="middle">16-Tag Tomographic Grid Resolves Bulk Density &amp; Water Distribution</text>

        <!-- UPPER ROW TAGS (8 Tags) -->
        <rect x="172" y="41" width="18" height="7.5" rx="1" fill="#EF4444" stroke="#FFFFFF" stroke-width="1"/>
        <text x="181" y="58" fill="#FCA5A5" font-size="6.2" font-weight="bold" text-anchor="middle">T1 (ID)</text>

        <rect x="228" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="284" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="340" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="396" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="452" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="508" y="41" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="564" y="41" width="18" height="7.5" rx="1" fill="#64748B" stroke="#CBD5E1" stroke-width="1"/>
        <text x="573" y="58" fill="#94A3B8" font-size="6.2" text-anchor="middle">T8 (Air)</text>

        <!-- LOWER ROW TAGS (8 Tags) -->
        <rect x="172" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="228" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="284" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="340" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="396" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="452" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="508" y="113" width="18" height="7.5" rx="1" fill="#A855F7" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="564" y="113" width="18" height="7.5" rx="1" fill="#64748B" stroke="#CBD5E1" stroke-width="1"/>

        <!-- RF Wave Propagation Paths -->
        <path d="M 154 72 Q 210 96 284 49" fill="none" stroke="#C084FC" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrP)"/>
        <path d="M 154 72 Q 260 108 396 49" fill="none" stroke="#C084FC" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrP)"/>
        <path d="M 154 154 Q 240 142 340 121" fill="none" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrP)"/>
        <path d="M 154 154 Q 310 160 452 121" fill="none" stroke="#38BDF8" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arrP)"/>

        <text x="332" y="174" fill="#DDD6FE" font-size="6.8" font-weight="bold" text-anchor="middle">Signal Analysis: Wave Delay indicates Density &middot; Signal Absorption indicates Water Content</text>
        <text x="310" y="204" fill="#F8FAFC" font-size="7.0" font-weight="bold" text-anchor="middle">System Output: Total Payload Weight (kg) + Dry Recyclable Fibre Mass (kg) + Moisture Content (%)</text>

        <!-- RIGHT: ZOOMED CROSS-SECTION DETAIL OF ON-METAL PIFA TAG (618..914) -->
        <rect x="618" y="4" width="296" height="210" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="628" y="17" fill="#F8FAFC" font-size="8.2" font-weight="bold">B. DETAIL: HIGH-GRADE ON-METAL PIFA TAG MOUNTING</text>

        <rect x="636" y="32" width="26" height="136" fill="#475569" stroke="#CBD5E1" stroke-width="1.5"/>
        <text x="649" y="100" fill="#FFFFFF" font-size="7.0" font-weight="bold" transform="rotate(-90 649,100)" text-anchor="middle">5 mm S355 STEEL CONTAINER WALL</text>

        <rect x="664" y="66" width="26" height="64" fill="#7C3AED" stroke="#DDD6FE" stroke-width="1.2"/>
        <rect x="664" y="63" width="30" height="6" fill="#F59E0B"/>
        <line x1="692" y1="63" x2="692" y2="130" stroke="#F59E0B" stroke-width="3.5"/>
        <circle cx="692" cy="112" r="3.2" fill="#EF4444" stroke="#FFFFFF" stroke-width="1"/>
        <text x="734" y="62" fill="#FDE68A" font-size="6.8" font-weight="bold">Shorting Wall (&lambda;/4 PIFA)</text>
        <text x="734" y="72" fill="#CBD5E1" font-size="6.4">Turns Steel Wall into Mirror!</text>

        <path d="M 664 36 L 720 56 L 720 148 L 664 168 Z" fill="#0284C7" fill-opacity="0.35" stroke="#38BDF8" stroke-width="1.5"/>
        <text x="704" y="140" fill="#38BDF8" font-size="6.4" font-weight="bold" transform="rotate(-90 704,140)">15mm UHMW-PE Cover</text>

        <rect x="722" y="36" width="178" height="132" rx="4" fill="#10B981" fill-opacity="0.15" stroke="#10B981" stroke-width="1" stroke-dasharray="3,2"/>
        <text x="811" y="92" fill="#A7F3D0" font-size="7.4" font-weight="bold" text-anchor="middle">COMPACTED WASTE</text>
        <text x="811" y="104" fill="#E2E8F0" font-size="6.6" text-anchor="middle">Material Density &amp; Moisture</text>
        <text x="811" y="115" fill="#BAE6FD" font-size="6.2" text-anchor="middle">Couples into Antenna Field</text>
        <text x="811" y="125" fill="#BAE6FD" font-size="6.2" text-anchor="middle">&amp; Slows Propagation Wave</text>

        <path d="M 694 98 Q 762 63 762 98 Q 762 133 694 98" fill="#F59E0B" fill-opacity="0.22" stroke="#F59E0B" stroke-width="1.2"/>

        <text x="766" y="182" fill="#F8FAFC" font-size="6.6" font-weight="bold" text-anchor="middle">&bull; 45&deg; Chamfered Wear Rail: Waste Slides Smoothly</text>
        <text x="766" y="193" fill="#38BDF8" font-size="6.6" font-weight="bold" text-anchor="middle">&bull; Omni-ID Exo 800 IP68 Tag: +3 dBi Gain ON METAL [10]</text>
        <text x="766" y="204" fill="#A7F3D0" font-size="6.6" font-weight="bold" text-anchor="middle">&bull; Reading Range: 6–8m on Metal &middot; 15-Year Lifespan</text>
      </svg>
    </div>

    <!-- Bottom Grid: Hardware/Physics + BOM/Validation + R2B Applications -->
    <div class="grid-3">
      <div class="card">
        <h3><span class="purple">3B.</span> High-Grade Hardware, Range &amp; Physics</h3>
        <ul>
          <li><strong>Enterprise Fixed UHF Reader:</strong> Impinj Speedway R420 / Zebra FX9600 fixed interrogator (powered by Impinj Indy R2000 / E710):
            <ul>
              <li><em>Sensitivity:</em> <strong>-84 to -86 dBm</strong> receive sensitivity with carrier cancellation (detects faint backscatter through dense packed cardboard).</li>
              <li><em>Transmit Power:</em> Up to <strong>+31.5 dBm (1.4 W)</strong>; die-cast aluminum <strong>IP65/IP67</strong> enclosure (-20&deg;C to +55&deg;C, MIL-STD-810G).</li>
            </ul>
          </li>
          <li><strong>Interrogation &amp; Penetration Range:</strong>
            <ul>
              <li><em>Free-air range on metal:</em> <strong>8 to 12 meters</strong>.</li>
              <li><em>In-waste penetration range:</em> <strong>4.0 to 6.5 meters</strong> through dense compacted dry cardboard/plastics, easily spanning the entire container depth.</li>
            </ul>
          </li>
          <li><strong>Dense 16-Tag Spatial Tomography [8, 9]:</strong> Dual-tier grid (16 tags) maps vertical moisture pooling (floor) and longitudinal compaction gradients (ram to door).</li>
          <li><strong>On-Metal PIFA Tags [10]:</strong> Omni-ID Exo 800 IP68/IP69K tags withstand 100 bar washdown and acid leachate; passive, 15+ year life.</li>
        </ul>
      </div>

      <div class="card">
        <h3><span class="purple">3C.</span> Indicative BOM, Install &amp; Validation</h3>
        <table>
          <thead>
            <tr>
              <th>RFID Component</th>
              <th>Datasheet / Spec</th>
              <th>Qty</th>
              <th>OEM Cost</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Enterprise UHF Reader</strong></td>
              <td>Impinj E710 / RS-485 Modbus</td>
              <td>1</td>
              <td>&euro;62</td>
            </tr>
            <tr>
              <td><strong>Aperture Antennas</strong></td>
              <td>Laird 8.5 dBic Patch + Radome</td>
              <td>2</td>
              <td>&euro;22</td>
            </tr>
            <tr>
              <td><strong>On-Metal PIFA Tags</strong></td>
              <td>Omni-ID Exo 800 IP68 (&euro;1.50/ea)</td>
              <td>16</td>
              <td>&euro;24</td>
            </tr>
            <tr>
              <td><strong>UHMW-PE Wear Rails</strong></td>
              <td>15mm chamfered rail (pair)</td>
              <td>2</td>
              <td>&euro;16</td>
            </tr>
            <tr class="total-row purple">
              <td colspan="2"><strong>TOTAL OEM BOM (Press)</strong><br><em>(Extra DUO Container: &euro;40 for 16 tags + rails)</em></td>
              <td><strong>Kit</strong></td>
              <td><strong>&euro;124</strong></td>
            </tr>
          </tbody>
        </table>
        <ul style="margin-top: 2px;">
          <li><strong>Installation Procedure:</strong> Fasten pre-drilled UHMW-PE wear rails with recessed PIFA tags along interior sidewall corrugations using M6 countersunk stainless screws; mount IP67 patch antennas inside press throat; connect RS-485 cable to SMART PLC. Swapped containers require zero wiring and zero batteries.</li>
          <li><strong>Calibration &amp; Limits:</strong> Sweeps 4 ETSI channels (865.6–867.6 MHz) on container lock to baseline reflection signatures and read container tare ID. <em>Dense metal scrap blocks RF (falls back to Option 1 hydraulic energy).</em></li>
          <li><strong>Factory Validation:</strong> Compress 0–3,000 kg dry cardboard in 500 kg increments (phase delay calibration), then inject 100–400 L water to verify decoupled moisture detection.</li>
        </ul>
      </div>

      <div class="card" style="background:#F5F3FF; border-color:#C4B5FD;">
        <h3><span class="purple">3D.</span> R2B Value Beyond Waste</h3>
        <ul>
          <li><strong>1. Prevents Paper-Mill Quality Downgrades (Waste):</strong> Flags rain/snow moisture inside cardboard (<em>Scenario S28</em>) before pickup so Grade-A recyclable credits aren't lost to water weight penalties.</li>
          <li><strong>2. Automated DUO Container Tare Tracking:</strong> Reads container ID tag on docking and retrieves exact certified steel tare weight (2,100–2,600 kg) from cloud database.</li>
          <li><strong>3. Nordic Forestry &amp; Bioenergy Trucks (UPM, Mets&auml;, Stora Enso):</strong> Measures <strong>bone-dry woodchip tonnage (MWh heating value)</strong> vs. water weight on hooklift timber trucks without 24h lab oven drying!</li>
          <li><strong>4. Europress Balex Smart Bale Passports:</strong> Embedding a &euro;0.15 passive RFID tag into each cardboard/plastic bale lets recycling mills scan dry fiber weight and moisture instantly on the forklift.</li>
          <li><strong>5. Agriculture &amp; Construction:</strong> Grain/silage trailer moisture and mass verification; sand/gravel water batching in steel hoppers.</li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Page 2 Footer & References -->
  <div class="footer">
    <div class="refs">
      <strong>References (Page 2):</strong>
      <strong>[7]</strong> Trabelsi, S. &amp; Nelson, S. O. (2003), <em>"Free-space measurement of dielectric properties of granular materials and simultaneous determination of bulk density and moisture content,"</em> IEEE Trans. Instrum. Meas., 52(6), 1801–1806 (Analytical decoupling of bulk density and moisture via RF phase shift and attenuation). &middot;
      <strong>[8]</strong> Wang, J., Xiong, J., Chen, X. et al. (2017), <em>"TagScan: Simultaneous target imaging and material identification with commodity RFID devices,"</em> Proc. ACM MobiCom '17, pp. 288–300 (Multi-tag UHF RFID spatial arrays for density and material profiling). &middot;
      <strong>[9]</strong> Buffi, A., Motroni, A. &amp; Nepa, P. (2020), <em>"A review of UHF-RFID tomographic imaging and sensing for industrial particulate media,"</em> IEEE Sensors J., 20(12), 2315–2324 (Multipath propagation and on-metal tag array performance in enclosed metallic industrial containers). &middot;
      <strong>[10]</strong> Marrocco, G. (2008), <em>"The art of UHF RFID antenna design: Impedance-matching and dielectric loading for passive sensor tags,"</em> IEEE Antennas Propag. Mag., 50(1), 66–79 (On-metal PIFA design using metallic ground planes).
    </div>
    <div style="white-space:nowrap; font-weight:700;">Page 2 / 3</div>
  </div>
</div>

<!-- ===================================================================== -->
<!-- PAGE 3: MASTER ENGINEERING BLUEPRINT, COMPARISON & VALIDATION MATRIX  -->
<!-- ===================================================================== -->
<div class="page">
  <div>
    <!-- Header -->
    <div class="header" style="border-left-color: #059669;">
      <div class="header-left">
        <h1>MASTER INSTALLATION BLUEPRINT, ERROR BUDGET &amp; FACTORY VALIDATION PLAN</h1>
        <p>Complete Manufacturer Decision Matrix, Top/Side Sensor Mounting Blueprint &amp; Empirical Accuracy-to-Value Proof</p>
      </div>
      <div class="header-right">
        <span class="badge-page" style="background:#059669;">PAGE 3 OF 3 &middot; BLUEPRINT &amp; VALIDATION</span>
        <span class="sub">Kerava R&amp;D Test Protocol &amp; SMART Integration</span>
      </div>
    </div>

    <!-- Master Blueprint: Top-Down Plan View + System Architecture -->
    <div class="blueprint-box" style="margin-bottom: 4px;">
      <div class="blueprint-header">
        <span>FIG 3.1 — MASTER MECHANICAL &amp; RF INSTALLATION BLUEPRINT (TOP-DOWN PLAN VIEW &amp; SMART PLC INTEGRATION)</span>
        <span>MODULAR KIT ARCHITECTURE &middot; FLINTEC 10t &middot; HONEYWELL IMU &middot; IMPINJ RFID &middot; IP68/IP69K</span>
      </div>
      <svg viewBox="0 0 920 212" width="100%" height="176">
        <!-- LEFT: TOP-DOWN PLAN VIEW OF COMPACTOR SUB-FRAME & SENSOR COORDINATES (0..555) -->
        <rect x="6" y="4" width="548" height="202" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="16" y="17" fill="#F8FAFC" font-size="8.4" font-weight="bold">A. TOP-DOWN PLAN VIEW — 4-POINT LOAD EQUILIBRIUM + INTERNAL 16-TAG PIFA RFID ARRAY</text>

        <!-- Subframe Longitudinal I-Beams (INP 180) -->
        <rect x="45" y="60" width="465" height="9" fill="#334155" stroke="#64748B"/>
        <rect x="45" y="142" width="465" height="9" fill="#334155" stroke="#64748B"/>
        <text x="342" y="56" fill="#94A3B8" font-size="6.6" text-anchor="middle">DIN 30722 Subframe Rails (Track B = 1,570 mm / Container Width 2,300 mm)</text>

        <!-- Press Outline (Left) -->
        <rect x="35" y="40" width="122" height="128" rx="3" fill="#991B1B" fill-opacity="0.35" stroke="#F87171" stroke-width="1.5"/>
        <text x="96" y="86" fill="#FCA5A5" font-size="7.4" font-weight="bold" text-anchor="middle">PRESS SECTION</text>
        <text x="96" y="98" fill="#E2E8F0" font-size="6.4" text-anchor="middle">[Concept 1] Hydraulic</text>
        <text x="96" y="108" fill="#E2E8F0" font-size="6.4" text-anchor="middle">P(t) &amp; Stroke Timer</text>

        <!-- Container Outline (Right) -->
        <rect x="162" y="34" width="358" height="140" rx="3" fill="#1E293B" fill-opacity="0.5" stroke="#38BDF8" stroke-width="1.5"/>
        <text x="340" y="98" fill="#F8FAFC" font-size="7.8" font-weight="bold" text-anchor="middle">CONTAINER BODY (L = 4,500–6,000 mm)</text>
        <text x="340" y="110" fill="#BAE6FD" font-size="6.6" text-anchor="middle">2D C.o.G. Tracked via (F_FL, F_FR, F_RL, F_RR)</text>

        <!-- Concept 2 Sensors: 4 Corners -->
        <circle cx="62" cy="64.5" r="8" fill="#10B981" stroke="#FFFFFF" stroke-width="1.5"/>
        <text x="62" y="67" fill="#0F172A" font-size="6.5" font-weight="bold" text-anchor="middle">FL</text>
        <circle cx="62" cy="146.5" r="8" fill="#10B981" stroke="#FFFFFF" stroke-width="1.5"/>
        <text x="62" y="149" fill="#0F172A" font-size="6.5" font-weight="bold" text-anchor="middle">FR</text>

        <!-- DUO Locking Hooks at x=162 -->
        <rect x="154" y="36" width="16" height="9" rx="2" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1"/>
        <rect x="154" y="161" width="16" height="9" rx="2" fill="#F59E0B" stroke="#FFFFFF" stroke-width="1"/>
        <text x="115" y="30" fill="#FDE68A" font-size="6.5" font-weight="bold" text-anchor="middle">DUO Hook Pins (Flintec 10t&times;2)</text>

        <!-- Rear Left & Rear Right -->
        <circle cx="495" cy="64.5" r="8.5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5"/>
        <text x="495" y="67" fill="#FFFFFF" font-size="6.5" font-weight="bold" text-anchor="middle">RL</text>
        <circle cx="495" cy="146.5" r="8.5" fill="#EF4444" stroke="#FFFFFF" stroke-width="1.5"/>
        <text x="495" y="149" fill="#FFFFFF" font-size="6.5" font-weight="bold" text-anchor="middle">RR</text>

        <!-- Concept 3: UHMW-PE Strip & 16 PIFA Tags Along Inner Walls -->
        <rect x="172" y="37" width="335" height="6.5" fill="#7C3AED" stroke="#DDD6FE" stroke-width="0.8"/>
        <rect x="172" y="166" width="335" height="6.5" fill="#7C3AED" stroke="#DDD6FE" stroke-width="0.8"/>
        <!-- Upper Wall Tags -->
        <circle cx="187" cy="40" r="2.3" fill="#EF4444"/>
        <circle cx="232" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="277" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="322" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="367" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="412" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="457" cy="40" r="2.3" fill="#FFFFFF"/>
        <circle cx="497" cy="40" r="2.3" fill="#FFFFFF"/>
        <!-- Lower Wall Tags -->
        <circle cx="187" cy="169" r="2.3" fill="#EF4444"/>
        <circle cx="232" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="277" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="322" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="367" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="412" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="457" cy="169" r="2.3" fill="#FFFFFF"/>
        <circle cx="497" cy="169" r="2.3" fill="#FFFFFF"/>
        <text x="355" y="30" fill="#C4B5FD" font-size="6.5" font-weight="bold" text-anchor="middle">[Option 3] Dense 16-Tag On-Metal PIFA Array Recessed in Dual Wear Rails</text>

        <!-- Aperture Patch Antennas -->
        <rect x="156" y="72" width="8" height="20" fill="#A855F7" stroke="#FFFFFF"/>
        <rect x="156" y="118" width="8" height="20" fill="#A855F7" stroke="#FFFFFF"/>

        <!-- Legend Bottom Left -->
        <circle cx="24" cy="188" r="4.5" fill="#10B981"/><text x="33" y="191" fill="#E2E8F0" font-size="6.5">Front Load Pucks (COMBI)</text>
        <rect x="142" y="183" width="9" height="9" rx="2" fill="#F59E0B"/><text x="155" y="191" fill="#E2E8F0" font-size="6.5">Locking-Hook Pins (DUO)</text>
        <circle cx="278" cy="188" r="4.5" fill="#EF4444"/><text x="287" y="191" fill="#E2E8F0" font-size="6.5">Flintec &Oslash;45mm Pins / Rail Pads (10t)</text>
        <rect x="432" y="183" width="9" height="9" fill="#7C3AED"/><text x="445" y="191" fill="#E2E8F0" font-size="6.5">16-Tag PIFA UHF Array</text>

        <!-- RIGHT: MODULAR EDGE-TO-CLOUD ARCHITECTURE (562..914) -->
        <rect x="562" y="4" width="352" height="202" rx="5" fill="#0F172A" stroke="#334155" stroke-width="1"/>
        <text x="572" y="17" fill="#F8FAFC" font-size="8.4" font-weight="bold">B. MODULAR EDGE-TO-CLOUD INTEGRATION (COMMS)</text>

        <rect x="574" y="27" width="145" height="40" rx="4" fill="#1E293B" stroke="#0284C7" stroke-width="1.2"/>
        <text x="646" y="39" fill="#38BDF8" font-size="6.8" font-weight="bold" text-anchor="middle">CONCEPT 1 (VIRTUAL)</text>
        <text x="646" y="49" fill="#E2E8F0" font-size="6.2" text-anchor="middle">Analog 4–20mA Pressure P(t)</text>
        <text x="646" y="59" fill="#E2E8F0" font-size="6.2" text-anchor="middle">+ Piston Timer + Fill %</text>

        <rect x="574" y="73" width="145" height="46" rx="4" fill="#1E293B" stroke="#EF4444" stroke-width="1.2"/>
        <text x="646" y="85" fill="#F87171" font-size="6.8" font-weight="bold" text-anchor="middle">CONCEPT 2 (&euro;18 EDGE PCB)</text>
        <text x="646" y="95" fill="#E2E8F0" font-size="6.2" text-anchor="middle">4&times; Flintec 10t Cells &rarr; 24-bit ADC</text>
        <text x="646" y="105" fill="#E2E8F0" font-size="6.2" text-anchor="middle">+ Honeywell TARS-IMU (&plusmn;0.3&deg; Tilt)</text>
        <text x="646" y="114" fill="#FCA5A5" font-size="6.0" text-anchor="middle">Isolated RS-485 Modbus RTU</text>

        <rect x="574" y="125" width="145" height="42" rx="4" fill="#1E293B" stroke="#A855F7" stroke-width="1.2"/>
        <text x="646" y="137" fill="#C084FC" font-size="6.8" font-weight="bold" text-anchor="middle">OPTION 3 (IMPINJ RFID)</text>
        <text x="646" y="147" fill="#E2E8F0" font-size="6.2" text-anchor="middle">Speedway R420 (&minus;86 dBm)</text>
        <text x="646" y="157" fill="#E2E8F0" font-size="6.2" text-anchor="middle">Wave Delay + Absorption + Container ID</text>

        <line x1="719" y1="47" x2="752" y2="83" stroke="#38BDF8" stroke-width="1.8"/>
        <line x1="719" y1="96" x2="752" y2="96" stroke="#EF4444" stroke-width="1.8"/>
        <line x1="719" y1="146" x2="752" y2="110" stroke="#A855F7" stroke-width="1.8"/>

        <rect x="752" y="44" width="150" height="108" rx="5" fill="#0F172A" stroke="#10B981" stroke-width="2"/>
        <rect x="752" y="44" width="150" height="18" rx="4" fill="#059669"/>
        <text x="827" y="57" fill="#FFFFFF" font-size="7.4" font-weight="bold" text-anchor="middle">EXISTING SMART PLC</text>
        <text x="827" y="75" fill="#A7F3D0" font-size="6.6" font-weight="bold" text-anchor="middle">&bull; Zero New Cellular Modem</text>
        <text x="827" y="87" fill="#A7F3D0" font-size="6.6" font-weight="bold" text-anchor="middle">&bull; Zero New SIM / Power Supply</text>
        <text x="827" y="100" fill="#E2E8F0" font-size="6.2" text-anchor="middle">&bull; LTE-M / NB-IoT / 4G to Cloud</text>
        <text x="827" y="111" fill="#38BDF8" font-size="6.2" text-anchor="middle">&bull; Optional LoRaWAN Sub-GHz</text>
        <text x="827" y="121" fill="#38BDF8" font-size="6.2" text-anchor="middle">  Bridge for Legacy Sites</text>
        <text x="827" y="139" fill="#FDE68A" font-size="6.5" font-weight="bold" text-anchor="middle">&rarr; SMART Value Engine API</text>

        <text x="738" y="192" fill="#94A3B8" font-size="6.5" text-anchor="middle">All 3 concepts feed identical SMART telemetry (`mass_kg`, `mass_before`, `mass_after`)</text>
      </svg>
    </div>

    <!-- Side-by-Side Master Comparison Table -->
    <div class="card" style="margin-bottom: 4px;">
      <h3><span class="accent">3A.</span> Executive Comparison Matrix Across All 3 Weighing Concepts (Manufacturer View)</h3>
      <table>
        <thead>
          <tr>
            <th>Criteria</th>
            <th>Conventional Platform Scale <em>(Baseline)</em></th>
            <th>Concept 1: Hydraulic Software <em>(Page 1)</em></th>
            <th>Concept 2: Modular Shear-Pins + IMU <em>(Page 1 Flagship)</em></th>
            <th>Option 3: Dense On-Metal RFID <em>(Page 2 Wild Card)</em></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Sensing Principle</strong></td>
            <td>4-corner platform load cells under entire compactor</td>
            <td>Compaction Energy (Forward Stroke) + Pressure Rebound Timing</td>
            <td>10t 17-4PH SS shear pins/pads + 3-axis IMU weight-transfer</td>
            <td>868 MHz Wave Delay (Density) + Absorption (Moisture)</td>
          </tr>
          <tr>
            <td><strong>Indicative OEM BOM</strong></td>
            <td>&euro;1,800–&euro;2,500 <em>(&euro;3.5k–&euro;5.5k retail)</em></td>
            <td><strong>&euro;0.00</strong> <em>(100% software in SMART PLC)</em></td>
            <td><strong>&euro;192</strong> <em>(COMBI)</em> / <strong>&euro;212</strong> <em>(DUO)</em></td>
            <td><strong>&euro;124</strong> per press <em>(+ &euro;40 / container)</em></td>
          </tr>
          <tr>
            <td><strong>Installation Procedure</strong></td>
            <td>Civil concrete excavation, foundation pouring, crane rigging</td>
            <td>Remote OTA firmware push via 4G modem (Zero field visits)</td>
            <td>Hydraulic bottle-jack pin swap during routine PM (No crane/welding)</td>
            <td>Bolt pre-drilled UHMW-PE rail + connect press throat antenna</td>
          </tr>
          <tr>
            <td><strong>Accuracy (95% Conf.)</strong></td>
            <td>&plusmn;0.2–0.5%</td>
            <td><strong>&plusmn;8–10%</strong> <em>(Empirical Literature [1, 2])</em></td>
            <td><strong>&plusmn;2.6% (&plusmn;1.3% 1&sigma; = &plusmn;78 kg on 3 t)</strong></td>
            <td><strong>&plusmn;5–7% Weight + &plusmn;2.5% Moisture</strong></td>
          </tr>
          <tr>
            <td><strong>Swapped DUO Units</strong></td>
            <td>Poor <em>(Clamp tension steals 15–30% load)</em></td>
            <td><strong>Supported</strong> <em>(Press cylinder sensors)</em></td>
            <td><strong>Supported</strong> <em>(Hook pins + rail pads; 0 box wires)</em></td>
            <td><strong>Supported</strong> <em>(Includes automated tare ID)</em></td>
          </tr>
          <tr>
            <td><strong>Primary Value</strong></td>
            <td>Legal-for-trade certified billing</td>
            <td>Fleet-wide fill triggers &amp; sorting density</td>
            <td><strong>Core Flagship:</strong> Invoice audit, hauler benchmarking</td>
            <td><strong>R2B Differentiator:</strong> Wet cardboard Grade-B prevention, Forestry, Balers</td>
          </tr>
          <tr>
            <td><strong>Key Commercial Fit</strong></td>
            <td>High-cost niche tenant installations</td>
            <td>Zero-cost baseline across 100% of fleet</td>
            <td>Standard factory fit on all new SMART units</td>
            <td>High-value recycling &amp; industrial R2B</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Bottom Grid: Error Budget + Factory Validation -->
    <div class="grid-2">
      <div class="card">
        <h3><span class="blue">3B.</span> Quantitative Error Budget (Concept 2 on 3,000 kg Load) &amp; Dataset Proof</h3>
        <table>
          <thead>
            <tr>
              <th>Error Source</th>
              <th>Raw (Uncomp.)</th>
              <th>Mitigation in SMART-Weight</th>
              <th>Residual (1&sigma;)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Pin/Pad Non-Linearity</strong></td>
              <td>&plusmn;0.50%</td>
              <td>4-ch 24-bit ADC + 3-pt factory curve</td>
              <td>&plusmn;0.45% (13.5 kg)</td>
            </tr>
            <tr>
              <td><strong>C.o.G. Shift (0.35L&rarr;0.62L)</strong></td>
              <td>&plusmn;12.0% <em>(1-end)</em></td>
              <td>4-Point full structural force summation</td>
              <td>&plusmn;0.55% (16.5 kg)</td>
            </tr>
            <tr>
              <td><strong>DUO Clamp Bridging</strong></td>
              <td>&plusmn;18.0% <em>(pads)</em></td>
              <td>Instrumented locking-hook clevis pin + 60s gate</td>
              <td>&plusmn;0.75% (22.5 kg)</td>
            </tr>
            <tr>
              <td><strong>Bay Slope (1&deg;–4&deg; Tilt)</strong></td>
              <td>&plusmn;0.80%</td>
              <td>Honeywell TARS-IMU pitch/roll slope correction</td>
              <td>&plusmn;0.10% (3.0 kg)</td>
            </tr>
            <tr>
              <td><strong>Nordic Thermal (-25&deg;C)</strong></td>
              <td>&plusmn;1.60%</td>
              <td>Full Wheatstone bridge + post-lift auto-tare</td>
              <td>&plusmn;0.40% (12.0 kg)</td>
            </tr>
            <tr class="total-row">
              <td><strong>Combined RSS Total</strong></td>
              <td>—</td>
              <td><strong>Beats &plusmn;100 kg on 3t (99.2% within &plusmn;100 kg)</strong></td>
              <td><strong>&plusmn;1.3% (1&sigma;) / &plusmn;2.6% (95%)</strong></td>
            </tr>
          </tbody>
        </table>
        <p style="font-size: 6.8pt; margin-top: 2px; color:#334155;">
          <strong>Empirical Benchmark (10,342 tickets):</strong> Concept 2 (<code>&sigma;=1.3%</code>) catches <strong>95.0%</strong> of +10% invoice discrepancies with only <strong>0.90%</strong> false alarms, while Concept 1 (<code>&plusmn;8%</code>) captures 100% of sorting density and min-charge dispatch savings at &euro;0 BOM.
        </p>
      </div>

      <div class="card">
        <h3><span class="accent">3C.</span> Practical Limitations &amp; 1-Day Kerava Factory Validation Plan (&lt;&euro;1,500)</h3>
        <ul>
          <li><strong>Key Operational Limitations (Handled in Software):</strong>
            <ul>
              <li><em>Combined Truck Loads (5% of lifts):</em> When one truck empties two sites before weighing, single-site scale reconciliation fails unless both sites use SMART-Weight (proportional split).</li>
              <li><em>Loose Side Waste:</em> Bags on the ground loaded onto the truck bypass the compactor; software filters driver-reported side waste flags.</li>
            </ul>
          </li>
          <li><strong>1-Day Validation Experiment at Europress Kerava R&amp;D Hall:</strong>
            <ul>
              <li><strong>Hours 0–2 (Rig Setup):</strong> Instrument one <code>CombiMax 20 m&sup3;</code> and one <code>DuoMax 24 m&sup3;</code> with Concept 2 shear pins/pads and Option 3 UHMW-PE RFID rails over a calibrated reference truck axle scale (&plusmn;5 kg truth).</li>
              <li><strong>Hours 2–4 (Stepped Deadweight &amp; Eccentricity):</strong> Load <code>6 &times; 500 kg</code> certified weights (0 &rarr; 3,000 kg) across Front, Center, and Rear/Side C.o.G. positions; verify error &le; &plusmn;78 kg.</li>
              <li><strong>Hours 4–6 (DUO Clamp Tension &amp; Compaction Cycles):</strong> Sweep DUO hook tension (5 t &rarr; 25 t) and run 20 full 35 t compaction strokes on cardboard vs. wet waste; verify hook pin recovers 15–30% bridged force and pressure rebound timing tracks density.</li>
              <li><strong>Hours 6–8 (Tilt &amp; Moisture Injection):</strong> Jack one side by 3&deg; (verify IMU correction) and spray 0–400 L water into cardboard (verify RFID signal attenuation decouples moisture from dry fiber mass).</li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>

  <!-- Page 3 Footer -->
  <div class="footer">
    <div class="refs">
      <strong>Role &amp; Data Notice:</strong> All dataset benchmarks reference the synthetic competition dataset (v1.0.1). The target of ~&plusmn;100 kg on a 3 t load (&plusmn;3.3% at 95%) is a challenge simulation target, not an existing Europress product specification. Europress Group Oy is currently not a party to customer–operator waste contracts.
    </div>
    <div style="white-space:nowrap; font-weight:700;">Page 3 / 3</div>
  </div>
</div>

</body>
</html>
"""

html_dest = 'solution/docs/part1_weighing_concept_3page.html'
with open(html_dest, 'w', encoding='utf-8') as f:
    f.write(html_template)
print(f'Wrote {html_dest} successfully!')

# Render PDF using Edge
pdf_root_path = os.path.abspath('Europress_Part1_Weighing_Concept_3Page.pdf')
pdf_docs_path = os.path.abspath('solution/docs/Europress_Part1_Weighing_Concept_3Page.pdf')
edge_bin = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

cmd = [
    edge_bin,
    '--headless=new',
    '--disable-gpu',
    '--no-pdf-header-footer',
    f'--print-to-pdf={pdf_root_path}',
    os.path.abspath(html_dest)
]
subprocess.run(cmd, check=True)
shutil.copyfile(pdf_root_path, pdf_docs_path)
print('PDF generated and copied.')

# Check PDF page content
doc = fitz.open(pdf_root_path)
print(f'Total pages: {len(doc)}')

for i, page in enumerate(doc):
    text = page.get_text()
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    print(f'Page {i+1} has {len(lines)} lines. Last line: {lines[-1] if lines else "NONE"}')

# Render PNG photos at 3x resolution (~216 DPI)
os.makedirs('solution/docs/photos', exist_ok=True)
matrix = fitz.Matrix(3.0, 3.0)
for i, page in enumerate(doc):
    pix = page.get_pixmap(matrix=matrix, alpha=False)
    root_png = f'Europress_Part1_Weighing_Concept_Page_{i+1}.png'
    doc_png = f'solution/docs/photos/page_{i+1}.png'
    pix.save(root_png)
    pix.save(doc_png)
    print(f'Saved Page {i+1} PNG: {pix.width}x{pix.height}')

print('All artifacts generated successfully!')
