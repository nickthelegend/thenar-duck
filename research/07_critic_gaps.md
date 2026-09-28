# 07 — Completeness critic: gaps, contradictions, budget risks, open sim decisions

Reviewed on 2026-09-26: `01_video_analysis.md`, `02_open_duck_mini_v2.md`, `03_sts3215.md`, `04_printing_petg_p1s.md`, `05_sim_training_options.md`, `06_electronics_bom_inr.md`, plus `references/SPECS.md` and `references/SOURCES.md`. Every file was read in full (including the tails past the 25k-token read cap).

Verification I did myself (not copied from the files): re-downloaded the Open Duck Playground MJCF and the `mini_bdx` XML/URDF and summed their inertials; downloaded the official BOM CSV and resolved its bearing ASIN on amazon.fr; downloaded 30+ Open Duck reference meshes from the `v2` branch and measured bounding boxes, bearing OD/ID and horn dimensions with a binary-STL parser; fetched the JAX installation page, the SolidWorks-URDF-exporter releases page, an Adafruit BNO055 page and one Indian vendor search. The web-search budget was exhausted before this task started, so anything I could not reach by direct URL is marked **[unverified]** instead of guessed.

Where I resolved a gap, a `## Critic additions` section has been appended to the owning file. Items are numbered so other agents can reference them (G = CAD gap, C = contradiction, B = budget, S = sim decision).

---

## 0. The five things that must be fixed before CAD starts

| # | Issue | Correct answer | Files affected |
|---|---|---|---|
| C1 | Open Duck's bearing is quoted as 8 × 22 × 7 mm (608) from one builder's log | Official BOM ASIN B0CXXSVFTV = **6804ZZ, 20 × 32 × 7 mm**, pack of 2 ([amazon.fr](https://www.amazon.fr/dp/B0CXXSVFTV)); the CAD mesh `roll_bearing.stl` measures **OD 32.00 / ID 20.00 / W 7.00 mm** (my measurement of [the v2 mesh](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/mini_bdx/robots/open_duck_mini_v2/roll_bearing.stl)). 3 needed (2 hip-roll, 1 head-roll). | 02 (wrong), 04 (pocket tables cover 608/MR115/684 only), 06 (buys 684/685, no 6804) |
| C2 | Three different "Open Duck model mass" values: 2.107 kg (02), 2.045 kg (03), 2.06 kg (SPECS) | Playground `open_duck_mini_v2.xml` = **2.1071 kg** (15 inertials, slicer-overridden masses); `mini_bdx/.../robot.xml` and the reference-motion URDF = **2.0615 kg** (21 inertials, CAD masses). 02 and SPECS are both right for their file; **03's 2.045 kg matches neither** (torque-margin arithmetic there is off by ~3 %, conclusion unchanged). | 03 |
| C3 | 05 lists the 7.4 V STS3215 no-load speed as unverified and the servo-P ↔ MuJoCo-kp mapping as undocumented | Both are already in the other files: **0.192 s/60° = 52 RPM = 5.45 rad/s at 7.4 V, 0.238 s/60° = 4.40 rad/s at 6 V** (03, Feetech C001 datasheet); maintainer statement "**17.8 in mujoco corresponds to 32 in the motors firmware units**" (02, [issue #20](https://github.com/apirrone/Open_Duck_Mini/issues/20)). | 05, and 04 §3.3 which mis-attributes 0.238 s/60° to 7.4 V |
| G1 | No file states the microduck's own target dimensions | Decision needed (see §1.1). My recommendation: **Open Duck Mini v2 kinematics unchanged** (78.65/78.65 mm links, 70 mm hip-yaw spacing, 218 mm hip-pitch spacing, 38.8 mm ankle-to-sole, 102 × 41 mm sole) with the **video's styling scaled by 0.525** (0.42 m / 0.80 m). Scaled styling table appended to 01. | 01, 02 |
| B1 | The "Recommended" BOM is ₹47,723 with **zero spare servos, no tools, no 6804 bearings, no TPU, no gamepad**; adding only tools puts it at ₹50,302 | Realistic all-in for the minimum-viable robot is **₹45–48 k** if the 18650 pack route is used instead of LiPo + charger; **₹51–53 k** with 2 spare servos. See §3. | 06 |

---

## 1. (a) Numbers a CAD engineer still needs

### 1.1 Not in any file — needs a decision, not a search

| ID | Missing number | Why it matters | Where it should live | Proposed value / how to get it |
|---|---|---|---|---|
| G1 | **Target overall height, link lengths, hip width, stance, foot size of the microduck** | Everything else scales from it. 01 gives a 0.8 m robot; 02 gives a 0.42 m robot; nothing says which the microduck is. | `SPECS.md` (new §6 "Microduck master skeleton") | Keep Open Duck v2 geometry (proven to walk on 14 × STS3215; the RL/placo pipeline, BAM actuator model and pretrained ONNX all assume it). Style with the video at scale 0.525 (table appended to 01). Only the *shells* change: head 158 W × 68 H (video-scaled) vs Open Duck's 200 × 59; torso 110 W × 158 H × 142 D vs Open Duck's 110 × 143 × 200. |
| G2 | **Thigh : shank ratio** | 01 measures 1.5 : 1 on the video; Open Duck is 1 : 1 (78.65/78.65); Disney/BDX-R is 0.8 : 1 (111/138, SPECS §2). Three different answers. | `SPECS.md` §6 | Keep 1 : 1 for phase 1. Changing it invalidates the placo presets, the 240 reference motions and the BAM-free "kp = 17.8" transfer — it is a phase-2 experiment. |
| G3 | **Ankle axis to ground** | 02 says 36.2 mm (to the foot *site*); SPECS says 38.8 mm (mesh sole bottom). | 02 §4.2 | Use **38.8 mm** (sole bottom); the MJCF site sits ~2.6 mm inside the 8 mm TPU sole. |
| G4 | **Servo orientation per joint** (which face carries the horn, where the idler disc/bearing goes, screw side) | Onshape is login-gated; 02 only has STL bounding boxes. | 02 §4 | Download the 36 `print/*.stl` **and** the `mini_bdx/robots/open_duck_mini_v2/*.stl` reference meshes (servo case halves, `drive_palonier`, `passive_palonier`, `roll_bearing`, boards) and place them in SolidWorks using the MJCF body `pos`/`quat` values from 02 §4.2 — this rebuilds the assembly without Onshape. Mesh dimensions appended to 02. |
| G5 | **Exact screw counts and lengths** | Open Duck docs say "TODO"; 06 budgets a guessed screw set. | 02 §5.3 / 06 §7 | Count from the rebuilt assembly (G4); budget ±₹300. |
| G6 | **STS3215 connector socket position and plug clearance** | 03 §1.5 could not resolve from drawings. | 03 §1.5 | Needs the Waveshare STEP ([ST3215-3D.zip](https://files.waveshare.com/upload/5/59/ST3215-3D.zip)) opened in SolidWorks, or one physical unit. Buy **2 servos first** (also needed for S2). |
| G7 | **Which Feetech horn ships with the Evelta C001** | 03 has the Waveshare disc (Ø19.2, Ø14 bolt cross); Open Duck's CAD models a **Ø19.95 × 5.05 mm drive disc (Ø3.2 centre) and Ø19.95 × 3.10 mm passive disc (Ø6.1 bore)** (my mesh measurement). | 03 §1.4 | Treat as Ø20 disc, 4 × M3 on a Ø14 cross, confirm on the first 2 units. |

### 1.2 Resolved by me (appended to the owning file)

| ID | Number | Value | Source | Appended to |
|---|---|---|---|---|
| G8 | STS3215 body envelope as modelled by Open Duck | **45.22 × 24.72 × 35.70 mm** (union of the three case meshes: top cabinet 9.70, middle 13.90, bottom 14.10 mm thick) | my measurement of `wj-wk00-012[2-4]*.stl` | 03, 04 |
| G9 | Horn discs | drive Ø19.95 × 5.05, passive Ø19.95 × 3.10 (bore 6.1) | `drive_palonier.stl`, `passive_palonier.stl` | 03 |
| G10 | Bearing | 6804ZZ 20 × 32 × 7, ×3 | BOM CSV row 27 + amazon.fr + mesh | 02, 04, 06 |
| G11 | Electronics envelopes for packaging | Pi Zero 2 W 65.9 × 31.25 (board mesh); Waveshare adapter 42.02 × 33.02 × 1.6; BNO055 generic 20 × 27 × 3 (mesh) / Adafruit **20 × 27 × 4 mm, 3 g** ([Adafruit 2472](https://www.adafruit.com/product/2472)); 18650 cell Ø18 × 65; 2-cell holder 76 × 41 × 20; USB-C charger 38.2 × 18.1 × 5.15; BMS 40.6 × 15.85 × 3.6; power switch 23.4 × 7.4 × 16.8; SG90 32.6 × 13 × 31 | Open Duck reference meshes (my measurement) | 02 |
| G12 | Open Duck bracket meshes | knee_to_ankle sheets 30.70 × 8.45/7.20 × 70.65; leg_spacer 28.07 × 36.90 × 10.00; head_pitch_to_yaw 31.99 × 44.90 × 72.00; head_yaw_to_roll 87.95 × 79.98 × 42.20; head_roll_mount 40.00 × 64.74 × 15.10; roll_motor_bottom 32.00 × 30.74 × 31.41; roll_motor_top 38.00 × 28.72 × 20.01; body_middle_top 150 × 110 × 56.78; battery_pack_lid 7.5 × 51.4 × 86.4 | same | 02 |
| G13 | STS3215 mounting holes | already fully in 03 §1.3 (8 × Ø1.6, 20.5 mm across, 18.41 mm from output end both faces; rear pair 2.36 / 6.11 mm); 04's open question #3 is stale | 03 | 04 |
| G14 | Video styling at microduck scale | table at ×0.525 | derived from 01 §10 | 01 |

### 1.3 Still unverified (say so; do not guess in CAD)

| ID | Number | Status |
|---|---|---|
| G15 | **Raspberry Pi 3 A+ outline / hole pattern** (the in-stock compute board 06 recommends; it is 65 × 56 mm class, much larger than the Zero 2 W the Open Duck head is designed around) | Official drawing at [pip-assets.raspberrypi.com … RP-008330-DS-1-raspberry-pi-3-a-plus-mechanical-drawing.pdf](https://pip-assets.raspberrypi.com/categories/512-raspberry-pi-3-model-a/documents/RP-008330-DS-1-raspberry-pi-3-a-plus-mechanical-drawing.pdf) — fetched, but it is a vector drawing with no extractable text and no PDF renderer is installed here. **Open it in a viewer and read off outline + hole grid before designing the head tray.** |
| G16 | 2S 2200 mAh 45C LiPo pack dimensions | robu.in returns 403; not in 06 either. Needed for the trunk/battery bay. |
| G17 | Omron SS-10 switch dimensions | Omron pages 403'd. Needed for the foot switch pocket. |
| G18 | Molex 5264 pitch | Molex page timed out twice. 03 says "2.54 mm", 06 says "2.5 mm"; Molex's 5264 SPOX family is nominally **2.50 mm** — treat as 2.50 mm pitch **[unverified here]**; JST-XH/Relimate 2.50 mm housings are the common substitute but need a fit test (06). |
| G19 | 6804ZZ availability in India | not at electronicscomp ([search](https://www.electronicscomp.com/index.php?route=product/search&search=6804): "no product matches"); robu.in unreachable; IndiaMART/amazon.in unverified. If unobtainable, redesign the hip-roll pivot around a 608 (8 × 22 × 7) or 6805 — but that is a CAD change, not a drop-in. |
| G20 | SolidWorks version vs the URDF exporter | latest [sw2urdf release v1.6.1](https://github.com/ros/solidworks_urdf_exporter/releases) states "SolidWorks 2021"; v1.6.0 "SolidWorks 2020". The user's SolidWorks version is unknown. Fallback that reproduces the Open Duck pipeline exactly: export STEP → free Onshape document → `onshape-to-robot` → MJCF (02 §6.1). |

---

## 2. (b) Contradictions and wrong-looking claims

| ID | Claim A | Claim B | Verdict / fix |
|---|---|---|---|
| C1 | 02 §5.3, 02 §3 table: bearing 8 × 22 × 7 mm "UNVERIFIED vs CAD" | BOM ASIN + CAD mesh | **6804ZZ 20 × 32 × 7**. Fixed in 02, 04, 06 additions. |
| C2 | 02: model mass 2.107 kg; SPECS: 2.06 kg | 03: 2.045 kg | 2.107 (Playground MJCF) and 2.0615 (mini_bdx XML/URDF) are both correct; 03's 2.045 is a mis-sum. Fixed in 03 addition. |
| C3 | 05 §5.1 / open Q1: 7.4 V no-load speed unverified | 03 §2.1: 52 RPM / 0.192 s/60° @ 7.4 V from the C001 datasheet | 05 is stale → `max_motor_velocity` = **5.45 rad/s datasheet, 5.1–5.3 BAM, 2.7 measured by 2026 builders** (issue #48). Fixed in 05 addition. |
| C4 | 05 open Q5: kp ↔ P-register mapping undocumented | 02 §2.5: maintainer "17.8 in mujoco ↔ 32 firmware" (issue #20) | Documented but not derived: 17.8 N·m/rad ↔ P = 32 → **~0.556 N·m/rad per P unit** (my arithmetic; treat as a starting point, still re-identify). Fixed in 05 addition. |
| C5 | 04 §3.3: "no-load 0.238 s/60° @ 7.4 V", "rated 19.5 kg·cm @ 7.4 V" | 03: 0.238 s/60° is the **6 V** figure; 19.5 kg·cm is **stall**, rated is 5 kg·cm | 04 wording wrong. Fixed in 04 addition. |
| C6 | 04 open Q3: STS3215 mounting-hole pattern not extractable | 03 §1.3 has it from the Waveshare DXF | Stale open question. Fixed in 04 addition. |
| C7 | 04 open Q1: Bambu PETG Basic INR price unverified, robu shows 0 products | 06 §8: robu.in PETG Basic refill **₹699/kg in stock** (SKU R260052/R260054), PETG HF ₹1,299 | Same day, same vendor. Trust 06 (it cites SKUs), but re-check the link before ordering. Fixed in 04 addition. |
| C8 | 06 §7: "STS3215 horn screws are M2 (ship with servo)" | 03 §1.2/1.4: horn centre screw **M3 × 6**, disc holes M3; body pilot holes are PA2.0 / M2 × 6 | 06 wrong; the M2 screws are the *body* screws. Fixed in 06 addition. |
| C9 | 06 §7: "PETG softens ~80 °C" | 04: Bambu PETG Basic **Tg 69 °C, HDT 68 °C** | 06 is generic-PETG folklore; use 04's TDS numbers. Fixed in 06 addition. |
| C10 | 06 §6: foot switches "optional — the policy can run without contact sensing" | 02 §6.3 / 05: the 101-dim observation includes **2 foot-contact bits** | Dropping them means retraining with a 99-dim obs or feeding constant zeros (distribution shift). Not optional for the pretrained policy. Fixed in 06 addition. |
| C11 | 06 §4: recommends BNO085 | 02/05: runtime is `adafruit_bno055`, obs uses raw gyro + accel | BNO085 works electrically but needs a new driver (`adafruit_bno08x`) and re-checking axis conventions; budget the software time or stay on BNO055 for phase 1. Noted in 06 addition. |
| C12 | 06 §10.2 open item: antenna servos as STS3215 (+₹4,318) or PWM 9 g servos | 01 §4: the reference robot has **no antennae** (static black ear pods instead) | Antennas are not part of this build → 14 servos, no SG90s, the "all STS3215" rule is satisfied for free. Noted in 06 addition. |
| C13 | 02 §8 pins: `playground==0.0.5 + jax[cuda12]==0.8.0` (issue #25) | 05 §3.3 pins: `jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5` (soyeon24 3090 run) | Both plausible; neither is a lockfile. JAX still ships CUDA-12 wheels for driver ≥ 525 ([JAX install page](https://docs.jax.dev/en/latest/installation.html): "at some point in the future we will drop CUDA 12 support"). See S4. |
| C14 | 02 §8: `XLA_PYTHON_CLIENT_MEM_FRACTION=0.6`, num_envs 2048–4096 | 05 §3.3: 0.85, try 8192 then 4096 | Both are guesses for a 6 GB GPU. Run the 2 M-step smoke test at 8192 → 4096 → 2048 and record VRAM (S5). |
| C15 | 05 §5.1: sim rate-limits targets at 5.24 rad/s | 02 §6.5: the 5.24 rad/s clip is **commented out on the real robot** | Real robot's limit is the physical servo (2.7–5.4 rad/s depending on S2). This is a genuine sim2real gap: keep the limiter in sim and set it to the *measured* speed. |
| C16 | 02 §8 "86 mm roll-to-pitch bracket" | 02 §4.2 hip_roll → hip_pitch axis-to-axis **82.0 mm** (74.15 outboard, 35.1 rearward) | 86.07 mm is the part's bounding box; 82.0 is the axis distance. Use 82.0 for kinematics. |
| C17 | 03 §0 TL;DR "2.3–4× stall margin" | 03 §5.1 table: 2.1–2.7× (C001), 3.3–4.2× (C018) | TL;DR rounding; the table is the number to use. |
| C18 | 03 §4.1: robu.in "Waveshare ST3215 (30 kg·cm) ₹2,097" | 06 §1.1: robu.in 12 V 30 kg ₹2,599; 7.4 V ₹2,159 (SKU R258500) | 03's ₹2,097 came from a search snippet with a 403'd page; 06 read listings. Trust 06, but SKU R258500's gear ratio/voltage is still **unverified** (robu 403 again today). |
| C19 | 01 §1: Disney BDX height "not published" | SPECS §1: **660 mm** from Grandia et al., RSS 2024 (arXiv 2501.05204) | SPECS is right; noted in 01 addition. |
| C20 | 01 open Q7: PETG on P1S unconfirmed | 04 §1.1: Bambu P1S spec sheet lists PETG as "Ideal" | Resolved; noted in 01 addition. |
| C21 | 03 §3: Waveshare adapter input 9–12.6 V | 06 §2: Waveshare docs "actually 5–8.4 V can also be input" | Not contradictory (spec vs note); 06 resolves the 2S question. |
| C22 | 06 §8: "duck body is ~500 g of plastic (Open Duck BOM)" | 02/04: builder re-slice **990 g PLA + 34 g TPU** | 500 g is the BOM's stale guess; budget 3 kg as 06 already does. |
| C23 | 04 §3.6 bearing scope "608, MR115, 684" | Open Duck uses 6804; 06 stocks 684ZZ/685ZZ | Neither 04 nor 06 covers the bearing the reference design actually uses. Fixed in both additions. |

Nothing in 01 (video) contradicts the other files on kinematics; its absolute sizes remain ±15–33 % (tile-size assumption), which is fine because G1 recommends not using them for the mechanics.

---

## 3. (c) Budget risks vs ₹50,000

Base: 06's Minimum-viable ₹41,787 (Pi Zero 2 W, OOS) / ₹42,919 (Pi 3 A+) and Recommended ₹47,723. I re-added both tables and they sum correctly.

| ID | Risk | ₹ impact | Mitigation |
|---|---|---|---|
| B1 | **No spare servos.** 14 servos, PETG brackets, first biped, head-servo breakage during offset calibration is a documented failure (02 §7 #5) | +₹4,318 for 2 | Buy 16 if budget allows; otherwise buy 14 and keep ₹2.2 k reserved. |
| B2 | **Tools not in the totals** (LiPo charger ₹2,079, insert tip ~₹500 est., 12 V PSU ₹425) | +₹2.6–3.0 k → Recommended becomes ₹50.3 k | Take the **18650 route** (holder ₹59 + 2S 20 A BMS ₹149 + USB-C 2S charger ₹329 = ₹537, cells 2 × ~₹300–540 **[cell price unverified, OOS at robu]**) — no balance charger needed, and it is what Open Duck does. Saves ≈ ₹2.5–3 k vs LiPo + iMAX. |
| B3 | **6804ZZ × 3 missing from every BOM** | +₹300–600 **[price unverified in India]**; possibly unobtainable (G19) | Source before CAD freeze; fallback redesign to 608. |
| B4 | **Servo unit-price drift / variant risk**: ₹2,159 (robu, SKU variant unverified) vs ₹2,224 (Evelta, C001 confirmed) | ±₹300/unit = ±₹4.2 k on 14 | Buy 2 from Evelta first (C001 confirmed, 24 h dispatch), measure speed (S2), then buy 12 more from the same vendor in one order. |
| B5 | Pi Zero 2 W OOS everywhere → Pi 3 A+ | +₹1,132; **plus a larger head tray** (G15) | Accept; set restock alerts. |
| B6 | Gamepad not budgeted (Open Duck runtime expects an Xbox controller over Bluetooth, 02 §6.5) | ₹0 with SSH keyboard teleop (the video robot is keyboard-tethered anyway) to ₹1.5–4 k **[unverified]** for a BT gamepad | Phase 1: keyboard over SSH/Wi-Fi. |
| B7 | TPU sole not budgeted (user said PETG; Open Duck uses TPU 40 % for grip) | +₹1,000–1,500 **[unverified]** | PETG soles on tile will slip (sim floor friction 0.6, DR 0.5–1.0); budget one TPU spool or a rubber sheet. |
| B8 | Robotics-shop markup on microSD (₹1,629) and screws (₹12–15 each) | −₹1.5–2 k if bought at amazon.in / hardware store **[unverified]** | Easy saving. |
| B9 | Shipping ₹60–150/order × 3–4 vendors, unverified | +₹300–600 | Consolidate to Evelta + robu. |
| B10 | Import duty 40.39 % (06) — any AliExpress/Seeed order lands at ₹2.4–3.35 k/servo | none if avoided | Do not import. |
| B11 | Camera (+₹3,249) or Pi 5 (+₹8–11 k) blow the cap | over | Out of scope for phase 1. |

**Net realistic totals (my arithmetic on 06's line items):** minimum-viable with Pi 3 A+, 18650 pack, 6804 bearings, insert tip, TPU: **≈ ₹45.5–47 k**; the same + 2 spare servos: **≈ ₹50–51.5 k** (over). The build is feasible under ₹50 k only with **exactly 14 servos, 18650 power, no camera, no Pi 5, local (not imported) servos** — every one of those is already the reference design's choice.

---

## 4. (d) Sim-stack decisions still open

| ID | Decision | Options and evidence | Recommendation |
|---|---|---|---|
| S1 | **Bus voltage / variant: C001 7.4 V on 2S vs C018 12 V on 3S** — 03 recommends C018 @ 3S; 06 prices 7.4 V; 02 leans C001 for pipeline reuse; 05 leaves it open | C001: BAM parameters exist (m1–m6), pretrained ONNX exists, over-voltage register trips > 7.4 V yet hundreds of ducks run 8.4 V (02 §2.2); C018: +₹2.8–4.2 k, 3S pack, full re-identification, published policy does not transfer (02 §7 #3) | **C001 @ 2S for phase 1** (only path with an existing actuator model); read register 14 on arrival; retrain with `forcerange ±1.9` (S3). Revisit C018 in phase 2 if knees overheat. |
| S2 | **Real STS3215 speed: 2.7 rad/s (issue #48, 2026 builders) vs 5.1–5.3 rad/s (BAM) vs 5.45 (datasheet)** | unresolved upstream | **Measure on the first 2 units at 7.4 V and 8.4 V before buying 12 more**, then set `max_motor_velocity` to the measured value and keep the sim rate limiter (C15). |
| S3 | `forcerange` ±3.23 N·m (Open Duck) vs ±1.9 N·m (7.4 V stall) | soyeon24: retraining at ±1.86 doubled real-limit walking speed (02 §2.4) | Retrain at **±1.9 N·m** (C001) — do not reuse the stock XML unchanged. |
| S4 | Dependency pins: `jax 0.6.2 / mujoco 3.3.4 / playground 0.0.5` (05) vs `jax[cuda12] 0.8.0 / playground 0.0.5` (02) | no lockfile upstream; CUDA-12 wheels still published, driver ≥ 525 OK ([JAX](https://docs.jax.dev/en/latest/installation.html)) | Start with the **soyeon24 triple** (the only one with a documented full 300 M-step training run); fall back to 0.8.0 if the `_src.collision` import fails (issue #25). Pin in a `uv.lock`. |
| S5 | `num_envs` and VRAM on 6 GB | unmeasured; smallest confirmed GPU 8 GB laptop 4060 (02 §6.4); 3050 throughput 9–14 k steps/s is an extrapolation (05 §2.4) | 2 M-step smoke test at 8192 → 4096 → 2048; `XLA_PYTHON_CLIENT_MEM_FRACTION=0.6–0.85`; run the TF ONNX exporter on CPU. |
| S6 | Geometry source of truth: reuse Open Duck MJCF vs export from SolidWorks | new geometry ⇒ new placo config + 240 reference motions + retrain; SW2URDF supports up to SolidWorks 2021 officially (G20) | Phase 1: **Open Duck MJCF with masses/inertias replaced** by SolidWorks PETG values (`sim2real.md` overrides masses with slicer values anyway). Phase 2: SolidWorks → STEP → Onshape → onshape-to-robot. |
| S7 | Isaac / ROS (the user asked for "ros or even isaac") | Isaac Sim needs ≥ 8 GB (4.5) / 16 GB (5.x, 6.0) and driver 580.88; WSL2 unsupported (05 §1.1). ROS 2 not used by the Open Duck runtime; Pi Zero/3 A+ cannot host it sensibly (05 §4) | **Isaac: no. ROS 2 Jazzy: optional, WSL2-only, for RViz/logging** — tell the user explicitly. |
| S8 | Windows NVIDIA driver 546.18 → ≥ 580.88 | not required for `jax[cuda12]`; removes ptxas warning; needed for cuda13 wheels (05 §3.1) | Update once, before the first run (OEM driver availability for this laptop SKU unverified). |
| S9 | Backlash model ±0.5° (Open Duck) vs measured 0.62–1.30° | Robonine (02 §2.3) | Widen to ±0.9° and randomise 0.3–1.0° (05 §5.4). |
| S10 | Foot-contact bits in the observation (C10) | keep = need 2 × SS-10 + GPIO; drop = retrain at 99 dims | Keep (₹197 × 4 budgeted). |
| S11 | IMU driver (C11) | BNO055 (runtime as-is) vs BNO085 (new driver) | BNO055 for phase 1. |
| S12 | Compute board Python: Pi OS Bookworm **Python 3.11** required (`onnxruntime==1.18.1` breaks on 3.13, 02 §6.5) | applies equally to Pi 3 A+ | Use the v0.2.3 `duck.iso` image or `uv python install 3.11`. |
| S13 | WSL2 distro | only `docker-desktop` exists today | `wsl --install -d Ubuntu-24.04`, ~10 GB disk (05 §3.2–3.4). |

---

## 5. Where each fix now lives

- `01_video_analysis.md` → Critic additions: BDX official height, PETG/P1S resolved, **video-to-microduck scaled styling table**, thigh:shank note.
- `02_open_duck_mini_v2.md` → Critic additions: **bearing = 6804ZZ**, mass 2.107 vs 2.0615 explained, ankle-to-sole 38.8, reference-mesh dimension table (servo case, horns, boards, cells, brackets), 82 vs 86 mm note.
- `03_sts3215.md` → Critic additions: mass correction (2.045 → 2.107/2.0615), horn disc as modelled by Open Duck, connector pitch note, pointer to the kp mapping.
- `04_printing_petg_p1s.md` → Critic additions: mounting holes (stale Q3), 0.238 s/60° mis-attribution, **6804 pocket sizes**, servo pocket from the CAD envelope, Bambu PETG price (stale Q1).
- `05_sim_training_options.md` → Critic additions: 7.4 V speed (stale Q1), kp mapping (stale Q5), rate-limiter sim/real mismatch, pin-set decision, forcerange, contact bits.
- `06_electronics_bom_inr.md` → Critic additions: 6804 bearings, horn screw M3, PETG Tg, antennas not needed, 18650 vs LiPo lever, foot switches not optional, BNO085 driver cost, gamepad, spares, revised realistic total.

---

## 6. Sources used by the critic (beyond those already cited in 01–06)

- Open Duck Playground MJCF (mass sum 2.1071 kg): https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml
- Open Duck `mini_bdx` MJCF and URDF (mass sum 2.0615 kg): https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/mini_bdx/robots/open_duck_mini_v2/robot.xml , https://raw.githubusercontent.com/apirrone/Open_Duck_reference_motion_generator/main/open_duck_reference_motion_generator/robots/open_duck_mini_v2/open_duck_mini_v2.urdf
- Open Duck reference meshes (directory listed via `gh api repos/apirrone/Open_Duck_Mini/contents/mini_bdx/robots/open_duck_mini_v2?ref=v2`): https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/mini_bdx/robots/open_duck_mini_v2/{roll_bearing,drive_palonier,passive_palonier,wj-wk00-0122topcabinetcase_95,wj-wk00-0123middlecase_56,wj-wk00-0124bottomcase_45,bno055,board,cell,holder,bms,usb_c_charger,power_switch,raspberrypizerow,sg90,left_knee_to_ankle_left_sheet,left_knee_to_ankle_right_sheet,leg_spacer,head_pitch_to_yaw,head_yaw_to_roll,head_roll_mount,roll_motor_bottom,roll_motor_top,left_roll_to_pitch,neck_left_sheet,foot_top,foot_side,foot_bottom_tpu,head,trunk_top,trunk_bottom,body_middle_top,battery_pack_lid}.stl
- Open Duck BOM CSV (bearing row: `Bearing, https://www.amazon.fr/dp/B0CXXSVFTV, qty 3, €3.5`): https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/export?format=csv
- Bearing ASIN: https://www.amazon.fr/dp/B0CXXSVFTV (Kozelo 2 pcs 6804ZZ 20 × 32 × 7 mm); same ASIN on amazon.com resolves to the same product
- seanmayer build log (source of the 8 × 22 × 7 claim; a builder substitution, not the BOM): https://raw.githubusercontent.com/seanmayer/open-duck-mini-build/main/README.md
- JAX installation page (CUDA 12 vs 13, WSL2 "experimental"): https://docs.jax.dev/en/latest/installation.html
- SolidWorks URDF exporter releases (v1.6.1 "SolidWorks 2021"): https://github.com/ros/solidworks_urdf_exporter/releases
- Adafruit BNO055 breakout dimensions: https://www.adafruit.com/product/2472
- Raspberry Pi 3 A+ mechanical drawing (fetched, not machine-readable here): https://pip-assets.raspberrypi.com/categories/512-raspberry-pi-3-model-a/documents/RP-008330-DS-1-raspberry-pi-3-a-plus-mechanical-drawing.pdf
- electronicscomp 6804 search (no listing): https://www.electronicscomp.com/index.php?route=product/search&search=6804
- Not reachable this session (403/timeout): robu.in product pages, Omron SS-10 pages, Molex 5264 datasheet.
