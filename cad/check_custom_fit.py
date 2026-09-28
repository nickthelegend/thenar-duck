"""Exact BREP intersection checks for the new electronics/chassis parts."""
import build_duck as b,json,numpy as np
b.base_and_sides();b.battery();b.electronics();b.eyes();b.coupons()
objects=[p for p in b.parts if p['body']=='trunk_assembly']+[p for p in b.hardware if p['body']=='trunk_assembly']
rows=[]
for i,a in enumerate(objects):
 for c in objects[i+1:]:
  if a in b.hardware and c in b.hardware:continue
  aa,cc=a['mesh'].bounds,c['mesh'].bounds
  if np.any(np.minimum(aa[1],cc[1])-np.maximum(aa[0],cc[0])<.01):continue
  v=a['shape'].intersect(c['shape']).Volume()
  if v>.05:rows.append(dict(a=a['name'],b=c['name'],overlap_mm3=round(v,3)))
print(json.dumps(rows,indent=2));(b.OUT/'reports/custom_intersections.json').write_text(json.dumps(rows,indent=2))
b.render([(p['mesh'],p['color']) for p in objects if not any(x in p['name'] for x in ['cover','fascia','roof','BLANK'])],b.OUT/'renders/00_rack_development.png',target=(-85,0,240),parallel=145,view=(-1,-1,1))
