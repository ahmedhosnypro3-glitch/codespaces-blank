#!/usr/bin/env python3
"""Slide 041 pass 8: panel interior row-band x zone analysis with ink colours,
plus tick-label geometry (dark mask inside gray panel). Banks measurements8.json.
"""
import json
import os

import numpy as np
from PIL import Image

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
a = np.asarray(Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape
HERE = os.path.dirname(os.path.abspath(__file__))
out = {}

dark = (R < 170) & (G < 170) & (B < 170)
red = (R > 110) & ((R - G) > 60) & ((R - B) > 40)
blue = (B - R >= 30) & (B >= 90) & (R <= 140)
green = (G - R >= 30) & (G - B >= 20) & (G >= 80)
navy = (B - R >= 40) & (B >= 60) & (R <= 120)


def runs(vals, tol=2):
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


# ---- panel interior: row bands (ink = any of the four classes) ----
panel = dark | red | blue | green
sub = panel[57:128, 71:718]
rsum = sub.sum(axis=1)
bands = runs([int(57 + i) for i, v in enumerate(rsum) if v >= 2], tol=1)
out["panel_row_bands"] = bands
detail = []
for (r0, r1, _) in bands:
    sub2 = panel[r0:r1 + 1, 71:718]
    csum = sub2.sum(axis=0)
    cols = runs([int(71 + i) for i, v in enumerate(csum) if v >= 1], tol=3)
    entry = {"rows": [int(r0), int(r1)], "col_groups": cols, "glyphs": []}
    for (c0, c1, cc) in cols:
        cell = (slice(r0, r1 + 1), slice(c0, c1 + 1))
        counts = {
            "dark": int(dark[cell].sum()),
            "red": int(red[cell].sum()),
            "blue": int(blue[cell].sum()),
            "green": int(green[cell].sum()),
        }
        dom = max(counts, key=counts.get)
        entry["glyphs"].append({"cols": [int(c0), int(c1), cc], "c": counts, "dom": dom if counts[dom] > 0 else "-"})
    detail.append(entry)
out["panel_detail"] = detail

# ---- vertical paren strokes of the left matrix: columns with tall ink runs ----
zone_l = panel[57:128, 80:240]
tall_cols = []
for c in range(80, 240):
    colv = panel[57:128, c]
    # longest run
    best = 0
    cur = 0
    for v in colv:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    if best >= 20:
        tall_cols.append((int(c), int(best)))
out["left_matrix_tall_cols"] = tall_cols

# ---- vertical paren strokes of the middle vector ----
zone_m = panel[57:128, 330:400]
tall_cols = []
for c in range(330, 400):
    colv = panel[57:128, c]
    best = cur = 0
    for v in colv:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    if best >= 15:
        tall_cols.append((int(c), int(best)))
out["mid_vector_tall_cols"] = tall_cols

# ---- vertical paren strokes of the right matrix ----
zone_r = panel[57:128, 590:665]
tall_cols = []
for c in range(590, 665):
    colv = panel[57:128, c]
    best = cur = 0
    for v in colv:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    if best >= 15:
        tall_cols.append((int(c), int(best)))
out["right_matrix_tall_cols"] = tall_cols

# ---- tick labels (dark digits inside gray panel) ----
xt = dark[482:516, 300:840]
out["xtick_col_groups"] = runs([int(300 + i) for i, v in enumerate(xt.sum(axis=0)) if v >= 1], tol=3)
out["xtick_row_band"] = runs([int(482 + i) for i, v in enumerate(xt.sum(axis=1)) if v >= 1], tol=1)
yt = dark[180:480, 275:311]
out["ytick_row_groups"] = runs([int(180 + i) for i, v in enumerate(yt.sum(axis=1)) if v >= 1], tol=1)
out["ytick_col_band"] = runs([int(275 + i) for i, v in enumerate(yt.sum(axis=0)) if v >= 1], tol=1)

# digit heights (x ticks): for each col group, the row extent
heights = []
for (c0, c1, cc) in out["xtick_col_groups"]:
    sub3 = dark[482:516, c0:c1 + 1]
    rows = np.where(sub3.sum(axis=1) >= 1)[0]
    if len(rows):
        heights.append([int(c0), int(c1), int(rows.min() + 482), int(rows.max() + 482), int(rows.max() - rows.min() + 1)])
out["xtick_glyph_heights"] = heights

# exact gridline x positions per tick label center (v gridlines)
out["v_gridlines_expected"] = [round(362.65 + 52.69 * k, 2) for k in range(9)]
out["h_gridlines_expected"] = [round(429.5 - 30.57 * k, 2) for k in range(8)]

with open(os.path.join(HERE, "measurements8.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1))
