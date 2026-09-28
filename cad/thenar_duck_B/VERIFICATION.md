# Verification — revision B

## Completed digital checks

- **P1S print release:** 19 native Bambu Studio plates, 94 colored objects including coupons and alternatives. All plates sliced successfully; a TPU orientation warning was corrected and its plate re-sliced. Native scale, membership and color checks passed, and deposited model/support/brim paths fit the stock bed and clear the cutter area. See [release evidence](bambu/RELEASE_CHECKS.md). No physical printing was performed.
- **91 STL files:** 79 installed-part files, 6 alternative files and 6 fit coupons. All are watertight, positive-volume meshes and fit a 256 mm cube. This checks the bounding envelope, not supports or slicing quality.
- Generator checks valid BREP and one connected solid per printed part. Tessellation is performed on independent copies to preserve imported head topology. Only sub-0.01 mm triangulation seams may be closed by the export repair routine.
- Exact checks found no overlap between the new torso parts and the modelled component envelopes in neutral.
- The full 140 × 50 × 32 mm battery capacity box, above the 2 mm pad, also clears the exported solid geometry in neutral; this goes beyond checking the smaller nominal battery example.
- Separate head/eye solid check: 10 candidate pairs, no overlaps above 0.1 mm³ after subtractive reliefs at the retainer corners. These reliefs only remove material; the earlier motion/servo checks remain conservative for the released caps.
- **64 candidate servo/print pairs** checked with vendor solid geometry in neutral: no intersections exceeding 0.1 mm³. Core mating reliefs are retained from A; this is not a connector insertion or manufacturing-tolerance proof.
- Battery, Pi tray and sensor removal checks found no overlaps at **20 sampled positions**. Covers and cables must be removed first as stated in ASSEMBLY.md. Fixed core/head and flexible wires were excluded from these torso-only service tests.
- Motion screen: **124 poses**, **122 with no detected contact**, **2 with detected contact**. Scope is moving assemblies against the new torso/electronics.
- Native SolidWorks: 123 components; missing: []. Assembly is static and imported, not fully mated or supplied with original native feature history.

## Movement restrictions

Detected contact poses: **`neck_pitch_50.8`; `neck_pitch_65.0`**. Do not command these poses. The exact angles and colliding part names are in `reports/motion_screen.json`. Tested coordinated head poses and crouches are in `reports/sampled_poses.json`.

Passing separate samples does not establish a continuous safe range or arbitrary simultaneous movement. The inherited mechanism's self-collision, flexible wires, plugged cable bends, screw heads, tool reach, structural strength, actuator torque, temperatures and walking balance have not been certified. No physical print or powered test has been performed.

## Dimensional basis and limits

Pi and SEN0374 mounting patterns come from manufacturer drawings. Battery reference is BONKA's 137 × 44 × 27 mm BK-4200/35-3S; the specific user pack's label was not available. Mount capacity is 140 × 50 × 32 with additional pad and lead space. PDB slots, UBEC ties, switch lids, LED sleeves and removable matrix carrier accommodate the stated ranges; these do not imply every product variant fits.

The new sensor bracket provides real mounting holes and plug space. M3 insert pilots still require a printer fit coupon because “M3 × 4” does not identify knurl outside diameter or printed shrinkage. Bearings, servo horns and foot switches likewise need first-assembly fitting/calibration.

## Inventory coverage

All components identified in the cart have an installed position or spare role. Four of six KW10s, two of three eye rings and three of four 6804 bearings are installed. The bare 2020 pixel requires an additional small solder carrier. The main switch, fuse holder and servo adapter are model assumptions or capacity-based mounts as disclosed in SOURCES.md.

The custom-part fastener count is derived from actual designed joints. The reference servo mechanism's complete fastener/insert count remains unspecified by its guide; the tables do not claim that 100 inserts covers the entire robot. Flexible soles, straps, insulation, wire, suitable connectors and small adhesive pads are separate assembly materials.
