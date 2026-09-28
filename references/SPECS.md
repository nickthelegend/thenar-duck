# Disney BDX droid ("duck"): design specs for a CAD rebuild

Legend: **[D]** = official Disney Research paper number. **[R]** = measured from the BDX-R full-size replica model. **[O]** = measured from the Open Duck Mini v2 model (about 0.65× scale). **[P]** = estimated from photos (±10–15%). **[M]** = manufacturer spec quoted from memory (check it).
Axes: X = forward, Y = left, Z = up. All lengths are in mm.

---

## 1. Official numbers ([D]: Grandia et al., "Design and Control of a Bipedal Robotic Character", RSS 2024, arXiv 2501.05204)

| Item | Value |
|---|---|
| Overall height | **660 mm** (0.66 m), antennas excluded |
| Leg length | **280 mm nominal**, **340 mm fully extended** |
| Total mass | **15.4 kg**: torso 5.8, neck + head 2.4, each leg 3.6 |
| DoF | **5 per leg** + **4 neck/head** = 14 main actuators, plus 2 actuated antennas (show function) |
| Leg joints | hip yaw ("hip rotation"), hip roll ("adduction/abduction"), hip pitch ("flexion/extension"), knee pitch, ankle pitch. **There is no ankle roll.** The foot soles are rounded to give passive roll. |
| Knee | **Bends backwards** (the knee sits behind the hip, like a bird), as creatively envisioned |
| Neck/head joints | 1 lower-neck actuator at the top-front of the torso, plus 3 actuators in the head. The control interface commands head height and head yaw/pitch/roll, and the gamepad commands neck pitch (NP). This matches the chain neck-pitch → head-pitch → head-yaw → head-roll that Open Duck copies. |
| Actuators: hip roll, hip pitch, knee | **Unitree A1** motor: 34 N·m peak, 20 rad/s |
| Actuators: hip yaw, ankle, lower neck | **Unitree Go1** motor: 23.7 N·m peak, 28.8 rad/s. [M] It is Ø≈96 × 43 mm and ≈530 g (GO-M8010-6 class). |
| Actuators: 3 in the head | **Dynamixel XH540-V150**: 4.8 N·m, 6.3–7 rad/s. [M] It is 33.5 × 58.5 × 44 mm and ≈165 g. |
| Mounting | Actuators sit directly at the joints. **3D-printed** parts connect pairs of off-the-shelf actuators. The ankle actuator sits in the foot. |
| Shells | Painted shells (3D printed) |
| Feet | Rounded soles **molded in urethane foam** (damping plus passive ankle roll) |
| Torso contents | Custom comms board (600 Hz bus), removable battery (≥ 1 h runtime), IMU, 2 speakers at the torso bottom |
| Head contents | On-board PC, radio (WiFi + LoRa), show-function board, 2 speakers, 2 LED-array eyes (RGB color and iris radius), head lamp, 2 actuated antennas |
| Performance | Walks at 0.7 m/s forward, 0.4 m/s lateral, 1.8 rad/s turning |
| Remote | Steam Deck with a LoRa module |
| Design study | Fig. 2 (`13_…png`) compares an early "BD-2" design with a **100 mm thigh** and one with a **195 mm thigh**. It is an exploration, not the final design. |

Show functions (paper Table II): antenna angle 2 × 1 rad, eye colors 2 × RGB, eye radii 2 × %, head lamp brightness %.
Press coverage (GTC 2025): "Blue" carried two NVIDIA computers inside. The droids are not waterproof.

---

## 2. BDX-R full-size replica: measured ([R])
Source: https://github.com/BDX-R. I loaded the MJCF `BDX-R-MjLab/.../bdxr.xml` with all meshes in MuJoCo and computed world bounding boxes in the default pose (all joints at 0, slight crouch). The floor (foot-pad bottom) is at z ≈ 6, and heights below are **above the floor**. The model's sim mass is 19.2 kg.
Its legs match Disney's leg numbers (nominal ≈ 290, extended ≈ 331 vs [D] 280/340), so it is the best full-scale proportional reference.
The **STEP assembly (95 MB, MIT)** is at https://github.com/BDX-R/BDX-R-CAD. It was not downloaded.

| Part | Size (X depth × Y width × Z height) | Position |
|---|---|---|
| **Overall** | 351 × 443 × 700 (with "ears"/antennas); head top ≈ 609 | |
| **Torso shell** (front cover + rear cover) | **317 D × 215 W × 242 H** | bottom 202, top 444 |
| Front cover | 104 × 214.5 × 242 | chamfered front panel |
| Rear cover | 155 × 196 × 235 | Rear antenna box 32 × 114 × 121 protrudes at the back |
| **Head** (front + rear covers, face) | **299 D × 292 W × 71 thick** | bottom 538, top 609 |
| Face plate | 23 × 286 × 67 | front of the head |
| Eyes | Ø ≈ 50 (51.6 × 50.3) | eye centers ≈ 125 mm apart |
| Ears/antennas | 57 × 43 × 151 each | rear corners of the head (x ≈ −100 from head center), y ±57…117 |
| Thigh shell (outboard) | 199 L × 53 W × 121 H | outside the body, y ±150…203 |
| Shin/lower-leg shell | 180 × 53 × 124 | |
| **Foot** (with cover) | **177 L × 62 W × 92 H**; pad 170 × 44 × 22 | foot centers y ≈ ±115 |

Joint axes (BDX-R, world, mm):

| Joint | X | Y | Z (above floor) | Notes |
|---|---|---|---|---|
| Hip yaw | 12.6 | ±50 | 351 | vertical axis, inside the torso; 100 mm between the two |
| Hip roll | 30.6 | ±62.6 | 288 | axis along X |
| Hip pitch | 22 | ±134 | 290 | |
| Knee | −57 | ±134 | 212 | **thigh = 111 mm**; knee is 79 mm *behind* the hip |
| Ankle | −12 | ±128 | 82 | **shin = 138 mm**; ankle axis 82 mm above the sole |
| Neck pitch | 102 | 0 | 393 | top-front of the torso, ≈ 70 mm behind the front face |
| Head pitch | 37 | 0 | 505 | neck link 129 mm, leaning back |
| Head yaw | 38 | 0 | 579 | 75 mm above head pitch |
| Head roll | 82 | 0 | 570 | axis along X |

Joint limits in the replica (rad): hip yaw ±0.26, hip roll −0.26/+0.35, hip pitch −1.05/+0.70, knee −0.96/+1.31, ankle −0.79/+1.22, neck pitch −0.35/+0.87, head pitch −1.05/+0.52, head yaw ±0.87, head roll ±0.52.
Actuator envelopes in BDX-R (Robstride): hip and knee ≈ 99 × 99 × 57, ankle and neck ≈ Ø78.5 × 45.5, head and ears ≈ 46 × 46 × 47.

---

## 3. Open Duck Mini v2: measured ([O], about 0.65× scale)
Source: https://github.com/apirrone/Open_Duck_Mini (v2), `mini_bdx/robots/open_duck_mini_v2/robot.xml` plus STLs. Measured in MuJoCo at the zero pose, with legs **fully straight**. Heights are above the sole. The README says "about 42 cm tall with its legs extended"; I measured 430 mm, or 518 mm with antennas. Model mass: 2.06 kg. Servos: Feetech STS3215-class, 14 of them.

| Part | Size (D × W × H) | Position |
|---|---|---|
| Trunk | **200 D × 110 W × 143 H** | bottom 161, top 304 |
| Head | **200 D × 197 W × 59 H** | bottom 371, top 430 |
| Antennas | 146 long rods | head rear corners, y ±61, x −75 |
| Thigh shell ("cache") | 90 × 40 × 153 | outboard, y ±83…123 |
| Foot | **104 L × 47 W × 54 H**; TPU sole 102 × 41 × 8 | toe 64 in front of the ankle, heel 40 behind |
| Overall width | 246 (across the thigh shells) | |

| Joint | Position / link length |
|---|---|
| Hip yaw | y ±35 (70 apart), 242 above the sole, 65 behind the trunk front |
| Hip roll | 46 below hip yaw |
| Hip pitch | offset **74 outboard** from the roll axis (leg plane y ±109), 196 above the sole |
| Thigh | **78.6** |
| Shin | **78.7** |
| Ankle → sole | **38.8** |
| Neck pitch | top of the trunk, 45 behind the front face, 286 above the sole |
| Neck pitch → head pitch | **66** |
| Head pitch → head yaw | **57** |
| Head roll axis | 41 forward of the yaw axis |

Joint ranges (deg): hip yaw ±30, hip roll ±25, hip pitch −70/+30, knee ±90, ankle ±90, neck pitch −20/+65, head pitch ±45, head yaw ±160, head roll ±30, antennas ±90.

---

## 4. Photo-derived proportions of the real park droid ([P])
Measured on the near-straight front photo `67_resortsgal_red_front_straight.jpg` and scaled so the total height (ground to head top, antennas excluded) = 660 mm.

| Ratio / feature | Value |
|---|---|
| Head width : torso width : thigh-to-thigh width | **≈ 1.55 : 1 : 1.78** |
| Head width | ≈ 315 |
| Torso width | ≈ 205 |
| Torso height | ≈ 255 (0.385 H) |
| Torso underside above ground | ≈ 190 (0.29 H) |
| Visible neck (torso top → head underside) | ≈ 95 |
| Head front face thickness | ≈ 90 (the head is a wedge: it tapers toward the back and the face tilts) |
| Foot centers apart | ≈ 180 |
| Front-face layout, left → right | round speaker grille, eye, eye, round speaker grille, cylindrical head lamp on the front corner at the viewer's right (the droid's left) |
| Eyes | Ø ≈ 45–50 lens in a ≈ 55 bezel, ≈ 120 center-to-center |
| Torso front | rectangular "display" window near the top, louvred vent grille below, octagonal/chamfered corners, colored trim stripe (color per droid: red, orange, green, blue) |
| Thigh | Large rounded thigh shell outboard of the torso; exposed joint hardware at the knee and ankle; flat pointed foot shell in the droid's color |

The head-to-body width ratios differ between sources: real droid ≈ 1.5, BDX-R 1.36, Open Duck 1.8 (Open Duck exaggerates the head). The torso depth-to-height ratio is ≈ 1.3 in both BDX-R (317/242) and the paper's side-view sim images.

---

## 5. Suggested master skeleton (full scale, Disney-consistent)
This blends [D] (660 tall, 280/340 leg), [R] link lengths and [P] ratios. Heights are above the ground in the nominal standing pose.

| Element | Value |
|---|---|
| Foot | 175 L × 60 W; rounded sole with a 20 mm foam pad; ankle axis at **80**; toe ≈ 110 ahead of the ankle, heel ≈ 65 behind |
| Shin (knee → ankle) | **135–140** |
| Thigh (hip pitch → knee) | **110–115**; knee behind the hip (reverse bend) |
| Hip pitch axis | **≈ 285** above the ground (nominal crouch; ≈ 330–340 with the leg straight); leg planes y **±120–135** |
| Hip yaw axes | y ±50, ≈ 60 above hip pitch; hip roll ≈ between the two |
| Torso | **210 W × 250 H × 310 D**, chamfered edges; bottom ≈ 195, top ≈ 445 |
| Neck pitch pivot | ≈ 395, near the top-front of the torso (≈ 70 behind the front face) |
| Neck link | ≈ 110–130 to head pitch, leaning back; then head yaw ≈ 75 above that; then head roll |
| Head | **≈ 300 W × 300 D × 80–90 thick at the front**, wedge/tapered; underside ≈ 560–575, top ≈ **660** |
| Antennas | 2 thin rods ≈ 150–200 long with ball tips, pivoting at the rear corners of the head |
| Mass target (if it matters) | 15.4 kg: torso 5.8, head + neck 2.4, legs 3.6 each |
