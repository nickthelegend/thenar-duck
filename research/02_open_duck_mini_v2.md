# 02 — Open Duck Mini v2 (apirrone) deep dive

Research date: 2026-09-26. Scope: apirrone/Open_Duck_Mini (v2 branch), Open_Duck_Mini_Runtime, Open_Duck_Playground, Open_Duck_reference_motion_generator, Rhoban BAM, official BOM sheet, GitHub issues, community build logs, and the 2026 commercial successor (Pollen/Hugging Face "Microduck").

Every number below is either (a) read directly from a raw repo file (URL given), (b) computed by me from those files (marked **computed**), or (c) quoted from a third-party page (URL given). Things I could not verify are marked **UNVERIFIED**. Discord and Onshape content could not be fetched (login-gated); everything attributed to Discord is second-hand via GitHub issues.

---

## 0. TL;DR for the "microduck" project (decision-relevant)

| Topic | Finding |
|---|---|
| Servos | **14× Feetech STS3215, 7.4 V "19 kg.cm" version** (Alibaba link in BOM), all 14 are the same model; 10 in legs (5/leg), 4 in neck/head. Two extra 9 g SG90 hobby servos drive the antennas (not on the bus). [BOM sheet](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc) |
| Servo variant trap | The BOM text "7.4v ones, also called 19kg.cm" maps to retail **STS3215-C001 (1:345)**. In June 2026 builders measured this variant tops out ≈2.7 rad/s while the policy assumes 5.24 rad/s max (BAM-identified) — [issue #48](https://github.com/apirrone/Open_Duck_Mini/issues/48). In March 2025 a core contributor said apirrone's sim2real duck used **Waveshare ST3215-HS (106 RPM)** — [issue #5](https://github.com/apirrone/Open_Duck_Mini/issues/5). **Unresolved** — see §2.4. |
| Bus voltage | 2S 18650 (7.4 V nominal, 8.4 V full) straight to the servo bus through a Waveshare Bus Servo Adapter (A); 5 V UBEC only for the Pi. |
| Compute | Raspberry Pi Zero 2W in the head, ONNX policy at **50 Hz**, servo bus at **1 Mbps** via `rustypot` (Rust) |
| IMU | BNO055 (I2C), raw gyro + accelerometer only (NDOF mode) |
| Size / mass | "about 42 cm tall with legs extended"; MJCF model mass **2.107 kg (computed)**; thigh = shin = **78.65 mm** axis-to-axis |
| Prints | 36 unique STLs, 51 printed parts, PLA 15 % infill + TPU foot soles 40 %; largest part head.stl ≈ **200 × 197 × 59 mm** → fits a P1S (256 mm) without splitting **(computed from STLs)** |
| Training | MuJoCo Playground / MJX + Brax PPO, 8192 envs, 300 M steps ≈ **1 h 11 min on an RTX 3090** (community), obs = 101, act = 14, imitation reward from Placo reference gaits |
| Successor | **No "Open Duck Mini v3" exists.** The 2026 successor is Pollen Robotics / Hugging Face **Microduck** ($399, 25 cm, 15 motors, Dynamixel XL330-class actuators, hardware NOT open). Open Duck Mini v2 repo still the only open-hardware duck. |

---

## 1. Project identity, versions, lineage

### 1.1 Repos and status (all Apache-2.0)

| Repo | Purpose | Status (from GitHub API on 2026-09-26) |
|---|---|---|
| [apirrone/Open_Duck_Mini](https://github.com/apirrone/Open_Duck_Mini) | Hub: CAD link, BOM, print/assembly docs, STLs, pretrained ONNX policies | 4,154 stars, 537 forks, default branch `v2`, last push 2026-01-31; branches `v1`, `v2`; no releases |
| [apirrone/Open_Duck_Mini_Runtime](https://github.com/apirrone/Open_Duck_Mini_Runtime) | On-robot code (Pi Zero 2W) | branches include `v2`, `main`, `mjlab_test`, `new_mjlab_test`, `new_firmware`, `improve_walk`, `awd_walk`, `basic_autonomy`, … |
| [apirrone/Open_Duck_Playground](https://github.com/apirrone/Open_Duck_Playground) | MJX RL training (MuJoCo Playground based) | 191 stars, 92 forks, last push 2025-08-11 |
| [apirrone/Open_Duck_reference_motion_generator](https://github.com/apirrone/Open_Duck_reference_motion_generator) | Placo-based parametric walk → reference motions for imitation reward | — |
| [Rhoban/bam](https://github.com/Rhoban/bam) | Actuator identification ("Better Actuator Models"); STS3215 7.4 V params live here | params at `bam/params/feetech_sts3215_7_4V/m1..m6.json` |
| [SteveNguyen/openduckminiv2_playground](https://github.com/SteveNguyen/openduckminiv2_playground) | Earlier/parallel MJX experiment (39 stars) | referenced by the ref-motion README |
| [rimim/AWD](https://github.com/rimim/AWD) | Isaac Gym AMP/ASE training for `mini_bdx` and `go_bdx` (v1-era pipeline) | referenced by the ref-motion README |

Community links: Discord https://discord.gg/UtJZsgfQGe (README), Tnkr build guide https://tnkr.ai/explore/docs/open-duck-mini/open-duck-mini-v2 (returned HTTP 403 to my fetches), Chinese BOM/guide on Feishu (README). Onshape CAD: https://cad.onshape.com/documents/64074dfcfa379b37d8a47762/w/3650ab4221e215a4f65eb7fe/e/0505c262d882183a25049d05 (public, not fetchable without login; MJCF header confirms `document_id: 64074dfcfa379b37d8a47762`).

Credits (`thanks.md`): Mimir Reynisson, Grégoire Passault, Augustin Crampette, Michel Aractingi, Mankaran Singh, Steve N'Guyen, Pierre Rouanet, Thomas Wolf. README: "Thanks a lot to HuggingFace and Pollen Robotics for sponsoring this project!" [README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/README.md)

### 1.2 Version history

- **v1 (2024)**: ~35 cm tall, Dynamixel XL330-M288-T then XC330-M288-T legs, U2D2 power hub, trained in Isaac Gym with AWD; "has some mechanical problems (too much play at some joints)"; v2 announced as "cheaper (aiming for ~$500), better designed, easier to build and more capable" — [v1 README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v1/README.md).
- **v2 (Jan 2025 →)**: "We are making a miniature version of the BDX Droid by Disney. It is about 42 centimeters tall with its legs extended. The full BOM cost should be under $400!" Timeline from README updates: 22/01/2025 mechanical design "pretty much finalized"; 07/02/2025 "design and BOM should not change drastically"; 24/02 and 07/02/2025 sim2real progress; 15/03/2025 Discord opened; two pretrained policies `BEST_WALK_ONNX.onnx` / `BEST_WALK_ONNX_2.onnx` (884,177 bytes each) — [README](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/README.md). Hackaday coverage 2025-04-05: "a little over 40 cm tall", "around 400 USD", Pi Zero 2W, BNO055 — [hackaday](https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/).
- **"v2.5" plans (Oct 2025, not released)**: maintainer TODO [issue #33](https://github.com/apirrone/Open_Duck_Mini/issues/33): "Fix neck part that breaks often", "Source new BMS (too many issues with the current one, and it's hard to get in certain parts of the world)", "12V motors ? -> update battery system (bms)", "retrain walk policy for these motors", "UART com instead of USB", "Provide PI hat files", "Complete screws information in the docs", "As little screws as possible, same screw everywhere", "Update official head", "Provide ISO", "Don't pull too much current on the rpi with the LEDs".
- **No v3.** Searches for "Open Duck Mini v3" return nothing; repo has no v3 branch; last push Jan 2026.
- **Microduck (Aug 27 2026, Pollen Robotics + Hugging Face)** — commercial descendant, core team lists Antoine Pirrone: 25 cm tall, 14 cm wide, < 800 g, 15 motors, camera, 8×8 ToF LiDAR, 2 IMUs, RK3566 (4× A55 @1.8 GHz, 1 GB RAM, 32 GB eMMC, 0.8 TOPS NPU), NP-F550 2600 mAh ≈ 1 h, $399, ships before Christmas 2026 (NA/EU/UK). Software open (Apache-2.0: [pollen-robotics/microduck](https://github.com/pollen-robotics/microduck) Rust runtime, [microduck_rl](https://github.com/pollen-robotics/microduck_rl) mjlab/MuJoCo-Warp PPO), **hardware/CAD not released** ("Pollen Robotics told the press not to refer to the robot as open-source hardware (for now)" — [CNX](https://www.cnx-software.com/2026/08/28/microduck-a-duck-like-biped-robot-designed-for-physical-ai-experimentation-and-fun/)). Actuators are modelled as "BAM M6 model of the Dynamixel XL330" i.e. **not STS3215** — [MarkTechPost](https://www.marktechpost.com/2026/08/28/pollen-robotics-hugging-face-microduck-399-open-source-rl-biped-robot/), [Pollen blog](https://pollen-robotics.com/microduck/blog/introducing-microduck/), [Engadget](https://www.engadget.com/2245407/huggingface-and-pollen-robotics-opn-pre-orders-for-the-microduck-robot/). Training: 4096 envs, "~1-2 h for a usable gait" on a CUDA GPU, obs 61 (48 proprio + 13 command), action 14, 50 Hz, randomizes battery voltage/sag, command delay, friction, ±1° gear play.
- **Hugging Face / LeRobot**: HF sponsors the project; HF acquired Pollen (Apr 2025); `experiments/LeRobot/` in the repo holds hdf5 episode-recording scripts (one marked NOT_WORKING); the LeRobot `configure_motor.py` was the original tool to set servo IDs ([issue #3 comment](https://github.com/apirrone/Open_Duck_Mini/issues/3)). Google I/O 2026 demo ran Gemma 4 E2B on Open Duck Minis fitted with Pi 5 / Jetson Orin Nano — [explainx](https://explainx.ai/blog/gemma-4-open-duck-mini-robot-on-device-ai-2026) (secondary source).

---

## 2. Servos

### 2.1 Exact list (official)

From the BOM sheet (row "Feetech 7.4v STS 3215", qty **14**, unit €14, total €196, comment: "Be sure to buy the 7.4v ones, also called 19kg.cm", link = Alibaba "Robot-Servo-STS3215-7-4V-19kg") — [BOM CSV export](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/export?format=csv). Plus "9g servos" qty 2 (Miuzei SG90-class, €3.33 each) for the antennas.

Joint → servo ID map (`docs/configure_motors.md`, `rustypot_position_hwi.py`) — all `sts3215`:

| Joint | ID | Joint | ID | Joint | ID |
|---|---|---|---|---|---|
| right_hip_yaw | 10 | left_hip_yaw | 20 | neck_pitch | 30 |
| right_hip_roll | 11 | left_hip_roll | 21 | head_pitch | 31 |
| right_hip_pitch | 12 | left_hip_pitch | 22 | head_yaw | 32 |
| right_knee | 13 | left_knee | 23 | head_roll | 33 |
| right_ankle | 14 | left_ankle | 24 | (antennas = SG90 on Pi PWM GPIO 12/13) | — |

Why one model everywhere: every MJCF joint uses the same `class="sts3215"` actuator defaults; the head servos simply get a lower firmware Kp (8 instead of 30) at runtime (`v2_rl_walk_mujoco.py` v2: `kps[5:9] = [8, 8, 8, 8]`). The Jetson fork upgraded all 14 to STS3250, showing the frame accepts the same 45×24.7×35 mm case family — [Open_Duck_Mini_Jetson](https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson).

Firmware configuration applied to every servo before assembly (`scripts/configure_motor.py`, v2 branch): `mode 0` (position), `max_acceleration 0`, `acceleration 0`, `P=32, I=0, D=0`, ID set, then goal position 0 — [configure_motor.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/configure_motor.py). "The motor will move to the 180 position during configuration, which is the actual zero position we want" ([issue #3](https://github.com/apirrone/Open_Duck_Mini/issues/3)); `hwi_feetech_sdk.py` adds a `global_offset = deg2rad(180)` for that reason.

### 2.2 Voltage

- Bus = 2S 18650 pack, 7.4 V nominal (8.4 V charged) → BMS → switch → Waveshare "Bus Servo Adapter (A)" DC-in → servos. 5 V UBEC feeds only the Pi (wiring diagram `docs/open_duck_mini_v2_wiring_diagram.png`, viewed).
- BAM identification was done at `vin=7.4` (`bam/feetech/actuator.py`: `vin=7.4, kp=32, error_gain=0.166, max_pwm=0.97`) — [actuator.py](https://raw.githubusercontent.com/Rhoban/bam/main/bam/feetech/actuator.py).
- A builder asked whether 8.4 V exceeds the "7.4 V" rating and whether a spring 18650 holder can feed 14 servos ([issue #51](https://github.com/apirrone/Open_Duck_Mini/issues/51)) — closed with no reply. Feetech's spec for the 7.4 V part says operating voltage "6-7.4V" (see below), so 8.4 V at full charge is above spec. **UNVERIFIED whether this matters in practice**; hundreds of ducks run this way.
- Waveshare adapter datasheet says "9~12.6V voltage input (the input voltage and the servo voltage must be matched)" — [waveshare](https://www.waveshare.com/bus-servo-adapter-a.htm); the duck runs it at 7.4–8.4 V (pass-through), community-confirmed working.

### 2.3 STS3215 datasheet numbers (7.4 V version, model ST-3215-C001)

From Feetech's product page ([feetechrc.com](https://www.feetechrc.com/74v-19-kgcm-plastic-case-metal-tooth-magnetic-code-double-axis-ttl-series-steering-gear.html)) and Evelta's listing ([evelta](https://evelta.com/sts3215-7-4v-19kg-dual-axis-ttl-string-servo-motor/)):

| Spec | Value |
|---|---|
| Model | ST-3215-C001, "7.4V 19KG dual-axis TTL serial servo" |
| Operating voltage | 6–7.4 V |
| Stall torque | 19.5 kg·cm @ 6 V (Feetech's 2020 evaluation page says "19.5kg.cm@7.4V", "Stall Speed: 52RPM@7.4V" — [feetechrc eval](https://www.feetechrc.com/2020-05-13_56655.html)) |
| Rated torque | 6.5 kg·cm @ 6 V (Seeed lists 5 kg·cm) |
| No-load speed | 0.238 s/60° @ 6 V (= 4.40 rad/s); 52 RPM @ 7.4 V (= 5.45 rad/s) |
| Stall current | 2000 mA @ 6 V; idle 150 mA |
| Gear ratio / material | 1:345, copper/brass ("铜") gears |
| Encoder | 12-bit magnetic, 4096 steps/360° (0.088°) |
| Weight / size | 55 ± 1 g; 45.2 × 24.7 × 35 mm |
| Comms | half-duplex TTL, 38400 bps–1 Mbps, ID 0–253 |
| Temp | operating −20…70 °C; overheat / overload (2 s at 20 % torque) / overcurrent protections in firmware |
| Price | Seeed $20 ($19 @10+) [seeed](https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html); Feetech "$15 US" overseas; Evelta India **₹2,224.30 incl. GST (₹1,885 ex-GST), 80 in stock, Mumbai** |

Sibling 7.4 V variants (same case): C044 1:191 27.4 kg·cm ([seeed C044](https://www.seeedstudio.com/Feetech-ST-3215-C044-Heavy-Duty-Servo-7-4V-1-191-Gear-Reduction-p-6460.html)), C046 1:147 14.4 kg·cm (wowrobo listing title). 12 V version C018: 30 kg·cm, 0.222 s/60°, 2.7 A stall ([robotshop](https://www.robotshop.com/products/feetech-12v-30kgcm-magnetic-encoding-servo-sts3215)). Waveshare ST3215-HS: 6–12.6 V, 20 kg·cm @ 12 V, 0.094 s/60° = 106 RPM @ 12 V, 2.4 A stall, 45.22 × 35 × 24.72 mm, 68.1 g ([waveshare wiki](https://www.waveshare.com/wiki/ST3215-HS_Servo_Motor)).

Independent bench test of an STS3215 ([Robo9](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/)): backlash ≈ 0.87° (spec ≤ 0.5°), repeatability ≈ 0.17°, 45.6 RPM at 100 % speed, ~35 kg·cm stall at 12 V, temperature 48 °C stable under 15 kg·cm static, 60 °C after 50 min oscillation and 71 °C (fault) after ~110 min. Backlash-compensation article: single motor 7–15 encoder counts (0.62–1.30°) of play depending on load — [Robo9](https://robonine.com/backlash-compensation-in-sts3215-servo-actuators/).

### 2.4 The variant / speed controversy (important for your build)

- Maintainer statement (Apr 2025): the 5.24 rad/s limit in the runtime "actually comes from system identification", linking BAM `m1.json` — [Runtime issue #7](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/7). BAM files: `max_velocity` 5.288 (m1), 5.297 (m2), 5.071 (m3/m4), 5.111 (m5), 5.096 (m6) rad/s; `kt` 1.18–1.28 N·m/A, `R` 2.45–2.75 Ω, `armature` 0.0216–0.026 kg·m² — [m1.json](https://raw.githubusercontent.com/Rhoban/bam/main/bam/params/feetech_sts3215_7_4V/m1.json) … [m6.json](https://raw.githubusercontent.com/Rhoban/bam/main/bam/params/feetech_sts3215_7_4V/m6.json). BAM's default max velocity = 3400·2π/4096 = 5.215 rad/s (firmware speed register), consistent with 52 RPM @ 7.4 V = 5.45 rad/s.
- Core contributor Mankaran Singh (Mar 2025): "Waveshare ones are compatible. But make sure to buy the ST3215-HS (106 RPM) version. the default waveshare ones have higher torque but lower speed. … @apirrone is far ahead with sim2real on ST3215-HS servos so you can buy those." — [issue #5](https://github.com/apirrone/Open_Duck_Mini/issues/5). **This contradicts the BOM (C001 1:345).**
- June 2026, two independent builders with retail C001: "the C001 model (1:345 gear ratio) seems to max out at around 2.7 rad/s. It looks like the motion requires a target velocity of around 5.24 rad/s" and a measured sim-vs-real tracking table (real Δratio: hip_pitch 0.37/0.35, knee 0.44/0.31, ankle 0.46, hip_roll ~1.0) — [issue #48](https://github.com/apirrone/Open_Duck_Mini/issues/48), open, no maintainer reply as of 2026-09-26.
- Simulation cross-check (soyeon24): MJCF `forcerange ±3.23 N·m` vs "real STS3215 stalls at 1.86 N·m" (19 kg·cm = 1.86 N·m); retraining with ±1.86 N·m limit doubled walking speed at the real limit (0.057 → 0.130 m/s) — [soyeon24/open-duck-mini-v2-build](https://github.com/soyeon24/open-duck-mini-v2-build).
- **Takeaway**: if you buy STS3215 for this kinematics, budget the policy around ≈1.9 N·m and verify no-load speed ≥ 5 rad/s at 7.4 V on your actual units before training; consider the faster 1:191 (C044) / 1:147 (C046) 7.4 V variants for knee/hip pitch, but then you must re-identify (BAM) and retrain — the published ONNX will not transfer (see 12 V experience, §6).

### 2.5 Servo model as used in simulation (MJCF defaults)

`open_duck_mini_v2.xml` class `sts3215`: `joint damping=0.56 frictionloss=0.068 armature=0.027`, `position kp=13.37 kv=0 forcerange=-3.23 3.23` (a commented `kp=17.12` line); the backlash model `open_duck_mini_v2_backlash.xml` uses `kp=17.11`; `joints_properties.xml` (onshape-to-robot template) uses `damping=0.60 frictionloss=0.052 armature=0.028 kp=17.8 forcerange=±3.35`. Maintainer: "the 17.8 in mujoco corresponds to 32 in the motors firmware units" — [issue #20](https://github.com/apirrone/Open_Duck_Mini/issues/20). Backlash class: dummy joints with `range ±0.008727 rad (±0.5°)`, `damping 0.01 armature 0.01`, one per leg joint (10 total, none on head) — [open_duck_mini_v2_backlash.xml](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2_backlash.xml). `experiments/v2/params_m6.json` in Open_Duck_Mini holds an older m6 fit (kt 1.43, R 2.04).

---

## 3. Official BOM (EUR sheet) + electronics

Source: [Google Sheet CSV export](https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/export?format=csv) (prices in €, "Estimated lowest price" column = price if you could buy exact quantities).

| Group | Part | Qty | Unit € | Total € | Lowest € | Comment / vendor |
|---|---|---|---|---|---|---|
| Power | 18650 cell (Molicel INR18650-P30B 3000 mAh 30 A) | 2 | 5 | 10 | 10 | "Get the beefiest 18650 cells you can find" (nkon.nl) |
| Power | 18650 cell holder (2S) | 1 | 4.99 | 4.99 | 4.99 | Amazon |
| Power | 2S BMS | 1 | 8.40 | 8.40 | 8.40 | (shorturl) |
| Power | 5 V regulator (HENGE UBEC 4–12 A) | 1 | 4 | 4 | 4 | Alibaba |
| Power | Small power switch | 1 | 4.49 | 4.49 | 4.49 | Amazon |
| Power | USB-C charger board | 1 | 9.99 | 9.99 | 9.99 | Amazon |
| Power | 2.1 mm barrel jack | 2 | 1 | 2 | 2 | Amazon |
| Power | XT30 connectors | 1 pair | 8 (bundle) | 8 | 0.5 | Amazon |
| Servos/ctrl/sensors | IMU BNO055 (Adafruit-style breakout) | 1 | 40 | 40 | 1 | "Need to find a cheaper alternative. Saw ~1$ ones on ali" |
| " | Raspberry Pi Zero 2W | 1 | 26.08 | 26.08 | 26.08 | |
| " | microSD card | 1 | 10 | 10 | 10 | |
| " | Servo control board — Waveshare Bus Servo Adapter (A) | 1 | 5 | 5 | 5 | [waveshare](https://www.waveshare.com/bus-servo-adapter-a.htm) ($4.99, USB-C UART, 42 × 33 mm, DC5521 jack + screw terminal, up to 253 ST/SC servos) |
| " | **Feetech 7.4 V STS3215** | **14** | 14 | **196** | 196 | Alibaba; "Be sure to buy the 7.4v ones, also called 19kg.cm" |
| " | Feet contact switches SS-10 | 4 | 1 | 4 | 4 | AliExpress (2 used per foot? guide shows one per foot pressed-fit; BOM says 4) |
| " | 9 g servos (antennas) | 2 | 3.33 | 6.66 | 6.66 | Amazon Miuzei |
| Misc | M3 heat-set inserts | 1 pack | 5.99 | 5.99 | 5.99 | Amazon |
| Misc | Standard PLA "maybe 500 g" | 1 | 20 | 20 | 0 | |
| Misc | TPU (feet) | 1 | 0 | 0 | 0 | "negligible" |
| Misc | Cable sheath | 1 | 9 | 9 | 9 | |
| Misc | 15 cm micro-USB → USB-C cable (Pi → servo board) | 1 | 7 | 7 | 7 | |
| Misc | 50 cm micro-USB → USB-C cable | 1 | 6 | 6 | 6 | |
| Misc | Bearing | 3 | 3.5 | 10.5 | 10.5 | Amazon B0CXXSVFTV (size not stated; a builder's log lists **8 × 22 × 7 mm** — [seanmayer](https://github.com/seanmayer/open-duck-mini-build), UNVERIFIED vs CAD) |
| | **Total (base robot)** | | | **398.10** | **331.10** | |
| Expression pkg | Projector reflector | 1 | 2 | 2 | 2 | AliExpress |
| " | Speaker | 1 | 6 | 6 | 6 | Amazon |
| " | LEDs (eyes + projector) | 3 | 0.2 | 0.6 | 0.6 | must buy 50 |
| " | Microphone | 1 | 15 | 15 | 15 | "Too expensive (not integrated yet)" |
| " | Eye diffusers | 4 | 0.16 | 0.64 | 0.64 | |
| " | Amplifier (MAX98357A I2S) | 1 | 5 | 5 | 5 | |
| " | Raspberry Pi camera | 1 | 5 | 5 | 5 | "(Not integrated yet)" |
| | **Total with expression package** | | | **432.34** | **365.34** | |

USD view (third-party aggregator, unverified against the sheet): STS3215 ×14 $318, Pi Zero 2W $18, BNO055 $16, Waveshare adapter $12, microSD $23, 18650 ×2 $14, UBEC $19, BMS $10, USB-C charger $11, 9 g servos $8, misc ~$31 → "Estimated Total: $500–650" — [orobot.io](https://orobot.io/o/program/BROKER-2/open-duck-mini).

India pricing datapoint: Evelta STS3215 7.4 V 19 kg 1/345 = ₹2,224.30 incl. GST → 14 pcs ≈ **₹31,140**; Alibaba/Feetech direct is $14–15 (~₹1,250–1,300 + duties). The rest of the BOM (~€200) is ≈ ₹19,000 at EU retail; cheaper in India for Pi/BMS/cells. So an STS3215 duck lands near the ₹50k ceiling only if servos are sourced at ≤ ₹1,500 each. (Exchange rates not verified; treat as order-of-magnitude.)

Electronics not in the BOM but in the design: MAX98357A I2S amp (pin table below), Pi camera (CSI, "cam" part in CAD), "flashlight" projector LED, eye LEDs, mic (not integrated). Community adapter PCBs exist for Pi Zero 2W / Pi 4 (XH2.54 connectors) — [maowenniao/Duck-mini-adapter](https://github.com/maowenniao/Duck-mini-adapter) via [issue #19](https://github.com/apirrone/Open_Duck_Mini/issues/19).

### 3.1 Wiring (from `docs/open_duck_mini_v2_wiring_diagram.png` + assembly guide pin table)

- Battery pack: 2×18650 series → BMS (B+/B−, BM tap between cells) → P+/P− → power switch → 7.4 V rail; USB-C charger board across the pack.
- 7.4 V rail → (a) UBEC → 5 V out → Pi Zero 2W micro-USB (routed through the neck), (b) Motor control board "7.4V DC in" → two servo daisy chains (left leg, right leg; neck/head servos chain from the trunk).
- Pi micro-USB (data) → motor control board USB-C. IMU → Pi I2C. Foot switches → Pi GPIO.

Pi Zero header mapping (assembly guide): Left eye LED GPIO 23 (pin 16), right eye GPIO 24 (18), projector GPIO 25 (22), common cathode GND (6); antennas left PWM GPIO 12 (32), right GPIO 13 (33), 5 V (2), GND (6); foot switches left GPIO 22 (15), right GPIO 27 (13), GND (9); BNO055 VIN 3V3 (1), SDA GPIO 2 (3), SCL GPIO 3 (5), GND (9); MAX98357A LRC GPIO 19 (35), BCLK GPIO 18 (12), DIN GPIO 21 (40), VIN 5 V (2), GND (6) — [assembly_guide.md](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/assembly_guide.md). Runtime confirms `LEFT_FOOT_PIN = 22`, `RIGHT_FOOT_PIN = 27`, pull-ups, active-low (`feet_contacts.py`).

---

## 4. Kinematics and geometry

### 4.1 Joints, axes, limits (from `open_duck_mini_v2.xml`, radians → degrees)

Source: [MJCF](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml) (generated by onshape-to-robot from the Onshape doc). Chain per leg: trunk → **hip_yaw** (z) → **hip_roll** (x) → **hip_pitch** (y) → **knee** (y) → **ankle** (y) → foot. Head: trunk → **neck_pitch** (y) → **head_pitch** (y) → **head_yaw** (z) → **head_roll** (x) → head; antennas are extra revolute joints in the URDF only (±90°, not actuated in sim).

| Joint | World axis at zero pose (computed) | Range (rad) | Range (deg) |
|---|---|---|---|
| left/right_hip_yaw | z (vertical) | ±0.5236 | ±30 |
| left/right_hip_roll | x (forward) | ±0.4363 | ±25 |
| left_hip_pitch | y (lateral) | −1.2217 … +0.5236 | −70 … +30 |
| right_hip_pitch | y | −0.5236 … +1.2217 | −30 … +70 (mirrored sign) |
| left/right_knee | y | ±1.5708 | ±90 |
| left/right_ankle | y | ±1.5708 | ±90 |
| neck_pitch | y | −0.3491 … +1.1345 | −20 … +65 |
| head_pitch | y | ±0.7854 | ±45 |
| head_yaw | z | ±2.7925 | ±160 |
| head_roll | x | ±0.5236 | ±30 |
| left/right_antenna (URDF only, SG90) | — | ±1.5708 | ±90 (runtime uses ~30° unless duty-cycle patched, [issue #41](https://github.com/apirrone/Open_Duck_Mini/issues/41)) |

Home (standing crouch) keyframe, `scene_flat_terrain_backlash.xml`: base at z = 0.15 m; left leg (yaw, roll, pitch, knee, ankle) = (0.002, 0.053, −0.63, 1.368, −0.784); right = (−0.003, −0.065, 0.635, 1.379, −0.796); head all 0. Same values are `init_pos` in the runtime HWI. Joint sign convention on hardware: leg servo ports "have to face right no matter which leg" ([issue #27](https://github.com/apirrone/Open_Duck_Mini/issues/27)); zero pose = legs straight, photo in [issue #17](https://github.com/apirrone/Open_Duck_Mini/issues/17).

Policy soft limits: `soft_joint_pos_limit_factor = 0.95`. Placo walk engine limits: `walk_max_dx_forward 0.08`, `backward 0.03` m/step, `walk_max_dy 0.1`, `walk_max_dtheta 1.0`.

### 4.2 Link lengths — computed by forward kinematics from the MJCF body `pos`/`quat` (all joints = 0, base origin at z = 220 mm as in the file)

| Segment | Value (mm) | How |
|---|---|---|
| Base origin → hip_yaw axis | x −19.0, y ±35.0, z +45.9 (hip yaw axes **70 mm apart**) | `hip_roll_assembly pos="-0.019 ±0.035 0.0459409"` |
| hip_yaw → hip_roll axis | 46.0 down, 19.05 forward (axis-to-axis 49.8) | `pos="0.01905 0 -0.046015"` |
| hip_roll → hip_pitch axis | 74.15 outboard (lateral), 35.1 rearward (axis-to-axis **82.0**) | `pos="0.07415 0 0.03511"` in the rolled frame |
| hip_pitch axis lateral position | y = ±109.1 from centre (pitch axes 218 mm apart) | computed |
| **Thigh** hip_pitch → knee | **78.65** (78.7 incl. 0.1 offset) | `pos="0 -0.07865 0.0001"` |
| **Shin** knee → ankle | **78.65** | `pos="0 -0.07865 0.0001"` |
| Ankle → foot site (sole centre) | 41.2 total: 36.2 down, 19.6 inboard, 0.5 forward | `site left_foot pos="0.0005 -0.036225 0.01955"` |
| Foot site lateral position | y = ±89.4 (foot centres ≈ 179 mm apart at zero pose; Placo uses `feet_spacing 0.16`) | computed |
| Leg fully extended: base origin → sole | 193.6 | computed |
| Home crouch: base origin → sole | 160.7 (scene puts base at 150 → sole ≈ ground, sole thickness 8 mm) | computed |
| Base origin → neck_pitch axis | 90.0 up, 19.15 lateral, 1.0 forward | `neck_pitch_assembly pos="0.001 0.01915 0.0900009"` |
| neck_pitch → head_pitch | **66.0** | `pos="0 0.066 0"` |
| head_pitch → head_yaw | 60.1 (57.0 + 19.05 offset) | `pos="0 0.057 0.01905"` |
| head_yaw → head_roll | 45.2 | `pos="0.04095 0 -0.01915"` |
| head_roll → head frame | 55.6 | `site head pos="0.04245 0 0.03595"` |
| IMU site | (−80, 0, +50) mm from base origin (rear of trunk) | `<site name="imu" pos="-0.08 -0.0 0.05"/>` |

Zero-pose heights above base origin (computed): hip yaw +46, hip roll 0, hip/knee/ankle pitch 0 / −79 / −157, sole −194; neck pitch +90, head pitch +156, head yaw +213, head roll +194, head frame +236. With the base origin ≈150 mm above ground in the crouch, the head frame sits ≈ 386 mm up; with legs extended the base is ≈ 200 mm up and the head frame ≈ 436 mm — consistent with the README's "about 42 cm".

### 4.3 Masses (MJCF inertials, overridden by slicer estimates per `sim2real.md`)

| Body | Mass (kg) |
|---|---|
| trunk_assembly (incl. 3 servos, battery, BMS, board) | 0.6985 |
| hip_roll_assembly (hip yaw servo carrier) ×2 | 0.0665 each |
| roll_to_pitch assembly ×2 | 0.0752 each |
| thigh (knee_and_ankle_assembly) ×2 | 0.1241 each |
| shin ×2 | 0.0726 each |
| foot ×2 | 0.0752 each |
| neck_pitch_assembly | 0.0662 |
| head_pitch_to_yaw | 0.0169 |
| neck_yaw_assembly | 0.0918 |
| head_assembly (incl. Pi, speaker, SG90s) | 0.4066 (URDF: 0.3526 + 2×0.0042 antenna holders) |
| **Total (computed)** | **2.107 kg** (per leg 0.414; head+neck 0.582) |

No official measured weight of the physical robot was found. 14 × 55 g servos = 0.77 kg of the total.

### 4.4 Foot and head dimensions (computed from official STLs, mm, bounding boxes)

| Part | X | Y | Z |
|---|---|---|---|
| foot_bottom_tpu (sole) | 101.9 | 40.7 | 8.0 |
| foot_bottom_pla | 93.0 | 27.7 | 8.0 |
| foot_top | 103.5 | 34.9 | 46.0 |
| foot_side | 103.5 | 12.0 | 46.0 |
| head (shell) | 199.8 | 197.3 | 59.4 |
| head_bot_sheet | 193.8 | 191.6 | 3.0 |
| body_middle_bottom | 150.0 | 110.0 | 86.2 |
| body_front | 10.0 | 110.0 | 143.0 |
| body_back | 40.0 | 110.0 | 125.0 |
| trunk_top | 125.5 | 100.7 | 41.0 |
| trunk_bottom | 54.4 | 108.0 | 73.7 |
| left/right_cache (leg cover) | 90.0 | 40.0 | 152.6 |
| left/right_roll_to_pitch | 46.9 | 86.1 | 30.7 |
| knee_to_ankle sheets | 30.7 | 7–8 | 70.6 |
| neck sheets | 30.7 | 6–7 | 58.0 |

Foot contact patch ≈ **102 × 41 mm** (TPU sole), foot length used by Placo `foot_length 0.06`. Everything fits a **256 × 256 × 256 mm P1S bed**; the head (200 mm) needs the full plate diagonal margin but no splitting (the A1-mini needs the split "Park Head" mod).

---

## 5. Printing and hardware

### 5.1 Official print guide ([print_guide.md](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/print_guide.md))

"All the parts are printed in standard PLA with 15% infill, except for `foot_bottom_tpu.stl`, which is to be printed in TPU at 40% infill." No orientation or support notes in the official guide (a Bambu 3MF was contributed in [PR #15](https://github.com/apirrone/Open_Duck_Mini/pull/15)).

Parts list (36 unique STLs in `print/`, **51 printed parts**; [issue #26](https://github.com/apirrone/Open_Duck_Mini/issues/26) says `bulb` should be ×2):

- Feet (×2 each): foot_top, foot_side, foot_bottom_pla, foot_bottom_tpu (TPU)
- Legs: knee_to_ankle_left_sheet ×4, knee_to_ankle_right_sheet ×4, leg_spacer ×4, left_roll_to_pitch ×1, right_roll_to_pitch ×1, roll_motor_bottom ×2, roll_motor_top ×2, left_cache ×1, right_cache ×1
- Trunk: trunk_bottom, trunk_top
- Neck/head: neck_left_sheet, neck_right_sheet, head_pitch_to_yaw, head_yaw_to_roll, head_roll_mount, head, head_bot_sheet, left/right_antenna_holder
- Body shells: body_front, body_middle_bottom, body_middle_top, body_back, battery_pack_lid
- Expression: bulb, flash_light_module, flash_reflector_interface, left_eye, right_eye, speaker_interface, speaker_stand

Filament: BOM says "maybe 500 g"; a builder's slicer total on an X1C/H2D: **990 g PLA + 34 g TPU** ([soyeon24](https://github.com/soyeon24/open-duck-mini-v2-build)); another builder counted "49 / 49 required printed parts + TPU feet" ([seanmayer](https://github.com/seanmayer/open-duck-mini-build)).

### 5.2 Community print settings (for PETG on a Bambu)

Jaime Machuca's BD-X cover mod README (in-repo, `print/mods/v2_Jaimes_Mods/README.md`): "Material: PETG or PLA-CF (for durability); Layer Height: 0.20 mm (features) / 0.28 mm (large flat shells optional); Infill: 15–20% gyroid or cubic; Walls: 3 perimeters for strength on structural covers; Supports: Only where unavoidable; Adhesion: Skirt or minimal brim for tall narrow pieces"; includes `Bambu_X1C_Project_File.3mf` with orientations and a `Print Orientation Reference.png`. Warning in the same README: covers "shift the overall mass distribution … existing policy still works, but may exhibit slightly reduced stability".

### 5.3 Fasteners, inserts, bearings

- Heat-set inserts: **M3** everywhere (BOM; guide: 4 in trunk_bottom for body mounting, 2 per foot, 4 in leg_spacers per leg, "all these holes" in head and body shells).
- Screws: **M3×10** (trunk_bottom↔trunk_top, corrected from M3×6 in [issue #3](https://github.com/apirrone/Open_Duck_Mini/issues/3)), **M3×6** (foot bottom), plastic self-tappers shipped with the servos for servo-to-print, servo horn screws metal-to-metal with **Loctite 243** ("Everytime you screw something in the motors metal against metal, you want to use a little loctite … Don't use loctite with the plastic screws"). Exact counts are a documented TODO ("X m3 screws (TODO : add the exact number)"); DeepWiki estimates "approximately 40-50 pieces of various lengths" (UNVERIFIED).
- Bearings: 3 in BOM (2 "roll_bearing" in the trunk for the hip-roll passive side, 1 in the head for head roll — CAD part names `roll_bearing`, `roll_bearing_2`, `roll_bearing_3`). Size not in official docs; builder log says 8×22×7 mm (608-class).
- Wire: 28 AWG silicone (Chinese guide via aifitlab), cable sheath, XT30 pack connector, 2.1 mm barrel for charger.

### 5.4 Print/CAD defects reported

- Screw head on `roll_motor_bottom` collides with `roll_to_pitch`; maintainer: "we need to dig a slot on the hip_to_pitch part … On my duck, it ended up digging its own slot" — [issue #17](https://github.com/apirrone/Open_Duck_Mini/issues/17).
- `left/right_roll_to_pitch` holes not concentric with servo holes — fixed in CAD Mar 2025 ([issue #7](https://github.com/apirrone/Open_Duck_Mini/issues/7)); make sure you use post-March-2025 STLs.
- "Fix neck part that breaks often" (maintainer TODO, [issue #33](https://github.com/apirrone/Open_Duck_Mini/issues/33)) — the neck sheets are 6–7 mm thick PLA plates; PETG/PLA-CF is the community mitigation.
- Missing STLs at one point ([issue #22](https://github.com/apirrone/Open_Duck_Mini/issues/22), closed).

---

## 6. Software and training

### 6.1 Pipeline overview (`docs/sim2real.md`)

1. Onshape → `onshape-to-robot` → MJCF (config `xmls/config.json`: `simplify_stls true`, `max_stl_size 0.005 MB`, only `foot_bottom_tpu` kept as collision geometry, all servo cases/electronics visual-only). Masses overridden with slicer estimates.
2. Actuators identified with Rhoban **BAM** on a pendulum testbench at 7.4 V; exported to MuJoCo `damping/kp/frictionloss/armature/forcerange` (§2.5).
3. Reference gaits from **Placo** (Open_Duck_reference_motion_generator) → `polynomial_coefficients.pkl`.
4. **Open_Duck_Playground** (MuJoCo Playground + MJX + Brax PPO) with Disney BDX-style imitation reward → ONNX.
5. **Open_Duck_Mini_Runtime** on the Pi runs the ONNX at 50 Hz.

### 6.2 Reference motion generator

- Engine: Placo walk engine (Rhoban); presets per robot in `robots/open_duck_mini_v2/placo_presets/{medium,fast}.json`; `auto_waddle.py --sweep` uses only the **medium** preset.
- `auto_gait.json` sweep: dx −0.04…0.06 step 0.02 (6 values), dy −0.03…0.03 step 0.02 (4), dθ −0.3…0.3 step 0.07 (10) → **240 motions** (≈ "240+ motion files" per [frankfu.blog](https://frankfu.blog/openai/understanding-reinforcement-learning-through-openduck/)); speed classes slow 0.05 / medium 0.10 / fast 0.15 m/s filter out-of-class results.
- Medium preset: `double_support_ratio 0.5`, `startend_double_support_ratio 1.0`, `walk_com_height 0.205`, `walk_foot_height 0.04`, `walk_trunk_pitch −4°`, `single_support_duration 0.18 s`, `foot_length 0.06`, `feet_spacing 0.16`, `foot_zmp_target_y −0.03`, head neck_pitch 20°, head_pitch −26° (fast: com 0.21, pitch +5°). `placo_defaults.json`: `double_support_ratio 0.18`, `walk_foot_rise_ratio 0.2`, `walk_trunk_pitch −3`.
- `fit_poly.py`: degree-15 polynomial per dimension over one gait period; 40 dims = 16 joint pos (incl. neck/head/antennas) + 16 joint vel + 2 foot contacts + 3 base lin vel + 3 base ang vel — [poly_reference_motion.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/poly_reference_motion.py).

### 6.3 Playground environment (`playground/open_duck_mini_v2/joystick.py`)

- `ctrl_dt 0.02` (**50 Hz**), `sim_dt 0.002` (500 Hz, decimation 10), `episode_length 1000` (20 s), commands resampled every 500 steps, `action_scale 0.25` rad, `dof_vel_scale 0.05`, `max_motor_velocity 5.24 rad/s` (motor targets rate-limited per control step when `USE_MOTOR_SPEED_LIMITS=True`), `USE_IMITATION_REWARD=True`.
- Tasks/XML: `flat_terrain`, `rough_terrain` (hfield), `flat_terrain_backlash`, `rough_terrain_backlash` (README "current win": `--task flat_terrain_backlash --num_timesteps 300000000`). Floor friction 0.6 (flat), 1.0 (rough).
- **Observation ("state", 101 dims, computed)**: gyro 3 + accelerometer 3 (sim adds +1.3 m/s² x-bias hack; [PR #24](https://github.com/apirrone/Open_Duck_Playground/pull/24) removes it) + command 7 (vx, vy, ωz, neck_pitch, head_pitch, head_yaw, head_roll) + (joint pos − default) 14 + joint vel×0.05 14 + last 3 actions 42 + motor_targets 14 + foot contacts 2 + imitation phase (cos, sin) 2 = **101** (matches "Observation size: 101" in training logs, [issue #19](https://github.com/apirrone/Open_Duck_Playground/issues/19)). Privileged critic obs adds true gyro/accel/gravity/linvel/angvel, root height, actuator forces, feet velocities/air time, reference frame.
- **Action**: 14 (all bus servos incl. head), `target = home_ctrl + 0.25·a`.
- Noise: joint pos hip 0.03 / knee 0.05 / ankle 0.08 rad, joint vel 2.5 rad/s, gravity 0.1, gyro 0.1, accel 0.05; action delay 0–3 steps; IMU delay 0–3 steps; pushes every 5–10 s of 0.1–1.0 m/s.
- Command ranges: vx [−0.15, 0.15] m/s, vy [−0.2, 0.2], ωz [−1, 1] rad/s; head ranges neck [−0.34, 1.1], pitch ±0.78, yaw ±1.5, roll ±0.5; 10 % zero commands.
- Rewards (scale): tracking_lin_vel 2.5 (σ 0.01, y tolerance 0.1), tracking_ang_vel 6.0, torques −1e−3, action_rate −0.5, stand_still −0.2, alive 20, **imitation 1.0** (internal: joint pos −15·Σerr², joint vel −1e−3, lin-vel xy/z exp(−8·err²), ang-vel 0.5·exp(−2·err²), contact match 1.0 per foot, torso orientation term disabled; zero when |cmd|<0.01). Reward = clip(Σ·dt, 0, 1e4). Termination: projected gravity z < 0 or NaN.
- Domain randomisation (`randomize.py`): floor friction U(0.5, 1.0), frictionloss ×U(0.9, 1.1), armature ×U(1.0, 1.05), torso CoM ±0.05 m, all link masses ×U(0.9, 1.1), torso mass ±0.1 kg, qpos0 ±0.03 rad, Kp ×U(0.9, 1.1).
- A second task `standing.py` (no imitation; orientation −0.5, head_pos −2.0, head yaw ±2.7) exists.

### 6.4 PPO / network / export

- Brax PPO with `locomotion_params.brax_ppo_config("BerkeleyHumanoidJoystickFlatTerrain")`: `num_envs 8192, batch_size 256, num_minibatches 32, unroll_length 20, num_updates_per_batch 4, learning_rate 3e-4, discounting 0.97, entropy_cost 0.005, clipping_epsilon 0.2, max_grad_norm 1.0, normalize_observations True, num_evals 15, episode_length 1000, action_repeat 1` (from training logs in [issue #8](https://github.com/apirrone/Open_Duck_Playground/issues/8) / #19).
- Policy MLP hidden **[512, 256, 128]** → 28 outputs (14 mean + 14 log-std), exported with swish activation, obs mean/std baked in, `tanh(mean)`; ONNX opset 11, output name `continuous_actions` (`export_onnx.py`); checkpoints via Orbax; TensorBoard logging.
- Deps (`pyproject.toml`): python ≥3.11, `jax[cuda12]`, `playground` (MuJoCo Playground; community pins **playground==0.0.5 + jax[cuda12]==0.8.0** to fix `mujoco_playground._src.collision` import, [issue #25](https://github.com/apirrone/Open_Duck_Playground/issues/25)), tensorflow, tf2onnx, onnxruntime, mediapy. Known fixes: `nvidia-cublas-cu12>=12.9.0` for cuSolver error ([#15](https://github.com/apirrone/Open_Duck_Playground/issues/15)); `params[1]["params"]` in export ([#8](https://github.com/apirrone/Open_Duck_Playground/issues/8)); RTX 50xx needs NGC TF container ([#16](https://github.com/apirrone/Open_Duck_Playground/issues/16)).
- **Training time/GPU**: 300 M steps "1 hour 11 minutes at 68,700 steps/s on an RTX 3090" ([soyeon24](https://github.com/soyeon24/open-duck-mini-v2-build)); "300 million steps, usually takes several hours" ([frankfu.blog](https://frankfu.blog/openai/understanding-reinforcement-learning-through-openduck/)); logs show it running on an RTX 2080 Ti and an **RTX 4060 Laptop GPU (8 GB)** ([#8 comments](https://github.com/apirrone/Open_Duck_Playground/issues/8)). **No data for a 6 GB GPU** — treat 8192 envs on an RTX 3050 6 GB as UNVERIFIED (JAX preallocation + TensorFlow export both grab VRAM; use `XLA_PYTHON_CLIENT_MEM_FRACTION`, fewer envs).
- Sim-only inference/validation: `mujoco_infer.py -o model.onnx` (keyboard/joystick), `mujoco_infer_base.py` mirrors the robot obs.

### 6.5 Deployment on the robot (Open_Duck_Mini_Runtime, `v2` branch)

- Hardware: Raspberry Pi Zero 2W (Pi 5 works with `lgpio`; it is not the reference); Raspberry Pi OS Lite 64-bit **Bookworm, Python 3.11** (3.13 images break `onnxruntime==1.18.1`, fix = `uv python install 3.11` — [Runtime #38](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/38)); pre-built image `duck.iso` v0.2.3 by MaxMakesStuff ([docs/INSTALL.md](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/docs/INSTALL.md)).
- Servo comms: `rustypot.feetech(port, 1000000)` (Pollen's Rust Feetech driver, `rustypot==0.1.0`) on `/dev/ttyACM0`; alternate HWIs exist for `pypot` (Pollen fork `support-feetech-sts3215`) and the LeRobot-style `FeetechMotorsBus` (`feetech.py`, 41 kB copy). udev: `latency_timer=1` for usb-serial.
- Control loop `v2_rl_walk_mujoco.py`: **50 Hz**, prints "Policy control budget exceeded" when late; firmware Kp `-p 30` default (HWI default 32, head 8), Kd 0; `action_scale 0.25`; `init_pos` = home pose; joint offsets from `~/duck_config.json` (found with `find_soft_offsets.py`); optional low-pass action filter (`--cutoff_frequency`); phase counter advanced by `phase_frequency_factor` 1.0 (LB "sprint" = 1.3, d-pad ±0.05); Xbox controller over Bluetooth at 20 Hz. The 5.24 rad/s target-rate clip is **commented out** on the robot.
- Robot observation (must match sim): `[gyro(3), accelero(3), cmds(7), dof_pos − init_pos(14), dof_vel×0.05(14), last_action(14), last_last(14), last_last_last(14), motor_targets(14), feet_contacts(2), imitation_phase(2)]` = 101 — [v2_rl_walk_mujoco.py](https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/v2_rl_walk_mujoco.py). Head joints: `motor_targets[5:9] += head commands` from the controller.
- IMU: `adafruit_bno055` over I2C, **NDOF mode**, axis remap depends on `imu_upside_down` (assembly note: photos show it mounted upside down; config flag handles it), raw `gyro` + `acceleration` read in a 50 Hz thread; optional calibration offsets pickle.
- Pretrained policy in the hub repo: `BEST_WALK_ONNX_2.onnx` (trained for the 7.4 V STS3215 model; does not transfer to 12 V servos, see §7).
- Features toggled in `duck_config.json`: eyes, projector, antennas, speaker, microphone, camera; `start_paused`; `phase_frequency_factor_offset`.

---

## 7. Known problems reported by builders and their fixes

| # | Problem | Evidence | Fix / status |
|---|---|---|---|
| 1 | **Leg servos too slow / weak for the policy** (STS3215-C001 1:345 ≈ 2.7 rad/s measured vs 5.24 rad/s assumed; real joint amplitude only 31–46 % of commanded on hip_pitch/knee/ankle) | [issue #48](https://github.com/apirrone/Open_Duck_Mini/issues/48) (Jun 2026, open); redEddie: "the motors couldn't keep up with the policy output" ([#49](https://github.com/apirrone/Open_Duck_Mini/issues/49)) | No maintainer answer yet. Options discussed: faster 1:191/1:147 variants, ST3215-HS (per [#5](https://github.com/apirrone/Open_Duck_Mini/issues/5)), or retrain with realistic `forcerange ±1.86` (soyeon24 doubled real-limit speed). |
| 2 | **Voltage sag → servo bus CRC/checksum errors, rustypot panic** | [#49](https://github.com/apirrone/Open_Duck_Mini/issues/49): 4 A-rated cell failed below ~50 % charge | "Switching to a high-discharge battery (I used a 25A-rated Samsung cell)" or bench PSU; BOM already specifies Molicel P30B 30 A cells. |
| 3 | **12 V / 30 kg STS3215 swap → feet trembling, wrong gait** | [#21](https://github.com/apirrone/Open_Duck_Mini/issues/21); maintainer: "12v servos and the 7.4v ones are different, meaning they require different parameters … not surprising … `BEST_WALK_ONNX2.onnx` doesn't work with your 12v servos" | Re-identify with BAM and retrain. One builder put 12 V servos only in the knees "which stopped the duck from falling over" but lost right-foot clearance ([#52](https://github.com/apirrone/Open_Duck_Mini/issues/52)). |
| 4 | **Wrong IMU orientation flag → oscillation / can't balance** | growbotics/Chinese guide note (search snippet): "If the imu_upside_down parameter is not set, the robot will exhibit abnormal oscillations"; assembly guide notes photos show it upside down | Set `imu_upside_down` in `duck_config.json`; verify with `imu_server.py`/`imu_client.py`. |
| 5 | **Head twists / breaks during `find_soft_offsets`** | [Runtime #32](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/32); README: head control "very experimental … it can break your duck's head" | Servo mounted in wrong orientation; compare with zero-pose photo ([#17](https://github.com/apirrone/Open_Duck_Mini/issues/17)); keep head Kp low (8). |
| 6 | **Neck part breaks often** | maintainer TODO [#33](https://github.com/apirrone/Open_Duck_Mini/issues/33) | Planned redesign (v2.5); community prints structural parts in PETG/PLA-CF. |
| 7 | **BMS problems / availability** | [#33](https://github.com/apirrone/Open_Duck_Mini/issues/33): "too many issues with the current one" | Planned new BMS; builders swap holders ("compact replacement 2S battery holder … fits the reprinted rear panel", [seanmayer](https://github.com/seanmayer/open-duck-mini-build)). |
| 8 | **Do not power servos from the UBEC 5 V** | seanmayer build log | Servos on raw 7.4 V rail only. |
| 9 | Hip screw-head interference; non-concentric holes | [#17](https://github.com/apirrone/Open_Duck_Mini/issues/17), [#7](https://github.com/apirrone/Open_Duck_Mini/issues/7) | Slot the part / use updated STLs. |
| 10 | Doc errors: M3×6 vs M3×10; bulb ×2; camera missing from BOM; SS-10 switch mounting undocumented | [#3](https://github.com/apirrone/Open_Duck_Mini/issues/3), [#26](https://github.com/apirrone/Open_Duck_Mini/issues/26), [#9](https://github.com/apirrone/Open_Duck_Mini/issues/9), [#14](https://github.com/apirrone/Open_Duck_Mini/issues/14) | Fixed in guide / press-fit switches "so that the switch is activated when the foot touches the ground". |
| 11 | Pi 5: GPIO (RP1) breaks `RPi.GPIO`; "Policy control budget exceeded" 2–35 ms | [Runtime #40](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/40), [#24](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/24) | `pip uninstall RPi.GPIO; pip install lgpio`; gpiozero shim. |
| 12 | `set_kps()` "Parsing error" at startup | [Runtime #26](https://github.com/apirrone/Open_Duck_Mini_Runtime/issues/26) (open, 6 comments) | Check all IDs with `check_motors.py`; often a missing/duplicate ID or bus power. |
| 13 | Antennas move only ~30° | [#41](https://github.com/apirrone/Open_Duck_Mini/issues/41) | Patch duty-cycle mapping to 0.5–2.5 ms. |
| 14 | Robot "won't move forward" with joystick; unstable in other people's sims | [#56](https://github.com/apirrone/Open_Duck_Mini/issues/56), [#43](https://github.com/apirrone/Open_Duck_Mini/issues/43) | Unresolved on GitHub; maintainer redirects to Discord. |
| 15 | Sim-side bugs found by an external audit | soyeon24: gravity sensor slot read `local_linvel` instead of `upvector`; "48 % of the forward range is unreachable" (command range vs reference sweep); head-tracking reward never registered; ONNX viewer 98 % CPU busy-wait | Fixed in that fork (commits c8eed76, 51d4212, 7d6cadb). |
| 16 | Cosmetic cover mods shift CoM → wobble | Jaime's mod README | Retrain/fine-tune with updated inertials. |
| 17 | **Foot slipping** | **No explicit builder reports found** on GitHub/blogs. Design mitigations: TPU sole at 40 % infill, sim floor friction 0.6 and DR 0.5–1.0. Discord not searchable. | — |
| 18 | **Servo overheating** | **No duck-specific reports found.** Generic STS3215 data: thermal fault ≈ 71 °C after ~110 min continuous oscillation, 48 °C steady under 15 kg·cm ([Robo9](https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/)); firmware overheat/overload protection. | — |
| 19 | Backlash | Designers model ±0.5° per leg joint in `flat_terrain_backlash`; independent measurement 0.62–1.30° per STS3215 ([Robo9](https://robonine.com/backlash-compensation-in-sts3215-servo-actuators/)) | Train with the backlash XML (the "current win"). |

---

## 8. Implications for the "microduck" build (PETG, P1S, STS3215-only, INR 50k, RTX 3050 6 GB, Windows/WSL2)

1. **Servo choice is the #1 risk.** Open Duck Mini v2 proves 14× STS3215 at 7.4 V can walk, but the published policy assumes ≈5.2 rad/s and ±3.2 N·m in sim, while retail C001 units measured ≈2.7 rad/s and stall at 1.86 N·m. Decide the exact sub-model (C001 1:345 / C044 1:191 / C046 1:147 / Waveshare ST3215-HS) before CAD, then identify it (BAM) and train against the true limits. Keep the mass budget ≤ 2.1 kg or lighter than the original.
2. **Geometry to reuse**: thigh = shin = 78.65 mm; hip yaw axes 70 mm apart; hip pitch axes ≈218 mm apart (wide BDX stance via the 86 mm roll-to-pitch bracket); foot 102 × 41 mm; neck 66 mm; head ≈200 mm wide. The 5-DoF leg (yaw-roll-pitch-knee-ankle, no ankle roll) is what the RL stack expects.
3. **Printing**: nothing exceeds 200 mm, so the P1S needs no split parts; official PLA 15 %/TPU 40 %; community PETG guidance 0.2 mm / 15–20 % gyroid / 3 walls; PETG on the servo-mount plates (neck, knee sheets) addresses the known breakage.
4. **Budget**: at Indian retail (₹2,224/servo) the 14 servos alone are ≈₹31k; the rest at EU prices is ≈₹19k → right at ₹50k. Direct-from-Feetech pricing (~$15) leaves headroom.
5. **Training on your machine**: the stack is Linux/CUDA (JAX + MJX); run it in WSL2 Ubuntu. Pins that worked for others: `playground==0.0.5`, `jax[cuda12]==0.8.0`, `nvidia-cublas-cu12>=12.9`. An 8 GB laptop 4060 ran the default 8192-env config; a 6 GB 3050 will likely need `num_envs` 2048–4096 and `XLA_PYTHON_CLIENT_MEM_FRACTION=0.6`, and the TensorFlow ONNX export should run on CPU. Expect several hours (3090 does 300 M steps in 71 min). Isaac Lab is an alternative path (Jetson fork trains `Isaac-Velocity-Rough-OpenDuck-v0` with 4096 envs, 50 Hz policy / 200 Hz physics) but the ROS/Isaac route has no official Open Duck support.
6. **Runtime**: copy the 50 Hz ONNX loop, 1 Mbps bus, firmware Kp 30–32 (= MuJoCo kp ≈17.8), Kd 0, acceleration 0, BNO055 raw gyro/accel, foot micro-switches; 25–30 A 18650 cells.

---

## 9. Open questions (could not be verified)

1. Which exact STS3215 sub-model apirrone's own walking duck uses (BOM says 7.4 V "19 kg.cm" = C001 1:345; a core contributor said ST3215-HS 106 RPM; BAM max velocity 5.1–5.3 rad/s matches 52 RPM @ 7.4 V, i.e. C001 at 7.4 V, not 6 V).
2. Physical measured mass of a built v2 (only the 2.107 kg model sum is available).
3. Bearing size (official BOM gives an Amazon link only; 8×22×7 mm comes from one builder).
4. Exact screw counts (documented TODO).
5. Whether 8.4 V (full 2S) on servos rated 6–7.4 V causes long-term issues (asked in #51, unanswered).
6. Any foot-slip or overheating reports (likely on Discord; not indexable).
7. VRAM needed for the default 8192-env MJX config (smallest confirmed GPU: 8 GB laptop 4060).
8. Tnkr guide contents (HTTP 403) and Onshape assembly details (login-gated).

---

## 10. Source index

Primary (raw files read):
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/README.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/print_guide.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/assembly_guide.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/sim2real.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/configure_motors.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/docs/open_duck_mini_v2_wiring_diagram.png
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/print/mods/v2_Jaimes_Mods/README.md
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v2/print/*.stl (36 files, bounding boxes computed)
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/v1/README.md
- https://docs.google.com/spreadsheets/d/1gq4iWWHEJVgAA_eemkTEsshXqrYlFxXAPwO515KpCJc/export?format=csv
- https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/xmls/open_duck_mini_v2.xml (+ `_backlash.xml`, `scene_*_backlash.xml`, `config.json`, `joints_properties.xml`)
- https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/open_duck_mini_v2/{joystick,base,constants,runner,standing,custom_rewards,mujoco_infer_base}.py
- https://raw.githubusercontent.com/apirrone/Open_Duck_Playground/main/playground/common/{rewards,randomize,runner,export_onnx,poly_reference_motion}.py and `pyproject.toml`, `README.md`
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/{README.md,checklist.md,example_config.json,setup.cfg,docs/INSTALL.md}
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/scripts/{v2_rl_walk_mujoco,configure_motor}.py
- https://raw.githubusercontent.com/apirrone/Open_Duck_Mini_Runtime/v2/mini_bdx_runtime/mini_bdx_runtime/{rustypot_position_hwi,raw_imu,duck_config}.py (+ `main` branch `hwi_feetech_sdk.py`, `imu.py`, `rl_utils.py`, `feet_contacts.py`, `find_soft_offsets.py`, `check_voltage.py`)
- https://raw.githubusercontent.com/apirrone/Open_Duck_reference_motion_generator/main/{README.md,scripts/auto_waddle.py,scripts/fit_poly.py}
- https://raw.githubusercontent.com/apirrone/Open_Duck_reference_motion_generator/main/open_duck_reference_motion_generator/robots/open_duck_mini_v2/{auto_gait.json,placo_defaults.json,placo_presets/medium.json,placo_presets/fast.json,open_duck_mini_v2.urdf}
- https://raw.githubusercontent.com/Rhoban/bam/main/bam/params/feetech_sts3215_7_4V/m1.json … m6.json ; https://raw.githubusercontent.com/Rhoban/bam/main/bam/feetech/actuator.py ; https://raw.githubusercontent.com/Rhoban/bam/main/README.md
- GitHub issues (via API): Open_Duck_Mini #1, #3, #5, #7, #9, #14, #17, #19, #20, #21, #26, #27, #33, #41, #43, #48, #49, #51, #52, #56, #57; Runtime #7, #12, #24, #26, #30, #32, #38, #40; Playground #4, #5, #8, #14, #15, #16, #19, #25

Secondary:
- https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/
- https://github.com/soyeon24/open-duck-mini-v2-build ; https://github.com/seanmayer/open-duck-mini-build ; https://scalablehuman.com/2026/08/14/building-open-duck-mini-v2-from-software-project-to-physical-robot/
- https://frankfu.blog/openai/understanding-reinforcement-learning-through-openduck/
- https://github.com/XiaohuiChen-personal/Open_Duck_Mini_Jetson ; https://github.com/SteveNguyen/openduckminiv2_playground ; https://github.com/rimim/AWD
- https://www.feetechrc.com/74v-19-kgcm-plastic-case-metal-tooth-magnetic-code-double-axis-ttl-series-steering-gear.html ; https://www.feetechrc.com/2020-05-13_56655.html ; https://www.seeedstudio.com/STS3215-19kg-cm-7-4V-Serial-Servo-p-6338.html ; https://www.seeedstudio.com/Feetech-ST-3215-C044-Heavy-Duty-Servo-7-4V-1-191-Gear-Reduction-p-6460.html ; https://evelta.com/sts3215-7-4v-19kg-dual-axis-ttl-string-servo-motor/ ; https://www.robotshop.com/products/feetech-12v-30kgcm-magnetic-encoding-servo-sts3215 ; https://www.waveshare.com/wiki/ST3215-HS_Servo_Motor ; https://www.waveshare.com/bus-servo-adapter-a.htm
- https://robonine.com/testing-of-feetech-sts3215-servomotor-backlash-repeatability-and-torque/ ; https://robonine.com/backlash-compensation-in-sts3215-servo-actuators/
- https://orobot.io/o/program/BROKER-2/open-duck-mini ; https://aifitlab.com/blogs/tech-blogs/all-info-about-openduckmini ; https://deepwiki.com/apirrone/Open_Duck_Mini/2.2-assembly-guide
- Microduck: https://pollen-robotics.com/microduck/ ; https://pollen-robotics.com/microduck/blog/introducing-microduck/ ; https://github.com/pollen-robotics/microduck ; https://github.com/pollen-robotics/microduck_rl ; https://www.cnx-software.com/2026/08/28/microduck-a-duck-like-biped-robot-designed-for-physical-ai-experimentation-and-fun/ ; https://www.marktechpost.com/2026/08/28/pollen-robotics-hugging-face-microduck-399-open-source-rl-biped-robot/ ; https://www.engadget.com/2245407/huggingface-and-pollen-robotics-opn-pre-orders-for-the-microduck-robot/
- https://explainx.ai/blog/gemma-4-open-duck-mini-robot-on-device-ai-2026 ; https://www.linkedin.com/posts/cherry-xu-60a12b103_feetech-sts3215-20kgservo-activity-7333775961068392452-LToH

---

## Critic additions (2026-09-26, from `07_critic_gaps.md`)

1. **Bearing size corrected (§3 BOM table, §5.3, open question 3).** The official BOM row 27 links amazon.fr ASIN **B0CXXSVFTV**, which is "Kozelo 2 pcs 6804ZZ 20 x 32 x 7 mm" ([amazon.fr](https://www.amazon.fr/dp/B0CXXSVFTV); the same ASIN on amazon.com resolves to the same 6804ZZ product). The reference mesh `mini_bdx/robots/open_duck_mini_v2/roll_bearing.stl` measures **OD 32.00 / ID 20.00 / W 7.00 mm** (critic's STL measurement). So the design uses **3 x 6804ZZ (20 x 32 x 7)**, not 8 x 22 x 7; the 8 x 22 x 7 in seanmayer's log is that builder's substitution. BOM qty 3 at EUR 3.5 = 3 bearings (2 hip-roll passive pivots, 1 head roll).
2. **Model mass, three files, two numbers (§4.3).** Critic re-summed: Playground `open_duck_mini_v2.xml` = **2.1071 kg** (15 `<inertial>`, slicer-overridden masses per `sim2real.md`); `mini_bdx/robots/open_duck_mini_v2/robot.xml` and the reference-motion-generator URDF = **2.0615 kg** (21 inertials, CAD masses). The 2.107 kg above and SPECS.md's 2.06 kg are both correct for their file; `03_sts3215.md`'s 2.045 kg matches neither.
3. **Ankle to ground (§4.2).** 36.2 mm is base-to-foot-*site*; the mesh sole bottom is **38.8 mm** below the ankle axis (SPECS §3). Use 38.8 mm for ground contact; the site sits ~2.6 mm inside the 8 mm TPU sole.
4. **Roll-to-pitch: 82.0 mm is the axis-to-axis distance** (74.15 outboard, 35.1 rearward); the "86 mm" in §8 is the `left_roll_to_pitch` part's bounding-box length (86.07). Use 82.0 for kinematics.
5. **Reference-mesh dimensions (critic's measurements of the `v2` branch `mini_bdx/robots/open_duck_mini_v2/*.stl`, bounding boxes in mm)** — these are the purchased/electronic parts and brackets as modelled in the Onshape CAD, which is otherwise login-gated:

| Mesh | Size (mm) | What it is |
|---|---|---|
| wj-wk00-0122topcabinetcase_95 / 0123middlecase_56 / 0124bottomcase_45 | 45.22 x 24.72 x 9.70 / 13.90 / 14.10; **union 45.22 x 24.72 x 35.70** | STS3215 case, three shells |
| drive_palonier | disc **O19.95 x 5.05**, centre hole O3.2 | output horn disc |
| passive_palonier | disc **O19.95 x 3.10**, bore O6.1 | idler-side disc (rides on the O6 rear shaft) |
| roll_bearing | OD 32.00 / ID 20.00 / W 7.00 | 6804ZZ |
| raspberrypizerow | 65.9 x 31.25 x 4.1 | Pi Zero 2 W board |
| board | 42.02 x 33.02 x 1.6 | Waveshare Bus Servo Adapter (A) |
| bno055 | 20.0 x 27.0 x 3.0 | generic BNO055 breakout (Adafruit version is 20 x 27 x 4 mm, 3 g: [adafruit.com/product/2472](https://www.adafruit.com/product/2472)) |
| cell / holder | O18 x 65 / 76 x 41 x 20 | 18650 cell / 2-cell holder |
| usb_c_charger / bms / power_switch | 38.2 x 18.1 x 5.15 / 40.6 x 15.85 x 3.6 / 23.4 x 7.4 x 16.8 | |
| sg90 | 32.6 x 13.0 x 31.0 | antenna servo (not needed for the microduck) |
| left_knee_to_ankle_left_sheet / _right_sheet | 30.70 x 8.45 x 70.65 / 30.70 x 7.20 x 70.65 | shin plates |
| leg_spacer | 28.07 x 36.90 x 10.00 | |
| roll_motor_bottom / roll_motor_top | 32.00 x 30.74 x 31.41 / 38.00 x 28.72 x 20.01 | hip-roll servo clamshell |
| left_roll_to_pitch | 46.90 x 86.07 x 30.72 | |
| neck_left_sheet | 30.72 x 7.05 x 57.99 | |
| head_pitch_to_yaw / head_yaw_to_roll / head_roll_mount | 31.99 x 44.90 x 72.00 / 87.95 x 79.98 x 42.20 / 40.00 x 64.74 x 15.10 | |
| foot_top / foot_side / foot_bottom_tpu | 103.47 x 34.90 x 46.00 / 103.46 x 12.00 x 46.00 / 101.93 x 40.73 x 8.00 | |
| head / trunk_top / trunk_bottom | 199.83 x 197.32 x 59.40 / 125.47 x 100.72 x 41.00 / 54.36 x 108.00 x 73.68 | |
| body_middle_top / battery_pack_lid | 150.0 x 110.0 x 56.78 / 7.5 x 51.4 x 86.4 | |

6. **Rebuilding the assembly without Onshape:** import the 36 `print/*.stl` plus the meshes above into SolidWorks and place each by the MJCF `<body pos quat>` values in §4.2 (the `mini_bdx` `robot.xml` has one `<geom>` per part with its pose). That yields servo orientation per joint, horn side, screw side and cable routing — the items a CAD engineer otherwise cannot get from this repo.
7. **Sim/real mismatch to remember (§6.3 vs §6.5):** the sim rate-limits motor targets at 5.24 rad/s, but the runtime has that clip commented out — the real limit is the physical servo (2.7 rad/s measured by 2026 builders vs 5.45 rad/s datasheet at 7.4 V). Measure on the first units and set the sim limiter to the measured value.
