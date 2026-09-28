import pathlib,json,xml.etree.ElementTree as ET
import numpy as np, trimesh
from scipy.spatial.transform import Rotation
ROOT=pathlib.Path(__file__).resolve().parent
SRC=ROOT/'reference_open_duck/mini_bdx/robots/open_duck_mini_v2'
OUT=ROOT/'development'; OUT.mkdir(exist_ok=True)
def tf(e):
    T=np.eye(4); T[:3,3]=np.fromstring(e.get('pos','0 0 0'),sep=' ')*1000
    q=np.fromstring(e.get('quat','1 0 0 0'),sep=' ')
    T[:3,:3]=Rotation.from_quat([*q[1:],q[0]]).as_matrix()
    return T
def load():
    xml=ET.parse(SRC/'robot.xml').getroot(); parts=[]; joints=[]
    def walk(b,T):
        T=T@tf(b)
        for j in b.findall('joint'):
            joints.append(dict(name=j.get('name'),body=b.get('name'),xyz=T[:3,3].tolist(),axis=(T[:3,:3]@np.fromstring(j.get('axis','0 0 1'),sep=' ')).tolist(),range=np.degrees(np.fromstring(j.get('range','0 0'),sep=' ')).tolist()))
        for g in b.findall('geom'):
            if not g.get('mesh'):continue
            name=g.get('mesh'); path=SRC/(name+'.stl')
            if not path.exists():
                path=SRC/(name.replace('left_knee','knee')+'.stl')
            m=trimesh.load_mesh(path);m.apply_scale(1000); G=T@tf(g);m.apply_transform(G)
            parts.append(dict(name=name,body=b.get('name'),mesh=m,T=G,color=list(map(float,g.get('rgba','.6 .6 .6 1').split()))))
        for child in b.findall('body'):walk(child,T)
    walk(xml.find('worldbody/body'),np.eye(4))
    floor=min(p['mesh'].bounds[0,2] for p in parts if p['name']=='foot_bottom_tpu')
    for p in parts:p['mesh'].apply_translation([0,0,-floor]);p['T'][2,3]-=floor
    for j in joints:j['xyz'][2]-=floor
    return parts,joints
if __name__=='__main__':
    parts,joints=load()
    data=[dict(name=p['name'],body=p['body'],bbox=p['mesh'].bounds.round(3).tolist(),T=p['T'].round(8).tolist(),watertight=p['mesh'].is_watertight) for p in parts]
    (OUT/'reference_instances.json').write_text(json.dumps(data,indent=2));(OUT/'reference_joints.json').write_text(json.dumps(joints,indent=2))
    for p in data:
        if p['body']=='trunk_assembly' or p['name'] in ['head','head_bot_sheet','head_roll_mount']:print(p['name'],p['bbox'])
    print('joints',json.dumps(joints,indent=2))
