#!/usr/bin/env python3
"""Slide 041 pass 5: settle the gridline raster, the red stroke colour and the
panel's navy border rows. Pass 4 only found verticals at 350 / 362.5 / 784, so
check the raw grey counts per column against the expected gridline positions
(X0=362.65, pitch=52.69, k=0..8) and dump the true red-stroke colour.
"""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = HERE
while not os.path.isdir(os.path.join(DECK, "unique_slides")):
    DECK = os.path.dirname(DECK)
a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape
out = {}

# --- true red-stroke colour: sample the badge ring and any strong red column ---
cand = []
for r in range(46, 539):
    row = a[r, 56:60]
    cand.extend(row.tolist())
uq, ct = np.unique(np.array(cand), axis=0, return_counts=True)
out["stroke_col_sample_x58_band"] = {str(tuple(uq[i].tolist())): int(ct[i]) for i in np.argsort(-ct)[:6]}

uq2, ct2 = np.unique(a[174:176, 312:824].reshape(-1, 3), axis=0, return_counts=True)
out["plot_border_top_row_colors"] = {str(tuple(uq2[i].tolist())): int(ct2[i]) for i in np.argsort(-ct2)[:5]}

uq3, ct3 = np.unique(a[313:315, 313:824].reshape(-1, 3), axis=0, return_counts=True)
out["plot_border_left_col_colors"] = {str(tuple(uq3[i].tolist())): int(ct3[i]) for i in np.argsort(-ct3)[:5]}

# --- grey counts per column over the gridline band (gy0..gy1) ---
gy0, gy1 = 215, 429
grey = (R >= 150) & (R <= 250) & (np.abs(R - G) <= 25) & (np.abs(G - B) <= 25) \
       & ~((R >= 248) & (G >= 248) & (B >= 245))
sub = grey[gy0:gy1 + 1, 300:840]
gcol = sub.sum(axis=0)
out["v_grid_top_columns"] = sorted([(int(300 + i), int(v)) for i, v in enumerate(gcol) if v >= 20],
                                   key=lambda t: -t[1])[:20]

# --- grey counts per row over the horizontal band gx0..gx1 ---
gx0, gx1 = 364, 782
sub2 = grey[170:485, gx0:gx1 + 1]
grow = sub2.sum(axis=1)
out["h_grid_top_rows"] = sorted([(int(170 + i), int(v)) for i, v in enumerate(grow) if v >= 100],
                                key=lambda t: -t[1])[:20]

# --- navy border rows of the content panel (full-width runs) ---
navy = (B - R >= 40) & (B >= 60) & (R <= 120)
nrow = navy.sum(axis=1)
out["navy_row_runs_ge200"] = [int(r) for r in range(H) if nrow[r] >= 200]
ncol = navy.sum(axis=0)
out["navy_col_runs_ge60"] = [int(c) for c in range(W) if ncol[c] >= 60]

# --- black spines inside the plot ---
black = (R <= 80) & (G <= 80) & (B <= 80)
bcol = black[215:430, 316:820].sum(axis=0)
brow = black[215:430, 316:820].sum(axis=1)
out["black_cols_ge40"] = [int(316 + i) for i, v in enumerate(bcol) if v >= 40]
out["black_rows_ge40"] = [int(215 + i) for i, v in enumerate(brow) if v >= 40]
out["black_col_top"] = sorted([(int(316 + i), int(v)) for i, v in enumerate(bcol) if v >= 5],
                              key=lambda t: -t[1])[:12]
out["black_row_top"] = sorted([(int(215 + i), int(v)) for i, v in enumerate(brow) if v >= 5],
                              key=lambda t: -t[1])[:12]

# --- tick labels: dark pixels below/left of the plot box, tight mask ---
def runs(vals, tol=4):
    if not vals:
        return []
    vals = sorted(vals)
    groups, cur = [], [vals[0]]
    for v in vals[1:]:
        if v - cur[-1] <= tol:
            cur.append(v)
        else:
            groups.append(cur)
            cur = [v]
    groups.append(cur)
    return [(g[0], g[-1], round(sum(g) / len(g), 2)) for g in groups]


dark = (R <= 110) & (G <= 110) & (B <= 110)
xb = dark[482:514, 355:792]
out["xtick_label_runs"] = runs([int(355 + i) for i, v in enumerate(xb.sum(axis=0)) if v >= 1])
out["xtick_label_bands_rows"] = runs([int(482 + i) for i, v in enumerate(xb.sum(axis=1)) if v >= 1], tol=2)
yb = dark[210:435, 300:358]
out["ytick_label_runs"] = runs([int(210 + i) for i, v in enumerate(yb.sum(axis=1)) if v >= 1])
out["ytick_label_bands_cols"] = runs([int(300 + i) for i, v in enumerate(yb.sum(axis=0)) if v >= 1], tol=2)

with open(os.path.join(HERE, "measurements5.json"), "w") as f:
    json.dump(out, f, indent=1)

for k, v in out.items():
    s = json.dumps(v)
    print(k, "=", (s[:400] + "...") if len(s) > 400 else s)
