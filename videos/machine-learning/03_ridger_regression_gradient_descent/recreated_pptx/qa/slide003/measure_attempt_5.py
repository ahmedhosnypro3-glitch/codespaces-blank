#!/usr/bin/env python3
"""Slide 003 closed-loop measurement: render_5.png vs the original frame.

Prints ink-bbox comparisons for every measured region (frame px, 960x540).
Usage: python3 measure_003.py [render.png]
"""
import sys
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
RENDER = sys.argv[1] if len(sys.argv) > 1 else \
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_5.png"

# frame-px ink bboxes measured on the ORIGINAL (2026-10-23)
EXPECT = {
    "title":            (82, 68, 832, 90),
    "n_training":       (81, 177, 272, 199),
    "top_matrix_box":   (271, 107, 596, 301),
    "remember_box":     (649, 153, 874, 221),
    "ingeneral_box":    (659, 268, 850, 294),
    "bottom_left_box":  (79, 323, 533, 517),
    "bottom_right_box": (572, 323, 752, 517),
    "arrow":            (532, 330, 573, 409),
}

def load(path, frame_h=540):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return im, im.shape[0] / frame_h

def ink_mask(a):
    gray = (np.abs(a[:, :, 0] - 233) < 14) & (np.abs(a[:, :, 1] - 233) < 14) & \
           (np.abs(a[:, :, 2] - 231) < 16)
    return ~gray

def bbox(mask, x0, y0, x1, y1, s):
    sub = mask[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (x0 + xs.min() / s, y0 + ys.min() / s, x0 + xs.max() / s, y0 + ys.max() / s)

print(f"render: {RENDER}")
a, s = load(RENDER)
ao, so = load(ORIG)
print(f"render scale {s:.4f}  original scale {so:.4f}")

mo, mr = ink_mask(ao), ink_mask(a)
print(f"\n{'region':18s} {'expected (frame px)':28s} {'render ink bbox':28s} status")
for name, (ex0, ey0, ex1, ey1) in EXPECT.items():
    got = bbox(mr, ex0 - 12, ey0 - 12, ex1 + 12, ey1 + 12, s)
    # expected self-derived from the original on the SAME window
    exp = bbox(mo, ex0 - 12, ey0 - 12, ex1 + 12, ey1 + 12, so)
    if got is None:
        print(f"{name:18s} {str(exp):28s} {'NO INK':28s} FAIL")
    else:
        g = tuple(round(v, 1) for v in got)
        e = tuple(round(v, 1) for v in exp) if exp else ("?", "?", "?", "?")
        drift = max(abs(g[i] - e[i]) for i in range(4)) if exp else 999
        print(f"{name:18s} {str(e):28s} {str(g):28s} {'ok' if drift <= 6 else 'DRIFT ' + str(round(drift, 1))}")
