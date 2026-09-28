from pathlib import Path
import subprocess,zipfile,json
p=Path('cad/thenar_duck_B/bambu/sample').resolve();src=p/'native_P1S.3mf';inp=p/'native_P1S_textured.3mf';out=p/'slice_test';out.mkdir(exist_ok=True)
with zipfile.ZipFile(src) as a,zipfile.ZipFile(inp,'w',zipfile.ZIP_DEFLATED) as z:
 for n in a.namelist():
  data=a.read(n)
  if n=='Metadata/project_settings.config':
   d=json.loads(data);d['curr_bed_type']='Textured PEI Plate';data=json.dumps(d).encode()
  z.writestr(n,data)
r=subprocess.run(['D:/Program Files/Bambu Studio/bambu-studio.exe','--outputdir',str(out),'--slice','0','--export-3mf',str(out/'sliced.3mf'),str(inp)],capture_output=True,timeout=180)
print('slice',r.returncode,(out/'result.json').read_text()[:2000],flush=True)
