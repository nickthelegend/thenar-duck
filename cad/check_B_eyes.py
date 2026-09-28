"""Nominal eye insert/retainer solids against the rebuilt head socket."""
import build_duck_B as b,json,numpy as np
b.eyes(False)
head=b.cq.Shape.importBrep(str(b.OUT/'brep/head_1.brep'))
objects=[dict(name='head_1',shape=head,mesh=b.mesh(head))]+[p for p in b.parts+b.hardware if p['body']=='head_assembly']
hits=[];tested=0
for i,p in enumerate(objects):
 for q in objects[i+1:]:
  if np.any(np.minimum(p['mesh'].bounds[1],q['mesh'].bounds[1])-np.maximum(p['mesh'].bounds[0],q['mesh'].bounds[0])<.01):continue
  v=p['shape'].intersect(q['shape']).Volume();tested+=1
  if v>.1:hits.append(dict(a=p['name'],b=q['name'],overlap_mm3=round(v,3)))
  print(p['name'],q['name'],v,flush=True)
report=dict(scope='Exact neutral head/socket/retainer/sleeve/diffuser/default ring intersections; excludes wires and LED packages',pairs_tested=tested,contacts=hits)
(b.OUT/'reports/eye_fit.json').write_text(json.dumps(report,indent=2));print(report,flush=True)
