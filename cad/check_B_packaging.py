"""Exact static and sampled service checks for revision B packaging."""
import build_duck_B as b,json,numpy as np
b.base_and_sides();b.battery();b.service_pod();b.electronics();b.chest_lights()
objects=[p for p in b.parts+b.hardware if p['body']=='trunk_assembly']
rows=[]
for i,a in enumerate(objects):
 for c in objects[i+1:]:
  if a in b.hardware and c in b.hardware:continue
  aa,cc=a['mesh'].bounds,c['mesh'].bounds
  if np.any(np.minimum(aa[1],cc[1])-np.maximum(aa[0],cc[0])<.01):continue
  v=a['shape'].intersect(c['shape']).Volume()
  if v>.05:rows.append(dict(a=a['name'],b=c['name'],overlap_mm3=round(v,3)))
(b.OUT/'reports/custom_intersections.json').write_text(json.dumps(rows,indent=2));print('Static contacts',rows,flush=True)
def test(label,moving,removed,translations):
 obstacles=[p for p in objects if p['name'] not in moving|removed];movers=[p for p in objects if p['name'] in moving];hits=[]
 for delta in translations:
  for m in movers:
   s=m['shape'].translate(delta);bb=s.BoundingBox();lo=np.array([bb.xmin,bb.ymin,bb.zmin]);hi=np.array([bb.xmax,bb.ymax,bb.zmax])
   for p in obstacles:
    bd=p['mesh'].bounds
    if np.any(np.minimum(hi,bd[1])-np.maximum(lo,bd[0])<.02):continue
    v=s.intersect(p['shape']).Volume()
    if v>.1:hits.append(dict(moving=m['name'],obstacle=p['name'],translation=delta,overlap_mm3=round(v,3)))
 return dict(test=label,removed_first=sorted(removed),positions_sampled=len(translations),collisions=hits,scope='New torso and envelopes; fixed core/head and flexible wires excluded')
pi={p['name'] for p in objects if p['name'].startswith('Pi4_') or p['name'] in ['Raspberry_Pi_4B_PCB','B10_Pi4B_removable_tray']}
roof={'B07_lift_off_roof'}
pod={p['name'] for p in objects if p['name'].startswith('B06') or p['name'] in ['Fuse_holder_capacity_45x24x24','Switch_terminal_reserved_volume']}
imu={p['name'] for p in objects if p['name'].startswith('IMU_header_') or p['name'] in ['B11_SEN0374_side_bridge','DFRobot_SEN0374_PCB']}
results=[test('Pi lift45 then rear withdrawal',pi,roof,[(0,0,z) for z in [0,5,15,30,45]]+[(-x,0,45) for x in [20,60,120]]),test('Battery rear withdrawal',{'BK4200_3S_published_137x44x27'},pod|{'B05_rear_service_cover','Battery_rear_connector_keepout'},[(-x,0,0) for x in [0,10,30,70,110,160]]),test('IMU vertical lift after Pi removal',imu,pi|roof,[(0,0,z) for z in [0,5,15,30,50,75]])]
(b.OUT/'reports/service_paths.json').write_text(json.dumps(results,indent=2));print('Service paths',json.dumps(results),flush=True)
b.render([(p['mesh'],p['color']) for p in objects if not any(x in p['name'] for x in ['cover','fascia','roof','rocker'])],b.OUT/'renders/00_packaging_check.png',target=(-85,0,235),parallel=155,view=(-1,-1,1))
