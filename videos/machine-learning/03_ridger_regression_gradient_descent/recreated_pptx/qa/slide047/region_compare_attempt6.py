#!/usr/bin/env python3
"""Slide 047 attempt 6: region-level ink-bbox comparison, render_10 vs original.
Frame-space (960x540) bboxes; render scaled by 540/1125. Tolerance note: font
substitution (Times->Liberation Serif) shifts glyph widths ~1-2px; structural
misplacement would show as >4px deltas."""
import numpy as np
from PIL import Image

R = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide047/render_10.png"
).convert("RGB")).astype(int)
O = np.asarray(Image.open(
    "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_047.jpg"
).convert("RGB")).astype(int)
S = R.shape[0] / 540.0
rl, ol = R.mean(axis=2), O.mean(axis=2)

regions = {
    "TL header":      (84, 60, 222, 74),
    "TL digits":      (86, 76, 220, 108),
    "TL class row":   (84, 112, 222, 126),
    "InitialW label": (264, 74, 356, 88),
    "W vector":       (320, 56, 356, 108),
    "Step eta":       (362, 64, 440, 82),
    "Check classes":  (496, 76, 586, 92),
    "legend":         (236, 108, 514, 126),
    "Z header":       (594, 62, 662, 78),
    "Z digits":       (594, 78, 662, 112),
    "aug title":      (78, 144, 246, 162),
    "aug header":     (88, 162, 224, 178),
    "aug digits":     (88, 176, 224, 228),
    "aug class":      (88, 228, 222, 246),
    "box1 label":     (280, 156, 330, 180),
    "box1 rowvec":    (332, 146, 380, 160),
    "box1 stack":     (384, 148, 410, 192),
    "box1 result":    (410, 158, 444, 178),
    "box1 sign":      (502, 158, 596, 176),
    "box1 class":     (660, 156, 704, 178),
    "box2 label":     (280, 221, 330, 245),
    "box3 result":    (410, 283, 444, 303),
    "box3 sign":      (502, 283, 596, 301),
    "button":         (78, 276, 240, 306),
}


def bbox(a, S, region, thr=170):
    x0, y0, x1, y1 = region
    X0, Y0, X1, Y1 = int(round(x0 * S)), int(round(y0 * S)), int(round(x1 * S)), int(round(y1 * S))
    sub = a[Y0:Y1, X0:X1]
    m = sub < thr
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (x0 + xs.min() / S, y0 + ys.min() / S, x0 + xs.max() / S, y0 + ys.max() / S)


print(f"{'region':16s} {'orig x0..x1 y0..y1':30s} {'render x0..x1 y0..y1':30s} dx0 dx1 dy0 dy1  ink_o ink_r")
for name, reg in regions.items():
    bo = bbox(ol, 1.0, reg)
    br = bbox(rl, S, reg)
    if bo is None or br is None:
        print(f"{name:16s} MISSING INK  orig={bo} render={br}")
        continue
    d = (br[0] - bo[0], br[2] - bo[2], br[1] - bo[1], br[3] - bo[3])
    flag = "  <-- CHECK" if max(abs(d[0]), abs(d[1]), abs(d[2]), abs(d[3])) > 4 else ""
    print(f"{name:16s} [{bo[0]:6.1f}..{bo[2]:6.1f}] [{bo[1]:6.1f}..{bo[3]:6.1f}] "
          f"[{br[0]:6.1f}..{br[2]:6.1f}] [{br[1]:6.1f}..{br[3]:6.1f}] "
          f"{d[0]:+5.1f} {d[1]:+5.1f} {d[2]:+5.1f} {d[3]:+5.1f}{flag}")
