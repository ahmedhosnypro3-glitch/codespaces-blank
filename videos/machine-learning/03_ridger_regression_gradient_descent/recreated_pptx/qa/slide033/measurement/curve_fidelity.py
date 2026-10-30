#!/usr/bin/env python3
"""Fidelity cross-check: the render's green curve vs the analysis contract.
analysis/slide_033_final.json gives f(x) = (x^2 cos(x) - x)/10 tabulated over
x = -11..-9.5, with a single tabulated local minimum at (-9.6, -8.11), the
initial point (-11, 1.15) and the annotations
"X is in between -9.7 and -9.6" / "f(x) is in between -8.08 and -8.011".
The curve on the slide must be ONE smooth curve with those extrema at their
measured positions. Run after every rebuild.
"""
import json, re
import numpy as np
from PIL import Image

V = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
SPEC = json.load(open(f"{V}/analysis/slide_033_final.json"))
ve = SPEC["visual_elements"][0]["description"]


def row(name):
    m = re.search(r"Row '" + re.escape(name) + r"': \[([^\]]*)\]", ve)
    return [float(v) for v in m.group(1).split(",")]


xr, fx = row("x"), row("f(x)")
mins = [(xr[i], fx[i]) for i in range(1, len(xr) - 1) if fx[i] < fx[i - 1] and fx[i] <= fx[i + 1]]
print("analysis contract")
print("  x row          :", xr)
print("  f(x) row       :", fx)
print("  initial point  : (%s, %s)" % (xr[0], fx[0]))
print("  local minima   :", mins)
print("  annotation 1   : X is in between -9.7 and -9.6")
print("  annotation 2   : f(x) is in between -8.08 and -8.011")


def curve_center(im, y0=105, y1=305, x0=615, x1=830):
    """centreline of the green curve, returned in FRAME px (offset-corrected)"""
    s = im.shape[0] / 540.0
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    grn = (G - R > 25) & (G - B > 25) & (G > 90)
    col = {}
    ys, xs = np.where(grn[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)])
    for y, x in zip(ys, xs):
        col.setdefault(int(x), []).append(int(y) + int(y0 * s))
    return {x0 + round(k / s): float(np.median(v) / s) for k, v in col.items()}


def check(path, name):
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    c = curve_center(im)
    if len(c) < 50:
        print(f"{name}: curve not detectable ({len(c)} columns)")
        return
    xs = sorted(c); cy = [c[x] for x in xs]
    d2 = np.diff(cy, 2)
    gaps = sum(1 for i in range(len(xs) - 1) if xs[i + 1] - xs[i] > 8)
    # turning points (de-duplicated)
    turn = []
    for i in range(2, len(xs) - 2):
        if cy[i] <= cy[i - 2] and cy[i] <= cy[i + 2]:
            turn.append(("min", xs[i], round(cy[i])))
        elif cy[i] >= cy[i - 2] and cy[i] >= cy[i + 2]:
            turn.append(("max", xs[i], round(cy[i])))
    ded = []
    for t in turn:
        if not ded or abs(t[1] - ded[-1][1]) > 25:
            ded.append(t)
    print(f"{name}: {len(c)} cols, x {min(c)}..{max(c)}, y {int(min(cy))}..{int(max(cy))}")
    print(f"   ripple std={np.std(d2):.3f}px max|d2|={np.abs(d2).max():.3f}px, column gaps>8px: {gaps}")
    print(f"   turning points: {ded}")
    ok_ripple = np.std(d2) <= 2.5
    ok_gaps = gaps <= 2
    print(f"   -> {'SMOOTH ONE-CURVE OK' if (ok_ripple and ok_gaps) else 'NOT SMOOTH / BROKEN'}")


check(f"{V}/unique_slides/slide_033.jpg", "ORIGINAL")
check(f"{V}/recreated_pptx/qa/slide033/render_3.png", "RENDER ")
