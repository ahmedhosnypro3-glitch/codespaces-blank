#!/usr/bin/env python3
"""Precise pixel geometry of slide_021.jpg: graph boxes (white), formula boxes (pink), badge, frame."""
from PIL import Image
import numpy as np

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
PPI = W / 13.3333
print(f"size {W}x{H}  px/in={PPI:.4f}")
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

def to_in(x, y=None):
    if y is None:
        return f"{x/PPI:.3f}in"
    return f"({x/PPI:.3f},{y/PPI:.3f})"

# ---------- frame: red thin rectangle ----------
redm = (R > 140) & (G < 110) & (B < 110)
# find long horizontal red runs (frame top/bottom) and vertical (left/right)
print("\n=== RED FRAME ===")
for name, axis in [("rows", 1), ("cols", 0)]:
    n = redm.shape[0] if axis == 1 else redm.shape[1]
    best = None
    for i in range(n):
        line = redm[i] if axis == 1 else redm[:, i]
        idx = np.where(line)[0]
        if len(idx) > 100:
            if best is None or len(idx) > len(best[3]):
                best = (i, idx.min(), idx.max(), idx)
    print(f"best {name}: idx {best[0]} span {best[1]}..{best[2]} len {len(best[3])}")

# ---------- white graph panels (the 4 chart areas) ----------
print("\n=== WHITE GRAPH PANELS (connected components) ===")
whitem = (R > 245) & (G > 245) & (B > 245)
# remove top banner zone (y<48) and black bar (y>510)
whitem[:50] = False
whitem[512:] = False
from scipy import ndimage
try:
    lab, nlab = ndimage.label(whitem)
    comps = []
    for i in range(1, nlab + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 5000:
            continue
        comps.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    comps.sort(key=lambda c: (c[1], c[0]))
    for c in comps:
        x0, y0, x1, y1, n = c
        print(f"  panel x {x0}..{x1} y {y0}..{y1} -> in x {x0/PPI:.3f}..{x1/PPI:.3f} y {y0/PPI:.3f}..{y1/PPI:.3f}"
              f"  (w {x1-x0}px={(x1-x0)/PPI:.3f}in h {y1-y0}px={(y1-y0)/PPI:.3f}in) area {n}")
except ImportError:
    print("no scipy, fallback below")

# ---------- pink formula boxes ----------
print("\n=== PINK FORMULA BOXES ===")
pinkm = (R > 235) & (G > 205) & (G < 252) & (B > 185) & (B < 245) & (R - B > 12)
pinkm[:50] = False
pinkm[512:] = False
try:
    lab, nlab = ndimage.label(pinkm)
    comps = []
    for i in range(1, nlab + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < 3000:
            continue
        comps.append((xs.min(), ys.min(), xs.max(), ys.max(), len(ys)))
    comps.sort(key=lambda c: (c[1], c[0]))
    for c in comps:
        x0, y0, x1, y1, n = c
        print(f"  box x {x0}..{x1} y {y0}..{y1} -> in x {x0/PPI:.3f}..{x1/PPI:.3f} y {y0/PPI:.3f}..{y1/PPI:.3f}"
              f"  (w {(x1-x0)/PPI:.3f}in h {(y1-y0)/PPI:.3f}in) area {n}")
except ImportError:
    pass

# ---------- yellow badge ----------
print("\n=== YELLOW BADGE ===")
yellowm = (R > 230) & (G > 230) & (B < 210) & (R - B > 20)
ys, xs = np.where(yellowm)
print(f"  bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()} -> in x {xs.min()/PPI:.3f}..{xs.max()/PPI:.3f} y {ys.min()/PPI:.3f}..{ys.max()/PPI:.3f}")

# ---------- black bar ----------
print("\n=== BLACK BAR ===")
blackm = (R < 45) & (G < 45) & (B < 45)
rows = np.where(blackm.sum(axis=1) > 500)[0]
print(f"  rows {rows.min()}..{rows.max()} -> in y {rows.min()/PPI:.3f}..{rows.max()/PPI:.3f}  (h {(rows.max()-rows.min()+1)/PPI:.3f}in)")
rowdata = blackm[rows.min()]
xs = np.where(rowdata)[0]
print(f"  x {xs.min()}..{xs.max()} -> in {xs.min()/PPI:.3f}..{xs.max()/PPI:.3f} (w {(xs.max()-xs.min()+1)/PPI:.3f}in)")

# ---------- red frame edges via scanline ----------
print("\n=== RED FRAME scanline ===")
for y in [108, 276, 516]:
    pass
# find red pixels by column
colred = redm.sum(axis=0)
xr = np.where(colred > 30)[0]
print(f"  cols with red ink: {xr.min()}..{xr.max()} -> in {xr.min()/PPI:.3f}..{xr.max()/PPI:.3f}")
rowred = redm.sum(axis=1)
yr = np.where(rowred > 60)[0]
print(f"  rows with red ink: {yr.min()}..{yr.max()} -> in {yr.min()/PPI:.3f}..{yr.max()/PPI:.3f}")
