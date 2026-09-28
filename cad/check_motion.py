"""Sampled triangle-level collision screen of the new torso against moving links.
Not a continuous swept-volume proof; reports exact tested poses and limitations.
"""
import pathlib,json,xml.etree.ElementTree as ET,numpy as np,trimesh,vtk
from scipy.spatial.transform import Rotation
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
from inspect_reference import load,SRC,tf
ROOT=pathlib.Path(__file__).resolve().parent;OUT=ROOT/('thenar_duck_B' if '--revision-b' in __import__('sys').argv else 'thenar_duck_A')
refs,joints=load();xml=ET.parse(SRC/'robot.xml').getroot()
base_z=next(p['T'][2,3] for p in refs if p['name']=='body_front')-64.8909
def frames(q):
 result={}
 def rec(b,T):
  rel=tf(b)
  if b.get('name')=='base':rel[2,3]=base_z
  T=T@rel
  j=b.find('joint')
  if j is not None:
   axis=np.fromstring(j.get('axis','0 0 1'),sep=' ');rot=np.eye(4);rot[:3,:3]=Rotation.from_rotvec(axis*np.radians(q.get(j.get('name'),0))).as_matrix();T=T@rot
  result[b.get('name')]=T
  for c in b.findall('body'):rec(c,T)
 rec(xml.find('worldbody/body'),np.eye(4));return result
zero=frames({})
def poly(m):
 pts=vtk.vtkPoints();pts.SetData(numpy_to_vtk(np.asarray(m.vertices),deep=True));cells=vtk.vtkCellArray();a=np.c_[np.full(len(m.faces),3),m.faces].astype(np.int64).ravel();cells.SetCells(len(m.faces),numpy_to_vtkIdTypeArray(a,deep=True));p=vtk.vtkPolyData();p.SetPoints(pts);p.SetPolys(cells);return p
filters={}
def touching(a,c,M):
 key=(a['name'],c['name'])
 if key not in filters:
  f=vtk.vtkCollisionDetectionFilter();f.SetInputData(0,a['poly']);f.SetInputData(1,c['poly'])
  for i in [0,1]:t=vtk.vtkTransform();t.Identity();f.SetTransform(i,t)
  f.SetCollisionModeToFirstContact();f.SetBoxTolerance(.01);f.SetCellTolerance(.0001);filters[key]=f
 f=filters[key];vm=vtk.vtkMatrix4x4()
 for i in range(4):
  for j in range(4):vm.SetElement(i,j,M[i,j])
 t=vtk.vtkTransform();t.SetMatrix(vm);f.SetTransform(0,t);f.Update();return f.GetNumberOfContacts()>0
scene=trimesh.load_scene(next(OUT.glob('*_FULL_ASSEMBLY.glb')))
idx=json.loads((OUT/'reports/assembly_index.json').read_text());lookup={p['name']:p for p in idx}
objects=[]
for name,m in scene.geometry.items():
 if name not in lookup:continue
 objects.append(dict(**lookup[name],mesh=m,poly=poly(m)))
static=[p for p in objects if p['body']=='trunk_assembly' and (p['name'].startswith(('A','B')) or (p['kind']=='hardware' and not p['name'].startswith(('ST3215','roll_bearing'))))]
moving=[p for p in objects if p['body'] not in ['trunk_assembly','coupon'] and 'antenna' not in p['body']]
poses=[('neutral',{})]
for j in joints:
 if 'antenna' in j['name']:continue
 lo,hi=j['range']
 for a in np.linspace(lo,hi,7):poses.append((j['name']+'_'+str(round(a,1)),{j['name']:float(a)}))
for k in range(11):
 t=k/10
 poses.append(('crouch_'+str(k),dict(left_hip_pitch=-40*t,right_hip_pitch=40*t,left_knee=65*t,right_knee=-65*t,left_ankle=-25*t,right_ankle=25*t)))
for n in [-15,0,15,30,45]:
 for tilt in [-10,0,10]:
  hp=tilt-n
  if -45<=hp<=45:poses.append(('coordinated_head_'+str(n)+'_'+str(tilt),dict(neck_pitch=n,head_pitch=hp)))
collisions=[]
for ni,(label,q) in enumerate(poses):
 F=frames(q)
 for p in moving:
  if p['body'] not in F:continue
  M=F[p['body']]@np.linalg.inv(zero[p['body']])
  if ni and np.allclose(M,np.eye(4)):continue
  corners=trimesh.bounds.corners(p['mesh'].bounds);v=trimesh.transform_points(corners,M);bounds=np.array([v.min(axis=0),v.max(axis=0)])
  candidates=[c for c in static if np.all(np.minimum(bounds[1],c['mesh'].bounds[1])-np.maximum(bounds[0],c['mesh'].bounds[0])>.1)]
  if not candidates:continue
  for c in candidates:
   if touching(p,c,M):collisions.append(dict(pose=label,q_degrees=q,moving=p['name'],fixed=c['name']))
 print(ni+1,len(poses),label,'cumulative contacts',len(collisions),flush=True)
report=dict(method='VTK triangle intersection, individual joints sampled at 7 values plus crouches, coordinated head poses, and neutral; 0.1mm broadphase overlap',limitations=['Does not prove continuous or untested combined joint clearance','No flexible cable deformation, screw heads, or tolerances','New torso parts AND reserved electronics versus moving assemblies; inherited core self-contact not certified'],poses_tested=poses,contacts=collisions)
(OUT/'reports/motion_screen.json').write_text(json.dumps(report,indent=2));print('CONTACTS',len(collisions),flush=True)
