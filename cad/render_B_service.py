"""Labelled views of the actual exported geometry, with parts moved for access illustration."""
from pathlib import Path
import json,numpy as np,trimesh
from PIL import Image,ImageDraw,ImageFont
from render_meshes import render
OUT=Path(__file__).resolve().parent/'thenar_duck_B'
scene=trimesh.load_scene(OUT/'Thenar_Duck_B_FULL_ASSEMBLY.glb')
idx=json.loads((OUT/'reports/assembly_index.json').read_text())
lookup={p['name']:p for p in idx}
fontpath='C:/Windows/Fonts/segoeui.ttf'
title=ImageFont.truetype(fontpath,34);font=ImageFont.truetype(fontpath,23);small=ImageFont.truetype(fontpath,19)
cards=[
 ('BATTERY + LEAD BAY', ['B08','BK4200','B05'], (-147,0,197),100, '137 × 44 × 27 mm published pack reference', '140 × 50 × 32 mm sled capacity; 2 mm pad'),
 ('PI 4B — REMOVABLE TRAY', ['B10','Raspberry','Pi4_'], (-140,0,262),70, '58 × 49 mm hole pitch; 5 mm standoffs', 'Lift through roof; USB and microSD access'),
 ('BNO055 — ITS OWN BRACKET', ['B11','DFRobot','IMU_header'], (-141,-37,243),36, 'SEN0374: 19 × 21 mm; two M2 holes', 'Header space beside Pi; bracket lifts out'),
 ('POWER DECK', ['B09','B19','PDB_','UBEC_','Waveshare_Adapter','Adapter_components'], (-126,0,234),91, 'PDB on slotted spacers; UBEC on ties', 'Adapter fixed separately; screw access from above'),
 ('SWITCH + FUSE SERVICE POD', ['B06','Fuse_holder','Switch_terminal'], (-216,0,249),53, 'Four removable switch-cutout lid options', 'Fuse in lower bay; insulated terminals above'),
 ('EYES + CHEST LIGHTS', ['B12','B13','B14','WS2812_ring','B21','B22','B23','WS2812_matrix'], (0,0,0),80, 'Ring sleeves: 37 / 44 / 45 / 46 mm', 'Matrix carrier: 30–40 mm square PCB'),
]
canvas=Image.new('RGB',(1800,1640),'#eff3f7');d=ImageDraw.Draw(canvas)
d.text((45,24),'THENAR DUCK  |  REVISION B',font=title,fill='#162733')
d.text((45,77),'Actual CAD parts • published dimensions + labelled adjustable mounts',font=font,fill='#435767')
for k,(heading,prefixes,target,scale,l1,l2) in enumerate(cards):
 items=[]
 for n,m in scene.geometry.items():
  if not n.startswith(tuple(prefixes)):continue
  m=m.copy()
  if k==0 and n.startswith('B05'):m.apply_translation((-28,0,0))
  if k==4:
   if n.startswith('B06b'):m.apply_translation((-40,0,0))
  if k==5:
   # Two groups placed side by side, deliberately exploded for visibility.
   if n.startswith(('B12','B13','B14','WS2812_ring')):
    if n.endswith('_L'):continue
    m.apply_translation((-90,8,-397))
    if n.startswith('B12'):m.apply_translation((-12,0,0))
    if n.startswith('B14'):m.apply_translation((12,0,0))
   else:
    m.apply_translation((-34,46,-244))
    if n.startswith(('B22','B23')):m.apply_translation((10,0,0))
  items.append((m,lookup[n]['color']))
 out=OUT/'renders'/('service_detail_'+str(k+1)+'.png')
 render(items,out,size=(850,360),view=(-1,-1,.85),target=target,parallel=scale)
 x=25+(k%2)*895;y=133+(k//2)*495
 tile=Image.open(out)
 canvas.paste(tile,(x,y+38));d.text((x+15,y),heading,font=font,fill='#075d93')
 d.text((x+15,y+414),l1,font=small,fill='#152c3b');d.text((x+15,y+443),l2,font=small,fill='#435767')
canvas.save(OUT/'renders/04_service_layout.png')
