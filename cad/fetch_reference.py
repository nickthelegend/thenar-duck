"""Fetch pinned, attributed Open Duck mechanical references (read-only vendor files)."""
import json, pathlib, urllib.request, concurrent.futures
ROOT=pathlib.Path(__file__).resolve().parent/'reference_open_duck'
ROOT.mkdir(exist_ok=True)
def get(url):
    return urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'ThenarDuck-CAD'}),timeout=90).read()
tree=json.loads(get('https://api.github.com/repos/apirrone/Open_Duck_Mini/git/trees/v2?recursive=1'))
sha=tree['sha']; (ROOT/'revision.json').write_text(json.dumps({'repo':'https://github.com/apirrone/Open_Duck_Mini','sha':sha},indent=2))
paths=[x['path'] for x in tree['tree'] if x['type']=='blob' and (x['path'].startswith('mini_bdx/robots/open_duck_mini_v2/') or (x['path'].startswith('print/') and x['path'].count('/')==1) or x['path'] in ['LICENSE','docs/assembly.md','README.md'] or x['path'].endswith('Mini BDX V2 Jaimes Mods.step'))]
def fetch(p):
    dest=ROOT/p; dest.parent.mkdir(parents=True,exist_ok=True)
    if not dest.exists(): dest.write_bytes(get('https://raw.githubusercontent.com/apirrone/Open_Duck_Mini/'+sha+'/'+urllib.parse.quote(p)))
    return p
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
    for p in pool.map(fetch,paths): print(p,flush=True)
print('PINNED',sha,flush=True)
