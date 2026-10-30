#!/usr/bin/env python3
"""Slide 049 — parenthesis probe (PIL-only, no vision calls).

Measures every parenthesis region in the ORIGINAL frame vs the CERTIFIED RENDER
(render_13) and reports structural agreement: delimiter span, bow depth
(curvature), stroke column profile, and digit-overlap. Founder reports a
"parenthesis defect" — this probe localizes which region disagrees.
"""
import numpy as np
from PIL import Image

BASE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
orig = np.array(Image.open(BASE + "/unique_slides/slide_049.jpg").convert("L"), dtype=np.uint8)
rend = np.array(Image.open(BASE + "/recreated_pptx/qa/slide049/render_13.png").convert("L"), dtype=np.uint8)
S = rend.shape[0] / orig.shape[0]  # ~2.0844

def ink(img, thr=140):
    return img < thr

# regions in FRAME coords (x0, y0, x1, y1, name)
REGIONS = [
    ( 83,  72, 222, 130, "A top-table 2-stacks (font parens)"),
    (322,  48, 432,  96, "B initial-W vector"),
    (634,  64, 706, 124, "C Z-block parens"),
    ( 86, 174, 226, 230, "D aug-table parens"),
    (372, 144, 400, 190, "E calc-row high-bracket col (row1)"),
    (712, 144, 768, 190, "F calc-row W column (row1)"),
]

def stroke_profile(mask, label):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
    # per-row leftmost/rightmost ink (delimiter = extreme strokes)
    rows = {}
    for y, x in zip(ys, xs):
        rows.setdefault(y, []).append(x)
    span = y1 - y0 + 1
    left, right = [], []
    for y in sorted(rows):
        v = rows[y]
        left.append(min(v)); right.append(max(v))
    # curvature: deviation of leftmost-ink column between thirds (top vs mid)
    n = len(left)
    t3 = left[: max(1, n // 3)]; m3 = left[n // 3: max(2, 2 * n // 3)]; b3 = left[2 * n // 3:]
    bow_left = (np.mean(t3) - np.mean(m3), np.mean(b3) - np.mean(m3))
    t3r = right[: max(1, n // 3)]; m3r = right[n // 3: max(2, 2 * n // 3)]; b3r = right[2 * n // 3:]
    bow_right = (np.mean(m3r) - np.mean(t3r), np.mean(m3r) - np.mean(b3r))
    return dict(bbox=(int(x0), int(y0), int(x1), int(y1)), span=int(span),
                bow_left=tuple(round(float(b), 2) for b in bow_left),
                bow_right=tuple(round(float(b), 2) for b in bow_right),
                n_ink=int(len(xs)), width=int(x1 - x0 + 1))

print(f"scale render/orig = {S:.4f}")
for (x0, y0, x1, y1, name) in REGIONS:
    o = orig[y0:y1 + 1, x0:x1 + 1]
    r = rend[int(y0 * S):int((y1 + 1) * S), int(x0 * S):int((x1 + 1) * S)]
    po = stroke_profile(ink(o), name + " ORIG")
    pr = stroke_profile(ink(r), name + " REND")
    print(f"\n== {name} ==")
    print("  ORIG:", po)
    print("  REND:", pr)
    if po and pr:
        # normalize render bbox to frame px
        rb = tuple(round(v / S, 1) for v in pr["bbox"])
        print(f"  REND bbox in frame px: {rb}  vs ORIG {po['bbox']}")
        print(f"  span frame px: orig {po['span']} vs render {pr['span'] / S:.1f}")
        print(f"  bow left(mid-top, mid-bot) frame px: orig {po['bow_left']} vs render {tuple(round(b / S, 1) for b in pr['bow_left'])}")
        print(f"  bow right: orig {po['bow_right']} vs render {tuple(round(b / S, 1) for b in pr['bow_right'])}")
