#!/usr/bin/env python3
"""Forensic measurement of unique_slides/slide_041.jpg (960x540, 1px = 1pt).
Every geometry/colour used by build/slide_041.js is derived here from the frame.
Prints a report; saves qa/slide041/measurements.json.
"""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

FRAME = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_041.jpg"
OUT   = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide041/measurements.json"
im = Image.open(FRAME).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
R = {"frame": [W, H], "notes": []}

def rgb(x, y):
    return tuple(int(v) for v in a[y, x])

def runs(idx, vals, gap=1):
    """group sorted indices into runs, merging gaps <= gap"""
    out, cur = [], []
    for i in idx:
        if cur and i - cur[-1] > gap + 1:
            out.append((cur[0], cur[-1])); cur = []
        cur.append(i)
    if cur: out.append((cur[0], cur[-1]))
    return out

def ink_runs(y0, y1, x0, x1, thr=600, axis=0, gap=1):
    sub = a[y0:y1, x0:x1]
    dark = sub.sum(axis=2) < thr
    prof = dark.sum(axis=axis)
    idx = np.where(prof > 0)[0]
    return [(int(s + x0), int(e + x0)) for s, e in runs(idx, None, gap)]

def median_rgb(x0, y0, x1, y1):
    sub = a[y0:y1, x0:x1].reshape(-1, 3)
    if not len(sub): return None
    return tuple(int(v) for v in np.median(sub, axis=0))

# ---------------------------------------------------------------- 1. panel
panel_fill_samples = [
    median_rgb(300, 60, 450, 70),
    median_rgb(300, 120, 450, 126),
    median_rgb(640, 115, 680, 126),
    median_rgb(100, 115, 200, 126),
]
R["panel"] = {
    "border_left_cols": ink_runs(60, 120, 60, 80, 600, axis=1, gap=2),
    "border_right_cols": ink_runs(60, 120, 705, 735, 600, axis=1, gap=2),
    "border_top_rows": ink_runs(46, 62, 200, 500, 600, axis=0, gap=2),
    "border_bottom_rows": ink_runs(122, 136, 200, 500, 600, axis=0, gap=2),
    "fill_median": median_rgb(300, 58, 500, 110),
    "fill_samples": panel_fill_samples,
    "border_core": median_rgb(69, 89, 70, 91),
}
# ---------------------------------------------------------------- 2. house panel context (sanity)
R["house_panel_left_px"] = ink_runs(300, 340, 50, 70, 600, axis=1, gap=2)
R["house_panel_right_px"] = ink_runs(300, 340, 890, 910, 600, axis=1, gap=2)

# ---------------------------------------------------------------- 3. text rows (generic profiler)
def row_bands(y0, y1, x0, x1, thr=600):
    sub = a[y0:y1, x0:x1]
    dark = sub.sum(axis=2) < thr
    prof = dark.sum(axis=1)
    out = []
    cur = []
    for i, c in enumerate(prof):
        if c > 0:
            if cur and i - cur[-1] > 3: out.append((y0 + cur[0], y0 + cur[-1])); cur = []
            cur.append(i)
        else:
            if cur: out.append((y0 + cur[0], y0 + cur[-1])); cur = []
    if cur: out.append((y0 + cur[0], y0 + cur[-1]))
    return out

def col_runs(y0, y1, x0, x1, thr=600, gap=6):
    sub = a[y0:y1, x0:x1]
    dark = sub.sum(axis=2) < thr
    prof = dark.sum(axis=0)
    idx = np.where(prof > 0)[0]
    return [(int(s + x0), int(e + x0)) for s, e in runs(idx, None, gap)]

R["panel_row_bands"] = row_bands(56, 128, 66, 722)

# ---------------------------------------------------------------- 4. table (left zone)
TBL = {}
# column ink groups per row band (tight threshold to separate digits)
TBL["header_groups"] = col_runs(63, 73, 88, 216, thr=560, gap=4)
TBL["row1_groups"] = col_runs(79, 91, 84, 220, thr=560, gap=4)
TBL["row2_groups"] = col_runs(95, 107, 84, 220, thr=560, gap=4)
TBL["label_groups"] = col_runs(111, 126, 84, 220, thr=560, gap=6)
# paren detection: vertical strokes spanning both digit rows
def vert_strokes(y0, y1, x0, x1, minrows):
    sub = a[y0:y1, x0:x1]
    dark = sub.sum(axis=2) < 620
    prof = dark.sum(axis=0)
    return [(int(i + x0), int(c)) for i, c in enumerate(prof) if c >= minrows]
TBL["vert_strokes_y79_107"] = vert_strokes(79, 108, 80, 225, 20)
TBL["vert_strokes_y111_126"] = vert_strokes(111, 127, 80, 225, 10)
# paren curvature: x-centroid of the left-most stroke per row
def _clean(o):
    import math
    if isinstance(o, dict): return {k: _clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [_clean(v) for v in o]
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.floating, float)):
        return None if (isinstance(o, float) and math.isnan(o)) else float(o)
    return o

def stroke_centroid_per_row(xc, y0, y1, rad=3, thr=620):
    out = []
    for y in range(y0, y1):
        cols = [x for x in range(xc - rad, xc + rad + 1) if a[y, x].sum() < thr]
        if cols: out.append((y, sum(cols) / len(cols)))
    return out
R["table"] = TBL

# ---------------------------------------------------------------- 5. legend line
LEG = {}
LEG["row_band"] = row_bands(102, 116, 235, 520)
LEG["groups"] = col_runs(103, 114, 235, 520, thr=560, gap=5)
def color_stat(x0, y0, x1, y1):
    sub = a[y0:y1, x0:x1].reshape(-1, 3).astype(int)
    r, g, b = sub[:, 0], sub[:, 1], sub[:, 2]
    red = ((r > g + 25) & (r > b + 25) & (r > 110)).sum()
    blue = ((b > r + 30) & (b > g + 30) & (b > 110)).sum()
    green = ((g > r + 15) & (g > b + 15) & (g > 90)).sum()
    dark = ((r + g + b) < 560).sum()
    return {"red": int(red), "blue": int(blue), "green": int(green), "dark": int(dark)}
LEG["group_colors"] = {}
for (x0, x1) in LEG["groups"]:
    LEG["group_colors"][f"{x0}-{x1}"] = color_stat(x0 - 1, 104, x1 + 2, 113)
R["legend"] = LEG

# ---------------------------------------------------------------- 6. middle zone
MID = {}
MID["initial_w_ink"] = col_runs(77, 86, 260, 345, thr=560, gap=5)
MID["vec_paren_left_cols"] = ink_runs(59, 103, 328, 340, 600, axis=1, gap=2)
MID["vec_paren_right_cols"] = ink_runs(59, 103, 349, 362, 600, axis=1, gap=2)
MID["stepeta_ink"] = col_runs(64, 83, 370, 445, thr=560, gap=6)
MID["stepeta_red_count"] = color_stat(370, 64, 445, 83)
R["middle"] = MID

# ---------------------------------------------------------------- 7. right zone
RT = {}
# "Check classes of"
RT["check_classes_groups"] = col_runs(78, 89, 495, 640, thr=560, gap=6)
# Z labels row (y64..76)
RT["z_labels_band"] = row_bands(60, 80, 540, 660)
RT["z_label_groups"] = col_runs(63, 77, 540, 660, thr=560, gap=6)
# 2x3 matrix
RT["m2_vert_strokes_y83_108"] = vert_strokes(83, 109, 592, 662, 16)
RT["m2_row_bands"] = row_bands(80, 110, 590, 665)
RT["m2_row1_groups"] = col_runs(83, 95, 595, 660, thr=560, gap=4)
RT["m2_row2_groups"] = col_runs(96, 108, 595, 660, thr=560, gap=4)
R["right"] = RT

# ---------------------------------------------------------------- 8. scatter plot
PL = {}
REDM = (a[:, :, 0].astype(int) - np.maximum(a[:, :, 1], a[:, :, 2]) > 25) & (a[:, :, 0] > 110)
PL["border_left_col"] = [int(i) + 300 for i in np.where(REDM[200:450, 300:320].sum(axis=0) > 100)[0]]
PL["border_right_col"] = [int(i) + 820 for i in np.where(REDM[200:450, 820:840].sum(axis=0) > 100)[0]]
PL["border_top_row"] = [int(i) + 168 for i in np.where(REDM[168:182, 400:700].sum(axis=1) > 100)[0]]
PL["border_bottom_row"] = [int(i) + 474 for i in np.where(REDM[474:486, 400:700].sum(axis=1) > 100)[0]]
# gridlines: gray rows/cols inside interior
sub = a[180:475, 320:815]
notwhite = sub.sum(axis=2) < 690
grid_rows = [int(i + 180) for i in range(notwhite.shape[0]) if notwhite[i].sum() > 150]
grid_cols = [int(i + 320) for i in range(notwhite.shape[1]) if notwhite[:, i].sum() > 120]
PL["grid_rows"] = grid_rows
PL["grid_cols"] = grid_cols
PL["gridline_gray"] = median_rgb(500, 214, 700, 216)
PL["interior_white"] = median_rgb(400, 350, 460, 360)
# tick labels
PL["xtick_band"] = row_bands(432, 500, 300, 840, thr=600)
PL["xtick_groups"] = col_runs(438, 448, 300, 840, thr=560, gap=8)
PL["ytick_band"] = row_bands(200, 440, 285, 315, thr=600)
PL["ytick_groups"] = col_runs(200, 440, 285, 315, thr=560, gap=8)
R["plot"] = PL

# markers
MK = {}
def marker_clusters(channel_test, label):
    m = channel_test(180, 478, 315, 822)
    ys, xs = np.where(m)
    pts = sorted(set(zip(xs + 315, ys + 180)))
    clusters = []
    for p in pts:
        if clusters and abs(p[0] - clusters[-1][-1][0]) < 16 and abs(p[1] - clusters[-1][-1][1]) < 16:
            clusters[-1].append(p)
        else:
            clusters.append([p])
    out = []
    for c in clusters:
        xs_ = [p[0] for p in c]; ys_ = [p[1] for p in c]
        out.append({"cx": float(round((min(xs_) + max(xs_)) / 2, 1)), "cy": float(round((min(ys_) + max(ys_)) / 2, 1)),
                    "w": int(max(xs_) - min(xs_) + 1), "h": int(max(ys_) - min(ys_) + 1), "n": int(len(c))})
    return {label: out}
MK.update(marker_clusters(lambda y0, y1, x0, x1:
    (a[y0:y1, x0:x1, 2] > 120) & (a[y0:y1, x0:x1, 2] - a[y0:y1, x0:x1, 0] > 50) &
    (a[y0:y1, x0:x1, 2] - a[y0:y1, x0:x1, 1] > 50), "blue"))
MK.update(marker_clusters(lambda y0, y1, x0, x1:
    (a[y0:y1, x0:x1, 0] > 140) & (a[y0:y1, x0:x1, 0] - a[y0:y1, x0:x1, 1] > 50) &
    (a[y0:y1, x0:x1, 0] - a[y0:y1, x0:x1, 2] > 50), "red"))
MK.update(marker_clusters(lambda y0, y1, x0, x1:
    (a[y0:y1, x0:x1, 0] > 140) & (a[y0:y1, x0:x1, 2] > 140) &
    (a[y0:y1, x0:x1, 1] < a[y0:y1, x0:x1, 0] - 50), "magenta"))
MK["blue_core"] = median_rgb(397, 398, 400, 401)
MK["red_core"] = median_rgb(367, 368, 369, 369)
MK["magenta_core"] = median_rgb(626, 306, 628, 308)
R["markers"] = MK

# ---------------------------------------------------------------- 9. mouse artifact
white = (a[:, :, 0] > 235) & (a[:, :, 1] > 235) & (a[:, :, 2] > 235)
sub = white[60:130, 60:900]
ys, xs = np.where(sub)
R["mouse_band"] = {"y0": int(ys.min()) if len(ys) else None, "y1": int(ys.max()) if len(ys) else None,
                   "x0": int(xs.min()) if len(xs) else None, "x1": int(xs.max()) if len(xs) else None}


# ---------------------------------------------------------------- 10. DIGIT OCR
# Normalized-template read of every small digit cell: ink mask -> tight bbox ->
# resize to a fixed grid -> IoU vs Liberation Sans (Arial-metric) glyphs.
_FONTS = ["/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
          "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
          "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
def _norm(mask, n=28):
    ys, xs = np.where(mask)
    if not len(ys): return None
    m = mask[ys.min():ys.max()+1, xs.min():xs.max()+1]
    img = Image.fromarray((m*255).astype(np.uint8)).resize((n, n), Image.LANCZOS)
    return np.asarray(img) > 110
def _iou(p, q):
    return (p & q).sum() / max(1, (p | q).sum())
_TCACHE = {}
def _templates(chars):
    out = []
    for fp in _FONTS:
        for sz in (18, 20, 22, 24, 26):
            key = (fp, sz)
            if key not in _TCACHE:
                _TCACHE[key] = ImageFont.truetype(fp, sz)
            f = _TCACHE[key]
            for ch in chars:
                m = f.getmask(ch); arr = np.array(m).reshape(m.size[1], m.size[0])
                t = _norm(arr > 110)
                if t is not None: out.append((ch, t))
    return out
_TPL = _templates("0123456789")
def read_digits(y0, y1, groups, label):
    res = []
    for (gx0, gx1) in groups:
        win = a[y0:y1, gx0-1:gx1+2]
        mask = win.sum(axis=2) < 560
        # drop thin vertical paren strokes (aspect > 6 and narrow)
        ys, xs = np.where(mask)
        if not len(ys):
            res.append({"x": gx0, "char": "", "iou": 0.0}); continue
        h = ys.max()-ys.min()+1; w = xs.max()-xs.min()+1
        cand = _norm(mask)
        scores = sorted(((round(_iou(cand, t), 3), ch) for ch, t in _TPL), reverse=True)
        res.append({"x": f"{gx0}-{gx1}", "h": h, "w": w,
                    "best": scores[0][1], "iou": scores[0][0],
                    "top3": [f"{ch}:{sc}" for sc, ch in scores[:3]]})
    R["digits_" + label] = res
    return res

# table digits: strip paren columns from the group list first (handled below)
read_digits(79, 91, TBL["row1_groups"], "table_row1")
read_digits(95, 107, TBL["row2_groups"], "table_row2")
read_digits(83, 95, RT["m2_row1_groups"], "m2_row1")
read_digits(96, 108, RT["m2_row2_groups"], "m2_row2")

# class-label row colours (per group)
R["label_colors"] = {f"{gx0}-{gx1}": color_stat(gx0-1, 112, gx1+2, 125)
                     for (gx0, gx1) in TBL["label_groups"]}

with open(OUT, "w") as f:
    json.dump(_clean(R), f, indent=1)
print(json.dumps(_clean(R), indent=1))
