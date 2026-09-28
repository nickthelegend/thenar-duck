"""Deterministic engineering review renders; no CAD geometry is altered."""
import vtk, numpy as np
from vtk.util.numpy_support import numpy_to_vtk,numpy_to_vtkIdTypeArray
def render(items,path,size=(1500,1200),view=(1,-1,.65),target=None,parallel=285):
    ren=vtk.vtkRenderer();ren.SetBackground(.94,.955,.97)
    for mesh,color in items:
        points=vtk.vtkPoints();points.SetData(numpy_to_vtk(np.asarray(mesh.vertices),deep=True))
        cells=vtk.vtkCellArray();arr=np.column_stack((np.full(len(mesh.faces),3),mesh.faces)).astype(np.int64).ravel();cells.SetCells(len(mesh.faces),numpy_to_vtkIdTypeArray(arr,deep=True))
        poly=vtk.vtkPolyData();poly.SetPoints(points);poly.SetPolys(cells)
        normal=vtk.vtkPolyDataNormals();normal.SetInputData(poly);normal.ComputePointNormalsOn();normal.SetFeatureAngle(35)
        mapper=vtk.vtkPolyDataMapper();mapper.SetInputConnection(normal.GetOutputPort())
        actor=vtk.vtkActor();actor.SetMapper(mapper);actor.GetProperty().SetColor(*color[:3]);actor.GetProperty().SetOpacity(color[3] if len(color)>3 else 1);actor.GetProperty().SetSpecular(.15);ren.AddActor(actor)
    win=vtk.vtkRenderWindow();win.SetOffScreenRendering(1);win.AddRenderer(ren);win.SetSize(*size);win.SetMultiSamples(4)
    ren.ResetCamera();cam=ren.GetActiveCamera();target=np.array(target if target is not None else cam.GetFocalPoint());cam.SetFocalPoint(*target);cam.SetPosition(*(target+np.array(view)*1000));cam.SetViewUp(0,0,1);cam.ParallelProjectionOn();cam.SetParallelScale(parallel);ren.ResetCameraClippingRange()
    win.Render();capture=vtk.vtkWindowToImageFilter();capture.SetInput(win);capture.Update();writer=vtk.vtkPNGWriter();writer.SetFileName(str(path));writer.SetInputConnection(capture.GetOutputPort());writer.Write();win.Finalize()
if __name__=='__main__':
    from inspect_reference import load,OUT
    parts,_=load();render([(p['mesh'],p['color']) for p in parts if 'antenna' not in p['name'] and p['name']!='sg90'],OUT/'reference.png',target=(-20,0,220))
