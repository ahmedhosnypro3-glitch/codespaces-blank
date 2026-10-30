#!/usr/bin/env python3
r"""PIL re-measure / pre-adjudication helper for slide 015 attempt 3.

Compares the original frame (960x540, 1px=1pt) against a given render
(2001x1125, scale = width/960) element by element, printing each element's ink
bbox and the width/height ratio.  Used to pre-adjudicate judge findings before
touching the build, and to prove render_2 vs render_3 equivalence.

Usage: readjudicate_015.py [render_path]
"""
import os
import sys

import numpy as np
from PIL import Image

D = "/worksp""aces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

# (label, y0, y1, x0, x1) - window must sit INSIDE the element so the element's
# own border is not measured as ink
WINDOWS = [
    ("title", 66, 86, 122, 850),
    ("redsentence", 294, 318, 210, 706),
    ("Remember", 277, 292, 788, 860),
    ("eq1_l1", 104, 152, 95, 795),
    ("eq1_l2", 163, 211, 95, 765),
    ("eq1_l3", 217, 264, 95, 656),
    ("redbox_eq", 278, 302, 78, 208),
    ("peach_eq", 295, 328, 788, 892),
    ("deriv_l1", 350, 403, 76, 655),
    ("deriv_l2", 416, 468, 76, 500),
    # normal sits left of the green box; solution inside it
    ("normal", 482, 510, 226, 545),
    ("solution", 477, 511, 552, 882),
]


def main():
    rend = sys.argv[1] if len(sys.argv) > 1 else f"{D}/recreated_pptx/qa/slide_015/render_3.png"
    o = np.asarray(Image.open(f"{D}/unique_slides/slide_015.jpg")).astype(int).mean(axis=2)
    r = np.asarray(Image.open(rend).convert("L")).astype(int)
    F = r.shape[1] / 960.0
    print(f"original {o.shape} render {r.shape} scale {F:.4f}\n")
    for label, y0, y1, x0, x1 in WINDOWS:
        om = o[y0:y1 + 1, x0:x1 + 1] < 150
        rm = r[int(y0 * F):int(y1 * F), int(x0 * F):int(x1 * F)] < 150
        if not om.any() or not rm.any():
            print(f"{label:13s} INK MISSING orig={om.any()} rend={rm.any()}")
            continue
        oy, ox = np.where(om)
        ry, rx = np.where(rm)
        ow = int(ox.max() - ox.min() + 1)
        oh = int(oy.max() - oy.min() + 1)
        rw = (x0 + rx.max() / F) - (x0 + rx.min() / F) + 1
        rh = (y0 + ry.max() / F) - (y0 + ry.min() / F) + 1
        print(f"{label:13s} orig x{x0 + ox.min()}..{x0 + ox.max()} y{y0 + oy.min()}..{y0 + oy.max()} "
              f"({ow}x{oh}) | rend x{x0 + rx.min() / F:.0f}..{x0 + rx.max() / F:.0f} "
              f"y{y0 + ry.min() / F:.0f}..{y0 + ry.max() / F:.0f} ({rw:.0f}x{rh:.0f}) "
              f"| w={rw / ow:.2f} h={rh / oh:.2f}")


if __name__ == "__main__":
    main()
