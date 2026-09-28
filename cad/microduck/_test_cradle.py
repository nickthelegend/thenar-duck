import sys, os; sys.path.insert(0, r"D:\Project\thenar-duck\cad\microduck")
from common import *
sw = SW(); sw.close_all()
w = PETG["wall_bracket"]; floor = 2.5
L, W, Hh = SERVO["L"], SERVO["W"], SERVO["H_case"] / 2
p = sw.new_part("cradle")
with p.sketch("Top Plane") as s:                       # block footprint (x = length, sketch y -> -Z)
    s.rounded_rect(0, 0, L + 2 * w + 0.5, W + 2 * w + 0.5, 3.0)
p.extrude(floor + Hh)                                  # +Y
p.plane_offset("Top Plane", floor, "FloorTop")
with p.sketch("FloorTop") as s:                        # servo pocket (idler face down)
    sx, sy = sk_servo_outline(s, 0, 0, 0)
p.extrude(Hh + 1, cut=True)                            # cut upward from the floor
with p.sketch("Top Plane") as s:                       # face-B mount holes + idler shaft clearance, through all
    pts = sk_servo_mount_holes(s, 0, 0, 0, face="B")
    s.circle(SERVO["shaft_x"], 0, 7.5 / 2)
p.extrude(50, cut=True, through_all=True, both=True)
inside = lambda p0, p1, il: edge_is_vertical(1, 10.0)(p0, p1, il) and abs(p0[0]) < L / 2 + 1 and abs(p0[2]) < W / 2 + 1
p.fillet(PETG["fillet_inner"], inside)
p.chamfer(PETG["chamfer_bottom"], edge_in_plane(1, 0.0))
m, bb = finish_and_save(p, "_test_servo_cradle", COL["dark"])
# assembly with the vendor servo: servo Z (shaft) -> SW +Y, body centre at y = floor + Hh
a = sw.new_assembly("cradle_test")
a.add(os.path.join(CAD_OUT, "_test_servo_cradle.SLDPRT"), IDENT, (0, 0, 0), fixed=True)
a.add(SERVO_SLDPRT, rot_x(-90), (0, floor + Hh, 0), fixed=True, key="servo")
a.rebuild()
for c in a.doc.GetComponents(True): print(c.Name2, [round(v / M, 1) for v in c.GetBox(False, False)])
print("probe pocket floor:", a.probe(([-10, 40, 0], [0, -1, 0])), " probe servo top:", a.probe(([-10, 60, 0], [0, -1, 0])))
a.save(os.path.join(CAD_OUT, "_test_cradle.SLDASM")); a.screenshot(os.path.join(IMG_OUT, "_test_cradle_asm.png"))
print("DONE")
