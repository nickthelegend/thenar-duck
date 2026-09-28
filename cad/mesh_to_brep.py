"""Preserve upstream STL facets as sewn BREP; never imply recovered design history."""
import cadquery as cq,trimesh
from OCP.BRepBuilderAPI import BRepBuilderAPI_Sewing,BRepBuilderAPI_MakeSolid
from OCP.TopoDS import TopoDS
def convert(mesh):
    sew=BRepBuilderAPI_Sewing(1e-5)
    for face in mesh.faces:
        pts=[cq.Vector(*p) for p in mesh.vertices[face]]
        try:sew.Add(cq.Face.makeFromWires(cq.Wire.makePolygon(pts,close=True)).wrapped)
        except Exception:pass
    sew.Perform();shape=cq.Shape.cast(sew.SewedShape());solids=[]
    for shell in shape.Shells():
        solid=cq.Solid(BRepBuilderAPI_MakeSolid(TopoDS.Shell_s(shell.wrapped)).Solid())
        if solid.Volume()<0:solid=cq.Solid(TopoDS.Solid_s(solid.wrapped.Reversed()))
        solids.append(solid)
    return cq.Compound.makeCompound(solids) if len(solids)>1 else solids[0]
if __name__=='__main__':
    from inspect_reference import load,OUT
    parts,_=load();p=next(p for p in parts if p['name']=='trunk_top');s=convert(p['mesh']);print('valid',s.isValid(),len(s.Solids()),s.Volume());cq.exporters.export(s,str(OUT/'trunk_top.brep'))
