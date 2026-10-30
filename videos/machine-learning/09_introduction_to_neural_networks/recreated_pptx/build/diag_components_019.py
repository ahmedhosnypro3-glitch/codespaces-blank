#!/usr/bin/env python3
"""Slide 019 — inventory every text-like ink component (original vs render).

Erodes away 1px gridlines/borders/curves, then connected-component labels what
remains: each component's bbox is a text blob (glyph cluster) or a swatch.
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rendered-1.png"


def lum(a):
    return 0.299 * a[..., 0] + 0.587 * a[..., 1] + 0.114 * a[..., 2]


def erode(mask):
    er = mask.copy()
    er[:-1, :] &= mask[1:, :]
    er[:, :-1] &= mask[:, 1:]
    er[:-1, :-1] &= mask[1:, 1:]
    er[1:, :-1] &= mask[:-1, 1:]
    er[:-1, 1:] &= mask[1:, :-1]
    er[1:, 1:] &= mask[:-1, :-1]
    return er


def inventory(path, label, scale=1.0, min_px=6, y_lo=0, y_hi=None, x_lo=0, x_hi=None):
    im = Image.open(path).convert("RGB")
    if scale != 1.0:
        im = im.resize((int(round(im.size[0] * scale)), int(round(im.size[1] * scale))), Image.LANCZOS)
    a = np.asarray(im).astype(int)
    H, W = a.shape[:2]
    l = lum(a)
    mask = l < 175
    er = erode(mask)
    lab, n = ndimage.label(er)
    print(f"\n=== {label}  ({W}x{H})  components={n} ===")
    out = []
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < min_px:
            continue
        x0, x1 = xs.min(), xs.max()
        y0, y1 = ys.min(), ys.max()
        bw, bh = x1 - x0 + 1, y1 - y0 + 1
        if bw > 120 and bh > 120:
            kind = "FRAME/PLANE"
        elif bw > bh * 2.2:
            kind = "horizontal-text"
        elif bh > bw * 2.2:
            kind = "VERTICAL-text"
        else:
            kind = "compact/swatch"
        out.append((y0, x0, bw, bh, kind, len(xs)))
    out.sort(key=lambda t: (t[0], t[1]))
    shown = 0
    for y0, x0, bw, bh, kind, px in out:
        fx0, fy0 = x0 / scale, y0 / scale
        if y_hi is not None and fy0 > y_hi:
            continue
        if y_lo is not None and fy0 < y_lo:
            continue
        if x_hi is not None and fx0 > x_hi:
            continue
        if x_lo is not None and fx0 < x_lo:
            continue
        print(f"  frame x={fx0:7.1f}..{fx0 + bw / scale:7.1f}  y={fy0:6.1f}..{fy0 + bh / scale:6.1f} "
              f"w={bw / scale:5.1f} h={bh / scale:5.1f}  {kind:<18} px={px}")
        shown += 1
    print(f"  ({shown} shown of {len(out)})")


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    if which in ("orig", "both"):
        inventory(ORIG, "ORIGINAL slide_019.jpg", min_px=5)
    if which in ("render", "both"):
        inventory(RENDER, "RENDER slide_019_rendered-1.png (frame coords)", scale=2001 / 960, min_px=8)
