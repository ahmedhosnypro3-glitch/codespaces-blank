#!/usr/bin/env python3
"""Extract exact feature geometry of slide 007 plot panel."""
import json

import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_007.jpg"
OUT = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_007_measure_v2.json"

im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

PX0, PX1, PY0, PY1 = 155, 758, 114, 478  # panel bounds (from re-analysis)


def panel_mask():
    m = np.zeros((H, W), bool)
    m[PY0:PY1, PX0:PX1] = True
    return m


PM = panel_mask()

yellow = (r > 190) & (g > 170) & (b < 160)
strong_red = (r > 160) & (g < 100) & (b < 100)
strong_blue = (b > 130) & (r < 120) & (g < 150)
strong_green = (g > 105) & (r < 130) & (b < 130)

from scipy import ndimage


def components(mask, min_px):
    lab, n = ndimage.label(mask)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px:
            continue
        out.append({
            "cx": round(float(xs.mean()), 1), "cy": round(float(ys.mean()), 1),
            "n": int(len(xs)),
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())],
        })
    return out


res = {}

res["yellow_boxes"] = sorted(components(yellow & PM, 60), key=lambda d: -d["n"])

# dots: strong colored blobs, exclude thin line pixels via min size & aspect
for name, m in [("red", strong_red), ("blue", strong_blue), ("green", strong_green)]:
    blobs = []
    for c in components(m & PM, 60):
        x0, y0, x1, y1 = c["bbox"]
        w, h = x1 - x0 + 1, y1 - y0 + 1
        if w > 26 or h > 26:
            continue
        if c["n"] < 90:
            continue
        blobs.append(c)
    res[f"dots_{name}"] = sorted(blobs, key=lambda d: (d["cy"], d["cx"]))

# hatch families (light tints) - coarse occupancy grid over panel
def tint_mask(kind):
    if kind == "green":
        m = (g - r > 22) & (g - b > 22) & (g > 165) & (r > 110) & (b > 110)
    elif kind == "blue":
        m = (b - r > 45) & (b - g > 45) & (b > 180) & (r > 100) & (r < 210)
    else:
        m = (r - g > 38) & (r - b > 38) & (r > 190) & (g > 120) & (g < 200)
    return m & PM


CELL = 12
grid = {}
for kind in ("green", "blue", "pink"):
    m = tint_mask(kind)
    ys, xs = np.nonzero(m)
    rows = []
    for y in range(PY0, PY1, CELL):
        line = ""
        for x in range(PX0, PX1, CELL):
            cell = m[y:y + CELL, x:x + CELL]
            frac = cell.mean()
            line += " " if frac < 0.04 else ("." if frac < 0.12 else ("+" if frac < 0.3 else "#"))
        rows.append(line)
    grid[kind] = {"y0": PY0, "x0": PX0, "cell": CELL, "rows": rows,
                  "n": int(m.sum()),
                  "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None}
res["hatch_grid"] = grid

# line fits: use pixels of strong color, robustly fit with least squares on the
# long thin structure (take pixels away from blobs and arrowheads by using
# per-column median y of red/green/blue pixels)
def line_profile(mask, name):
    cols = {}
    for x in range(PX0, PX1):
        ys = np.nonzero(mask[:, x])[0]
        ys = ys[(ys >= PY0) & (ys < PY1)]
        if len(ys):
            cols[x] = (int(ys.min()), int(ys.max()), int(len(ys)))
    return cols


for name, m in [("red", strong_red), ("green", strong_green), ("blue", strong_blue)]:
    cols = line_profile(m, name)
    thick = {x: v for x, v in cols.items() if v[2] >= 3}
    xs = np.array(sorted(thick))
    ys = np.array([(thick[x][0] + thick[x][1]) / 2 for x in xs])
    if len(xs) > 10:
        p = np.polyfit(xs, ys, 1)
        res[f"line_{name}"] = {
            "slope_dy_dx": round(float(p[0]), 4),
            "intercept": round(float(p[1]), 1),
            "x_range": [int(xs.min()), int(xs.max())],
            "resid_rms": round(float(np.sqrt(np.mean((np.polyval(p, xs) - ys) ** 2))), 2),
            "thick_cols": int(len(xs)),
        }
    res[f"cols_{name}"] = {str(x): thick.get(x) for x in range(PX0, PX1, 1) if x in thick}

with open(OUT, "w") as fh:
    json.dump(res, fh, indent=1)

print("yellow boxes:", res["yellow_boxes"])
for k in ("red", "blue", "green"):
    print(f"dots_{k}:", res[f"dots_{k}"])
for k in ("red", "green", "blue"):
    if f"line_{k}" in res:
        print(f"line_{k}:", res[f"line_{k}"])
for kind, d in grid.items():
    print(f"--- hatch {kind} bbox={d['bbox']} n={d['n']}")
    for i, row in enumerate(d["rows"]):
        print(f"{d['y0'] + i * d['cell']:3d} {row}")
