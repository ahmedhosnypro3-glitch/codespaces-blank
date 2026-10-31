#!/usr/bin/env python3
"""Wave-rb2 segmented 2-D equation PNGs for slides 036 and 037.

Content comes ONLY from qa/reanalysis2/slide_03{6,7}_analysis.txt section 8
(verbatim strings, rendered as professional 2-D mathtext). Each equation is a
list of [label, color, latex] segments composed on a shared baseline at 600
dpi; the sibling JSON records the box (spec coords in inches) and each
segment's pixel bbox so the build script can place highlight rects exactly
over the marked terms. Assets use fresh s36rb2_* / s37rb2_* names; nothing
existing is overwritten.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

BUILD = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BUILD)
from render_eq_multi import render_segment, DPI, PAD_PX

EQ36 = os.path.join(BUILD, "eq_036")
EQ37 = os.path.join(BUILD, "eq_037")

BLUE, RED, BLACK = "0000CC", "FF0000", "000000"
IN_X, IN_Y = 13.33, 7.5


def compose(segs, fontsize):
    rendered = [render_segment(latex, "#" + color, fontsize) for _, color, latex in segs]
    max_b = max(b for _, b in rendered)
    heights = [a.shape[0] for a, _ in rendered]
    h = max_b + max(hh - b for (_, b), hh in zip(rendered, heights)) + PAD_PX
    w = sum(a.shape[1] for a, _ in rendered) + 2 * PAD_PX
    canvas = np.zeros((h, w, 4), dtype=np.uint8)
    boxes = {}
    x = PAD_PX
    for (arr, b), (label, _, _) in zip(rendered, segs):
        y = max_b - b
        canvas[y:y + arr.shape[0], x:x + arr.shape[1]] = arr
        boxes[label] = [int(x), int(x + arr.shape[1]), int(y), int(y + arr.shape[0])]
        x += arr.shape[1]
    return canvas, boxes


def fit(segs, box, size0=20.0):
    """Largest font size whose composed image fits inside the spec box."""
    x0, y0, x1, y1 = box
    maxw, maxh = (x1 - x0) * IN_X, (y1 - y0) * IN_Y
    c0, _ = compose(segs, size0)
    pt = size0 * min(maxw / (c0.shape[1] / DPI), maxh / (c0.shape[0] / DPI))
    pt = max(6.0, min(30.0, pt * 0.98))
    for _ in range(6):
        c, boxes = compose(segs, pt)
        if c.shape[1] / DPI <= maxw and c.shape[0] / DPI <= maxh:
            return c, boxes, pt
        pt *= 0.94
    return compose(segs, pt)[0], compose(segs, pt)[1], pt


def lag(tail):
    return [
        ["ld", BLUE, r"\mathcal{L}_D(\alpha)"],
        ["eq", BLACK, "="],
        ["suma", BLACK, r"\sum_{i=1}^{N}\alpha_i"],
        ["minus", BLACK, "-"],
        ["half", BLACK, r"\frac{1}{2}"],
        ["sumij", BLACK, r"\sum_{i=1}^{N}\sum_{j=1}^{N}\alpha_i\alpha_j y_i y_j"],
        ["tail", BLACK, tail],
    ]


def w_form():
    return [["w", BLUE, "w"], ["eq", BLACK, "="],
            ["sum", BLACK, r"\sum_{i=1}^{N}\alpha_i y_i X_i"]]


def b_form(t1, t2):
    return [
        ["b", BLUE, "b"], ["eq", BLACK, "="], ["minus", BLACK, "-"],
        ["half", BLACK, r"\frac{1}{2}"], ["lb", BLACK, "["],
        ["max", BLACK, r"\max_{i:y_i=-1}"], ["t1", BLACK, t1],
        ["plus", BLACK, "+"],
        ["min", BLACK, r"\min_{i:y_i=+1}"], ["t2", BLACK, t2],
        ["rb", BLACK, "]"],
    ]


# name, dir, segments, spec box [x0,y0,x1,y1], highlight labels
JOBS = [
    ("s36rb2_lag_top", EQ36, lag(r"X_i^T X_j"), [0.08, 0.24, 0.92, 0.31], ["tail"]),
    ("s36rb2_w", EQ36, w_form(), [0.08, 0.32, 0.35, 0.39], []),
    ("s36rb2_b_top", EQ36, b_form(r"W^T X_i", r"W^T X_i"), [0.38, 0.32, 0.92, 0.39], []),
    ("s36rb2_cls_top", EQ36,
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(W^T Z + b)"]],
     [0.12, 0.47, 0.88, 0.51], []),
    ("s36rb2_kern", EQ36, [["k", RED, r"K(a,b) = [a^T b]^2"]], [0.59, 0.48, 0.71, 0.54], []),
    ("s36rb2_lag_bot", EQ36, lag(r"[X_i^T X_j]^2"), [0.08, 0.61, 0.92, 0.70], ["tail"]),
    ("s36rb2_b_bot", EQ36, b_form(r"[W_i^T X_j]^2", r"[W_i^T X_j]^2"),
     [0.38, 0.71, 0.92, 0.78], []),
    ("s36rb2_cls_bot", EQ36,
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}([W^T Z]^2 + b)"]],
     [0.12, 0.83, 0.88, 0.87], []),
    ("s37rb2_lag_orig", EQ37, lag(r"X_i^T X_j"), [0.1, 0.2, 0.9, 0.28], ["tail"]),
    ("s37rb2_w", EQ37, w_form(), [0.1, 0.3, 0.3, 0.35], ["sum"]),
    ("s37rb2_b_orig", EQ37, b_form(r"w^T X_i", r"w^T X_i"), [0.35, 0.3, 0.9, 0.35], ["t1", "t2"]),
    ("s37rb2_cls_orig", EQ37,
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(w^T Z + b)"]],
     [0.2, 0.4, 0.8, 0.45], []),
    ("s37rb2_kernel", EQ37, [["k", BLACK, r"K(a,b) = [a^T b + 1]^d"]], [0.4, 0.5, 0.75, 0.55],
     ["k"]),
    ("s37rb2_lag_kern", EQ37, lag(r"[X_i^T X_j + 1]^d"), [0.1, 0.64, 0.9, 0.72], ["tail"]),
    ("s37rb2_b_kern", EQ37, b_form(r"[w^T X_i + 1]^d", r"[w^T X_i + 1]^d"),
     [0.35, 0.73, 0.9, 0.78], ["t1", "t2"]),
    ("s37rb2_cls_kern", EQ37,
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}([w^T Z + 1]^d + b)"]],
     [0.2, 0.83, 0.8, 0.88], []),
]


def main():
    manifest = {}
    for name, eqdir, segs, box, hl in JOBS:
        os.makedirs(eqdir, exist_ok=True)
        canvas, boxes, pt = fit(segs, box)
        out = os.path.join(eqdir, name + ".png")
        Image.fromarray(canvas).save(out)
        x0, y0, x1, y1 = box
        entry = {
            "image": name + ".png",
            "box": [round(x0 * IN_X, 4), round(y0 * IN_Y, 4),
                    round((x1 - x0) * IN_X, 4), round((y1 - y0) * IN_Y, 4)],
            "w_in": round(canvas.shape[1] / DPI, 5),
            "h_in": round(canvas.shape[0] / DPI, 5),
            "fontsize_pt": round(pt, 3),
            "segments": boxes,
            "highlights": hl,
        }
        with open(out + ".json", "w") as fh:
            json.dump(entry, fh, indent=1)
        manifest[name] = entry
        print(name, entry["w_in"], "x", entry["h_in"], "in @", entry["fontsize_pt"], "pt")
    for eqdir, fname in ((EQ36, "eq_s36rb2_manifest.json"), (EQ37, "eq_s37rb2_manifest.json")):
        sub = {k: v for k, v in manifest.items() if os.path.dirname(os.path.join(eqdir, v["image"])) == eqdir}
        with open(os.path.join(eqdir, fname), "w") as fh:
            json.dump(sub, fh, indent=1)


if __name__ == "__main__":
    main()
