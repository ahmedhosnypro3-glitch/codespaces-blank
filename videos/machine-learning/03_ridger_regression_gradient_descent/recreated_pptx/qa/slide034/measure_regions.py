#!/usr/bin/env python3
"""Measure slide_034.jpg (original) + render_2.png at frame-px scale.

Purpose: derive every content region's geometry before editing the build.
Output is compact: one line per detected text/colour band with its bbox.
"""
import sys

import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"


def load(path, sc):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return im, sc


def masks(im):
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    gray = (abs(r - 233) < 16) & (abs(g - 233) < 16) & (abs(b - 231) < 18)
    white = (r > 245) & (g > 245) & (b > 245)
    red = (r > 90) & (r - g > 40) & (r - b > 10)
    blue = (b > 110) & (b - r > 40) & (b - g > 15)
    dark = (r < 110) & (g < 110) & (b < 110)
    ink = ~(gray | white)
    return dict(ink=ink, red=red, blue=blue, dark=dark, gray=gray, white=white)


def bands(mask, sc, y0, y1, x0, x1, min_h=3, min_n=8):
    m = mask[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
    rows = m.sum(axis=1)
    out, prev = [], False
    for y in range(m.shape[0]):
        cur = rows[y] > 0
        if cur and not prev:
            out.append([y, y])
        elif not cur and prev:
            out[-1][1] = y - 1
        prev = cur
    if prev and out:
        out[-1][1] = m.shape[0] - 1     # close a band running to the slice edge
    res = []
    for a, b in out:
        if (b - a + 1) / sc < min_h:
            continue
        sub = m[a:b + 1]
        if sub.sum() < min_n:
            continue
        ys, xs = np.where(sub)
        res.append((y0 + a / sc, y0 + b / sc + 1, x0 + xs.min() / sc, x0 + xs.max() / sc + 1, int(sub.sum())))
    return res


def describe(tag, mk, sc, y0, y1, x0, x1):
    for name in ("ink", "red", "blue", "dark"):
        b = bands(mk[name], sc, y0, y1, x0, x1)
        if not b:
            continue
        print(f"  {tag} {name:4s}: " + " | ".join(
            f"r{a:.0f}..{b:.0f} x{c:.0f}..{d:.0f} n{e}" for a, b, c, d, e in b))


if __name__ == "__main__":
    which = sys.argv[1]
    if which == "orig":
        im, sc = load(f"{BASE}/unique_slides/slide_034.jpg", 1.0)
    else:
        im, sc = load(f"{BASE}/recreated_pptx/qa/slide034/render_2.png", 1125 / 540.0)
    mk = masks(im)
    print(f"=== {which}: {im.shape[1]}x{im.shape[0]} (scale {sc:.3f}) ===")
    print("-- TITLE/SUBTITLE area (rows 40..190, cols 50..560) --")
    describe(which, mk, sc, 40, 190, 50, 560)
    print("-- LEFT-CENTER (rows 185..300, cols 50..560) --")
    describe(which, mk, sc, 185, 300, 50, 560)
    print("-- TABLE area (rows 295..510, cols 60..900) --")
    describe(which, mk, sc, 295, 510, 60, 900)
    print("-- PLOT area (rows 40..280, cols 560..912) --")
    describe(which, mk, sc, 40, 280, 560, 912)
    print("-- BADGE (rows 45..105, cols 840..900) --")
    describe(which, mk, sc, 45, 105, 840, 900)
