"""Apply a subtractive eye-cap clearance revision without regenerating unchanged parts."""
import build_duck_B as b,json,csv,numpy as np
b.eyes(False);out=b.OUT
idx=json.loads((out/'reports/assembly_index.json').read_text());lookup={p['name']:p for p in idx}
manifest=json.loads((out/'reports/print_manifest.json').read_text())
scene=b.trimesh.load_scene(out/'Thenar_Duck_B_FULL_ASSEMBLY.glb')
for p in b.parts:
 n=p['name']
 if not n.startswith('B12'):continue
 s=p['shape'];s.exportBrep(str(out/'brep'/(n+'.brep')));b.cq.exporters.export(s,str(out/'step'/(n+'.step')))
 assert b.cq.Shape.importBrep(str(out/'brep'/(n+'.brep'))).isValid()
 pm=p['mesh'].copy();pm.apply_transform(b.trimesh.transformations.rotation_matrix(np.pi/2,[0,1,0]));pm.apply_translation(-pm.bounds[0]);pm,repair=b.prepare_mesh(pm);pm.export(out/'stl'/(n+'.stl'))
 m=p['mesh'].copy();m.visual.face_colors=np.array([*p['color'][:3],1])*255
 scene.geometry[n]=m
 row=next(x for x in manifest if x['part']==n);row['size_mm']=[round(float(v),2) for v in pm.extents];row['solid_volume_cm3']=round(s.Volume()/1000,2);row['notes']='Upper inner corner relieved for faceted shell; wire notch fully intersects centre opening'
 print('Updated',n,flush=True)
scene.export(out/'Thenar_Duck_B_FULL_ASSEMBLY.glb')
(out/'reports/print_manifest.json').write_text(json.dumps(manifest,indent=2))
with open(out/'reports/print_manifest.csv','w',newline='',encoding='utf-8-sig') as f:
 w=csv.DictWriter(f,fieldnames=manifest[0].keys());w.writeheader();w.writerows(manifest)
assy=b.cq.Assembly(name='Thenar_Duck_B_REVIEW')
for p in manifest:
 if lookup[p['part']]['body']=='coupon':continue
 s=b.cq.Shape.importBrep(str(out/'brep'/(p['part']+'.brep')));assy.add(s,name=p['part'],color=b.cq.Color(*lookup[p['part']]['color']))
print('Rebuilding printed-parts STEP',flush=True);assy.save(str(out/'Thenar_Duck_B_PRINTED_PARTS.step'))
print('DONE',flush=True)
