"""
common.py - shared constants and sketch-level feature helpers for the microduck CAD.

Numbers come from research/03_sts3215.md (Waveshare DXF / Feetech drawing) and research/04_printing_petg_p1s.md.
Units: mm and degrees everywhere.

Frames
------
Robot/spec frame (design/spec.json):   X forward, Y left, Z up, origin on the floor between the feet.
SolidWorks assembly frame:             X forward, Y up,   Z right  (right-handed).   sw = (x, z, -y)
STS3215 vendor STEP (cad/vendor/STS3215.SLDPRT): origin at the footprint centre, Z = shaft axis (+Z = output/spline face),
    X along the 45.22 length with the shaft at X = +12.5, Y across the 24.72 width.
"""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from swlib import *  # noqa

ROOT = r"D:\Project\thenar-duck"
CAD_OUT = os.path.join(ROOT, "cad", "microduck", "parts")
STL_OUT = os.path.join(ROOT, "cad", "microduck", "stl")
IMG_OUT = os.path.join(ROOT, "cad", "microduck", "renders")
SERVO_SLDPRT = os.path.join(ROOT, "cad", "vendor", "STS3215.SLDPRT")

# ----------------------------------------------------------------------------- STS3215 (ST-3215-C018, 12 V)
SERVO = dict(
    L=45.22, W=24.72,            # footprint
    H_case=29.0,                 # between the two flat mounting faces
    boss_h=3.0,                  # raised gear-head cover on the spline face (D-shaped, r 10.85, flat 12.5 behind axis)
    boss_r=10.9, boss_flat_behind_axis=12.5,
    rear_h=3.0,                  # rear cover on the idler face  (total catalogue height 35)
    idler_shaft_d=6.0, idler_shaft_protrusion=4.1,
    shaft_from_end=10.11,        # output shaft axis from the gearbox end face, on the width centreline
    shaft_x=12.5,                # = L/2 - 10.11, shaft X in the vendor STEP frame
    mount_y=10.25,               # mounting holes at Y = +-10.25 (20.5 across)
    mount_x_front=18.41,         # from the output end, both faces
    mount_x_rear_A=42.86,        # spline face (A) rear pair, from output end
    mount_x_rear_B=39.11,        # idler face (B) rear pair, from output end
    pilot_d=1.6,                 # PA2.0 self-tapping / M2 machine screw pilot
    horn_d=19.2, horn_hole_d=2.5, horn_hole_r=7.0, horn_thick=3.1, horn_center_screw="M3x6",
    spline_od=5.9, horn_top_above_face=6.0,   # horn top ~ +18.7 from centre -> ~4.2 above the boss
    mass_g=55.0,
    stall_kgcm=30.0, rated_kgcm=10.0, no_load_rpm=45.0, stall_A=2.7,
    connector_note="5264-3P plug exits sideways at the rear-bottom corner; leave >= 10 mm side clearance",
)

# ----------------------------------------------------------------------------- PETG on P1S design rules
PETG = dict(
    density_g_cc=1.27,
    wall_shell=1.77,             # 4 walls of 0.42/0.45 -> shells
    wall_bracket=2.22,           # 5 walls -> load-bearing brackets
    wall_min=1.32,               # 3 walls
    servo_clearance=0.25,        # per side, pocket for the 45.22 x 24.72 body
    boss_clearance=0.4,          # around the D-shaped gear-head boss
    m2_clear=2.3, m25_clear=2.8, m3_clear=3.3,        # through-hole clearances (after +0.1 XY hole comp)
    insert_M2=dict(hole=3.15, boss_od=6.4, depth=4.5),
    insert_M25=dict(hole=3.6, boss_od=7.2, depth=5.5),
    insert_M3=dict(hole=3.95, boss_od=8.0, depth=7.0),
    bearing_684_press=8.92, bearing_684_slip=9.07, bearing_684_depth=4.2,
    bearing_MR115_press=10.92, bearing_MR115_slip=11.07, bearing_MR115_depth=4.2,
    max_overhang_deg=45.0, max_bridge=25.0,
    fillet_outer=2.0, fillet_inner=1.0, chamfer_bottom=0.5,
    plate=256.0,
)

BUILD_MAX = 250.0   # keep every part comfortably inside the 256 mm plate

# ----------------------------------------------------------------------------- colours (RGB 0-1)
COL = dict(
    shell=(0.93, 0.93, 0.90),       # matte off-white PETG
    dark=(0.12, 0.12, 0.13),        # black/charcoal structural links
    accent=(0.10, 0.40, 0.85),      # blue stripe / accent
    grey=(0.55, 0.56, 0.58),
    lens=(0.85, 0.90, 1.0),
    servo=(0.13, 0.13, 0.14),
    tpu=(0.20, 0.20, 0.22),
)


# ----------------------------------------------------------------------------- frame helpers
def robot_to_sw(p):
    """Robot frame (X fwd, Y left, Z up) -> SolidWorks assembly frame (X fwd, Y up, Z right)."""
    return [p[0], p[2], -p[1]]


def rot2(x, y, deg):
    a = math.radians(deg); c, s = math.cos(a), math.sin(a)
    return x * c - y * s, x * s + y * c


def R_robot_to_sw():
    """Rotation matrix taking robot-frame axes to SW axes (columns = images of x,y,z)."""
    return [[1, 0, 0], [0, 0, 1], [0, -1, 0]]


# ----------------------------------------------------------------------------- sketch-level features
def sk_servo_outline(s, cx, cy, ang=0.0, clearance=None, shaft_along=None):
    """Rectangle footprint of the STS3215 seen along its shaft axis, centred on the BODY centre (cx, cy),
    rotated by ang. Sketch +x is the servo's length direction at ang=0. Returns the shaft centre (x, y)."""
    c = PETG["servo_clearance"] if clearance is None else clearance
    L, W = SERVO["L"] + 2 * c, SERVO["W"] + 2 * c
    pts = [rot2(px, py, ang) for px, py in [(-L / 2, -W / 2), (L / 2, -W / 2), (L / 2, W / 2), (-L / 2, W / 2)]]
    s.polyline([(cx + x, cy + y) for x, y in pts], close=True)
    sx, sy = rot2(SERVO["shaft_x"], 0, ang)
    return cx + sx, cy + sy


def sk_servo_side_profile(s, cx, cy, ang=0.0, clearance=None, with_bosses=True):
    """Profile of the servo seen from the side (length x height), centred on the case centre.
    Sketch +x = length direction, +y = shaft axis (spline face at +y). Used to cut clamshell pockets."""
    c = PETG["servo_clearance"] if clearance is None else clearance
    L = SERVO["L"] + 2 * c
    H = SERVO["H_case"] + 2 * c
    pts = [(-L / 2, -H / 2), (L / 2, -H / 2), (L / 2, H / 2), (-L / 2, H / 2)]
    s.polyline([(cx + x, cy + y) for x, y in (rot2(px, py, ang) for px, py in pts)], close=True)


def sk_servo_mount_holes(s, cx, cy, ang=0.0, face="A", dia=None):
    """The 4 mounting holes of face A (spline) or B (idler) as circles, servo body centre at (cx, cy), +x = length.
    Positions are measured from the output end (= +x end of the body)."""
    d = dia or PETG["m2_clear"]
    L = SERVO["L"]
    xr = SERVO["mount_x_rear_A"] if face == "A" else SERVO["mount_x_rear_B"]
    pts = []
    for xo in (SERVO["mount_x_front"], xr):
        for y in (-SERVO["mount_y"], SERVO["mount_y"]):
            x = L / 2 - xo          # from output end -> body-centre coordinates
            pts.append(rot2(x, y, ang))
    for x, y in pts:
        s.circle(cx + x, cy + y, d / 2)
    return [(cx + x, cy + y) for x, y in pts]


def sk_horn_holes(s, cx, cy, ang=0.0, dia=None, center_dia=None):
    """4 horn holes on the 14 mm cross + optional centre clearance, around a shaft centre (cx, cy)."""
    d = dia or PETG["m3_clear"]
    for k in range(4):
        x, y = rot2(SERVO["horn_hole_r"], 0, ang + 90 * k)
        s.circle(cx + x, cy + y, d / 2)
    if center_dia:
        s.circle(cx, cy, center_dia / 2)


def sk_boss_clearance(s, cx, cy, extra=None):
    """Round clearance for the D-shaped gear-head boss (use a full circle: simpler, prints better)."""
    r = SERVO["boss_r"] + (PETG["boss_clearance"] if extra is None else extra)
    s.circle(cx, cy, r)


def sk_insert_holes(s, pts, size="M3"):
    key = {"M2": "insert_M2", "M2.5": "insert_M25", "M3": "insert_M3"}[size]
    for x, y in pts:
        s.circle(x, y, PETG[key]["hole"] / 2)


def sk_clearance_holes(s, pts, size="M3"):
    d = {"M2": PETG["m2_clear"], "M2.5": PETG["m25_clear"], "M3": PETG["m3_clear"]}[size]
    for x, y in pts:
        s.circle(x, y, d / 2)


def sk_bearing_pocket(s, cx, cy, bearing="684", fit="press"):
    d = PETG[f"bearing_{bearing}_{fit}"]
    s.circle(cx, cy, d / 2)


def sk_chamfered_rect(s, cx, cy, w, h, c):
    """Octagon-ish rectangle with 45-degree corner chamfers of size c (BDX panel look)."""
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    s.polyline([(x0 + c, y0), (x1 - c, y0), (x1, y0 + c), (x1, y1 - c), (x1 - c, y1), (x0 + c, y1), (x0, y1 - c), (x0, y0 + c)], True)


def sk_grille(s, cx, cy, w, h, n, slot_h=1.6):
    """n horizontal louvre slots inside a w x h area (for the torso vent / head speaker look)."""
    pitch = h / n
    for i in range(n):
        y = cy - h / 2 + pitch * (i + 0.5)
        s.rounded_rect(cx, y, w, slot_h, slot_h / 2 - 0.01)


def sk_hole_grid(s, cx, cy, dx, dy, nx, ny, d):
    for i in range(nx):
        for j in range(ny):
            s.circle(cx + (i - (nx - 1) / 2) * dx, cy + (j - (ny - 1) / 2) * dy, d / 2)


# ----------------------------------------------------------------------------- part-level helpers
def finish_and_save(part, name, color=None, stl=True, views=("*Isometric",), density=None):
    """Colour, rebuild, save SLDPRT (+STL, +PNG renders) into the microduck folders. Returns mass (g) and bbox."""
    for d in (CAD_OUT, STL_OUT, IMG_OUT):
        os.makedirs(d, exist_ok=True)
    if color:
        part.color(color)
    part.rebuild()
    bb = part.bbox()
    size = [bb[3] - bb[0], bb[4] - bb[1], bb[5] - bb[2]]
    if max(size) > BUILD_MAX:
        print(f"  !! {name}: {size} exceeds {BUILD_MAX} mm build limit")
    m, vol, com = part.mass_props((density or PETG["density_g_cc"]) * 1000)
    part.save(os.path.join(CAD_OUT, name + ".SLDPRT"))
    if stl:
        part.export_stl(os.path.join(STL_OUT, name + ".STL"))
    for v in views:
        tag = v.strip("*").lower()
        part.screenshot(os.path.join(IMG_OUT, f"{name}_{tag}.png"), v)
    print(f"  {name}: size {[round(x,1) for x in size]} mm, mass {m*1000:.1f} g, com {[round(c,1) for c in com]}")
    return m * 1000, bb


def edge_is_vertical(axis=1, min_len=5.0):
    """Edge filter factory: straight edges parallel to the given axis (0=X,1=Y,2=Z) longer than min_len."""
    def f(p0, p1, is_line):
        if not is_line:
            return False
        d = [abs(p1[i] - p0[i]) for i in range(3)]
        return d[axis] >= min_len and all(d[i] < 0.01 for i in range(3) if i != axis)
    return f


def edge_in_plane(axis=1, value=0.0, tol=0.05):
    """Edge filter: both endpoints lie at coordinate[axis] == value (e.g. the outline of a top face)."""
    def f(p0, p1, is_line):
        return abs(p0[axis] - value) < tol and abs(p1[axis] - value) < tol
    return f


def edge_any(*filters):
    return lambda p0, p1, il: any(f(p0, p1, il) for f in filters)
