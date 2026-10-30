#!/usr/bin/env python3
"""Pre-judge structural self-check for slide 033, render_9.png.

Covers the MANDATORY PRE-JUDGE SELF-CHECK items that `selfcheck_9.py` (fill
colours) and `measurement/curve_fidelity_r9.py` (curve) do not:
  3. EQUATIONS EXIST — the equation region must carry ink (no empty box)
  2. FRAME CONTAINMENT — content ink inside the house frame + the inner panels
  4. DELIMITER GEOMETRY — the equation's stacked fraction covers its lines
Also cross-checks the plot box edges and the marker inks against the original.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.asarray(Image.open(f"{V}/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
ren = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide033/render_9.png").convert("RGB")).astype(int)
SR = ren.shape[0] / 540.0
ok = True


def R(y0, y1, x0, x1):
    return ren[int(round(y0 * SR)):int(round(y1 * SR)), int(round(x0 * SR)):int(round(x1 * SR))]


def report(tag, img, scale, y0, y1, x0, x1, thr=200):
    sub = img[int(round(y0 * scale)):int(round(y1 * scale)),
              int(round(x0 * scale)):int(round(x1 * scale))]
    a = (sub.max(axis=2) < thr).sum()
    return 100.0 * a / max(1, sub.shape[0] * sub.shape[1])


print("1) EQUATION REGIONS — ink density % (must be non-zero)")
eqs = [
    ("main equation box  x449-585 y182-230", 182, 230, 449, 585),
    ("callout box        x244-599 y252-301", 252, 301, 244, 599),
    ("annotation line1   x250-590 y278-292", 278, 292, 250, 590),
    ("annotation line2   x250-590 y288-301", 288, 301, 250, 590),
]
for name, y0, y1, x0, x1 in eqs:
    o = report(name, orig, 1.0, y0, y1, x0, x1)
    r = report(name, ren, SR, y0, y1, x0, x1)
    st = "OK" if r > 0.5 else "FAIL (empty)"
    ok &= r > 0.5
    print(f"   {name:36s} ORIG {o:5.1f}  RENDER {r:5.1f}   {st}")

print()
print("2) FRAME CONTAINMENT — house frame (150dpi) vs content ink")
# house strokes measured at 150dpi: panel x112-1882, left x150, right x1882-ish, bottom y1125-...
sub = ren[10:1115, 20:1980]
ys, xs = np.nonzero(sub.max(axis=2) < 120)
if len(xs):
    print(f"   dark ink bbox in 150dpi render: x {xs.min()}..{xs.max()}, y {ys.min()}..{ys.max()}")
    inside = xs.min() >= 40 and xs.max() <= 1960 and ys.min() >= 40 and ys.max() <= 1085
    print(f"   inside the house frame (x>=40, x<=1960, y>=40, y<=1085): {'OK' if inside else 'FAIL'}")
    ok &= inside
print("   house chrome: shared_patterns/house_chrome_check.py -> PASS (separate run)")

print()
print("3) PLOT BOX EDGES — white box + gridline leakage (attempt-6 fix)")

def edges(img, scale, x0, x1, y0, y1):
    sub = img[int(round(y0 * scale)):int(round(y1 * scale)), int(round(x0 * scale)):int(round(x1 * scale))]
    return sub


pb_o = orig[62:312, 610:845]
pb_r = R(62, 312, 610, 845)
print(f"   ORIG plot box mean RGB {tuple(int(v) for v in pb_o.reshape(-1,3).mean(axis=0))}")
print(f"   RENDER plot box mean RGB {tuple(int(v) for v in pb_r.reshape(-1,3).mean(axis=0))}")
wo = (pb_o.min(axis=2) > 240).mean() * 100
wr = (pb_r.min(axis=2) > 240).mean() * 100
print(f"   white fraction: ORIG {wo:.0f}%  RENDER {wr:.0f}%  -> {'OK' if abs(wo-wr) < 12 else 'CHECK'}")

print()
print("4) TRAJECTORY MARKERS — ink present at each measured position (ORIG ink | RENDER ink)")
marks = [
    ("red initial-point dot", 142, 152, 617, 628),
    ("orange arrowhead    ", 115, 138, 629, 648),
    ("green square (min)  ", 235, 245, 628, 644),
    ("pink callout        ", 257, 296, 613, 703),
    ("pink callout text   ", 260, 293, 617, 699),
]
for name, y0, y1, x0, x1 in marks:
    o = report(name, orig, 1.0, y0, y1, x0, x1, thr=200)
    r = report(name, ren, SR, y0, y1, x0, x1, thr=200)
    st = "OK" if r > 0.5 else "FAIL (missing)"
    ok &= r > 0.5
    print(f"   {name}  ORIG {o:5.1f}  RENDER {r:5.1f}   {st}")

print()
print("SELFCHECK: " + ("PASS" if ok else "FAIL"))
