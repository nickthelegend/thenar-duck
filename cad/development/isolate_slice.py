from pathlib import Path
import json,zipfile,subprocess,xml.etree.ElementTree as ET
p=Path('cad/thenar_duck_B/bambu/sample').resolve()
native=p/'native_P1S_textured.3mf';custom=p/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf'
def config(f):
 with zipfile.ZipFile(f) as z:return json.loads(z.read('Metadata/project_settings.config'))
for name,geometry,settings,force in [('native',native,config(native),False),('custom',custom,config(custom),False),('native_custom',native,config(custom),False),('custom_native',custom,config(native),True)]:
 out=p/name;out.mkdir(exist_ok=True);inp=out/'input.3mf'
 with zipfile.ZipFile(geometry) as a,zipfile.ZipFile(inp,'w',zipfile.ZIP_DEFLATED) as z:
  for n in a.namelist():
   data=a.read(n)
   if n=='Metadata/project_settings.config':data=json.dumps(settings).encode()
   if n=='Metadata/model_settings.config' and force:
    root=ET.fromstring(data)
    for e in root.findall('.//metadata'):
     if e.get('key')=='extruder':e.set('value','1')
    data=ET.tostring(root)
   z.writestr(n,data)
 r=subprocess.run(['D:/Program Files/Bambu Studio/bambu-studio.exe','--outputdir',str(out),'--slice','0',str(inp)],capture_output=True,timeout=120)
 result=json.loads((out/'result.json').read_text())
 print(name,r.returncode,result.get('error_string'),len(result.get('sliced_plates',[])),flush=True)
