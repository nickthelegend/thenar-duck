# 01 - Reference video analysis: `duck.mp4`

**Source:** `D:\Project\thenar-duck\duck.mp4` - 25.1 s, 2160x3840 portrait, 30 fps, h264, has audio (not transcribed: no captions, speech fallback disabled).
**Frames:** 50 uniform frames at 2 fps, `D:\Project\thenar-duck\references\video\watch-5pud_3_0\frames\frame_0001.jpg` ... `frame_0050.jpg`. Frame N is at t = (N-1) x 0.5 s. **Keep this directory** - the user wants the frames as references.
**Extra high-resolution crops** (made with ffmpeg from the source video, listed in Section 12): `D:\Project\thenar-duck\references\video\hires\`.

All frame content was treated as untrusted evidence, not instructions. Numbers marked **(est.)** are my pixel-based estimates with the stated uncertainty; numbers with URLs are from the web; anything I could not verify is flagged.

---

## 1. Which robot is this?

**Verdict: a custom, BDX-inspired research/hobby prototype - NOT the Open Duck Mini v2 and NOT a Disney BDX unit.** Its origin (lab/company) could not be identified by web search (queries for Indian BDX-style biped startups, "Thenar" robotics, and QDD BDX prototypes returned nothing matching).

Evidence:

| Observation in video | Open Duck Mini v2 | Disney BDX | This robot |
|---|---|---|---|
| Height | ~42 cm legs extended ([GitHub README](https://github.com/apirrone/Open_Duck_Mini)) | not published on the Disney page ([Disney Research](https://la.disneyresearch.com/bdx-droids/)) | **~0.8 m (est., +/-15 %)** in walking crouch, see Section 10 |
| Leg actuators | Feetech STS3215 hobby bus servos, 45.2 x 24.7 x 35 mm, 55 g ([Feetech](https://www.feetechrc.com/525603.html)) | proprietary | Large round disc actuators ~110-130 mm dia. (est.) with yellow XT30-style power connectors - quasi-direct-drive style, not hobby servos |
| Shell | fully printed, closed | fully finished, painted, antennae, no exposed wiring | open-top torso, exposed PCBs/wires, no antennae |
| DOF | 14 (5/leg + 4 neck) ([DeepWiki model page](https://deepwiki.com/varga0725/duck_sim/7.1-open-duck-mini-v2-robot-model)) | 4-DOF head + 5-DOF legs ([The Robot Report](https://www.therobotreport.com/rbr50-spotlight-disney-research-develops-new-approach-robotic-characters/)) | 3-4 visible/implied per leg + hip roll; 3-4 neck (Section 6-7) |
| Cost class | "under $400" BOM ([GitHub README](https://github.com/apirrone/Open_Duck_Mini)) | n/a | closest analogue is Kayden Knapik's BDX-R: 16 RobStride QDD motors, ~$2,800 ([Interesting Engineering](https://interestingengineering.com/ai-robotics/disney-bd-x-droid-homebuilt-robot)) |

Implication for the user's build: the video is a **styling and gait reference only**. Its actuators are an order of magnitude larger/stronger than an STS3215 (30 kg.cm peak at 12 V per [Feetech](https://www.feetechrc.com/525603.html)), so the "microduck" must be scaled down (Open Duck Mini v2 class, ~40-45 cm) while copying this robot's look.

---

## 2. Scene, scale cues and on-screen text

- Indoor office: glossy light-beige marble-look floor tiles laid on a diagonal to the camera; whiteboard with handwritten notes (illegible at this resolution, not robot-relevant text); potted plants, a steel bin, curtains.
- A seated operator (office chair, barefoot) holds a **black wired compact keyboard-like device** on his lap and presses keys throughout - teleoperation input. Two thin cables run from the keyboard down to the robot's head (visible frames 1-5 and 36-50): the robot is **wire-tethered** to the operator's input device. Whether the walk is an RL policy taking velocity commands or a scripted gait cannot be determined.
- **No captions, overlays or on-screen text.** Only a small blue/white sticker on the head's top surface (frames 3-7, unreadable).
- Scale cues: floor tiles (assumed 600 x 600 mm, the most common Indian vitrified size per [HouseYog](https://www.houseyog.com/blog/standard-tile-sizes-india/) and [Orientbell](https://www.orientbell.com/tiles/tile-size) - **not verified for this floor**), the seated adult, and a standard office chair.
- Camera: handheld phone, ~1.2-1.4 m high, tilted down ~28-30 deg (derived from tile-line vanishing geometry and the operator's head position; see Section 10).

---

## 3. Colour scheme and panel lines

- **Shells (head + torso): matte off-white** (printed/painted, slightly glossy). Faceted "low-poly" styling with chamfers.
- **Everything mechanical is black**: neck column, all leg links, actuator housings, feet, cable sleeving. A **light-grey** ankle knuckle part on each leg (frames 10-17, `side_t02_legs.jpg`) - different material or unpainted print.
- **Accents:** blue/white eye LEDs; one blue LED and one green LED on PCBs inside the open torso top; two small green status LEDs on the rear-top grey panel; a **red LED in the torso's bottom-front "chin" slot**; yellow XT30-type connectors on leg actuators; green PCB visible as the head's base plate.
- **Panel lines:** torso is split into left/right side shells + a top cap (visible seam on the top edge, frames 3-7); a thin horizontal slit ~1/3 of the way up each torso side (frames 10-25); front face split into 5-6 facets with a vertical centre seam (frames 45-50); a dark grey rectangular inset panel on the torso's top-rear (frames 3-7, 36-50); a trapezoidal dark "mouth" slot at the bottom-front chin (frames 44-50, `front_t24_hips.jpg`).

---

## 4. Head

Best frames: side/three-quarter `frame_0003.jpg` (t=1.0), `frame_0005.jpg` (t=2.0), `frame_0007.jpg` (t=3.0); frontal `frame_0044.jpg` (t=21.5), `frame_0046.jpg` (t=22.5), `frame_0048.jpg` (t=23.5); hires `side_t02_head.jpg`, `front_t22_head.jpg`.

- **Shape:** wide, flat, wedge/"visor" head - a truncated triangular prism seen from the side, much wider than tall. Top surface slopes down toward the front; front face is a wide dark **visor opening** (open, no glass) spanning ~85 % of the head width. Whole head is pitched **~15-25 deg nose-down (est.)**.
- **Two round eyes** inside the visor: LED rings ~ 1/6 of head width (est.), bright white/blue. Left eye reads as a white ring with dark centre, right eye a blue glow (frames 44-50).
- **Two black cylindrical "ear pods"** (speaker-grille position on BDX) on the left and right ends of the head, roughly eye-diameter, protruding sideways/slightly forward (frames 3-7 show the near pod as a black dome; frames 40-50 show both).
- **No antennae** on this robot.
- **Base plate:** a green PCB-like flat plate closes the bottom of the head and extends **behind** the white shell as a tray carrying boards (an SBC-sized green board with connectors, a black camera-like module at front centre, wires). Frames 3-7 and 20-24 show the tray; `side_t02_head.jpg` shows it clearly.
- **Interior:** a large black round component (eye housing or speaker) behind each eye, loose wiring, small PCBs.
- **Rough dimensions (est., +/-20 %):** width ~0.30 m shell / ~0.33 m over ear pods; height ~0.13 m; depth (shell) ~0.20-0.25 m, PCB tray extends further back. Head width : torso width ~ 1.4-1.6 : 1.

---

## 5. Neck and head articulation

Best frames: `frame_0005.jpg`, `frame_0013.jpg` (t=6.0), `frame_0021.jpg` (t=10.0), frontal `frame_0044.jpg`-`frame_0050.jpg`; hires `front_t22_head.jpg`, `side_t12_full.jpg`.

- **Neck = one angled black column** (~60 mm square section, est.) rising from the torso's top-centre, tilted forward ~30 deg from vertical, ending in a bracket under the head's rear third. The head is **cantilevered forward**: the visor front sits well ahead of the torso front.
- **Base actuator:** a large silver-topped round motor (vertical axis, ~2/3 of the torso's inner width) sits centrally in the upper torso directly under the neck column (frames 3-7, `side_t02_full.jpg`, `side_t12_torso_top.jpg`). Most likely the neck-base yaw - not verifiable.
- A small round bolt-circle disc is visible at the neck-to-head junction (`frame_0005.jpg`, `frame_0011.jpg`) - a head pitch and/or roll actuator.
- **Observed motion:** head **roll** oscillates roughly +/-5-10 deg in phase with the gait (compare `frame_0044.jpg`, `frame_0047.jpg`, `frame_0049.jpg`, `frame_0050.jpg`); small head **yaw** changes (frames 46-48); head **pitch** stays nose-down throughout. This is consistent with a 3-4 DOF neck like BDX's "four degrees of freedom to look up, down, around, and tilt" ([The Robot Report](https://www.therobotreport.com/rbr50-spotlight-disney-research-develops-new-approach-robotic-characters/)). Vertical head bob is small (a few cm at most).

---

## 6. Torso

Best frames: `frame_0005.jpg`, `frame_0016.jpg` (t=7.5), `frame_0028.jpg` (t=13.5), frontal `frame_0048.jpg`, `frame_0050.jpg`; hires `side_t02_full.jpg`, `side_t12_full.jpg`, `front_t24_full.jpg`, `front_t24_hips.jpg`.

- **Boxy, taller than wide**, chamfered/faceted: vertical side walls, faceted front face narrowing to a chamfered **chin** at the bottom-front with the red-LED "mouth" slot. Top is flat with the **open front half** (electronics exposed - prototype state) and a dark grey inset panel with two green LEDs on the rear half (looks like a power/status panel).
- Lower rear corners are cut away where the legs attach; the side shells extend down over the hip actuators (frames 10-17).
- **Rough dimensions (est., +/-20 %):** width ~0.21 m, height ~0.30 m, depth ~0.25-0.30 m. Torso height is ~0.35-0.4 of total robot height - the body is big and the legs short, as on BDX.
- Wiring: a thick black braided sleeve exits the torso's rear-lower side and runs down each leg to the knee/ankle (frames 3-35).

---

## 7. Leg kinematic chain

Best frames: `frame_0011.jpg` (t=5.0), `frame_0013.jpg` (t=6.0), `frame_0016.jpg` (t=7.5), `frame_0024.jpg` (t=11.5), `frame_0028.jpg` (t=13.5); frontal `frame_0046.jpg`-`frame_0050.jpg`; hires `side_t02_legs.jpg`, `side_t12_full.jpg`, `front_t24_hips.jpg`, `front_t24_full.jpg`.

Chain from torso to floor (per leg), as visible:

1. **Hip roll (abduction)** - a black disc seen face-on at each lower-outer torso corner in the frontal frames (axis fore-aft), e.g. `frame_0047.jpg` right hip, `frame_0050.jpg` both. Connects the torso to the outboard thigh block via a short black bracket (`front_t24_full.jpg`, left side around x 430-480, y 600-700 in the 1050 px crop).
2. **Hip pitch** - the **upper large round disc** at the torso's bottom-front corner (axis left-right); ~110-130 mm dia. (est.); bolt circle of 8-10 screws; yellow XT30-type connector.
3. **Thigh link** - flat black plate joining hip disc to knee disc; hip-to-knee axis distance ~1.4-1.7 disc diameters (est.), i.e. ~170-200 mm.
4. **Knee** - the **lower large disc**, same size as the hip disc, sitting low and behind the hip (digitigrade / "reverse-knee" look like BDX and Open Duck). Both discs are motors (both have power connectors).
5. **Shank link** - short black link, knee-to-ankle ~1.0 disc diameter (est.), ~110-130 mm. Thigh : shank ~ 1.5 : 1 (est.).
6. **Ankle pitch** - a **small disc ~60-70 mm (est.)** with a silver bearing rim, housed at the top of the foot's heel block (`front_t24_hips.jpg` shows the rim inside each heel block; `frame_0024.jpg` shows the disc at the ankle). Light-grey knuckle part between shank and foot.
7. **Foot** - see Section 8.

**Hip yaw could not be resolved.** BDX has "five degree-of-freedom legs" ([The Robot Report](https://www.therobotreport.com/rbr50-spotlight-disney-research-develops-new-approach-robotic-characters/)) and Open Duck Mini v2 has hip yaw/roll/pitch, knee, ankle ([DeepWiki](https://deepwiki.com/varga0725/duck_sim/7.1-open-duck-mini-v2-robot-model)); this robot may hide a hip yaw inside the torso or have only 4 DOF/leg. The robot does turn ~90 deg in place during t=8-17 s, which is easier with hip yaw but not proof.

Hip span (outer edge to outer edge of thigh blocks) ~2x torso width; stance width (foot centre to centre) ~1x torso width (est., frontal frames).

---

## 8. Foot

Best frames: `frame_0005.jpg`, `frame_0011.jpg`, `frame_0024.jpg`, `frame_0031.jpg` (t=15.0), frontal `frame_0048.jpg`; hires `side_t02_legs.jpg`, `front_t24_hips.jpg`, `floor_t24_tiles.jpg`.

- **Wedge / "boot" shape:** a tall rectangular **heel block** at the rear (houses the ankle actuator) and a **low sloped toe wedge** running forward to a thin toe edge. Flat sole. No toe/heel articulation seen.
- **Bolt pattern:** a circular pattern (6 screws around 1 centre) on the heel block's top face, plus screws along the wedge.
- **Rough size (est., +/-20 %):** length ~0.20-0.23 m (~1.6-1.7 hip-disc diameters; from `floor_t00_tiles.jpg` the foot is ~0.36-0.38 of a 600 mm tile edge), width ~65-70 mm (~0.3 torso width), heel-block height ~90 mm, toe edge ~15-20 mm thick.
- Feet stay nearly parallel to each other; during swing the foot pitches toe-down and lifts only ~2-3 cm (est.) - see the 4 fps strips.

---

## 9. Fasteners, servo horns, cables, electronics (as visible)

- Countersunk/socket-head screws on all leg plates and the foot; actuator faces show 8-10 bolt circles (typical of a printed planetary/cycloidal housing or a QDD motor flange). No hobby servo horns anywhere.
- Yellow XT30-style power connectors on each large leg actuator; multi-coloured thin signal wires; black braided sleeving torso-to-leg on both legs.
- Head: green base PCB/tray with an SBC-sized board and a camera-like module; open wiring.
- Torso: blue and green LEDs on boards around the central motor; grey rear-top panel with two green LEDs.
- Two thin tether wires head-to-keyboard (operator).

---

## 10. Scale and proportional estimates

**Method.** (a) Grout lines were detected with intensity scan-lines in `floor_t00_tiles.jpg` (0.6 x full-res crop from y=1900). Two depth-direction lines D1: x = 280 + 0.65(y-450), D2: x = 914 + 1.18(y-450) and the left-right line L1: y = 544 - 0.30(x-100) (passing just in front of the near foot) give a 600 mm tile edge of ~502 px at the foot's depth; from the L1 and D2 slope ratio the camera tilt is ~30 deg and the grid yaw ~31 deg, giving ~1.55 px/mm (full-res) at the foot. (b) Independently, from the seated operator's head (assumed 1.25-1.35 m above the floor when seated) and a typical phone FOV (64-70 deg long side), the camera tilt is ~28-30 deg at ~1.2-1.4 m height, the robot's foot is ~1.6-1.8 m from the camera and the head top projects to **0.80-0.86 m**. (c) The tile method gives 0.67-0.83 m depending on the assumed tilt; at the 30 deg tilt found in (b) it gives ~0.83 m.

**Total height (head top to floor, walking crouch, t=0): ~0.80 m (est., range 0.7-0.9 m).** Fully extended legs would add maybe 5-10 cm. **This depends on the 600 mm tile assumption**; if the tiles are 800 mm the robot would be ~1.0 m.

Proportions (est., +/-15-20 %, perspective-corrected where possible; from `side_t12_full.jpg` verticals and `front_t24_full.jpg` widths):

| Item | Fraction of total height | Absolute (for 0.8 m) |
|---|---|---|
| Head height (shell top to PCB base) | 0.14-0.16 | ~0.12-0.13 m |
| Neck gap (head base to torso top) | 0.10-0.12 | ~0.09-0.10 m |
| Torso height | 0.35-0.40 | ~0.28-0.32 m |
| Hip axis above floor (crouched) | ~0.40 | ~0.32 m |
| Leg length hip axis to sole (extended, est.) | ~0.45 | ~0.33-0.39 m |
| Head width (shell / with ear pods) | 0.36-0.40 / ~0.42 | ~0.29-0.32 / ~0.33 m |
| Torso width | ~0.26 | ~0.21 m |
| Hip span (outer) | ~0.52 | ~0.42 m |
| Stance width (foot centres) | ~0.25 | ~0.20 m |
| Foot length / width | ~0.27 / ~0.085 | ~0.22 m / ~0.07 m |
| Large actuator disc dia. | ~0.14 | ~0.11-0.13 m |

**Requested ratio - head width : torso width : leg length : total height ~ 0.37 : 0.26 : 0.45 : 1** (or ~1.4 : 1 : 1.7 : 3.8 in torso-width units).

---

## 11. Gait

Sources: 2 fps frames; 6 fps sheets `gait_sheet_t03-07_6fps.jpg`, `gait_sheet_t09-13_6fps.jpg`, `gait_sheet_t19-23_6fps.jpg`; 4 fps feet strips `feet_strip_t08-16_4fps.jpg`, `feet_strip_t17-25_4fps.jpg`, `feet_t17-21_4fps_4x4.jpg`, `feet_t21-25_4fps_4x4.jpg` (read left-to-right, top-to-bottom; cell k is at t_start + (k-1)/4 s).

- **Timeline:** t=0-8 s the robot walks toward the camera-left in a three-quarter/side view (camera zooms in and briefly pans up to the operator at t~4 s, frames 8-9). t=8-17 s it **turns ~90 deg toward the camera** with very slow steps, mostly pivoting on the near (left) foot while the far leg steps around (frames 18-35). t=17-25 s it walks **straight toward the camera** (frames 36-50).
- **Cadence (straight walk, t=17-25):** alternating foot lifts at roughly 1.0 s intervals - left ~17.3, 19.5, 21.2, 23.1 s; right ~18.4, 20.4, 22.4, 24.1 s (read from the 4 fps strips, +/-0.25 s). **Stride period ~2.0 s per leg (~0.5 Hz), ~1 step/s overall.** Swing lasts only 1-2 cells (~0.25-0.5 s), so the gait spends >50 % of the cycle in double support - a shuffling, flat-footed walk.
- **Turning phase (t=8-16):** roughly one far-leg step per 3-4 s.
- **Step length:** small - ~0.3-0.5 foot lengths (~5-10 cm, est.). Forward speed ~0.04-0.08 m/s (est. from the robot's apparent size change over t=17-25 s).
- **Body motion:** clear lateral weight shift/sway each step (torso shifts relative to the head, `gait_sheet_t19-23_6fps.jpg` row 2), small torso yaw, low vertical bob; the head **rolls +/-5-10 deg** with the sway and stays nose-down; knees stay bent throughout (never straightens - BDX-style crouched posture).
- **Foot behaviour:** foot pitches toe-down during swing, lands roughly flat, ~2-3 cm clearance; feet parallel, stance ~ torso width.

For the RL agent: target a ~0.5 Hz stride at ~0.05-0.1 m/s for a look-alike gait on the small robot; Open Duck Mini v2 was trained in MuJoCo per the [Hackaday coverage](https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/), and BDX itself was trained with RL "in simulation before ever taking a real step" ([Disney](https://thewaltdisneycompany.com/news/behind-the-bdx-droids/)).

---

## 12. Where to look (timestamp -> frame -> feature)

| Feature | Timestamps | 2 fps frames | Hi-res crops |
|---|---|---|---|
| Wide shot, floor tiles, operator, whole robot | 0.0-0.5 s | `frame_0001.jpg`, `frame_0002.jpg` | `wide_t00_full.jpg`, `floor_t00_tiles.jpg` (+`_grid`) |
| Head side/three-quarter: visor, ear pod, PCB tray, sticker | 1.0-3.5 s | `frame_0003`-`frame_0008` | `side_t02_head.jpg`, `side_t02_full.jpg` (+`_grid`) |
| Neck column, base motor, torso top electronics, rear grey panel | 1.0-3.0 s, 5.5-9.5 s | `frame_0003`-`frame_0007`, `frame_0012`-`frame_0020` | `side_t02_full.jpg`, `side_t12_torso_top.jpg` |
| Operator + keyboard (context) | 4.0-4.5 s | `frame_0008`, `frame_0009` | - |
| Leg chain side view: hip disc, thigh, knee disc, shank, ankle, foot | 4.5-8.0 s | `frame_0010`-`frame_0017` (best 11, 13, 16) | `side_t02_legs.jpg` |
| Turning; far knee disc, hip-roll housing, foot pivot | 8.5-17.0 s | `frame_0018`-`frame_0035` (best 24, 28, 31) | `side_t12_full.jpg` (+`_grid`), `gait_sheet_t09-13_6fps.jpg`, `feet_strip_t08-16_4fps.jpg` |
| Frontal: both eyes, ear pods, torso facets, chin LED, hip-roll discs, both feet | 17.5-25.0 s | `frame_0036`-`frame_0050` (best 46, 48, 50) | `front_t22_head.jpg`, `front_t24_full.jpg` (+`_grid`), `front_t24_hips.jpg`, `floor_t24_tiles.jpg` |
| Head roll/yaw during walking | 21.5-24.5 s | `frame_0044`-`frame_0050` | `gait_sheet_t19-23_6fps.jpg` |
| Gait cadence | 17-25 s | - | `feet_t17-21_4fps_4x4.jpg`, `feet_t21-25_4fps_4x4.jpg` |

Hi-res crops were made with ffmpeg from the source at full 2160x3840 resolution: `side_t02_*` = t=2.0 s, `side_t12_*` = t=12.0 s, `front_t22_head` = t=22.0 s, `front_t24_*` = t=24.5 s, `wide_t00_full` = t=0 s scaled to 1080 px. `_grid` variants have a labelled 100 px pixel grid for measurement. Watch-skill working dir: `D:\Project\thenar-duck\references\video\watch-5pud_3_0\` (do not delete).

---

## 13. Reference specs pulled for later agents (with sources)

- Open Duck Mini v2: "about 42 centimeters tall with its legs extended", BOM "under $400", Raspberry Pi Zero 2W, Onshape CAD, BOM in Google Sheets - [github.com/apirrone/Open_Duck_Mini](https://github.com/apirrone/Open_Duck_Mini). 14 DOF: left/right hip_yaw, hip_roll, hip_pitch, knee, ankle + neck_pitch, head_pitch, head_yaw, head_roll - [DeepWiki duck_sim model page](https://deepwiki.com/varga0725/duck_sim/7.1-open-duck-mini-v2-robot-model). BNO055 IMU, MuJoCo simulation, designers Antoine Pirrone and Gregoire Passault - [Hackaday](https://hackaday.com/2025/04/05/disneys-bipedal-bdx-series-droid-gets-the-diy-treatment/).
- Disney BDX: head 4 DOF, legs 5 DOF, RL pipeline in simulation - [The Robot Report](https://www.therobotreport.com/rbr50-spotlight-disney-research-develops-new-approach-robotic-characters/); trained in simulation before real steps - [Disney](https://thewaltdisneycompany.com/news/behind-the-bdx-droids/). No official height/weight found.
- BDX-R (DIY, closest analogue to the video robot's actuator class): 16 RobStride motors, ~$2,800, 40 V mower battery, trained in NVIDIA simulation - [Interesting Engineering](https://interestingengineering.com/ai-robotics/disney-bd-x-droid-homebuilt-robot).
- Feetech STS3215 (12 V variant ST-3215-C018): 45.2 x 24.7 x 35 mm, 55 +/-1 g, 30 kg.cm peak / 10 kg.cm rated at 12 V, 0.222 s/60 deg, 4-14 V, 12-bit magnetic encoder, half-duplex serial 38400 bps-1 Mbps, 360 deg / 4096 counts - [feetechrc.com](https://www.feetechrc.com/525603.html). 7.4 V variant listed as 19 kg.cm - [RobotShop](https://www.robotshop.com/products/magnetic-encoding-servo-sts3215-74v-19kgcm).
- Bambu Lab P1S: 256 x 256 x 256 mm build volume, all-metal hotend to 300 C, enclosed - [3DPros](https://3dpros.com/printers/bambu-lab-p1s); Bambu's own page on using the full 256 mm volume - [Bambu Wiki](https://wiki.bambulab.com/en/knowledge-sharing/print-volume-limitations) (fetch returned 402; title only). PETG support on P1S not confirmed from a fetched page (Bambu store returned 403) - verify.
- Indian floor tiles: 600 x 600 mm is the most common size - [HouseYog](https://www.houseyog.com/blog/standard-tile-sizes-india/), [Orientbell](https://www.orientbell.com/tiles/tile-size).

---

## 14. Open questions / unverifiable items

1. Exact tile size in the video (600 vs 800 mm) - changes all absolute sizes by 33 %.
2. Whether the legs have a hip-yaw joint (hidden inside the torso) - 4 vs 5 DOF per leg.
3. Actuator make/model (large discs look like printed planetary/cycloidal housings on BLDC motors, but could be commercial QDD units); no logos visible.
4. Whether walking is an RL policy with keyboard velocity commands or a scripted gait.
5. Head interior: is the green base a functional PCB, and what is the black front-centre module (camera/depth sensor)?
6. Identity of the lab/company - no web match found.

---

## Critic additions (2026-09-26, from `07_critic_gaps.md`)

1. **Disney BDX official height is published**: 660 mm (antennas excluded), leg 280 mm nominal / 340 mm extended, 15.4 kg — Grandia et al., RSS 2024, arXiv 2501.05204 (see `references/SPECS.md` §1). Section 1's "not published" refers only to the Disney Research web page. The video robot at ~0.8 m (est.) is therefore ~1.2x a real BDX, not a BDX.
2. **PETG on the P1S is confirmed** (open question 7): Bambu's P1S spec sheet lists PETG under "Ideal" (see `04_printing_petg_p1s.md` §1.1).
3. **Video styling scaled to the microduck (Open Duck Mini v2 size).** Scale factor = 0.42 m / 0.80 m = **0.525** (Open Duck legs-extended height over the video robot's crouched height; both +/-15 %, so treat every number below as +/-20 %). Derived from Section 10; compare with the Open Duck v2 part sizes in `02_open_duck_mini_v2.md` §4.4 / `SPECS.md` §3.

| Feature | Video (0.8 m robot) | x0.525 -> microduck | Open Duck Mini v2 actual | Note |
|---|---|---|---|---|
| Total height (crouch) | 0.80 m | 420 mm | 386 crouch / 430 extended | matches |
| Head width (shell / over ear pods) | 0.30 / 0.33 m | 158 / 173 mm | 200 (shell) | Open Duck head is ~25 % wider; the video head is narrower and taller |
| Head height | 0.13 m | 68 mm | 59 | |
| Head depth (shell) | 0.20-0.25 m | 105-131 mm | 197 | video head is a shallow visor; Open Duck head is a deep plate |
| Neck gap (head base to torso top) | 0.09-0.10 m | 47-53 mm | ~67 (neck-pitch axis 286 -> head bottom 371 minus shell) | |
| Torso W x H x D | 0.21 x 0.30 x 0.27 m | 110 x 158 x 142 mm | 110 x 143 x 200 | width identical; video torso is taller and shallower |
| Hip axis above floor (crouch) | 0.32 m | 168 mm | hip pitch 196 (legs straight) | |
| Leg length hip axis -> sole (extended) | 0.33-0.39 m | 173-205 mm | 78.65 + 78.65 + 38.8 = 196 | matches |
| Hip span (outer) | 0.42 m | 220 mm | 246 across thigh shells; hip-pitch axes 218 apart | matches |
| Stance width (foot centres) | 0.20 m | 105 mm | 179 (zero pose), placo feet_spacing 160 | video stance is much narrower relative to hip span; do not copy — the RL policy was trained at ~160-180 |
| Foot L x W | 0.22 x 0.07 m | 115 x 37 mm | 104 x 47 (sole 102 x 41) | close; a 115 x 40 wedge foot is a cosmetic-only change if the sole stays 102 x 41 |
| Heel block height | 0.09 m | 47 mm | foot_top 46 | matches |
| Large actuator disc dia. | 0.11-0.13 m | 58-68 mm | STS3215 case 45.2 x 24.7 x 35.7 | a ~O60 printed disc cover hides the servo and reproduces the QDD look |

4. **Thigh : shank.** Video 1.5 : 1 (est.), Open Duck 1 : 1 (78.65/78.65), Disney/BDX-R 0.8 : 1 (111/138). Recommendation in `07_critic_gaps.md` G2: keep 1 : 1 for phase 1 (placo presets, reference motions and the actuator model all assume it); reverse-knee styling covers can fake the video's longer-thigh look.
5. **Antennae**: this robot has none (Section 4), so the microduck needs no antenna servos — 14 x STS3215 total, no PWM servos.
