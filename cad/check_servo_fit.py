"""Check vendor servo solid geometry against printed parts in the neutral assembly."""
import pathlib,json,time
import cadquery as cq
ROOT=pathlib.Path(__file__).resolve().parent/('thenar_duck_B' if '--revision-b' in __import__('sys').argv else 'thenar_duck_A');R=ROOT/'reports'
manifest=json.loads((R/'print_manifest.json').read_text())
def bounds(s):
 b=s.BoundingBox();return [(b.xmin,b.xmax),(b.ymin,b.ymax),(b.zmin,b.zmax)]
servos=[]
for f in (ROOT/'hardware').glob('ST3215_C018_*.step'):
 s=cq.importers.importStep(str(f)).val();servos.append((f.stem,s,bounds(s)))
contacts=[];tested=0
for p in manifest:
 if p['part'].startswith('C0'):continue
 s=cq.Shape.importBrep(str(ROOT/'brep'/(p['part']+'.brep')));b=bounds(s)
 for n,v,vb in servos:
  if not all(min(a[1],c[1])-max(a[0],c[0])>.05 for a,c in zip(b,vb)):continue
  tested+=1
  overlap=s.intersect(v).Volume()
  if overlap>.1:
   row=dict(printed=p['part'],servo=n,overlap_mm3=round(overlap,4));contacts.append(row);print(row,flush=True)
 print('Checked',p['part'],flush=True)
report=dict(scope='Exact solid intersection of vendor servo geometry and printed parts in neutral pose; excludes wires, screw heads, tolerances and moving insertion paths',pairs_tested=tested,contacts=contacts)
(R/'servo_neutral_fit.json').write_text(json.dumps(report,indent=2));print('FINAL',report,flush=True)
