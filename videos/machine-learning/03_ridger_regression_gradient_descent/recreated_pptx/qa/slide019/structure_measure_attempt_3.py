#!/usr/bin/env python3
"""Definitive structure measurement of the original slide 019 table.

Outputs:
  1. yellow band extents (x/y) — row-group highlights
  2. per-column text bands (blue/red/green/black) with y-range + x-extent
  3. top/bottom table border colors per x-segment
  4. thin vertical rules: x, y-extent, sampled color (real gridlines?)
"""
import numpy as np
from PIL import Image

VID = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{VID}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]
mx = np.max(o, axis=2); mn = np.min(o, axis=2); sat = mx - mn
Bl = (b > 150) & (r < 130) & (g < 130)
Rd = (r > 150) & (g < 110) & (b < 110)
Gr = (g > 110) & (r < 130) & (b < 130)
K = (mx < 95)
Y = (r > 170) & (g > 170) & (b < 150) & (sat > 40)

# ── 1. yellow bands ───────────────────────────────────────────────────────────
print("=== YELLOW bands: rows with >=400 yellow px in x54..903 ===")
rows = np.where(Y[:, 54:903].sum(axis=1) >= 400)[0]
for y in rows:
    xs = np.where(Y[y, 54:903])[0] + 54
    print(f"  y={y}  x{xs.min()}..{xs.max()}  n={len(xs)}")

# ── 2. per-column text bands ──────────────────────────────────────────────────
def bands_in(mask, x0, x1, y0, y1, min_rows=2):
    rows = mask[y0:y1, x0:x1].sum(axis=1)
    on = rows > 0
    out, y = [], 0
    while y < len(on):
        if on[y]:
            j = y
            while j < len(on) and on[j]:
                j += 1
            if j - y >= min_rows:
                sub = mask[y0 + y:y0 + j, x0:x1]
                cols = np.where(sub.any(axis=0))[0] + x0
                out.append((y0 + y, y0 + j, cols.min(), cols.max(), int(sub.sum())))
            y = j
        else:
            y += 1
    return out

print("\n=== per-column text bands (y165..530) ===")
for name, x0, x1 in [("OUTLIER", 66, 118), ("NOREG", 124, 380), ("RIDGE3", 384, 640), ("RIDGE10", 644, 900)]:
    print(f"\n--- {name} x{x0}..{x1} ---")
    for cname, m in (("blue", Bl), ("red", Rd), ("green", Gr), ("black", K)):
        for y0, y1, cx0, cx1, n in bands_in(m, x0, x1, 165, 530):
            # skip rule-like bands: nearly full column width and <=2px tall
            if (y1 - y0) <= 2 and (cx1 - cx0) > (x1 - x0) * 0.8:
                print(f"  {cname:5s} RULE  y{y0}..{y1} x{cx0}..{cx1}")
                continue
            print(f"  {cname:5s} y{y0:3d}..{y1:3d} (h={y1-y0:2d}) x{cx0:3d}..{cx1:3d} (w={cx1-cx0:3d}) px={n}")

# ── 3. top/bottom border colors per x-segment ─────────────────────────────────
print("\n=== table top/bottom border color per x-segment ===")
for label, y0, y1 in (("TOP", 168, 173), ("BOTTOM", 521, 527)):
    for xa, xb in ((60, 130), (130, 380), (384, 640), (644, 900)):
        sub = o[y0:y1, xa:xb].reshape(-1, 3)
        inked = sub[(np.abs(sub - np.array([233, 233, 227])).sum(axis=1) > 60)]
        if len(inked):
            q = (inked // 16) * 16
            keys, counts = np.unique(q, axis=0, return_counts=True)
            i = np.argmax(counts)
            print(f"  {label} x{xa}..{xb}: dominant {tuple(int(v) for v in keys[i])} n={counts[i]}/{len(inked)}")
        else:
            print(f"  {label} x{xa}..{xb}: none")

# ── 4. thin vertical rules: y-extent + color at mid-height ────────────────────
print("\n=== thin vertical rules (1-2px) y-extent + color ===")
cands = [(129, 131), (205, 206), (236, 237), (269, 270), (302, 303), (335, 336), (368, 374),
         (390, 390), (465, 466), (495, 497), (528, 530), (562, 563), (595, 596), (628, 649),
         (648, 649), (724, 725), (754, 755), (787, 788), (821, 821), (853, 854), (886, 895)]
for xa, xb in cands:
    col = o[:, xa:xb + 1]
    inked = (np.abs(col - np.array([233, 233, 227])).sum(axis=2) > 60).any(axis=1)
    ys = np.where(inked)[0]
    if len(ys) == 0:
        continue
    # dominant color over the rule's span
    sub = o[ys.min():ys.max() + 1, xa:xb + 1].reshape(-1, 3)
    q = (sub // 16) * 16
    keys, counts = np.unique(q, axis=0, return_counts=True)
    i = np.argmax(counts)
    print(f"  x{xa:3d}..{xb:3d}  y{ys.min():3d}..{ys.max():3d} (span {ys.max()-ys.min():3d})  "
          f"dominant {tuple(int(v) for v in keys[i])} n={counts[i]}")
