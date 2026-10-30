#!/usr/bin/env python3
"""Slide 041 pass 7: colors (histograms), marker glyph shapes (ASCII), tick
label bands, panel-interior text line bands. Banks measurements7.json.
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


def topcolors(arr, n=5):
    uq, ct = np.unique(arr.reshape(-1, 3), axis=0, return_counts=True)
    idx = np.argsort(-ct)[:n]
    return {str(tuple(uq[i].tolist())): int(ct[i]) for i in idx}


def runs(vals, tol=1):
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


# ---- colors ----
out["plot_border_top_hist"] = topcolors(a[173:176, 350:790])
out["plot_border_left_hist"] = topcolors(a[200:450, 312:316])
out["gridline_v_hist"] = topcolors(a[180:470, 361:364])
out["gridline_h_hist"] = topcolors(a[213:216, 380:770])
out["panel_border_top_hist"] = topcolors(a[54:58, 100:700])
out["panel_border_left_hist"] = topcolors(a[60:125, 68:71])
out["panel_fill_hist"] = topcolors(a[60:125, 300:700])
out["blue_marker_hist"] = topcolors(a[364:372, 412:420])
out["red_marker_hist"] = topcolors(a[425:433, 359:367])
out["red_marker2_hist"] = topcolors(a[241:249, 728:736])
out["magenta_marker_hist"] = topcolors(a[242:249, 676:683])
out["magenta_marker2_hist"] = topcolors(a[304:310, 623:630])

# ---- marker glyph shapes as ascii ----
def ascii_shape(box, mask, label):
    y0, y1, x0, x1 = box
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    lines = []
    for row in sub:
        lines.append("".join("#" if v else "." for v in row))
    out["shape_" + label] = lines


blue = (B - R >= 40) & (B >= 90) & (R <= 120)
redm = (R > 110) & ((R - G) > 60) & ((R - B) > 30)
mag = (R > 110) & (B > 110) & (G <= 110) & (abs(R - B) <= 60)
ascii_shape((364, 371, 412, 419), blue, "blue")
ascii_shape((395, 402, 464, 472), blue, "blue2")
ascii_shape((425, 432, 359, 367), redm, "red00")
ascii_shape((364, 371, 517, 525), redm, "red32")
ascii_shape((241, 248, 728, 735), redm, "red76")
ascii_shape((242, 249, 676, 682), mag, "mag66")
ascii_shape((273, 279, 676, 682), mag, "mag65")
ascii_shape((304, 309, 623, 629), mag, "mag54")

# ---- tick labels: loose ink mask ----
ink = (R < 235) & (G < 235) & (B < 235)
out["xtick_ink_cols"] = runs([c for c in range(310, 830) if ink[483:518, c].sum() >= 1])
out["xtick_ink_rows"] = runs([r for r in range(482, 520) if ink[r, 340:800].sum() >= 1])
out["ytick_ink_rows"] = runs([r for r in range(180, 480) if ink[r, 285:311].sum() >= 1])
out["ytick_ink_cols"] = runs([c for c in range(280, 315) if ink[180:480, c].sum() >= 1])
# heights of individual tick glyphs (x labels): column groups in band
xb = ink[483:518, 310:830]
colsum = xb.sum(axis=0)
groups = []
cur = None
for c, v in enumerate(colsum):
    if v >= 1:
        if cur is None:
            cur = [310 + c, 310 + c]
        else:
            cur[1] = 310 + c
    else:
        if cur:
            groups.append(tuple(cur))
            cur = None
if cur:
    groups.append(tuple(cur))
out["xtick_glyph_groups"] = groups
out["xtick_glyph_heights"] = []
for g in groups:
    sub = ink[483:518, g[0]:g[1] + 1]
    rows = np.where(sub.sum(axis=1) >= 1)[0]
    if len(rows):
        out["xtick_glyph_heights"].append([g, int(rows.min() + 483), int(rows.max() + 483), int(rows.max() - rows.min() + 1)])
yb = ink[180:480, 285:311]
rowsum = yb.sum(axis=1)
groups = []
cur = None
for r, v in enumerate(rowsum):
    if v >= 1:
        if cur is None:
            cur = [180 + r, 180 + r]
        else:
            cur[1] = 180 + r
    else:
        if cur:
            groups.append(tuple(cur))
            cur = None
if cur:
    groups.append(tuple(cur))
out["ytick_glyph_groups"] = groups

# ---- panel interior text bands ----
ink2 = (R < 200) & (G < 200) & (B < 200)
zone = ink2[57:128, 71:718]
zrow = zone.sum(axis=1)
out["panel_text_row_bands"] = runs([int(57 + i) for i, v in enumerate(zrow) if v >= 2], tol=1)
# per row-band, column groups
bands = []
for r0, r1, _ in out["panel_text_row_bands"]:
    sub = ink2[r0:r1 + 1, 71:718]
    csum = sub.sum(axis=0)
    cols = runs([int(71 + i) for i, v in enumerate(csum) if v >= 1], tol=3)
    bands.append([int(r0), int(r1), cols])
out["panel_band_cols"] = bands

# red italics zone inside panel ("Step eta = 2" red italic)
red3 = (R > 110) & ((R - G) > 50) & ((R - B) > 40)
sub3 = red3[57:128, 71:718]
rrow = sub3.sum(axis=1)
out["panel_red_row_bands"] = runs([int(57 + i) for i, v in enumerate(rrow) if v >= 1], tol=1)
rcols_runs = runs([int(71 + i) for i, v in enumerate(sub3.sum(axis=0)) if v >= 1], tol=3)
out["panel_red_cols"] = rcols_runs

with open(os.path.join(HERE, "measurements7.json"), "w") as f:
    json.dump(out, f, indent=1)
for k, v in out.items():
    print(k, "=", json.dumps(v)[:900])
