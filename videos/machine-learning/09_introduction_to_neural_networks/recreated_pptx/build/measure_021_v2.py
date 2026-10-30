"""Precise geometry of slide_021.jpg for the wave-3 rebuild: formula boxes, plot frames,
axis/grid calibration, curve traces, tick-label placement.

Frame is 960x540 px and the slide is 13.33x7.5 in (LAYOUT_WIDE), so 1 px = 1 pt = 1/72 in.
"""
import json
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
OUT = V + "recreated_pptx/qa/slide021/measure_021_v2.json"

im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, bl = a[:, :, 0], a[:, :, 1], a[:, :, 2]

BLUE = (r < 90) & (bl > 100) & (bl - g > 50) & (r - g < 80)          # indigo plot borders
PINK = (r > 235) & (r - g > 8) & (r - bl > 8) & (g > 200) & (b > 200)
RED = (r > 110) & (r - g > 45) & (r - bl > 40)
DARK = (r < 150) & (g < 150) & (b < 150)
GRAY = (np.abs(r - g) < 14) & (np.abs(g - bl) < 14) & (r > 175) & (r < 235)


def runs(idx, gap=3):
    out, prev = [], None
    for i in idx:
        if prev is None or i - prev > gap:
            out.append([int(i), int(i)])
        else:
            out[-1][1] = int(i)
        prev = i
    return out


def box_of(mask, region):
    x0, y0, x1, y1 = region
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return [int(x0 + xs.min()), int(y0 + ys.min()), int(x0 + xs.max()), int(y0 + ys.max())]


def segments(mask, axis, region, frac=0.25):
    """Long runs of mask along axis=0 (rows) or 1 (cols) inside region."""
    x0, y0, x1, y1 = region
    sub = mask[y0:y1, x0:x1]
    counts = sub.sum(axis=axis)
    span = sub.shape[1 - axis]
    idx = np.where(counts > span * frac)[0]
    return [[int(v + (x0 if axis == 1 else y0)), int(v + (x0 if axis == 1 else y0))]
            for v in runs(idx, gap=1)]


report = {"frame_size": [W, H], "panels": {}}

# ---- formula boxes: pink fill runs in the two row bands -----------------------
FORM = {
    "TL": (100, 40, 460, 112),
    "TR": (538, 40, 780, 112),
    "BL": (88, 280, 435, 347),
    "BR": (580, 280, 820, 343),
}
for name, reg in FORM.items():
    x0, y0, x1, y1 = reg
    sub = PINK[y0:y1, x0:x1]
    cols = sub.sum(axis=0)
    rows = sub.sum(axis=1)
    xs = np.where(cols > (y1 - y0) * 0.30)[0]
    ys = np.where(rows > (x1 - x0) * 0.15)[0]
    report["panels"].setdefault(name, {})["formula_box"] = {
        "x": [int(x0 + xs.min()), int(x0 + xs.max())],
        "y": [int(y0 + ys.min()), int(y0 + ys.max())],
    }

# ---- graph frames: blue border bbox -------------------------------------------
GRAPHS = {
    "TL": (118, 105, 404, 276),
    "TR": (560, 105, 846, 278),
    "BL": (118, 342, 404, 512),
    "BR": (560, 342, 846, 512),
}
for name, reg in GRAPHS.items():
    p = report["panels"].setdefault(name, {})
    b = box_of(BLUE, reg)
    p["graph_box"] = b
    x0, y0, x1, y1 = b
    interior = (x0 + 3, y0 + 3, x1 - 2, y1 - 2)
    p["interior"] = list(interior)

    # gridlines (light gray) inside interior
    gi0, gi1 = interior[1], interior[3]
    gx0, gx1 = interior[0], interior[2]
    grow = GRAY[gi0:gi1, gx0:gx1].sum(axis=1)
    gcol = GRAY[gi0:gi1, gx0:gx1].sum(axis=0)
    w = gx1 - gx0
    h = gi1 - gi0
    p["grid_rows"] = [[int(v + gi0), int(c)] for v, c in zip(*np.unique(np.where(grow > w * 0.5)[0], return_counts=True))] if False else \
        [[int(v + gi0)] for v in np.where(grow > w * 0.5)[0]]
    p["grid_cols"] = [[int(v + gx0)] for v in np.where(gcol > h * 0.5)[0]]

    # dark axis lines
    drow = DARK[gi0:gi1, gx0:gx1].sum(axis=1)
    dcol = DARK[gi0:gi1, gx0:gx1].sum(axis=0)
    p["axis_rows"] = [[int(v + gi0), int(c)] for v, c in zip(np.where(drow > w * 0.25)[0], drow[drow > w * 0.25])]
    p["axis_cols"] = [[int(v + gx0), int(c)] for v, c in zip(np.where(dcol > h * 0.25)[0], dcol[dcol > h * 0.25])]

    # red curve trace: per column min/max y within interior
    sub = RED[gi0:gi1, gx0:gx1]
    ys, xs = np.where(sub)
    if len(xs):
        p["red_bbox"] = [int(gx0 + xs.min()), int(gi0 + ys.min()), int(gx0 + xs.max()), int(gi0 + ys.max())]
        trace = []
        for frac in np.arange(0.0, 1.001, 0.05):
            cx = int(frac * (gx1 - gx0 - 1))
            col = np.where(sub[:, cx])[0]
            if len(col):
                trace.append([round(float(frac), 2), int(gx0 + cx), int(gi0 + col.min()), int(gi0 + col.max())])
        p["red_trace"] = trace

    # blue/green/orange curve traces (ELU family) - saturated non-red colors
    for cname, cmask in [
        ("blue_curve", (bl > 140) & (bl - r > 60) & (bl - g > 50)),
        ("orange_curve", (r > 150) & (g > 90) & (g < 190) & (r - bl > 70)),
        ("green_curve", (g > 110) & (g - r > 50) & (g - bl > 50)),
    ]:
        cm = cmask[gi0:gi1, gx0:gx1]
        cy, cx = np.where(cm)
        if len(cx) > 8:
            p[cname] = [int(gx0 + cx.min()), int(gi0 + cy.min()), int(gx0 + cx.max()), int(gi0 + cy.max())]

    # black text blobs (tick labels / axis labels / legend) as connected runs
    dm = DARK[gi0:gi1, gx0:gx1]
    rowsum = dm.sum(axis=1)
    rowbands = runs(np.where(rowsum > 0)[0], gap=2)
    blobs = []
    for rb in rowbands:
        band = dm[rb[0]:rb[1] + 1]
        colsum = band.sum(axis=0)
        colidx = np.where(colsum > 0)[0]
        for cb in runs(colidx, gap=4):
            if rb[1] - rb[0] >= 2 and cb[1] - cb[0] >= 1:
                blobs.append({
                    "x": [int(gx0 + cb[0]), int(gx0 + cb[1])],
                    "y": [int(gi0 + rb[0]), int(gi0 + rb[1])],
                })
    p["text_blobs"] = blobs

# ---- slide badge (yellow) ------------------------------------------------------
YEL = (r > 190) & (g > 170) & (bl < 160) & (r - bl > 60)
b = box_of(YEL, (850, 30, 960, 120))
report["badge_yellow_bbox"] = b

# ---- black letterbox bar ------------------------------------------------------
blk = (r < 60) & (g < 60) & (b < 60)
b = box_of(blk, (0, 505, W, H))
report["bottom_black_bar"] = b

# ---- outer red content frame of the ORIGINAL ----------------------------------
redf = RED & ~PINK
b = box_of(redf, (0, 0, W, 540))
report["original_red_frame_bbox"] = b
report["original_red_frame_cols"] = [int(v) for v in np.where(redf.sum(axis=0) > 200)[0]]
report["original_red_frame_rows"] = [int(v) for v in np.where(redf.sum(axis=1) > 200)[0]]

with open(OUT, "w") as f:
    json.dump(report, f, indent=1)
print(json.dumps(report, indent=1))
