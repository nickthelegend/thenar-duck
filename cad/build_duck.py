"""Thenar Duck A: Open Duck mechanical core + removable Pi4 / 3S packaging.

Run with .venv-cad/Scripts/python.exe cad/build_duck.py.
Dimensions in mm. Upstream facets are preserved; new parts are parametric BREP.
This is a fit-review release until the measurements in design/spec.json are confirmed.
"""
import pathlib,json,math,csv,shutil,collections
import cadquery as cq
import numpy as np,trimesh
from inspect_reference import load as load_reference,SRC
from mesh_to_brep import convert
from render_meshes import render
from print_mesh import prepare_mesh
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'cad/thenar_duck_A';CACHE=ROOT/'cad/development/brep_cache'
SPEC=json.loads((ROOT/'design/spec.json').read_text())
for d in [OUT,CACHE,OUT/'step',OUT/'stl',OUT/'renders',OUT/'hardware',OUT/'reports',OUT/'brep']:d.mkdir(exist_ok=True,parents=True)
COL={'shell':(.91,.92,.90),'dark':(.12,.15,.18),'blue':(.04,.37,.68),'pcb':(.03,.36,.22),'metal':(.62,.65,.68),'battery':(.10,.21,.55),'rubber':(.12,.12,.13)}
parts=[];hardware=[];fasteners=[];interfaces=[]
def box(x0,x1,y0,y1,z0,z1):return cq.Solid.makeBox(x1-x0,y1-y0,z1-z0,cq.Vector(x0,y0,z0))
def cyl(r,h,p,axis=(0,0,1)):return cq.Solid.makeCylinder(r,h,cq.Vector(*p),cq.Vector(*axis))
def union(*s):
 r=s[0]
 for v in s[1:]:r=r.fuse(v)
 return r.clean()
def holes(shape,pts,d,depth,axis=(0,0,1)):
 for p in pts:shape=shape.cut(cyl(d/2,depth,p,axis))
 return shape.clean()
def mesh(shape):
 v,f=shape.tessellate(.15,.15);return trimesh.Trimesh(vertices=np.array([i.toTuple() for i in v]),faces=np.asarray(f),process=False)
def part(name,shape,color='dark',qty=1,body='trunk_assembly',material='PETG',notes='',print_rotation=None,render_mesh=None):
 if not shape.isValid():raise ValueError('Invalid BREP: '+name)
 solids=shape.Solids()
 if len(solids)!=1:raise ValueError(f'{name}: {len(solids)} disconnected solids')
 item=dict(name=name,shape=shape,mesh=render_mesh if render_mesh is not None else mesh(shape),color=COL.get(color,color),qty=qty,body=body,material=material,notes=notes,rotation=print_rotation)
 parts.append(item);return shape
def hw(name,shape,color='pcb',body='trunk_assembly',status='nominal envelope'):
 hardware.append(dict(name=name,shape=shape,mesh=mesh(shape),color=COL.get(color,color),body=body,status=status));return shape
def screw(joint,qty,size,length,stack,engagement,notes=''):
 fasteners.append(dict(joint=joint,quantity=qty,thread=size,length_mm=length,clamped_stack_mm=stack,engagement_mm=engagement,notes=notes))
def insert(shape,points,axis=(0,0,-1)):
 return holes(shape,points,SPEC['insert']['pilot_diameter'],SPEC['insert']['pilot_depth'],axis)
def bore_cache(name):
 path=CACHE/(name+'.brep')
 if path.exists():return cq.Shape.importBrep(str(path)).clean()
 m=trimesh.load_mesh(SRC/(name+'.stl'));m.apply_scale(1000);s=convert(m)
 if not s.isValid():raise ValueError('Invalid reference '+name)
 s=s.clean();s.exportBrep(str(path));return s
def transform(shape,T):
 from OCP.gp import gp_Trsf
 tr=gp_Trsf();tr.SetValues(*[float(T[i,j]) for i in range(3) for j in range(4)])
 return shape.moved(cq.Location(tr))
def core(selection=None):
 refs,joints=load_reference();(OUT/'reports/joints.json').write_text(json.dumps(joints,indent=2))
 vendor=None;servo_number=0
 if selection is None:
  va=cq.Assembly.load(str(ROOT/'cad/vendor/STS3215_Waveshare_ST3215.step'))
  vendor=cq.Compound.makeCompound([shape.located(loc) for shape,name,loc,color in va])
 keep={'trunk_bottom','trunk_top','roll_motor_bottom','roll_motor_top','left_roll_to_pitch','right_roll_to_pitch','left_cache','right_cache','leg_spacer','left_knee_to_ankle_left_sheet','left_knee_to_ankle_right_sheet','foot_side','foot_top','foot_bottom_pla','foot_bottom_tpu','neck_left_sheet','neck_right_sheet','head_pitch_to_yaw','head_yaw_to_roll','head_roll_mount','head','head_bot_sheet'}
 counts=collections.Counter()
 for p in refs:
  n=p['name'];counts[n]+=1;name=n+'_'+str(counts[n]);isprint=n in keep
  if selection is not None and n not in selection:continue
  if not isprint:
   if n.startswith('wj-wk00-0123') and vendor is not None:
    servo_number+=1
    hw('ST3215_C018_'+str(servo_number).zfill(2),transform(vendor,p['T']),'dark',body=p['body'],status='Waveshare vendor STEP in the verified reference case frame; physical horn stack may vary by revision')
   elif n=='roll_bearing':
    bearing=transform(bore_cache(n),p['T'])
    hardware.append(dict(name=name,mesh=p['mesh'],shape=bearing,color=COL['metal'],body=p['body'],status='6804 20 x 32 x 7 mm reference geometry; physical fit coupon required'))
   continue
  srcname=n.replace('left_knee','knee') if not (SRC/(n+'.stl')).exists() else n
  print('Core',name,flush=True);s=transform(bore_cache(srcname),p['T'])
  if n=='trunk_top':
   # Retain every original servo mounting face. Remove obsolete Zero-era board shelf.
   s=s.cut(box(-300,-60,-200,200,0,500)).clean()
   # New upper rack fixing holes through the retained central web.
  if n=='head':
   for y in [-48,48]:
    s=s.cut(cyl(23,70,(65,y,397),(1,0,0)))
    # Integrated eye sockets overlap the existing front shell; open toward rear for insertion.
    outer=cyl(28,31,(77,y,397),(1,0,0)).cut(cyl(23,30.5,(76,y,397),(1,0,0)))
    outer=outer.cut(cyl(21.5,3,(106.4,y,397),(1,0,0)))
    for yy,zz in [(y-24,385),(y+24,385),(y-24,409),(y+24,409)]:
     outer=outer.fuse(cyl(4.5,12,(77,yy,zz),(1,0,0)))
    s=s.fuse(outer).clean()
    s=insert(s,[(77,y-24,385),(77,y+24,385),(77,y-24,409),(77,y+24,409)],(1,0,0))
  if n=='head_bot_sheet':
   for side,limits in [('L',(.4,200)),('R',(-200,-.2))]:
    sh=s.intersect(box(-200,200,*limits,300,500)).clean()
    part('head_bot_sheet_'+side,sh,'dark',body=p['body'],notes='Modified: split at centreline with 0.6mm seam, so panels slide sideways off the assembled neck; existing perimeter fasteners retained')
   continue
  if n=='foot_bottom_tpu':color='rubber';mat='TPU'
  elif 'cache' in n or n=='head':color='shell';mat='PETG'
  elif n in ['foot_top','left_roll_to_pitch','right_roll_to_pitch']:color='blue';mat='PETG'
  else:color='dark';mat='PETG'
  part(name,s,color,body=p['body'],material=mat,notes='Derived from pinned Open Duck Mini v2; reference facet geometry retained'+('; obsolete electronics shelf removed' if n=='trunk_top' else ''),render_mesh=p['mesh'] if n not in ['trunk_top','head'] else None)
 return refs
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
 part('A01_chassis_base',s,'dark',notes='Four M3x6 attach upward into original trunk_bottom inserts; print flat')
 screw('Chassis to trunk_bottom',4,'M3',6,3,3,'Existing inserts open downward; no washer with this length')
 screw('Side frames to chassis',6,'M3',8,3.5,4.5,'0.5 mm flat washer; 4 mm inserts')
 # Removable perimeter frames, with large hip-yaw/roll windows.
 for sign,label in [(1,'L'),(-1,'R')]:
  ya,yb=(50,54) if sign==1 else (-54,-50)
  s=box(-194,33,ya,yb,z+5,305)
  s=s.cut(box(-180,-100,ya-1,yb+1,185,295)).cut(box(-88,24,ya-1,yb+1,z+4,295))
  for x in [-185,-94,27]:
   lo,hi=(41,54) if sign==1 else (-54,-41)
   s=s.fuse(box(x-5,x+5,lo,hi,z+5,z+8))
   s=holes(s,[(x,sign*46,z+4)],3.3,5)
  # Rack ledges use recessed, top-inserted M3 hardware.
  for x in [-184,-94]:
   lo,hi=(39,54) if sign==1 else (-54,-39)
   s=s.fuse(box(x-5,x+5,lo,hi,223,230));s=insert(s,[(x,sign*43,230)])
  # Side panel sockets, head access remains outside.
  for x,zz in [(-185,189),(-185,288),(-94,253),(28,285)]:
   lo,hi=(45,54) if sign==1 else (-54,-45)
   s=s.fuse(box(x-5,x+5,lo,hi,zz-5,zz+5));s=insert(s,[(x,sign*54,zz)],(0,-sign,0))
  for x in [-185,27]:
   lo,hi=(44,54) if sign==1 else (-54,-44)
   s=s.fuse(box(x-5,x+5,lo,hi,298,305));s=insert(s,[(x,sign*49,305)])
  for zz in [190,294]:
   lo,hi=(44,54) if sign==1 else (-54,-44)
   s=s.fuse(box(24,33,lo,hi,zz-5,zz+5));s=insert(s,[(33,sign*49,zz)],(-1,0,0))
   s=s.fuse(box(-194,-185,lo,hi,zz-5,zz+5));s=insert(s,[(-194,sign*49,zz)],(1,0,0))
  part('A02_side_frame_'+label,s,'dark',print_rotation=((0,0,0),(1,0,0),90))
  panel=box(-194,33,sign*54 if sign==1 else -56,56 if sign==1 else -54,z+6,305)
  panel=panel.cut(box(-88,24,-60,60,z+5,251))
  # Pi side sockets and cooling, accessible without disturbing the board.
  panel=panel.cut(box(-186,-95,-60,60,273,298))
  for zz in [198,204,210,216,242,248,254,260]:panel=panel.cut(box(-176,-88,-60,60,zz,zz+2.4))
  panel=holes(panel,[(x,-57 if sign==-1 else 53,zz) for x,zz in [(-185,189),(-185,288),(-94,253),(28,285)]],3.3,5,(0,1,0))
  part('A03_side_cover_'+label,panel,'shell',print_rotation=((0,0,0),(1,0,0),90))
 screw('Side covers',8,'M3',6,2.5,3.5,'0.5 mm washers; remove covers for battery strap access')
 # Front fascia, external screws and ventilation slots.
 s=box(33,36,-54,54,z+6,305)
 for zz in np.arange(258,293,6):s=s.cut(box(32,37,-36,36,zz,zz+3))
 s=holes(s,[(32,y,zz) for y in [-49,49] for zz in [190,294]],3.3,5,(1,0,0))
 part('A04_front_fascia',s,'shell',print_rotation=((0,0,0),(0,1,0),90))
 screw('Front and rear fascias',8,'M3',8,3.5,4.5,'0.5 mm washers')
 # Back panel with a replaceable switch plate: exact cutout awaits the chosen switch.
 s=box(-197,-194,-54,54,z+6,305)
 s=s.cut(box(-198,-193,-22.4,22.4,260,294.8))
 for y in [-27,27]:
  for zz in [264,290]:
   s=s.fuse(cyl(4.5,4,(-194,y,zz),(1,0,0)))
   s=insert(s,[(-197,y,zz)],(1,0,0))
 s=holes(s,[(-198,y,zz) for y in [-49,49] for zz in [190,294]],3.3,5,(1,0,0))
 part('A05_rear_service_cover',s,'shell',print_rotation=((0,0,0),(0,1,0),90))
 blank=box(-200,-197,-32,32,257,298)
 blank=holes(blank,[(-201,y,zz) for y in [-27,27] for zz in [264,290]],3.3,5,(1,0,0))
 part('A06_switch_plate_BLANK',blank,'blue',notes='HOLD: user switch cutout not provided; replace this small plate after measurement',print_rotation=((0,0,0),(0,1,0),90))
 screw('Replaceable switch plate',4,'M3',8,3.5,4.5,'Cutout pending exact switch; 0.5 mm washer')
 roof=box(-194,33,-54,54,305,307.5).cut(box(-55,34,-36,36,304,309))
 for x in np.arange(-172,-80,9):roof=roof.cut(box(x,x+4,-28,28,304,309))
 roof=holes(roof,[(x,y,304) for x in [-185,27] for y in [-49,49]],3.3,5)
 part('A07_lift_off_roof',roof,'shell',notes='Remove four screws for vertical Pi tray extraction')
 screw('Roof',4,'M3',6,3,3,'0.5 mm washers')
def battery():
 z=177.31499
 s=box(-190,-44,-35,35,z,z+3)
 # Strap rails and a padded end stop; no squeeze-fit walls around LiPo cells.
 s=s.fuse(box(-190,-44,-30,-27,z+3,z+9)).fuse(box(-190,-44,27,30,z+3,z+9)).fuse(box(-47,-44,-27,27,z+3,z+13))
 for x in [-155,-82]:
  for y in [-23,23]:s=s.cut(box(x-10.5,x+10.5,y-1.5,y+1.5,z-1,z+4))
 s=holes(s,[(x,y,z-1) for x in [-179,-56] for y in [-31,31]],3.3,6)
 # Lightweight central opening with broad edges, foam spans the ribs.
 for xa,xb in [(-176,-168),(-138,-104),(-65,-53)]:s=s.cut(box(xa,xb,-15,15,z-1,z+4))
 part('A08_battery_sled',s,'blue',notes='Fits envelope <=136 x 52 x 42 plus 2mm pad; two 20mm hook-and-loop straps; dimensions NOT yet confirmed')
 screw('Battery sled',4,'M3',8,3.5,4.5,'0.5mm washer; remove pack before reaching these screws')
 hw('BK_3S_BATTERY_MAX_RESERVED',box(-185,-49,-26,26,z+5,z+47),'battery',status='RESERVED CAPACITY ONLY; actual battery dimensions unknown')
 interfaces.append(dict(component='BK 4200mAh 3S',mount='A08_battery_sled',installation='Remove roof and upper trays; lower pack vertically. For later swaps remove rear cover and release both straps.',clearance='1 mm per side at maximum 52 mm width; 2 mm foam pad; lead exit and connector bend space require actual pack measurement',status='HOLD actual dimensions'))
def electronics():
 s=box(-189,-61,-45,45,230,233)
 s=holes(s,[(x,y,229) for x in [-184,-94] for y in [-43,43]],3.3,5)
 # Open strap slots for fuse, UBEC, PDB: exact hardware can move without a new chassis.
 for cx,cy,L,W in [(-145,0,56,44),(-151,37,45,22),(-151,-36,45,24)]:
  for xx in [cx-L*.3,cx+L*.3]:
   for yy in [cy-W*.36,cy+W*.36]:s=s.cut(box(xx-3,xx+3,yy-1.3,yy+1.3,229,234))
 # Pi carrier pillars (tray is removable, board stays attached).
 for x in [-184,-96]:
  for y in [-32,32]:
   s=s.fuse(cyl(4.5,33,(x,y,233)));s=insert(s,[(x,y,266)])
 # Four adapter standoffs and captive M2.5 nut pockets, accessible before tray installation.
 adapterpts=[(x,y) for x in [-104,-67] for y in [-14,14]]
 for x,y in adapterpts:s=s.fuse(cyl(3.4,4,(x,y,233)))
 s=holes(s,[(x,y,229) for x,y in adapterpts],2.8,10)
 part('A09_power_and_compute_rack',s,'dark',notes='Install boards and threaded hardware on bench; bolt rack to side frames; Pi is a separate upper tray')
 screw('Power rack to side ledges',4,'M3',8,3.5,4.5,'0.5mm washer')
 hw('PDB_MAX_RESERVED',box(-173,-117,-22,22,237,257),'pcb',status='56x44x20 reserved; exact PDB unconfirmed; insulating 4mm standoffs required')
 hw('UBEC_MAX_RESERVED',box(-173.5,-128.5,26,48,237,252),'blue',status='45x22x15 reserved; secure with two ties; do not clamp components')
 hw('FUSE_HOLDER_MAX_RESERVED',box(-173.5,-128.5,-48,-24,237,261),'dark',status='45x24x24 reserved; exact holder unconfirmed; fuse pulls upward after Pi tray removal')
 # Nominal adapter physical board; cable areas remain open forward and upward.
 board=box(-106.5,-64.5,-16.5,16.5,237,238.6)
 board=holes(board,[(x,y,236) for x,y in adapterpts],2.5,4)
 hw('Waveshare_Adapter_A_PCB',board,'pcb',status='42x33 outline, 37x28 holes; exact board revision confirmation pending')
 hw('Adapter_components_envelope',box(-103,-67,-12,12,238.6,252),'dark')
 screw('Adapter A PCB',4,'M2.5',12,8.6,3.4,'4 M2.5 nuts under rack; standoffs 4mm; verify supplied board holes')
 # Pi4 board hole pattern has an asymmetric 23.5mm extension at the USB end.
 s=box(-189,-91,-36,36,266,269)
 s=s.cut(box(-174,-128,-17,17,265,270))
 pi_pts=[(x,y) for x in [-179.5,-121.5] for y in [-24.5,24.5]]
 for x,y in pi_pts:s=s.fuse(cyl(3.2,5,(x,y,269)))
 s=holes(s,[(x,y,265) for x,y in pi_pts],2.8,12)
 s=holes(s,[(x,y,265) for x in [-184,-96] for y in [-32,32]],3.3,6)
 # MicroSD finger access at the -X edge, below PCB.
 s=s.cut(box(-190,-176,-10,10,265,270))
 part('A10_Pi4B_removable_tray',s,'blue',notes='85x56 PCB, asymmetric official mounting pattern; M2.5 screws and nuts, no M2.5 heat inserts')
 pcb=box(-183,-98,-28,28,274,275.6);pcb=holes(pcb,[(x,y,273) for x,y in pi_pts],2.75,4)
 hw('Raspberry_Pi_4B_PCB',pcb,'pcb',status='Official mechanical drawing; bare board, not a case')
 # Port volumes from official drawing; conservative plug-clearance spaces handled separately.
 for name,sh in [('USB2',box(-116,-95,0,15,275.6,291.6)),('USB3',box(-116,-95,-18,-3,275.6,291.6)),('Ethernet',box(-116,-95,16,29,275.6,289.1)),('GPIO',box(-176,-124,22,27,275.6,284.1)),('USB_C_power',box(-178,-166,-30,-23,275.6,278.8))]:hw('Pi4_'+name,sh,'metal' if name!='GPIO' else 'dark')
 screw('Pi4 PCB to tray',4,'M2.5',12,9.6,2.4,'4 M2.5 nuts; 5mm standoff + 3mm tray + 1.6mm PCB; verify connector-side clearance')
 screw('Pi tray to rack pillars',4,'M3',8,3.5,4.5,'0.5mm washers; four screws exposed at tray corners')
 interfaces.append(dict(component='Raspberry Pi 4B',mount='A10_Pi4B_removable_tray',installation='Mount Pi to tray outside robot. Connect short USB leads. Lower tray through roof opening, then fix four M3 screws.',clearance='5mm underside, side I/O window, open USB end, microSD notch, 29.4mm PCB-top to roof',status='Drawing checked; physical cables/cooling unconfirmed'))
 # Torso-fixed IMU bridge, independent of all removable covers and Pi tray.
 s=box(-69,-52,-43,43,283,286)
 s=s.fuse(box(-69,-28,-14,14,283,286))
 for sign in [-1,1]:
  s=s.fuse(box(-69,-59,min(sign*40,sign*45),max(sign*40,sign*45),233,283))
  s=s.fuse(box(-80,-57,min(sign*37,sign*45),max(sign*37,sign*45),233,236))
 # Bolt bridge to removable rack, which is rigidly fixed to chassis during operation.
 s=holes(s,[(-74,y,232) for y in [-40,40]],3.3,6)
 for y in [-8,8]:s=s.fuse(cyl(2.4,3,(-50,y,286)))
 s=holes(s,[(-50,y,282) for y in [-8,8]],2.2,10)
 part('A11_SEN0374_fixed_IMU_bridge',s,'dark',notes='2xM2 through fasteners at 16mm pitch on the same PCB edge. IMU does not move when covers/Pi tray are removed.')
 # Through bolt positions added to power rack after it is created.
 idx=next(i for i,p in enumerate(parts) if p['name']=='A09_power_and_compute_rack');parts[idx]['shape']=holes(parts[idx]['shape'],[(-74,y,229) for y in [-40,40]],3.3,6);parts[idx]['mesh']=mesh(parts[idx]['shape'])
 pcb=box(-52.5,-33.5,-10.5,10.5,289,290.6);pcb=holes(pcb,[(-50,y,288) for y in [-8,8]],2,4)
 hw('DFRobot_SEN0374_PCB',pcb,'pcb',status='19x21 board; two holes x=2.5 from edge, y=2.5/18.5; official diagram')
 for y in [-9,9]:hw('IMU_header_'+str(y),box(-46.5,-34.5,y-1.3,y+1.3,290.6,300),'dark')
 screw('IMU PCB',2,'M2',10,7.6,2.4,'2 M2 nuts under bridge; 3mm spacers; access with bridge outside robot')
 screw('IMU bridge to rack',2,'M3',10,6,4,'2 M3 nuts under rack; no inserts required')
 interfaces.append(dict(component='DFRobot SEN0374',mount='A11_SEN0374_fixed_IMU_bridge',installation='Fit two M2 screws and nuts on bench, then bolt bridge to rack. Headers soldered before installation.',clearance='3mm under board; header space to z300; full vertical removal after roof removal',status='Manufacturer drawing checked; physical header style pending'))
def eyes():
 for y,label in [(-48,'R'),(48,'L')]:
  # Socket opens from the rear, with a separate retaining cap; no trapped board.
  s=cyl(28,2.5,(74.5,y,397),(1,0,0)).cut(cyl(20,4,(74,y,397),(1,0,0)))
  for yy,zz in [(y-24,385),(y+24,385),(y-24,409),(y+24,409)]:s=s.fuse(cyl(4.5,2.5,(74.5,yy,zz),(1,0,0)))
  s=holes(s,[(74,yy,zz) for yy,zz in [(y-24,385),(y+24,385),(y-24,409),(y+24,409)]],3.3,5,(1,0,0))
  s=s.cut(box(74,79,y-5,y+5,373,380))
  part('A12_eye_retainer_'+label,s,'blue',body='head_assembly',notes='Remove rear cap to insert LED assembly; ring size remains a measurement gate',print_rotation=((0,0,0),(0,1,0),90))
  # Removable annular spacer supports only the back of the PCB, not the LEDs.
  sh=cyl(22.7,24,(77,y,397),(1,0,0)).cut(cyl(19.5,26,(76,y,397),(1,0,0)))
  sh=sh.cut(box(76,102,y-4,y+4,373,380))
  part('A13_eye_depth_spacer_'+label,sh,'dark',body='head_assembly',notes='Adjust length after actual ring + diffuser stack measurement',print_rotation=((0,0,0),(0,1,0),90))
  ring=cyl(22,1.6,(101,y,397),(1,0,0)).cut(cyl(15,2,(100.8,y,397),(1,0,0)))
  hw('WS2812_ring_'+label,ring,'pcb',body='head_assembly',status='44mm nominal example only; max socket46mm; measure actual ring')
  lens=cyl(22.8,1,(105.5,y,397),(1,0,0))
  part('A14_eye_diffuser_'+label,lens,(.65,.84,.95),body='head_assembly',material='translucent PETG',print_rotation=((0,0,0),(0,1,0),90),notes='Front retention lip must be validated with actual optical stack')
 screw('Eye retaining caps',8,'M3',6,3,3,'0.5mm washers; access from rear with head bottom removed')
def foot_contacts():
 # Inverted KW10: the guided ground plunger pushes the lever upward. Case mounting
 # has 3mm vertical adjustment; the TPU sole carries body load, not the switch.
 for foot,cy,body in [('L',89.4,'foot_assembly'),('R',-89.4,'foot_assembly_2')]:
  for end,cx,direction in [('toe',7.4,1),('heel',-57.4,-1)]:
   px=cx+direction*8.6
   # Change the actual retained foot parts, not just add floating switch models.
   for p in parts:
    if p['body']!=body:continue
    n=p['name'];s=p['shape']
    if n.startswith('foot_bottom_pla'):
     for yy in [cy-9,cy+9]:s=s.fuse(cyl(4.5,8,(cx,yy,8)))
     s=insert(s,[(cx,yy,16) for yy in [cy-9,cy+9]])
     s=s.cut(box(cx-10,cx+10,cy-3.5,cy+3.5,10.5,36))
     s=s.cut(cyl(2.25,10,(px,cy,7)))
    elif n.startswith('foot_bottom_tpu'):
     s=s.cut(cyl(2.25,10,(px,cy,-1))).cut(cyl(4.25,3,(px,cy,5.5)))
    elif n.startswith('foot_top') or n.startswith('foot_side'):
     s=s.cut(box(cx-15,cx+15,cy-14,cy+14,10.5,35))
    else:continue
    if not s.isValid() or len(s.Solids())!=1:raise ValueError('Foot sensor modification invalid: '+n)
    p['shape']=s.clean();p['mesh']=mesh(p['shape']);p['notes']+='; KW10 cassette clearance/plunger passages added'
   # Bench-assembled removable cassette: switch slides in through the open top.
   s=box(cx-10,cx+10,cy-13.5,cy+13.5,16,19)
   s=s.cut(box(cx-6.8,cx+6.8,cy-3.2,cy+3.2,15,31))
   for sign in [-1,1]:
    ya,yb=(cy+3.2,cy+5.6) if sign==1 else (cy-5.6,cy-3.2)
    s=s.fuse(box(cx-8,cx+8,ya,yb,16,27))
   for xx in [cx-3.25,cx+3.25]:
    slot=union(cyl(1.1,14,(xx,cy-7,20),(0,1,0)),cyl(1.1,14,(xx,cy-7,23),(0,1,0)),box(xx-1.1,xx+1.1,cy-7,cy+7,20,23))
    s=s.cut(slot)
   for xx in [cx-11,cx+11]:s=s.fuse(cyl(3.5,14,(xx,cy,16)))
   s=insert(s,[(xx,cy,30) for xx in [cx-11,cx+11]])
   s=holes(s,[(cx,yy,15) for yy in [cy-9,cy+9]],3.3,6)
   name='A15_KW10_cassette_'+foot+'_'+end
   part(name,s,'blue',body=body,notes='Mount inverted switch with M2 bolts through 3mm adjustment slots; bench-calibrate before printing full feet')
   cap=box(cx-15,cx+15,cy-13.5,cy+13.5,30,32)
   cap=holes(cap,[(xx,cy,29) for xx in [cx-11,cx+11]],3.3,5)
   cap=cap.cut(box(cx-4,cx+4,cy+7,cy+11,29,33))
   part('A16_switch_cover_'+foot+'_'+end,cap,'blue',body=body,notes='Wire exit, lift-off lid; screw heads remain outside the shell')
   plunger=union(cyl(2,12.25,(px,cy,-.5)),cyl(4,1.25,(px,cy,5.5)))
   part('A17_ground_plunger_'+foot+'_'+end,plunger,'dark',body=body,notes='Install from underneath before TPU sole. 0.5mm protrusion unloaded, 1.25mm hard-stop travel. Smooth bore and confirm no sticking.')
   sh=box(cx-6.4,cx+6.4,cy-2.9,cy+2.9,17,23.5)
   sh=holes(sh,[(xx,cy-4,21.5) for xx in [cx-3.25,cx+3.25]],2,8,(0,1,0))
   hw('KW10_'+foot+'_'+end,sh,'dark',body=body,status='Daier KW10-DZ2P075 nominal; operating height requires bench adjustment')
   screw(name+' to foot',2,'M3',8,3.5,4.5,'0.5mm washers; inserts open upward at z16')
   screw(name+' switch pins',2,'M2',14,11.2,2.8,'Two M2 nuts; adjust height in slots, check continuity; do not over-tighten plastic case')
   screw(name+' cover',2,'M3',6,2.5,3.5,'0.5mm washers')
 interfaces.append(dict(component='4 KW10-DZ2P075 foot switches',mount='A15 cassettes + A17 plungers',installation='Solder and insulate wires, insert switches from top, install M2 bolts through slots. Insert plungers from underneath, then fit TPU soles. Adjust switch height with meter.',clearance='12.8x5.8x6.5 case; 6.5 hole pitch; 3mm vertical adjustment; 1.25mm plunger hard-stop travel',status='Catalogue checked; physical actuation calibration REQUIRED'))
def coupons():
 s=box(0,105,0,40,0,7)
 for i,d in enumerate([3.8,3.9,4.0,4.1,4.2]):s=s.cut(cyl(d/2,4.5,(10+i*20,10,2.5)))
 for i,d in enumerate([3.2,3.3,3.4,3.5,3.6]):s=s.cut(cyl(d/2,9,(10+i*20,29,-1)))
 part('C01_M3_insert_and_clearance_coupon',s,'blue',body='coupon',notes='Rows: 3.8/3.9/4.0/4.1/4.2 blind insert pilots, then 3.2/3.3/3.4/3.5/3.6 through clearance; left to right')
 for d in [32.0,32.1,32.2]:
  s=cyl(20,8,(0,0,0)).cut(cyl(d/2,9,(0,0,-.5)))
  part('C02_6804_fit_'+str(d).replace('.','p'),s,'blue',body='coupon',notes='Bearing slip-fit trial; do not force a tight PETG ring')
 s=box(0,56,0,36,0,8).cut(box(5.14,50.86,5.39,30.61,-1,9))
 part('C03_servo_case_clearance_gauge',s,'blue',body='coupon',notes='45.72x25.22mm opening: 0.25mm per side around 45.22x24.72 case. Slide case through before building robot.')
 s=cyl(14,3,(0,0,0));s=holes(s,[(0,0,-1)],6.5,5)
 s=holes(s,[(7,0,-1),(-7,0,-1),(0,7,-1),(0,-7,-1)],3.3,5)
 part('C04_servo_horn_pattern_gauge',s,'blue',body='coupon',notes='14mm pitch-circle, four M3 clearance holes; verify supplied horn and actual screw engagement')
def adapt_vendor_interfaces():
 config=json.loads((ROOT/'design/servo_interface_reliefs.json').read_text())
 lookup={p['name']:p for p in parts};vendors={h['name']:h for h in hardware};report=[]
 for pair in config['interfaces']:
  p=lookup[pair['printed']];before=p['shape'];s=before.cut(vendors[pair['servo']]['shape']).clean()
  if not s.isValid() or len(s.Solids())!=1:raise ValueError('Servo relief invalid/disconnected: '+p['name'])
  removed=before.Volume()-s.Volume()
  if removed>before.Volume()*.05:raise ValueError('Servo relief removes over 5% of part: '+p['name'])
  p['shape']=s;p['mesh']=mesh(s)
  note='; nominal mating relief for Waveshare vendor servo, physical seating/cable fit required'
  if note not in p['notes']:p['notes']+=note
  report.append(dict(**pair,removed_mm3=round(removed,4),removed_percent=round(100*removed/before.Volume(),4)))
  print('Servo relief',report[-1],flush=True)
 (OUT/'reports/servo_interface_reliefs.json').write_text(json.dumps(report,indent=2))

def export():
 assy=cq.Assembly(name='Thenar_Duck_A_FIT_REVIEW');inventory=[]
 for p in parts:
  name=p['name'];s=p['shape'];s.exportBrep(str(OUT/'brep'/(name+'.brep')));cq.exporters.export(s,str(OUT/'step'/(name+'.step')))
  # Some sewn reference faces need STEP's tolerance healing after BREP serialization.
  if not cq.Shape.importBrep(str(OUT/'brep'/(name+'.brep'))).isValid():
   s=cq.importers.importStep(str(OUT/'step'/(name+'.step'))).val()
   if not s.isValid() or len(s.Solids())!=1:raise ValueError('Invalid serialized solid: '+name)
   s.exportBrep(str(OUT/'brep'/(name+'.brep')))
   if not cq.Shape.importBrep(str(OUT/'brep'/(name+'.brep'))).isValid():raise ValueError('BREP round-trip failed: '+name)
   p['shape']=s;p['mesh']=mesh(s)
  printable=s
  rotation=p['rotation']
  if rotation is None and ('sheet' in name or 'neck_' in name):
   bb=s.BoundingBox()
   if bb.ylen<min(bb.xlen,bb.zlen):rotation=((0,0,0),(1,0,0),90)
  if rotation:printable=printable.rotate(*rotation)
  bb=printable.BoundingBox();printable=printable.translate((-bb.xmin,-bb.ymin,-bb.zmin));bb=printable.BoundingBox()
  pm=p['mesh'].copy()
  if rotation:
   p0,p1,deg=rotation;axis=np.asarray(p1)-np.asarray(p0);pm.apply_transform(trimesh.transformations.rotation_matrix(math.radians(deg),axis,p0))
  pm.apply_translation(-pm.bounds[0])
  try:pm,repair=prepare_mesh(pm)
  except ValueError as e:raise ValueError(name+': '+str(e)) from e
  pm.export(str(OUT/'stl'/(name+'.stl')))
  if p['body']!='coupon':assy.add(s,name=name,color=cq.Color(*p['color']))
  inventory.append(dict(part=name,quantity=p['qty'],material=p['material'],size_mm=[round(bb.xlen,2),round(bb.ylen,2),round(bb.zlen,2)],solid_volume_cm3=round(s.Volume()/1000,2),print_bed_fits=max(bb.xlen,bb.ylen,bb.zlen)<=250,watertight=pm.is_watertight,notes=p['notes']))
 print('Saving STEP assembly',flush=True);assy.save(str(OUT/'Thenar_Duck_A_PRINTED_PARTS.step'))
 # Hardware and print geometry together in a portable, named mesh scene.
 scene=trimesh.Scene()
 for p in [*parts,*hardware]:
  if p['body']=='coupon':continue
  m=p['mesh'].copy();m.visual.face_colors=np.array([*p['color'][:3],1])*255;scene.add_geometry(m,node_name=p['name'],geom_name=p['name'])
 scene.export(str(OUT/'Thenar_Duck_A_FULL_ASSEMBLY.glb'))
 (OUT/'reports/assembly_index.json').write_text(json.dumps([dict(name=p['name'],body=p['body'],color=p['color'],kind='printed') for p in parts]+[dict(name=p['name'],body=p['body'],color=p['color'],kind='hardware') for p in hardware],indent=2))
 for h in hardware:
  h['mesh'].export(str(OUT/'hardware'/(h['name']+'.stl')))
  if h['shape'] is not None:cq.exporters.export(h['shape'],str(OUT/'hardware'/(h['name']+'.step')))
 for title,rows in [('print_manifest',inventory),('fasteners_custom_parts',fasteners),('interfaces',interfaces)]:
  (OUT/'reports'/(title+'.json')).write_text(json.dumps(rows,indent=2))
  with open(OUT/'reports'/(title+'.csv'),'w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
 (OUT/'reports/component_envelopes.json').write_text(json.dumps([dict(name=h['name'],bbox=h['mesh'].bounds.round(3).tolist(),body=h['body'],status=h['status']) for h in hardware],indent=2))
 print('Rendering assembly',flush=True)
 render([(p['mesh'],p['color']) for p in [*parts,*hardware] if p['body']!='coupon'],OUT/'renders/01_assembled.png',view=(1,-1,.6),target=(-35,0,217),parallel=260)
 hidden={'head','left_cache','right_cache','head_bot_sheet'}
 show=[p for p in [*parts,*hardware] if p['body']!='coupon' and not any(p['name'].startswith(x) for x in hidden) and not any(x in p['name'] for x in ['cover','fascia','roof','BLANK'])]
 render([(p['mesh'],p['color']) for p in show],OUT/'renders/02_covers_removed.png',view=(-1,-1,.65),target=(-45,0,217),parallel=255)
 show=[p for p in show if p['body']=='trunk_assembly']
 render([(p['mesh'],p['color']) for p in show],OUT/'renders/03_electronics_access.png',view=(-1,-1,1),target=(-99,0,238),parallel=130)
 print('DONE',len(parts),'printed instances',flush=True)
if __name__=='__main__':
 core();base_and_sides();battery();electronics();eyes();foot_contacts();coupons();adapt_vendor_interfaces();export()
