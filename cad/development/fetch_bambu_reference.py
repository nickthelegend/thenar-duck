from pathlib import Path
import urllib.request
out=Path('cad/development/bambu_source');out.mkdir(exist_ok=True)
paths=['src/libslic3r/Format/bbs_3mf.cpp','src/BambuStudio.cpp','src/slic3r/GUI/PartPlate.cpp','src/slic3r/GUI/PartPlate.hpp']
for p in paths:
 try:
  data=urllib.request.urlopen('https://raw.githubusercontent.com/bambulab/BambuStudio/master/'+p,timeout=30).read()
  f=out/Path(p).name;f.write_bytes(data);print(f,len(data),flush=True)
 except Exception as e:print(p,type(e).__name__,str(e),flush=True)
