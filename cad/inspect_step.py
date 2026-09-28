import cadquery as cq,json,pathlib
R=pathlib.Path(__file__).resolve().parent
path=R/'reference_open_duck/print/mods/v2_Jaimes_Mods/Mini BDX V2 Jaimes Mods.step'
print('loading',flush=True)
a=cq.Assembly.load(str(path)); data=[]
for shape,name,loc,color in a:
    s=shape.located(loc); b=s.BoundingBox()
    data.append(dict(name=name,solids=len(s.Solids()),bbox=[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax]))
print('parts',len(data),flush=True)
(R/'development/step_instances.json').write_text(json.dumps(data,indent=2))
a.save(str(R/'development/reference.xml'))
print('saved',flush=True)
