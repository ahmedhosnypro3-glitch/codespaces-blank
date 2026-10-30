#!/usr/bin/env python3
"""Curve fidelity for slide 033 — render_11 (attempt 11, == render_8/build_attempt_8).

Attempts 1-6 drew the curve in #00B050 green (a loose green mask measured it).
The attempt-7 rebuild replaced the hand-traced curve with the generated asset
`build/assets/slide_033_plot_v7.png`, whose curve ink is TEAL ≈(32,160,160) —
which matches the ORIGINAL frame's own dominant saturated plot-box hue
(72,168,168)/(96,168,168). So the mask is now teal-selective:
    R < 110, G > 120, B > 120, |G-B| < 45, G-R > 50, B-R > 50
and still excludes the two marker colours (green square, orange arrowhead),
which otherwise contaminate the per-column centreline.

Curve law: ONE continuous curve (no column gap > 8px), small second-difference
ripple, extrema at the frame's MEASURED positions.
"""
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"


def curve(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    s = im.shape[0] / 540.0
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    m = (R < 110) & (G > 120) & (B > 120) & (abs(G - B) < 45) & (G - R > 50) & (B - R > 50)
    m &= ~((abs(R - 143) < 40) & (G > 215) & (B < 60))    # green square #8FFF17
    m &= ~((R > 205) & (G > 95) & (G < 150) & (B < 70))   # orange arrowhead #EE730C
    col = {}
    ys, xs = np.where(m[int(105 * s):int(305 * s), int(612 * s):int(835 * s)])
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


report(f"{V}/unique_slides/slide_033.jpg", "ORIG  ")
report(f"{V}/recreated_pptx/qa/slide033/render_11.png", "RENDER11")
