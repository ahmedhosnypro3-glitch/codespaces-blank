#!/usr/bin/env python3
"""Verify slide_013 rejudge render against the original frame geometry + house frame.

Expected geometry comes from analysis/reanalysis_v2/slide_013_reanalysis.txt mapped
through the build's 1px = 1pt (960x540 -> 13.33x7.5in) transform. Major elements are
checked by ink colour bbox with ~4px tolerance; house chrome is asserted directly.
"""
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
RENDER = V + "/recreated_pptx/build/slide_013_rejudge_rendered-1.png"

img = Image.open(RENDER).convert("RGB")
W, H = img.size
px = img.load()
print("render:", RENDER, f"{W}x{H}")
assert (W, H) == (2001, 1125), "unexpected render size"

SX = W / 960.0   # 2.0844 render px per original px
SY = H / 540.0
IN_X = W / 13.33  # 150.06 render px per inch
IN_Y = H / 7.5

def R(x, y):
    return (x * SX, y * SY)

def close(p, t, tol):
    return all(abs(a - b) <= tol for a, b in zip(p, t))

def ink_bbox(target, tol, x0, y0, x1, y1, min_count=8):
    xs, ys = [], []
    for y in range(int(y0), int(y1)):
        for x in range(int(x0), int(x1)):
            if close(px[x, y], target, tol):
                xs.append(x); ys.append(y)
    if len(xs) < min_count:
        return None, len(xs)
    return (min(xs), min(ys), max(xs), max(ys)), len(xs)

def near(target, tol, cx, cy, rad):
    for y in range(int(cy - rad), int(cy + rad) + 1):
        for x in range(int(cx - rad), int(cx + rad) + 1):
            if 0 <= x < W and 0 <= y < H and close(px[x, y], target, tol):
                return True
    return False

results = []
def check(name, ok, detail):
    results.append(ok)
    print(("PASS  " if ok else "FAIL  ") + name + "  ::  " + detail)

# ---------------- house frame + background ----------------
bg_ok = close(px[8, 8], (0xE8, 0xE8, 0xE8), 10)
check("background #E8E8E8", bg_ok, f"corner px {px[8, 8]}")

def edge_hit(x, y):
    return near((0xC0, 0x00, 0x00), 70, x, y, 5)

FX0, FY0 = 0.15 * IN_X, 0.15 * IN_Y
FX1, FY1 = 13.18 * IN_X, 7.35 * IN_Y
edges = {
    "top":    [edge_hit(FX0 + 25, FY0), edge_hit(W / 2, FY0), edge_hit(FX1 - 25, FY0)],
    "bottom": [edge_hit(FX0 + 25, FY1), edge_hit(W / 2, FY1), edge_hit(FX1 - 25, FY1)],
    "left":   [edge_hit(FX0, FY0 + 25), edge_hit(FX0, H / 2), edge_hit(FX0, FY1 - 25)],
    "right":  [edge_hit(FX1, FY0 + 25), edge_hit(FX1, H / 2), edge_hit(FX1, FY1 - 25)],
}
check("house frame red rect (0.15in inset, all edges)",
      all(all(v) for v in edges.values()),
      "edges " + ", ".join(k + ":" + str(all(v)) for k, v in edges.items()))

# badge: oval 12.48-12.98in x 0.30-0.80in, fill FFF9C4, dark bold numeral
bx0, by0, bx1, by1 = 12.48 * IN_X, 0.30 * IN_Y, 12.98 * IN_X, 0.80 * IN_Y
fill_ok = near((0xFF, 0xF9, 0xC4), 12, (bx0 + bx1) / 2, (by0 + by1) / 2, 6)
ink, n = ink_bbox((0x33, 0x33, 0x33), 45, bx0 - 4, by0 - 4, bx1 + 4, by1 + 4, min_count=10)
check("badge oval FFF9C4 + numeral ink", bool(fill_ok and ink),
      f"fill={fill_ok} ink_bbox={ink} n={n}")

# ---------------- content elements (expected bboxes in render px) ----------------
TOL = 5  # ~4px tolerance + stroke half-width
def element(name, target, tol, exp, window_pad=12, min_count=8):
    ex0, ey0 = R(exp[0], exp[1]); ex1, ey1 = R(exp[2], exp[3])
    bb, n = ink_bbox(target, tol,
                     ex0 - window_pad * SX - 6, ey0 - window_pad * SY - 6,
                     ex1 + window_pad * SX + 6, ey1 + window_pad * SY + 6, min_count)
    if bb is None:
        check(name, False, f"no ink found (n={n})")
        return
    dx = max(abs(bb[0] - ex0), abs(bb[1] - ey0), abs(bb[2] - ex1), abs(bb[3] - ey1))
    check(name, dx <= TOL,
          f"ink bbox {tuple(round(v,1) for v in bb)} vs expected {tuple(round(v,1) for v in (ex0,ey0,ex1,ey1))} maxdev={dx:.1f}px n={n}")

# truth table outer border FF3030 (93,131)-(300,295); stroke is 2pt -> grows ~2px out
element("truth table border bbox", (0xFF, 0x30, 0x30), 40, (93 - 2, 131 - 2, 300 + 2, 295 + 2))
# plot panel pink hairline E89898 (510,107)-(800,355)
element("scatter plot panel border bbox", (0xE8, 0x98, 0x98), 22, (510, 107, 800, 355))
# schematic panel pink border (135,343)-(490,473)
element("neuron schematic panel border bbox", (0xE8, 0x98, 0x98), 22, (135, 343, 490, 473))
# caption peach fill FDE7E0 (548,396)-(740,442)
element("caption box bbox", (0xFD, 0xE7, 0xE0), 10, (548, 396, 740, 442))

# ---------------- title ----------------
tx0, ty0, tx1, ty1 = 0.6 * IN_X, 0.26 * IN_Y, 12.73 * IN_X, 1.15 * IN_Y
bb, n = ink_bbox((0xC0, 0x00, 0x00), 45, tx0, ty0, tx1, ty1, min_count=30)
if bb is None:
    check("title crimson, centered, in house band", False, f"no ink (n={n})")
else:
    cx = (bb[0] + bb[2]) / 2
    h_ink = bb[3] - bb[1]
    check("title crimson, centered, in house band",
          abs(cx - W / 2) <= 8 and 20 <= h_ink <= 80 and bb[1] >= 0.26 * IN_Y - 4,
          f"bbox {tuple(round(v,1) for v in bb)} center_dev={abs(cx-W/2):.1f}px height={h_ink}px")

# ---------------- neuron fan: three distinct arc terminations ----------------
LAV = (0xC8, 0xC8, 0xD8)
terms = {"upper-left (287,398)": (287, 398), "mid-left (285,405)": (285, 405), "lower-left (287,412)": (287, 412)}
for label, (tx, ty) in terms.items():
    cx, cy = R(tx, ty)
    ok = near(LAV, 30, cx, cy, 7)
    check("fan stroke terminates at " + label, ok, f"lavender near render ({cx:.0f},{cy:.0f}) rad 7px")

# mid-line must touch the circle's leftmost point (285,405): lavender at the arc
cx, cy = R(285, 405)
check("fan touches the node arc (mid-left)", near(LAV, 30, cx, cy, 4),
      f"lavender at arc ({cx:.0f},{cy:.0f})")

# red arrowhead just OUTSIDE the arc: red ink left of x=286 at y=405, none right of 287
cy = R(0, 405)[1]
red_left = near((0xFF, 0x00, 0x00), 45, R(278, 0)[0], cy, 6)
red_inside = near((0xFF, 0x00, 0x00), 45, R(290, 0)[0], cy, 4)
check("red arrowhead outside arc, pointing into node", bool(red_left and not red_inside),
      f"red@x278={red_left} red@x290={red_inside} (arc leftmost x=285)")

# spread: upper and lower terminations distinct (14 original px -> ~29 render px)
check("fan terminations span the arc (not a single junction)",
      abs(R(0, 412)[1] - R(0, 398)[1]) >= 20 and near(LAV, 30, *R(287, 398), 7) and near(LAV, 30, *R(287, 412), 7),
      f"termination spread {abs(R(0,412)[1]-R(0,398)[1]):.1f} render px")

# ---------------- Σ glyph + activation glyph + O/P ----------------
sx0, sy0 = R(286, 391); sx1, sy1 = R(315, 419)
sig_ok, n = ink_bbox((0, 0, 0), 60, sx0, sy0, sx1, sy1, min_count=6)
check("Σ glyph ink inside node circle", sig_ok is not None, f"bbox={sig_ok} n={n}")
ax0, ay0 = R(343, 394); ax1, ay1 = R(379, 419)
gl, n = ink_bbox((0x3F, 0x00, 0xFF), 45, ax0, ay0, ax1, ay1, min_count=4)
check("step-function glyph ink inside activation box", gl is not None, f"bbox={gl} n={n}")

# ---------------- table chips ----------------
c0, n0 = ink_bbox((0xCC, 0xFF, 0xFF), 12, *R(236, 132), *R(300, 295), min_count=40)
c1, n1 = ink_bbox((0xCC, 0xFF, 0xCC), 12, *R(236, 132), *R(300, 295), min_count=40)
check("O/P chips: 2 cyan + 2 green fills", bool(c0 and c1), f"cyan n={n0} green n={n1}")

print()
bad = results.count(False)
print(f"SUMMARY: {len(results)-bad}/{len(results)} checks passed" + ("" if bad == 0 else f"  ({bad} FAILED)"))
raise SystemExit(1 if bad else 0)
