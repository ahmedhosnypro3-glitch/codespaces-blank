#!/usr/bin/env python3
r"""Banked colour/structure probe for slide 015 (deck 03, 2026-10-23).

For each measured band/region of unique_slides/slide_015.jpg: dominant dark-ink
colour cores (median of the darkest 20% of ink pixels, per window) and the column
groups, so the rebuild can reproduce per-symbol colours instead of guessing.

Usage: python3 probe_015_colors.py
"""
import numpy as np
from PIL import Image

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_015.jpg"
LUM_THR = 190

rgb = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
lum = rgb.mean(axis=2)
ink = lum < LUM_THR


def colgroups(m):
    cols = np.where(m.sum(axis=0) > 0)[0]
    out, prev = [], None
    for c in cols:
        if prev is None or c - prev > 2:
            out.append([int(c), int(c)])
        else:
            out[-1][1] = int(c)
        prev = c
    return out


def core(y0, y1, x0, x1, tag, n=25):
    m = ink[y0:y1 + 1, x0:x1 + 1]
    reg = rgb[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(m)
    if len(ys) == 0:
        print(f"  {tag:22s} NO INK")
        return
    sel = reg[ys, xs]
    l = sel.sum(axis=1)
    k = np.argsort(l)[: max(n, len(ys) // 20)]
    c = sel[k].mean(axis=0)
    print(f"  {tag:22s} n={len(ys):6d} core=({c[0]:.0f},{c[1]:.0f},{c[2]:.0f}) "
          f"#%02X%02X%02X" % (int(round(c[0])), int(round(c[1])), int(round(c[2]))))


def band(tag, y0, y1):
    print(f"\n=== {tag}: rows {y0}..{y1}")
    xc = colgroups(ink[y0:y1 + 1])
    print(f"   colgroups: {xc}")
    # split the band into columns windows and probe each
    if not xc:
        return
    for g0, g1 in xc:
        w = g1 - g0 + 1
        if w < 3:
            continue
        step = 40
        for x0 in range(g0, g1 + 1, step):
            x1 = min(x0 + step - 1, g1)
            core(y0, y1, x0, x1, f"x{x0}..{x1}")


band("TITLE", 55, 92)
band("EQ1 line1 (J(W) head)", 108, 151)
band("EQ1 line2", 167, 209)
band("EQ1 line3", 220, 263)
band("RED+PEACH box row", 275, 334)
band("DERIV steps", 351, 402)
band("NORMAL EQ", 417, 467)
band("GREEN box", 472, 517)
