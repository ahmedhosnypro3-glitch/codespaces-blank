#!/usr/bin/env python3
"""Final geometry for slide_021: pink box borders, per-graph axes fit, curve colors."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape

# Red is not pure FF0000 in this frame (measured ~(188,150,147) at frame edge, bright red text).
redish = (R - G > 30) & (R - B > 30) & (R > 90)

# pink box red borders: restrict to the two row bands, exclude outer frame rows
for label, (y0, y1) in [("TOP", (50, 108)), ("BOTTOM", (280, 345))]:
    band = redish[y0:y1 + 1]
    # exclude the outer frame cols 56..60 and 899..904
    band[:, 50:66] = False
    band[:, 895:910] = False
    cs = band.sum(axis=0)
    rs = band.sum(axis=1)
    def runs(vals, thr):
        out, st = [], None
        for i, v in enumerate(vals):
            if v > thr and st is None:
                st = i
            elif v <= thr and st is not None:
                out.append((st, i - 1)); st = None
        if st is not None: out.append((st, len(vals) - 1))
        return [r for r in out if r[1] - r[0] >= 1]
    print(f"{label} red col runs:", runs(cs, 30))
    print(f"{label} red row runs:", runs(rs, 100))

# also: full border via bbox of red within each quadrant band
for label, (x0, x1, y0, y1) in [("TL box", (110, 420, 50, 108)), ("TR box", (545, 855, 50, 108)),
                                 ("BL box", (90, 435, 280, 345)), ("BR box", (580, 820, 280, 345))]:
    sub = redish[y0:y1 + 1, x0:x1 + 1]
    sub[:, 0:14] = False
    ys, xs = np.nonzero(sub)
    if len(xs):
        print(f"{label} red ink bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")

# ---- axis / grid fit per graph using the strong gray gridlines measured earlier
FRAMES = {"TL": (121, 109, 400, 272), "TR": (563, 109, 842, 275),
          "BL": (121, 346, 400, 508), "BR": (564, 346, 842, 508)}

print("\n--- grid geometry (measured earlier, re-derived) ---")
for name, (x0, y0, x1, y1) in FRAMES.items():
    ix0, iy0, ix1, iy1 = x0 + 5, y0 + 5, x1 - 5, y1 - 5
    sub = a[iy0:iy1 + 1, ix0:ix1 + 1]
    sr, sg, sb = sub[:, :, 0], sub[:, :, 1], sub[:, :, 2]
    gray = (abs(sr - sg) < 16) & (abs(sg - sb) < 16) & (sr > 130) & (sr < 250)
    gcol = gray.sum(axis=0)
    grow = gray.sum(axis=1)
    cols = [(ix0 + i, int(gcol[i])) for i in np.nonzero(gcol > (iy1 - iy0) * 0.45)[0]]
    rows = [(iy0 + i, int(grow[i])) for i in np.nonzero(grow > (ix1 - ix0) * 0.45)[0]]
    print(f"{name}: frame w={x1-x0+1} h={y1-y0+1}")
    print(f"   strong gray cols: {cols}")
    print(f"   strong gray rows: {rows}")
