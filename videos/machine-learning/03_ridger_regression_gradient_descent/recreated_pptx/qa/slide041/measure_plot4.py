#!/usr/bin/env python3
"""Slide 041 measurement pass 4 — definitive geometry.

Pass 2/3 grid windows were too loose (JPEG near-white noise). This pass:
  * locates the original's content panel (pale-yellow fill, navy border) precisely
  * locates the house-chrome panel (E9E9E7) + the three red strokes + the badge
  * measures the plot's red border box, the black axis spines, the gridlines
    (window 175..248 grey, excluding near-white), and the tick labels
  * classifies every marker inside the plot by an exact colour-window dump
Everything is reported in frame px, 1px = 1pt.
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

a = np.asarray(Image.open(IMG).convert("RGB")).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape
out = {"frame": [W, H]}

# ---------- 1. house chrome ----------
house = (np.abs(R - 233) <= 14) & (np.abs(G - 233) <= 14) & (np.abs(B - 231) <= 14)
ys, xs = np.nonzero(house)
if len(xs):
    out["house_panel_px"] = {"x": [int(xs.min()), int(xs.max())],
                             "y": [int(ys.min()), int(ys.max())]}

red = (np.abs(R - 192) <= 45) & (G <= 70) & (B <= 70)
colred = red.sum(axis=0)
rowred = red.sum(axis=1)
out["red_cols_ge_300"] = [int(c) for c in range(W) if colred[c] >= 300]
out["red_rows_ge_300"] = [int(r) for r in range(H) if rowred[r] >= 300]
out["red_cols_ge_100"] = [int(c) for c in range(W) if 100 <= colred[c] < 300]
out["red_rows_ge_100"] = [int(r) for r in range(H) if 100 <= rowred[r] < 300]

badge = (np.abs(R - 253) <= 10) & (np.abs(G - 253) <= 10) & (np.abs(B - 150) <= 12)
by, bx = np.nonzero(badge)
if len(bx):
    out["badge_bbox"] = {"x": [int(bx.min()), int(bx.max())],
                         "y": [int(by.min()), int(by.max())]}

# ---------- 2. original content panel (pale-yellow) ----------
pale = (R >= 240) & (G >= 240) & (B >= 210) & (B <= 245) & (R - B >= 8) & (G - B >= 8)
pcol = pale.sum(axis=0)
prow = pale.sum(axis=1)
out["pale_panel_cols"] = [int(c) for c in range(W) if pcol[c] >= 20]
out["pale_panel_rows"] = [int(r) for r in range(H) if prow[r] >= 20]

# navy border of that panel: dark blue, |B-R| >= 40
navy = (B - R >= 40) & (B >= 60) & (R <= 120)
ncol = navy.sum(axis=0)
nrow = navy.sum(axis=1)
out["navy_cols_ge_60"] = [int(c) for c in range(W) if ncol[c] >= 60]
out["navy_rows_ge_200"] = [int(r) for r in range(H) if 200 <= nrow[r] < 380]

# ---------- 3. plot red border box ----------
# the plot border is a red box; find the inner faces by looking at columns 300..340 etc.
out["plot_border_sides"] = {
    "col_counts": {c: int(colred[c]) for c in range(305, 340) if colred[c] > 0},
    "col_counts_r": {c: int(colred[c]) for c in range(810, 840) if colred[c] > 0},
    "row_counts": {r: int(rowred[r]) for r in range(165, 200) if rowred[r] > 0},
    "row_counts_b": {r: int(rowred[r]) for r in range(470, 500) if rowred[r] > 0},
}

# ---------- 4. gridlines, excluding near-white ----------
PL, PR, PT, PB = 316, 820, 177, 477
grey = (R >= 170) & (R <= 250) & (np.abs(R - G) <= 12) & (np.abs(G - B) <= 12) \
       & ~((R >= 248) & (G >= 248) & (B >= 245))
gcol = grey[PT:PB, PL:PR].sum(axis=0)
grow = grey[PT:PB, PL:PR].sum(axis=1)


def runs(idxs, tol=2):
    if not idxs:
        return []
    idxs = sorted(idxs)
    groups, cur = [], [idxs[0]]
    for v in idxs[1:]:
        if v - cur[-1] <= tol:
            cur.append(v)
        else:
            groups.append(cur)
            cur = [v]
    groups.append(cur)
    return [(g[0], g[-1], round(sum(g) / len(g), 2)) for g in groups]


out["v_grid_frac_runs"] = runs([PL + i for i, v in enumerate(gcol) if v >= 40])
out["h_grid_frac_runs"] = runs([PT + i for i, v in enumerate(grow) if v >= 60])
out["v_grid_frac_max"] = int(gcol.max())
out["h_grid_frac_max"] = int(grow.max())

# ---------- 5. black axis spines ----------
black = (R <= 80) & (G <= 80) & (B <= 80)
bcol = black[PT:PB, PL:PR].sum(axis=0)
brow = black[PT:PB, PL:PR].sum(axis=1)
out["black_cols_ge_40"] = [PL + i for i, v in enumerate(bcol) if v >= 40]
out["black_rows_ge_40"] = [PT + i for i, v in enumerate(brow) if v >= 40]

# ---------- 6. tick labels (dark, outside the plot box) ----------
out["xtick_label_runs"] = runs(
    [PL + i for i, v in enumerate(black[PB + 4:PB + 32, PL:PR].sum(axis=0)) if v >= 1], tol=4)
out["ytick_label_runs"] = runs(
    [PT - 4 + i for i, v in enumerate(black[PT - 4:PB + 4, PL - 52:PL - 2].sum(axis=1)) if v >= 1],
    tol=4)

# ---------- 7. markers ----------
def comps(mask, min_px=8, region=None):
    m = mask.copy()
    if region:
        y0, y1, x0, x1 = region
        m[:y0] = False
        m[y1:] = False
        m[:, :x0] = False
        m[:, x1:] = False
    res, seen = [], np.zeros_like(m, dtype=bool)
    ys, xs = np.nonzero(m)
    for y, x in zip(ys, xs):
        if seen[y, x]:
            continue
        st = [(y, x)]
        seen[y, x] = True
        pts = []
        while st:
            cy, cx = st.pop()
            pts.append((cy, cx))
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = cy + dy, cx + dx
                    if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        st.append((ny, nx))
        if len(pts) >= min_px:
            yy = [p[0] for p in pts]
            xx = [p[1] for p in pts]
            res.append({"n": len(pts), "cx": round(sum(xx) / len(xx), 2),
                        "cy": round(sum(yy) / len(yy), 2),
                        "bbox": [int(min(xx)), int(max(xx)), int(min(yy)), int(max(yy))]})
    return sorted(res, key=lambda c: (c["cy"], c["cx"]))


red_m = (R >= 120) & (G <= 90) & (B <= 90)
mag_m = (R >= 120) & (B >= 120) & (G <= 110)
blue_m = (R <= 90) & (B - R >= 30) & (B <= 160) & (G <= 110)
green_m = (G >= 90) & (R <= 110) & (B <= 110)
for nm, mk in (("red", red_m), ("magenta", mag_m), ("blue_navy", blue_m), ("green", green_m)):
    out["markers_" + nm] = comps(mk, min_px=6, region=(PT, PB, PL, PR))
    out["markers_" + nm + "_count"] = len(out["markers_" + nm])

# colour dump at the known marker centres to settle shapes/hues
probe = {}
for cy, cx in [(244, 731), (367, 521), (428, 363), (245, 679), (276, 679), (306, 626)]:
    patch = a[cy - 3:cy + 4, cx - 3:cx + 4].reshape(-1, 3)
    uq, ct = np.unique(patch, axis=0, return_counts=True)
    probe["%d,%d" % (cy, cx)] = {str(tuple(uq[i].tolist())): int(ct[i]) for i in np.argsort(-ct)[:4]}
out["marker_colour_probe"] = probe

with open(os.path.join(HERE, "measurements4.json"), "w") as f:
    json.dump(out, f, indent=1)

for k in ("house_panel_px", "badge_bbox", "red_cols_ge_300", "red_rows_ge_300",
          "red_cols_ge_100", "red_rows_ge_100", "pale_panel_cols", "pale_panel_rows",
          "navy_cols_ge_60", "navy_rows_ge_200", "plot_border_sides", "v_grid_frac_runs",
          "h_grid_frac_runs", "black_cols_ge_40", "black_rows_ge_40",
          "xtick_label_runs", "ytick_label_runs", "markers_red_count",
          "markers_magenta_count", "markers_blue_navy_count", "markers_green_count"):
    print(k, "=", out.get(k))
