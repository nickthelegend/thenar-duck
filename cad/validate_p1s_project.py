"""Normalize the project in installed Bambu Studio, then slice all plates locally.
Never connects to a printer. Result JSON is retained as evidence.
"""
from pathlib import Path
import subprocess,json,time,hashlib
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'cad/thenar_duck_B/bambu';exe=Path('D:/Program Files/Bambu Studio/bambu-studio.exe')
native=p/'Thenar_Duck_B_P1S_ALL_PARTS.3mf'
t=time.time()
r=subprocess.run([str(exe),'--arrange','0','--export-3mf',str(native),str(p/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf')],capture_output=True,timeout=180)
print('Native export',r.returncode,flush=True)
assert r.returncode==0 and native.exists()
out=p/'validation';out.mkdir(exist_ok=True)
r=subprocess.run([str(exe),'--outputdir',str(out),'--slice','0',str(native)],capture_output=True,timeout=3600)
print('All-plate slice',r.returncode,'seconds',round(time.time()-t,1),flush=True)
result=json.loads((out/'result.json').read_text())
if r.returncode==0 and result['return_code']==0:
 (out/'full_run_project_sha256.txt').write_text(hashlib.sha256(native.read_bytes()).hexdigest())
print(json.dumps(result,indent=2)[:6000],flush=True)
