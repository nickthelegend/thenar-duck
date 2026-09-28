"""Repair only sub-0.01 mm tessellation seams; reject larger open boundaries."""
import numpy as np,trimesh
def prepare_mesh(original):
 for digits in [5,4]:
  m=original.copy();m.merge_vertices(digits_vertex=digits);m.update_faces(m.nondegenerate_faces());m.update_faces(m.unique_faces());m.remove_unreferenced_vertices()
  if m.is_watertight:return m,dict(vertex_merge_digits=digits,filled_microloops=0)
 edges=m.edges;_,inverse,counts=np.unique(np.sort(edges,axis=1),axis=0,return_inverse=True,return_counts=True)
 if max(counts)>2:raise ValueError('Nonmanifold mesh requires geometry review')
 boundary=edges[counts[inverse]==1];adj={}
 for u,v in boundary:adj.setdefault(int(u),set()).add(int(v));adj.setdefault(int(v),set()).add(int(u))
 if any(len(v)!=2 for v in adj.values()):raise ValueError('Branching mesh boundary requires geometry review')
 seen=set();groups=[]
 for start in adj:
  if start in seen:continue
  todo=[start];group=set()
  while todo:
   u=todo.pop()
   if u in group:continue
   group.add(u);todo.extend(adj[u]-group)
  seen|=group;groups.append(group)
 verts=list(m.vertices);faces=list(m.faces)
 for group in groups:
  pts=m.vertices[list(group)]
  if max(np.ptp(pts,axis=0))>.01 or len(group)>30:raise ValueError('Mesh opening exceeds 0.01 mm seam-repair limit')
  center=len(verts);verts.append(pts.mean(axis=0))
  for u,v in boundary:
   if int(u) in group:faces.append([int(v),int(u),center])
 result=trimesh.Trimesh(vertices=verts,faces=faces,process=False)
 if not result.is_watertight or result.volume<=0:raise ValueError('Micro-seam repair did not produce a closed positive mesh')
 return result,dict(vertex_merge_digits=4,filled_microloops=len(groups),maximum_repair_extent_mm=.01)
