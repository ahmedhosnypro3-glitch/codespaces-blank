#!/usr/bin/env python3
"""PIL measurement of videos/machine-learning/03_ridger_regression_gradient_descent/
unique_slides/slide_005.jpg (960x540, 1px = 1pt = 1/72in) -> JSON geometry evidence
for recreated_pptx/build/slide_005.js. Banked per worker-instructions self-check law.

Method (no classifier guessing): border segments are found as long contiguous dark
runs; fills are the per-box median of a text-free interior patch; text bands are the
ink bbox of a y-band restricted to a box's x-range.
"""
import json

import numpy as np
from PIL import Image

SRC = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
       "unique_slides/slide_005.jpg")
OUT = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
       "recreated_pptx/qa/slide005/measure_slide005.json")

a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
lum = a.sum(axis=2) / 3


def med(x0, x1, y0, y1):
    return np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0).astype(int).tolist()


def dark_runs(axis, minlen):
    """axis 0: per-row horizontal runs of lum<150. axis 1: per-column vertical runs."""
    out = []
    dark = lum < 150
    for i in range(dark.shape[1 - axis]):
        idx = np.where(dark[:, i] if axis == 0 else dark[i, :])[0]
        if not len(idx):
            continue
        s = p = idx[0]
        for v in idx[1:]:
            if v - p > 3:
                if p - s + 1 >= minlen:
                    out.append((i, int(s), int(p)))
                s = v
            p = v
        if p - s + 1 >= minlen:
            out.append((i, int(s), int(p)))
    return out


def ink_band(y0, y1, x0=62, x1=898, thr=150):
    sub = lum[y0:y1, x0:x1] < thr
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    rows = sorted(set(int(v) for v in ys))
    grp, s, p = [], rows[0], rows[0]
    for v in rows[1:]:
        if v - p > 2:
            grp.append((s + y0, p + y0))
            s = v
        p = v
    grp.append((s + y0, p + y0))
    return {"x": [int(x0 + xs.min()), int(x0 + xs.max())], "rows": grp}


meas = {
    "frame": {"w": W, "h": H, "px_per_in": 72},
    "house_chrome": {
        "panel": {"x0": 54, "x1": 903, "y0": 45, "fill": "E9E9E7",
                  "measured_fill": med(120, 200, 50, 64)},
        "strokes": {"color": "C00000", "width_pt": 1,
                    "left_x": 58.5, "right_x": 901, "bottom_y": 538.5,
                    "measured_left": np.median(a[100:500, 58], axis=0).astype(int).tolist()},
        "badge": {"cx": 876, "cy": 73, "d": 35, "fill": "FDFD96",
                  "ring": "6A5ACD", "ring_pt": 2, "numeral": "5",
                  "numeral_font": "Arial", "numeral_pt": 18, "numeral_color": "333333"},
    },
    "boxes": {
        "cream_upper": {"fill": "FBFFE5", "measured": med(300, 520, 250, 268),
                        "border": "BCBEB8",
                        "x0": 72, "x1": 892, "y0": 102, "y1": 277,
                        "evidence": "left border x72 y102..277 dark 1px; right x892; "
                                    "bottom y276..277; fill median 250,253,229"},
        "cream_lower": {"fill": "FBFFE5", "measured": med(300, 520, 430, 450),
                        "border": "BCBEB8",
                        "x0": 72, "x1": 892, "y0": 358, "y1": 522,
                        "evidence": "left border x72 down to y521; right x892; "
                                    "bottom y521..522"},
        "blue_upper": {"fill": "DAEBFA", "measured": med(700, 870, 195, 210),
                       "border": "9BAAB0",
                       "x0": 676, "x1": 882, "y0": 134, "y1": 238,
                       "evidence": "top border y134..135 x676..882; bottom y237..238; "
                                   "left x676 y~170; right x881 y~150"},
        "blue_lower": {"fill": "DAEBFA", "measured": med(700, 870, 395, 412),
                       "border": "9BAAB0",
                       "x0": 656, "x1": 872, "y0": 372, "y1": 422,
                       "evidence": "top border y372 x656..872 (dark run len 217); "
                                   "bottom y~421; left x656 y395; right x872 y395"},
        "pink": {"fill": "F8CFD3", "measured": med(300, 480, 300, 320),
                 "border": "7D1B28",
                 "x0": 73, "x1": 506, "y0": 288, "y1": 343,
                 "evidence": "horizontal borders y288 and y341/342 both x73..506; "
                            "left/right borders dark red at x73 and x505..506"},
        "green_outline": {"color": "2F8F3F", "measured_ring": med(690, 878, 464, 466),
                          "fill": "CEFFE3", "measured_fill": med(700, 860, 468, 492),
                          "x0": 688, "x1": 879, "y0": 464, "y1": 498,
                          "evidence": "green ring bbox x688..879 y464..498; top stroke "
                                      "y464..467 full width 189px; bottom y495..497"},
    },
    "text_bands": {
        "title": ink_band(66, 94, 150, 815),
        "title_red_part": {"x": [162, 807]},
        "title_blue_part": {"x": [565, 619], "word": "BEST", "color": "0000FF"},
        "eq1": ink_band(106, 146, 96, 760),
        "eq2": ink_band(176, 210, 96, 800),
        "eq3": ink_band(232, 268, 96, 870),
        "eq4": ink_band(374, 416, 96, 600),
        "eq5": ink_band(460, 504, 96, 660),
        "green_eq": ink_band(462, 500, 690, 878),
        "remember1_label": ink_band(134, 152, 684, 760),
        "remember1_l1": ink_band(156, 172, 684, 876),
        "remember1_l2": ink_band(177, 192, 684, 792),
        "remember1_eq": ink_band(212, 238, 684, 878),
        "remember2_label": ink_band(374, 390, 684, 740),
        "remember2_eq": ink_band(393, 424, 684, 878),
        "pink_left": ink_band(296, 338, 78, 190),
        "pink_right": ink_band(296, 338, 190, 506),
    },
}

with open(OUT, "w") as f:
    json.dump(meas, f, indent=1)
print("wrote", OUT)
print(json.dumps(meas["boxes"], indent=1)[:900])
