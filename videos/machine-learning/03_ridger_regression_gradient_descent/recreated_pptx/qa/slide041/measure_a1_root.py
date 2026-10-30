#!/usr/bin/env python3
"""Slide 041 measurement pass A (root worker 2): full geometry census of the
original frame unique_slides/slide_041.jpg (960x540, 1px=1pt).

Banks measurements_a1.json. Nothing here is assumed; every number below is
measured. Sections:
  1. frame size + house chrome (panel/strokes/badge)
  2. pale-yellow top panel bbox + border
  3. plot frame bbox, gridlines, axes
  4. marker census (colour family + shape bitmap per marker)
  5. panel ink components (text groups) with dominant colour
"""
import json
import os
from collections import Counter

import numpy as np
from PIL import Image

DECK = "/worksp" + "aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "measurements_a1.json")

im = Image.open(os.path.join(DECK, "unique_slides", "slide_041.jpg")).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

out = {"frame": [W, H], "notes": []}


def mask_red(v=140):
    return (R > v) & (G < 90) & (B < 90)


def mask_blue(v=60):
    return (B > 150) & (R < v + 40) & (G < 140) & (B - R > 50)


def mask_magenta():
    return (R > 140) & (B > 140) & (G < 110) & (abs(R - B) < 90)


def mask_dark():
    return (R < 120) & (G < 120) & (B < 120)


def mask_pale():
    # FFFFCC family
    return (R > 245) & (G > 240) & (B < 245) & (B > 190) & (G - B > 15)


def mask_navy():
    return (B > 110) & (R < 120) & (G < 120) & (B - R > 40)


def rowruns(m, minlen):
    m = np.asarray(m)
    W = m.shape[1]
    res = []
    for y in range(H):
        row = m[y]
        x = 0
        while x < W:
            if row[x]:
                x0 = x
                while x < W and row[x]:
                    x += 1
                if x - x0 >= minlen:
                    res.append([x0, x - 1, x - 1 - x0 / 2.0])
            else:
                x += 1
    return res


def colruns(m, minlen):
    m = np.asarray(m)
    H = m.shape[0]
    res = []
    for x in range(W):
        col = m[:, x]
        y = 0
        while y < H:
            if col[y]:
                y0 = y
                while y < H and col[y]:
                    y += 1
                if y - y0 >= minlen:
                    res.append([y0, y - 1, y - 1 - y0 / 2.0])
            else:
                y += 1
    return res


# ---------------------------------------------------------------- 1. house chrome
tp = mask_pale()
pale_cols = np.where(tp.sum(axis=0) > 40)[0]
pale_rows = np.where(tp.sum(axis=1) > 40)[0]
out["pale_panel_cols"] = [int(pale_cols.min()), int(pale_cols.max())] if len(pale_cols) else None
out["pale_panel_rows"] = [int(pale_rows.min()), int(pale_rows.max())] if len(pale_rows) else None

navy = mask_navy()
out["navy_col_runs_ge50"] = colruns(navy, 50)
out["navy_row_runs_ge100"] = rowruns(navy, 100)

red = mask_red()
out["red_col_runs"] = colruns(red, 30)
out["red_row_runs"] = rowruns(red, 30)
out["red_px_top_band_44_52"] = int(red[44:53, :].sum())

badge = mask_pale()
out["badge_bbox"] = None
# badge is a yellow circle: look for FDFD96-like pixels near (876,73)
cand = (np.abs(R - 253) < 12) & (np.abs(G - 253) < 12) & (np.abs(B - 150) < 40)
ys, xs = np.where(cand)
if len(ys):
    sel = (xs > 840) & (xs < 915) & (ys > 50) & (ys < 100)
    if sel.sum():
        out["badge_bbox"] = [int(xs[sel].min()), int(ys[sel].min()), int(xs[sel].max()), int(ys[sel].max())]

# ---------------------------------------------------------------- 2. panel colours
sub = a[60:128, 60:720]
out["panel_fill_median"] = [int(v) for v in np.median(sub.reshape(-1, 3), axis=0)]
# border samples (navy) - scan the top row band of the panel
pb = navy[56:60, 60:720]
out["panel_border_top_median"] = [int(v) for v in np.median(a[56, 100:700], axis=0)]

# ---------------------------------------------------------------- 3. plot frame
pr = mask_red()
plot_cols = [c for c in out["red_col_runs"] if 250 < c[2] < 400 or 800 < c[2] < 900]
out["plot_frame_cols"] = plot_cols
plot_rows = [r for r in out["red_row_runs"] if 150 < r[2] < 250 or 450 < r[2] < 500]
out["plot_frame_rows"] = plot_rows

# plot interior white
white = (R > 245) & (G > 245) & (B > 245)
out["plot_white_rows"] = rowruns(white & (np.arange(W)[None, :] > 300) & (np.arange(W)[None, :] < 840), 1)[:3]
# gridlines: near-white but slightly darker grey rows inside the plot
inner = slice(180, 478)
grey_rows = []
for y in range(178, 484):
    seg = a[y, 330:820]
    if np.all(seg[:, 0] > 200) and np.all(seg[:, 1] > 200) and np.all(seg[:, 2] > 200):
        pass
# horizontal gridlines: rows where a long run of slightly-grey pixels exists
grey = (np.abs(R - G) < 8) & (np.abs(G - B) < 8) & (R > 190) & (R < 240)
out["hgrid_rows"] = rowruns(grey[:, 320:820], 200)
out["hgrid_rows"] = [(r[0] + 320, r[1] + 320, r[2] + 320) for r in out["hgrid_rows"]]
out["vgrid_cols"] = colruns(grey[180:480, :], 200)
out["vgrid_cols"] = [(c[0] + 180, c[1] + 180, c[2] + 180) for c in out["vgrid_cols"]]

# ---------------------------------------------------------------- 4. markers
out["markers"] = {}
for name, mk in (("blue", lambda: mask_blue()), ("red", lambda: mask_red()), ("magenta", mask_magenta)):
    m = mk()
    if name == "red":
        # restrict to plot interior so the plot frame is not a marker
        m[:180] = False
        m[484:] = False
        m[:, :300] = False
        m[:, 840:] = False
    if name == "magenta":
        m[:180] = False
        m[484:] = False
        m[:, :300] = False
        m[:, 840:] = False
    if name == "blue":
        m[:180] = False
        m[484:] = False
        m[:, :300] = False
        m[:, 840:] = False
    # connected components via simple flood on 4-neighbours
    lab = np.zeros_like(m, dtype=int)
    cur = 0
    comps = []
    yy, xx = np.where(m)
    pix = set(zip(yy.tolist(), xx.tolist()))
    while pix:
        cy, cx = pix.pop()
        stack = [(cy, cx)]
        comp = []
        while stack:
            y, x = stack.pop()
            if (y, x) in pix:
                pix.discard((y, x))
                comp.append((y, x))
                for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    if (y + dy, x + dx) in pix:
                        stack.append((y + dy, x + dx))
        cur += 1
        if len(comp) >= 12:
            comps.append(comp)
    lst = []
    for comp in comps:
        ys = [p[0] for p in comp]
        xs = [p[1] for p in comp]
        bbox = [min(xs), min(ys), max(xs), max(ys)]
        w = bbox[2] - bbox[0] + 1
        h = bbox[3] - bbox[1] + 1
        # per-row width profile -> shape family
        prof = []
        for y in range(bbox[1], bbox[3] + 1):
            prof.append(sum(1 for x in range(bbox[0], bbox[2] + 1) if (y, x) in set(comp)))
        lst.append({
            "bbox": bbox, "cx": round((bbox[0] + bbox[2]) / 2.0, 2),
            "cy": round((bbox[1] + bbox[3]) / 2.0, 2),
            "w": w, "h": h, "n": len(comp), "profile": prof,
        })
    lst.sort(key=lambda d: (-d["cy"], -d["cx"]))
    out["markers"][name] = lst

# colour cores of each marker family
for name, lst in out["markers"].items():
    for i, d in enumerate(lst):
        y0, y1 = d["bbox"][1], d["bbox"][3]
        x0, x1 = d["bbox"][0], d["bbox"][2]
        cnt = Counter(map(tuple, a[y0:y1 + 1, x0:x1 + 1].reshape(-1, 3).tolist()))
        out["markers"][name][i]["top_colors"] = [[int(k[0]), int(k[1]), int(k[2]), v] for k, v in cnt.most_common(3)]

with open(OUT, "w") as f:
    json.dump(out, f, indent=1)

print("frame", out["frame"])
print("pale panel cols/rows", out["pale_panel_cols"], out["pale_panel_rows"])
print("red col runs", out["red_col_runs"])
print("red row runs", out["red_row_runs"])
print("red px top band", out["red_px_top_band_44_52"])
print("badge", out["badge_bbox"])
print("plot white rows", out["plot_white_rows"])
print("hgrid rows", out["hgrid_rows"])
print("vgrid cols", out["vgrid_cols"])
for n, lst in out["markers"].items():
    print("---", n, len(lst))
    for d in lst:
        print("   cx=%s cy=%s w=%s h=%s n=%s prof=%s" % (d["cx"], d["cy"], d["w"], d["h"], d["n"], d["profile"]))
