#!/usr/bin/env python3
"""Slide 041 measurement pass 3: full gridline raster + marker/axis colour census.

Pass 2 found horizontal gridlines at y = 214.5, 245, 276, 306.5, 337, 368, 398.5, 429.5
(pitch ~30.7) and two verticals at x = 362.5, 784.5. Red/magenta markers are found but
blue and green are not, and tick labels are dark-on-white outside the mask used by pass 2.
This pass widens the colour windows and dumps the gridline raster inside the plot.
"""
import json
import os

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = HERE
while not os.path.isdir(os.path.join(DECK, "unique_slides")):
    DECK = os.path.dirname(DECK)
IMG = os.path.join(DECK, "unique_slides", "slide_041.jpg")

im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape

out = {}
L, Rr, T, Bt = 316, 820, 177, 477
out["plot_interior"] = {"left": L, "right": Rr, "top": T, "bottom": Bt}

# ---- gridline raster: any pixel inside the plot that is neither white nor coloured ----
white = (R >= 240) & (G >= 240) & (B >= 240)
gray_ish = (np.abs(R - 216) <= 40) & (np.abs(R - G) <= 12) & (np.abs(G - B) <= 12)

colfrac = gray_ish[T:Bt, L:Rr].mean(axis=0)
rowfrac = gray_ish[T:Bt, L:Rr].mean(axis=1)
vc = [L + i for i, f in enumerate(colfrac) if f >= 0.60]
hr = [T + i for i, f in enumerate(rowfrac) if f >= 0.60]


def runs(vals, tol=3):
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
    return [(g[0], g[-1], round(sum(g) / len(g), 2), len(g)) for g in groups]


out["v_grid_frac_runs"] = runs(vc)
out["h_grid_frac_runs"] = runs(hr)

# ---- wide colour census inside the plot (count exact-ish hue families) ----
def census(lo, hi, name):
    m = lo[T:Bt, L:Rr]
    ys, xs = np.nonzero(m)
    out.setdefault("color_census", {})[name] = {"count": int(m.sum())}


census((R >= 120) & (G <= 90) & (B <= 90), None, "redish")
census((B >= 120) & (R <= 90) & (G <= 90), None, "blueish")
census((G >= 100) & (R <= 110) & (B <= 100), None, "greenish")
census((R >= 120) & (B >= 120) & (G <= 110), None, "magentaish")
census((R <= 60) & (G <= 60) & (B <= 60), None, "dark")
out["distinct_colors_top"] = {}
flat = a[T:Bt, L:Rr].reshape(-1, 3)
uniq, cnt = np.unique(flat, axis=0, return_counts=True)
order = np.argsort(-cnt)
for i in order[:18]:
    out["distinct_colors_top"][str(tuple(uniq[i].tolist()))] = int(cnt[i])

# ---- axis tick label rows/cols: dark pixels outside the plot box ----
dark = (R <= 90) & (G <= 90) & (B <= 90)
xband = dark[Bt + 3:Bt + 30, L:Rr]
colhits = xband.sum(axis=0)
out["xtick_label_runs"] = runs([L + i for i, v in enumerate(colhits) if v >= 1], tol=4)
yband = dark[T - 3:Bt + 3, L - 55:L]
rowhits = yband.sum(axis=1)
out["ytick_label_runs"] = runs([T - 3 + i for i, v in enumerate(rowhits) if v >= 1], tol=4)

# ---- scan the whole frame for colour-coded text outside the plot (panel zone) ----
for name, mask in (("red_text_all", (R >= 120) & (G <= 100) & (B <= 100)),
                   ("blue_text_all", (B >= 120) & (R <= 100) & (G <= 100)),
                   ("green_text_all", (G >= 100) & (R <= 120) & (B <= 100))):
    m = mask.copy()
    m[T - 20:Bt + 20, L - 20:Rr + 20] = False  # exclude plot zone
    ys, xs = np.nonzero(m)
    if len(xs):
        out.setdefault("panel_colored_runs", {})[name] = {
            "count": len(xs), "x": [int(xs.min()), int(xs.max())],
            "y": [int(ys.min()), int(ys.max())]}

with open(os.path.join(HERE, "measurements3.json"), "w") as f:
    json.dump(out, f, indent=1)

print("v_grid_frac_runs", out["v_grid_frac_runs"])
print("h_grid_frac_runs", out["h_grid_frac_runs"])
print("color_census", out["color_census"])
print("top colors", out["distinct_colors_top"])
print("xtick_label_runs", out["xtick_label_runs"])
print("ytick_label_runs", out["ytick_label_runs"])
print("panel_colored_runs", out.get("panel_colored_runs"))
