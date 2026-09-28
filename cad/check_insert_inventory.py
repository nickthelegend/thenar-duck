import numpy as np,trimesh,json,collections
from inspect_reference import load
from pathlib import Path
refs,_=load();picked=collections.Counter()
keep={'trunk_bottom','trunk_top','roll_motor_bottom','roll_motor_top','left_roll_to_pitch','right_roll_to_pitch','left_cache','right_cache','leg_spacer','left_knee_to_ankle_left_sheet','left_knee_to_ankle_right_sheet','foot_side','foot_top','foot_bottom_pla','foot_bottom_tpu','neck_left_sheet','neck_right_sheet','head_pitch_to_yaw','head_yaw_to_roll','head_roll_mount','head','head_bot_sheet'}
found=[]
for p in refs:
 if p['name'] not in keep:continue
 name=p['name'];picked[name]+=1;m=p['mesh'];circles=[]
 for axis in range(3):
  for sign in [-1,1]:
   ids=np.where(m.face_normals[:,axis]*sign>.9999)[0];vals=np.round(m.triangles_center[ids,axis],2)
   for val in np.unique(vals):
    f=ids[vals==val]
    if len(f)<5:continue
    subset=m.submesh([f],append=True);unq,counts=np.unique(subset.edges_sorted,axis=0,return_counts=True);bd=unq[counts==1]
    if not len(bd):continue
    for loop in trimesh.graph.connected_components(bd):
     pts=subset.vertices[loop];other=[i for i in range(3) if i!=axis];size=np.ptp(pts,axis=0)[other];c=(pts.max(axis=0)+pts.min(axis=0))/2;d=size.mean()
     if len(loop)>8 and abs(size[0]-size[1])<.15 and any(abs(d-z)<.08 for z in [4,3.2]):circles.append((axis,c,d))
 holes=[]
 for axis,c,d in circles:
  if abs(d-4)>.08:continue
  for ax2,c2,d2 in circles:
   other=[i for i in range(3) if i!=axis];depth=abs(c2[axis]-c[axis])
   if ax2!=axis or abs(d2-4)>.08 or not 4<=depth<=8 or np.linalg.norm((c2-c)[other])>.12:continue
   if not any(ax3==axis and abs(d3-3.2)<.08 and np.linalg.norm(c3-c2)<.15 for ax3,c3,d3 in circles):continue
   key=tuple(np.round((c+c2)/2,2))
   if key in holes:continue
   holes.append(key);found.append(dict(part=name+'_'+str(picked[name]),axis=axis,position_mm=np.round(c,3).tolist(),depth_mm=round(depth,3)))
print(json.dumps(dict(count=len(found),pockets=found),indent=2))
Path('cad/thenar_duck_A/reports/reference_insert_pockets.json').write_text(json.dumps(dict(method='D4 to D3.2 stepped bores, 4-8mm depth, axis-aligned mesh edges only; manual review required',count=len(found),pockets=found),indent=2))
