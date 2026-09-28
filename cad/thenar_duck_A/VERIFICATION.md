# Verification record — revision A

**Status: fit-review candidate; do not print the whole robot yet.**

## Completed digital checks

- 75 active STL files: 69 robot pieces and six fit coupons. Every exported mesh is watertight, has positive volume, and fits within a 256 mm cube. This is an envelope check, not a slicer/support check.
- The generator rejects invalid BREP or disconnected printed solids. Retained source meshes were converted to faceted solids; their original feature history is not reconstructed.
- Exact solid checks found no overlap between the new torso parts and the reserved electronics volumes in the neutral position.
- The vendor servo models were checked against the printed parts in neutral. Local nominal mounting reliefs corrected the detected overlaps; the repeat check found none above the 0.1 mm³ reporting threshold. Reliefs preserve one solid per bracket and remove less than 1% at each affected interface. These are nominal mating surfaces, not a substitute for measuring printed tolerances or testing insertion with cables attached.
- Sampled removal checks passed for the battery, Pi tray and IMU bridge (24 positions total). Follow ASSEMBLY.md: covers, cables and fasteners must be removed first.
- The motion screen evaluated 124 poses against the new torso and reserved electronics: 120 had no detected contact; four had contact. All sampled individual leg poses, 11 crouches, and 14 coordinated neck/head poses passed that screen.
- This motion screen preceded the final local servo-interface reliefs. Those changes only remove material and leave every joint axis unchanged; the recorded restrictions are retained conservatively. No wider motion range is claimed from the reliefs.

## Motion restrictions still requiring engineering and physical checks

Contact occurred at **neck pitch 36.7°, 50.8°, 65° with the other joints at zero**, and **head pitch +45° with the other joints at zero**. Do not use these poses. The coordinated head samples are listed in `reports/sampled_poses.json`; a few successful samples do not establish a continuous safe range. Do not interpolate arbitrary combinations or use the stock joint limits as certified limits.

The screen checks moving geometry against the new torso/electronics. It does **not** certify collisions within the inherited mechanism, wires, plugs, screw heads, all combined poses, torque margin, cooling, printed strength or walking stability. No physical print or powered test has been performed.

## Hardware dimensions needed to freeze the design

| Item | Required information | Current treatment |
|---|---|---|
| BK 4200 mAh 3S battery | Actual length, width, thickness including wrap; lead exit; mass | Reserved 136 × 52 × 42 mm volume, removable sled; connector bend clearance unconfirmed |
| Switch | Model and cutout, body depth, tabs and terminals | Removable blank plate; switch cannot yet be fitted as supplied |
| Fuse holder, PDB, UBEC, servo adapter | Actual board/body outlines, mounting pattern and connectors | Separate nominal reserved spaces; straps and removable power rack |
| WS2812 eye rings | OD, ID, PCB thickness, LED height, solder/wire exit | Two removable nominal 44 mm ring mounts; spacer revision pending |
| M3 × 4 mm inserts | Outside diameter plus a successful printed coupon | 4 mm nominal pilot, 4.5 mm depth; actual bore calibration pending |
| ST3215 kit | Case/horn/connector fit in coupons and one assembled joint | Full vendor CAD placed in assembly; physical horn stack check pending |

## Inventory coverage

Installed in the candidate: 14 servos, Pi 4B, one SEN0374 IMU, battery, one adapter, PDB, UBEC, fuse holder position, switch panel, three bearings, four KW10 switches and two eye rings.

The fourth bearing, two extra KW10 switches and third ring are spares. The purchased 4×4 LED matrix and bare WS2812 pixel have **no assigned mount in this revision**. If they are intended robot features, their placement and dimensions must be specified before calling the hardware packaging complete.

The fastener CSV covers the new mounts only. The inherited core fastener count and total insert consumption are not yet reconciled; 100 owned inserts must not be treated as a verified sufficient quantity. PETG is specified for structural prints and TPU for soles; rigid PETG is not a substitute for the compliant sole in the foot-contact mechanism.

## Files

Use `reports/print_manifest.csv` as the active parts list. The fit-review ZIP contains exactly those STLs, these instructions and the reports. It excludes obsolete exports. Native SolidWorks import completeness is recorded separately in `reports/solidworks_assembly.json` when that operation succeeds.
