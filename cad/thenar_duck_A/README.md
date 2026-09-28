# Thenar Duck — revision A, fit review

**This is an assembly candidate, not an approved full-print release.** The battery, power parts, insert outside diameter, and LED ring still need physical dimensions. The final torso motion screen found contact in four of 124 sampled poses; use `VERIFICATION.md` and the reports, not the upstream angle limits as a promise of clearance.

## Open these first

- `renders/01_assembled.png`: closed robot.
- `VERIFICATION.md`: checks completed, unresolved dimensions, motion restrictions and hardware coverage.
- `Thenar_Duck_A_FIT_REVIEW_PRINTS.zip`: manifest-selected print files, fit coupons, instructions and reports. This is not a full-print approval.
- `renders/02_covers_removed.png`: internal layout.
- `renders/03_electronics_access.png`: battery, Pi 4B, power rack, and torso-fixed DFRobot IMU.
- `Thenar_Duck_A_FULL_ASSEMBLY.glb`: labelled review mesh including hardware.
- `Thenar_Duck_A_PRINTED_PARTS.step`: named printed parts in assembly coordinates (millimetres, Z up).
- `step/`: individual parts in assembly coordinates.
- `stl/`: individual print files, moved onto Z=0. Quantity and material are in `reports/print_manifest.csv`. Do not print every file in the directory indiscriminately: use the manifest; obsolete exports may remain during revision.
- `solidworks/`: imported native parts, and the review assembly if its import report says it saved successfully. These are imported solids, not a reconstructed SolidWorks feature history. Native placement is static, not a fully mated mechanism.

## What was designed for your hardware

The 14-servo mechanical chain is derived from the pinned Open Duck Mini v2 source. Its 78.65 mm leg links, bearing stations, and main joint axes are retained. The torso shell and electronics mounts are new parametric parts.

| Hardware | Physical provision |
|---|---|
| Raspberry Pi **4B** | Correct asymmetric 85 × 56 mm PCB pattern, 58 × 49 mm hole spacing, 5 mm underside stand-offs, microSD access notch, open USB end, side I/O opening, removable tray |
| BK 4200 mAh 3S | Rear-removable sled, two strap passages, 2 mm pad allowance; **136 × 52 × 42 mm is reserved capacity, not a measurement of your pack** |
| DFRobot **SEN0374** BNO055 | Dedicated rigid bridge; correct 19 × 21 mm board and two Ø2 mm holes on one edge at 16 mm pitch; pin-header space; no M3 screw forced through an M2 hole |
| Waveshare Bus Servo Adapter (A) | 42 × 33 mm board position, 37 × 28 mm nominal hole grid; mounting revision still needs confirmation |
| PDB, UBEC, fuse holder | Separate strapped positions on a removable power deck; no conductive board underside directly against other boards |
| Main switch | Replaceable rear plate. It is deliberately a **blank** until the actual switch and locking tabs are measured |
| Four KW10-DZ2P075 switches | Top-loading, removable cassettes; 3 mm height adjustment; captive ground plungers; lift-off wire covers |
| Two WS2812 rings | Rear-loading eye sockets, removable retainers and spacers, front diffuser lip; actual PCB and LED stack dimensions still required |
| 6804 bearings | Three reference bearing locations; separate 32.0/32.1/32.2 mm fit coupons |
| M3 × 4 mm inserts | New sockets use 4.5 mm pilot depth. Pilot diameter is a parameter; confirm with the actual inserts before committing all prints |

The AS5600 from your previous project is **not** a component of this robot. The current BNO055 has an explicit mount and removal sequence.

## Build and revise

Source of truth: `../../design/spec.json` and `../build_duck.py`. Run from the project root:

```powershell
.venv-cad\Scripts\python.exe cad\build_duck.py
.venv-cad\Scripts\python.exe cad\check_custom_fit.py
.venv-cad\Scripts\python.exe cad\check_service_paths.py
.venv-cad\Scripts\python.exe cad\check_motion.py
```

The generator checks BREP validity, single-solid printed parts, print envelope, and exported STL watertightness. The motion screen is sampled, not an exhaustive continuous collision proof. Flexible wires, real plug bends, manufacturing tolerances, thermal performance, strength, and walking stability require physical validation.

**A 3S pack and 12 V servos change the actuator model and mass distribution. The stock Open Duck walking policy is not validated for this assembly.**

## Before a full print

1. Measure the battery including wrap and lead exit, and provide its mass. Confirm it fits the reserved envelope without squeezing it.
2. Confirm the final adapter, switch, PDB, UBEC and fuse holder models, outlines, connectors, and mounting tabs. Finish the small switch plate.
3. Measure the LED ring OD/ID, PCB thickness, LED height and wire exit. Set the eye spacer length from that stack.
4. Print the M3 insert, bearing, servo-case and horn-pattern coupons. Test the actual hardware. Print one foot-switch cassette and plunger to set operating height and verify return without sticking.
5. Slice structural parts, check support removal and estimated masses. Print one leg first, assemble with a cable plugged in, and check the full intended movement before duplicating it.
6. Review `reports/motion_screen.json` and resolve/restrict colliding poses. A pass on individual joints or a few crouches does not prove all simultaneous combinations clear.

See `ASSEMBLY.md` for the insertion and service sequence. See `reports/fasteners_custom_parts.csv` for screw lengths derived from the new-part stacks; that CSV is **not** the complete inherited servo/core fastener count.

## Provenance

Open Duck Mini v2, commit `b23317a485b3cec7d8417f352478778b3475173c`, Apache-2.0. Retained reference STLs are converted to sewn faceted BREP, with the original source and licence kept in `../reference_open_duck/`. New changes include the complete torso package, Pi/IMU trays, split head underside, eye sockets, foot-contact carriers, and clearance changes. Waveshare/Feetech vendor CAD is hardware reference geometry; it has no explicit redistribution licence stated. Official Pi and DFRobot drawings are stored in `../vendor/electronics/`.

Sources: [Open Duck](https://github.com/apirrone/Open_Duck_Mini/tree/b23317a485b3cec7d8417f352478778b3475173c), [Pi 4B drawing](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf), [DFRobot SEN0374](https://wiki.dfrobot.com/sen0374), [Daier KW10 catalogue](https://www.chinadaier.com/wp-content/uploads/2017/08/Micro-switch.pdf).
