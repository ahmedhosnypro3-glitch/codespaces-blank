"""Core measurement: chrome-masked ink geometry, render vs original, frame scale."""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
FRAME_W, FRAME_H = 960, 540
SX = FRAME_W / 2001.0
SY = FRAME_H / 1125.0


def ink_mask(img, thresh=14, radius=12):
    rgb = img.convert("RGB")
    a = np.asarray(rgb).astype(np.int16)
    bg = np.asarray(rgb.filter(ImageFilter.GaussianBlur(radius))).astype(np.int16)
    return np.abs(a - bg).max(axis=2) > thresh


def bbox(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def box_in(mask, y0, y1, x0, x1):
    sub = np.zeros_like(mask)
    y0, y1 = max(0, y0), min(mask.shape[0] - 1, y1)
    x0, x1 = max(0, x0), min(mask.shape[1] - 1, x1)
    sub[y0:y1 + 1, x0:x1 + 1] = mask[y0:y1 + 1, x0:x1 + 1]
    return bbox(sub)


def mask_render_chrome(mask):
    """Mask the house chrome on a 2001x1125 render: red frame ring + yellow badge."""
    H, W = mask.shape
    ex = np.zeros_like(mask)
    inset = int(round(0.15 * 150))
    band = 7
    # the frame is a 1.5pt stroke -> ~3px; band generously to kill anti-aliased halo
    for t in (inset, W - 1 - inset):
        ex[max(0, t - band):t + band + 1, :] = True
    for t in (inset, H - 1 - inset):
        ex[:, max(0, t - band):t + band + 1] = True
    # yellow badge disc
    ex[int(0.18 * 150):int(0.92 * 150), int(12.36 * 150):int(13.08 * 150)] = True
    return mask & ~ex


def mask_orig_chrome(mask):
    """Mask the original frame's own outer border ring (per-slide, not house chrome)."""
    H, W = mask.shape
    ex = np.zeros_like(mask)
    rows = mask.sum(1)
    cols = mask.sum(0)
    band = 9
    # outer border only: top 12% of rows, bottom 12%, left 12% of cols, right 12%
    top = [y for y in range(int(H * 0.12)) if rows[y] > W * 0.55]
    bot = [y for y in range(int(H * 0.88), H) if rows[y] > W * 0.55]
    lef = [x for x in range(int(W * 0.12)) if cols[x] > H * 0.45]
    rig = [x for x in range(int(W * 0.88), W) if cols[x] > H * 0.45]
    for y in top:
        ex[max(0, y - band):y + band + 1, :] = True
    for y in bot:
        ex[max(0, y - band):y + band + 1, :] = True
    for x in lef:
        ex[:, max(0, x - band):x + band + 1] = True
    for x in rig:
        ex[:, max(0, x - band):x + band + 1] = True
    return mask & ~ex


def content_boxes(render_path, orig_path, bands):
    """Return per-band bboxes: render (frame-scaled) and original (frame scale)."""
    rimg = Image.open(render_path).convert("RGB")
    oimg = Image.open(orig_path).convert("RGB")
    rm = mask_render_chrome(ink_mask(rimg))
    om = mask_orig_chrome(ink_mask(oimg))
    out = {}
    for name, (y0, y1) in bands.items():
        # render band -> render px, then normalise to frame scale
        ry0, ry1 = int(y0 / SY), int(y1 / SY)
        rb = box_in(rm, ry0, ry1, 0, rm.shape[1] - 1)
        rbf = None if rb is None else (rb[0] * SX, rb[1] * SY, rb[2] * SX, rb[3] * SY)
        ob = box_in(om, y0, y1, 0, om.shape[1] - 1)
        out[name] = (rbf, ob)
    return out, rm, om
