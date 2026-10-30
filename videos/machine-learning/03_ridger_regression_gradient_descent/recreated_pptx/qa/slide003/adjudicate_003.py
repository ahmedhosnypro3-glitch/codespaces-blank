#!/usr/bin/env python3
"""Slide 003 PIL adjudication of judge FAIL/MINOR findings.

Settles every claim from the three full-slide verdicts (judge_attempt_5/6/7)
and the crop verdict (crop_5_matrix_stack_judge) with measurements on the
original frame + the render, both in 960x540 frame-px space.

Usage: python3 adjudicate_003.py <region> [which]
  region: top | bl | br | remember | ingeneral | title | ntrain | arrow | chrome
  which:  orig (default) | render | both
"""
import sys
import numpy as np
from PIL import Image

ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003/render_5.png"
FRAME_H = 540.0

REGIONS = {
    "top":       (271, 107, 596, 301),
    "topband":   (285, 115, 600, 300),
    "bl":        (79, 323, 533, 517),
    "br":        (572, 323, 752, 517),
    "remember":  (649, 153, 874, 221),
    "ingeneral": (659, 268, 850, 294),
    "title":     (55, 60, 900, 100),
    "ntrain":    (55, 100, 290, 210),
    "arrow":     (525, 325, 580, 412),
    "chrome":    (40, 40, 920, 535),
}


def load(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    return im, im.shape[0] / FRAME_H


def cls(r, g, b):
    """ASCII class for one pixel."""
    if r > 240 and g > 240 and b > 240:
        return " "                                    # white
    if abs(r - 233) < 16 and abs(g - 233) < 16 and abs(b - 231) < 18:
        return "."                                    # panel gray E9E9E7
    if r < 100 and g < 100 and b < 100:
        return "#"                                    # near-black ink
    if r > 145 and r - g > 45 and r - b > 45:
        return "R"                                    # red
    if b > 145 and b - r > 30:
        return "B"                                    # blue
    if r > 235 and g > 235 and b < 215:
        return "Y"                                    # yellow band
    if g > 215 and b > 215 and r < 225:
        return "C"                                    # cyan fill
    if r > 225 and 165 < g < 225 and 160 < b < 228:
        return "P"                                    # pink band
    return "?"


def ascii_map(a, s, reg, sx=2, sy=2, label=""):
    x0, y0, x1, y1 = reg
    print(f"--- {label} frame x{x0}..{x1} y{y0}..{y1}  step {sx}/{sy} "
          f"(1 col = {sx}px, 1 row = {sy}px) ---")
    hdr = "".join(str((x0 + i * sx) // 100 % 10) for i in range((x1 - x0) // sx))
    print("      " + hdr)
    for y in range(y0, y1, sy):
        cols = []
        for x in range(x0, x1, sx):
            # majority class inside the step cell
            vals = {}
            for dy in range(sy):
                yy = y + dy
                if yy >= a.shape[0]:
                    continue
                for dx in range(sx):
                    xx = x + dx
                    if xx >= a.shape[1]:
                        continue
                    c = cls(*a[yy, xx])
                    vals[c] = vals.get(c, 0) + 1
            if not vals:
                cols.append(" ")
                continue
            best = max(vals, key=vals.get)
            # prefer ink over background inside a mixed cell
            if best in (" ", ".") and sum(v for k, v in vals.items()
                                         if k not in (" ", ".")) >= 2:
                ink = [k for k in vals if k not in (" ", ".")]
                best = max(ink, key=vals.get)
            cols.append(best)
        print(f"{y:5d} " + "".join(cols))


def ink_profile(a, s, reg, axis):
    """Per-row (axis=0) or per-column (axis=1) non-background ink count."""
    x0, y0, x1, y1 = reg
    sub = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    bg = (np.abs(sub[:, :, 0] - 233) < 16) & (np.abs(sub[:, :, 1] - 233) < 16) & \
         (np.abs(sub[:, :, 2] - 231) < 18)
    wht = (sub[:, :, 0] > 240) & (sub[:, :, 1] > 240) & (sub[:, :, 2] > 240)
    ink = ~(bg | wht)
    return ink.sum(axis=axis)


def bands(vals, minlen=1):
    """Contiguous index ranges where vals > 0."""
    out, start = [], None
    for i, v in enumerate(vals):
        if v > 0 and start is None:
            start = i
        elif v == 0 and start is not None:
            if i - start >= minlen:
                out.append((start, i - 1))
            start = None
    if start is not None and len(vals) - start >= minlen:
        out.append((start, len(vals) - 1))
    return out


def run(which):
    p = ORIG if which == "orig" else RENDER
    a, s = load(p)
    print(f"### {p}  size {a.shape[1]}x{a.shape[0]}  scale {s:.4f}")
    for name in sys.argv[1:]:
        reg = REGIONS[name]
        if name == "chrome":
            continue
        ascii_map(a, s, reg, label=f"{which}:{name}")
        rows = ink_profile(a, s, reg, axis=1)
        cols = ink_profile(a, s, reg, axis=0)
        ry = bands(list(rows))
        rx = bands(list(cols))
        print(f"  ink row-bands (frame px): "
              f"{[(reg[1] + b[0] / s, reg[1] + b[1] / s) for b in ry]}")
        print(f"  ink col-bands (frame px): "
              f"{[(reg[0] + b[0] / s, reg[0] + b[1] / s) for b in rx]}")
        print()


if __name__ == "__main__":
    run(sys.argv[1])
