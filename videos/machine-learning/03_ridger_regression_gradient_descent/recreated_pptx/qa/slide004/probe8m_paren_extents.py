#!/usr/bin/env python3
"""Probe 8m: definitive paren measurement - eq PNGs (native px) + render extents (frame coords).

Renders are 2001x1125 (S=2.0844). All frame coords via raw/S.
"""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)
REND = np.asarray(Image.open("recreated_pptx/qa/slide004/render_8.png").convert("RGB")).astype(int)
S = REND.shape[1] / 960.0

def ink_runs(mask_1d):
    out, in_run, start = [], False, 0
    for i, v in enumerate(mask_1d):
        if v and not in_run:
            start, in_run = i, True
        elif not v and in_run:
            out.append((start, i - 1)); in_run = False
    if in_run:
        out.append((start, len(mask_1d) - 1))
    return out

def vert_extent(img, sx0, sx1, sy0, sy1, thr=215):
    """Per-column y-extent of ink in raw window; returns list of (x, y0, y1, nrows)."""
    reg = img[sy0:sy1, sx0:sx1]
    ink = reg.min(axis=2) < thr
    res = []
    for c in range(reg.shape[1]):
        ys = np.where(ink[:, c])[0]
        if len(ys) >= 8:
            res.append((sx0 + c, sy0 + ys.min(), sy0 + ys.max(), len(ys)))
    return res

for tag, img, fx0, fx1, tag2 in [
    ("ORIG left", ORIG, 150, 200, "oL"),
    ("REND left", REND, int(150 * S), int(200 * S), "rL"),
    ("ORIG right", ORIG, 498, 540, "oR"),
    ("REND right", REND, int(498 * S), int(540 * S), "rR"),
]:
    sy0, sy1 = int(95 * S) if tag.startswith("REND") else 95, int(220 * S) if tag.startswith("REND") else 220
    ext = vert_extent(img, fx0, fx1, sy0, sy1)
    # group adjacent columns with similar extents
    print(f"===== {tag} columns with >=8 ink rows (frame x, y0..y1, n) =====")
    for (x, y0, y1, n) in ext:
        fx, fy0, fy1 = x / S, y0 / S, y1 / S
        print(f"  x{fx:7.1f}  y{fy0:6.1f}..{fy1:6.1f}  n={n}")

print()
print("===== eq PNG dims =====")
for name in ["eq_004_Yvec.png", "eq_004_Yhatvec.png"]:
    im = Image.open(f"recreated_pptx/build/{name}") if __import__("os").path.exists(f"recreated_pptx/build/{name}") else Image.open(name)
    print(f"  {name}: {im.size} mode={im.mode}")
