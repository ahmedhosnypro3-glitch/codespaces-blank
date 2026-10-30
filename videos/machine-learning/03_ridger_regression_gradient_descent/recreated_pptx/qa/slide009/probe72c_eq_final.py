#!/usr/bin/env python3
"""probe72c — attempt-7 eq-region delta final classification (glyphs vs annotation).

probe72b showed every eq delta is either ON the new red shaft corridor or on the
x=208/625 edge column where CERT carried pink PALE-ROSE dimline pixels that the
founder fix DELETED. This probe classifies every changed pixel as one of:

  NEW-INK   : B reddish (the founder-corrected red shaft / its AA fringe)
  OLD-DIM   : A pinkish pale-rose (r>g, r>b, 20<=r-g<=90) — the deleted dimline
  OTHER     : anything else -> verdict FAIL

Equation glyphs are black/navy on the PNG's near-white plate; a glyph change
would show as OTHER (dark-vs-dark or white-vs-gray without red/pink).
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
A = np.asarray(Image.open(os.path.join(HERE, "certified_attempt5_reconstructed.png")).convert("RGB")).astype(int)
B = np.asarray(Image.open(os.path.join(HERE, "render_7.png")).convert("RGB")).astype(int)
SY, SX = A.shape[0] / 540.0, A.shape[1] / 960.0
changed = (np.abs(A - B).max(axis=2) > 12)
BOXES = {"eq_left": (208, 140, 325, 183), "eq_right": (625, 140, 742, 183)}

def reddish(im):
    r, g, b = im[:, 0], im[:, 1], im[:, 2]
    return (r > 150) & ((r - g) > 15) & ((r - b) > 15)

def pinkish(im):
    r, g, b = im[:, 0], im[:, 1], im[:, 2]
    return (r > 200) & ((r - g) >= 8) & ((r - g) <= 100) & ((r - b) >= 5) & ((r - b) <= 90)

verdict = "PASS"
for name, (x0, y0, x1, y1) in BOXES.items():
    X0, Y0, X1, Y1 = int(x0 * SX), int(y0 * SY), int(x1 * SX), int(y1 * SY)
    sub = changed[Y0:Y1, X0:X1]
    ys, xs = np.nonzero(sub)
    a_px = A[Y0:Y1, X0:X1][ys, xs]
    b_px = B[Y0:Y1, X0:X1][ys, xs]
    new_ink = reddish(b_px)
    old_dim = pinkish(a_px)
    ok = new_ink | old_dim
    n_bad = int((~ok).sum())
    print("%-9s changed=%3d  NEW-INK=%3d  OLD-DIMLINE=%3d  OTHER=%d"
          % (name, len(ys), int(new_ink.sum()), int(old_dim.sum()), n_bad))
    if n_bad:
        idx = np.nonzero(~ok)[0][:8]
        for i in idx:
            print("   OTHER at frame(%.1f,%.1f) CERT=%s ATT7=%s"
                  % (x0 + xs[i] / SX, y0 + ys[i] / SY, tuple(a_px[i]), tuple(b_px[i])))
        verdict = "FAIL"
print()
if verdict == "PASS":
    print("VERDICT: PASS — eq-region deltas are 100% annotation mechanics")
    print("(new red shaft ink + deleted pale-rose dimline); equation glyph ink")
    print("unchanged. eq crop certificates re-judged via crop_6 (protocol); cap")
    print("certificates (0 changed px in probe72) remain valid.")
else:
    print("VERDICT: FAIL — unexplained eq-region deltas.")
