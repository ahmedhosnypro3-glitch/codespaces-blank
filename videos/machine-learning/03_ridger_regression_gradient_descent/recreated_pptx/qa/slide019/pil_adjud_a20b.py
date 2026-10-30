#!/usr/bin/env python3
"""Attempt-20 disputed-window ground truth: classify ink px into named color
classes (nearest-reference), print counts + bboxes + sample px per class.
Windows chosen to EXCLUDE known neighbors (arrow, rules) where possible."""
from PIL import Image
import numpy as np

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_20.png"
O = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
ri = Image.open(R).convert("RGB"); oi = Image.open(O).convert("RGB")
ra = np.asarray(ri).astype(int); oa = np.asarray(oi).astype(int)
RS = ri.size[0] / 960.0

def cf(a, x0, y0, x1, y1, s):
    return a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]

CLASSES = {
    "BLACK":  (40, 40, 40),
    "GRAY":   (119, 119, 119),
    "RED":    (192, 0, 0),
    "MAROON": (139, 58, 58),
    "BLUE":   (60, 90, 200),
    "PURPLE": (115, 106, 184),
}

def classify(c, ink_t=500):
    ink = c.sum(axis=2) < ink_t
    out = {}
    ys, xs = np.nonzero(ink)
    if not len(xs):
        return {k: (0, None, []) for k in CLASSES}
    px = c[ys, xs]
    for name, ref in CLASSES.items():
        d = np.abs(px - np.array(ref)).sum(axis=1)
        sel = d < 150
        n = int(sel.sum())
        if n:
            cys, cxs = ys[sel], xs[sel]
            bb = (cxs.min(), cys.min(), cxs.max(), cys.max())
            best = np.argsort(d[sel])[:3]
            samp = px[sel][best]
            out[name] = (n, bb, [tuple(int(v) for v in p) for p in samp])
        else:
            out[name] = (0, None, [])
    return out

def report(tag, a, s, x0, y0, x1, y1):
    c = cf(a, x0, y0, x1, y1, s)
    print(f"  [{tag}]")
    for name, (n, bb, samp) in classify(c).items():
        if n:
            bbs = (f"x {x0+bb[0]/s:.1f}..{x0+bb[2]/s:.1f} y {y0+bb[1]/s:.1f}..{y0+bb[3]/s:.1f}") if bb else ""
            print(f"    {name:7s} n={n:5d}  {bbs}  ref-samples {samp}")

def both(x0, y0, x1, y1, label):
    print(f"=== {label} (x{x0}..{x1} y{y0}..{y1}) ===")
    report("R", ra, RS, x0, y0, x1, y1)
    report("O", oa, 1.0, x0, y0, x1, y1)

# 1. x1 label row (above arrow top y244.5)
both(196, 226, 290, 244, "x1 label row")
# 2. x2 label row (right of arrow right edge 233.8)
both(236, 246, 290, 264, "x2 label row (right of arrow)")
# 3. y label row (below x2)
both(196, 264, 290, 282, "y label row")
# 4. norm text full
both(126, 258, 215, 292, "norm text zone")
# 5. outlier digits rows
both(78, 203, 122, 222, "outlier row1")
both(78, 312, 122, 335, "outlier row2")
both(78, 422, 122, 445, "outlier row3")
# 6. value col1 rows (NO REG table)
both(264, 203, 306, 224, "value col1 row1")
both(264, 313, 306, 334, "value col1 row2")
both(264, 423, 306, 444, "value col1 row3")
