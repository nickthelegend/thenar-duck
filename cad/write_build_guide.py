"""Assemble the user build manual from the maintained revision-B records."""
from pathlib import Path
import json,collections
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'cad/thenar_duck_B';P=B/'bambu'
manifest=json.loads((P/'plate_manifest.json').read_text())
plates=collections.defaultdict(list)
for p in manifest:plates[p['plate']].append(p)
header='''# Thenar Duck — complete build guide, revision B

A 14-servo duck with a Raspberry Pi 4B, a 3S battery, a separately mounted DFRobot SEN0374 BNO055, removable electronics trays and serviceable lights. Prepared for your **Bambu Lab P1S, standard 0.4 mm nozzle and AMS**.

**Start with the fit-test plate.** This is a digitally checked prototype. The files have not been physically printed, assembled or tested walking. Published component dimensions and adjustable mount capacities are distinguished below; CAD clearance does not prove the fit of an unidentified hardware variant.

## 1. Files to open

| File | Purpose |
|---|---|
| [All-parts Bambu Studio project](cad/thenar_duck_B/bambu/Thenar_Duck_B_P1S_ALL_PARTS.3mf) | Full-size, named, colored parts on 19 P1S plates. Open **as a project**, retaining settings and plate arrangement. |
| [Plate overview](cad/thenar_duck_B/bambu/plate_overview.png) | Color/material and plate selection map. |
| [Plate inventory](cad/thenar_duck_B/bambu/plate_manifest.csv) | Each object's plate, quantity instance, material, orientation and source STL. |
| [Individual STL pack](cad/thenar_duck_B/Thenar_Duck_B_PRINTS.zip) | Separate meshes and original revision-B documentation. |
| [Assembly review](cad/thenar_duck_B/Thenar_Duck_B_FULL_ASSEMBLY.glb) | Colored assembled model, including non-printable hardware envelopes. |
| [Printed-parts STEP](cad/thenar_duck_B/Thenar_Duck_B_PRINTED_PARTS.step) | Imported solids in assembly coordinates. |
| [SolidWorks review assembly](cad/thenar_duck_B/solidworks/Thenar_Duck_B_REVIEW.SLDASM) | Keep its neighboring SLDPRT files together; a fixed review assembly. |
| [Service layout](cad/thenar_duck_B/renders/04_service_layout.png) | Board positions, insertion/removal access. |

The 3MF contains **94 print objects**: **79 installed pieces**, **6 fit coupons**, and **9 optional replacement pieces**. There are 91 distinct STL files; each alternative eye sleeve appears twice. Hardware models such as the Pi, battery, bearings and servos are excluded from the print project. Do not print all optional variants for one robot.

Revision B is the build reference. Revision A and the older research documents retain historical alternatives; they do not override this guide.

## 2. P1S printing and colors

### Open and select material

1. Open the all-parts `.3mf` using Bambu Studio's project-open option. Do not import it as one merged model. The project was normalized with Bambu Studio **2.8.2.61**.
2. Confirm **Bambu Lab P1S / 0.4 mm nozzle**. All models are at **100% scale in millimetres**. Do not scale a part to fix a hardware-fit problem.
3. The saved build surface is **Textured PEI Plate**. Select your actual plate if different, then re-slice; the plate profile affects adhesion and first-layer behavior.
4. Replace the generic filament presets with the actual spool's suitable PETG/TPU profile and retain the intended object color assignments. Run flow calibration and the fit coupons with those same spools. Follow the spool manufacturer's drying instructions.
5. Map the four PETG project colors to your AMS slots when preparing each PETG plate. The project numbers are virtual material roles, not an assertion about what is currently loaded in your AMS.
6. Print the TPU sole plate with **ordinary TPU from the external spool and AMS disabled for that job**. Virtual filament 5 is not a fifth AMS slot. A specifically AMS-compatible TPU grade requires its own supported profile and a fresh slice.

| Project filament | Color | Use | Feed |
|---|---|---|---|
| 1 | White PETG | Main shells and selected exterior parts | AMS |
| 2 | Dark grey PETG | Internal structure and mechanism parts | AMS |
| 3 | Blue PETG | Accents, selected mounts and test coupons | AMS |
| 4 | Translucent PETG | Two eyes, chest diffuser and status lightpipe | AMS |
| 5 | Black TPU | Two compliant soles | External spool |

Each plate contains one material/color. The assembled robot gets its colors from separate pieces, so no mid-layer color changes or prime tower are needed in this layout. The translucent appearance in CAD is illustrative; printed PETG is a diffuser, not guaranteed optically clear plastic.

### Saved process

| Setting | Structural PETG | Diffusers/lightpipe | TPU soles |
|---|---|---|---|
| Layer height | 0.20 mm | 0.20 mm | 0.20 mm |
| Walls | 4 | 3 | 3 |
| Top/bottom layers | 5 / 5 | 5 / 5 | 5 / 5 |
| Infill | 30% gyroid | 100% rectilinear | 20% gyroid |
| Supports | Automatic tree, build plate only, 30° threshold | Off | Off |
| Brim | 4 mm outer, 0.15 mm gap | 4 mm outer | Off |
| Flow limit | 8 mm³/s | 5 mm³/s | 3 mm³/s |

Coupon and optional-variant supports are off. Structural outer/inner walls are limited to 60/90 mm/s; sole walls and infill to 30 mm/s. Generic temperatures are starting presets, not a calibration of your filament. Inspect the newly sliced preview after any profile change, especially support contact, small bearing seats, insert holes and the first layer.

Models and their reserved brim margins fit inside the stock P1S bed. The stock **18 × 28 mm front-left cutter exclusion** is preserved, and the layout reserves the entire front 34 mm band. The default 250 mm height limit is retained. No printer hardware modification or extended-volume override is used.

The head prints roof-down with its open underside accessible. Hip covers print on their broad closed side. TPU soles print flat mounting face down and curved ground-contact face up. Other parts retain the CAD print orientations. Remove support remnants from mating faces, insert pilots, bearing seats and connector openings before assembly; do not force hardware into a supported cavity.

### Plate order

Print plate 1 first. Then make one foot-switch cassette/plunger and check its actual switch action before printing all four. The installed pieces occupy plates 2–17; plates 18–19 hold alternatives. If a replacement is selected, disable the corresponding default object before printing its plate. Keep mirrored left/right names distinct.

| Plate | Material / purpose | Objects |
|---:|---|---:|
'''
for n,items in plates.items():header+=f"| {n} | {items[0]['plate_name']} | {len(items)} |\n"
header+='''
**Fit-test acceptance:** the real insert seats flush without splitting the coupon; the screw engages without bottoming; the bearing seats without distorting its races; the servo case and horn pattern align; and the foot switch makes/releases with a freely returning plunger. The new insert pilots default to Ø4.0 × 4.5 mm deep. Your M3 × 4 insert listing gives thread and length, not knurl outside diameter. Adjust the relevant CAD fit parameter if the coupon fails, then regenerate the affected parts and re-slice. Keep global model scale at 100%.

## 3. Hardware and fasteners

'''
bom=(B/'BOM.md').read_text(encoding='utf-8').split('\n',1)[1]
bom=bom.replace('## ','### ').replace('`reports/fasteners_custom_parts.csv`','[joint-by-joint fastener table](cad/thenar_duck_B/reports/fasteners_custom_parts.csv)')
header+=bom+'''

### Tools and consumables

Have a soldering iron and suitable heat-set tip, hex drivers, small screwdrivers, cutters, wire stripper, crimping tools for the chosen connectors, heat-shrink, a multimeter, and a 3S-compatible LiPo balance charger. A current-limited bench supply helps with first electrical tests. Use the supplied servo screws only in their intended case/horn locations; a visually similar screw may have a different thread or depth. Threadlocker is for compatible metal-to-metal joints; keep it off plastic and electronics.

An **M3 × 8 mm screw** has a 3 mm nominal thread diameter and 8 mm length below the head. A normal M3 nut is bought by its thread size; it does not need to be 8 mm long. At an insert joint the brass insert is already the nut. Washer thickness changes usable screw engagement, which is why the 1 mm and 0.5 mm stacks are listed separately.

## 4. Assembly, insertion and service

Keep the battery disconnected during assembly. Install connectors and wires while each tray is accessible. Use the [labelled service layout](cad/thenar_duck_B/renders/04_service_layout.png) beside this sequence.

'''
assembly=(B/'ASSEMBLY.md').read_text(encoding='utf-8').split('\n',1)[1]
assembly='\n'.join('#'+line if line.startswith('#') else line for line in assembly.splitlines())
assembly=assembly.replace('`../reference_open_duck/assembly_guide.md`','[pinned illustrated mechanism guide](cad/reference_open_duck/assembly_guide.md)').replace('`VERIFICATION.md`','[verification record](cad/thenar_duck_B/VERIFICATION.md)')
header+=assembly
footer='''

## 5. Power and signal connections

This section gives the connection architecture and bench sequence. Exact fuse, switch, wire and connector ratings remain dependent on the purchased models and measured loads; the cart screenshots do not establish them. Do not treat a mechanical fit check as approval of the full-current harness.

### Power path

```text
Battery + (3S)
   |
   +-- fuse close to battery -- DC-rated main switch -- PDB raw battery bus
                                                        |
                                                        +-- rated servo power branches
                                                        |      -> 12 V-variant servos
                                                        |
                                                        +-- UBEC set to 5 V
                                                        |      -> suitable Pi USB-C power lead
                                                        |      -> Raspberry Pi 4B
                                                        |
                                                        +-- separately sized 5 V LED supply
                                                               -> eyes / matrix / status pixel

Battery - ------------------- common power return / PDB ground
                               -> servo / regulator / logic grounds
```

The LED branch is a proposed supply provision, not an extra regulator already verified in the existing CAD. If adding a regulator, its mount and cooling need checking. Sharing a 5 V rail is possible only after verifying its combined current capacity, transient response and wiring. Do not connect the outputs of two regulators together.

The **fuse** opens the supply during an excessive-current fault, protecting the wiring. Put it near battery positive so most of the harness is downstream of it. The **main switch** disconnects the load; its DC rating must cover this circuit. The **PDB** distributes power. Its raw battery pads do not turn 3S voltage into 5 V. Keep servo-current returns out of thin Pi/sensor leads.

A conventional 3S LiPo is nominally 11.1 V and reaches 12.6 V full. Direct servo supply is conditional on the actual servos being the specified **12 V variant with a compatible maximum voltage**. Never connect this battery to the Pi or WS2812 boards. Verify component labels and polarity before connecting them.

Use the ReadyToSky UBEC's **5 V setting**, and measure its output while the Pi is disconnected. Its manufacturer specifies 4–6S input for 12 V output mode. The Pi 4B has a 5 V / 3 A power requirement; a nominal 3 A regulator has no established full-load margin for the Pi plus all LEDs. Use a suitable USB-C power cable, and verify voltage at the Pi under load. Avoid powering the Pi simultaneously from the UBEC and another supply. Sources: [ReadyToSky UBEC](https://www.readytosky.com/e_productshow/?951-Readytosky-2-6S-5V3A-and-12V3A-Switchable-UBEC-951.html=), [Raspberry Pi hardware documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html).

Size the battery harness from its worst expected load and the weakest wire/connector/switch/PDB rating. Select the fuse using its time-current curve and the protected wire's capacity; a larger fuse is not a fix for nuisance trips. The 4200 mAh capacity describes stored charge, not safe current delivery. The pack's discharge rating and the full servo load budget are still required. No fuse amp rating is invented in this guide.

### Servo communications

Use **Waveshare Bus Servo Adapter (A)**, not the small 7.2 V buck regulator. For the Pi 4B, use its USB connection and set the adapter's control jumper to **B**. The adapter also needs a servo-matched external supply. Use the labeled servo-bus connectors and matching cables; ordinary three-pin PWM extensions from the cart are not assumed mechanically or electrically compatible. Follow [Waveshare's USB wiring example](https://docs.waveshare.com/Bus_Servo_Adapter_A/Product-Wiring-Example).

Do not infer that the adapter's small power terminals or one daisy-chain cable can carry all fourteen servos' combined current. Supply rated power branches from distribution while maintaining the required common signal reference. The exact branch harness is an electrical design item to settle before all-servo loading.

### BNO055 and foot switches

Proposed Pi header wiring for the selected **DFRobot SEN0374**, using 3.3 V logic:

| Pi 4B physical pin | Signal | SEN0374 label |
|---:|---|---|
| 1 | 3.3 V | VCC |
| 6 | Ground | GND |
| 3 | GPIO2 / SDA1 | SDA |
| 5 | GPIO3 / SCL1 | SCL |

Leave the board in its default I²C mode, address 0x28; enable I²C in the Pi software. Check pin numbers against the header orientation before connecting. The sensor mount rotates the board 90° in plan: verify robot-axis signs and configure the sensor-to-body transform before using attitude feedback. Sources: [SEN0374 pinout](https://wiki.dfrobot.com/sen0374), [Pi GPIO documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio).

Each foot switch is a dry contact: COM to logic ground, NO to its selected GPIO input with a 3.3 V pull-up. A suggested allocation is left toe GPIO17 (pin 11), left heel GPIO27 (pin 13), right toe GPIO22 (pin 15), right heel GPIO23 (pin 16). These are **proposed assignments**, not an implemented firmware configuration. Add software debounce and confirm all four channels separately. Apply no battery or 5 V power to these GPIO inputs.

### Lighting

Feed the WS2812 boards from a correctly sized regulated 5 V rail and common ground. Signal enters **DIN** and leaves **DOUT**. Use a suitable 3.3 V-to-5 V logic buffer for reliable Pi control, together with the LED manufacturer's decoupling and data-line recommendations. The exact buffer/carrier and GPIO driver are not supplied as a tested electronics design here. Start with limited brightness and confirm current before increasing it. Power wires must bypass the Pi GPIO header. The bare WS2812B-2020 needs the additional small carrier described in the assembly section.

## 6. Bring-up: from loose parts to a supported robot

1. **Unpowered inspection:** inspect insulation, screw lengths, insert seating, bearing freedom, plug polarity and connector strain relief. Check the main switch actually interrupts the load. Inspect for shorts; allow for capacitor charging when interpreting a meter.
2. **Power board only:** use a suitably current-limited supply for the first bench test. Verify raw and regulated voltages with the Pi, LEDs and servos unplugged. Fit the correctly selected fuse before using the battery.
3. **Pi and sensor:** boot from a prepared microSD with Raspberry Pi OS using a known suitable Pi supply first. Enable I²C, confirm the sensor address, and verify attitude responses by gently tilting the rigid mount. This workspace does not contain a validated production controller image for revision B.
4. **One servo at a time:** with the horn unloaded, use the adapter manufacturer's setup tools to read its identity, voltage and feedback; assign a unique ID, set position mode, and establish its center. Reference groups are right leg 10–14, left leg 20–24 and neck/head 30–33. Label each physical servo. Do not power a group of duplicate default IDs for configuration.
5. **Fit horns at the intended neutral pose:** follow the pinned mechanism guide for each joint orientation. Record each joint's ID, zero offset and sign. Recheck its mounting screws and free cable loop.
6. **Foot contacts and lights:** observe one switch at a time and verify release with no foot load. Test each LED board at low brightness before installing its diffuser.
7. **Supported single-joint tests:** keep the robot supported above the bench; enable one actuator at limited speed/current where supported. Verify direction and feedback, then check conservative motion limits and cable slack. Do not start by broadcasting large moves to all joints.
8. **Supported groups:** verify stable Pi power during servo motion, connector temperatures, sensor readings and stop behavior. Configure torque-disable on communication loss, startup motion prevention and a reachable hardware power cutoff before gait work. A sudden main-switch cutoff also cuts Pi power; shut down Linux first during normal servicing.
9. **Standing and walking:** revise the mass/inertia model and controller for the Pi 4B, large battery and new enclosure, then validate in simulation and restrained trials. The upstream walking policy is not certified for this heavier arrangement. Existing research and simulation smoke tests are not proof that this robot will balance.

The motion screen detected contact at **neck pitch 50.8° and 65° with head pitch at zero**. These failed samples are excluded. Passing 122 other samples is not a continuous joint-limit specification. Start from neutral and establish conservative physical limits; do not interpret the nearest passing sample as a guaranteed boundary.

Charge the removable battery with a charger configured for its actual 3S chemistry and balance connector, following its maker's instructions. Disconnect it from the robot for charging and servicing. The model provides a removable battery sled; it does not provide a charger or low-voltage protection circuit.

## 7. Verification and known limits

| Check | Evidence and scope |
|---|---|
| Printable meshes | 91 distinct STLs, watertight and positive volume; 94 placed instances including alternatives. |
| P1S arrangement | [Placement report](cad/thenar_duck_B/bambu/placement_validation.json): full scale, stock cutter area, non-overlapping padded footprints. |
| Native project and slicing | [Bambu Studio result](cad/thenar_duck_B/bambu/validation/result.json); [release verification](cad/thenar_duck_B/bambu/RELEASE_CHECKS.md). |
| Servo fit | 64 candidate vendor-servo/printed-solid pairs checked in neutral; no intersections above 0.1 mm³. |
| Eyes | 10 candidate pairs checked; no intersections above 0.1 mm³. |
| Battery capacity | Full 140 × 50 × 32 mm allowance plus 2 mm pad checked in neutral. Battery identity remains an assumption. |
| Service paths | 20 sampled battery/Pi/IMU removal positions clear of tested torso geometry; core/head and flexible wiring excluded. |
| Motion | 124 poses screened, 122 clear, 2 detected contacts as noted above. |
| Native review | 123 SolidWorks components, no missing components in the export. |

These checks do not establish physical fit tolerances, continuous collision-free travel, driver/tool access at every fastener, structural strength, walking stability or electrical current capacity. The [detailed verification record](cad/thenar_duck_B/VERIFICATION.md) and [dimensional sources](cad/thenar_duck_B/SOURCES.md) explain what was modeled. In particular, xcluma PDB, UBEC, fuse holder, switch, LED PCB and the exact BK battery variant are accommodated by the stated capacities rather than claimed physical measurements.

## 8. Editing and rebuilding

Edit [design/spec_B.json](design/spec_B.json) and the relevant generators. Current CAD uses CadQuery 2.8, trimesh 5.1, NumPy, Pillow and VTK in `.venv-cad`; SolidWorks export also requires the installed SolidWorks application and pywin32. The retained core is revision A's modified upstream geometry.

```powershell
# From the project root; regeneration overwrites generated revision-B outputs.
.venv-cad/Scripts/python.exe cad/build_duck_B.py
.venv-cad/Scripts/python.exe cad/check_B_packaging.py
.venv-cad/Scripts/python.exe cad/check_B_eyes.py
.venv-cad/Scripts/python.exe cad/check_B_battery_capacity.py
.venv-cad/Scripts/python.exe cad/check_motion.py --revision-b
.venv-cad/Scripts/python.exe cad/check_servo_fit.py --revision-b
.venv-cad/Scripts/python.exe cad/finalize_B.py
.venv-cad/Scripts/python.exe cad/build_p1s_project.py
.venv-cad/Scripts/python.exe cad/validate_p1s_project.py
.venv-cad/Scripts/python.exe cad/audit_p1s_release.py
.venv-cad/Scripts/python.exe cad/write_build_guide.py
# Optional native CAD review export:
py cad/export_solidworks.py --revision-b
```

The Bambu generator resolves installed P1S/process/filament profiles and uses the saved normalized native settings in `cad/development/p1s_native_settings.json` as its schema baseline. Its Bambu installation path is near the top of the scripts; update that path on another computer. The delivered 3MF already embeds its settings and does not require running the generators. Local slice checks write temporary G-code under `bambu/validation`; those files are evidence, not the user print deliverable. Re-slice the 3MF with the actual spools before printing.

Mechanical sources retain the pinned [Open Duck Mini commit](https://github.com/apirrone/Open_Duck_Mini/tree/b23317a485b3cec7d8417f352478778b3475173c) and its Apache-2.0 licence under `cad/reference_open_duck/`. Imported core solids do not recreate upstream feature history; the SolidWorks assembly is static. Manufacturer servo STEP geometry is a reference asset whose redistribution licence has not been established. The printable package excludes that hardware geometry.

## 9. Quick troubleshooting

| Symptom | First check |
|---|---|
| Studio opens one combined model or loses colors | Reopen the 3MF as a project and retain project settings. |
| An optional lid/sleeve seems duplicated | Select one switch lid and one matched pair of eye sleeves; optional plates are replacements. |
| Insert spins or splits the part | Stop and correct coupon/pilot fit and insertion process; global model scaling will break other interfaces. |
| Screw stops before clamping | Check under-head length, washer thickness and pilot bottom; never force it. |
| Servo case fits but cable cannot enter | Plug the cable before the cheek plate is closed; inspect the actual connector and loop. |
| Pi resets when a joint moves | Check its regulated voltage at the board, power-return layout and load transients. |
| IMU axes look wrong | Apply the mount's sensor-to-body rotation and verify signs with known physical tilts. |
| Foot switch stays triggered | Adjust cassette height; confirm free plunger return and that the rigid sole stop carries the load. |
| Neck touches torso | Return unpowered to neutral; inspect the documented failed poses and establish smaller limits. |

No print or robot motion is started by generating this package.
'''
(ROOT/'README.md').write_text(header+footer,encoding='utf-8')
print('Wrote README.md',len((header+footer).split()),'words')
