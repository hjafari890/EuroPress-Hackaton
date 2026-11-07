# Europress SMART Material Value Engine — 3-Minute Hackathon Pitch Script
**Target Audience:** Europress Group Oy Leadership, Since AI Hackathon Jury  
**Presentation Time:** 3 Minutes + 2 Minutes Q&A  
**Core Motto:** *"Weigh at Source, Create Value: From Steel Manufacturer to Circular Economy Partner"*

---

## Slide 1: The Core Problem (0:00 - 0:40)
**Visual:** Split screen: An arched cardboard box inside a compactor hopper vs. an invoice with €180 haulage fee for 800 kg.

**Speaker 1:**
> "Good afternoon judges and Europress leadership. 
> 
> In waste management, every single euro is billed in **tonnes**—haulage tipping fees, incineration penalties, and cardboard rebates. Yet for decades, compactors have only measured **volume percentage**.
> 
> This mismatch creates an expensive disaster for Europress customers:
> 1. **Cardboard Bridging (Scenario S40):** A single corrugated box jams across the hopper. The hydraulic ram spikes pressure, the machine shouts *'95% Full'*, and a retail store pays a **€180 haulage fee** to transport compressed air—only **800 kg** inside a **3-tonne** container. Across the public competition dataset alone, this happens hundreds of times, wasting over **€350,000** in avoidable transport.
> 2. **The 30-Day Data Blackout:** Haulers hold the depot weighbridge tickets. In the dataset, **26.6% of collections have zero weighbridge data shared**, and delayed tickets lag by up to **116 days**. Customers cannot audit what they are paying for.
> 
> Today, we present the **Europress SMART Material Value Engine**."

---

## Slide 2: The Engineering Solution — Part 1 Hardware (0:40 - 1:20)
**Visual:** Technical schematics showing COMBI roller shear-pins and DUO clamp-bridging load cells.

**Speaker 2:**
> "To solve this practically without blowing customer budgets, we developed a **Two-Tier Hardware Architecture**:
> 
> * **Tier 1 Lite (€74 BOM):** A 45-minute bolt-on retrofit for Europress's existing 15,000+ fleet. Dual strain sensors on the front legs + hydraulic compaction energy monitoring + MEMS tilt IMU. It delivers **$\pm 4.5\%$ accuracy**, completely eliminating bridging false-alarms and panic weekend emptyings.
> * **Tier 2 Factory / Verify (€192 BOM):** For new COMBI units ($\le 22\text{ m}^3$) and stationary DUO units ($\le 30\text{ m}^3$). We place dual-shear load pins in the rear rollers and solve the notorious **15–30% DUO clamp friction bridging** using lower hook load pins—meaning **zero wires on swappable containers**.
> 
> In our step-load validation test protocol at Kerava, Tier 2 achieves **$\pm 2.6\%$ accuracy** ($\pm 78\text{ kg}$ on a 3 t load)—comfortably beating the brief's $\pm 100\text{ kg}$ requirement."

---

## Slide 3: The Software Cockpit & Benchmark Proof (1:20 - 2:10)
**Visual:** Live demo of the Cockpit UI showing True-Fullness, Day-0 Ledger, and Operator Scorecards.

**Speaker 1:**
> "Hardware measures weight; our **SMART Value Engine** turns that weight into cash.
> 
> On the official competition benchmark, our engine achieved:
> * **99.68% Value Capture on Contract & Operator Actions (Task C2)**, slashing decision regret from €240.07 down to **€3.46 per case**.
> * **Premature Lift Detection $F_1$ of 0.865 (Task B)**, jumping recall from 59% to 85% by recognizing cardboard bridging and weekend panic calls.
> * **Deconvolved Hauler Tare Bias Error slashed to 0.68% MAE (Task B2)** using empirical Bayes shrinkage.
> 
> In our live Cockpit:
> 1. Store managers see **True Weight Fill %** alongside pressure volume, receiving an automated anti-bridging crush recommendation instead of calling a hauler.
> 2. Customers receive a **Day-0 Weight Ledger** the second the truck departs, automatically cross-checking hauler invoices 30 days later.
> 3. Disputed invoices require **one-click human approval**, outputting professional, non-accusatory inquiry letters based on sensor facts."

---

## Slide 4: Commercial Business Case & Europress Growth (2:10 - 3:00)
**Visual:** Economics dashboard showing Customer Payback (2.4 mo) and Europress ARR (€960,000).

**Speaker 3:**
> "The economics create an immediate win-win:
> 
> * **For the Customer:** A typical supermarket saves **€1,930 every year** per compactor through 10 avoided haulage lifts and automated invoice recovery. Against our €32/month SaaS tier, the investment **pays for itself in just 2.4 months**.
> * **For Europress:** This shifts Europress from a one-off machinery sale to a recurring software powerhouse. With 25% adoption across 10,000 Nordic units, Europress unlocks **€960,000 in annual recurring SaaS revenue (ARR)** at an **$>82\%$ gross margin**.
> * **Legal & Compliance:** 100% of our code runs on permissive MIT, Apache, and BSD open-source libraries. Zero copyleft code, and zero vendor friction.
> 
> Europress compactors already lead European engineering; with the SMART Material Value Engine, Europress now owns the **financial and circular data ledger** of the circular economy. Thank you, and we welcome your questions!"

---

## Jury Q&A Defense ("Grill Me" Preparation)

### Q1 (Jury/Europress): *"On DUO compactors, containers are constantly swapped by third-party haulers. How do you weigh without putting expensive sensors or wiring on every container?"*
**Answer:**  
> "That was our primary design constraint. We put all active sensors on the **stationary press unit and floor guides**—zero wires on the swappable containers. The rear of the container sits on stationary flat low-profile weigh pads embedded into the floor guide rails. To capture the 15–30% container weight that transfers onto the press unit through friction at the hydraulic clamps, we use instrumented dual-shear load pins directly inside the lower press locking hooks. When clamped, the hooks measure the vertical tension vector, mathematically decoupling press friction from container payload."

### Q2 (Jury): *"How do you handle Nordic winter weather, where 300 kg of snow and ice accumulate on top of the container?"*
**Answer:**  
> "We deconvolve passive roof weight from payload using **hydraulic compaction stroke work integration**. Waste inside the chamber creates stroke resistance and hydraulic pressure spikes as the piston advances. Snow or ice on the container roof adds passive static mass but requires zero hydraulic compaction energy. When our static strain rises without corresponding compaction work cycles, the auto-calibration engine flags a winter environmental load bias and adjusts the tare baseline."

### Q3 (Jury): *"Waste operators are vital partners for Europress. Won't an invoice audit tool cause friction between customers and waste haulers?"*
**Answer:**  
> "We explicitly engineered regulatory and commercial neutrality into the platform. We strictly avoid inflammatory words like 'fraud' or 'cheating'. Every discrepancy is phrased objectively—such as *'Tonnage differing from weighbridge record'* or *'Line tariff exceeding index rate'*. Crucially, the system does not auto-withhold payment; it generates a professional inquiry with Day-0 sensor data, turning adversarial disputes into evidence-based supplier collaboration. In fact, haulers with high scorecards use our data to demonstrate transparency."

### Q4 (Jury): *"Why not just use volume cameras or computer vision inside the container?"*
**Answer:**  
> "Computer vision fails inside a waste compactor for three physical reasons: 
> 1. Dust, moisture, and shredded waste coat optical lenses within days.
> 2. Cameras only observe surface geometry, which cannot measure material bulk density or hidden moisture.
> 3. Optical sensors do not measure mass (kg), which is the sole legal currency of waste haulage billing."
