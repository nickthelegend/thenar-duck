# Thenar Duck — revision B

Rebuilt mechanical CAD for the 14-servo duck, Raspberry Pi 4B and DFRobot SEN0374 BNO055. This is a digital prototype: dimensions were taken from manufacturer drawings where available; unknown product variants use adjustable mounts and explicitly stated capacity limits. No physical measurement, print, load test or powered walking test has been performed.

## Open these first

- [Complete build guide](../../README.md) — printing, BOM, assembly, wiring and commissioning.
- [P1S 0.4 mm colored Bambu Studio project](bambu/Thenar_Duck_B_P1S_ALL_PARTS.3mf) — 19 plates, 94 objects including tests and alternatives; ordinary TPU uses the external spool.
- [P1S plate overview](bambu/plate_overview.png) and [slicer verification](bambu/RELEASE_CHECKS.md).
- `renders/01_assembled.png` — assembled robot.
- `renders/02_covers_removed.png` — mechanism and internal layout.
- `renders/04_service_layout.png` — labelled component positions and access.
- `ASSEMBLY.md` — installation order, screw access and removal paths.
- `VERIFICATION.md` — actual test results and motion restrictions.
- `Thenar_Duck_B_PRINTS.zip` — selected STLs, alternatives, fit coupons and instructions.
- `Thenar_Duck_B_FULL_ASSEMBLY.glb` — named review model with hardware envelopes.
- `Thenar_Duck_B_PRINTED_PARTS.step` — editable imported solids in assembly positions.
- `solidworks/Thenar_Duck_B_REVIEW.SLDASM` — static native review assembly; keep its accompanying SLDPRTs together.

## What changed

| Item | Revision B provision |
|---|---|
| BK 4200 3S battery | BONKA BK-4200/35-3S published reference **137 × 44 × 27 mm**; sled accepts **140 × 50 × 32 mm**, plus 2 mm pad and separate rear connector bay. “BK” was interpreted as BONKA; the actual battery label was not available. |
| Pi 4B | Removable tray, official 58 × 49 mm mounting grid, 5 mm underside standoffs, microSD notch and side connector opening. |
| DFRobot SEN0374 | Its own rigid bracket beside the Pi, matching the **two Ø2 mm holes on one edge, 16 mm apart**. Space above the board for header plugs. |
| Servo adapter | Dedicated Waveshare Bus Servo Adapter (A) mounting pattern. The 7.2 V buck adapter from the original cart is a different component. |
| PDB | Insulated 4 mm spacers and adjustment slots for 28–33 mm square mounting pitch. Matek PDB-XT60 is the dimensional reference for the unverified xcluma clone. |
| UBEC | Open tie-down saddle, capacity 45 × 22 × 15 mm. No invented mounting-hole pattern. |
| Fuse and switch | External service pod; fuse-body capacity 45 × 24 × 24 mm and separate terminal space. Four interchangeable switch-cutout lids. |
| Eye LED rings | Two rear-loading sockets, removable sleeves for 37/44/45/46 mm ring PCBs, wire notches and front diffusers. |
| 4×4 LED matrix | Removable chest carrier for a 30–40 mm square PCB, bezel and diffuser. |
| Bare WS2812B-2020 | Dedicated 10 × 10 mm solder-carrier pocket and lightpipe. A small carrier PCB must be added; the bare LED cannot be screwed into plastic. |
| Foot switches | Four retained adjustable KW10 cassettes, removable wire covers and captive ground plungers. |

The enclosure is 21 mm lower than revision A. The head and limb interfaces retain the pinned Open Duck mechanism, including the local clearances for the Waveshare vendor servo model. This changes packaging, mass and load distribution; a stock walking controller is not validated for it.

## Print selection

Use `reports/print_manifest.csv`, **not every file indiscriminately**. Each ordinary file is an installed part; mirrored instances have separate names. `C01–C04` are fit coupons. `C05` lids and `C06` eye sleeves are **alternatives**, not additional installed parts. The assembled default uses the 19.4 × 13.2 mm switch lid and two 45 mm eye sleeves. Choose the matching alternatives if needed.

Structural parts use PETG; soles require TPU or an appropriately compliant replacement. Eye/chest diffusers and the lightpipe use translucent material. Print the small insert/bearing/servo coupons and one switch cassette first to establish printer fit. M3 × 4 mm means a 3 mm screw thread and 4 mm insert length; it does not specify the insert's outside diameter. The default new-part pilot is Ø4.0 × 4.5 mm deep and is adjustable in the source.

## Source and regeneration

- Parameters and evidence: `../../design/spec_B.json`.
- Parametric generator: `../build_duck_B.py`, using helpers from `../build_duck.py`.
- Retained validated core: `../thenar_duck_A/`, derived from Open Duck Mini v2 commit `b23317a485b3cec7d8417f352478778b3475173c`.
- Original reference and Apache-2.0 licence: `../reference_open_duck/`.

From `D:\Project\thenar-duck`:

```powershell
.venv-cad\Scripts\python.exe cad\build_duck_B.py
.venv-cad\Scripts\python.exe cad\check_B_packaging.py
.venv-cad\Scripts\python.exe cad\check_B_eyes.py
.venv-cad\Scripts\python.exe cad\check_B_battery_capacity.py
.venv-cad\Scripts\python.exe cad\check_motion.py --revision-b
.venv-cad\Scripts\python.exe cad\check_servo_fit.py --revision-b
py cad\export_solidworks.py --revision-b
.venv-cad\Scripts\python.exe cad\finalize_B.py
```

New mounts are parametric solids. Retained upstream STL geometry is sewn faceted BREP; its original feature history has not been reconstructed. The SolidWorks assembly is fixed in a review pose, not a fully mated mechanism. Manufacturer servo CAD is included as reference geometry; its redistribution licence was not established.

See `SOURCES.md` for published evidence and `BOM.md` for installed hardware and custom fastener counts.
