#!/usr/bin/env python3
"""probe72b — attempt-7 eq-region delta classification: annotation corridor vs glyphs.

probe72 found eq_left/eq_right NOT zero-diff vs certified attempt-5 (162/65 px).
This probe decides whether those deltas are (a) the founder-corrected annotation
corridor — EXPECTED, the old pale-rose dimline crossed the same corner in the
certified render — or (b) equation-glyph changes — which WOULD void the region.

Test: every changed pixel inside an eq box must lie within CORR px of the
founder-corrected dimension-shaft segment (the build's PANELS.dim geometry).
Then the glyph ink OUTSIDE the corridor is compared directly: changed px in the
box minus corridor band must be 0.
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
A = np.asarray(Image.open(os.path.join(HERE, "certified_attempt5_reconstructed.png")).convert("RGB")).astype(int)
B = np.asarray(Image.open(os.path.join(HERE, "render_7.png")).convert("RGB")).astype(int)
SY, SX = A.shape[0] / 540.0, A.shape[1] / 960.0
changed = (np.abs(A - B).max(axis=2) > 12)

# founder-corrected dimension shafts (build/slide_009.js PANELS, frame px)
SHAFTS = {
    "eq_left":  ((197.5, 145.0), (269.43, 285.03)),
    "eq_right": ((611.0, 145.0), (694.59, 320.53)),
}
BOXES = {"eq_left": (208, 140, 325, 183), "eq_right": (625, 140, 742, 183)}
CORR = 3.0  # frame px around the shaft centreline (1pt stroke + AA)

def seg_dist(px, py, p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    vx, vy = x1 - x0, y1 - y0
    L2 = vx * vx + vy * vy
    t = max(0.0, min(1.0, ((px - x0) * vx + (py - y0) * vy) / L2))
    cx, cy = x0 + t * vx, y0 + t * vy
    return ((px - cx) ** 2 + (py - cy) ** 2) ** 0.5

verdict = "PASS"
for name, (x0, y0, x1, y1) in BOXES.items():
    X0, Y0, X1, Y1 = int(x0 * SX), int(y0 * SY), int(x1 * SX), int(y1 * SY)
    sub = changed[Y0:Y1, X0:X1]
    ys, xs = np.nonzero(sub)
    fx = x0 + xs / SX
    fy = y0 + ys / SY
    p0, p1 = SHAFTS[name]
    d = np.array([seg_dist(px, py, p0, p1) for px, py in zip(fx, fy)])
    in_corr = d <= CORR
    out = int((~in_corr).sum())
    print("%-9s changed=%3d  in-corridor(<=%.1fpx)=%3d  OUTSIDE=%d  max_d=%.2fpx"
          % (name, len(ys), CORR, int(in_corr.sum()), out, d.max() if len(d) else 0.0))
    if out:
        bad = sorted(zip(fx[~in_corr], fy[~in_corr]))[:8]
        print("   outside-corridor sample:", ", ".join("(%.1f,%.1f)" % t for t in bad))
        verdict = "FAIL"
if verdict == "PASS":
    print()
    print("VERDICT: PASS — every eq-region delta sits on the founder-corrected shaft")
    print("corridor; equation glyph ink is unchanged. The attempt-5 eq-region")
    print("certificates are VOID for the corridor band only (re-judged via crop_6);")
    print("glyph content itself carries over.")
else:
    print()
    print("VERDICT: FAIL — eq deltas exist OUTSIDE the annotation corridor.")
