"""Build a colored, full-scale Bambu Studio project from the revision-B manifest.
Native project schema follows BambuStudio's open source bbs_3mf.cpp / PartPlate.cpp.
No printer connection or print submission occurs here.
"""
from pathlib import Path
import json,math,uuid,zipfile,csv,hashlib,xml.etree.ElementTree as ET,sys
import numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];CAD=ROOT/'cad/thenar_duck_B';OUT=CAD/'bambu';OUT.mkdir(exist_ok=True)
if '--sample' in sys.argv:OUT=OUT/'sample';OUT.mkdir(exist_ok=True)
PROFILES=Path('D:/Program Files/Bambu Studio/resources/profiles/BBL')
FILES={f.stem:f for f in PROFILES.rglob('*.json')}
META={'type','name','inherits','include','from','setting_id','instantiation','description','compatible_printers','compatible_printers_condition','compatible_prints','compatible_prints_condition','filament_id','renamed_from'}
def resolve(name,stack=()):
 assert name not in stack,name
 d=json.loads(FILES[name].read_text(encoding='utf-8'));r={}
 if d.get('inherits'):r.update(resolve(d['inherits'],stack+(name,)))
 for inc in d.get('include',[]):r.update(resolve(inc,stack+(name,)))
 r.update(d);return r
machine=resolve('Bambu Lab P1S 0.4 nozzle');process=resolve('0.20mm Standard @BBL X1C')
petg=resolve('Generic PETG');tpu=resolve('Generic TPU')
base=json.loads((ROOT/'cad/development/p1s_native_settings.json').read_text())
for d in [machine,process]:base.update({k:v for k,v in d.items() if k not in META})
COLORS=['#E8EBE5','#26333D','#096DB5','#C4E5F2','#252525']
LABELS=['White PETG','Dark grey PETG','Blue PETG','Translucent PETG','Black TPU - external spool']
filaments=[petg,petg,petg,petg,tpu]
for key in set().union(*(set(f) for f in filaments)):
 if key in META:continue
 values=[f.get(key,base.get(key)) for f in filaments]
 if all(isinstance(v,list) and len(v) for v in values):base[key]=[v[0] for v in values]
base.update({
 'printer_model':'Bambu Lab P1S','printer_variant':'0.4','printer_settings_id':'Bambu Lab P1S 0.4 nozzle',
 'print_settings_id':'Thenar Duck B - PETG 0.20 structural - P1S',
 'filament_settings_id':['Generic PETG']*4+['Generic TPU'],'filament_colour':COLORS,
 'inherits_group':['']*7,'different_settings_to_system':['']*7,
 'flush_volumes_matrix':['0' if i==j else '280' for i in range(5) for j in range(5)],
 'flush_volumes_vector':['140']*10,
 'filament_type':['PETG']*4+['TPU'],'filament_ids':['GFG99']*4+['GFR99'],
 'filament_map':['1']*5,'filament_map_mode':'Auto For Flush','filament_is_support':['0']*5,
 'nozzle_diameter':['0.4'],'curr_bed_type':'Textured PEI Plate','printable_height':'250',
 'layer_height':'0.2','initial_layer_print_height':'0.2','wall_loops':'4',
 'top_shell_layers':'5','bottom_shell_layers':'5','sparse_infill_density':'30%','sparse_infill_pattern':'gyroid',
 'outer_wall_speed':['60','60'],'inner_wall_speed':['90','90'],'sparse_infill_speed':['100','100'],
 'internal_solid_infill_speed':['80','80'],'top_surface_speed':['45','45'],
 'initial_layer_speed':['25','25'],'initial_layer_infill_speed':['35','35'],'bridge_speed':['25','25'],
 'default_acceleration':['3000','3000'],'outer_wall_acceleration':['2000','2000'],
 'enable_support':'1','support_type':'tree(auto)','support_style':'default',
 'support_on_build_plate_only':'1','support_threshold_angle':'30','support_top_z_distance':'0.2',
 'support_object_xy_distance':'0.35','support_filament':'0','support_interface_filament':'0',
 'brim_type':'outer_only','brim_width':'4','brim_object_gap':'0.15',
 'enable_prime_tower':'0','skirt_loops':'0','print_sequence':'by layer','timelapse_type':'0',
 'filament_max_volumetric_speed':['8','8','8','5','3'],
 'filament_notes':['Project role: '+x+'. Select your actual spool profile before printing.' for x in LABELS],
})
# Use machine vendor commands without editing their motion/temperature macros.
(OUT/'resolved_project_settings.json').write_text(json.dumps(base,indent=2))
(OUT/'profile_sources.json').write_text(json.dumps(dict(studio='2.8.2.61',printer='Bambu Lab P1S 0.4 nozzle',source=str(PROFILES),user_confirmed_AMS=True,profiles=['Bambu Lab P1S 0.4 nozzle','0.20mm Standard @BBL X1C','Generic PETG','Generic TPU']),indent=2))
manifest=json.loads((CAD/'reports/print_manifest.json').read_text());index={p['name']:p for p in json.loads((CAD/'reports/assembly_index.json').read_text())}

def color_for(p):
 if p['material']=='TPU':return 5
 if 'translucent' in p['material']:return 4
 c=index[p['part']]['color']
 if min(c)>.7:return 1
 if c[2]>.5 and c[0]<.2:return 3
 return 2

def oriented(p):
 m=trimesh.load_mesh(CAD/'stl'/(p['part']+'.stl'));reason='CAD print orientation retained'
 if p['part']=='head_1':
  m.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]));reason='Roof down; open underside faces up for support access'
 if p['material']=='TPU':
  m.apply_transform(trimesh.transformations.rotation_matrix(math.pi,[1,0,0]));reason='Flat mounting face down; curved ground-contact face up to avoid unsupported rim'
 if p['part'].startswith(('left_cache','right_cache')):
  # The broad closed face is a Y plane. Select its outward normal using facet area.
  mask=np.abs(m.face_normals[:,1])>.999
  sign=1 if m.area_faces[mask & (m.face_normals[:,1]>0)].sum()>m.area_faces[mask & (m.face_normals[:,1]<0)].sum() else -1
  m.apply_transform(trimesh.transformations.rotation_matrix(-sign*math.pi/2,[1,0,0]));reason='Broad closed side down; hip cover height reduced to40mm'
 m.apply_translation(-m.bounds[0]);assert m.is_watertight and m.volume>0
 return m,reason

objects=[]
if '--sample' in sys.argv:manifest=[p for p in manifest if p['part']=='C04_servo_horn_pattern_gauge']
for p in manifest:
 m,reason=oriented(p);fil=color_for(p)
 role='coupon' if p['part'].startswith(('C01','C02','C03','C04')) else 'alternative' if p['part'].startswith(('C05','C06')) else 'installed'
 for copy in range(p['quantity']):objects.append(dict(part=p['part'],copy=copy+1,mesh=m.copy(),filament=fil,role=role,orientation=reason,material=p['material']))

# Rectangular footprint packing with 6mm around each object for a4mm brim.
# The complete y<34 band is reserved, including the18x28 cutter exclusion.
PAD=6;X0=5;Y0=34;W=246;H=217
plates=[]
def pack_group(group,label):
 local=[]
 for o in sorted(group,key=lambda o:float(np.prod(o['mesh'].extents[:2])),reverse=True):
  best=None
  for plate in local:
   for ri,(x,y,w,h) in enumerate(plate['free']):
    for turn in [0,1]:
     dims=o['mesh'].extents;pw=float(dims[turn]+PAD*2);ph=float(dims[1-turn]+PAD*2)
     if pw<=w+1e-5 and ph<=h+1e-5:
      score=(min(w-pw,h-ph),w*h-pw*ph)
      if best is None or score<best[0]:best=(score,plate,ri,turn,pw,ph)
  if best is None:
   plate=dict(label=label,filament=o['filament'],role=o['role'],free=[(X0,Y0,W,H)],objects=[])
   local.append(plate)
   for turn in [0,1]:
    dims=o['mesh'].extents;pw=float(dims[turn]+PAD*2);ph=float(dims[1-turn]+PAD*2)
    if pw<=W and ph<=H:best=((0,0),plate,0,turn,pw,ph);break
   assert best is not None,('Does not fit stock P1S with clearance',o['part'],o['mesh'].extents)
  _,plate,ri,turn,pw,ph=best;x,y,w,h=plate['free'].pop(ri)
  if turn:o['mesh'].apply_transform(trimesh.transformations.rotation_matrix(math.pi/2,[0,0,1]));o['mesh'].apply_translation(-o['mesh'].bounds[0])
  o.update(x=x+PAD,y=y+PAD,packing_z_rotation=turn*90)
  plate['objects'].append(o)
  # Non-overlapping guillotine leftovers.
  if w-pw>.1:plate['free'].append((x+pw,y,w-pw,ph))
  if h-ph>.1:plate['free'].append((x,y+ph,w,h-ph))
 for i,p in enumerate(local):p['name']=label+(' '+str(i+1) if len(local)>1 else '')
 plates.extend(local)
for role in ['coupon','installed','alternative']:
 for fil in [3,2,1,4,5]:
  group=[o for o in objects if o['role']==role and o['filament']==fil]
  if group:pack_group(group,('TEST FIRST - ' if role=='coupon' else 'OPTIONAL - ' if role=='alternative' else '')+LABELS[fil-1])
assert len(plates)<=36

CORE='http://schemas.microsoft.com/3dmanufacturing/core/2015/02';PROD='http://schemas.microsoft.com/3dmanufacturing/production/2015/06';BAMBU='http://schemas.bambulab.com/package/2021'
ET.register_namespace('',CORE);ET.register_namespace('p',PROD);ET.register_namespace('BambuStudio',BAMBU)
def sub(parent,tag,**attrs):return ET.SubElement(parent,'{'+CORE+'}'+tag,{k:str(v) for k,v in attrs.items()})
def meta(parent,key,value):ET.SubElement(parent,'metadata',{'key':key,'value':str(value)})
def xml(element):return ET.tostring(element,encoding='utf-8',xml_declaration=True)
root=ET.Element('{'+CORE+'}model',{'unit':'millimeter','{http://www.w3.org/XML/1998/namespace}lang':'en-US','requiredextensions':'p'})
root.set('xmlns:BambuStudio',BAMBU)
for k,v in [('Application','BambuStudio-02.08.02.61'),('BambuStudio:3mfVersion','1'),('Title','Thenar Duck B - P1S 0.4 AMS - all parts'),('Description','Full scale; installed parts, fit coupons and optional alternatives on separate named plates. Generic filament profiles: select actual spool profiles before printing.')]:sub(root,'metadata',name=k).text=v
res=sub(root,'resources');build=sub(root,'build');build.set('{'+PROD+'}UUID',str(uuid.uuid4()))
settings=ET.Element('config');rels=ET.Element('Relationships',xmlns='http://schemas.openxmlformats.org/package/2006/relationships')
plate_manifest=[];members={};counter=0;cols=math.ceil(math.sqrt(len(plates)))
for pi,plate in enumerate(plates):
 plate_el=ET.SubElement(settings,'plate');meta(plate_el,'plater_id',pi+1);meta(plate_el,'plater_name',plate['name']);meta(plate_el,'locked','false')
 meta(plate_el,'filament_map_mode','Auto For Flush')
 origin=((pi%cols)*307.2,-(pi//cols)*307.2)
 for o in plate['objects']:
  counter+=1;partid=counter*2-1;oid=counter*2;o['id']=oid;o['plate']=pi+1
  name=o['part']+('_copy'+str(o['copy']) if o['copy']>1 else '')
  path='3D/Objects/object_'+str(counter)+'.model'
  obj=sub(res,'object',id=oid,type='model');obj.set('{'+PROD+'}UUID',str(uuid.uuid4()));comp=sub(sub(obj,'components'),'component',objectid=partid,transform='1 0 0 0 1 0 0 0 1 0 0 0');comp.set('{'+PROD+'}path','/'+path);comp.set('{'+PROD+'}UUID',str(uuid.uuid4()))
  item=sub(build,'item',objectid=oid,transform=f'1 0 0 0 1 0 0 0 1 {origin[0]+o["x"]:.6f} {origin[1]+o["y"]:.6f} 0',printable=1);item.set('{'+PROD+'}UUID',str(uuid.uuid4()))
  child=ET.Element('{'+CORE+'}model',{'unit':'millimeter','requiredextensions':'p','xmlns:BambuStudio':BAMBU});sub(child,'metadata',name='BambuStudio:3mfVersion').text='1';co=sub(sub(child,'resources'),'object',id=partid,type='model');co.set('{'+PROD+'}UUID',str(uuid.uuid4()));me=sub(co,'mesh');ve=sub(me,'vertices');tr=sub(me,'triangles');sub(child,'build')
  m=o['mesh']
  for v in m.vertices:sub(ve,'vertex',x=f'{v[0]:.7f}',y=f'{v[1]:.7f}',z=f'{v[2]:.7f}')
  for f in m.faces:sub(tr,'triangle',v1=f[0],v2=f[1],v3=f[2])
  members[path]=xml(child)
  ET.SubElement(rels,'Relationship',Target='/'+path,Id='rel-'+str(counter),Type='http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel')
  obj_cfg=ET.SubElement(settings,'object',id=str(oid));meta(obj_cfg,'name',name);meta(obj_cfg,'extruder',o['filament'])
  if o['role']!='installed' or o['filament'] in [4,5]:meta(obj_cfg,'enable_support','0')
  if o['filament']==4:meta(obj_cfg,'sparse_infill_density','100%');meta(obj_cfg,'sparse_infill_pattern','rectilinear');meta(obj_cfg,'wall_loops','3')
  if o['filament']==5:
   for k,v in dict(wall_loops='3',sparse_infill_density='20%',brim_type='no_brim',outer_wall_speed='30,30',inner_wall_speed='30,30',sparse_infill_speed='30,30',top_surface_speed='25,25').items():meta(obj_cfg,k,v)
  part=ET.SubElement(obj_cfg,'part',id=str(partid),subtype='normal_part');meta(part,'name',name);meta(part,'matrix','1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1');meta(part,'source_file',o['part']+'.stl')
  ET.SubElement(part,'mesh_stat',face_count=str(len(m.faces)),edges_fixed='0',degenerate_facets='0',facets_removed='0',facets_reversed='0',backwards_edges='0')
  instance=ET.SubElement(plate_el,'model_instance');meta(instance,'object_id',oid);meta(instance,'instance_id',0);meta(instance,'identify_id',counter)
  plate_manifest.append(dict(plate=pi+1,plate_name=plate['name'],object_id=oid,part=o['part'],copy=o['copy'],role=o['role'],filament=o['filament'],color=COLORS[o['filament']-1],material=o['material'],x_mm=round(o['x'],4),y_mm=round(o['y'],4),size_mm=m.extents.round(4).tolist(),orientation=o['orientation'],packing_z_rotation=o['packing_z_rotation'],stl_sha256=hashlib.sha256((CAD/'stl'/(o['part']+'.stl')).read_bytes()).hexdigest()))
settings[:]=list(settings.findall('object'))+list(settings.findall('plate'))
members['3D/3dmodel.model']=xml(root);members['3D/_rels/3dmodel.model.rels']=xml(rels);members['Metadata/model_settings.config']=xml(settings);members['Metadata/project_settings.config']=json.dumps(base,indent=2).encode()
members['[Content_Types].xml']=b'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/><Default Extension="config" ContentType="text/xml"/><Default Extension="png" ContentType="image/png"/></Types>'
members['_rels/.rels']=b'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/></Relationships>'
with zipfile.ZipFile(OUT/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf','w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for n,data in members.items():z.writestr(n,data)
(OUT/'plate_manifest.json').write_text(json.dumps(plate_manifest,indent=2))
with open(OUT/'plate_manifest.csv','w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=plate_manifest[0]);w.writeheader();w.writerows(plate_manifest)
# Independent placement assertions, including margins for brim and the stock cutter area.
for pi,plate in enumerate(plates):
 boxes=[]
 for o in plate['objects']:
  w,h,z=o['mesh'].extents;x,y=o['x'],o['y'];assert x-PAD>=0 and y-PAD>=28 and x+w+PAD<=256 and y+h+PAD<=256 and z<=250
  box=(x-PAD,y-PAD,x+w+PAD,y+h+PAD)
  for other in boxes:assert min(box[2],other[2])-max(box[0],other[0])<=1e-5 or min(box[3],other[3])-max(box[1],other[1])<=1e-5
  boxes.append(box)
report=dict(printer='Bambu Lab P1S',nozzle_mm=.4,AMS=True,plates=len(plates),objects=counter,unique_stl_files=len(manifest),installed_objects=sum(o['role']=='installed' for o in objects),alternative_objects=sum(o['role']=='alternative' for o in objects),coupon_objects=sum(o['role']=='coupon' for o in objects),scale=1,bed_mm=[256,256,250],stock_exclusion_mm=[0,0,18,28],all_parts_and_reserved_brim_margin_inside=True,all_padded_footprints_nonoverlapping=True,filament_roles=dict(zip(range(1,6),LABELS)),note='Geometric placement proof; native slicer validation recorded separately')
(OUT/'placement_validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2),flush=True)
