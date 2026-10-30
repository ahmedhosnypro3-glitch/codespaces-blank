#!/usr/bin/env python3
"""slide_007 — least-squares line fits for the pure-color decision boundaries + axes."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

pure_red   = (R>170)&(G<95)&(B<95)
pure_green = (G>105)&(R<95)&(B<95)
pure_blue  = (B>165)&(R<95)&(G<105)

def fit(name, pts, ybounds):
    """pts: list of (x,y). fit y = m*x + c, report endpoints at given y."""
    p = np.array(pts, dtype=float)
    A = np.vstack([p[:,0], np.ones(len(p))]).T
    m, c = np.linalg.lstsq(A, p[:,1], rcond=None)[0]
    print(f"\n=== {name}: n={len(pts)} y = {m:.4f}x + {c:.1f} ===")
    res = p[:,1] - (m*p[:,0] + c)
    print(f"  residual max abs = {np.abs(res).max():.2f}  rms={np.sqrt((res**2).mean()):.2f}")
    for y in ybounds:
        x = (y - c) / m
        print(f"  at y={y}: x={x:.1f}")
    for x in ybounds:
        y = m*x + c
        print(f"  at x={x}: y={y:.1f}")
    return m, c

# ---- BLUE d3: isolating the diagonal strand ----
blue_pts = []
for r in range(130, 490):
    xs = np.where(pure_blue[r, 160:800])[0] + 160
    # keep only runs that look like a thin strand (width<=3) and are NOT the dotted/label region
    if len(xs) == 0: continue
    runs = []; s = xs[0]; p = xs[0]
    for x in xs[1:]:
        if x-p > 4: runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    for (s0, e0) in runs:
        w = e0 - s0 + 1
        if w <= 4 and not (490 < e0 < 700 and 340 < r < 420):
            blue_pts.append(((s0+e0)/2, r))

# red AXIS (vertical, x~310) and red d1 (descending) - split by row
red_axis = [(310, r) for r in range(125, 500) if pure_red[r, 305:316].any()]
red_d1 = []
for r in range(130, 500):
    xs = np.where(pure_red[r, 160:800])[0] + 160
    if len(xs) == 0: continue
    runs = []; s = xs[0]; p = xs[0]
    for x in xs[1:]:
        if x-p > 4: runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    for (s0, e0) in runs:
        w = e0 - s0 + 1
        if w <= 6 and not (300 < s0 < 320) and not (520 < s0 < 700 and 330 < r < 400):
            red_d1.append(((s0+e0)/2, r))

# ---- green d2 ----
green_pts = []
for r in range(155, 390):
    xs = np.where(pure_green[r, 160:800])[0] + 160
    if len(xs) == 0: continue
    runs = []; s = xs[0]; p = xs[0]
    for x in xs[1:]:
        if x-p > 4: runs.append((s, p)); s = x
        p = x
    runs.append((s, p))
    for (s0, e0) in runs:
        w = e0 - s0 + 1
        if w <= 6 and not (440 < s0 < 560 and 160 < r < 290):
            green_pts.append(((s0+e0)/2, r))

print("BLUE pts:", len(blue_pts), "GREEN pts:", len(green_pts), "REDd1 pts:", len(red_d1))
fit("blue d3 diagonal", blue_pts, [140, 200, 300, 400, 480])
fit("green d2 diagonal", green_pts, [160, 220, 280, 340, 380])
fit("red d1 diagonal", red_d1, [150, 250, 350, 450, 490])

# ---- intersections ----
def inter(m1, c1, m2, c2):
    x = (c2 - c1) / (m1 - m2); return x, m1*x + c1

m3, c3 = fit("blue", blue_pts, [])[0:2] if False else fit("blue", blue_pts, [140])
m2, c2 = fit("green", green_pts, [160])
m1, c1 = fit("red", red_d1, [150])
print("\n=== intersections ===")
for (n1, x1, m, c, n2) in []:
    pass
# d1 vs d3
print("d1 x d3:", inter(m1, c1, m3, c3))
print("d1 x d2:", inter(m1, c1, m2, c2))
print("d2 x d3:", inter(m2, c2, m3, c3))
