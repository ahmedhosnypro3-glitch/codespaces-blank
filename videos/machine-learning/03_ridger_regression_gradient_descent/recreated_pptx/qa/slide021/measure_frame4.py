#!/usr/bin/env python3
"""measure_frame4.py — pixel-precise per-element geometry of slide_021.jpg.

Elements: panel outline edges; title; labels (red/blue/green parts); table
gridlines (long horizontal/vertical dark runs); digit glyph bands; chain text
bands with per-cluster color cores; arrows.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
yellow = (r > 180) & (g > 180) & (b < 140)
dark = (r < 110) & (g < 110) & (b < 110) & ~blue & ~red
ink = dark | blue | red | green | yellow

def runs(vec):
    """yield (start, end) inclusive runs of True in vec"""
    out = []
    s = None
    for i, v in enumerate(vec):
        if v and s is None:
            s = i
        elif not v and s is not None:
            out.append((s, i - 1)); s = None
    if s is not None:
        out.append((s, len(vec) - 1))
    return out

def color_core(y0, y1, x0, x1, mask):
    ys, xs = np.where(mask[y0:y1 + 1, x0:x1 + 1])
    if not len(ys):
        return None
    pts = a[ys + y0, xs + x0]
    # darkest-core: the most saturated pixels of the mask
    if mask is blue or True:
        med = np.median(pts, axis=0)
    return (int(med[0]), int(med[1]), int(med[2])), len(ys)

print("=== 1. PANEL OUTLINE EDGES (blue mask) ===")
# panel row bands (from outline top/bottom): scan col x=480 for vertical blue runs
for xprobe in (480, 200, 700):
    rr = runs(blue[:, xprobe])
    print(f" col x={xprobe}: blue row runs: {rr}")
# scan row y=200 for horizontal blue runs
for yprobe in (192, 350, 480):
    rr = runs(blue[yprobe, :])
    print(f" row y={yprobe}: blue col runs: {rr}")

print("\n=== 2. TITLE ===")
tm = red.copy()
tm[100:, :] = False  # title band only (y<100)
ys, xs = np.where(tm)
print(f" red title bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")
pts = a[ys, xs]
dk = pts[pts[:, 0].argsort()][:30]
print(f" darkest red core px: {tuple(dk[0])}")
# per-row ink to find glyph band edges
for y in range(70, 105):
    n = tm[y].sum()
    if n:
        xs2 = np.where(tm[y])[0]
        print(f"   y={y}: n={n} x {xs2.min()}..{xs2.max()}")

print("\n=== 3. TOP PANEL (y128..257) ===")
# label
m = red[128:170, 60:400]
ys, xs = np.where(m)
if len(ys):
    print(f" label red bbox: x {xs.min()+60}..{xs.max()+60} y {ys.min()+128}..{ys.max()+128}")
    pts = a[ys+128, xs+60]; med = np.median(pts, axis=0)
    print(f"   color median: ({med[0]},{med[1]},{med[2]})")
# table region: horizontal gridlines (dark runs >= 80px) between y150..250, x60..400
print(" top-panel horizontal dark runs (>=60px):")
for y in range(150, 258):
    rr = runs(dark[y, 60:400])
    long_rr = [(s+60, e+60) for s, e in rr if e - s >= 60]
    if long_rr:
        print(f"   y={y}: {long_rr}")
print(" top-panel vertical dark runs (>=15px):")
for x in range(60, 400):
    rr = runs(dark[150:258, x])
    long_rr = [(s+150, e+150) for s, e in rr if e - s >= 15]
    if long_rr:
        print(f"   x={x}: {long_rr}")
# digits: dark ink clusters in table region x60..320, y150..250
print(" top-panel table digit bands (dark, x 60..330):")
dig = dark[150:258, 60:330]
rowink = dig.any(axis=1)
rb = runs(rowink)
for (y0, y1) in rb:
    sub = dig[y0:y1+1]
    xs3 = np.where(sub.any(axis=0))[0]
    # cluster by gaps>6
    ccl = []
    s = xs3[0]; p = xs3[0]
    for x in xs3[1:]:
        if x - p > 6:
            ccl.append((s+60, p+60)); s = x
        p = x
    ccl.append((s+60, p+60))
    print(f"   y {y0+150}..{y1+150}: x clusters {ccl}")

print("\n=== 4. TOP PANEL CHAIN (right side, x330..900, y170..230) ===")
# per-cluster decomposition on mixed ink
chain = ink[170:235, 330:900]
ys, xs = np.where(chain)
# row bands
rowink = chain.any(axis=1)
rb = runs(rowink)
for (y0, y1) in rb:
    sub = chain[y0:y1+1]
    xs3 = np.where(sub.any(axis=0))[0]
    ccl = []
    s = xs3[0]; p = xs3[0]
    for x in xs3[1:]:
        if x - p > 8:
            ccl.append((s+330, p+330)); s = x
        p = x
    ccl.append((s+330, p+330))
    print(f" chain band y {y0+170}..{y1+170}:")
    for (cx0, cx1) in ccl:
        # color composition of the cluster
        sub2 = ink[y0+170:y1+170, cx0:cx1+1]
        nd = int((dark[y0+170:y1+170, cx0:cx1+1] & sub2).sum())
        nb = int(blue[y0+170:y1+170, cx0:cx1+1].sum())
        nr = int(red[y0+170:y1+170, cx0:cx1+1].sum())
        # core colors: darkest px of each class
        info = []
        for cls_name, cls in (("dark", dark), ("blue", blue), ("red", red)):
            if cls is dark:
                mm = cls[y0+170:y1+170, cx0:cx1+1]
            else:
                mm = cls[y0+170:y1+170, cx0:cx1+1]
            if mm.sum() >= 3:
                cys, cxs = np.where(mm)
                cpts = a[cys+y0+170, cxs+cx0]
                # take the 10 most extreme (min sum for dark, max channel for colors)
                if cls_name == "dark":
                    srt = cpts[cpts.sum(axis=1).argsort()][:8]
                elif cls_name == "blue":
                    srt = cpts[cpts[:, 2].argsort()][::-1][:8]
                else:
                    srt = cpts[cpts[:, 0].argsort()][::-1][:8]
                med = np.median(srt, axis=0)
                info.append(f"{cls_name}({mm.sum()}) core({int(med[0])},{int(med[1])},{int(med[2])})")
        print(f"   x {cx0}..{cx1} (w {cx1-cx0}): {' '.join(info)}")
