from pathlib import Path
import subprocess,json,hashlib
p=Path('cad/thenar_duck_B/bambu').resolve();exe='D:/Program Files/Bambu Studio/bambu-studio.exe';native=p/'Thenar_Duck_B_P1S_ALL_PARTS.3mf'
r=subprocess.run([exe,'--arrange','0','--export-3mf',str(native),str(p/'Thenar_Duck_B_P1S_ALL_PARTS_source.3mf')],capture_output=True,timeout=180);assert r.returncode==0
out=p/'validation/plate17_corrected';out.mkdir(exist_ok=True)
r=subprocess.run([exe,'--outputdir',str(out),'--slice','17',str(native)],capture_output=True,timeout=180)
result=json.loads((out/'result.json').read_text());print(r.returncode,result['error_string'],[(v['id'],v['warning_message']) for v in result['sliced_plates']],flush=True)
if r.returncode==0 and result['return_code']==0:(out/'project_sha256.txt').write_text(hashlib.sha256(native.read_bytes()).hexdigest())
