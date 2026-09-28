"""Revision B: published battery dimensions and adjustable serviceable packaging.
Regenerate with .venv-cad/Scripts/python.exe cad/build_duck_B.py.
Retains validated revision-A mechanical core; all B mounts are generated below.
"""
import build_duck as a
import pathlib,json
OUT=pathlib.Path(__file__).resolve().parent/'thenar_duck_B'
a.OUT=OUT;a.SPEC=json.loads((OUT.parents[1]/'design/spec_B.json').read_text())
from build_duck import *
# Tessellation of the imported faceted head can poison its shared triangulation.
# Keep presentation meshing on independent topology throughout this revision.
def mesh(shape):return a._original_mesh(shape.copy())
if not hasattr(a,'_original_mesh'):a._original_mesh=a.mesh
a.mesh=mesh
for folder in ['step','stl','brep','hardware','reports','renders']: (OUT/folder).mkdir(parents=True,exist_ok=True)
AOUT=OUT.parent/'thenar_duck_A'

def load_validated_core():
 scene=trimesh.load_scene(AOUT/'Thenar_Duck_A_FULL_ASSEMBLY.glb')
 index={p['name']:p for p in json.loads((AOUT/'reports/assembly_index.json').read_text())}
 manifests=json.loads((AOUT/'reports/print_manifest.json').read_text())
 for p in manifests:
  n=p['part']
  if n.startswith('C') or (n.startswith('A') and not n.startswith(('A15','A16','A17'))):continue
  i=index[n];s=cq.Shape.importBrep(str(AOUT/'brep'/(n+'.brep')))
  if not s.isValid():s=cq.importers.importStep(str(AOUT/'step'/(n+'.step'))).val()
  if not s.isValid() and n=='head_1':
   print('Re-sewing validated head print mesh',flush=True)
   m=trimesh.load_mesh(AOUT/'stl'/(n+'.stl'));m.apply_translation(scene.geometry[n].bounds[0]-m.bounds[0]);s=convert(m)
  print('Load core',n,flush=True)
  part(n,s,tuple(i['color']),qty=p['quantity'],body=i['body'],material=p['material'],notes=p['notes'],render_mesh=mesh(s))
 for h in json.loads((AOUT/'reports/component_envelopes.json').read_text()):
  n=h['name']
  if not n.startswith(('ST3215','roll_bearing','KW10')):continue
  i=index[n];f=AOUT/'hardware'/(n+'.step')
  hardware.append(dict(name=n,shape=None,mesh=scene.geometry[n],color=i['color'],body=i['body'],status=h['status']))
  if f.exists():shutil.copy2(f,OUT/'hardware'/f.name)
 for row in json.loads((AOUT/'reports/fasteners_custom_parts.json').read_text()):
  if row['joint'].startswith('A15'):fasteners.append(row)
 shutil.copy2(AOUT/'reports/joints.json',OUT/'reports/joints.json')

def base_and_sides():
 z=172.31499
 # Base supports the factory four-hole body interface. Battery and rack loads reach this chassis.
 s=box(-194,33,-54,54,z-3,z)
 # Lightening pockets leave peripheral rails, battery crossmembers, and trunk attachment region.
 for xa,xb in [(-175,-137),(-121,-84),(-68,-43)]:s=s.cut(box(xa,xb,-37,37,z-4,z+1))
 for x in [-179,-56]:s=s.fuse(box(x-5,x+5,-54,54,z-3,z))
 for ya,yb in [(-55,-38),(38,55)]:s=s.cut(box(-88,21,ya,yb,z-4,z+1))
 trunkpts=[(x,y,z-4) for x in [-29,-9] for y in [-10,10]];s=holes(s,trunkpts,3.3,6)
 mount=[(x,y) for x in [-185,-94,27] for y in [-46,46]]
 for x,y in mount:s=s.fuse(cyl(5,5,(x,y,z)))
 s=insert(s,[(x,y,z+5) for x,y in mount])
 # Four battery tray sockets, reachable from above with the battery removed.
 for x in [-179,-56]:
  for y in [-31,31]:s=s.fuse(cyl(5,5,(x,y,z)))
 s=insert(s,[(x,y,z+5) for x in [-179,-56] for y in [-31,31]])
 part('B01_chassis_base',s,'dark',notes='Four M3x6 attach upward into original trunk_bottom inserts; print flat')
 screw('Chassis to trunk_bottom',4,'M3',6,3,3,'Existing inserts open downward; no washer with this length')
 screw('Side frames to chassis',6,'M3',8,3.5,4.5,'0.5 mm flat washer; 4 mm inserts')
 # Removable perimeter frames, with large hip-yaw/roll windows.
 for sign,label in [(1,'L'),(-1,'R')]:
  ya,yb=(50,54) if sign==1 else (-54,-50)
  s=box(-194,33,ya,yb,z+5,284)
  s=s.cut(box(-180,-100,ya-1,yb+1,185,274)).cut(box(-88,24,ya-1,yb+1,z+4,274))
  for x in [-185,-94,27]:
   lo,hi=(41,54) if sign==1 else (-54,-41)
   s=s.fuse(box(x-5,x+5,lo,hi,z+5,z+8))
   s=holes(s,[(x,sign*46,z+4)],3.3,5)
  # Rack ledges use recessed, top-inserted M3 hardware.
  for x in [-184,-94]:
   lo,hi=(39,54) if sign==1 else (-54,-39)
   s=s.fuse(box(x-5,x+5,lo,hi,211,218));s=insert(s,[(x,sign*43,218)])
  # Side panel sockets, head access remains outside.
  for x,zz in [(-185,189),(-185,267),(-94,241),(28,264)]:
   lo,hi=(45,54) if sign==1 else (-54,-45)
   s=s.fuse(box(x-5,x+5,lo,hi,zz-5,zz+5));s=insert(s,[(x,sign*54,zz)],(0,-sign,0))
  for x in [-185,27]:
   lo,hi=(44,54) if sign==1 else (-54,-44)
   s=s.fuse(box(x-5,x+5,lo,hi,277,284));s=insert(s,[(x,sign*49,284)])
  for zz in [190,273]:
   lo,hi=(44,54) if sign==1 else (-54,-44)
   s=s.fuse(box(24,33,lo,hi,zz-5,zz+5));s=insert(s,[(33,sign*49,zz)],(-1,0,0))
   s=s.fuse(box(-194,-185,lo,hi,zz-5,zz+5));s=insert(s,[(-194,sign*49,zz)],(1,0,0))
  part('B02_side_frame_'+label,s,'dark',print_rotation=((0,0,0),(1,0,0),90))
  panel=box(-194,33,sign*54 if sign==1 else -56,56 if sign==1 else -54,z+6,284)
  panel=panel.cut(box(-88,24,-60,60,z+5,251))
  # Pi side sockets and cooling, accessible without disturbing the board.
  panel=panel.cut(box(-181,-100,-60,60,256,281))
  for zz in [198,204,210,216,242,248,254,260]:panel=panel.cut(box(-176,-102,-60,60,zz,zz+2.4))
  panel=holes(panel,[(x,-57 if sign==-1 else 53,zz) for x,zz in [(-185,189),(-185,267),(-94,241),(28,264)]],3.3,5,(0,1,0))
  part('B03_side_cover_'+label,panel,'shell',print_rotation=((0,0,0),(1,0,0),90))
 screw('Side covers',8,'M3',6,2.5,3.5,'0.5 mm washers; remove covers for battery strap access')
 # Front fascia, external screws and ventilation slots.
 s=box(33,36,-54,54,z+6,284)
 for zz in np.arange(246,272,6):s=s.cut(box(32,37,-36,36,zz,zz+3))
 s=holes(s,[(32,y,zz) for y in [-49,49] for zz in [190,273]],3.3,5,(1,0,0))
 part('B04_front_fascia',s,'shell',print_rotation=((0,0,0),(0,1,0),90))
 screw('Front and rear fascias',8,'M3',8,3.5,4.5,'0.5 mm washers')
 # Rear service cover and battery connector tunnel.
 s=box(-197,-194,-54,54,z+6,284)
 s=holes(s,[(-198,y,zz) for y in [-49,49] for zz in [190,273]],3.3,5,(1,0,0))
 s=s.cut(box(-198,-193,-29,29,181,210))
 for sh in [box(-222,-219,-32,32,178,213),box(-220,-194,-32,-29,178,213),box(-220,-194,29,32,178,213),box(-220,-194,-29,29,178,181),box(-220,-194,-29,29,210,213)]:s=s.fuse(sh)
 for y in [-30,30]:
  for zz in [220,275]:
   s=s.fuse(cyl(4.5,4,(-194,y,zz),(1,0,0)));s=insert(s,[(-197,y,zz)],(1,0,0))
 s=holes(s,[(-198,0,231)],14,6,(1,0,0))
 part('B05_rear_service_cover',s.clean(),'shell',notes='35mm rear lead bay behind nominal battery; pod and battery leads disconnect before removing cover',print_rotation=((0,0,0),(0,1,0),90))
 roof=box(-194,33,-54,54,284,286.5).cut(box(-55,34,-36,36,283,288))
 for x in np.arange(-172,-80,9):roof=roof.cut(box(x,x+4,-28,28,283,288))
 roof=holes(roof,[(x,y,283) for x in [-185,27] for y in [-49,49]],3.3,5)
 part('B07_lift_off_roof',roof,'shell',notes='Remove four screws for vertical Pi tray extraction')
 screw('Roof',4,'M3',6,3,3,'0.5 mm washers')

def battery():
 z=177.31499
 s=box(-191,-43,-35,35,z,z+3)
 for y0,y1 in [(-30,-27),(27,30)]:s=s.fuse(box(-191,-43,y0,y1,z+3,z+9))
 s=s.fuse(box(-46,-43,-27,27,z+3,z+13))
 for x in [-155,-82]:
  for y in [-23,23]:s=s.cut(box(x-10.5,x+10.5,y-1.5,y+1.5,z-1,z+4))
 s=holes(s,[(x,y,z-1) for x in [-179,-56] for y in [-31,31]],3.3,6)
 for xa,xb in [(-176,-168),(-138,-104),(-65,-53)]:s=s.cut(box(xa,xb,-15,15,z-1,z+4))
 part('B08_BK4200_battery_sled',s.clean(),'blue',notes='BONKA published 137x44x27; designed pack capacity140x50x32; 2mm pad and two20mm straps; leads face rear connector bay')
 screw('Battery sled',4,'M3',8,3.5,4.5,'0.5mm washer')
 hw('BK4200_3S_published_137x44x27',box(-187,-50,-22,22,z+5,z+32),'battery',status='BONKA BK-4200/35-3S published dimensions; model inference from user BK4200 label')
 hw('Battery_rear_connector_keepout',box(-215,-189,-12,12,185,208),'dark',status='Reserved plug and lead corridor; not a solid connector model')
 interfaces.append(dict(component='BK4200 3S',mount='B08 sled / B05 rear lead bay',installation='Thread straps, install pad, lower pack with leads rearward. Rear cover removes for horizontal swaps.',clearance='140x50x32 pack capacity; published pack137x44x27; rear lead/connector bay35mm beyond nominal pack',status='Manufacturer dimensions used; label-model inference recorded'))

def service_pod():
 # External box: switch terminals and fuse no longer compete with Pi or battery.
 s=union(box(-229,-197,-37,-34,214,283),box(-229,-197,34,37,214,283),box(-229,-197,-34,34,214,217),box(-229,-197,-34,34,280,283))
 for y in [-30,30]:
  for z in [220,275]:
   s=s.fuse(cyl(6,7,(-204,y,z),(1,0,0)))
   s=holes(s,[(-205,y,z)],3.3,10,(1,0,0))
 for y in [-30,30]:
  for z in [220,276]:
   s=s.fuse(cyl(6,8,(-229,y,z),(1,0,0)))
   s=insert(s,[(-229,y,z)],(1,0,0))
 # Ties pass through the floor and around a protected fuse-holder body.
 for x in [-223,-205]:
  for y in [-24,24]:s=s.cut(box(x-1.3,x+1.3,y-3,y+3,213,218))
 part('B06a_external_power_pod',s.clean(),'dark',notes='Open rear for terminal work; fuse cradle 45x24x24; rounded/insulated leads through 14mm rear-cover passage',print_rotation=((0,0,0),(0,1,0),90))
 for name,cutout,default in [('B06b_rocker_19p4x13p2',('rect',13.2,19.4),True),('C05_switch_30p2x22p2',('rect',22.2,30.2),False),('C05_switch_round_12p2',('round',12.2,0),False),('C05_switch_round_20p2',('round',20.2,0),False)]:
  lid=box(-232,-229,-37,37,214,283)
  if cutout[0]=='rect':lid=lid.cut(box(-233,-228,-cutout[1]/2,cutout[1]/2,261-cutout[2]/2,261+cutout[2]/2))
  else:lid=lid.cut(cyl(cutout[1]/2,5,(-233,0,261),(1,0,0)))
  lid=holes(lid,[(-233,y,z) for y in [-30,30] for z in [220,276]],3.3,5,(1,0,0))
  part(name,lid,'blue',body='trunk_assembly' if default else 'coupon',notes='Alternative lids: print ONE matching switch. Cutout dimensions are design choices, not identification of the owned switch. 3mm panel.',print_rotation=((0,0,0),(0,1,0),90))
 hw('Fuse_holder_capacity_45x24x24',box(-226,-202,-22.5,22.5,217,241),'dark',status='Maximum supported fuse body envelope; strapped, not a guessed hole pattern')
 hw('Switch_terminal_reserved_volume',box(-228,-204,-11,11,246,276),'dark',status='Switch+terminal design capacity24 deep x22 wide x30 high; use matching lid and insulate terminals')
 screw('Power pod to rear panel',4,'M3',10,7,3,'No washer for7mm flange stack')
 screw('Power pod lid',4,'M3',8,3.5,4.5,'0.5mm washer; interchangeable cutout panels')
 interfaces.append(dict(component='Main switch / fuse holder',mount='B06 external service pod',installation='Fit switch to matching lid on bench; strap fuse body into lower cradle; insulate terminals; mount lid last.',clearance='Fuse45x24x24; switch+terminals24x22x30. Four complete lid variants supplied.',status='Adjustable packaging, actual switch identity not asserted'))

def electronics():
 z=218
 s=box(-189,-61,-45,45,z,z+3)
 s=holes(s,[(x,y,z-1) for x in [-184,-94] for y in [-43,43]],3.3,5)
 # Pi tray at249: shorter pillars than A, without changing board standoff height.
 for x in [-184,-96]:
  for y in [-32,32]:s=s.fuse(cyl(4.5,28,(x,y,z+3)));s=insert(s,[(x,y,249)])
 adapterpts=[(x,y) for x in [-104,-67] for y in [-14,14]]
 for x,y in adapterpts:s=s.fuse(cyl(3.4,4,(x,y,z+3)))
 s=holes(s,[(x,y,z-1) for x,y in adapterpts],2.8,10)
 # PDB diagonal adjustment slots: 28..33mm mounting pitch, 30.5 nominal.
 pdbpts=[(-145+sx*15.25,sy*15.25) for sx in [-1,1] for sy in [-1,1]]
 for i,(x,y) in enumerate(pdbpts):
  sx=1 if x>-145 else -1;sy=1 if y>0 else -1
  tool=union(cyl(1.7,5,(x-sx*1.25,y-sy*1.25,z-1)),cyl(1.7,5,(x+sx*1.25,y+sy*1.25,z-1)),box(x-1.8,x+1.8,y-1.8,y+1.8,z-1,z+4))
  s=s.cut(tool)
  sh=cyl(3.5,4,(x,y,z+3)).cut(cyl(1.7,6,(x,y,z+2)))
  part('B19_PDB_insulating_spacer_'+str(i+1),sh,'blue',notes='4mm under-board spacing; position within slotted deck before tightening')
 # Insulated UBEC saddle and tie passages, open to differently wrapped modules.
 s=s.fuse(box(-176,-127,24,50,z+3,z+5))
 for x in [-166,-138]:
  for y in [25.5,48.5]:s=s.cut(box(x-3,x+3,y-1.1,y+1.1,z-1,z+6))
 s=holes(s,[(x,-40,z-1) for x in [-160,-122]],3.3,5)
 part('B09_power_and_compute_rack',s.clean(),'dark',notes='PDB 28..33mm diagonal slots;4mm spacers; adjustable UBEC ties; exact Waveshare A 37x28 pattern')
 pcb=box(-170,-120,-18,18,z+7,z+8.6);pcb=holes(pcb,[(x,y,z+6) for x,y in pdbpts],3,4)
 hw('PDB_XT60_reference_PCB',pcb,'pcb',status='Matek50x36x4 reference; xcluma clone mounting variation handled by slots')
 hw('PDB_component_and_XT60_keepout',box(-173,-117,-22,22,z+8.6,z+23),'dark',status='Conservative connector/component volume56x44; not exact purchased board CAD')
 hw('UBEC_adjustable_capacity',box(-173.5,-128.5,26,48,z+7,z+22),'blue',status='45x22x15 module capacity; dimensions not published by Readytosky; adjustable tie saddle')
 board=holes(box(-106.5,-64.5,-16.5,16.5,z+7,z+8.6),[(x,y,z+6) for x,y in adapterpts],2.5,4)
 hw('Waveshare_Adapter_A_PCB',board,'pcb',status='Waveshare published42x33 board,37x28 mounting pattern')
 hw('Adapter_components_envelope',box(-103,-67,-12,12,z+8.6,z+22),'dark')
 screw('Power rack to side ledges',4,'M3',8,3.5,4.5,'0.5mm washers')
 screw('PDB through bolts',4,'M3',12,9.1,2.9,'Four M3 nuts; 3mm deck+4mm spacer+1.6PCB+0.5washer')
 screw('Adapter PCB',4,'M2.5',12,8.6,3.4,'Four M2.5 nuts;4mm standoffs')
 # Correct Pi4 mounting pattern, with a side opening for the separate IMU.
 s=box(-189,-91,-36,36,249,252).cut(box(-174,-128,-17,17,248,253))
 s=s.cut(box(-156,-126,-37,-28.8,248,253))
 pi_pts=[(x,y) for x in [-179.5,-121.5] for y in [-24.5,24.5]]
 for x,y in pi_pts:s=s.fuse(cyl(3.2,5,(x,y,252)))
 s=holes(s,[(x,y,248) for x,y in pi_pts],2.8,12)
 s=holes(s,[(x,y,248) for x in [-184,-96] for y in [-32,32]],3.3,6)
 s=s.cut(box(-190,-176,-10,10,248,253))
 part('B10_Pi4B_removable_tray',s.clean(),'blue',notes='Official85x56 board;58x49 holes;5mm underside standoffs; lateral IMU/header slot')
 pcb=holes(box(-183,-98,-28,28,257,258.6),[(x,y,256) for x,y in pi_pts],2.75,4)
 hw('Raspberry_Pi_4B_PCB',pcb,'pcb',status='Official Pi4B mechanical drawing')
 for name,sh in [('USB2',box(-116,-95,0,15,258.6,274.6)),('USB3',box(-116,-95,-18,-3,258.6,274.6)),('Ethernet',box(-116,-95,16,29,258.6,272.1)),('GPIO',box(-176,-124,22,27,258.6,267.1)),('USB_C_power',box(-178,-166,-30,-23,258.6,261.8))]:hw('Pi4_'+name,sh,'metal' if name!='GPIO' else 'dark')
 screw('Pi4 PCB to tray',4,'M2.5',12,9.6,2.4,'Four M2.5 nuts;5mm standoff;0.5mm washers require longer screw')
 screw('Pi tray to rack pillars',4,'M3',8,3.5,4.5,'0.5mm washers')
 # IMU sits outside the Pi PCB footprint and is fixed independently to the rack.
 s=union(box(-166,-116,-49,-26,221,224),box(-156,-126,-31,-26,224,240),box(-156,-126,-49,-26,240,243))
 s=holes(s,[(x,-40,220) for x in [-160,-122]],3.3,6)
 for x in [-149.5,-133.5]:s=s.fuse(cyl(2.4,3,(x,-46,243)))
 s=holes(s,[(x,-46,239) for x in [-149.5,-133.5]],2.2,10)
 part('B11_SEN0374_side_bridge',s.clean(),'dark',notes='PCB rotated90deg: holes16mm apart on same edge; mount independent of Pi and covers; underside nut access')
 pcb=holes(box(-152,-131,-48.5,-29.5,246,247.6),[(x,-46,245) for x in [-149.5,-133.5]],2,4)
 hw('DFRobot_SEN0374_PCB',pcb,'pcb',status='DFRobot19x21 drawing; two2mm holes16mm apart')
 for x in [-150.5,-132.5]:hw('IMU_header_'+str(x),box(x-1.3,x+1.3,-42.5,-30.5,247.6,262),'dark',status='14.4mm header-and-plug clearance above PCB; lateral to Pi')
 screw('IMU PCB',2,'M2',10,7.6,2.4,'Two M2 nuts under top bridge;3mm standoffs')
 screw('IMU bridge to rack',2,'M3',10,6.5,3.5,'Two M3 nuts;0.5mm washers; accessible after Pi removal')
 interfaces.extend([
  dict(component='Pi4B',mount='B10 tray',installation='Fit board/cables on bench, lower tray through roof, fasten corners.',clearance='5mm below board; open USB end;microSD notch;roof9.4mm above USB shells',status='Published mechanical drawing'),
  dict(component='DFRobot SEN0374',mount='B11 side bridge',installation='Fit M2 bolts and nuts on bench. Bolt bridge to rack; Pi tray clears it through side slot.',clearance='PCB outside Pi footprint; header/plug height14.4mm; independent removal after Pi tray',status='Published mechanical drawing'),
  dict(component='PDB / UBEC / Waveshare adapter',mount='B09 rack',installation='Fit spacers, align slot-mounted PDB, tie UBEC to insulated saddle, bolt adapter on37x28 pattern before lowering rack.',clearance='PDB pitch28..33;UBEC45x22x15;adapter42x33',status='Published adapter/Matek reference; adjustable unmeasured clone/wrapped module')])

def eyes(update_head=True):
 # Widen only eye sockets; retain joint interfaces and original head geometry.
 if update_head:
  h=next(p for p in parts if p['name']=='head_1')
  for y in [-48,48]:h['shape']=h['shape'].cut(cyl(24,30.4,(76,y,397),(1,0,0))).clean()
  if not h['shape'].isValid() or len(h['shape'].Solids())!=1:raise ValueError('Head eye pocket revision invalid')
  h['mesh']=mesh(h['shape']);h['notes']+='; B48mm eye sockets with interchangeable centering sleeves'
 for y,label in [(-48,'R'),(48,'L')]:
  s=cyl(28,2.5,(74.5,y,397),(1,0,0)).cut(cyl(13,4,(74,y,397),(1,0,0)))
  pts=[(yy,zz) for yy,zz in [(y-24,385),(y+24,385),(y-24,409),(y+24,409)]]
  for yy,zz in pts:s=s.fuse(cyl(4.5,2.5,(74.5,yy,zz),(1,0,0)))
  s=holes(s,[(74,yy,zz) for yy,zz in pts],3.3,5,(1,0,0)).cut(box(74,79,y-5,y+5,373,386))
  # The faceted inner upper shell projects behind the nominal cylindrical eye.
  # Relieve the cap's upper inside corner, away from all four screw bosses.
  lo,hi=(y+8,y+18) if y<0 else (y-18,y-8)
  s=s.cut(box(74,79,lo,hi,419.5,427))
  part('B12_eye_retainer_'+label,s.clean(),'blue',body='head_assembly',print_rotation=((0,0,0),(0,1,0),90))
  sh=cyl(23.8,26,(77,y,397),(1,0,0)).cut(cyl(14,28,(76,y,397),(1,0,0)))
  sh=sh.cut(cyl(22.8,3,(101,y,397),(1,0,0))).cut(box(76,104,y-4,y+4,372,386))
  part('B13_eye_centering_sleeve_45_'+label,sh.clean(),'dark',body='head_assembly',notes='Default45mm PCB pocket45.6;0.2mm removable adhesive dots on rear PCB rim; LEDs face forward, no hard clamping of LEDs',print_rotation=((0,0,0),(0,1,0),90))
  ring=cyl(22.5,1.6,(101.2,y,397),(1,0,0)).cut(cyl(15,2,(101,y,397),(1,0,0)))
  hw('WS2812_ring_'+label,ring,'pcb',body='head_assembly',status='45mm design example; included37/44/46 centering alternatives, actual module identity not measured')
  part('B14_eye_diffuser_'+label,cyl(22.8,1,(105.5,y,397),(1,0,0)),(.65,.84,.95),body='head_assembly',material='translucent PETG',print_rotation=((0,0,0),(0,1,0),90))
 for d in [37,44,46]:
  sh=cyl(23.8,26,(0,0,0)).cut(cyl(14,28,(0,0,-1))).cut(cyl((d+.4)/2,3,(0,0,24))).cut(box(-4,4,-25,-11,-1,28))
  part('C06_eye_sleeve_'+str(d),sh.clean(),'dark',body='coupon',qty=2,notes='Alternative to B13, print two of the matching diameter; do not install all alternatives')
 screw('Eye retaining caps',8,'M3',6,3,3,'0.5mm washers')

def chest_lights():
 p=next(p for p in parts if p['name']=='B04_front_fascia');s=p['shape']
 s=s.cut(box(32,37,-21,21,223,265))
 for y,z in [(-25,244),(25,244),(40,234),(40,254)]:s=holes(s,[(32,y,z)],3.3,5,(1,0,0))
 for y in [-28,28]:
  for z in [230,258]:
   s=s.fuse(cyl(4.5,4,(29,y,z),(1,0,0)));s=insert(s,[(36,y,z)],(-1,0,0))
 s=holes(s,[(32,40,244)],3.2,5,(1,0,0));p['shape']=s.clean();p['mesh']=mesh(p['shape'])
 # Universal no-hole LED PCB support; board fixed on insulating removable tape.
 carrier=box(30,33,-23,23,222,266).cut(box(29,34,-10,10,234,254))
 for y in [-25,25]:carrier=carrier.fuse(cyl(4.5,7,(26,y,244),(1,0,0)));carrier=insert(carrier,[(33,y,244)],(-1,0,0))
 part('B21_matrix_PCB_carrier',carrier.clean(),'blue',notes='Supports square PCB30..40mm using thin insulated removable adhesive at bare PCB rear edges; no assumed mounting holes',print_rotation=((0,0,0),(0,1,0),90))
 bezel=box(36,42,-25,25,219,269).cut(box(35,43,-21,21,223,265))
 bezel=bezel.fuse(box(39,40,-22.5,22.5,221.5,266.5).cut(box(38,41,-21,21,223,265)))
 bezel=bezel.cut(box(35,39,-22.5,22.5,221.5,266.5))
 for y in [-28,28]:
  for z in [230,258]:bezel=bezel.fuse(cyl(4.5,3,(36,y,z),(1,0,0)))
 bezel=holes(bezel,[(35,y,z) for y in [-28,28] for z in [230,258]],3.3,5,(1,0,0))
 part('B22_matrix_bezel',bezel.clean(),'shell',print_rotation=((0,0,0),(0,1,0),90))
 part('B23_matrix_diffuser',box(38,39,-22.3,22.3,221.7,266.3),(.65,.84,.95),material='translucent PETG',print_rotation=((0,0,0),(0,1,0),90),notes='Retain with small removable adhesive dots; do not glue PCB permanently')
 hw('WS2812_matrix_PCB_30mm_example',box(33.2,34.8,-15,15,229,259),'pcb',status='30mm layout example;carrier accepts30..40mm square; seller dimensions unavailable')
 # A bare2020 LED needs a small solder carrier; provide explicit mounting space.
 pocket=box(24,33,33,47,237,251).cut(box(26,34,34.7,45.3,238.7,249.3))
 for z in [234,254]:pocket=pocket.fuse(cyl(4.5,9,(24,40,z),(1,0,0)));pocket=insert(pocket,[(33,40,z)],(-1,0,0))
 part('B24_status_pixel_carrier',pocket.clean(),'blue',notes='Fits10x10mm solder carrier for bare WS2812B-2020; bare chip is not mechanically mounted directly',print_rotation=((0,0,0),(0,1,0),90))
 part('B25_status_pixel_lightpipe',cyl(1.5,7,(30,40,244),(1,0,0)),(.65,.84,.95),material='translucent PETG',print_rotation=((0,0,0),(0,1,0),90))
 hw('Status_pixel_required_10x10_carrier',box(26.2,27.8,35,45,239,249),'pcb',status='Small solder carrier required for purchased bare2020 LED; not claimed supplied')
 hw('WS2812B_2020_pixel',box(27.8,28.8,39,41,243,245),'dark',status='2x2mm package envelope; solder to carrier before installing')
 screw('Matrix PCB carrier',2,'M3',8,3.5,4.5,'0.5mm washers; insert openings facefront')
 screw('Matrix bezel',4,'M3',8,3.5,4.5,'0.5mm washers')
 screw('Status pixel carrier',2,'M3',8,3.5,4.5,'0.5mm washers')

def finish_export():
 # Reuse standard fit coupons plus the already-added interchangeable parts.
 for row in fasteners:
  if row['thread']=='M3' and row['length_mm']==8 and row['engagement_mm']==4.5:
   row['clamped_stack_mm']=4;row['engagement_mm']=4
   row['notes']=row['notes'].replace('0.5mm','1mm').replace('0.5 mm','1 mm')+'; 0.5mm pilot-bottom allowance'
 a.coupons()
 a.export()
 for f in OUT.glob('Thenar_Duck_A_*'):f.rename(f.with_name(f.name.replace('Thenar_Duck_A_','Thenar_Duck_B_')))
 print('REVISION B COMPLETE',flush=True)

if __name__=='__main__':
 load_validated_core();base_and_sides();battery();service_pod();electronics();eyes();chest_lights();finish_export()
