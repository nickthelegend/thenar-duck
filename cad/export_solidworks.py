"""Create a native review assembly from verified STEP exports, retaining separate parts.
Imported reference geometry is faceted BREP, not a recovered native feature tree.
"""
import pathlib,json,sys,time,hashlib,shutil
from swlib import SW,Assembly,rot_x,call,_byref_int
REV='B' if '--revision-b' in sys.argv else 'A'
ROOT=pathlib.Path(__file__).resolve().parent/('thenar_duck_'+REV);OUT=ROOT/'solidworks';OUT.mkdir(exist_ok=True)
TITLE='Thenar_Duck_'+REV+'_REVIEW'
sw=SW();report=[]
if '--interface-revision' in sys.argv:
 sw.app.CloseDoc('Thenar_Duck_A_REVIEW.SLDASM')
 revised={p['printed'] for p in json.loads((ROOT/'reports/servo_interface_reliefs.json').read_text())}|{'head_1'}
else:revised=None
manifest=json.loads((ROOT/'reports/print_manifest.json').read_text())
paths=[ROOT/'step'/(p['part']+'.step') for p in manifest if not p['part'].startswith('C0')]
index={p['name']:p for p in json.loads((ROOT/'reports/assembly_index.json').read_text())}
paths += [p for p in (ROOT/'hardware').glob('*.step') if p.stem in index and index[p.stem]['kind']=='hardware']
if '--sample' in sys.argv:paths=[ROOT/'step/A10_Pi4B_removable_tray.step']
for path in paths:
 dest=OUT/(path.stem+'.SLDPRT')
 try:
  fingerprint=hashlib.sha256(path.read_bytes()).hexdigest();stamp=dest.with_suffix('.source.sha256')
  if REV=='B' and path.stem!='head_1' and not path.stem.startswith('B') and not dest.exists():
   previous=ROOT.parent/'thenar_duck_A/solidworks'/dest.name
   # These retained core parts, KW10s, bearings and vendor servos are unchanged.
   if previous.exists() and (path.stem.startswith(('A15','A16','A17','ST3215','roll_bearing','KW10')) or path.parent.name=='step'):
    shutil.copy2(previous,dest);stamp.write_text(fingerprint)
  if revised is not None and path.stem not in revised and dest.exists():stamp.write_text(fingerprint)
  if not dest.exists() or not stamp.exists() or stamp.read_text()!=fingerprint:
   print('Importing',path.stem,flush=True)
   # 579 / 2 verified from installed SW 2026 enums: neutral import as multibody part.
   # Restore the user's preference after each import, including failed imports.
   old=sw.app.GetUserPreferenceIntegerValue(579)
   try:
    sw.app.CloseDoc(dest.name)
    sw.app.CloseDoc(path.stem+'.SLDASM')
    sw.app.SetUserPreferenceIntegerValue(579,2)
    p=sw.import_step(str(path));p.color(index[path.stem]['color']);p.save(str(dest));p.close()
   finally:sw.app.SetUserPreferenceIntegerValue(579,old)
   stamp.write_text(fingerprint)
  report.append(dict(part=path.stem,path=str(dest),status='saved'))
 except Exception as e:
  report.append(dict(part=path.stem,status='failed',error=str(e)));print('FAILED',path.stem,e,flush=True)
 (ROOT/'reports/solidworks_import.json').write_text(json.dumps(report,indent=2))
if '--sample' not in sys.argv:
 asm_path=str(OUT/(TITLE+'.SLDASM'))
 doc=sw.app.GetOpenDocumentByName(asm_path)
 if doc is None and pathlib.Path(asm_path).exists():doc=sw.app.OpenDoc6(asm_path,2,1,'',_byref_int(),_byref_int())
 a=Assembly(sw,doc,TITLE) if doc is not None else sw.new_assembly(TITLE)
 existing={pathlib.Path(call(c,'GetPathName')).stem for c in (a.doc.GetComponents(True) or [])}
 view=a.doc.ActiveView
 if view is not None:view.EnableGraphicsUpdate=False
 for ni,p in enumerate(report):
  if p['status']=='saved':
   if p['part'] in existing:continue
   print('Adding',p['part'],flush=True)
   comp=a.add(p['path'],rot_x(-90),(0,0,0),fixed=True,key=p['part'])
   sw.app.CloseDoc(pathlib.Path(p['path']).name)
   comp.SetSuppression2(1)  # swComponentLightweight, verified from installed swconst DLL
   if ni%10==0:a.save(asm_path)
 if view is not None:view.EnableGraphicsUpdate=True
 a.rebuild();a.save(asm_path);a.view();print('ASSEMBLY SAVED',flush=True)
 components=a.doc.GetComponents(True) or []
 expected={v['name'] for v in index.values() if v['body']!='coupon'}
 present={pathlib.Path(call(c,'GetPathName')).stem for c in components}
 validation=dict(saved=True,component_count=len(components),expected_count=len(expected),missing=sorted(expected-present),extra=sorted(present-expected),first_transform=list(components[0].Transform2.ArrayData))
 (ROOT/'reports/solidworks_assembly.json').write_text(json.dumps(validation,indent=2))
 print(validation,flush=True)
