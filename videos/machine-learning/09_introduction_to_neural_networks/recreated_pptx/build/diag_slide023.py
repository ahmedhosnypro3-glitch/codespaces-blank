#!/usr/bin/env python3
"""Precise slide_023 extents: badge, title, peach/cream boxes per row."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_023.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = a.shape
gray = a.mean(axis=2)
EXCL_BOTTOM = 518


def runs(mask_rows, axis=0, min_len=5):
    """contiguous runs of True along axis"""
    out = []
    start = None
    for i, v in enumerate(mask_rows):
        if v and start is None:
            start = i
        elif not v and start is not None:
            if i - start >= min_len:
                out.append((start, i - 1))
            start = None
    if start is not None and len(mask_rows) - start >= min_len:
        out.append((start, len(mask_rows) - 1))
    return out


def row_bands(mask, y0, y1, min_count=40, min_len=20):
    sel = mask[y0:y1]
    rows = sel.sum(axis=1)
    yy = np.where(rows > min_count)[0] + y0
    if not len(yy):
        return []
    bands, start = [], yy[0]
    for i in range(1, len(yy)):
        if yy[i] - yy[i - 1] > 3:
            bands.append((start, yy[i - 1]))
            start = yy[i]
    bands.append((start, yy[-1]))
    res = []
    for b in bands:
        sub = mask[b[0]:b[1] + 1]
        cols = sub.any(axis=0)
        rs = runs(cols, min_len=min_len)
        res.append((b, rs))
    return res


# ---- badge: yellow circle top-right ----
print("== badge search (x>850, y<200) ==")
sub = a[:200, 850:]
yel = (sub[:, :, 0] > 235) & (sub[:, :, 1] > 235) & (sub[:, :, 2] < 210)
ys, xs = np.where(yel)
if len(xs):
    x0, x1 = 850 + xs.min(), 850 + xs.max()
    y0, y1 = ys.min(), ys.max()
    print(f"  yellow bbox x={x0}..{x1} (w={x1-x0+1}) y={y0}..{y1} (h={y1-y0+1})")
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    print("  center px:", a[cy, cx], " px at +5,+5:", a[cy+5, cx+5])
    # dark pixels inside badge (the numeral)
    inner = gray[y0:y1+1, x0:x1+1]
    dk = inner < 100
    dys, dxs = np.where(dk)
    if len(dxs):
        print(f"  numeral ink bbox rel x={dxs.min()}..{dxs.max()} y={dys.min()}..{dys.max()}")

# ---- title ----
print("\n== title text (red on white, y<110) ==")
top = a[:110]
red = (top[:, :, 0] > 140) & (top[:, :, 1] < 110) & (top[:, :, 2] < 110)
ys, xs = np.where(red)
print("  red bbox x=", xs.min(), "..", xs.max(), " y=", ys.min(), "..", ys.max())
print("  sample red px:", a[ys.min()+3, xs.min()+3])

# ---- peach boxes ----
print("\n== peach boxes ==")
peach = (a[:, :, 0] > 230) & (a[:, :, 1] > 200) & (a[:, :, 1] < 245) & (a[:, :, 2] < 245) & (a[:, :, 2] > 190) & (a[:, :, 1] < a[:, :, 0] - 15)
for band, rs in row_bands(peach, 110, EXCL_BOTTOM, min_count=200, min_len=80):
    print(f"  band y={band[0]}..{band[1]} h={band[1]-band[0]+1} xruns={rs}")

# ---- cream boxes ----
print("\n== cream boxes ==")
cream = (a[:, :, 0] > 240) & (a[:, :, 1] > 240) & (a[:, :, 2] > 190) & (a[:, :, 2] < 245)
for band, rs in row_bands(cream, 110, EXCL_BOTTOM, min_count=200, min_len=80):
    print(f"  band y={band[0]}..{band[1]} h={band[1]-band[0]+1} xruns={rs}")

# ---- inner violet frame ----
print("\n== violet frame lines ==")
bv = (a[:, :, 2] > 140) & (a[:, :, 0] < 170) & (a[:, :, 1] < 170)
rows = bv[:EXCL_BOTTOM].sum(axis=1)
cols = bv[:EXCL_BOTTOM].sum(axis=0)
print("  heavy rows:", [(y, int(rows[y])) for y in range(EXCL_BOTTOM) if rows[y] > 300])
print("  heavy cols:", [(x, int(cols[x])) for x in range(W) if cols[x] > 200])

# ---- box borders (red-ish on left boxes, blue-ish on right boxes) ----
print("\n== left-box red borders (rows of left boxes) ==")
for y0, y1 in [(139, 193), (220, 277), (301, 350), (382, 431), (459, 490)]:
    sub = a[y0-8:y1+8]
    r = (sub[:, :, 0] > 120) & (sub[:, :, 1] < 130) & (sub[:, :, 2] < 130)
    for ry in range(sub.shape[0]):
        rs = runs(r[ry], min_len=30)
        if rs:
            print(f"  y={y0-8+ry}: {rs}")
    print("  ---")
