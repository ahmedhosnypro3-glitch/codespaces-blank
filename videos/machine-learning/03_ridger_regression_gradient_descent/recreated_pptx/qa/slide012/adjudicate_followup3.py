#!/usr/bin/env python3
"""Focused adjudication follow-up for findings 3 (test-table colour phase) and
5 (arrow), measured against BOTH images. Also a whole-frame red-ink census of
the original so the arrow question is settled by inventory, not by a single
window."""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg"
REND = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_2.png"

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
S = r.shape[1] / o.shape[1]


def hue_split(a, x0, y0, x1, y1, scale=1.0):
    """Classify each clearly-inked pixel as RED-dominant, BLUE-dominant, or
    neutral (grid/label black). Returns counts + the dominant ratio."""
    sub = a[int(y0*scale):int(y1*scale), int(x0*scale):int(x1*scale)]
    flat = sub.reshape(-1, 3)
    R, G, B = flat[:, 0], flat[:, 1], flat[:, 2]
    bright = flat.max(axis=1) - flat.min(axis=1)   # saturation
    isred = (R > G + 25) & (R > B + 25) & (bright > 30) & (R > 120)
    isblue = (B > R + 25) & (B > G + 25) & (bright > 30) & (B > 120)
    return int(isred.sum()), int(isblue.sum())


print("=" * 74)
print("FINDING 3 — test-table colour phase (ORIGINAL vs RENDER)")
print("=" * 74)
print("Classified per cell: (red px, blue px). 'phase' = which dominates.")
TX = [719, 770, 821, 871]
TY = [128, 160, 190, 221, 252]
labels = [["Test1", "Test2", "Test3"], ["30", "40", "50"], ["15", "20", "25"], ["60", "80", "100"]]
for nm, img, sc in (("ORIGINAL", o, 1.0), ("RENDER  ", r, S)):
    print(f"\n{nm}:")
    for ri in range(4):
        cells = []
        for ci in range(3):
            rp, bp = hue_split(img, TX[ci]+4, TY[ri]+4, TX[ci+1]-4, TY[ri+1]-4, sc)
            ph = "RED" if rp > bp else ("BLUE" if bp > rp else "tie")
            cells.append(f"{labels[ri][ci]:>6s}: r{rp:5d} b{bp:5d} -> {ph}")
        print("   " + " | ".join(cells))

print("\n" + "=" * 74)
print("Same test on the TRAINING tables (known-good reference phase)")
print("=" * 74)
TC = [203, 244, 285, 326, 367, 407, 448, 489, 529, 571]
TH = [127, 158, 189, 219, 249]
tl = [["", "X1", "X2", "X3", "X4", "X5", "X6", "X7", "X8"],
      ["X1", "1", "2", "3", "4", "8", "9", "10", "11"],
      ["X2", "1", "3", "5", "6", "16", "7", "5", "3"],
      ["y", "2", "4", "6", "8", "16", "18", "20", "22"]]
for nm, img, sc in (("ORIGINAL", o, 1.0), ("RENDER  ", r, S)):
    out = []
    for ci in range(9):
        rp, bp = hue_split(img, TC[ci]+4, TH[1]+4, TC[ci+1]-4, TH[2]-4, sc)
        out.append(f"{tl[1][ci]}>={ 'R' if rp>bp else 'B'}" if rp != bp else f"{tl[1][ci]}>=tie")
    print(f"{nm} T1 row1: " + " ".join(out))

print("\n" + "=" * 74)
print("FINDING 5 — whole-frame red-ink census of the ORIGINAL")
print("=" * 74)
m = (o[:, :, 0] > 150) & (o[:, :, 1] < 90) & (o[:, :, 2] < 90)
print(f"total red px in frame: {m.sum()}")
# 8-connected component inventory via simple BFS (small counts expected)
from collections import deque
seen = np.zeros_like(m, dtype=bool)
comps = []
ys, xs = np.nonzero(m)
for y0, x0 in zip(ys, xs):
    if seen[y0, x0]:
        continue
    q = deque([(y0, x0)]); seen[y0, x0] = True
    pts = []
    while q:
        y, x = q.popleft(); pts.append((y, x))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y+dy, x+dx
                if 0 <= ny < m.shape[0] and 0 <= nx < m.shape[1] and m[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
    P = np.array(pts)
    if len(pts) >= 8:
        comps.append((len(pts), P[:, 1].min(), P[:, 1].max(), P[:, 0].min(), P[:, 0].max()))
comps.sort(reverse=True)
print(f"components with >=8 px: {len(comps)}")
for n, x0, x1, y0, y1 in comps[:18]:
    print(f"   n={n:5d}  bbox x{x0}..{x1} y{y0}..{y1}  (w={x1-x0+1} h={y1-y0+1})")
print("\nRed-ink census done. Any narrow tall component far from the known boxes")
print("(title, 4 label boxes, Again callout) is a candidate arrow/leader.")

print("\n" + "=" * 74)
print("Same census for the RENDER")
print("=" * 74)
mr = (r[:, :, 0] > 150) & (r[:, :, 1] < 90) & (r[:, :, 2] < 90)
print(f"total red px: {mr.sum()}")
seen = np.zeros_like(mr, dtype=bool); comps = []
ys, xs = np.nonzero(mr)
for y0, x0 in zip(ys, xs):
    if seen[y0, x0]:
        continue
    q = deque([(y0, x0)]); seen[y0, x0] = True; pts = []
    while q:
        y, x = q.popleft(); pts.append((y, x))
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                ny, nx = y+dy, x+dx
                if 0 <= ny < mr.shape[0] and 0 <= nx < mr.shape[1] and mr[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True; q.append((ny, nx))
    P = np.array(pts)
    if len(pts) >= 8:
        comps.append((len(pts), P[:, 1].min()/S, P[:, 1].max()/S, P[:, 0].min()/S, P[:, 0].max()/S))
comps.sort(reverse=True)
for n, x0, x1, y0, y1 in comps[:14]:
    print(f"   n={n:5d}  bbox x{x0:.0f}..{x1:.0f} y{y0:.0f}..{y1:.0f} (frame px)")
