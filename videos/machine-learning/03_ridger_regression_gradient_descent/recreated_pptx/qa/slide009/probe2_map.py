#!/usr/bin/env python3
"""Probe 2: coarse spatial class map + refined region probes for slide_009."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# ---- class masks (order matters: first match wins) ----
yellow = (r > 235) & (g > 230) & (b < 200) & ((r - b) > 40)          # FDFD96 badge
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
blue = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
orange = (r > 200) & (g > 100) & (g < 210) & (b < 130) & ((r - g) > 40)
lightblue = (b > r + 12) & (b > 225) & (g > 215) & (g < 252) & (r > 200)  # E0F0FF
dark = (r < 95) & (g < 95) & (b < 95)
panel_gray = (abs(r - 233) < 10) & (abs(g - 231) < 12) & (abs(b - 230) < 14)
white = (r > 248) & (g > 248) & (b > 248)
chart_gray = (~panel_gray) & (~white) & (abs(r - g) < 14) & (abs(g - b) < 14) & \
             (r > 225) & (r < 252)

CLASSES = [
    ("Y", yellow), ("R", red), ("B", blue), ("O", orange),
    ("L", lightblue), ("K", dark), ("G", panel_gray),
    ("W", white), ("C", chart_gray),
]
lab = np.full((H, W), "?", dtype="<U1")
for name, m in CLASSES:
    lab[m & (lab == "?")] = name
lab[lab == "?"] = "."

print("=== class totals ===")
for name, m in CLASSES:
    print(f"  {name}: {int(m.sum())}")

# ---- coarse map: 10x10 px blocks ----
print("\n=== coarse map (10px blocks; 96 cols x 54 rows) ===")
print("    " + "".join(str((x // 10) % 10) for x in range(0, W, 10)))
for y0 in range(0, H, 10):
    row = ""
    for x0 in range(0, W, 10):
        blk = lab[y0:y0 + 10, x0:x0 + 10]
        vals, cnts = np.unique(blk, return_counts=True)
        dom = vals[cnts.argmax()]
        frac = cnts.max() / blk.size
        row += dom if frac > 0.45 else (dom.lower() if frac > 0.18 else " ")
    print(f"{y0:4d}{row}")

# ---- refined: chart panel fill regions ----
print("\n=== CHART-GRAY (C) extent ===")
pys, pxs = np.where(chart_gray)
print(f"  chart_gray bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")
for nm, c0, c1 in (("LEFT", 40, 470), ("RIGHT", 470, 910)):
    sub = chart_gray[:, c0:c1]
    rows = np.where(sub.mean(axis=1) > 0.4)[0]
    cols = np.where(sub.mean(axis=0) > 0.4)[0] + c0
    def runs(idx):
        if not len(idx):
            return []
        idx = [int(v) for v in idx]
        out, s, p = [], idx[0], idx[0]
        for v in idx[1:]:
            if v <= p + 2:
                p = v
                continue
            out.append((s, p))
            s = p = v
        out.append((s, p))
        return out
    print(f"  {nm} rows (>40%): {runs(rows)}")
    print(f"  {nm} cols (>40%): {runs(cols)}")

# ---- lightblue annotation boxes, tight ----
print("\n=== LIGHTBLUE annotation boxes ===")
pys, pxs = np.where(lightblue)
print(f"  lightblue total {len(pys)} bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")
# column-histogram of lightblue to separate the two boxes
lc = lightblue.sum(axis=0)
print("  lightblue cols >5:", np.where(lc > 5)[0][[0, -1]] if (lc > 5).any() else None)
# split at x=470
for nm, c0, c1 in (("LEFT", 0, 470), ("RIGHT", 470, W)):
    sub = lightblue[:, c0:c1]
    if not sub.any():
        print(f"  {nm}: none")
        continue
    ys, xs = np.where(sub)
    print(f"  {nm}: bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()} n={sub.sum()}")
    # row histogram
    rh = sub.sum(axis=1)
    rr = np.where(rh > 3)[0]
    print(f"     rows>3px: {rr.min()}..{rr.max()}  peaks "
          f"{[(int(v), int(rh[v])) for v in np.argsort(rh)[-6:]]}")

# ---- RED element breakdown ----
print("\n=== RED element breakdown ===")
# vertical red strokes (tall columns)
rc = red.sum(axis=0)
print("  red col counts (cols>25):")
for x in range(W):
    if rc[x] > 25:
        print(f"    x={x} count={rc[x]}")
rr = red.sum(axis=1)
print("  red row counts (rows>25):")
for y in range(H):
    if rr[y] > 25:
        print(f"    y={y} count={rr[y]}")

# red inside left panel only vs right panel
for nm, c0, c1 in (("LEFT", 54, 460), ("RIGHT", 460, 903)):
    sub = red[:, c0:c1]
    print(f"  {nm} red total {int(sub.sum())}")
    ys, xs = np.where(sub)
    if len(ys):
        print(f"    bbox x {xs.min()+c0}..{xs.max()+c0} y {ys.min()}..{ys.max()}")
    rr2 = sub.sum(axis=1)
    print(f"    rows>40: {[(y, int(rr2[y])) for y in range(H) if rr2[y] > 40]}")

# ---- BLUE fitted line: per-panel line trace ----
print("\n=== BLUE fitted line trace (per column, topmost blue in panel body) ===")
for nm, c0, c1 in (("LEFT", 60, 450), ("RIGHT", 490, 900)):
    print(f"  {nm}:")
    for x in range(c0, c1, 20):
        ys = np.where(blue[:, x])[0]
        if len(ys):
            print(f"    x={x:4d} ymin={ys.min()} ymax={ys.max()} n={len(ys)}")

# ---- ORANGE points full list with size ----
print("\n=== ORANGE blobs (>=8 px) ===")
from scipy import ndimage
lab_o, n = ndimage.label(orange)
sizes = ndimage.sum(orange, lab_o, range(1, n + 1))
objs = ndimage.find_objects(lab_o)
cents = ndimage.center_of_mass(orange, lab_o, range(1, n + 1))
left, right = [], []
for sl, sz, cm in zip(objs, sizes, cents):
    if sz >= 8:
        rec = (round(cm[1], 1), round(cm[0], 1), int(sz),
               sl[1].start, sl[1].stop - 1, sl[0].start, sl[0].stop - 1)
        (left if cm[1] < 470 else right).append(rec)
print(f"  LEFT ({len(left)}):")
for v in sorted(left, key=lambda t: t[0]):
    print(f"    cx={v[0]:6.1f} cy={v[1]:6.1f} n={v[2]:4d} bbox x{v[3]}..{v[4]} y{v[5]}..{v[6]}")
print(f"  RIGHT ({len(right)}):")
for v in sorted(right, key=lambda t: t[0]):
    print(f"    cx={v[0]:6.1f} cy={v[1]:6.1f} n={v[2]:4d} bbox x{v[3]}..{v[4]} y{v[5]}..{v[6]}")

# ---- DARK text regions ----
print("\n=== DARK text clusters ===")
lab_d, nd = ndimage.label(dark, structure=np.ones((3, 3)))
for i in range(1, nd + 1):
    m = lab_d == i
    if m.sum() < 8:
        continue
    ys, xs = np.where(m)
    print(f"  cluster{i}: n={int(m.sum())} x {xs.min()}..{xs.max()} "
          f"y {ys.min()}..{ys.max()}")
