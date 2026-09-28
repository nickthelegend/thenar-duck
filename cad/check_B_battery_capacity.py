"""Check the full advertised battery capacity, beyond the nominal pack example."""
import build_duck_B as b,json,numpy as np
scene=b.trimesh.load_scene(b.OUT/'Thenar_Duck_B_FULL_ASSEMBLY.glb')
idx=json.loads((b.OUT/'reports/assembly_index.json').read_text())
s=b.box(-190,-50,-25,25,182.31499,214.31499);lo=np.array([-190,-25,182.31499]);hi=np.array([-50,25,214.31499]);hits=[];tested=0
for p in idx:
 n=p['name']
 if n not in scene.geometry or n.startswith(('BK4200','Battery_rear')):continue
 m=scene.geometry[n]
 if np.any(np.minimum(hi,m.bounds[1])-np.maximum(lo,m.bounds[0])<.02):continue
 path=b.OUT/('brep' if p['kind']=='printed' else 'hardware')/(n+('.brep' if p['kind']=='printed' else '.step'))
 q=b.cq.Shape.importBrep(str(path)) if p['kind']=='printed' else b.cq.importers.importStep(str(path)).val()
 v=s.intersect(q).Volume();tested+=1;print(n,v,flush=True)
 if v>.1:hits.append(dict(obstacle=n,overlap_mm3=round(v,3)))
report=dict(capacity_mm=[140,50,32],pad_mm=2,scope='Maximum pack box against all exported printed and hardware solids in neutral; excludes wires and fasteners',candidate_pairs=tested,contacts=hits)
(b.OUT/'reports/battery_capacity.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
