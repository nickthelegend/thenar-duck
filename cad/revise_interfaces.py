"""Apply the source-defined interface revision to cached assembly geometry."""
from build_duck import *
scene=trimesh.load_scene(OUT/'Thenar_Duck_A_FULL_ASSEMBLY.glb')
index={p['name']:p for p in json.loads((OUT/'reports/assembly_index.json').read_text())}
manifest=json.loads((OUT/'reports/print_manifest.json').read_text())
for p in manifest:
 n=p['part'];i=index[n];s=cq.Shape.importBrep(str(OUT/'brep'/(n+'.brep')))
 rotation=None
 if n.startswith(('A02_','A03_')):rotation=((0,0,0),(1,0,0),90)
 if n.startswith(('A04_','A05_','A06_','A12_','A13_','A14_')):rotation=((0,0,0),(0,1,0),90)
 part(n,s,tuple(i['color']),qty=p['quantity'],body=i['body'],material=p['material'],notes=p['notes'],print_rotation=rotation,render_mesh=scene.geometry[n] if n in scene.geometry else mesh(s))
for p in json.loads((OUT/'reports/component_envelopes.json').read_text()):
 n=p['name'];i=index[n];f=OUT/'hardware'/(n+'.step');s=cq.importers.importStep(str(f)).val() if f.exists() else None
 hardware.append(dict(name=n,shape=s,mesh=scene.geometry[n],color=i['color'],body=i['body'],status=p['status']))
fasteners.extend(json.loads((OUT/'reports/fasteners_custom_parts.json').read_text()))
interfaces.extend(json.loads((OUT/'reports/interfaces.json').read_text()))
adapt_vendor_interfaces();export()
