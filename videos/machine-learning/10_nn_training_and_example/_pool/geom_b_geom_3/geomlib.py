"""Lane G / scope b_geom_3 — geometry closed-loop PIL verification.

Measures the ink edges of slide-specific content for slides 014,016,017,023,024 in
BOTH the LO render (2001x1125 @150dpi, private profile) and the original frame
(960x540), normalised to frame scale, and reports per-region deltas vs a ~4px@150dpi
(~2px frame scale) tolerance.

Gateway-free by design: no vision calls.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
SLIDES = ["014", "016", "017", "023", "024"]
SCOPE = "b_geom_3"
TOL_FRAME = 2.0  # ~4px at 150dpi expressed at 960x540 frame scale
TOL_RENDER = 4.0

RENDER_DIR = os.path.join(NS, "_pool", "lo_geom_b_geom_3", "out")
FRAME_W, FRAME_H = 960, 540
PPI_FRAME = 72.0  # 13.333in x 7.5in over 960x540


def ink_mask(img, thresh=14, radius=12):
    """Local-contrast ink mask: handles the non-uniform slide backgrounds."""
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    bg = np.asarray(img.convert("RGB").filter(ImageFilter.GaussianBlur(radius))).astype(np.int16)
    d = np.abs(a - bg).max(axis=2)
    m = d > thresh
    return m


def ranges(vals, min_len=1):
    """Collapse a 0/1 array into contiguous (start, end) inclusive ranges."""
    out = []
    s = None
    for i, v in enumerate(vals):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if i - s >= min_len:
                out.append((s, i - 1))
            s = None
    if s is not None and len(vals) - s >= min_len:
        out.append((s, len(vals) - 1))
    return out


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def bbox_in(mask, y0, y1, x0, x1):
    sub = np.zeros_like(mask)
    sub[y0:y1 + 1, x0:x1 + 1] = mask[y0:y1 + 1, x0:x1 + 1]
    return bbox(sub)


def yellow_bbox(a):
    """House badge colour FFF9C4-ish; tolerant to JPEG."""
    r, g, b = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
    m = (r > 225) & (g > 220) & (b > 150) & (b < 225) & (r - b > 45) & (g - b > 45)
    return bbox(m)


def house_chrome_exclusion(shape):
    """Render-scale exclusion of the house chrome: red frame ring @0.15in inset + badge."""
    H, W = shape
    inset = int(round(0.15 * 150))
    band = 8
    ex = np.zeros((H, W), bool)
    for x in range(W):
        for y in list(range(max(0, inset - band), min(H, inset + band + 1))) + \
                 list(range(max(0, H - 1 - inset - band), min(H, H - inset + band + 1))):
            ex[y, x] = True
    for y in range(H):
        for x in list(range(max(0, inset - band), min(W, inset + band + 1))) + \
                 list(range(max(0, W - 1 - inset - band), min(W, W - inset + band + 1))):
            ex[y, x] = True
    # badge: x=12.48..12.98in, y=0.30..0.80in at 150dpi
    bx0, bx1 = int(12.40 * 150), int(13.06 * 150)
    by0, by1 = int(0.22 * 150), int(0.88 * 150)
    ex[by0:by1, bx0:bx1] = True
    return ex


def orig_chrome_exclusion(shape, m):
    """Original-frame exclusion: its own outer border ring + its own yellow badge."""
    H, W = shape
    ex = np.zeros((H, W), bool)
    rows = m.sum(1) > W * 0.75
    cols = m.sum(0) > H * 0.75
    band = 8
    for y in range(H):
        if rows[y]:
            ex[max(0, y - band):y + band + 1, :] = True
    for x in range(W):
        if cols[x]:
            ex[:, max(0, x - band):x + band + 1] = True
    return ex, rows, cols
