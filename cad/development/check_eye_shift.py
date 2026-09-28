import sys
sys.path.insert(0,'cad')
import cadquery as cq
from pathlib import Path
p=Path('cad/thenar_duck_B/brep');h=cq.Shape.importBrep(str(p/'head_1.brep'))
for side in ['R','L']:
 s=cq.Shape.importBrep(str(p/('B12_eye_retainer_'+side+'.brep')))
 for dx in [0,-.15,-.3,-.5]:
  q=s.translate((dx,0,0)).intersect(h);bb=q.BoundingBox()
  print(side,dx,q.Volume(),(bb.xmin,bb.xmax,bb.ymin,bb.ymax,bb.zmin,bb.zmax),flush=True)
