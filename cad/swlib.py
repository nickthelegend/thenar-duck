"""
swlib.py - thin, tested helper layer over the SolidWorks 2026 COM API (pywin32, late-bound).

Units: every public function takes MILLIMETRES and DEGREES; internally converted to metres/radians.

Gotchas encoded here (verified on SW 2026 / pywin32 late binding):
  * zero-argument API members are inconsistently exposed as properties OR methods under late binding
    (doc.GetTitle, feat.GetFaces, doc.FirstFeature, comp.IsFixed, asm.EditRebuild3 are properties;
    body.GetEdges() is a method) -> always go through `call(obj, name)`.
  * null COM arguments must be VARIANT(VT_DISPATCH, None), never None.
  * IBody2.Select2(append, callout) has no mark argument; select bodies with SelectByRay(type=76, mark=...).
  * IModelDoc2.InsertFeatureShell returns nothing; check the feature tree.
"""
import math, os, types, pythoncom
import win32com.client
from win32com.client import VARIANT

NONE = VARIANT(pythoncom.VT_DISPATCH, None)
PART_TEMPLATE = r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2026\templates\Part.PRTDOT"
ASM_TEMPLATE = r"C:\ProgramData\SOLIDWORKS\SOLIDWORKS 2026\templates\Assembly.ASMDOT"

# selection types (swSelectType_e)
SEL_EDGES, SEL_FACES, SEL_SOLIDBODIES, SEL_PLANES = 1, 2, 76, 4
# mates (swMateType_e)
MATE_COINCIDENT, MATE_CONCENTRIC, MATE_PERPENDICULAR, MATE_PARALLEL, MATE_TANGENT, MATE_DISTANCE, MATE_ANGLE = 0, 1, 2, 3, 4, 5, 6
MATE_ALIGN_ALIGNED, MATE_ALIGN_ANTI, MATE_ALIGN_CLOSEST = 0, 1, 2

M = 0.001  # mm -> m


def call(obj, name, *args):
    """Invoke a COM member that late binding may expose as a property or a method."""
    v = getattr(obj, name)
    # dynamic COM dispatch objects are callable too (default member); only invoke real bound methods
    return v(*args) if isinstance(v, types.MethodType) else v


def dbl_array(vals):
    return VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, list(vals))


def _byref_int():
    return VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, 0)


# ----------------------------------------------------------------------------- math helpers
def rot_x(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [[1, 0, 0], [0, c, -s], [0, s, c]]


def rot_y(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [[c, 0, s], [0, 1, 0], [-s, 0, c]]


def rot_z(deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def matvec(a, v):
    return [sum(a[i][k] * v[k] for k in range(3)) for i in range(3)]


IDENT = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]


def sw_transform_data(R, t_mm):
    """SolidWorks MathTransform ArrayData: 3x3 rotation stored column-major-ish
    (rows are the images of the x, y, z axes), then translation (m), scale, then 3 zeros."""
    return [R[0][0], R[1][0], R[2][0],
            R[0][1], R[1][1], R[2][1],
            R[0][2], R[1][2], R[2][2],
            t_mm[0] * M, t_mm[1] * M, t_mm[2] * M,
            1.0, 0.0, 0.0, 0.0]


# ----------------------------------------------------------------------------- app
class SW:
    def __init__(self, visible=True):
        self.app = win32com.client.Dispatch("SldWorks.Application")
        self.app.Visible = visible

    def close_all(self):
        self.app.CloseAllDocuments(True)

    def new_part(self, name="part"):
        doc = self.app.NewDocument(PART_TEMPLATE, 0, 0, 0)
        return Part(self, doc, name)

    def new_assembly(self, name="assembly"):
        doc = self.app.NewDocument(ASM_TEMPLATE, 0, 0, 0)
        return Assembly(self, doc, name)

    def open_part(self, path):
        errs, warns = _byref_int(), _byref_int()
        doc = self.app.OpenDoc6(path, 1, 1, "", errs, warns)   # 1 = swDocPART, 1 = silent
        return Part(self, doc, os.path.splitext(os.path.basename(path))[0])

    def close(self, doc_title):
        self.app.CloseDoc(doc_title)

    def import_step(self, path, name=None):
        """Import a STEP file as a new part document (returns Part)."""
        errs = _byref_int()
        data = self.app.GetImportFileData(path)
        doc = self.app.LoadFile4(path, "r", data, errs)
        if doc is None:
            doc = self.app.ActiveDoc
        part = Part(self, doc, name or os.path.splitext(os.path.basename(path))[0])
        if not part.bodies():
            raise RuntimeError(f"STEP import produced no bodies: {path} (err {errs.value})")
        return part


# ----------------------------------------------------------------------------- sketch
class Sketch:
    """Context manager: with part.sketch('Front Plane') as s: s.rect(...)"""

    def __init__(self, part, plane):
        self.part, self.plane = part, plane
        self.sm = part.doc.SketchManager
        self.centerline = None
        self.segments = []

    def __enter__(self):
        self.part.select(self.plane, "PLANE")
        self.sm.InsertSketch(True)
        self.sm.AddToDB = True          # no snapping/inference while adding entities
        self.sm.DisplayWhenAdded = False
        return self

    def __exit__(self, *exc):
        self.sm.AddToDB = False
        self.sm.DisplayWhenAdded = True
        self.sm.InsertSketch(True)      # close sketch
        self.part.doc.ClearSelection2(True)
        return False

    # -- entities (mm) --
    def rect(self, cx, cy, w, h):
        self.segments.append(self.sm.CreateCenterRectangle(cx * M, cy * M, 0, (cx + w / 2) * M, (cy + h / 2) * M, 0))

    def rect_corners(self, x0, y0, x1, y1):
        self.segments.append(self.sm.CreateCornerRectangle(x0 * M, y0 * M, 0, x1 * M, y1 * M, 0))

    def circle(self, cx, cy, r):
        self.segments.append(self.sm.CreateCircleByRadius(cx * M, cy * M, 0, r * M))

    def line(self, x0, y0, x1, y1):
        seg = self.sm.CreateLine(x0 * M, y0 * M, 0, x1 * M, y1 * M, 0)
        self.segments.append(seg)
        return seg

    def polyline(self, pts, close=True):
        n = len(pts)
        for i in range(n if close else n - 1):
            x0, y0 = pts[i]; x1, y1 = pts[(i + 1) % n]
            self.line(x0, y0, x1, y1)

    def arc_center(self, cx, cy, x0, y0, x1, y1, ccw=True):
        """Arc by centre, start point, end point. ccw=True -> direction +1."""
        seg = self.sm.CreateArc(cx * M, cy * M, 0, x0 * M, y0 * M, 0, x1 * M, y1 * M, 0, 1 if ccw else -1)
        self.segments.append(seg)
        return seg

    def rounded_rect(self, cx, cy, w, h, r):
        """Rectangle with all four corners filleted by r (built from lines + arcs)."""
        x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
        self.line(x0 + r, y0, x1 - r, y0)
        self.arc_center(x1 - r, y0 + r, x1 - r, y0, x1, y0 + r, True)
        self.line(x1, y0 + r, x1, y1 - r)
        self.arc_center(x1 - r, y1 - r, x1, y1 - r, x1 - r, y1, True)
        self.line(x1 - r, y1, x0 + r, y1)
        self.arc_center(x0 + r, y1 - r, x0 + r, y1, x0, y1 - r, True)
        self.line(x0, y1 - r, x0, y0 + r)
        self.arc_center(x0 + r, y0 + r, x0, y0 + r, x0 + r, y0, True)

    def slot(self, x0, y0, x1, y1, width):
        """Straight slot from (x0,y0) to (x1,y1) centreline, given width."""
        self.segments.append(self.sm.CreateSketchSlot(0, 0, width * M, x0 * M, y0 * M, 0, x1 * M, y1 * M, 0, 0, 0, 0, 0, 0, 0, False))

    def polygon(self, cx, cy, r_circ, n, rot_deg=0.0):
        pts = [(cx + r_circ * math.cos(math.radians(rot_deg + 360 * i / n)),
                cy + r_circ * math.sin(math.radians(rot_deg + 360 * i / n))) for i in range(n)]
        self.polyline(pts, True)

    def center_line(self, x0, y0, x1, y1):
        self.centerline = self.sm.CreateCenterLine(x0 * M, y0 * M, 0, x1 * M, y1 * M, 0)
        return self.centerline

    def spline(self, pts):
        flat = []
        for x, y in pts:
            flat += [x * M, y * M, 0.0]
        seg = self.sm.CreateSpline2(dbl_array(flat), False)
        self.segments.append(seg)
        return seg


# ----------------------------------------------------------------------------- part
class Part:
    def __init__(self, sw, doc, name):
        self.sw, self.doc, self.name = sw, doc, name
        self.ext = doc.Extension
        self.fm = doc.FeatureManager
        self.last_sketch = None
        self._nplanes = 0

    # -- selection --
    def clear(self):
        self.doc.ClearSelection2(True)

    def select(self, name, typ="PLANE", append=False, mark=0):
        if not append:
            self.clear()
        ok = self.ext.SelectByID2(name, typ, 0, 0, 0, append, mark, NONE, 0)
        if not ok:
            raise RuntimeError(f"could not select {typ} '{name}'")
        return ok

    def select_ray(self, origin_mm, direction, typ=SEL_FACES, append=False, mark=0, radius_mm=0.5):
        if not append:
            self.clear()
        o = [v * M for v in origin_mm]
        return self.ext.SelectByRay(o[0], o[1], o[2], direction[0], direction[1], direction[2], radius_mm * M, typ, append, mark, 0)

    def sketch(self, plane="Front Plane"):
        s = Sketch(self, plane)
        self.last_sketch = s
        return s

    def _select_last_sketch(self):
        # the sketch just closed is the last feature named Sketch*
        f = self.last_feature("Sketch")
        self.select(f.Name, "SKETCH")
        return f

    # -- features (mm) --
    def extrude(self, depth, cut=False, flip=False, both=False, draft=0.0, merge=True, through_all=False, mid=False):
        """Extrude the last sketch. both: symmetric (each side = depth). mid: mid-plane (total = depth).
        flip reverses the direction relative to the sketch/plane normal for BOTH bosses and cuts
        (internally FeatureCut4's Dir flag is inverted because its default cuts against the normal); API arg 2 (Flip)
        is *flip side to cut* and stays False."""
        if depth <= 0:
            raise ValueError("extrude depth must be > 0 (use flip=True for the other direction)")
        self._select_last_sketch()
        d = depth * M
        if mid:
            end1, both = 6, False       # swEndCondMidPlane
        elif through_all:
            end1 = 1                    # swEndCondThroughAll
        else:
            end1 = 0                    # swEndCondBlind
        end2 = 0 if not both else end1
        single = not both
        if cut:
            # FeatureCut4 Dir=False cuts AGAINST the sketch normal (verified); invert so flip=False means +normal like bosses
            f = self.fm.FeatureCut4(single, False, (not flip), end1, end2, d, d, False, False, False, False,
                                    math.radians(draft), math.radians(draft), False, False, False, False,
                                    False, True, True, True, True, False, 0, 0, False, False)
        else:
            f = self.fm.FeatureExtrusion3(single, False, flip, end1, end2, d, d, False, False, False, False,
                                          math.radians(draft), math.radians(draft), False, False, False, False,
                                          merge, True, True, 0, 0, False)
        if f is None:
            raise RuntimeError("extrude failed")
        return f

    def revolve(self, angle=360.0, cut=False):
        """Revolve the last sketch about its centre line (sketch.center_line must have been called)."""
        s = self.last_sketch
        if s is None or s.centerline is None:
            raise RuntimeError("revolve needs a sketch with a center_line")
        f = self._select_last_sketch()
        sd = call(self.doc.SelectionManager, "CreateSelectData")
        sd.Mark = 16
        # the sketch must be selected (mark 0) and the axis (mark 16); centerline segment keeps its object
        s.centerline.Select4(True, sd)
        f = self.fm.FeatureRevolve2(True, True, False, cut, False, False, 0, 0, math.radians(angle), 0,
                                    False, False, 0.01, 0.01, 0, 0, 0, True, True, True)
        if f is None:
            raise RuntimeError("revolve failed")
        return f

    def plane_offset(self, base, dist, name=None, flip=False):
        self.select(base, "PLANE")
        f = self.fm.InsertRefPlane(8 | (512 if flip else 0), dist * M, 0, 0, 0, 0)   # 8 = distance, 512 = flip
        if f is None:
            raise RuntimeError("plane_offset failed")
        self._nplanes += 1
        f.Name = name or f"Plane_{self._nplanes}"
        return f.Name

    def fillet(self, radius, edge_filter=None, edges=None):
        """Fillet edges. edge_filter(p0_mm, p1_mm, is_line) -> bool selects edges of all bodies."""
        self.clear()
        n = 0
        for e, p0, p1, is_line in (edges or self.edges()):
            if edge_filter is None or edge_filter(p0, p1, is_line):
                e.Select4(True, NONE); n += 1
        if n == 0:
            raise RuntimeError("fillet: no edges matched")
        f = self.fm.FeatureFillet3(195, radius * M, 0, 0, 0, 0, 0, NONE, NONE, NONE, NONE, NONE, NONE, NONE)
        if f is None:
            raise RuntimeError("fillet failed")
        return f

    def chamfer(self, dist, edge_filter=None):
        self.clear()
        n = 0
        for e, p0, p1, is_line in self.edges():
            if edge_filter is None or edge_filter(p0, p1, is_line):
                e.Select4(True, NONE); n += 1
        if n == 0:
            raise RuntimeError("chamfer: no edges matched")
        f = self.fm.InsertFeatureChamfer(4, 4, dist * M, 0, 0, 0, 0, 0)   # 4 = equal-distance
        if f is None:
            raise RuntimeError("chamfer failed")
        return f

    def shell(self, thickness, open_face_rays):
        """open_face_rays: list of (origin_mm, direction) rays; each selects a face to remove."""
        self.clear()
        for o, d in open_face_rays:
            if not self.select_ray(o, d, SEL_FACES, append=True):
                raise RuntimeError(f"shell: ray {o}->{d} hit no face")
        before = self.feature_count()
        self.doc.InsertFeatureShell(thickness * M, False)
        if self.feature_count() == before:
            raise RuntimeError("shell failed")

    def mirror_bodies(self, plane="Right Plane", body_rays=None):
        """Mirror all solid bodies (or those hit by body_rays) about a plane, merging where they touch."""
        self.clear()
        self.select(plane, "PLANE", append=False, mark=2)
        if body_rays:
            for o, d in body_rays:
                self.select_ray(o, d, SEL_SOLIDBODIES, append=True, mark=256)
        else:
            for b in self.bodies():
                # select body via a ray through its bounding box centre
                bb = call(b, "GetBodyBox")
                c = [(bb[0] + bb[3]) / 2 / M, (bb[1] + bb[4]) / 2 / M, (bb[2] + bb[5]) / 2 / M]
                self.select_ray([c[0], c[1], bb[5] / M + 50], [0, 0, -1], SEL_SOLIDBODIES, append=True, mark=256)
        f = self.fm.InsertMirrorFeature2(True, False, False, False, 0)
        if f is None:
            raise RuntimeError("mirror failed")
        return f

    def mirror_feature(self, plane, feature_names):
        self.clear()
        self.select(plane, "PLANE", append=False, mark=2)
        for n in feature_names:
            self.ext.SelectByID2(n, "BODYFEATURE", 0, 0, 0, True, 1, NONE, 0)
        f = self.fm.InsertMirrorFeature2(False, False, False, False, 0)
        if f is None:
            raise RuntimeError("mirror feature failed")
        return f

    def combine_add(self):
        """Boolean-add all bodies into one."""
        self.clear()
        bodies = self.bodies()
        if len(bodies) < 2:
            return None
        for b in bodies:
            bb = call(b, "GetBodyBox")
            c = [(bb[0] + bb[3]) / 2 / M, (bb[1] + bb[4]) / 2 / M, (bb[2] + bb[5]) / 2 / M]
            self.select_ray([c[0], c[1], bb[5] / M + 50], [0, 0, -1], SEL_SOLIDBODIES, append=True, mark=2)
        f = self.fm.InsertCombineFeature(15903, NONE, NONE)   # swBodyOperationType_e.SWBODYADD
        return f

    # -- geometry queries --
    def bodies(self):
        b = self.doc.GetBodies2(0, True)
        return list(b) if b else []

    def edges(self):
        out = []
        for b in self.bodies():
            for e in call(b, "GetEdges"):
                v0, v1 = call(e, "GetStartVertex"), call(e, "GetEndVertex")
                if v0 is None or v1 is None:
                    # closed edge (full circle): use curve bounds midpoint via GetCurveParams3
                    cp = call(e, "GetCurveParams3")
                    p0 = [cp.StartPoint[i] / M for i in range(3)]
                    out.append((e, p0, p0, False))
                    continue
                p0 = [x / M for x in call(v0, "GetPoint")]
                p1 = [x / M for x in call(v1, "GetPoint")]
                crv = call(e, "GetCurve")
                out.append((e, p0, p1, bool(call(crv, "IsLine"))))
        return out

    def feature_count(self):
        n, f = 0, call(self.doc, "FirstFeature")
        while f:
            n += 1; f = call(f, "GetNextFeature")
        return n

    def last_feature(self, prefix):
        found, f = None, call(self.doc, "FirstFeature")
        while f:
            if f.Name.startswith(prefix):
                found = f
            f = call(f, "GetNextFeature")
        if found is None:
            raise RuntimeError(f"no feature starting with {prefix}")
        return found

    def mass_props(self, density_kg_m3=1270.0):
        """Returns (mass_kg, volume_mm3, com_mm) using the given density (PETG ~1.27 g/cc)."""
        mp = call(self.ext, "CreateMassProperty")
        vol = mp.Volume
        com = [c / M for c in mp.CenterOfMass]
        return vol * density_kg_m3, vol / (M ** 3), com

    def bbox(self):
        """Overall bounding box in mm: (xmin,ymin,zmin,xmax,ymax,zmax)."""
        lo = [1e9] * 3; hi = [-1e9] * 3
        for b in self.bodies():
            bb = call(b, "GetBodyBox")
            for i in range(3):
                lo[i] = min(lo[i], bb[i] / M); hi[i] = max(hi[i], bb[i + 3] / M)
        return (*lo, *hi)

    # -- appearance / output --
    def color(self, rgb, faces=None):
        vals = dbl_array([rgb[0], rgb[1], rgb[2], 1, 1, 0.5, 0.4, 0, 0])
        if faces is None:
            self.doc.MaterialPropertyValues = vals
        else:
            for fc in faces:
                fc.MaterialPropertyValues = vals

    def color_feature(self, feature, rgb):
        self.color(rgb, faces=list(call(feature, "GetFaces")))

    def color_faces_by_ray(self, rays, rgb):
        for o, d in rays:
            self.clear()
            if self.select_ray(o, d, SEL_FACES):
                fc = self.doc.SelectionManager.GetSelectedObject6(1, -1)
                self.color(rgb, faces=[fc])
        self.clear()

    def rebuild(self):
        return call(self.doc, "EditRebuild3")

    def view(self, name="*Isometric"):
        self.doc.ShowNamedView2(name, 7 if name == "*Isometric" else -1)
        self.doc.ViewZoomtofit2()
        self.doc.GraphicsRedraw2()

    def activate(self):
        """Make this document the active one (exports such as STEP silently export the active doc)."""
        self.sw.app.ActivateDoc2(call(self.doc, "GetTitle"), False, _byref_int())

    def save(self, path):
        errs, warns = _byref_int(), _byref_int()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.activate()
        ok = self.ext.SaveAs3(path, 0, 1, NONE, NONE, errs, warns)
        if not ok:
            raise RuntimeError(f"save failed ({errs.value}) for {path}")
        return path

    def export_stl(self, path):
        return self.save(path)

    def screenshot(self, path, view="*Isometric"):
        self.view(view)
        return self.save(path)

    def close(self):
        self.sw.app.CloseDoc(call(self.doc, "GetTitle"))


# ----------------------------------------------------------------------------- assembly
class Assembly:
    def __init__(self, sw, doc, name):
        self.sw, self.doc, self.name = sw, doc, name
        self.ext = doc.Extension
        self.components = {}

    def add(self, part_path, R=IDENT, t_mm=(0, 0, 0), fixed=True, key=None):
        # AddComponent5 needs the component document loaded in the session: open it silently first
        errs, warns = _byref_int(), _byref_int()
        self.sw.app.OpenDoc6(part_path, 1, 1, "", errs, warns)
        self.sw.app.ActivateDoc2(call(self.doc, "GetTitle"), False, _byref_int())
        comp = self.doc.AddComponent5(part_path, 0, "", False, "", 0, 0, 0)
        if comp is None:
            raise RuntimeError(f"AddComponent5 failed for {part_path}")
        xf = comp.Transform2
        xf.ArrayData = dbl_array(sw_transform_data(R, t_mm))
        comp.Transform2 = xf
        comp.Select4(False, NONE, False)
        if fixed:
            self.doc.FixComponent()
        else:
            self.doc.UnfixComponent()
        self.doc.ClearSelection2(True)
        key = key or os.path.splitext(os.path.basename(part_path))[0]
        self.components[key] = comp
        return comp

    def select_ray(self, origin_mm, direction, typ=SEL_FACES, append=False, mark=1, radius_mm=0.5):
        if not append:
            self.doc.ClearSelection2(True)
        o = [v * M for v in origin_mm]
        return self.ext.SelectByRay(o[0], o[1], o[2], direction[0], direction[1], direction[2], radius_mm * M, typ, append, mark, 0)

    def probe(self, ray):
        """Return (component_name, surface_kind) for the first face hit by ray, or None."""
        self.doc.ClearSelection2(True)
        if not self.select_ray(*ray, append=True, mark=1):
            return None
        sm = self.doc.SelectionManager
        face = sm.GetSelectedObject6(1, -1)
        comp = sm.GetSelectedObjectsComponent4(1, -1)
        surf = call(face, "GetSurface")
        kind = "cylinder" if call(surf, "IsCylinder") else "plane" if call(surf, "IsPlane") else "other"
        self.doc.ClearSelection2(True)
        return (comp.Name2 if comp else "?", kind)

    def mate(self, ray_a, ray_b, mate_type=MATE_CONCENTRIC, align=MATE_ALIGN_CLOSEST, dist_mm=0.0):
        """Mate the faces hit by two rays (origin_mm, direction)."""
        self.doc.ClearSelection2(True)
        if not self.select_ray(*ray_a, append=True, mark=1):
            raise RuntimeError(f"mate: ray A {ray_a} hit nothing")
        if not self.select_ray(*ray_b, append=True, mark=1):
            raise RuntimeError(f"mate: ray B {ray_b} hit nothing")
        err = _byref_int()
        m = self.doc.AddMate5(mate_type, align, False, dist_mm * M, dist_mm * M, dist_mm * M, 0, 0, 0, 0, 0, False, False, 0, err)
        self.doc.ClearSelection2(True)
        return m, err.value

    def rebuild(self):
        return call(self.doc, "EditRebuild3")

    def view(self, name="*Isometric"):
        self.doc.ShowNamedView2(name, 7 if name == "*Isometric" else -1)
        self.doc.ViewZoomtofit2()
        self.doc.GraphicsRedraw2()

    def save(self, path):
        errs, warns = _byref_int(), _byref_int()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.sw.app.ActivateDoc2(call(self.doc, "GetTitle"), False, _byref_int())
        ok = self.ext.SaveAs3(path, 0, 1, NONE, NONE, errs, warns)
        if not ok:
            raise RuntimeError(f"save failed ({errs.value}) for {path}")
        return path

    def screenshot(self, path, view="*Isometric"):
        self.view(view)
        return self.save(path)
