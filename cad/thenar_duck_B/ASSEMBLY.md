# Revision B — assembly and access

Coordinates: X forward, Y left, Z up. Lengths are under the screw head; use the fastener table for the stated washer stack. An M3 insert replaces the nut at that joint: do not add a separate nut behind it.

## 1. Establish printed fit

Print C01 insert/clearance coupon, C02 bearing coupons, C03 servo-case gauge and C04 horn-pattern gauge. Use the real purchased parts to choose fit before making repeated pieces. The new M3 insert pilots default to Ø4.0 and 4.5 deep for 4 mm-long inserts. Seat inserts flush, leaving the nominal 0.5 mm bottom allowance. The M3×8 insert joints use **1 mm washers**, giving 4 mm screw engagement; a thinner washer can bottom the screw.

Print one A15 foot-switch cassette and A17 plunger. Adjust the switch while observing continuity; the unloaded plunger must return freely. This is printer calibration and assembly validation, not a request for another dimension survey.

## 2. Retained servo mechanism

Use `../reference_open_duck/assembly_guide.md` for the retained trunk, feet, leg links and neck orientations (also bundled as `UPSTREAM_ASSEMBLY.md` in the print ZIP). Skip its obsolete Pi Zero, old battery/body, IMU and LED wiring instructions.

1. Assign unique servo IDs and centre each servo before fitting horns. Retained reference IDs are right leg 10–14, left leg 20–24 and neck/head 30–33.
2. Fit the two hip bearings and retained trunk inserts. Join the trunk halves with the reference two M3×10 screws.
3. Install the appropriate case and horn hardware from the servo kit. **Plug in the matching bus cable before closing the opposite cheek plate.** Ordinary PWM extension connectors are not assumed compatible.
4. Build one leg, then the other. Check the cable loop with the actual joint rotated by hand through the intended limited range.
5. Fit the head bearing and head mechanism. The revised head underside is split into left/right removable panels. Leave these off until the eye wiring is installed.

The inherited guide does not enumerate every screw. Its kit screws and retained insert count are not replaced by the custom-part fastener table. Vendor nominal mating reliefs are already included in the supplied core CAD.

## 3. Four foot contacts

1. Fit the original sole inserts and the two new cassette mounting inserts for each cassette.
2. Solder and insulate KW10 leads on the bench. Fit each switch inverted in its cassette with two M2×14 bolts/nuts through the height-adjustment slots.
3. Insert the captive ground plunger from below and fit the compliant sole. Nominal CAD protrusion is 0.5 mm and maximum travel 1.25 mm; set switch height for reliable make/release.
4. The sole and rigid stop must carry foot load, not the switch lever. Fit the A16 wire cover after the adjustment, then secure a flexible lead loop up the leg.

## 4. Chassis and battery

1. B01 bolts upward into four retained trunk-bottom inserts with M3×6, no washer for this 3 mm stack.
2. Bolt B02 side frames onto B01 with six M3×8 and 1 mm washers.
3. Install B08 sled with four M3×8 and 1 mm washers. Thread two 20 mm straps while the deck is accessible; place a 2 mm soft nonabrasive pad.
4. Place the battery lengthwise, leads toward the rear. Published reference is 137 × 44 × 27; designed pack capacity is 140 × 50 × 32. The separate rear tunnel holds the plugs and lead bend. Do not squeeze a larger pack into the sled.

## 5. Power rack and sensor

Assemble B09 on the bench before inserting it into the torso.

1. Place four B19 spacers below the PDB, align the four slots to its hole pitch and use four M3×12 through bolts, 0.5 mm washers and nuts. Insulate exposed solder joints. The 4 mm spacers must clear the actual underside.
2. Tie the UBEC to its saddle with insulating padding, within the 45 × 22 × 15 allowance. Keep the tie clear of components and adjustment controls.
3. Fit Waveshare Adapter (A) using four M2.5×12 and nuts. Its four standoffs match a 37 × 28 pattern.
4. Attach the SEN0374 to B11 with two M2×10 and nuts. Both mounting holes lie on the same PCB edge; the board is rotated 90° in plan. Install/solder headers outside the robot.
5. Bolt B11 onto B09 with two M3×10 through bolts, 0.5 mm washers and nuts. The board and plugs sit beside the Pi footprint, rather than under it.
6. Lower the rack into the side frames and use four M3×8 with 1 mm washers. The battery can still withdraw rearward after its cover and straps are released.

## 6. Pi tray

1. Fit the Pi onto B10's 5 mm standoffs using four M2.5×12 and ordinary nuts, with no extra washer in that screw stack. Check microSD insertion before installing the tray.
2. Connect suitable cables while the board is accessible. Reserve slack outside the moving neck. USB sockets face toward the open central space; side power/GPIO access is through the cover opening.
3. Lower the tray onto the four rack pillars; its side notch passes beside the IMU headers. Use four M3×8 with 1 mm washers.
4. For service, disconnect cables, remove roof and four tray screws, lift the tray 45 mm, then move it rearward. Keep the head in the neutral service pose. The IMU then lifts vertically after its two rack bolts are removed.

## 7. Rear switch/fuse pod

1. Use **one** lid: default B06b for a 19.4 × 13.2 rectangular opening, or C05 for 30.2 × 22.2, Ø12.2 or Ø20.2. Check the actual switch's latches and 3 mm panel tolerance against the chosen lid. Do not force a mismatched switch.
2. Fit the switch into the lid on the bench. Its terminals and insulated connectors must stay within the reserved 24 mm depth × 22 mm width × 30 mm height. The wider rectangular opening is an alternative cutout, not a guarantee of extra terminal space.
3. Strap the inline fuse holder into the lower pod, within 45 × 24 × 24. Route protected leads through the rear cover's 14 mm opening, with a grommet or rounded insulating sleeve. Leave removable connectors for service.
4. Attach the pod to B05 using four M3×10, no washer for the 7 mm flange. Fit the lid with four M3×8 and 1 mm washers.
5. Install B05 only after the battery connectors and fuse are accessible. Removing B05 takes the pod with it; unplug its leads before pulling the cover away.

## 8. Eyes, chest and status pixel

### Eyes

With the split head underside open, insert each diffuser from behind to the front lip. Choose one centering sleeve per eye: B13 for 45 mm PCBs, or two copies of the matching C06 alternative. The sleeve pocket adds radial clearance to the named PCB diameter. Fit the PCB at the front of the sleeve using thin removable insulating adhesive on bare back-edge areas, LEDs forward. The sleeve provides axial spacing; it must not bear on LED packages. Route wires through the lower notch, insert the sleeve from behind and fit B12 retainers with M3×6 and 0.5 mm washers. A short unplugging loop stays accessible behind each eye.

### Chest matrix

Fit the 30–40 mm square matrix PCB onto B21 with thin removable insulating adhesive at bare rear edges; its solder and component profile must clear the carrier. Insert the diffuser into B22's rear rebate, retain with small removable adhesive dots, and install the bezel. B21, B22 and B24 fasteners are M3×8 with 1 mm washers. The model's 30 mm PCB is a layout example, not a measured claim about the supplied matrix.

### Tiny status pixel

Solder the bare WS2812B-2020 to a small **10 × 10 mm carrier PCB** with insulated connections first. Fit this carrier in B24, align it behind B25 lightpipe and secure with removable insulating adhesive. This carrier is additional hardware. Keep its rear wiring away from the moving neck.

Finish by fitting side covers, front fascia, roof and split head underside. Access panels use the lengths and washers listed in the fastener CSV. A third eye ring, two KW10 switches and fourth bearing remain spares.

## Removal paths checked digitally

| Module | Remove/disconnect first | Path |
|---|---|---|
| Battery | Battery/pod leads, rear cover with pod, straps | Straight rearward; rack and Pi stay installed. |
| Pi tray | Roof, cables, four tray screws | Lift 45 mm, withdraw rearward. |
| IMU bracket | Roof, Pi tray, sensor leads, two rack bolts | Lift vertically through the open top. |
| Switch or fuse | Pod lid and associated disconnected leads | Service through the rear opening on the bench. |
| Eye ring | Split head underside, rear retainer, ring plug | Rearward out of the eye socket. |
| Chest matrix | Bezel, diffuser, carrier screws, plug | Remove front carrier; no bonded closed shell. |
| Foot switch | Wire cover, connector, two M2 bolts | Lift from its adjustable cassette. |

The first three paths are sampled geometric tests. The remaining paths are designed assembly sequences, not swept-volume certificates. Wire bends, plug latches, screwdrivers and hand access are not fully simulated. Move the unpowered mechanism gently during first assembly and retain only the movement range documented in `VERIFICATION.md` until physically checked.
