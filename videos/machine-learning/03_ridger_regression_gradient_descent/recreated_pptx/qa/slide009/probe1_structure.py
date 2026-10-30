#!/usr/bin/env python3
"""Probe 1 for slide_009 structural measurement.

Re-derive every geometry fact from unique_slides/slide_009.jpg (960x540, 1px=1pt).
Do NOT trust the dead worker's measurements.txt blindly - verify each claim.
"""
import sys
import numpy as np
from PIL import Image
from collections import Counter

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")

im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
print(f"frame {W}x{H}")

r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# ---------- 1. background / panel census ----------
print("\n=== TOP-40 most common exact colors ===")
flat = a.reshape(-1, 3)
cnt = Counter(map(tuple, flat[::3]))  # sample every 3rd px for speed
for c, n in cnt.most_common(40):
    print(f"  {c}  #{c[0]:02X}{c[1]:02X}{c[2]:02X}  n={n*3}")

# ---------- 2. panel: near-F5F5F5 fill ----------
print("\n=== PANEL fill scan (#F5F5F5 family) ===")
for name, tol in (("strict10", 10), ("loose25", 25)):
    mask = (abs(r - 245) < tol) & (abs(g - 245) < tol) & (abs(b - 245) < tol)
    colcnt = mask.sum(axis=0)
    rowcnt = mask.sum(axis=1)
    # column runs where >55% of rows are panel-colored
    cols = np.where(colcnt > H * 0.55)[0]
    rows = np.where(rowcnt > W * 0.25)[0]
    def runs(idx):
        if not len(idx):
            return []
        out, s, p = [], idx[0], idx[0]
        for v in idx[1:]:
            if v == p + 1:
                p = v
                continue
            out.append((int(s), int(p)))
            s = p = v
        out.append((int(s), int(p)))
        return out
    print(f"  {name}: panelish col runs {runs(cols)}")
    print(f"  {name}: panelish row runs {runs(rows)}")

# explicit: fraction of panel-ish px per column, to find left/right panel edges
tol = 12
mask = (abs(r - 245) < tol) & (abs(g - 245) < tol) & (abs(b - 245) < tol)
colfrac = mask.mean(axis=0)
print("\n  colfrac>0.5 columns:", np.where(colfrac > 0.5)[0][[0, -1]],
      "count", int((colfrac > 0.5).sum()))
print("  colfrac>0.2 columns:", np.where(colfrac > 0.2)[0][[0, -1]],
      "count", int((colfrac > 0.2).sum()))
print("  rowfrac>0.5 rows:", np.where(mask.mean(axis=1) > 0.5)[0][[0, -1]])
print("  rowfrac>0.3 rows:", np.where(mask.mean(axis=1) > 0.3)[0][[0, -1]])

# ---------- 3. gray panel E9E9E7 (house chrome) ----------
print("\n=== HOUSE gray panel E9E9E7 (233) ===")
gray = (abs(r - 233) < 12) & (abs(g - 233) < 12) & (abs(b - 230) < 14)
gf = gray.mean(axis=0)
print("  gray colfrac>0.5:", np.where(gf > 0.5)[0][[0, -1]],
      "count", int((gf > 0.5).sum()))
# where does gray appear outside the panel? left/right margins
print("  gray colfrac (x<54):", gf[:54].max(), "at", int(gf[:54].argmax()))
print("  gray colfrac (x>903):", gf[904:].max(), "at", 904 + int(gf[904:].argmax()))
grows = gray.mean(axis=1)
print("  gray rowfrac>0.5 rows:", np.where(grows > 0.5)[0][[0, -1]])

# ---------- 4. RED ink (all) ----------
print("\n=== RED ink ===")
red = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
print("  total red px:", int(red.sum()))
# column profile: red count per column
rc = red.sum(axis=0)
strong = np.where(rc > 30)[0]
def runs_idx(idx):
    if not len(idx):
        return []
    out, s, p = [], int(idx[0]), int(idx[0])
    for v in idx[1:]:
        v = int(v)
        if v == p + 1:
            p = v
            continue
        out.append((s, p))
        s = p = v
    out.append((s, p))
    return out
print("  red cols count>30:", runs_idx(strong))
rr = red.sum(axis=1)
print("  red rows count>30:", runs_idx(np.where(rr > 30)[0]))
print("  red rows count>100:", runs_idx(np.where(rr > 100)[0]))

# top band check (house: no top stroke)
top = red[:40, :]
print("  red px rows 0..39:", int(top.sum()))
print("  red px rows 0..45:", int(red[:46, :].sum()))

# bottom stroke
print("  red px rows 533..539:", int(red[533:, :].sum()),
      "cols", runs_idx(np.where(red[533:, :].sum(axis=0) > 0)[0]))
print("  red px rows 536..539:", int(red[536:, :].sum()))

# ---------- 5. BLUE ink ----------
print("\n=== BLUE ink ===")
blue = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
print("  total blue px:", int(blue.sum()))
pys, pxs = np.where(blue)
if len(pys):
    print(f"  blue bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")
# per column blue centroid
for x in range(60, 910, 25):
    ys = np.where(blue[:, x])[0]
    if len(ys):
        print(f"    x={x:4d} blue y {ys.min()}..{ys.max()} n={len(ys)} "
              f"centroid {ys.mean():.1f}")

# ---------- 6. ORANGE ink ----------
print("\n=== ORANGE ink ===")
orange = (r > 200) & (g > 100) & (g < 210) & (b < 130) & ((r - g) > 40)
print("  total orange px:", int(orange.sum()))
pys, pxs = np.where(orange)
if len(pys):
    print(f"  orange bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")

# connected components via simple flood-free labeling (scipy may exist)
try:
    from scipy import ndimage
    lab, n = ndimage.label(orange)
    print(f"  scipy orange components: {n}")
    objs = ndimage.find_objects(lab)
    sizes = ndimage.sum(orange, lab, range(1, n + 1))
    cents = ndimage.center_of_mass(orange, lab, range(1, n + 1))
    for i, (sl, sz, cm) in enumerate(zip(objs, sizes, cents), 1):
        if sz >= 6:
            print(f"    blob{i}: bbox y{sl[0].start}..{sl[0].stop-1} "
                  f"x{sl[1].start}..{sl[1].stop-1} n={int(sz)} "
                  f"centroid=({cm[1]:.1f},{cm[0]:.1f})")
except ImportError:
    print("  (no scipy)")

# ---------- 7. LIGHT BLUE annotation box ----------
print("\n=== LIGHT-BLUE annotation box (E0F0FF family) ===")
lb = (b > 235) & (b > r + 8) & (g > 225) & (g < 250) & (r > 215)
print("  total lightblue px:", int(lb.sum()))
pys, pxs = np.where(lb)
if len(pys):
    print(f"  lightblue bbox x {pxs.min()}..{pxs.max()} y {pys.min()}..{pys.max()}")
print("  lightblue colfrac>0.3:", runs_idx(np.where(lb.mean(axis=0) > 0.3)[0]))
print("  lightblue rowfrac>0.3:", runs_idx(np.where(lb.mean(axis=1) > 0.3)[0]))

# ---------- 8. DARK (near-black) ink ----------
print("\n=== DARK ink (text: black labels + badge numeral) ===")
dark = (r < 90) & (g < 90) & (b < 90)
print("  total dark px:", int(dark.sum()))
print("  dark rowfrac>1:", runs_idx(np.where(dark.mean(axis=1) > 0.01)[0]))
print("  dark colfrac>0.5:", runs_idx(np.where(dark.mean(axis=0) > 0.005)[0]))

# ---------- 9. GRID lines (#CCCCCC family) inside panels ----------
print("\n=== GRID lines (near-CCC / between F5F5F5 and gray) ===")
grid = (abs(r - 204) < 26) & (abs(g - 204) < 26) & (abs(b - 204) < 26) & \
       (abs(r - g) < 12) & (abs(g - b) < 12)
print("  total grid px:", int(grid.sum()))
# restrict to left panel columns
for nm, c0, c1 in (("LEFT", 53, 449), ("RIGHT", 484, 908)):
    sub = grid[:, c0:c1]
    rows = np.where(sub.sum(axis=1) > (c1 - c0) * 0.25)[0]
    cols = np.where(sub.sum(axis=0) > 100)[0] + c0
    print(f"  {nm}: grid-heavy rows {runs_idx(rows)}")
    print(f"  {nm}: grid-heavy cols {runs_idx(cols)}")
