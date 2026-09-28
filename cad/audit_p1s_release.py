"""Audit native 3MF membership, scale, color, slice results and deposited paths.
Render an overview from meshes actually read back from the delivered project.
"""
from pathlib import Path
import json,zipfile,xml.etree.ElementTree as ET,math,re,hashlib,collections,csv
import numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
from render_meshes import render
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'cad/thenar_duck_B/bambu'
manifest=json.loads((P/'plate_manifest.json').read_text());plates=collections.defaultdict(list)
def name(o):return o['part']+('_copy'+str(o['copy']) if o['copy']>1 else '')
expected={name(o):o for o in manifest}
for o in manifest:plates[o['plate']].append(o)
cols=math.ceil(math.sqrt(len(plates)))
def origin(n):return np.array([((n-1)%cols)*307.2,-((n-1)//cols)*307.2,0])
def matrix(text):
 m=np.eye(4)
 if text:m[:3,:]=np.array(list(map(float,text.split()))).reshape(4,3).T
 return m
C='{http://schemas.microsoft.com/3dmanufacturing/core/2015/02}';Q='{http://schemas.microsoft.com/3dmanufacturing/production/2015/06}'
def metadata(e):return {v.get('key'):v.get('value') for v in e.findall('metadata') if v.get('key')}
native=P/'Thenar_Duck_B_P1S_ALL_PARTS.3mf';renders=collections.defaultdict(list)
with zipfile.ZipFile(native) as z:
 settings=json.loads(z.read('Metadata/project_settings.config'));config=ET.fromstring(z.read('Metadata/model_settings.config'))
 assert settings['printer_settings_id']=='Bambu Lab P1S 0.4 nozzle'
 assert settings['nozzle_diameter']==['0.4'] and settings['printable_height']=='250'
 assert settings['filament_type']==['PETG']*4+['TPU']
 configs={o.get('id'):metadata(o) for o in config.findall('object')};membership={}
 for p in config.findall('plate'):
  pn=int(metadata(p)['plater_id'])
  for inst in p.findall('model_instance'):membership[metadata(inst)['object_id']]=pn
 root=ET.fromstring(z.read('3D/3dmodel.model'));assert root.get('unit')=='millimeter'
 objects={o.get('id'):o for o in root.findall(C+'resources/'+C+'object')};seen=[]
 for item in root.findall(C+'build/'+C+'item'):
  oid=item.get('objectid');nm=configs[oid]['name'];o=expected[nm];seen.append(nm)
  assert int(configs[oid]['extruder'])==o['filament'] and membership[oid]==o['plate']
  assert settings['filament_colour'][o['filament']-1].lower()==o['color'].lower()
  component=objects[oid].find(C+'components/'+C+'component')
  child=ET.fromstring(z.read(component.get(Q+'path').lstrip('/')))
  mesh=child.find(C+'resources/'+C+'object/'+C+'mesh')
  verts=np.array([[float(v.get(k)) for k in ['x','y','z']] for v in mesh.find(C+'vertices')])
  faces=np.array([[int(v.get(k)) for k in ['v1','v2','v3']] for v in mesh.find(C+'triangles')])
  transform=matrix(item.get('transform'))@matrix(component.get('transform'))
  assert np.allclose(np.linalg.svd(transform[:3,:3])[1],1,atol=1e-6),'Unexpected scale'
  m=trimesh.Trimesh(verts,faces,process=False);m.apply_transform(transform);m.apply_translation(-origin(o['plate']))
  assert np.allclose(m.bounds[0],[o['x_mm'],o['y_mm'],0],atol=.002),(nm,m.bounds)
  assert np.allclose(m.extents,o['size_mm'],atol=.002)
  assert m.is_watertight and m.volume>0
  renders[o['plate']].append((m,trimesh.visual.color.hex_to_rgba(o['color'])[:3]/255))
 assert sorted(seen)==sorted(expected)

initial=json.loads((P/'validation/result.json').read_text());assert initial['return_code']==0
sliceplates={p['id']:p for p in initial['sliced_plates']};corrected=P/'validation/plate17_corrected/result.json'
project_hash=hashlib.sha256(native.read_bytes()).hexdigest()
full_stamp=P/'validation/full_run_project_sha256.txt'
use_corrected=corrected.exists() and (not full_stamp.exists() or full_stamp.read_text().strip()!=project_hash)
if use_corrected:
 assert (corrected.parent/'project_sha256.txt').read_text().strip()==project_hash,'Correction evidence belongs to a different project; run full validation again'
 correction=json.loads(corrected.read_text());assert correction['return_code']==0
 sliceplates.update({p['id']:p for p in correction['sliced_plates']})
else:
 assert full_stamp.read_text().strip()==project_hash,'Run native slice validation for the current project'
assert sorted(sliceplates)==list(range(1,20))
summary=[]
for pn,items in plates.items():
 sp=sliceplates[pn];assert not sp['warning_message'],sp['warning_message']
 assert sorted(o['name'] for o in sp['objects'])==sorted(name(o) for o in items)
 for so in sp['objects']:
  o=expected[so['name']];b=so['bbox'];local=np.array([b['x'],b['y'],b['z']])-origin(pn)
  assert np.allclose(local,[o['x_mm'],o['y_mm'],0],atol=.003)
  assert np.allclose([b['width'],b['depth'],b['height']],o['size_mm'],atol=.003)
 assert len(sp['filaments'])==1 and sp['filaments'][0]['id']==items[0]['filament']
 assert sp['filament_change_times']==0
 gcode=P/f'validation/plate_{pn}.gcode'
 if pn==17 and use_corrected:gcode=corrected.parent/'plate_17.gcode'
 # Bound model, brim and support deposition, excluding vendor start/end purge moves.
 active=False;relative=True;pos=np.zeros(3);previous_e=0.;width=.5;low=np.ones(3)*np.inf;high=-low;segments=0;arcs=0
 for raw in gcode.open(encoding='utf-8'):
  if raw.startswith('; FEATURE: '):active=raw.strip()!='; FEATURE: Custom'
  if raw.startswith('; LINE_WIDTH: '):width=float(raw.split(':')[1])
  line=raw.split(';')[0].strip()
  if line=='M83':relative=True
  if line=='M82':relative=False
  if line.startswith('G92 E'):previous_e=float(line[5:])
  if not re.match(r'^G[0123] ',line):continue
  args={k:float(v) for k,v in re.findall(r'([XYZEFIJP])([-+]?\d*\.?\d+)',line)};nxt=pos.copy()
  for i,k in enumerate('XYZ'):
   if k in args:nxt[i]=args[k]
  de=args.get('E',0) if relative else args.get('E',previous_e)-previous_e
  if 'E' in args:previous_e=args['E']
  if active and de>0 and np.linalg.norm(nxt[:2]-pos[:2])>1e-7:
   points=[pos.copy(),nxt.copy()]
   if line.startswith(('G2 ','G3 ')):
    arcs+=1;center=pos[:2]+np.array([args.get('I',0),args.get('J',0)]);radius=np.linalg.norm(pos[:2]-center)
    a=math.atan2(pos[1]-center[1],pos[0]-center[0]);b=math.atan2(nxt[1]-center[1],nxt[0]-center[0]);cw=line.startswith('G2 ')
    sweep=(a-b)%(2*math.pi) if cw else (b-a)%(2*math.pi)
    for angle in [0,math.pi/2,math.pi,math.pi*1.5]:
     offset=(a-angle)%(2*math.pi) if cw else (angle-a)%(2*math.pi)
     if offset<=sweep+1e-7:points.append(np.array([center[0]+radius*math.cos(angle),center[1]+radius*math.sin(angle),nxt[2]]))
   pts=np.array(points);low=np.minimum(low,pts.min(0)-[width/2,width/2,0]);high=np.maximum(high,pts.max(0)+[width/2,width/2,0]);segments+=1
  pos=nxt
 assert segments>0 and np.all(low>=[0,28,0]) and np.all(high<=[256,256,250]),(pn,low,high)
 summary.append(dict(plate=pn,name=items[0]['plate_name'],role=items[0]['role'],objects=len(items),filament=items[0]['filament'],grams=round(sp['filaments'][0]['total_used_g'],1),hours=round(sp['total_predication']/3600,2),warning='',deposition_bounds_mm=[low.round(3).tolist(),high.round(3).tolist()],extrusion_segments=segments,arc_segments=arcs))
note=('Initial full run succeeded; sole warning corrected by flipping TPU pieces and re-slicing plate17. Other plates unchanged. ' if use_corrected else 'Full native slice run succeeded. ')+'Start/end machine purge paths excluded from deposition bound check. Physical printing and strength not validated.'
report=dict(project=native.name,sha256=project_hash,native_objects_verified=94,plates_verified=19,colors_verified=5,full_scale=True,all_plates_sliced=True,no_remaining_slice_warnings=True,all_model_support_brim_paths_inside_stock_bed=True,sources=['validation/result.json']+(['validation/plate17_corrected/result.json'] if use_corrected else []),note=note,plates=summary)
(P/'release_validation.json').write_text(json.dumps(report,indent=2))
with (P/'slice_estimates.csv').open('w',newline='',encoding='utf-8-sig') as f:
 fields=['plate','name','role','objects','filament','grams','hours'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(summary)
md='# P1S release checks\n\n'
md+='Native Bambu Studio 2.8.2.61 export and local slicing completed successfully. **19/19 plates, 94/94 objects, no remaining slicer warnings.** No physical print was started.\n\n'
if use_corrected:md+='The initial full slice flagged a curved TPU rim. Both soles were flipped onto their flat mounting face; plate17 was re-sliced successfully without that warning. The other 18 plates were unchanged. The original and corrected result records are retained, and `release_validation.json` consolidates them.\n\n'
md+='Checks read the delivered native project back, including all meshes, scale, positions, plate membership and color assignments. Deposited model/support/brim paths, including XY arc extrema and line-width margins, remain within the stock bed and clear of the front cutter area. Vendor start/end purge moves are outside this geometric check. This is not a mechanical load test or physical fit guarantee.\n\n'
md+='SHA-256: `'+report['sha256']+'`\n\n## Slicer estimates\n\nThese use generic filament profiles and include supports/brims. They are estimates; actual spools, calibration and printer overhead change the result. Optional parts are included only in their own total.\n\n| Selection | Filament g | Estimated hours |\n|---|---:|---:|\n'
for role in ['coupon','installed','alternative']:
 rows=[s for s in summary if s['role']==role];md+=f'| {role} | {sum(s["grams"] for s in rows):.1f} | {sum(s["hours"] for s in rows):.2f} |\n'
md+='\nSee `slice_estimates.csv` for each plate. Select actual material profiles and inspect Preview before printing. TPU uses the external spool; filament5 is a project role, not an AMS slot.\n'
(P/'RELEASE_CHECKS.md').write_text(md)
print(json.dumps({k:v for k,v in report.items() if k!='plates'},indent=2),flush=True)

# A native-mesh overview, not a synthetic concept image.
thumbs=P/'plate_previews';thumbs.mkdir(exist_ok=True)
fontpath='C:/Windows/Fonts/arial.ttf';boldpath='C:/Windows/Fonts/arialbd.ttf'
titlefont=ImageFont.truetype(boldpath,34);font=ImageFont.truetype(fontpath,19);small=ImageFont.truetype(fontpath,17)
sheet=Image.new('RGB',(1920,2170),'#f1f4f7');draw=ImageDraw.Draw(sheet)
draw.text((32,22),'THENAR DUCK / REVISION B',font=titlefont,fill='#122c40')
draw.text((32,68),'P1S 0.4 mm  |  Full scale  |  19 plates  |  79 installed + 6 tests + 9 alternatives',font=font,fill='#294356')
draw.text((32,100),'PETG: white / dark grey / blue / translucent via AMS. Black TPU: external spool.',font=font,fill='#294356')
for n,items in plates.items():
 bed=trimesh.creation.box(extents=[256,256,1]);bed.apply_translation([128,128,-.7])
 exclusion=trimesh.creation.box(extents=[18,28,.3]);exclusion.apply_translation([9,14,0])
 png=thumbs/f'plate_{n:02}.png'
 render([(bed,(.78,.82,.85)),(exclusion,(.9,.25,.25))]+renders[n],png,size=(460,310),view=(.15,-1,1.5),target=(128,128,5),parallel=190)
 x=20+((n-1)%4)*475;y=154+((n-1)//4)*398
 draw.rounded_rectangle((x,y,x+460,y+380),radius=12,fill='white')
 title=items[0]['plate_name'].replace(' - external spool','').replace('TEST FIRST - ','TEST / ').replace('OPTIONAL - ','OPTION / ')
 draw.text((x+12,y+10),f'{n:02}  {title}',font=font,fill='#122c40')
 sheet.paste(Image.open(png),(x,y+43));s=summary[n-1]
 draw.text((x+12,y+349),f'{len(items)} objects  /  {s["grams"]:.0f} g  /  {s["hours"]:.1f} h estimated',font=small,fill='#486171')
sheet.save(P/'plate_overview.png')
print('Rendered plate overview',flush=True)
