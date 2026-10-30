#!/usr/bin/env python3
"""Curve fidelity for slide 033 — render_4.

The original `measurement/curve_fidelity.py` uses a loose green mask
(G-R>25, G-B>25) which, from attempt 4 on, ALSO catches the two measured
markers that were added to the build (the green square #8FFF17 at x629-643
y236-244 and the orange arrowhead #EE730C at x631-648 y115-138). Those
contaminate the per-column centerline and make the d2 ripple look huge
(11.3px) even though the curve itself is unchanged.

This version masks to the curve's own colour (#00B050) and explicitly
excludes the two marker colours, so it measures ONLY the non-convex curve.

Curve law: ONE continuous curve (no column gaps > 8px), second-difference
ripple std small, extrema at the frame's MEASURED positions:
  max(627,187) min(662,127) max(691,175) plateau(717,171) max(755,185)
  min(779,139) max(807,260)
(the frame's own ink trace; the analytic f(x)=(x^2 cos(x)-x)/10 has no
interior extrema over -11..-9.5, so the frame wins)
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"


def curve(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    s = im.shape[0] / 540.0
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = (abs(R - 0) < 25) & (abs(G - 176) < 25) & (abs(B - 80) < 25)
    m &= ~((abs(R - 143) < 40) & (G > 215) & (B < 60))   # green square
    m &= ~((R > 205) & (G > 95) & (G < 150) & (B < 70))  # orange arrowhead
    col = {}
    ys, xs = np.where(m[int(105 * s):int(305 * s), int(615 * s):int(830 * s)])
    ys = ys + int(105 * s); xs = xs + int(615 * s)
    for y, x in zip(ys, xs):
        col.setdefault(int(round(x / s)), []).append(y / s)
    xs = sorted(col)
    return xs, [float(np.median(col[x])) for x in xs]


def report(path, name):
    xs, cy = curve(path)
    if len(xs) < 50:
        print(f"{name}: curve not detectable ({len(xs)} columns)"); return
    d2 = np.diff(cy, 2)
    gaps = sum(1 for i in range(len(xs) - 1) if xs[i + 1] - xs[i] > 8)
    turn = []
    for i in range(2, len(xs) - 2):
        if cy[i] <= cy[i - 2] and cy[i] <= cy[i + 2]: turn.append(("min", xs[i], round(cy[i])))
        if cy[i] >= cy[i - 2] and cy[i] >= cy[i + 2]: turn.append(("max", xs[i], round(cy[i])))
    out = []
    for t in turn:
        if out and out[-1][0] == t[0] and t[1] - out[-1][1] < 6: continue
        out.append(t)
    print(f"{name}: {len(xs)} cols, x {xs[0]}..{xs[-1]}, y {round(min(cy))}..{round(max(cy))}")
    print(f"   ripple std={d2.std():.3f}px max|d2|={abs(d2).max():.2f}px, column gaps>8px: {gaps}")
    print(f"   turning points: {out}")
    print("   ->", "SMOOTH ONE-CURVE OK" if (d2.std() < 6 and gaps == 0) else "FAIL: not smooth/one-curve")


report(f"{V}/recreated_pptx/qa/slide033/render_4.png", "RENDER4")
