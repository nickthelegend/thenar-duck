from pathlib import Path
import json,zipfile,subprocess
p=Path('cad/thenar_duck_B/bambu/sample').resolve();src=p/'native_P1S_textured.3mf';custom=p/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf';out=p/'bisect';out.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as z:members={n:z.read(n) for n in z.namelist()};base=json.loads(members['Metadata/project_settings.config'])
with zipfile.ZipFile(custom) as z:target=json.loads(z.read('Metadata/project_settings.config'))
diff=[k for k in target if target[k]!=base.get(k)]
def fails(keys):
 settings=base.copy();settings.update({k:target[k] for k in keys})
 # Always maintain valid import metadata for the selected filament count.
 n=len(settings['filament_colour']);settings['inherits_group']=['']*(n+2);settings['different_settings_to_system']=['']*(n+2)
 with zipfile.ZipFile(out/'input.3mf','w',zipfile.ZIP_DEFLATED) as z:
  for name,data in members.items():z.writestr(name,json.dumps(settings).encode() if name=='Metadata/project_settings.config' else data)
 r=subprocess.run(['D:/Program Files/Bambu Studio/bambu-studio.exe','--outputdir',str(out),'--slice','0',str(out/'input.3mf')],capture_output=True,timeout=120)
 return r.returncode!=0
while len(diff)>1:
 half=len(diff)//2
 if fails(diff[:half]):diff=diff[:half]
 elif fails(diff[half:]):diff=diff[half:]
 else:
  print('interaction',diff,flush=True);break
 print(len(diff),diff if len(diff)<8 else '',flush=True)
print('FINAL',diff,flush=True)
