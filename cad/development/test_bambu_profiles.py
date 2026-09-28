from pathlib import Path
import json,subprocess
root=Path('D:/Program Files/Bambu Studio/resources/profiles/BBL');files={f.stem:f for f in root.rglob('*.json')}
def resolve(name):
 d=json.loads(files[name].read_text());r=resolve(d['inherits']) if d.get('inherits') else {}
 for i in d.get('include',[]):r.update(resolve(i))
 r.update(d);r.pop('inherits',None);r.pop('include',None);return r
p=Path('cad/thenar_duck_B/bambu/sample').resolve()
for name,label in [('Bambu Lab P1S 0.4 nozzle','machine'),('0.20mm Standard @BBL X1C','process'),('Generic PETG','filament')]:
 d=resolve(name);(p/(label+'.json')).write_text(json.dumps(d,indent=2))
args=['D:/Program Files/Bambu Studio/bambu-studio.exe','--load-settings',str(p/'machine.json')+';'+str(p/'process.json'),'--load-filaments',str(p/'filament.json'),'--arrange','1','--export-3mf',str(p/'native_P1S.3mf'),str(Path('cad/thenar_duck_B/stl/C04_servo_horn_pattern_gauge.stl').resolve())]
r=subprocess.run(args,capture_output=True,timeout=90);print('build',r.returncode,(p/'native_P1S.3mf').exists(),flush=True)
if (p/'native_P1S.3mf').exists():
 r=subprocess.run(['D:/Program Files/Bambu Studio/bambu-studio.exe','--info',str(p/'native_P1S.3mf')],capture_output=True,timeout=90);print('reopen',r.returncode,flush=True)
