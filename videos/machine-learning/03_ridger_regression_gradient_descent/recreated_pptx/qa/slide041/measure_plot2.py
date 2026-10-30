#!/usr/bin/env python3
"""Slide 041 measurement pass 2: plot axes, gridlines, tick labels, markers.

Frame: unique_slides/slide_041.jpg, 960x540, 1px = 1pt.
Plot border measured pass 1: left 312-314, right 822-825, top 173-175, bottom 478-481.
Purpose: derive data coordinates of every gridline, tick label and marker so the
recreation can place them from measurement rather than guesswork.
"""
import json
import os
from collections import defaultdict

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
while not os.path.isdir(os.path.join(ROOT, "unique_slides")):
    ROOT = os.path.dirname(ROOT)
IMG = os.path.join(ROOT, "unique_slides", "slide_041.jpg")

im = Image.open(IMG).convert("RGB")
W, H = im.size
a = np.asarray(im).astype(np.int16)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
print("frame", W, H)

out = {}

# ---- plot interior (strictly inside the red border) ----
L, Rr, T, Bt = 316, 820, 177, 477
out["plot_interior"] = {"left": L, "right": Rr, "top": T, "bottom": Bt}

# ---- masks ----
dark = (R < 110) & (G < 110) & (B < 110)
gray_grid = (np.abs(R - 216) <= 16) & (np.abs(G - 216) <= 16) & (np.abs(B - 216) <= 16)
not_gray = ~gray_grid
red = (R >= 140) & (G <= 100) & (B <= 100)
blue = (B >= 140) & (R <= 100) & (G <= 100)
magenta = (R >= 140) & (B >= 140) & (G <= 100)
green = (G >= 90) & (R <= 120) & (B <= 120)

out["mask_counts_inside_plot"] = {
    "dark": int(dark[T:Bt, L:Rr].sum()),
    "gray_grid": int(gray_grid[T:Bt, L:Rr].sum()),
    "red": int(red[T:Bt, L:Rr].sum()),
    "blue": int(blue[T:Bt, L:Rr].sum()),
    "magenta": int(magenta[T:Bt, L:Rr].sum()),
    "green": int(green[T:Bt, L:Rr].sum()),
}

# ---- vertical gridlines: columns with many grid-gray px inside interior ----
colcount = gray_grid[T:Bt, L:Rr].sum(axis=0)
rows, cols = [], []
for c in range(L, Rr):
    if colcount[c - L] >= 120:
        cols.append(c)
out["v_grid_cols_raw"] = cols

# ---- horizontal gridlines ----
rowcount = gray_grid[T:Bt, L:Rr].sum(axis=1)
for r in range(T, Bt):
    if rowcount[r - T] >= 120:
        rows.append(r)
out["h_grid_rows_raw"] = rows


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


out["v_grid_runs"] = runs(cols)
out["h_grid_runs"] = runs(rows)

# ---- red border of the PLOT only (inside interior, not the panel) ----
out["plot_border_red_cols"] = [c for c in range(L, Rr)
                               if int(((T < 0) and 0) or red[176:478, c].sum()) >= 200]
out["plot_border_red_rows"] = [r for r in range(T - 8, Bt + 8)
                               if int(red[r, 310:828].sum()) >= 200]

# ---- tick labels ----
# x tick labels: dark text in the band just below the plot bottom border
band = dark[Bt + 4:Bt + 34, L:Rr]
colhits = band.sum(axis=0)
lab_cols = [L + i for i, v in enumerate(colhits) if v >= 1]
out["xtick_label_runs"] = runs(lab_cols, tol=3)
out["xtick_label_pixelcounts"] = {str(g[2]): int(colhits[g[0] - L:g[1] - L + 1].sum())
                                  for g in runs(lab_cols, tol=3)}

# y tick labels: dark text just left of the left border
band2 = dark[T - 4:Bt + 4, L - 60:L]
rowhits = band2.sum(axis=1)
lab_rows = [T - 4 + i for i, v in enumerate(rowhits) if v >= 1]
out["ytick_label_runs"] = runs(lab_rows, tol=3)

# ---- connected components for each marker colour (inside interior) ----
def components(mask, min_px=4):
    m = mask.copy()
    m[:T] = False
    m[Bt:] = False
    m[:, :L] = False
    m[:, Rr:] = False
    comps = []
    seen = np.zeros_like(m, dtype=bool)
    h, w = m.shape
    for y in range(T, Bt):
        xs = np.nonzero(m[y, L:Rr])[0]
        for x0 in xs:
            x = L + int(x0)
            if seen[y, x]:
                continue
            stack = [(y, x)]
            seen[y, x] = True
            pts = []
            while stack:
                cy, cx = stack.pop()
                pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if T <= ny < Bt and L <= nx < Rr and m[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True
                            stack.append((ny, nx))
            if len(pts) >= min_px:
                ys = [p[0] for p in pts]
                xs2 = [p[1] for p in pts]
                comps.append({"n": len(pts),
                              "cx": round(sum(xs2) / len(xs2), 2),
                              "cy": round(sum(ys) / len(ys), 2),
                              "x0": min(xs2), "x1": max(xs2),
                              "y0": min(ys), "y1": max(ys)})
    return sorted(comps, key=lambda c: (c["cy"], c["cx"]))


out["red_markers"] = components(red, min_px=8)
out["blue_markers"] = components(blue, min_px=8)
out["magenta_markers"] = components(magenta, min_px=8)
out["green_markers"] = components(green, min_px=8)

with open(os.path.join(HERE, "measurements2.json"), "w") as f:
    json.dump(out, f, indent=1)

print("v_grid_runs", out["v_grid_runs"])
print("h_grid_runs", out["h_grid_runs"])
print("red_markers", out["red_markers"])
print("blue_markers", out["blue_markers"])
print("magenta_markers", out["magenta_markers"])
print("green_markers", out["green_markers"])
print("xtick_label_runs", out["xtick_label_runs"])
print("ytick_label_runs", out["ytick_label_runs"])
print("plot_border_red_cols", out["plot_border_red_cols"][:20])
print("plot_border_red_rows", out["plot_border_red_rows"][:20])
