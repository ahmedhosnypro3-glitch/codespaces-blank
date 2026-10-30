#!/usr/bin/env python3
"""Slide 019 — diagnose duplicate text overlays vs the original frame.

The build draws some labels TWICE: once baked into the matplotlib graph PNG
and once again as native pptx text. This script measures the ORIGINAL frame's
ink in the corresponding regions and reports the ink extent/orientation so the
duplicate overlay can be decided on pixels, not on prose.
"""
import sys
import numpy as np
from PIL import Image

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_019.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_019_rendered-1.png"

# Panel borders measured by gen_slide_019_graphs.py (frame px, 960x540)
PANELS = {
    "sigmoid": (105, 59, 410, 237),
    "tanh":    (499, 59, 804, 237),
    "tan":     (105, 297, 410, 475),
    "arctan":  (499, 297, 804, 475),
}


def ink_mask(arr, bg_tol=26):
    """Dark-ish ink on the light-gray panel background."""
    bg = np.median(arr.reshape(-1, arr.shape[2]), axis=0)
    d = np.abs(arr.astype(int) - bg.astype(int)).max(axis=2)
    return d > bg_tol, bg


def report(path, label, scale=1.0):
    im = Image.open(path).convert("RGB")
    arr = np.asarray(im)
    h, w = arr.shape[:2]
    print(f"\n=== {label}  ({w}x{h}) ===")
    regions = [
        ("sigmoid TL y-label area", "sigmoid", (0, 0, 90, 60)),
        ("sigmoid TL legend area", "sigmoid", (0, 0, 190, 45)),
        ("tanh TL y-label area", "tanh", (0, 0, 90, 60)),
        ("arctan TL title area", "arctan", (0, 0, 210, 30)),
    ]
    for rname, panel, off in regions:
        x0, y0, x1, y1 = PANELS[panel]
        rx0 = int(x0 * scale) + off[0]
        ry0 = int(y0 * scale) + off[1]
        rx1 = int(x0 * scale) + off[2]
        ry1 = int(y0 * scale) + off[3]
        rx0, ry0 = max(0, rx0), max(0, ry0)
        rx1, ry1 = min(w, rx1), min(h, ry1)
        sub = arr[ry0:ry1, rx0:rx1]
        if sub.size == 0:
            continue
        m, bg = ink_mask(sub)
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            print(f"  {rname}: NO INK in frame box x={rx0}..{rx1} y={ry0}..{ry1}")
            continue
        ink_x0, ink_x1 = rx0 + xs.min(), rx0 + xs.max()
        ink_y0, ink_y1 = ry0 + ys.min(), ry0 + ys.max()
        bw, bh = ink_x1 - ink_x0 + 1, ink_y1 - ink_y0 + 1
        # orientation: compare ink width vs height of the bounding box
        orient = "HORIZONTAL" if bw > bh * 1.6 else ("VERTICAL" if bh > bw * 1.6 else "square/compact")
        # column and row profiles to see if it is a word-run or a stacked blob
        colprof = m.sum(axis=0)
        rowprof = m.sum(axis=1)
        print(f"  {rname}: ink bbox frame x={ink_x0}..{ink_x1} y={ink_y0}..{ink_y1} "
              f"w={bw} h={bh} -> {orient}; ink_px={m.sum()}")
        print(f"      bg_rgb={tuple(int(v) for v in bg)}  colprof_nonzero_cols="
              f"{int((colprof > 0).sum())}/{bw} rowprof_nonzero_rows={int((rowprof > 0).sum())}/{bh}")


if __name__ == "__main__":
    report(ORIG, "ORIGINAL unique_slides/slide_019.jpg")
    try:
        report(RENDER, "RENDER build/slide_019_rendered-1.png", scale=2001 / 960)
    except FileNotFoundError:
        print("render missing")
