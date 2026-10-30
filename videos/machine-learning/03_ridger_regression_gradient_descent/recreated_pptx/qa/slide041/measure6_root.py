#!/usr/bin/env python3
"""Slide 041 measurement pass 6 (root worker): full self-derivation of every
build-relevant fact from unique_slides/slide_041.jpg (960x540, 1px=1pt).

Banks measurements6.json next to this script.
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
out = {"frame": [W, H]}


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


def label_simple(m):
    # 4-connectivity labeling (no scipy dependency)
    lbl = np.zeros_like(m, dtype=np.int32)
    cur = 0
    Hh, Ww = m.shape
    for r in range(Hh):
        for c in range(Ww):
            if m[r, c] and not lbl[r, c]:
                cur += 1
                stack = [(r, c)]
                while stack:
                    y0, x0 = stack.pop()
                    if y0 < 0 or x0 < 0 or y0 >= Hh or x0 >= Ww:
                        continue
                    if m[y0, x0] and not lbl[y0, x0]:
                        lbl[y0, x0] = cur
                        stack += [(y0 + 1, x0), (y0 - 1, x0), (y0, x0 + 1), (y0, x0 - 1)]
    return lbl


# ---------- 1. pale-yellow content panel + its blue border ----------
pale = (R >= 248) & (G >= 238) & (B >= 195) & (B <= 245)
sub = pale[40:200, 40:930]
prow = sub.sum(axis=1)
pcol = sub.sum(axis=0)
out["pale_fill_rows"] = runs([int(40 + i) for i, v in enumerate(prow) if v > 300])
out["pale_fill_cols"] = runs([int(40 + i) for i, v in enumerate(pcol) if v > 60])
navy = (B - R >= 40) & (B >= 60) & (R <= 120)
out["navy_col_runs_ge30"] = runs([c for c in range(W) if navy[40:200, c].sum() >= 30])
out["navy_row_runs_ge100"] = runs([r for r in range(H) if navy[r, 40:930].sum() >= 100])
# sample border and fill colours
out["fill_sample"] = a[70, 400].tolist()
out["border_sample_top"] = a[55, 400].tolist()
out["border_sample_left"] = a[70, 70].tolist()
out["border_sample_right"] = a[70, 718].tolist()
out["border_sample_bottom"] = a[129, 400].tolist()

# ---------- 2. gray house panel + red strokes ----------
gray = (abs(R - 233) < 14) & (abs(G - 233) < 14) & (abs(B - 231) < 16)
gcol = gray[100:530, :].sum(axis=0)
grow = gray[:, 100:880].sum(axis=1)
out["house_panel_cols"] = runs([c for c in range(W) if gcol[c] > 300], tol=1)
out["house_panel_rows"] = runs([r for r in range(H) if grow[r] > 300], tol=1)
red = (R > 90) & ((R - G) > 40) & ((R - B) > 10)
out["red_col_runs"] = runs([c for c in range(W) if red[46:520, c].sum() >= 200], tol=1)
out["red_row_runs"] = runs([r for r in range(H) if red[r, 60:900].sum() >= 400], tol=1)
top_band = red[44:52, 80:880].sum()
out["red_px_top_band_44_52"] = int(top_band)
out["stroke_left_core"] = a[300, 58].tolist()
out["stroke_right_core"] = a[300, 901].tolist()
out["stroke_bottom_core"] = a[538, 480].tolist()

# ---------- 3. badge ----------
yb = (R > 200) & (G > 200) & (B < 190)
sub3 = yb[50:100, 840:915]
pys, pxs = np.where(sub3)
if len(pys):
    out["badge_bbox"] = [int(840 + pxs.min()), int(50 + pys.min()), int(840 + pxs.max()), int(50 + pys.max())]
    out["badge_center"] = [(840 + pxs.min() + 840 + pxs.max()) / 2, (50 + pys.min() + 50 + pys.max()) / 2]
pur = (B > 150) & (R > 70) & (R < 180) & (G < 130)
out["badge_ring_px"] = int(pur[50:100, 840:915].sum())

# ---------- 4. plot: white area, red border, gridlines ----------
white = (R >= 250) & (G >= 250) & (B >= 250)
out["plot_white_rows"] = runs([r for r in range(160, 500) if white[r, 320:810].sum() > 400], tol=1)
out["plot_white_cols"] = runs([c for c in range(290, 870) if white[200:460, c].sum() > 200], tol=1)
# red border of plot: search strong red runs in the plot zone
red2 = (R > 110) & ((R - G) > 60) & ((R - B) > 30)
out["plot_red_col_runs"] = runs([c for c in range(300, 840) if red2[200:460, c].sum() >= 150], tol=1)
out["plot_red_row_runs"] = runs([r for r in range(160, 500) if red2[r, 320:810].sum() >= 150], tol=1)
# gridline gray: inside plot only
grayish = (R > 140) & (R < 250) & (abs(R - G) <= 25) & (abs(G - B) <= 25)
subg = grayish[180:475, 316:820]
out["v_grid_runs"] = runs([int(316 + i) for i, v in enumerate(subg.sum(axis=0)) if v >= 100], tol=1)
out["h_grid_runs"] = runs([int(180 + i) for i, v in enumerate(subg.sum(axis=1)) if v >= 100], tol=1)
out["gridline_color"] = a[245, 500].tolist()
out["gridline_color2"] = a[245, 550].tolist()

# ---------- 5. markers ----------
blue = (B - R >= 40) & (B >= 90) & (R <= 120)
redm = (R > 110) & ((R - G) > 60) & ((R - B) > 30)
mag = (R > 110) & (B > 110) & (G <= 110) & (abs(R - B) <= 60)
for name, mask in (("blue", blue), ("red", redm), ("magenta", mag)):
    m = mask[180:475, 316:820].astype(np.uint8)
    lbl = label_simple(m)
    comps = []
    for lab in range(1, lbl.max() + 1):
        ys, xs = np.where(lbl == lab)
        n = len(ys)
        if n >= 6:
            comps.append({"cx": round(float(316 + xs.mean()), 2), "cy": round(float(180 + ys.mean()), 2),
                          "w": int(xs.max() - xs.min() + 1), "h": int(ys.max() - ys.min() + 1), "n": int(n),
                          "bbox": [int(316 + xs.min()), int(180 + ys.min()), int(316 + xs.max()), int(180 + ys.max())]})
    out["markers_" + name] = sorted(comps, key=lambda c: (c["cy"], c["cx"]))

# core colors
out["color_red_core"] = a[244, 731].tolist()
out["color_red_core2"] = a[367, 521].tolist()
out["color_mag_core"] = a[245, 679].tolist()
out["color_blue_core"] = a[367, 415].tolist()

# corner check: blue square at (0,0)?
out["corner_00_box"] = a[424:436, 356:370].reshape(-1, 3).tolist()[:0]
corner = a[422:436, 356:370].reshape(-1, 3)
uq, ct = np.unique(corner, axis=0, return_counts=True)
out["corner_00_top"] = {str(tuple(uq[i].tolist())): int(ct[i]) for i in np.argsort(-ct)[:6]}

# ---------- 6. text bands inside pale panel (ink columns/rows) ----------
ink = (R < 200) & (G < 200) & (B < 200)
zone = ink[50:135, 60:730]
zrow = zone.sum(axis=1)
zcol = zone.sum(axis=0)
out["panel_ink_rows"] = runs([int(50 + i) for i, v in enumerate(zrow) if v >= 2], tol=1)
out["panel_ink_cols"] = runs([int(60 + i) for i, v in enumerate(zcol) if v >= 1], tol=1)


# ---------- 7. tick labels ----------
dark = (R <= 110) & (G <= 110) & (B <= 110)
xb = dark[484:516, 340:800]
out["xtick_label_col_runs"] = runs([int(340 + i) for i, v in enumerate(xb.sum(axis=0)) if v >= 1])
out["xtick_label_row_band"] = runs([int(484 + i) for i, v in enumerate(xb.sum(axis=1)) if v >= 1], tol=1)
yb2 = dark[205:435, 300:355]
out["ytick_label_row_runs"] = runs([int(205 + i) for i, v in enumerate(yb2.sum(axis=1)) if v >= 1])
out["ytick_label_col_band"] = runs([int(300 + i) for i, v in enumerate(yb2.sum(axis=0)) if v >= 1], tol=1)

with open(os.path.join(HERE, "measurements6.json"), "w") as f:
    json.dump(out, f, indent=1)
print(json.dumps(out, indent=1)[:6000])
