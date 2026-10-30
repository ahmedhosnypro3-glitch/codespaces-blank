#!/usr/bin/env python3
"""Adjudicate improvised-A27 finding 1: '22' tag glyph color (orig black-on-yellow
claimed vs build green). Measure ink hue inside the three yellow 22-patches in
ORIG (native 960x540) and render_27 (scale 2.08438)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
oa = np.asarray(Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")).astype(int)
ra = np.asarray(Image.open(f"{V}/recreated_pptx/qa/slide019/render_27.png").convert("RGB")).astype(int)
RS = ra.shape[1] / 960.0


def yellow(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > 170) & (g > 140) & (b < 190) & (r - b > 60) & (g - b > 40)


def classify(px):
    r, g, b = px
    mx, mn = max(px), min(px)
    if mx < 130 and mx - mn < 60:
        return "black/gray"
    if g - max(r, b) > 30:
        return "green"
    if b - max(r, g) > 30:
        return "blue"
    if r - max(g, b) > 40:
        return "red"
    if mx - mn < 50 and mx >= 130:
        return "light-gray"
    return f"other rgb=({r},{g},{b})"


for tag, a, sc in [("ORIG", oa, 1.0), ("RENDER27", ra, RS)]:
    print(f"=== {tag} (scale {sc:.5f}) ===")
    for row, (y0, y1) in enumerate([(265, 296), (373, 402), (478, 500)], 1):
        # window: outlier column zone below the pair arc
        wx0, wx1 = int(70 * sc), int(122 * sc)
        wy0, wy1 = int(y0 * sc), int(y1 * sc)
        win = a[wy0:wy1, wx0:wx1]
        ym = yellow(win)
        n_yellow = int(ym.sum())
        if n_yellow < 20:
            print(f"  row {row} y{y0}..{y1}: NO yellow patch ({n_yellow} px)")
            continue
        ys, xs = np.nonzero(ym)
        px0, px1 = wx0 + xs.min(), wx0 + xs.max()
        py0, py1 = wy0 + ys.min(), wy0 + ys.max()
        # ink = non-yellow, non-near-white pixels inside the patch bbox
        inner = a[py0:py1 + 1, px0:px1 + 1]
        r, g, b = inner[..., 0].astype(int), inner[..., 1].astype(int), inner[..., 2].astype(int)
        lum = inner.sum(axis=2)
        ink = (lum < 560) & ~yellow(inner)
        n = int(ink.sum())
        if n < 5:
            print(f"  row {row}: patch x{px0/sc:.0f}..{px1/sc:.0f} y{py0/sc:.0f}..{py1/sc:.0f}, no ink px")
            continue
        ir, ig, ib = r[ink], g[ink], b[ink]
        mean = (ir.mean(), ig.mean(), ib.mean())
        # darkest quartile = glyph core
        order = np.argsort(lum[ink])
        k = max(1, n // 4)
        core = (ir[order][:k].mean(), ig[order][:k].mean(), ib[order][:k].mean())
        cls = classify(tuple(int(v) for v in core))
        print(f"  row {row}: patch x{px0/sc:.1f}..{px1/sc:.1f} y{py0/sc:.1f}..{py1/sc:.1f} | "
              f"ink n={n} mean=({mean[0]:.0f},{mean[1]:.0f},{mean[2]:.0f}) "
              f"core=({core[0]:.0f},{core[1]:.0f},{core[2]:.0f}) -> {cls}")
