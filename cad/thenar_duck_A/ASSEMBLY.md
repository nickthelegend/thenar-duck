# Assembly and service sequence

Do not install hardware in an order that closes off its fasteners. All positions use X forward, Y left, Z up.

## 1. First fit samples

- C01: insert pilots 3.8, 3.9, 4.0, 4.1, 4.2 mm; clearance row 3.2 through 3.6 mm. Put the actual 4 mm-long insert flush in the successful bore; do not drive it to the bottom of a deeper hole. Change `design/spec.json` before rebuilding if needed.
- C02: three 6804 OD-fit rings. The bearing should seat without splitting the print. Do not heat the bearing to force a bad fit.
- C03: servo-case opening 45.72 × 25.22 mm. Check the actual case can pass through.
- C04: servo-horn four-hole pattern on a 14 mm pitch circle. Check the supplied horn and screw length. Vendor model horn stack differs slightly from the upstream reference; use the real unit for final seating.
- A15/A17: one KW10 carrier and ground plunger. Confirm the switch matches the catalogue and returns freely after actuation.

## 2. Mechanical core

Use the pinned `../reference_open_duck/assembly_guide.md` for servo orientation and the retained link assemblies. Skip its old battery, Pi Zero, IMU, electronics, and outer-body steps.

1. Set every servo ID and centre it individually before placing horns. IDs: right leg 10–14, left leg 20–24, neck/head 30–33. Do not power fourteen default-ID-1 units and expect unique addressing.
2. Install the two hip bearings and trunk inserts, then join trunk_bottom and trunk_top with the reference two M3×10 screws.
3. Fit servo-case screws from the supplied kit in the appropriate body holes. Fit and inspect the 5264 cable **before** closing the opposite cheek plate; some inherited brackets require this order.
4. Assemble shins/thighs, feet and hips. Preserve the reverse-knee orientation.
5. Install the neck and head mechanism. Fit the head's third 6804 bearing before closing the head. The revised left/right underside panels are installed last and can leave sideways rather than being trapped around the neck.

Only the new custom-part fasteners are counted in the generated fastener table. The inherited guide does not publish every screw count; supplied servo kits and the four-insert leg spacers still need reconciliation. Do not interpret “100 inserts owned” as a verified final consumption count.

## 3. Feet with KW10 contacts

1. Heat-set the two cassette mounting inserts per carrier in the revised rigid foot plate. Fit the original sole inserts separately.
2. Solder and insulate the switch leads outside the robot. Mount each switch inverted inside its open A15 carrier, with two M2×14 bolts and nuts through the vertical slots. Leave adjustment loose initially.
3. Insert A17 plungers from below. The 8 mm collar enters the top recess in the TPU sole; the 4 mm stem passes through the guide. The 0.5 mm unloaded protrusion and 1.25 mm maximum stroke are nominal CAD values, not calibrated switching distances.
4. Fit the sole. Adjust each switch vertically with a continuity meter: off when lifted, on as the foot contacts the ground, and reliably off on release. The rigid stop and sole must carry foot load; do not use the switch lever as a load-bearing stop.
5. Tighten the M2 mounting bolts gently. Route wires through the cover slot, fit the cover with its two M3 screws, and secure a flexible loop up the leg.

## 4. Torso chassis and battery

1. Attach A01 upward into the original four trunk-bottom inserts with M3×6 screws (3 mm plate; no washer for this stack).
2. Fit the two side frames to the six chassis sockets with M3×8 and 0.5 mm washers. Their large lower openings are hip clearance windows, not missing panels.
3. Fit the battery sled with four M3×8 and washers. Thread two 20 mm hook-and-loop straps before placing the battery. Use a thin nonabrasive 2 mm pad; do not tighten straps enough to deform the pack.
4. Confirm lead and balance-connector reach before installing the power deck. Keep the battery fuse near the battery positive lead, with its holder secured and accessible. Fit electrical ratings to the measured current and wire, not to CAD dimensions.

## 5. Power rack and Pi

1. On the bench, mount the servo adapter to its four stand-offs using M2.5 hardware. Secure the PDB, UBEC and fuse holder to their separate reserved areas using insulated supports/straps. The reserved boxes in the model are maximum packaging volumes, not exact models of unconfirmed products.
2. Keep PDB solder joints clear of the deck and other boards. Terminate and insulate power leads before lowering the rack into the body.
3. Mount the IMU PCB to its bridge on the bench using two M2×10 screws and nuts. Fit the bridge to the rack with two M3×10 through bolts and nuts; the rack is rigidly fixed to the chassis in operation. Solder headers before installation.
4. Lower the power rack through the open top and attach it to four side-frame ledges with M3×8 plus washers. The battery remains removable toward the rear.
5. On the bench, attach the Pi 4B to A10 using four M2.5×12 screws and nuts. There are no M2.5 heat-set inserts in this tray. Verify the card and underside components clear the 5 mm stand-offs.
6. Connect suitably short USB leads, place the tray on the four pillars, and secure it with M3×8 plus washers. Confirm all connectors fully latch; a cable that needs more room must be measured and the local clearance changed.
7. Check polarity and regulated output with a meter before connecting the Pi. A 3S battery must never feed the Pi directly. The adapter's signal bus and power-distribution wiring are separate design concerns; do not send the combined fourteen-servo load through the small adapter board.

## 6. Eyes and covers

1. With the head underside open, insert the diffuser from behind until it reaches the front lip. Install the actual LED ring, then the corrected-length spacer and rear retainer. Confirm the retainer supports the PCB without crushing LEDs or soldered leads.
2. Route the eye wiring through the rear-retainer notch. Leave accessible connectors before routing through the neck. Check a slack loop through all intended head poses; do not assume the upstream ±160° yaw range is cable-safe.
3. Close the split underside covers. Fit torso side covers, front panel, rear panel, and roof only after checking connectors and screw reach.
4. The switch blank must be replaced with a measured cutout before an electrical switch can be installed. Do not drill it from a guessed product name.

## Removal paths checked in CAD

| Module | Remove/disconnect first | Path |
|---|---|---|
| Battery | Battery connector, rear panel, straps | Straight toward the rear; the power rack and Pi can stay installed |
| Pi tray | Roof, cables, four tray screws | Lift about 45 mm, then move rearward |
| IMU bridge | Roof, Pi tray, sensor wires, two bridge bolts | Lift 35 mm, slide 80 mm rearward, then lift out; dragging it rearward at its installed height hits the UBEC/fuse volumes |
| Power rack | Roof, Pi tray, IMU bridge, power/data connectors, four rack screws | Lift clear of the side-frame ledges, then withdraw rearward before approaching the head |
| LED ring | Split head underside, rear eye retainer | Withdraw toward the rear of the head |
| Foot switch | Two cover screws, switch cable connector, two M2 screws | Lift out of its carrier; no need to cut a sealed shell |

These are rigid-part checks. Actual leads, plug bodies and bend radii still have to be checked with your purchased hardware.
