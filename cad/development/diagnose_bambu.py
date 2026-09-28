from pathlib import Path
import zipfile,subprocess
p=Path('cad/thenar_duck_B/bambu/sample').resolve()
probe=zipfile.ZipFile('cad/development/bambu_probe.3mf');ours=zipfile.ZipFile(p/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf')
for name,source,config in [('native_geometry_our_settings',probe,ours),('our_geometry_native_settings',ours,probe)]:
 inp=p/(name+'.3mf');out=p/(name+'_export.3mf')
 with zipfile.ZipFile(inp,'w',zipfile.ZIP_DEFLATED) as z:
  for n in source.namelist():
   data=config.read(n) if n=='Metadata/project_settings.config' else source.read(n)
   if n=='Metadata/model_settings.config':data=data.replace(b'key="extruder" value="3"',b'key="extruder" value="1"')
   z.writestr(n,data)
 r=subprocess.run(['D:/Program Files/Bambu Studio/bambu-studio.exe','--arrange','0','--export-3mf',str(out),str(inp)],capture_output=True,timeout=90)
 print(name,r.returncode,out.exists(),flush=True)
