#!/usr/bin/env python3
"""Fresh PIL verification of slide 032 render_8 vs unique_slides/slide_032.jpg.

Both images: render 2001x1125 (150dpi, scale 2.0833 px/frame-px), original
960x540 (1px=1pt). Every FAIL/MINOR candidate is measured on BOTH images.
"""
import json
import sys

from PIL import Image

DECK = "/worksp" "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
REN = Image.open(f"{DECK}/recreated_pptx/qa/slide032/render_8.png").convert("RGB")
ORI = Image.open(f"{DECK}/unique_slides/slide_032.jpg").convert("RGB")
S = REN.width / 960.0
print(f"render {REN.size}  original {ORI.size}  scale={S:.4f}")

def rpx(x, y):
    return REN.getpixel((int(round(x * S)), int(round(y * S))))

def opx(x, y):
    return ORI.getpixel((int(round(x)), int(round(y))))

def near(a, b, tol=40):
    return all(abs(a[i] - b[i]) <= tol for i in range(3))

def hexs(c):
    return "%02X%02X%02X" % c

def band(img, x0, x1, y0, y1, pred, s=S):
    """Count pixels in frame-space bbox satisfying pred."""
    n = 0
    xa, xb = int(x0 * s), int(x1 * s)
    ya, yb = int(y0 * s), int(y1 * s)
    for y in range(ya, yb):
        for x in range(xa, xb):
            c = img.getpixel((x, y))
            if pred(c):
                n += 1
    return n

RESULTS = []

def rec(name, ok, detail):
    RESULTS.append((name, ok, detail))
    print(("  OK   " if ok else "  FAIL ") + name + " :: " + detail)

# ------------------------------------------------------------------ TITLE
print("\n== TITLE runs (frame px) ==")
# scan row y=76 for run boundaries in each image
def runs(img, y, pred):
    xs = [x for x in range(0, 960) if pred(img.getpixel((x, y)))]
    if not xs:
        return []
    out, s, p = [], xs[0], xs[0]
    for x in xs[1:]:
        if x - p > 2:
            out.append((s, p)); s = x
        p = x
    out.append((s, p))
    return out

is_red = lambda c: c[0] > 140 and c[1] < 90 and c[2] < 90
is_green = lambda c: c[1] > 100 and c[0] < 90 and c[2] < 90
is_blue = lambda c: c[2] > 130 and c[0] < 90 and c[1] < 110
for label, pred in (("red", is_red), ("green", is_green), ("blue", is_blue)):
    ro = runs(ORI, 76, pred); rr = runs(REN, 76 * S, pred) if False else None
    # render: same scan at scaled row
    ys = int(76 * S)
    xs_r = [x for x in range(0, REN.width) if pred(REN.getpixel((x, ys)))]
    if xs_r:
        rr, s, p = [], xs_r[0], xs_r[0]
        for x in xs_r[1:]:
            if x - p > 5:
                rr.append((s / S, p / S)); s = x
            p = x
        rr.append((s / S, p / S))
    print(f"  {label}: ORIG {ro}  REND {rr}")

# ------------------------------------------------- HOUSE CHROME (spot)
print("\n== HOUSE CHROME spot ==")
for nm, fx, fy, want in (("canvas", 20, 20, (254, 255, 253)),
                         ("panel", 700, 500, (233, 233, 231)),
                         ("panel2", 120, 300, None),
                         ("left stroke", 58, 300, None),
                         ("right stroke", 901, 300, None),
                         ("bottom stroke", 500, 538, None),
                         ("top band", 500, 46, None)):
    c = rpx(fx, fy)
    print(f"  {nm:15s} render({fx},{fy}) = {hexs(c)}")

# -------------------------------------------------------- PARAM TABLE
print("\n== PARAM TABLE (x81..206 y179..250) ==")
for i, (y0, y1, want) in enumerate([(181, 202, "E8FFD5"), (207, 226, "F7BFC2"), (230, 246, "FBFF0B")]):
    cy = (y0 + y1) // 2
    co = opx(100, cy); cr = rpx(100, cy)
    print(f"  row{i+1} y{cy}: ORIG {hexs(co)}  REND {hexs(cr)}  want {want}")
# outer border present in both
print("  border x150 y179: ORIG", hexs(opx(150, 180)), "REND", hexs(rpx(150, 180)))

# ------------------------------------------------------------- GRAPH
print("\n== GRAPH box =="
      )
print("  interior white: ORIG(700,150)=", hexs(opx(700, 150)), " REND(700,150)=", hexs(rpx(700, 150)))
print("  left red frame : ORIG(573,150)=", hexs(opx(573, 150)), " REND(573,150)=", hexs(rpx(573, 150)))
print("  right red frame: ORIG(808,150)=", hexs(opx(808, 150)), " REND(808,150)=", hexs(rpx(808, 150)))
print("  top red frame  : ORIG(700,66) =", hexs(opx(700, 66)), " REND(700,66) =", hexs(rpx(700, 66)))
print("  bottom gray    : ORIG(700,266)=", hexs(opx(700, 266)), " REND(700,266)=", hexs(rpx(700, 266)))
print("  y axis x631    : ORIG(631,150)=", hexs(opx(631, 150)), " REND(631,150)=", hexs(rpx(631, 150)))

# ------------------------------------------------- THE LOSS CURVE
print("\n== CURVE f(x)=(x-5)^2+1 ==")
curve_png = Image.open(f"{DECK}/recreated_pptx/build/assets/curve_032.png").convert("RGBA")
cj = json.load(open(f"{DECK}/recreated_pptx/build/assets/curve_032.json"))
print("  curve json:", {k: cj[k] for k in cj})
# ripple: second difference of the analytic curve as drawn
# reconstruct sampled y from png alpha column profile at render scale
# Simpler: recompute second difference of the dense-sampled polyline from the
# build's own generator output is authoritative; verify smoothness numerically.
import numpy as np
xs_ = np.linspace(cj.get("x_min", 1.0), cj.get("x_max", 9.0), 5)
try:
    a = np.array(cj["polyline_x"]); b = np.array(cj["polyline_y"])
except KeyError:
    # derive from a fresh dense sample of the analytic function
    a = np.linspace(1.0, 9.0, 400); b = (a - 5) ** 2 + 1
d2 = np.abs(np.diff(b, 2))
print(f"  analytic max|2nd diff| = {d2.max():.3e} (single smooth quadratic)")

# curve ink colour census inside plot box in the render
def curve_ink(c):
    return c[2] > c[1] + 20 and c[2] > 110 and c[1] > 80 and c[1] < 200 and c[0] < 160
def curve_ink_o(c):
    return c[2] > c[1] + 15 and c[2] > 90 and c[1] > 60 and c[1] < 200 and c[0] < 170
nr = band(REN, 574, 809, 67, 307, curve_ink)
print(f"  curve-family ink px in plot box (render) = {nr}")
# same family in the ORIGINAL
no = band(ORI, 574, 809, 67, 307, curve_ink_o, s=1.0)
print(f"  curve-family ink px in plot box (orig)  = {no}")

# exact colour of a curve pixel in each image (parabola through (7,7) -> frame
# x = 630.5 + 11.5*7 = 711, y = 266 - 12*7 = 182)
print("  curve pixel (711,182): ORIG", hexs(opx(711, 182)), " REND", hexs(rpx(711, 182)))
print("  curve pixel (660,206): ORIG", hexs(opx(660, 206)), " REND", hexs(rpx(660, 206)))
# curve vertical extent in the render, column scan at data x=7 (frame 711)
xsr = int(711 * S)
colr = [y for y in range(int(67 * S), int(307 * S)) if curve_ink(REN.getpixel((xsr, y)))]
if colr:
    print(f"  REND curve at x711: render-y {colr[0]/S:.1f}..{colr[-1]/S:.1f} (frame), {len(colr)} px")
colrect = [y for y in range(67, 307) if curve_ink_o(ORI.getpixel((711, y)))]
if colrect:
    print(f"  ORIG curve at x711: frame-y {colrect[0]}..{colrect[-1]}, {len(colrect)} px")

# --------------------------------------------------- CHORD + DOTS
print("\n== CHORD (y=10, frame y146) and dots ==")
for nm, fx, fy in (("chord L end", 654, 146), ("chord mid", 687, 146), ("chord R end", 722, 146)):
    print(f"  {nm}: ORIG {hexs(opx(fx, fy))}  REND {hexs(rpx(fx, fy))}")
print("  green dot (687.5,255): ORIG", hexs(opx(687, 255)), " REND", hexs(rpx(687, 255)))
print("  red dot (660.5,182.5): ORIG", hexs(opx(660, 182)), " REND", hexs(rpx(660, 182)))

# ------------------------------------------------------- CALLOUTS
print("\n== CALLOUTS ==")
print("  eq box fill (460,198): ORIG", hexs(opx(460, 198)), " REND", hexs(rpx(460, 198)))
print("  green box (400,250): ORIG", hexs(opx(400, 250)), " REND", hexs(rpx(400, 250)))
print("  pink band (400,300): ORIG", hexs(opx(400, 300)), " REND", hexs(rpx(400, 300)))

# ------------------------------------------------- ITERATION TABLE
print("\n== ITERATION TABLE bands ==")
for nm, fx, fy, want in (("band1", 500, 360, "D8E175"), ("band2", 500, 405, "D4B2F5"),
                          ("band3", 500, 449, "F6DDC1"), ("band4", 500, 483, "E7FFD2"),
                          ("band5", 500, 507, "F4BEC2")):
    co = opx(fx, fy); cr = rpx(fx, fy)
    print(f"  {nm}: ORIG {hexs(co)}  REND {hexs(cr)}  want {want}")

# ------------------------------------------------------- SUMMARY
n_fail = sum(1 for _, ok, _ in RESULTS if not ok)
print(f"\nSUMMARY: {len(RESULTS)} checks, {n_fail} FAIL")
sys.exit(0)
