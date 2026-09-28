"""Exact sampled rigid insertion/removal of the new torso hardware envelopes."""
import json,numpy as np
import build_duck as b
b.base_and_sides();b.battery();b.electronics()
allparts=b.parts+b.hardware
def test(label,moving,removed,translations):
 obstacles=[p for p in allparts if p['name'] not in moving|removed]
 movers=[p for p in allparts if p['name'] in moving];hits=[]
 for delta in translations:
  for m in movers:
   s=m['shape'].translate(delta);bb=s.BoundingBox();lo=np.array([bb.xmin,bb.ymin,bb.zmin]);hi=np.array([bb.xmax,bb.ymax,bb.zmax])
   for p in obstacles:
    bnd=p['mesh'].bounds
    if np.any(np.minimum(hi,bnd[1])-np.maximum(lo,bnd[0])<.02):continue
    vol=s.intersect(p['shape']).Volume()
    if vol>.1:hits.append(dict(moving=m['name'],obstacle=p['name'],translation=delta,overlap_mm3=round(vol,2)))
 return dict(test=label,removed_first=sorted(removed),positions_sampled=len(translations),collisions=hits,scope='New torso printed parts and nominal hardware envelopes; plugs/cables and moving head are outside this test')
pi={p['name'] for p in allparts if p['name'].startswith('Pi4_') or p['name'] in ['Raspberry_Pi_4B_PCB','A10_Pi4B_removable_tray']}
results=[test('Pi tray lift then rear withdrawal',pi,{'A07_lift_off_roof'},[(0,0,z) for z in [0,5,15,30,45]]+[(-x,0,45) for x in [20,60,120]])]
results.append(test('Battery rear withdrawal',{'BK_3S_BATTERY_MAX_RESERVED'},{'A05_rear_service_cover','A06_switch_plate_BLANK'},[(-x,0,0) for x in [0,10,30,70,110,160]]))
results.append(test('IMU bridge lift 35 then slide rear 80 after Pi removal',{'A11_SEN0374_fixed_IMU_bridge','DFRobot_SEN0374_PCB','IMU_header_-9','IMU_header_9'},pi|{'A07_lift_off_roof'},[(0,0,z) for z in [0,10,20,35]]+[(-x,0,35) for x in [20,40,60,80]]+[(-80,0,z) for z in [50,75]]))
(b.OUT/'reports/service_paths.json').write_text(json.dumps(results,indent=2));print(json.dumps(results,indent=2))
