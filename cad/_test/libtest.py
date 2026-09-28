import sys, os; sys.path.insert(0, r"D:\Project\thenar-duck\cad")
from swlib import *
sw = SW(); sw.close_all()
out = r"D:\Project\thenar-duck\cad\_test"
# ---- servo mock (placeholder dims, STS3215-like: 45.2 L x 24.7 W x 32 H, ears at top) ----
p = sw.new_part("servo_mock")
with p.sketch("Top Plane") as s:           # body footprint in XZ plane (Top plane: sketch x -> X, sketch y -> -Z)
    s.rect(0, 0, 45.2, 24.7)
p.extrude(32.0)                              # body up +Y
with p.sketch("Top Plane") as s:           # mounting ears
    s.rect(0, 0, 61.0, 24.7)
p.extrude(2.5, flip=True)
p.plane_offset("Top Plane", 32.0, "TopFace")
with p.sketch("TopFace") as s:             # output shaft boss at 11.3 mm from one end
    s.circle(11.3, 0, 6.0)
p.extrude(4.0)
with p.sketch("TopFace") as s:             # revolve test: horn disc via revolve
    s.polyline([(11.3, 4), (11.3 + 9, 4), (11.3 + 9, 6), (11.3, 6)], close=True)
    s.center_line(11.3, 0, 11.3, 10)
p.revolve(360)
with p.sketch("TopFace") as s:             # ear holes cut
    for x in (-27, 27):
        for z in (-8, 8):
            s.circle(x, z, 1.6)
p.extrude(60, cut=True, through_all=True, both=True)
p.fillet(1.5, lambda p0, p1, is_line: is_line and abs(p0[1] - p1[1]) > 20)   # vertical body edges
p.chamfer(0.5, lambda p0, p1, is_line: (not is_line) and p0[1] > 35.9)  # boss top rim
p.color((0.12, 0.12, 0.13))
bb = p.bbox(); print("bbox", [round(v, 1) for v in bb])
m, vol, com = p.mass_props(); print("mass g", round(m * 1000, 1), "com", [round(c, 1) for c in com])
p.save(out + r"\servo_mock.SLDPRT"); p.export_stl(out + r"\servo_mock.STL"); p.screenshot(out + r"\servo_mock.png")
# ---- bracket with shell + mirror ----
b = sw.new_part("bracket")
with b.sketch("Front Plane") as s:
    s.rounded_rect(0, 20, 60, 40, 5)
b.extrude(30, mid=True)
b.shell(2.0, [([0, 45, 0], [0, -1, 0])])       # remove top face -> U channel
with b.sketch("Front Plane") as s:
    s.circle(0, 20, 6.2)
b.extrude(100, cut=True, mid=True)
b.color((0.95, 0.95, 0.93))
b.save(out + r"\bracket.SLDPRT"); b.screenshot(out + r"\bracket.png")
# ---- assembly with concentric mate ----
a = sw.new_assembly("test_asm")
a.add(out + r"\servo_mock.SLDPRT", IDENT, (0, 0, 0), fixed=True)
a.add(out + r"\bracket.SLDPRT", rot_x(90), (80, 60, 0), fixed=False)
# rays: servo shaft boss cylinder (hit from the side), bracket hole cylinder (hit from inside the hole outward)
m, err = a.mate(([11.3, 34, 50], [0, 0, -1]), ([80, 60, 60], [0, 0, -1]), MATE_CONCENTRIC)
print("mate concentric", m is not None, err)
a.rebuild(); a.save(out + r"\test_asm.SLDASM"); a.screenshot(out + r"\test_asm.png")
print("DONE")
