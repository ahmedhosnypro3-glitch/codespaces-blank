#!/usr/bin/env python3
"""Probe 17: ASCII of the four caption lines (strict dark-ink predicate,
background = the local panel gray 233,233,231 / off-white JPEG noise), with
the vertical-rule column 840 excluded, so the true per-line glyph bboxes and
the text color are settled.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

# caption ink: clearly darker/greyer than the off-white band background
bg = (r + g + b > 690)          # bright band
ink = ~bg


def dump(nm, x0, x1, y0, y1, drop_cols=()):
    m = ink[y0:y1 + 1, x0:x1 + 1].copy()
    if drop_cols:
        for c in drop_cols:
            if x0 <= c <= x1:
                m[:, c - x0] = False
    ys, xs = np.where(m)
    print(f"\n===== {nm} (y{y0}..{y1} x{x0}..{x1}) =====")
    if not len(ys):
        print("  no ink")
        return
    print(f"  INK BBOX x {x0+xs.min()}..{x0+xs.max()} (w={xs.max()-xs.min()+1}) "
          f"y {y0+ys.min()}..{y0+ys.max()} (h={ys.max()-ys.min()+1}) "
          f"center ({(x0+xs.min()+x0+xs.max())/2:.1f},{(y0+ys.min()+y0+ys.max())/2:.1f})")
    # ink color of the darkest decile
    vals = a[y0:y1 + 1, x0:x1 + 1][m]
    s = vals.sum(axis=1)
    dk = vals[s < np.percentile(s, 15)]
    print(f"  darkest-decile mean RGB ({dk[:,0].mean():.0f},{dk[:,1].mean():.0f},{dk[:,2].mean():.0f})")
    X0, X1 = x0 + xs.min() - 1, x0 + xs.max() + 1
    if X1 - X0 > 240:
        print("  (wide; printing every 2nd column)")
        step = 2
    else:
        step = 1
    print("      " + "".join(str((x // 10) % 10) if x % 10 == 0 else " " for x in range(X0, X1 + 1, step)))
    for y in range(y0 + ys.min() - 1, y0 + ys.max() + 2):
        print(f"  {y:4d} " + "".join("#" if m[y - y0, x - x0] else " " for x in range(X0, X1 + 1, step)))


dump("LCAP line1 'Overfit (try to minimize the residuals ONLY)'", 100, 470, 486, 506)
dump("LCAP line2 'Fails to detect the Pattern'", 100, 470, 506, 526)
dump("RCAP line1 'Generalized (Residuals are not minimized)'", 480, 878, 486, 506, drop_cols=(840,))
dump("RCAP line2 'Successes to detect the Pattern'", 480, 878, 506, 526, drop_cols=(840,))
