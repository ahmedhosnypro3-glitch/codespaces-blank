#!/usr/bin/env python3
"""Slide 030 parabola containment + shape check (w030-finish).

Build law: the convex cost curve must be ONE smooth parabolic arc, fully INSIDE
its plot frame. Checks:
  1. render parabola ink extent vs plot frame (x572..810, y65..311)
  2. one-arc smoothness (second difference of a densely sampled centreline)
  3. vertex position vs analytic f(x)=(x-5)^2+1 mapped through the build scale
  4. the ORIGINAL's parabola ink extent for comparison
"""
import numpy as np
from PIL import Image

V = "videos/machine-learning/03_ridger_regression_gradient_descent"
rend = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide030/render_6.png").convert("RGB")).astype(int)
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_030.jpg").convert("RGB")).astype(int)
H, W = rend.shape[:2]
SX, SY = W / 960.0, H / 540.0
print(f"render {W}x{H} SX={SX:.4f} SY={SY:.4f}")

# build constants (from build/slide_030.js)
BX0, BX1, BY0, BY1 = 572, 810, 65, 311
X0, Y0, UX, UY = 630.5, 266.5, 11.45, 12.0

# ---------------- render: parabola blue ink, full plot height
rr, gg, bb = rend[:, :, 0], rend[:, :, 1], rend[:, :, 2]
blue = (bb - rr > 25) & (bb - gg > 8) & (bb > 90)
# restrict x to inside the plot span so only the curve counts
blue[:, :int(560 * SX)] = False
blue[:, int(820 * SX):] = False
blue[:int(40 * SY), :] = False     # above the title band
blue[int(330 * SY):, :] = False    # below the plot
ys, xs = np.where(blue)
fx = xs / SX
fy = ys / SY
print(f"\n== render parabola ink ==  n={len(xs)}  x {fx.min():.1f}..{fx.max():.1f}  y {fy.min():.1f}..{fy.max():.1f}")
print(f"  plot frame: x {BX0}..{BX1}  y {BY0}..{BY1}")
above = blue[int(40 * SY):int(BY0 * SY), :].sum()
below = blue[int(BY1 * SY):int(330 * SY), :].sum()
outside_x = blue[:, int(560*SX):int(BX0*SX)].sum() + blue[:, int(BX1*SX):int(820*SX)].sum()
print(f"  ink OUTSIDE plot frame: above-top={above}  below-bottom={below}  outside-left/right={outside_x}")

# centreline: per-column median y, columns with >=2 ink px
cols = {}
for x, y in zip(np.round(fx, 1), fy):
    cols.setdefault(x, []).append(y)
cx = np.array(sorted(cols))
cy = np.array([np.median(cols[k]) for k in cx])
cy = cy[np.isfinite(cy)]
keep = np.array([len(cols[k]) >= 2 for k in cx])
cx, cy = cx[keep], cy[keep]
print(f"  centreline: {len(cx)} cols, x {cx.min():.1f}..{cx.max():.1f}")

# vertex: analytic x=5 -> XS(5)=687.7 ; y at vertex -> YS(1)=254.5
print(f"  analytic vertex px: x={X0 + 5*UX:.1f} y={Y0 - 1*UY:.1f}")
vcol = cx[np.argmin(cy)]
vrow = cy.min()
print(f"  measured vertex: x={vcol:.1f} y={vrow:.1f}  (delta {vcol-(X0+5*UX):+.1f}, {vrow-(Y0-1*UY):+.1f})")

# smoothness on the well-populated middle band (y within plot, arms not clipped)
mid = (cy > BY0 + 2) & (cy < BY1 - 2)
mx, my = cx[mid], cy[mid]
if len(mx) > 10:
    d1 = np.diff(my) / np.diff(mx)
    d2 = np.diff(d1) / np.diff(mx)[1:]
    print(f"  smoothness band x {mx.min():.1f}..{mx.max():.1f} ({len(mx)} cols): "
          f"max|d2|={np.abs(d2).max():.3f} mean|d2|={np.abs(d2).mean():.3f}")
    # theoretical: y = A(x-xv)^2 + c with A = UY/UX^2 px per frame px^2
    A = UY / UX**2
    print(f"  theoretical d2 for a parabola: {2*A:.3f} px/px^2 (a single arc tracks ~2A)")
    # ripple magnitude in frame px
    print(f"  ripple in frame px: max {np.abs(d2).max()*SX*SX:.3f}  mean {np.abs(d2).mean()*SX*SX:.3f}")

# arm symmetry: slope magnitude at +-3 units from vertex
for dv in (2.0, 3.0, 4.0):
    xt = X0 + (5 + dv) * UX
    xl = X0 + (5 - dv) * UX
    sel_r = np.argmin(np.abs(mx - xt))
    sel_l = np.argmin(np.abs(mx - xl))
    if len(mx) > max(sel_r, sel_l):
        sr = (my[sel_r] - vrow) / (mx[sel_r] - vcol)
        sl = (my[sel_l] - vrow) / (mx[sel_l] - vcol)
        print(f"  |x-5|={dv}: arm slopes {sl:+.3f} / {sr:+.3f} (should mirror)")

# ---------------- original: blue-ish parabola
o_r, o_g, o_b = orig[:, :, 0], orig[:, :, 1], orig[:, :, 2]
# JPEG-soft: canalise a wide blue band, then keep the curve-like pixels
ob = (o_b - o_r > 8) & (o_b - o_g > 4) & (o_b > 70)
ob[:40, :] = False
ob[330:, :] = False
ob[:, :560] = False
ob[:, 820:] = False
ys2, xs2 = np.where(ob)
if len(xs2):
    print(f"\n== orig parabola ink == n={len(xs2)} x {xs2.min()}..{xs2.max()} y {ys2.min()}..{ys2.max()}")
    print(f"  (orig plot frame measured x572..810 y65..311)")
    print(f"  orig ink outside frame: above-top={ob[40:65,:].sum()} below-bottom={ob[311:330,:].sum()}")
else:
    print("\n== orig parabola ink == none with this classifier (JPEG wash)")

# original: where is the ORIGINAL's parabola vertex? scan the blue band columns
if len(xs2):
    colsy = {}
    for x, y in zip(xs2, ys2):
        colsy.setdefault(x, []).append(y)
    ocx = np.array(sorted(colsy))
    ocy = np.array([np.min(colsy[k]) for k in ocx])
    ovi = np.argmin(ocy)
    print(f"  orig vertex-ish x={ocx[ovi]} y={ocy[ovi]}")
print("\nPARABOLA CHECK DONE")
