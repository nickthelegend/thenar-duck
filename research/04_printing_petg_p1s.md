# 04 — Printing the microduck in PETG on a Bambu Lab P1S: design-for-manufacturing rules

Scope: structural shells, links and servo brackets for a ~40 cm, STS3215-driven BDX-style biped, printed in PETG on a stock Bambu Lab P1S (0.4 mm stainless nozzle, textured PEI plate, no hardened extruder). Every number below is cited; where I could not verify a number it is marked **[unverified]** or listed under Open questions. "Stock profile" values were read directly from the Bambu Studio profile JSONs in the `bambulab/BambuStudio` repository, so they are the values the slicer actually ships with, not forum folklore.

Compiled 2026-09-26.

---

## 0. TL;DR (decision-relevant numbers)

| Topic | Number | Source |
|---|---|---|
| P1S advertised build volume | 256 × 256 × 256 mm | [Bambu P1S tech-spec sheet (PDF)](https://marketplace.createeducation.com/wp-content/uploads/2023/11/bambu-lab-P1S-tech-specs.pdf) |
| Stock excluded bed area (front-left, cutter stopper) | 18 × 28 mm | [Bambu wiki: print volume limitations](https://wiki.bambulab.com/en/knowledge-sharing/print-volume-limitations); `bed_exclude_area: 0x0,18x0,18x28,0x28` in [P1S machine profile](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json) |
| Stock printable height in Bambu Studio | 250 mm (256 only with the stopper mod + AMS/cutter disabled) | [Bambu wiki: print volume limitations](https://wiki.bambulab.com/en/knowledge-sharing/print-volume-limitations) |
| Practical XY with exclusion zone, Z with z-hop | 238 × 256 × 249 or 256 × 228 × 249 mm (community measurement) | [Bambu forum: real maximum print volume](https://forum.bambulab.com/t/what-is-the-real-maximum-print-volume/12875) |
| Layer heights allowed with 0.4 mm nozzle | 0.08–0.28 mm (20–70 % of nozzle); first layer 0.2 mm | [Bambu wiki: layer height](https://wiki.bambulab.com/en/software/bambu-studio/layer-height) |
| Bambu PETG Basic nozzle / bed | 230–260 °C nozzle, 65–75 °C bed; stock profile 255 °C (245 °C first layer), 70 °C textured PEI | [PETG Basic TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf); [PETG Basic @BBL X1C profile](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PETG%20Basic%20%40BBL%20X1C.json) |
| Bambu PETG Basic fan (stock) | min 20 %, max 40 %, first layers 0 %, overhang 50 % | same profile + [@base](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PETG%20Basic%20%40base.json) |
| Chamber temp recommended for PETG Basic | 35–50 °C (P1S has no heater; passive) | TDS V3.0 |
| PETG Basic Tg / HDT | Tg 69 °C; HDT 68 °C @1.8 MPa, 71 °C @0.45 MPa | TDS V3.0 |
| PETG Basic strength XY vs Z | Tensile 51 vs 35 MPa; impact 34.2 vs 10.5 kJ/m² | TDS V3.0 |
| PETG Basic density | 1.25 g/cm³ | TDS V3.0 |
| Max overhang / bridge (Bambu's claim) | ~70°, ~30 mm | TDS V3.0 |
| Stock elephant-foot compensation (0.20 mm profiles) | 0.15 mm | [fdm_process_single_0.20.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_single_0.20.json) |
| Stock XY hole / contour compensation | 0 / 0 mm | [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json) |
| Stock walls / infill / line widths | 2 walls, 15 % grid, 0.42 outer / 0.45 inner / 0.50 first-layer line width | fdm_process_common.json |
| STS3215 body | 45.2 × 24.7 × 35 mm, 55 ± 1 g, 25T / OD 5.9 mm spline, torque cut-off above 70 °C | [Feetech STS3215 datasheet (translated PDF)](https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf); [Feetech product page](https://www.feetechrc.com/525603.html) |
| Heat-set insert holes | M2 ≈ 3.1–3.2 mm; M2.5 ≈ 3.4–3.8 mm (brand-dependent); M3 ≈ 3.9–4.0 mm | [3DJake/ruthex M2](https://www.3djake.com/ruthex/threaded-insert-m2-70-pieces), [3DJake/ruthex M3](https://www.3djake.com/ruthex/threaded-insert-m3-100-pieces), [Accu chart](https://accu-components.com/us/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin), [InsertGuide](https://insertguide.com/guides/heat-set-insert-hole-size/) |
| Filament for a first build | ~0.8–1.2 kg in the robot, buy 2.5–3 kg (estimate, see §5) | derived from [Open Duck Mini v2 slicer estimate](https://github.com/soyeon24/open-duck-mini-v2-build) |
| Indian PETG price | Numakers PETG-HS Rs 599/kg; eSun ≈ Rs 1,290 + GST to Rs 2,025/kg; Bambu PETG Basic US$23/spool (INR reseller price **unverified**) | [Numakers](https://india.numakers.com/products/petg-hs-filament), [ElectronicsComp](https://www.electronicscomp.com/esun-petg-1.75mm-3d-printing-filament-1kg-solid-black), [Flipkart](https://www.flipkart.com/esun-3d-petg-black-filament-1kg-2-2lb-1-75mm-solid-printer/p/itm557274389850f), [ToolGuyd](https://toolguyd.com/bambu-petg-basic-3d-printing-filaments-relaunch-2026/) |

---

## 1. The P1S as a PETG machine

### 1.1 Build volume, exclusion zone, real usable envelope

- Advertised build volume is **256 × 256 × 256 mm**; the included plate is the **Bambu Dual-Sided Textured PEI Plate**; all-metal hotend to **300 °C**, **0.4 mm stainless-steel** nozzle included (0.2/0.6/0.8 optional), max bed **100 °C**, toolhead 500 mm/s and 20 m/s². Supported-filament table lists PETG under **"Ideal"**, PA/PC under "Capable" and carbon/glass-fibre polymers as **"Not Recommended"** on the stock toolhead. [Bambu P1S tech-spec sheet](https://marketplace.createeducation.com/wp-content/uploads/2023/11/bambu-lab-P1S-tech-specs.pdf), [bambulab.com/en/p1 FAQ](https://bambulab.com/en/p1) ("it is not recommended to directly print fiber-reinforced filaments … before an extruder and hotend upgrade is done").
- Bambu's own wiki explains why the stock slicer envelope is smaller than 256³: "The lost print volume is **18x28mm for the front left corner**" (the filament-cutter stopper), and Bambu Studio's default printable height is **250 mm** because z-hop needs headroom; you can "Clear the 'Excluded bed area' … and change the printable height from the default 250mm to 256mm" only after collapsing the stopper with a printed clip and accepting that "The full print volume is only accessible when the AMS system is NOT used." [Bambu wiki: print volume limitations](https://wiki.bambulab.com/en/knowledge-sharing/print-volume-limitations). The machine profile confirms `bed_exclude_area = (0,0)-(18,28)` and `printable_area = 256 × 256`, `extruder_clearance_radius 57 mm`, `extruder_clearance_height_to_lid 90 mm` (the latter two limit by-object/sequential printing). [P1S machine JSON](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json), [common machine JSON](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/fdm_bbl_3dp_001_common.json).
- Community measurement of what actually fits with the exclusion zone and z-hop left stock: "**H 249mm W 238mm D 256mm**" or "**H 249mm W 256mm D 228mm**". [Bambu forum thread](https://forum.bambulab.com/t/what-is-the-real-maximum-print-volume/12875).
- Brim/skirt overhead from the stock process profile: `brim_width 5 mm`, `brim_object_gap 0.1 mm`, `skirt_loops 0`, `skirt_distance 2 mm` — i.e. a brimmed part needs its footprint **+5 mm on every side**; Bambu prints no skirt by default (it prints a purge line at the front of the plate instead). [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json); purge/wipe zone description in [Bambu wiki: build plates](https://wiki.bambulab.com/en/filament-acc/acc/plates).
- **Max part diagonal (derived):** flat XY diagonal is √2 × 256 = **362 mm** for a zero-width part laid front-right to back-left (that diagonal avoids the 18 × 28 mm front-left exclusion); a strip of width *w* on that diagonal gets roughly 362 − *w* mm. In practice for this robot: keep every link ≤ ~240 mm axis-aligned, or ≤ ~300 mm × 30 mm if laid diagonally, and keep tall prints ≤ 249 mm. (Derived from the numbers above; no separate source.)

### 1.2 Textured PEI plate and PETG

- The Textured PEI plate "is the standard plate included with Bambu lab printers … In most cases, it provides excellent adhesion without the need for an adhesive"; glue stick is mentioned only for PC/PA/ABS/ASA. Prints "come off easily when the temperature of the heatbed reaches room temperature, and we always recommend waiting until it reaches 35℃ or lower." [Bambu wiki: build plates](https://wiki.bambulab.com/en/filament-acc/acc/plates).
- Do **not** print PETG bare on the **Smooth** PEI plate: "Only PLA filament does not require glue, while printing with other filaments requires the use of gluing to prevent the PEI sheet from tearing." [same page]. Prusa says the same for their smooth sheet: "Do not print on the smooth PEI sheet as the adhesion may be too strong!" [Prusa KB: PETG](https://help.prusa3d.com/article/petg_2059).
- Dimensional side-effect: Bambu Studio applies a plate-specific Z offset — "the Textured PEI Plate lowers the nozzle by 0.04 mm automatically during levelling" — so always select the correct plate type in the slicer, and note that elephant-foot compensation "can vary between different types of build plates, so values are not interchangeable." [Bambu wiki: warping](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing), [Bambu wiki: elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot). The bottom face of every part will carry the plate texture; if a bottom face is a mating/bearing face, print it on the smooth side (with glue) or design that face as a top/side surface.
- PETG Basic TDS lists plate options "Cool Plate Supertack / Textured PEI Plate / Smooth PEI Plate" and, contradicting the wiki slightly, "Glue: Recommended (Glue Stick/Liquid Glue)". [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). Interpretation: on textured PEI, glue is a *release agent* for large flat PETG bottoms, not an adhesion aid.

### 1.3 Nozzle and layer-height defaults

- 0.4 mm nozzle: "the appropriate printing layer height is between **0.08mm and 0.28mm**"; the stock first-layer height is nozzle × 50 % = **0.2 mm**. [Bambu wiki: layer height](https://wiki.bambulab.com/en/software/bambu-studio/layer-height). Stock process: `layer_height 0.2`, `initial_layer_print_height 0.2`, `line_width 0.42`, `outer_wall_line_width 0.42`, `inner_wall_line_width 0.45`, `initial_layer_line_width 0.5`. [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json).
- Bambu's PETG guide: "with a 0.4 mm nozzle, the default inner wall line width is 0.45 mm, and the outer wall is 0.42 mm … It is recommended to adjust the line width within 0.75 to 1.5 times the nozzle diameter." [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg).
- "Precise Z height" (Bambu Studio ≥ 1.9) "fine-tune[s] the height of the last 5 layers to ensure that the final layer height matches the actual value" — turn it on for any part whose total height is a mating dimension. [Bambu wiki: layer height](https://wiki.bambulab.com/en/software/bambu-studio/layer-height).
- Recommendation for this robot: **0.20 mm** for shells and links; **0.12–0.16 mm** for parts with horizontal bearing pockets, servo pockets, or snap features (better Z resolution of round features and less stair-stepping on 45–60° overhangs). Stainless nozzle is fine for plain PETG; PETG-CF/PA-CF need a hardened nozzle *and* the P1S extruder upgrade (see §4).

### 1.4 Does the enclosure help PETG? (door / top glass)

- Bambu's TDS gives a **chamber temperature of 35–50 °C** for PETG Basic. [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). The P1S has a "Chamber Temperature Regulator Fan" and auxiliary part-cooling fan but no chamber heater. [P1S spec sheet](https://marketplace.createeducation.com/wp-content/uploads/2023/11/bambu-lab-P1S-tech-specs.pdf).
- Heat-creep rule from Bambu: "always keep the temperature inside an enclosure at least 10 degrees lower than the glass transition temperature of the filament … It also applies to PETG filament if the enclosure temperature is too high." With Tg = 69 °C for PETG Basic that means chamber ≤ ~59 °C; the "open door / top off" advice on that page is written for **PLA** on the textured plate. [Bambu wiki: heat creep](https://wiki.bambulab.com/en/filament-acc/filament/heat-creep).
- Community reading of Bambu's Filament Guide is "PETG: Top off" (door not specified); users also report success "with the top on and the door closed" on a P1S; no measured chamber temperatures were posted. [Bambu forum: P1S cover and door open or closed](https://forum.bambulab.com/t/p1s-cover-and-door-open-or-closed/25553).
- Bambu's own PETG guide: "PETG is more prone to warping than PLA. In most cases, warping occurs due to the layers cooling too quickly" — recommended fixes are glue, brim, and avoiding drafts. [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg). Warping-risk ranking from Bambu: "PC → PA-CF → PA → ABS → ASA → PETG → PLA" (PETG second lowest). [Bambu wiki: warping](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing).
- **Practical rule for the P1S in an Indian room (30–35 °C ambient):** door closed, top glass on for the first hour of large parts (draft protection, better layer bonding), then crack the top glass if the chamber reads > 50 °C on a cheap thermometer; never let it approach 59 °C. Verify with a thermometer — Bambu publishes no P1S passive chamber curve (Open question #5).

---

## 2. Bambu Studio PETG settings that matter for dimensional accuracy

### 2.1 Stock profile values (what the slicer actually ships)

| Setting | Bambu PETG Basic (P1S/X1C) | Generic PETG (@base) | Bambu PETG HF (@base) | Source |
|---|---|---|---|---|
| Nozzle temp / first layer | 255 / 245 °C | 255 / 255 °C (from `fdm_filament_pet`) | 245 / 230 °C | [PETG Basic @BBL X1C](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PETG%20Basic%20%40BBL%20X1C.json), [fdm_filament_pet](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/fdm_filament_pet.json), [PETG HF @base](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PETG%20HF%20%40base.json) |
| Allowed nozzle range | 230–270 °C | 220–270 °C | 230–270 °C | same |
| Textured / hot plate temp | 70 °C | 70 °C | 70 °C | same |
| Fan min / max | 20 % / 40 % | 40 % / 90 % | 10 % / 40 % | same |
| Overhang fan | 50 % | 90 % | 90 % | same |
| First-layer fan | 0 % | (inherits) | (inherits) | [PETG Basic @base](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PETG%20Basic%20%40base.json) |
| Fan cooling layer time / slow-down layer time | 30 s / 12 s | 30 s / 12 s | 30 s / 12 s | same |
| Flow ratio | 0.95 | 0.95 | 0.95 | same |
| Max volumetric speed | 15 mm³/s | 12 mm³/s | 21 mm³/s | same |
| Retraction | 0.4 mm (filament override; machine default 0.8 mm @ 30 mm/s) | machine default 0.8 mm | (inherits) | PETG Basic @BBL X1C; [P1S machine JSON](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json) |
| Z-hop | 0.4 mm, PETG Basic forces "Spiral Lift"; wipe 1 mm | 0.4 mm Auto Lift | — | same |
| Density | 1.25 g/cm³ | 1.27 (generic default) | 1.28 | same |
| Vitrification (softening) temp used by slicer | 60 °C | 70 °C | — | same |

- The TDS ranges agree: nozzle 230–260 °C, bed 65–75 °C, cooling fan 0–60 %, speed < 200 mm/s, retraction 0.4–0.8 mm at 30–60 mm/s, "Support Material: Support for PLA/PETG". [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf).
- **"Bambu PETG Basic" vs "Generic PETG":** the Bambu profile runs hotter first layer *cooler* (245 °C), much *less* fan (20–40 % vs 40–90 %) and faster flow (15 vs 12 mm³/s). Less fan = stronger layer bonding but more sag on overhangs; the Generic profile's 90 % fan is what you want for bridges and dimensional crispness on cheap PETG at the cost of Z-strength. For Indian filament (eSun/Numakers) start from **Generic PETG**, then calibrate flow, PA and shrinkage per spool (§2.3).
- Product status: PETG Basic was "discontinued due to product optimization" in June 2024 [Bambu forum](https://forum.bambulab.com/t/petg-basic-has-been-discontinued/81068) and **relaunched on 27 Mar 2026** with a new formula: vs PETG HF "Bending Strength (XY): 75 MPa vs 64 MPa; Layer Strength (Z): 56 MPa vs 48 MPa; Toughness (XY): 34.2 kJ/m² vs 31.5 kJ/m²", priced US$23/spool, US$20 refill. [ToolGuyd](https://toolguyd.com/bambu-petg-basic-3d-printing-filaments-relaunch-2026/). The TDS V3.0 numbers in this file are for the relaunched formula.

### 2.2 Flow, temperature, line width (Bambu's PETG-specific advice)

- "The recommended flow ratio range for PETG-like filaments is **0.93 – 0.96**. Below 0.93: May cause under-extrusion and weaken layer adhesion strength. Above 0.96: Can increase layer adhesion strength but may lead to oozing or clogging." Default 0.95 for PETG Basic; reduce to 0.93–0.94 only if clogging. [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg).
- Lower temperature when you lower speed (less oozing); raise it when running near max volumetric speed. Reduce line width to 0.36–0.40 mm only for non-structural parts ("If you don't have high requirements for model strength"). [same].
- Dimensional-accuracy workflow on a P1S (no LiDAR): run Flow Dynamics (pressure advance) manually per spool — "Manual calibration is the go-to method for P1P/P1S users since it's the only method available" — then flow-rate calibration. [Bambu wiki: flow rate calibration](https://wiki.bambulab.com/en/software/bambu-studio/calibration_flow_rate), [BabaBuilds calibration guide](https://bababuilds.com/blog/bambu-lab-calibration-guide/).
- Drying is a dimensional setting, not just a cosmetic one: "PETG filaments are highly hygroscopic"; dry **60–65 °C for 8 h** (oven) or **80 °C for 12 h** on the heat bed, store at "< 20% RH (Sealed, with desiccant)". Wet PETG gives "stringing, oozing, holes, rough surfaces, and low strength". [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg), [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). In monsoon humidity, dry every spool before precision parts.

### 2.3 Shrinkage compensation

- Bambu Studio has a per-filament **Shrinkage** field (Filament Settings → Basic Information), default 100 %; value = (measured / designed) × 100 %. It "only adjusts the scaling of the model's outer dimensions (X and Y axes). It does not affect the size of internal features (such as holes and contours)". Calibrate with a 20 mm or 100 mm cube; Bambu's example went 18.5 → 19.7 mm after one correction. [Bambu wiki: 3D print shrinkage](https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage).
- Typical magnitude on Bambu CoreXY machines: users measured **99.71 / 99.69 mm on 100 mm** test prints (≈0.3 % undersize), PLA slightly better than PETG, and "0.1mm around the measurement is what to expect". [Bambu forum: dimensional accuracy](https://forum.bambulab.com/t/how-to-tune-your-bambu-printer-for-dimensional-accuracy/25564). Prusa characterises PETG as having "very little thermal expansion" so it "does not shrink or warp" much. [Prusa KB: PETG](https://help.prusa3d.com/article/petg_2059). Bambu publishes no per-material % — **measure your own spool** (Open question #6).
- Fibre-filled filaments shrink less ("the fibers act as reinforcement and help control the shrinkage"), which is one argument for PETG-CF on precision brackets *if* you upgrade the nozzle. [Bambu wiki: 3D print shrinkage](https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage).

### 2.4 Elephant foot

- Cause: first layer "pressed onto the heatbed … still soft" plus weight of upper layers; "On tolerance-critical parts such as assemblies, snaps, rails, and shaft holes, the flared base directly affects fit." Setting: Process → Quality → Precision → Elephant foot compensation. Calibration: print a 25 × 25 × 10 mm cube with compensation 0 and no brim, measure top vs bottom width mid-side, value = average deviation (Bambu's worked example: 0.10 mm). [Bambu wiki: elephant foot](https://wiki.bambulab.com/en/software/bambu-studio/parameter/elephant-foot).
- Stock value: the base process sets 0, but the 0.20 mm single-extruder profiles set **`elefant_foot_compensation 0.15`**. [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json), [fdm_process_single_0.20.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_single_0.20.json).
- PETG-specific note: the bed sits at 70 °C, above PETG Basic's 60 °C "vitrification" value in the profile and only ~9 °C under its Tg of 69 °C, so the bottom millimetre stays soft the whole print; some flare is unavoidable — design a **0.3–0.5 mm × 45° chamfer on every bottom edge** so the flare has nowhere to go, and keep bearing pockets and servo pockets off the first layers.

### 2.5 XY hole and contour compensation

- Two separate fields under Process → Quality → Precision. **XY Hole Compensation** "only affects holes and does not change the outer size of the model"; **XY Contour Compensation** "increases or decreases the overall XY size while keeping hole sizes unchanged". "The hole diameter will increase by twice the compensation value." Calibrate with a metric-screw hole test (M6 recommended; ISO 6g M6 measures ≈5.9 mm); Bambu's example lands at **+0.15 mm**. Limitation: hole compensation "only applies to closed paths" — a pocket open to the side of the part is not a hole to the slicer and will not be compensated; "noticeable layer separation will occur" if you force it. [Bambu wiki: XY hole/contour compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation).
- Stock: `xy_hole_compensation 0`, `xy_contour_compensation 0`. [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json).
- Fix these *before* touching compensation: material shrinkage, elephant foot, moist filament, untuned flow dynamics, holes near nozzle size, missing chamfers/lead-ins, seam position. [same wiki].
- "Auto circle contour-hole compensation" (Quality → Precision) is "mainly optimized for the H2D"; on other printers "it may not give the best results. In this case, you do not need to enable the feature." [Bambu wiki: 3D print shrinkage](https://wiki.bambulab.com/en/knowledge-sharing/3d-prints-shrinkage). So on the P1S, calibrate manually.
- **Precise wall** (Quality → Precision) keeps the outer wall at exactly one line width and improves inter-layer consistency; **Arachne** vs **Classic** wall generator changes how thin features are sized (stock is `wall_generator classic`). Community explanation: [Fashion3D: Classic vs Arachne](https://www.fashion3d.com.au/blogs/news/bambu-studio-settings-01-classic-vs-arachne-wall-generator); stock value from [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json). Use Precise wall + Classic for mechanical parts; Arachne only for thin cosmetic shells.

### 2.6 Stringing control

- Root cause #1 is moisture (see §2.2). Bambu's ordered fixes: dry; lower temperature when printing slower; keep flow ≤ 0.96; retraction 0.4–0.8 mm at 30–60 mm/s; for un-dried PETG HF use the Generic PETG HF numbers "nozzle temperature 220 ℃, volume speed 16 mm³/s". [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg), [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf).
- Slicer defaults that already help: retract on layer change = 1, wipe = 1 (2 mm machine / 1 mm PETG Basic), z-hop 0.4 mm, retraction minimum travel 1 mm. [P1S machine JSON](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/machine/Bambu%20Lab%20P1S%200.4%20nozzle.json).
- Design-side: avoid tall isolated pins and towers printed in the same job (travel between them = strings); print servo horns/pins in a separate job or use "by object" sequencing (57 mm clearance radius).

---

## 3. Design rules for structural PETG parts

### 3.1 Wall thickness (perimeters beat infill)

- Guidance (Indian FDM bureau): "0.8 mm (two perimeters at 0.4 mm nozzle) — only for non-structural features"; "1.2 mm (three perimeters) for general structural walls"; "2.4 mm or more, combined with 40–60% infill" for load-bearing; snap-fit arms "1.5–2.5 mm". [LayerX 3D: FDM design rules](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances).
- CNC Kitchen: a hook "with more perimeters was nearly 22% stronger than one with more infill" — increase walls before infill. [CNC Kitchen summary via 3dprinting.com](https://3dprinting.com/how-to/how-to-get-stronger-fdm-3d-prints/); Bambu: "keep the wall count ≤ 6 and infill density ≤ 50%" because more walls/infill raise warping stress. [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg).
- With Bambu's stock line widths (0.42 outer + 0.45 inner) design wall thicknesses as multiples so the slicer does not gap-fill: **2 walls ≈ 0.87 mm, 3 ≈ 1.32, 4 ≈ 1.77, 5 ≈ 2.22, 6 ≈ 2.67 mm** (derived from `outer_wall_line_width 0.42`, `inner_wall_line_width 0.45`). Set `detect_thin_wall` on (stock 0) for any rib thinner than 0.87 mm, or better, never design one.
- **Recommendation for the duck:** shells 3 walls / 4 top / 4 bottom / 15–20 % gyroid; leg links and servo brackets **4–5 walls / 5 top / 5 bottom / 30–40 % gyroid**; anything under 4 mm thick → 100 % (set via modifier). Gyroid is Bambu's own pick for warping-prone large flat parts ("Gyroid shrinks more evenly in all directions"), and grid/triangle patterns "cross in a single layer, building a small bump that the nozzle clips". [Bambu wiki: warping](https://wiki.bambulab.com/en/filament-acc/filament/print-quality/warping-falling-off-collapsing). Research on FDM PETG finds "infill density is the most dominant factor … while infill pattern … has comparatively limited impact". [ScienceDirect: functionally graded PETG](https://www.sciencedirect.com/science/article/pii/S2949822825006112).

### 3.2 Screw bosses, heat-set inserts, screws-into-plastic

Insert hole diameters (design the CAD hole; verify with a test coupon because "Printed holes almost always come out smaller than in CAD" [CNC Kitchen](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts)):

| Thread | Insert OD (ruthex) | CAD hole Ø | Boss OD (min) | Depth | Sources |
|---|---|---|---|---|---|
| M2 | 3.6 mm, L 4.0 | **3.1–3.2 mm** | ≥ 3.6 + 2 × 1.3 = **6.2 mm** (min wall 1.3) | insert L + 1 mm | [3DJake ruthex M2](https://www.3djake.com/ruthex/threaded-insert-m2-70-pieces) (D1 3.6, D2 3.1, D3 3.2, W 1.3); [Accu FAQ](https://accu-components.com/us/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin) (3.0–3.2 mm) |
| M2.5 | ruthex RX-M2.5x5.7 (OD not retrieved) | **3.4–3.8 mm, brand-specific** | ≈ insert OD + 2.6 mm | insert L + 1 mm | [InsertGuide](https://insertguide.com/guides/heat-set-insert-hole-size/) (3.8 mm); forum-quoted 3.4–3.6 mm **[unverified]**; see Open question #4 |
| M3 | 4.6 mm, L 5.7 (ruthex); 4.4 mm (Accu) | **3.9–4.0 mm** (users report 4.1 mm best for ruthex) | ≥ 4.6 + 2 × 1.6 = **7.8 mm** (min wall 1.6) | insert L + 1 mm | [3DJake ruthex M3](https://www.3djake.com/ruthex/threaded-insert-m3-100-pieces) (D1 4.6, D2 3.9, D3 4.0, W 1.6); [Accu chart](https://accu-components.com/us/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin) (4.0 mm −0/+0.1); [3DJake reviews via search](https://www.3djake.com/ruthex/threaded-insert-m3-voron-100-pieces) |

- Rules: blind hole "roughly 1 mm deeper than the insert is long, straight rather than tapered holes, respect the minimum wall thickness, and normally no chamfer at the hole edge"; iron at "10 to 20 °C above your printing temperature: … **245 °C for PETG**"; melt "only about 90% of the way" then press flush; horizontal (side-wall) holes come out smaller at the top, so print a coupon per orientation. [CNC Kitchen](https://www.cnckitchen.com/blog/tips-and-tricks-for-heat-set-inserts). Boss OD rule of thumb 1.5–2× insert OD. [Sovol](https://www.sovol3d.com/blogs/news/3d-printing-with-heat-set-inserts-design-strong-screw-bosses-that-last). Depth ≥ insert length + two thread pitches. [InsertGuide](https://insertguide.com/guides/heat-set-insert-hole-size/). PETG "Tougher, but plastic flow and stringing can be more noticeable" during install. [same].
- Screws directly into PETG: pilot 80–90 % of screw major diameter (M2 ≈ 1.6–1.8 mm, M3 ≈ 2.4–2.7 mm); "threads may wear out with repeated use and are less durable than heat-set inserts". [Kingroon](https://kingroon.com/blogs/3d-print-101/how-to-screw-into-3d-printed-parts), [Accu](https://accu-components.com/us/p/488-threaded-insert-hole-size-charts-for-3d-printing-pla-petg-resin). Never rely on a self-tapped thread that crosses layer lines for a joint you will open more than twice.
- What the reference design does: Open Duck Mini v2's BOM lists "3D printing M3 inserts" and the servos ship with "M3X6" horn screws. [Open Duck Mini v2 BOM (Google Sheet)](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing), [Feetech datasheet](https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf). **Recommendation:** M3 heat-set inserts for every structural joint and every servo-tab screw; M2/M2.5 inserts only for electronics and covers; M2 self-tappers only for cosmetic panels.

### 3.3 Servo pocket for the STS3215 (45.2 × 24.7 × 35 mm body)

- Body 45.2 × 24.7 × 35 mm, 55 ± 1 g, output spline 25T / OD 5.9 mm, horn screw M3 × 6, "Turn off the torque output when the temperature is higher than 70°C", rated 19.5 kg·cm @ 7.4 V, no-load 0.238 s/60° @ 7.4 V. [Feetech STS3215 datasheet (translated)](https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf), [Feetech product page](https://www.feetechrc.com/525603.html) (Size A 45.2, B 24.7, C 35 mm), [Waveshare ST3215 wiki](https://www.waveshare.com/wiki/ST3215_Servo) (45.22 × 35 × 24.72 mm, 6–12.6 V).
- Pocket clearance: micro-servo mount guides use body **+0.2 mm per axis** so the servo "should slide in with light finger pressure but not fall out when turned upside down"; Kapton tape shims if loose. [Kpower servo-mount guide](https://www.kpower.com/insight_bldc/7305.html). Printed pockets read as *holes* and come out 0.1–0.3 mm undersize (LayerX: "Hole diameter −0.3 to −0.5 mm undersized" on uncalibrated machines) [LayerX 3D](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances), [Creative3DP](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/).
- **Recommendation:** after calibrating XY hole compensation so an M6 hole prints true, model the pocket at **45.5 × 25.0 mm** (+0.15 mm/side) with three 0.2 mm-proud crush ribs on the long faces, 0.5 mm × 45° lead-in chamfer, and never let the pocket be "open" on the side that the slicer needs closed for hole compensation (§2.5). Locate the servo by its mounting tabs and the output-shaft boss, not by the pocket walls. Screw length matters: "If screws make contact with the servo body during tightening … can ultimately cause the servo to burn out." [Waveshare ST3215 wiki](https://www.waveshare.com/wiki/ST3215_Servo). Mounting-tab hole pattern: not extractable from the datasheet text — Open question #3.
- **Thermal caveat:** the servo's own cut-off is 70 °C and PETG Basic's HDT is **68 °C @ 1.8 MPa** (Tg 69 °C) [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf); PETG under continuous load near 60 °C creeps ("When subjected to continuous force at around 60°C, creep occurs") [JLC3DP](https://jlc3dp.com/blog/petg-temperature-resistance), [ScienceDirect: creep in 3D-printed PETG](https://www.sciencedirect.com/science/article/abs/pii/S1350630725008611). Keep the servo case ventilated (slots in the pocket, no foam), clamp with screws not preload, and avoid designs where a hot servo case is the only thing holding a press-fit.

### 3.4 Snap fits and living hinges

- Snap-fit cantilevers: fillet at the root "at least 0.5 times the cantilever base thickness"; "minimum width of 5 mm"; FDM clearance 0.5 mm; taper the beam; "avoid snap-fit cantilevers built vertically in the Z direction". [Hubs/Protolabs snap-fit guide](https://www.hubs.com/knowledge-base/how-design-snap-fit-joints-3d-printing/). Arm thickness 1.5–2.5 mm. [LayerX 3D](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances). L/t 5:1–8:1 for ductile materials like PETG, and reduce allowable strain 50 % for any Z-built cantilever. [Sovol snap-fit guide](https://www.sovol3d.com/blogs/news/3d-printed-snap-fit-joints-how-to-design-clips-that-work). PETG Basic's elongation at break is 9.5 % XY but only **5.2 % in Z** [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf) — keep design strain ≤ 1–2 % for anything snapped more than a handful of times. Use snaps only for cosmetic covers (head shell, battery lid); never for structure.
- Living hinges: **no-go in PETG** for anything cycled. PP "is widely regarded as the best material for living hinges"; PETG "can be a candidate for low-cycle closures" only, with FDM showing "a substantial reduction of the elongation at break" for PETG. [Hubs living-hinge guide](https://www.hubs.com/knowledge-base/how-design-living-hinges-3d-printing/), [vprint3d checklist](https://vprint3d.com.hk/resources/living-hinge-design-for-3d-printing-the-2026-engineers-checklist/), [PMC: PETG FDM tensile](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6680790/). Use pinned hinges on bearings or bushings instead.

### 3.5 Overhangs, bridges, fillets vs chamfers

- General 45° rule; well-tuned printers 55–60°. [LayerX 3D](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances), [Snapmaker 45° rule](https://www.snapmaker.com/blog/45-degree-rule-3d-printing/). Bambu claims PETG Basic can do "Max Overhang Angle ~70°" and "Max Bridging Length ~30 mm" (with its profile). [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). Prusa: PETG has "Poor bridging and overhangs" relative to PLA. [Prusa KB: PETG](https://help.prusa3d.com/article/petg_2059). Bridging rule of thumb: PETG "up to 40 mm (more flexible, more sag)" vs PLA 50–60 mm. [LayerX 3D](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances).
- Stock Bambu process: `support_threshold_angle 30`, `bridge_flow 0.95` (1.0 in the 0.20 profile), `max_bridge_length 0` (= no limit), overhang speeds 50/30/10 mm/s for 2/4–4/4 overhangs. [fdm_process_common.json](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/fdm_process_common.json), [0.20mm Standard @BBL X1C](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/process/0.20mm%20Standard%20%40BBL%20X1C.json).
- Chamfer, not fillet, on bottom edges: "With a fillet on the base of a model, the overhang angle changes from 90 to 0 degrees and the first few layers are usually unsupported. With a chamfer … a constant 45 degrees overhang should be easy to handle." [Prusa forum: overhang near the bed](https://forum.prusa3d.com/forum/original-prusa-i3-mk3s-mk3-how-do-i-print-this-printing-help/how-to-improve-angled-overhang-prints-near-the-bed/). Bambu recommends adding **inner fillets** in CAD where thin walls meet large bottoms to kill "step-change layer lines" and keep bridges off inner walls. [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg). LayerX: 1–3 mm fillets at all bottom corners of load paths (internal), wall height-to-base < 8:1. [LayerX 3D](https://layerx3d.in/blog/fdm-design-rules-wall-thickness-overhangs-bridging-tolerances).
- Design targets for this robot: ≤ 45° from vertical without support; 45–60° allowed on non-visible internal faces with overhang fan at 90–100 %; bridges ≤ 25 mm; horizontal holes > 8 mm as teardrops or with a 0.3–0.4 mm sacrificial bridge layer.

### 3.6 Tolerances for rotating fits and bearing pockets

Bearings in scope: **608** (8 × 22 × 7 mm), **MR115** (5 × 11 × 4 mm), **684** (4 × 9 × 4 mm). [123Bearing MR115](https://www.123bearing.com/bearing-housing/deep-groove-bearing/single-row/mr115-2rs), [VXB 684](https://www.vxb.com/684-Bearing-Open-4x9x4-Miniature-p/kit12913.htm), [MakerWorld 608 fitment test](https://makerworld.com/models/36682).

Fit classes (diametral, after you have calibrated hole compensation so holes print true):

| Fit | Diametral offset | Use | Source |
|---|---|---|---|
| Press / interference | −0.10 mm (≈0.05 mm/side; PETG "up to 0.10" per side) | bearing outer race in pocket | [Creative3DP press-fit tolerances](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/) |
| Snug / transition | +0.05 mm | bearing that is also retained by a lip/screw | same |
| Close running | +0.15 mm | printed bushing on metal pin | same |
| Free | +0.35 mm | covers, non-precision | same |
| Prusa's floor for moving parts | ≥ 0.3 mm modelled clearance | any printed-on-printed sliding fit | [Prusa forum: general tolerances](https://forum.prusa3d.com/forum/original-prusa-i3-mk2-s-others-archive/general-tolerances-for-part-design/) |

- Uncalibrated reality check: "A printed hole comes out 0.1–0.3mm undersize … A printed shaft comes out ~0.1mm oversize"; Creative3DP's worked example puts a 608 pocket at **≈21.95 mm** in PLA and recommends a **0.5 mm × 45° lead-in chamfer** and "three or four small ribs (~0.2mm proud)" as a more forgiving alternative to shrinking the diameter. [Creative3DP](https://tools.creative3dp.com/blog/press-fit-tolerances-3d-printing/).
- **CAD starting points for PETG on a calibrated P1S** (derived from the offsets above; print a coupon in 0.05 mm steps before committing):
  - 608 pocket: press **21.85–21.95 mm**; slip/retained **22.05–22.10 mm**; pocket depth 7.2 mm with a 0.6 mm lip on ID 20 mm so the race seats on the lip, not the floor.
  - MR115 pocket: press **10.90–10.95 mm**; slip **11.05–11.10 mm**; depth 4.2 mm.
  - 684 pocket: press **8.90–8.95 mm**; slip **9.05–9.10 mm**; depth 4.2 mm.
  - Inner race: always a **metal** pin/screw shank (M4/M5/M8 shoulder or dowel), never a printed shaft (printed shafts run +0.1 mm and layer-lined).
  - Orient bearing pockets with their axis along Z (round in XY) whenever possible; a pocket printed with its axis horizontal is a polygonised, sagging bridge and needs +0.2–0.3 mm on its vertical diameter plus a teardrop top.
- Bambu's note that hole compensation is "specific to each filament and should be repeated when changing materials" applies doubly to bearing pockets — one profile per spool colour. [Bambu wiki: XY hole/contour compensation](https://wiki.bambulab.com/en/software/bambu-studio/xy-hole-contour-compensation).

### 3.7 Layer orientation vs load (servo brackets, leg links)

- PETG Basic's own datasheet is the clearest argument: tensile **51 MPa (XY) vs 35 MPa (Z)**, bending strength **75 vs 56 MPa**, impact **34.2 vs 10.5 kJ/m²**, elongation **9.5 vs 5.2 %**. [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). CNC Kitchen's Prusament test: PETG layer adhesion is **46 %** of its in-plane strength (25 kg vs 55 kg). [CNC Kitchen: PLA vs PETG vs ASA](https://www.cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament).
- Practical rules: "Print the bracket on its side so the load-bearing shape is formed by continuous strands of plastic, not stacked layers … A clean snap exactly along layer lines indicates interlayer bond failure"; split a part into two halves printed in their best orientations rather than one compromised part; large fillets at every internal junction. [3DBite: print orientation for strength](https://3dbite.com/print-orientation-for-strength-parts-that-dont-snap/). Bambu: decide "the main force direction of the model in actual use. Then, adjust the printing orientation accordingly". [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg).
- For the duck: the knee/ankle links carry bending about the servo axis → print each link **lying on its side** so the bending stress runs along extrusion lines; the servo-tab screw bosses must not be a stack of layers in tension (put the tab plane in XY or add a gusset); the hip "roll motor" clamshells split along a plane that puts the screw bosses in-plane. Open Duck Mini v2 already splits its shins into "knee_to_ankle_left/right_sheet" pairs plus spacers — flat "sheets" printed flat are exactly this rule. [Open Duck Mini v2 print guide](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md).

---

## 4. Community and reference-design advice (Open Duck Mini / BDX replicas / humanoids)

### 4.1 What the reference designs actually print

- **Open Duck Mini v2** (apirrone, ~42 cm, 14 × STS3215 7.4 V): print guide says "Standard material: PLA at **15% infill**; Exception: `foot_bottom_tpu.stl` printed in **TPU at 40% infill**"; 37 unique STLs (feet, knee-to-ankle "sheets" ×8, spacers, roll-motor clamshells, trunk halves, neck sheets, head, body panels, antenna holders, battery lid, eyes/speaker). [print_guide.md](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md), [repo README](https://github.com/apirrone/Open_Duck_Mini). BOM: 14 × "Feetech 7.4v STS 3215" at €14 (€196), "3D printing M3 inserts", "Standard PLA … Maybe 500g of filament", TPU "for the feet, negligeable cost", 3 packs of bearings, total €398 (€331 lowest). [BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing).
- A third-party build log that re-sliced the v2 STL set for Bambu machines reports "**PLA 990 g + TPU 34 g**, Bambu H2D/X1C" for "36 STL types (51 parts)" (slicer estimate, build not yet completed). [soyeon24/open-duck-mini-v2-build](https://github.com/soyeon24/open-duck-mini-v2-build). The gap between "maybe 500 g" and 990 g is supports + the 2025-26 STL set; budget for the larger number.
- Sim-to-real note relevant to the URDF: "because we print with infill we override the mass of the parts with the (pretty accurate) estimation of the slicer" — use Bambu Studio's per-object mass for every link. [Open Duck Mini sim2real.md](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/sim2real.md).
- **Pollen/Hugging Face "Microduck"** (the name the user is using): 25 cm, "under 800 g", 15 motors, US$399 preorder, ships assembled, Dynamixel XL330 servos — not STS3215 — so it is a mass/scale reference, not a print reference. [kingy.ai summary](https://kingy.ai/blog/hugging-face-microduck-physical-ai-robot/), [CNX Software](https://www.cnx-software.com/2026/08/28/microduck-a-duck-like-biped-robot-designed-for-physical-ai-experimentation-and-fun/), [Pollen](https://pollen-robotics.com/microduck/).
- I could not reach the Open Duck Discord or MakerWorld BDX pages (403); the material advice below therefore comes from measured data rather than anecdotes.

### 4.2 PETG vs PLA vs ABS/ASA vs PA-CF for brackets and legs

| Property | PLA | PETG | ASA | Source |
|---|---|---|---|---|
| In-plane pull (Prusament hook) | 73 kg | 55 kg | 57 kg | [CNC Kitchen](https://www.cnckitchen.com/blog/comparing-pla-petg-amp-asa-feat-prusament) |
| Layer adhesion (vertical) | 40 kg (55 %) | 25 kg (46 %) | 17 kg (29 %; +20 % with 30 °C chamber) | same |
| Bending modulus | 3300 MPa | 1900 MPa | 2300 MPa | same |
| Impact | 5 kJ/m² | 8.6 kJ/m² | 18 kJ/m² | same |
| Softens / fails | 60 / 65 °C | 80 / 85 °C | 110 / 120 °C | same |
| Bambu Basic datasheets | PLA Basic density 1.26, impact-Z 13.8 (profile) | PETG Basic 1.25 g/cm³, Z-impact 10.5 kJ/m², HDT 68 °C, bending modulus 1950 MPa | — | [PLA Basic @base](https://raw.githubusercontent.com/bambulab/BambuStudio/master/resources/profiles/BBL/filament/Bambu%20PLA%20Basic%20%40base.json), [PETG Basic TDS](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf) |

- Reading: PLA is stiffer and has the best layer bond; PETG gives up ~40 % stiffness for ~70 % more impact toughness and 20 °C more heat margin; ASA is the tough/hot option but needs a warm chamber and a well-ventilated room. Bambu's own PETG Basic pitch is "PLA-level strength while maintaining its signature toughness", and it says annealing PETG Basic is not recommended ("prints with not very simple shape and structure may deform obviously"). [TDS V3.0](https://store.bblcdn.com/s1/default/cb94589bf7994fdcbfa833badefae9cd/Bambu_PETG_Basic_Technical_Data_Sheet.pdf). A walking biped that falls over is an impact problem more than a stiffness problem, which is why PETG (user's choice) is defensible for links and brackets; compensate the stiffness loss with 4–5 walls and ribs rather than solid infill.
- PA-CF / PETG-CF on the P1S: the P1S ships with a stainless nozzle and Bambu says "it is not recommended to directly print fiber-reinforced filaments … before an extruder and hotend upgrade is done"; Bambu's PETG guide lists PETG-CF as "Compatible with hardened steel nozzles". [bambulab.com/en/p1](https://bambulab.com/en/p1), [Bambu wiki: PETG usage guide](https://wiki.bambulab.com/en/filament/petg), [P1S extruder upgrade wiki](https://wiki.bambulab.com/en/p1/manual/p1s-extruder-upgrade). Treat CF as a later upgrade for the two or three most-stressed brackets, not the baseline.
- Feet: follow Open Duck — TPU sole at 40 % infill for grip and impact. [print_guide.md](https://github.com/apirrone/Open_Duck_Mini/blob/v2/docs/print_guide.md).

### 4.3 Mass budget per part (estimates — flag as such in the CAD/URDF)

Servos alone: 14 × 55 g = **770 g** (if the design copies Open Duck's 14 actuators). [Feetech datasheet](https://core-electronics.com.au/attachments/uploads/sts3215-smart-servo-datasheet-translated.pdf). Printed mass targets below are **my estimates** for a ~40 cm, ~30-part PETG build at 3–5 walls / 25–40 % gyroid (PETG 1.25 vs PLA 1.26 g/cm³, so the Open Duck PLA numbers carry over); replace them with Bambu Studio's sliced mass as parts are designed.

| Group | Parts | Est. mass each | Est. group mass |
|---|---|---|---|
| Foot (PETG shell + TPU sole) | 2 | 40–60 g | 80–120 g |
| Shin / thigh links (sheets + spacers) | 8–12 | 15–40 g | 200–350 g |
| Hip / knee servo clamshells & brackets | 6–8 | 15–30 g | 120–200 g |
| Trunk halves | 2 | 80–150 g | 160–300 g |
| Head shell + neck | 4–6 | 20–100 g | 150–250 g |
| Covers, antenna, lids | 4–6 | 5–20 g | 40–90 g |
| **Printed total** | ~30 | | **≈ 0.75–1.3 kg** |

Cross-check: Open Duck v2's 51-part set slices to 990 g PLA at Bambu defaults [soyeon24 build log](https://github.com/soyeon24/open-duck-mini-v2-build); stronger walls/infill add roughly 20–35 % (estimate), fewer parts subtract.

---

## 5. PETG quantity and cost for the build

- **Quantity:** ≈ 0.8–1.2 kg in the finished robot (§4.3) + supports/purge (~10–15 % on Bambu with tree supports) + at least one full reprint of legs/brackets during tuning → **buy 2.5–3 kg** for the first build (estimate).
- **Prices found (Sept 2026):**
  - Numakers PETG-HS (Indian brand, official store): **Rs 599 / 1 kg** (Rs 575 at 13–24 spools, Rs 549 at 25+); nozzle 240 ± 10 °C, bed 80–90 °C, stated max working temp 75 °C, "Dimensional Accuracy Tolerance: 0.15mm or more" as printed on the page. [india.numakers.com PETG-HS](https://india.numakers.com/products/petg-hs-filament). Numakers PETG-CF Rs 1,149 (MRP Rs 1,800); PETG Translucent Rs 599. [Numakers all products](https://india.numakers.com/collections/all). Numakers standard PETG: REES52 lists Rs 845 (sold out) and a price-tracker shows Rs 899 on Amazon.in **[unverified]**. [REES52](https://rees52.com/products/numaker-petg-filament-3d-printing-filament-1-75mm-filament-1kg-filament-numaker-filament-high-quality-petg-filament-for-3d-printing-pure-white-rs6761), [pricehistory.app](https://pricehistory.app/p/numakers-petg-3d-printer-filament-1-75mm-nOznClG5).
  - eSun PETG 1 kg: **Rs 1,289 + 18 % GST (MRP Rs 1,639)** at ElectronicsComp (out of stock when checked); Rs 1,499.99 on IndiaMART; Rs 2,025 (offer Rs 1,923) on Flipkart. [ElectronicsComp](https://www.electronicscomp.com/esun-petg-1.75mm-3d-printing-filament-1kg-solid-black), [IndiaMART](https://www.indiamart.com/proddetail/esun-petg-filament-1kg-2849488315612.html), [Flipkart](https://www.flipkart.com/esun-3d-petg-black-filament-1kg-2-2lb-1-75mm-solid-printer/p/itm557274389850f).
  - Bambu PETG Basic: **US$23 / 1 kg spool, US$20 refill** at relaunch (Mar 2026), US$14.94/12.99 at 10+ qty. [ToolGuyd](https://toolguyd.com/bambu-petg-basic-3d-printing-filaments-relaunch-2026/). Indian reseller price: robu.in (an authorised Bambu reseller) has a "PETG Basic Filaments" category but a site search for "bambu petg" returned **0 products** on 2026-09-26; WOL3D could not be checked. [robu.in Bambu PETG category](https://robu.in/product-category/bambu-lab-petg-filaments/), [Bambu authorised resellers, India](https://bambulab.com/en/dealer?region=India). **INR price unverified** — Open question #1.
- **Cost of 3 kg:** Numakers PETG-HS ≈ **Rs 1,800**; eSun ≈ **Rs 4,500–6,000**; Bambu ≈ **US$60–69 plus import/reseller margin** (unverified in INR). Even the expensive option is < 10 % of the Rs 50,000 cap; the 14 servos (€196 in the Open Duck BOM) dominate. [Open Duck BOM](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/edit?usp=sharing).
- **Recommendation:** prototype links and shells in Numakers PETG-HS (cheap, Indian, tolerates 240 °C profile); print the final servo brackets and bearing carriers in Bambu PETG Basic (first-party profile, published XY/Z data, lower moisture sensitivity claim) *if* an Indian reseller stocks it, otherwise in eSun PETG with a fully calibrated Generic PETG profile. Whichever spool: dry it, run flow-dynamics + flow-rate + shrinkage cube + M6 hole test, and save one Process profile per spool.

---

## 6. One-page checklist for every microduck part

1. Fits in 238 × 256 × 249 mm (stock), footprint +5 mm/side if brimmed; avoid the front-left 18 × 28 mm corner. [§1.1]
2. Bottom edges chamfered 0.3–0.5 mm × 45°; no fillets that start tangent to the bed. [§2.4, §3.5]
3. Walls in multiples of 0.42/0.45 mm; ≥ 1.3 mm for anything structural, ≥ 1.8 mm for brackets; ribs never < 0.9 mm. [§3.1]
4. Overhangs ≤ 45°, bridges ≤ 25 mm, horizontal holes teardropped. [§3.5]
5. Bending loads run along XY; split parts rather than accept a Z-stacked load path; gussets at every servo tab. [§3.7]
6. M3 heat-set inserts at ≈ 3.9–4.0 mm Ø in ≥ 7.8 mm bosses, ≥ 6.7 mm deep; M2 at 3.1–3.2 mm Ø in ≥ 6.2 mm bosses. [§3.2]
7. STS3215 pocket 45.5 × 25.0 mm with crush ribs and ventilation slots; screws cannot bottom on the servo case. [§3.3]
8. Bearing pockets axis-along-Z, 608 → 21.85–21.95 (press) / 22.05–22.10 (slip), MR115 → 10.90–10.95 / 11.05–11.10, 684 → 8.90–8.95 / 9.05–9.10, with 0.5 × 45° lead-in; metal inner shafts only. [§3.6]
9. No living hinges; snaps only on covers, strain ≤ 1–2 %, root fillet ≥ 0.5 t, not built in Z. [§3.4]
10. Slicer: 0.20 mm (0.12–0.16 for pockets), Precise wall on, Precise Z height on, elephant foot per plate (start 0.15 mm), XY hole comp from M6 test (expect ≈ +0.1–0.15 mm), shrinkage % from cube, 4–5 walls / 5 top / 5 bottom / 30–40 % gyroid for brackets, Bambu PETG Basic or a calibrated Generic PETG profile, dried filament, door closed, top glass off if chamber > 50 °C. [§2]

---

## Open questions (could not be verified)

1. **Bambu PETG Basic price and availability in India.** robu.in shows the category but no products; WOL3D was not reachable from this session; no official Bambu India store exists (store.bambulab.com/en-in redirects). Need a live quote.
2. **Total mass of a finished Open Duck Mini v2** is not published in the repo, BOM or vendor pages I could read; only the slicer estimate (990 g PLA + 34 g TPU for 51 parts) and 14 × 55 g servos are known.
3. **STS3215 mounting-tab hole diameter and spacing** — the datasheet's dimension drawing is an image; extract from Feetech's 2D DXF/STEP or measure the physical servo before modelling the bracket.
4. **M2.5 heat-set insert hole diameter** varies 3.4–3.8 mm across brands (ruthex RX-M2.5x5.7 spec not retrieved); pick one brand and print the coupon.
5. **P1S passive chamber temperature with door closed and top on during a multi-hour PETG print at 30–35 °C room temperature** — Bambu publishes none; must stay ≥ 10 °C below Tg (≤ ~59 °C) and ideally within the TDS's 35–50 °C.
6. **Actual linear shrinkage of the chosen spool** (Bambu gives no % for PETG); community P1S/X1C data show ≈ 0.3 % undersize on 100 mm.
7. **Servo case temperature during walking** vs PETG's 68 °C HDT — needs a thermocouple test on the assembled leg before trusting press-fits near the servo.
8. **Whether "Bambu PETG HF" is still sold** — one search summary said it is discontinued; not confirmed on a Bambu page. Irrelevant if PETG Basic is used.

---

## Critic additions (2026-09-26, from `07_critic_gaps.md`)

1. **Open question 3 (STS3215 mounting holes) is already answered in `03_sts3215.md` §1.3** from the Waveshare DXF: no side ears; 8 x O1.6 pilot holes (mouth O2.0) for PA2.0 self-tappers / M2x6, in pairs **20.5 mm apart across the width**, at **18.41 mm from the output end on both faces**, plus a rear pair at 2.36 mm (spline face) / 6.11 mm (idler face) from the rear end; output axis 10.11 mm from the gearbox end; raised D-boss O21.6-21.8 x 3 mm; spline OD 5.9 mm protruding 3.4 mm; idler O6 protruding 4.1 mm. Critic's measurement of the Open Duck reference meshes gives the case envelope as **45.22 x 24.72 x 35.70 mm** (three shells 9.70 / 13.90 / 14.10). The §3.3 pocket 45.5 x 25.0 mm stands; use 35.7 mm for the height stack and keep the O22 relief for the boss.
2. **§3.3 wording corrections:** 0.238 s/60 deg is the STS3215-C001's **6 V** no-load speed; at **7.4 V it is 0.192 s/60 deg (52 RPM)**. 19.5 kg.cm is the **stall** torque at 7.4 V; the **rated (continuous)** torque is 5 kg.cm (Feetech C001 datasheet, 03 §2.1).
3. **Bearing pockets (§3.6): the reference design uses 6804ZZ (20 x 32 x 7 mm), not 608/MR115/684.** Official BOM ASIN B0CXXSVFTV = Kozelo 6804ZZ ([amazon.fr](https://www.amazon.fr/dp/B0CXXSVFTV)); the CAD mesh `roll_bearing.stl` measures OD 32.00 / ID 20.00 / W 7.00 (critic). Apply the same offsets as §3.6: **6804 pocket press 31.85-31.95 mm, slip/retained 32.05-32.10 mm, depth 7.2 mm, 0.6 mm lip on ~O29 so the outer race seats on the lip; 0.5 x 45 deg lead-in.** The 20 mm inner race in Open Duck rides on a *printed* boss (no metal shaft that size in the BOM): model the boss at 19.90-19.95 mm (press) or 19.80-19.85 (slip + retained by a screw head), print it with its axis along Z, and calibrate with a coupon — this is the one place §3.6's "metal inner shafts only" rule is knowingly relaxed. 6804ZZ Indian availability is unverified (not at electronicscomp); if unobtainable, redesign the pivot around a 608 (8 x 22 x 7, Rs 27) with a metal M8 shoulder screw.
4. **Open question 1 (Bambu PETG Basic INR price) is answered in `06_electronics_bom_inr.md` §8** (same day): robu.in Bambu PETG Basic **refill Rs 699/kg in stock** (SKU R260052 / R260054), PETG HF spool Rs 1,299 in stock, Sunlu PETG Rs 739, eSun Rs 1,099-1,329 ex-GST. Re-check the robu links before ordering (the critic's robu fetches returned 403). Open question 8 (PETG HF still sold): listed at robu, so yes for now.
5. **§4.3 mass budget / §5 quantity:** the total sliced mass of the 51-part Open Duck set is 990 g PLA + 34 g TPU (already cited); the "maybe 500 g" in the Open Duck BOM (repeated in 06 §8) is stale — keep the 2.5-3 kg purchase.
6. **Foot sole material:** the user specified PETG, but the sim floor friction is 0.6 with DR 0.5-1.0 (05 §5.4) and PETG on glossy vitrified tile (the video's floor) will be below that. Budget a TPU sole (Open Duck: TPU 40 % infill) or a glued rubber sheet; PETG-only soles are a sim2real risk, not a print-settings problem.
