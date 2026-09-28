import numpy as np,trimesh,json
from inspect_reference import load,OUT
from render_meshes import render
parts,_=load(); names=['trunk_bottom','trunk_top','head_roll_mount','foot_bottom_pla','body_front']
for name in names:
 p=next(p for p in parts if p['name']==name);m=p['mesh'];print('\nPART',name,flush=True)
 for axis in range(3):
  for sign in [-1,1]:
   ids=np.where(m.face_normals[:,axis]*sign>.9999)[0]
   vals=np.round(m.triangles_center[ids,axis],2)
   for value in np.unique(vals):
    f=ids[vals==value]
    if len(f)<5:continue
    subset=m.submesh([f],append=True); edges=subset.edges_sorted;unq,counts=np.unique(edges,axis=0,return_counts=True); boundary=unq[counts==1]
    if len(boundary)==0:continue
    loops=trimesh.graph.connected_components(boundary)
    for loop in loops:
     pts=subset.vertices[loop]; other=[i for i in range(3) if i!=axis];size=np.ptp(pts,axis=0)[other];center=(pts.max(axis=0)+pts.min(axis=0))/2
     if len(loop)>8 and abs(size[0]-size[1])<.25 and .8<size[0]<12:
      print('hole',np.round(center,3).tolist(),'diam',round(size.mean(),3),'axis',axis,flush=True)
 render([(m,(.65,.7,.8))],OUT/(name+'.png'),target=m.centroid,parallel=max(m.extents)*.75)
