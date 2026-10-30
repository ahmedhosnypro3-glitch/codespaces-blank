#!/usr/bin/env python3
"""Control test on the build renders (crisp green ink).

For each render, split each row group's green y-line into its three numbers and
cross-correlate them across row groups.

render_6 (the bytes attempt 6 judged) repeats row 1's numbers in rows 2/3, so
its cross-row correlations must be ~1.0. render_8 (current) does not, so they
must be low. This calibrates what a correlation value means before the same
measurement is applied to the original frame.
"""
from PIL import Image
import numpy as np

QA = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019"
SCALE = 150 / 72.0
COL_X = (134, 376)
ROW_Y = {"rg1": (243, 265), "rg2": (348, 370), "rg3": (458, 480)}
NUM_GAP = 20
GLYPH_GAP = 2


def green(path):
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return np.clip((g - r) - 10, 0, None)


def runs_from_mask(m, x0, x1, y0, y1, gap):
    sub = m[y0:y1, x0:x1]
    cols = np.nonzero(sub.max(axis=0) > 20)[0]
    if len(cols) == 0:
        return []
    out, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - p > gap:
            out.append((s, p))
            s = c
        p = c
    out.append((s, p))
    return [(x0 + int(a), x0 + int(b)) for a, b in out]


def numbers(path, row):
    m = green(path)
    fy0, fy1 = ROW_Y[row]
    y0, y1 = int(fy0 * SCALE), int(fy1 * SCALE)
    x0, x1 = int(COL_X[0] * SCALE), int(COL_X[1] * SCALE)
    nums = []
    for a, b in runs_from_mask(m, x0, x1, y0, y1, NUM_GAP):
        sub = m[y0:y1, a:b + 1]
        nums.append((a, sub))
    return nums


def norm(bm):
    ys, xs = np.nonzero(bm > 20)
    if len(ys) == 0:
        return None
    sub = bm[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    out = np.asarray(Image.fromarray(np.clip(sub, 0, 255).astype(np.uint8))
                     .resize((24, 12), Image.BILINEAR)).astype(float)
    out -= out.min()
    return out / out.max() if out.max() else None


def corr(a, b):
    if a is None or b is None:
        return float("nan")
    a, b = a - a.mean(), b - b.mean()
    d = np.sqrt((a * a).sum() * (b * b).sum())
    return float((a * b).sum() / d) if d else float("nan")


for name in ("render_6.png", "render_8.png"):
    path = f"{QA}/{name}"
    print(f"===== {name} : NO REG column, green y-line numbers =====")
    data = {rg: [norm(bm) for _, bm in numbers(path, rg)] for rg in ROW_Y}
    widths = {rg: [(b - a + 1) for (a, b) in
                   runs_from_mask(green(path), int(COL_X[0] * SCALE),
                                  int(COL_X[1] * SCALE),
                                  int(ROW_Y[rg][0] * SCALE),
                                  int(ROW_Y[rg][1] * SCALE), NUM_GAP)]
              for rg in ROW_Y}
    for rg in ROW_Y:
        print(f"  {rg}: {len(data[rg])} numbers, widths(render px) {widths[rg]}")
    for rg in ROW_Y:
        for i in range(3):
            vals = [round(corr(data[rg][i], data[o][i]), 3) for o in ROW_Y]
            print(f"    {rg} number{i+1} vs rg1/rg2/rg3 number{i+1}: {vals}")
    print()
