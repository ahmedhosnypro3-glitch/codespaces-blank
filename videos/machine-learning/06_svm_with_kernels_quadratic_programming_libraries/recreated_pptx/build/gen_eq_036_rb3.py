#!/usr/bin/env python3
"""Wave-rb3 segmented 2-D equation PNGs for slide 036.

Content ONLY from qa/reanalysis2/slide_036_analysis.txt section 8 (verbatim
strings rendered as professional 2-D mathtext at 600 dpi). Fresh s36rb3_*
names; nothing existing is overwritten. Writes eq_036/eq_s36rb3_manifest.json.
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
    c, boxes = compose(segs, pt)
    return c, boxes, pt


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


JOBS = [
    ("s36rb3_lag_top", lag(r"X_i^T X_j"), [0.08, 0.24, 0.92, 0.31], ["tail"]),
    ("s36rb3_w", w_form(), [0.08, 0.32, 0.35, 0.39], []),
    ("s36rb3_b_top", b_form(r"W^T X_i", r"W^T X_i"), [0.38, 0.32, 0.92, 0.39], []),
    ("s36rb3_cls_top",
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z \Rightarrow \mathrm{sign}(W^T Z + b)"]],
     [0.12, 0.47, 0.88, 0.51], []),
    ("s36rb3_kern", [["k", RED, r"K(a,b) = \left(a^T b\right)^2"]], [0.59, 0.48, 0.71, 0.54], []),
    ("s36rb3_lag_bot", lag(r"[X_i^T X_j]^2"), [0.08, 0.61, 0.92, 0.70], ["tail"]),
    ("s36rb3_b_bot", b_form(r"[W_i^T X_j]^2", r"[W_i^T X_j]^2"),
     [0.38, 0.71, 0.92, 0.78], []),
    ("s36rb3_cls_bot",
     [["t", BLACK, r"\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}([W^T Z]^2 + b)"]],
     [0.12, 0.83, 0.88, 0.87], []),
]


def main():
    manifest = {}
    for name, segs, box, hl in JOBS:
        canvas, boxes, pt = fit(segs, box)
        out = os.path.join(EQ36, name + ".png")
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
    with open(os.path.join(EQ36, "eq_s36rb3_manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)


if __name__ == "__main__":
    main()
