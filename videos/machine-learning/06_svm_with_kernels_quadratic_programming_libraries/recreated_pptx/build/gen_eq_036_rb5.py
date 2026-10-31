#!/usr/bin/env python3
"""Wave-rb5: re-render ONLY the bottom class-of-vector line as three segments so the
[W^T Z]^2 term carries the green highlight the original shows (judge MINOR).
Copies the rb4 manifest and swaps in s36rb5_cls_bot (centered on the peach strip).
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
BLACK = "000000"


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


def fit(segs, target_w_in, max_h_in):
    ref, _ = compose(segs, 20.0)
    rw, rh = ref.shape[1] / DPI, ref.shape[0] / DPI
    pt = 20.0 * min(target_w_in / rw, max_h_in / rh, 30.0 / 20.0)
    pt = max(6.0, pt)
    c, boxes = compose(segs, pt)
    return c, boxes, pt, c.shape[1] / DPI, c.shape[0] / DPI


SEGS = [
    ["pre", BLACK, r"\mathrm{Class\ of\ vector}\ Z\ \mathrm{is}\ \mathrm{sign}("],
    ["mid", BLACK, r"[W^T Z]^2"],
    ["post", BLACK, r" + b)"],
]


def main():
    m = json.load(open(os.path.join(EQ36, "eq_s36rb4_manifest.json")))
    canvas, boxes, pt, w_in, h_in = fit(SEGS, 9.0, 0.28)
    name = "s36rb5_cls_bot"
    Image.fromarray(canvas).save(os.path.join(EQ36, name + ".png"))
    cx = 6.665  # peach strip center x (in)
    entry = {
        "image": name + ".png",
        "x_in": round(cx - w_in / 2, 4),
        "cy_in": 6.30,  # peach strip [0.12,0.815,0.88,0.86] center
        "w_in": round(w_in, 5),
        "h_in": round(h_in, 5),
        "fontsize_pt": round(pt, 3),
        "segments": boxes,
        "highlights": ["mid"],
    }
    with open(os.path.join(EQ36, name + ".png.json"), "w") as fh:
        json.dump(entry, fh, indent=1)
    m["s36rb5_cls_bot"] = entry
    m["s36rb4_cls_bot"]["cy_in"] = 3.30  # top peach strip [0.12,0.41,0.88,0.45] center
    with open(os.path.join(EQ36, "eq_s36rb5_manifest.json"), "w") as fh:
        json.dump(m, fh, indent=1)
    print(name, round(w_in, 3), "x", round(h_in, 3), "@", round(pt, 2), "pt")


if __name__ == "__main__":
    main()
