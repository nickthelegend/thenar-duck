import sys; sys.path.insert(0, r"D:\Project\thenar-duck\cad")
from swlib import *
sw = SW(); sw.close_all()
for plane in ("Front Plane", "Top Plane", "Right Plane"):
    for flip in (False, True):
        p = sw.new_part("o")
        with p.sketch(plane) as s:
            s.rect_corners(0, 0, 10, 20)      # sketch x 0..10, sketch y 0..20
        p.extrude(5, flip=flip)
        print(f"{plane:12s} flip={flip!s:5s} bbox(mm) =", [round(v, 1) for v in p.bbox()])
        p.close() if False else sw.app.CloseDoc(call(p.doc, "GetTitle"))
