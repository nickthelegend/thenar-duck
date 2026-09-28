"""Build labelled review indices and hardware STEP envelopes from the completed GLB.
Also used after an export made by an earlier version of build_duck.py.
"""
import json,collections,trimesh
import build_duck as b
from inspect_reference import load
refs,_=load();index={};counts=collections.Counter()
for p in refs:
 counts[p['name']]+=1;n=p['name']+'_'+str(counts[p['name']]);index[n]=dict(name=n,body=p['body'],color=p['color'][:3],kind='reference')
b.base_and_sides();b.battery();b.electronics();b.eyes();b.foot_contacts();b.coupons()
for p in b.parts:index[p['name']]=dict(name=p['name'],body=p['body'],color=list(p['color']),kind='printed')
for p in b.hardware:index[p['name']]=dict(name=p['name'],body=p['body'],color=list(p['color']),kind='hardware')
scene=trimesh.load_scene(b.OUT/'Thenar_Duck_A_FULL_ASSEMBLY.glb')
missing=[n for n in scene.geometry if n not in index]
assert not missing,missing
(b.OUT/'reports/assembly_index.json').write_text(json.dumps([index[n] for n in scene.geometry],indent=2))
for h in b.hardware:
 b.cq.exporters.export(h['shape'],str(b.OUT/'hardware'/(h['name']+'.step')))
for n,m in scene.geometry.items():m.export(str(b.OUT/'hardware'/(n+'.stl')))
print('Indexed',len(scene.geometry),'instances')
