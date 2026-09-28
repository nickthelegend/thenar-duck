"""Audit exported revision B and build its print package from the manifest."""
import pathlib,json,csv,collections,zipfile
import trimesh
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'cad/thenar_duck_B';R=OUT/'reports'
def read(name):return json.loads((R/(name+'.json')).read_text())
manifest=read('print_manifest');motion=read('motion_screen');services=read('service_paths');servo=read('servo_neutral_fit');static=read('custom_intersections');eyes=read('eye_fit')
capacity=read('battery_capacity');assert not capacity['contacts'],capacity['contacts']
failed=collections.Counter(c['pose'] for c in motion['contacts'])
poses=[dict(name=n,joints_degrees=q,result='CONTACT' if n in failed else 'no contact found',contact_pairs=failed[n]) for n,q in motion['poses_tested']]
(R/'sampled_poses.json').write_text(json.dumps(poses,indent=2))
rows=[]
for p in manifest:
 m=trimesh.load_mesh(OUT/'stl'/(p['part']+'.stl'))
 rows.append(dict(part=p['part'],watertight=bool(m.is_watertight),positive_volume=bool(m.volume>0),fits_256_cube=bool(max(m.extents)<=256),size_mm=[round(float(x),3) for x in m.extents]))
assert all(r['watertight'] and r['positive_volume'] and r['fits_256_cube'] for r in rows)
assert not static,static
assert not servo['contacts'],servo['contacts']
assert not eyes['contacts'],eyes['contacts']
assert all(not p['collisions'] for p in services),services
robot=[p for p in manifest if not p['part'].startswith('C0')]
alternatives=[p for p in manifest if p['part'].startswith(('C05','C06'))]
coupons=[p for p in manifest if p['part'].startswith(('C01','C02','C03','C04'))]
sw=read('solidworks_assembly') if (R/'solidworks_assembly.json').exists() else {'saved':False}
assert sw.get('saved') and not sw.get('missing') and not sw.get('extra'),'Native assembly must be complete before packaging'
audit=dict(release='Digital prototype: published dimensions and adjustable mounts; physical fitting and powered validation not performed',active_print_files=len(rows),robot_print_files=len(robot),alternative_files=len(alternatives),coupon_files=len(coupons),all_watertight=True,all_positive_volume=True,all_fit_256_cube=True,custom_intersections=static,removal_paths=services,servo_neutral_fit=servo,eye_fit=eyes,motion=dict(sampled=len(poses),no_contact_found=sum(p['result']=='no contact found' for p in poses),contact_poses=dict(failed),limitations=motion['limitations']),solidworks=sw,files=rows)
audit['maximum_battery_capacity']=capacity
(R/'validation_summary.json').write_text(json.dumps(audit,indent=2))
bad='; '.join(f'`{k}`' for k in failed) or 'None in this screen'
text=f'''# Verification — revision B

## Completed digital checks

- **{len(rows)} STL files:** {len(robot)} installed-part files, {len(alternatives)} alternative files and {len(coupons)} fit coupons. All are watertight, positive-volume meshes and fit a 256 mm cube. This checks the bounding envelope, not supports or slicing quality.
- Generator checks valid BREP and one connected solid per printed part. Tessellation is performed on independent copies to preserve imported head topology. Only sub-0.01 mm triangulation seams may be closed by the export repair routine.
- Exact checks found no overlap between the new torso parts and the modelled component envelopes in neutral.
- The full 140 × 50 × 32 mm battery capacity box, above the 2 mm pad, also clears the exported solid geometry in neutral; this goes beyond checking the smaller nominal battery example.
- Separate head/eye solid check: {eyes['pairs_tested']} candidate pairs, no overlaps above 0.1 mm³ after subtractive reliefs at the retainer corners. These reliefs only remove material; the earlier motion/servo checks remain conservative for the released caps.
- **{servo['pairs_tested']} candidate servo/print pairs** checked with vendor solid geometry in neutral: no intersections exceeding 0.1 mm³. Core mating reliefs are retained from A; this is not a connector insertion or manufacturing-tolerance proof.
- Battery, Pi tray and sensor removal checks found no overlaps at **{sum(p['positions_sampled'] for p in services)} sampled positions**. Covers and cables must be removed first as stated in ASSEMBLY.md. Fixed core/head and flexible wires were excluded from these torso-only service tests.
- Motion screen: **{len(poses)} poses**, **{sum(p['result']=='no contact found' for p in poses)} with no detected contact**, **{len(failed)} with detected contact**. Scope is moving assemblies against the new torso/electronics.
- Native SolidWorks: {sw.get('component_count','not yet verified')} components; missing: {sw.get('missing','not yet verified')}. Assembly is static and imported, not fully mated or supplied with original native feature history.

## Movement restrictions

Detected contact poses: **{bad}**. Do not command these poses. The exact angles and colliding part names are in `reports/motion_screen.json`. Tested coordinated head poses and crouches are in `reports/sampled_poses.json`.

Passing separate samples does not establish a continuous safe range or arbitrary simultaneous movement. The inherited mechanism's self-collision, flexible wires, plugged cable bends, screw heads, tool reach, structural strength, actuator torque, temperatures and walking balance have not been certified. No physical print or powered test has been performed.

## Dimensional basis and limits

Pi and SEN0374 mounting patterns come from manufacturer drawings. Battery reference is BONKA's 137 × 44 × 27 mm BK-4200/35-3S; the specific user pack's label was not available. Mount capacity is 140 × 50 × 32 with additional pad and lead space. PDB slots, UBEC ties, switch lids, LED sleeves and removable matrix carrier accommodate the stated ranges; these do not imply every product variant fits.

The new sensor bracket provides real mounting holes and plug space. M3 insert pilots still require a printer fit coupon because “M3 × 4” does not identify knurl outside diameter or printed shrinkage. Bearings, servo horns and foot switches likewise need first-assembly fitting/calibration.

## Inventory coverage

All components identified in the cart have an installed position or spare role. Four of six KW10s, two of three eye rings and three of four 6804 bearings are installed. The bare 2020 pixel requires an additional small solder carrier. The main switch, fuse holder and servo adapter are model assumptions or capacity-based mounts as disclosed in SOURCES.md.

The custom-part fastener count is derived from actual designed joints. The reference servo mechanism's complete fastener/insert count remains unspecified by its guide; the tables do not claim that 100 inserts covers the entire robot. Flexible soles, straps, insulation, wire, suitable connectors and small adhesive pads are separate assembly materials.
'''
(OUT/'VERIFICATION.md').write_text(text,encoding='utf-8')
fast=read('fasteners_custom_parts');counts=collections.Counter()
for p in fast:counts[(p['thread'],p['length_mm'])]+=p['quantity']
table='\n'.join(f'| {k[0]} × {k[1]} mm | {v} |' for k,v in sorted(counts.items()))
one=sum(p['quantity'] for p in fast if '1mm washer' in p['notes'] or '1 mm washer' in p['notes'] or '1 mm flat washer' in p['notes'])
half=sum(p['quantity'] for p in fast if p['thread']=='M3' and ('0.5mm washer' in p['notes'] or '0.5 mm washer' in p['notes'] or '0.5washer' in p['notes']) and 'require' not in p['notes'])
bom=f'''# Hardware and fasteners — revision B

## Installed hardware

| Item | Installed | From stated cart/ownership |
|---|---:|---|
| Waveshare ST3215 C018 12 V servo | 14 | 14 |
| Raspberry Pi 4B | 1 | Owned |
| BK 4200 mAh 3S | 1 | Owned; BONKA dimensional reference used |
| DFRobot SEN0374 BNO055 | 1 | Replacement selected |
| Waveshare Bus Servo Adapter (A) | 1 | Assumed corrected interface; distinct from 7.2 V buck |
| PDB and UBEC | 1 each | Cart |
| Inline fuse holder + fuse / DC main switch | 1 each | User reported corrections; exact models not supplied |
| 6804 ZZ bearing | 3 | 4; one spare |
| KW10 microswitch | 4 | 6; two spare |
| 16-pixel ring | 2 | 3; one spare |
| 4×4 LED matrix | 1 | Cart |
| Bare 2020 pixel | 1 | Cart; needs 10 × 10 mm solder carrier |

## Screws for the custom mounting system

These quantities include the four foot-contact cassettes, torso, lights and board mounts. **Add the retained servo mechanism's kit screws and core fasteners separately.** Screw length is measured under the head.

| Screw | Quantity |
|---|---:|
{table}

**Ordinary nuts for these custom mounts:** M3 **6**, M2.5 **8**, M2 **10**. Inserts already provide a nut at insert joints; do not buy one extra nut per insert. M3 nuts go to the PDB (4) and IMU bridge (2); M2.5 nuts go to Pi/adapter; M2 nuts go to sensor/foot switches.

**M3 flat washers:** {one} at **1 mm thickness**, {half} at **0.5 mm thickness**, for the explicitly washer-specified custom joints. Do not substitute arbitrary thickness at the short insert joints. PCB bolts use the individual stack specified in `reports/fasteners_custom_parts.csv`; the Pi M2.5×12 stack has no extra washer.

The B enclosure, eyes and light mounts contain **62 M3 insert positions**. The retained foot-contact changes add **16**, making **78 custom insert positions**, plus the original core's retained inserts (including four used to attach B01). The total inherited consumption is not reconciled; 100 owned inserts is not a verified whole-robot total. Alternative lids reuse the same installed inserts.

## Assembly materials

- Two 20 mm hook-and-loop battery straps and 2 mm nonabrasive pad.
- Insulating spacers B19 are printed; add ties for the UBEC/fuse, wire insulation and a grommet/sleeve for the 14 mm pass-through.
- Matching serial-bus cables, suitable power wires/connectors, Pi power lead and board/header leads. Cart PWM extension cables are not assumed to fit the bus servos.
- Thin removable insulating adhesive pads for LED PCB backs and diffuser retention; small 10 × 10 mm solder carrier for the bare pixel.
- PETG structural prints, compliant TPU/rubber sole provision and translucent diffuser material.

Electrical current budget, fuse rating, wire size and switch DC rating are outside this geometric BOM and have not been approved by the CAD fit check.
'''
(OUT/'BOM.md').write_text(bom,encoding='utf-8')
with zipfile.ZipFile(OUT/'Thenar_Duck_B_PRINTS.zip','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in manifest:
  f=OUT/'stl'/(p['part']+'.stl');z.write(f,str(f.relative_to(OUT)))
 for f in [*OUT.glob('*.md'),*R.glob('*.json'),*R.glob('*.csv')]:z.write(f,str(f.relative_to(OUT)))
 z.write(ROOT/'cad/reference_open_duck/LICENSE','SOURCE_LICENSE.txt')
 z.write(ROOT/'cad/reference_open_duck/assembly_guide.md','UPSTREAM_ASSEMBLY.md')
 z.write(ROOT/'design/spec_B.json','parameters/spec_B.json')
 for n in ['01_assembled.png','04_service_layout.png']:
  z.write(OUT/'renders'/n,'renders/'+n)
print(json.dumps({k:v for k,v in audit.items() if k not in ['files','removal_paths']},indent=2))
