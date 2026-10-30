#!/usr/bin/env python3
"""Slide 026 word-run comparator — ORIGINAL frame vs a render, same predicates.

Purpose: separate REAL build defects from the original font's per-word metric
noise (calibration spread +/-2.6% of line width). A mid-line word/bar that lands
+/-5-7px from the original is font noise; fighting it with heavy tracking
distorts the build. A systematic line-total error is a real defect.

Usage: word_runs_026.py [render.png]
"""
import sys
import numpy as np
from PIL import Image

HERE = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide026"
ORG = HERE + "/../../../unique_slides/slide_026.jpg"


def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)


def masks(im):
    R, G, B = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    return {
        "red": (R - G > 40) & (R - B > 40),
        "blue": (B - R > 40) & (B - G > 40),
        "inkW": (np.abs(im - 255).max(axis=2) > 30),
    }


def wordruns(mask, y0, y1, x0, x1, gap=3, minlen=2):
    """Word runs (contiguous ink columns, split by >=gap empty cols)."""
    sub = mask[y0:y1 + 1, x0:x1 + 1]
    colink = sub.any(axis=0)
    out, start, miss = [], None, 0
    for i, v in enumerate(colink):
        if v:
            if start is None:
                start = i
            miss = 0
        elif start is not None:
            miss += 1
            if miss >= gap:
                if i - miss - start >= minlen:
                    out.append((x0 + start, x0 + i - miss))
                start = None
    if start is not None and len(colink) - start >= minlen:
        out.append((x0 + start, x0 + len(colink) - 1))
    return out


def cmp_line(name, mkey, y0, y1, x0, x1, gap=3):
    print("\n== %s  (y %d..%d, x %d..%d, %s) ==" % (name, y0, y1, x0, x1, mkey))
    wo = wordruns(mo[mkey], y0, y1, x0, x1, gap)
    wr = wordruns(mr[mkey], y0, y1, x0, x1, gap)
    print("  ORIG %d runs: %s" % (len(wo), wo))
    print("  REN  %d runs: %s" % (len(wr), wr))
    if len(wo) == len(wr):
        tot = 0
        for i, (a, b) in enumerate(zip(wo, wr)):
            d0, d1 = wr[i][0] - a, wr[i][1] - b
            tot += abs(d0)
            print("    w%-2d x %4d..%4d (w%3d) | ren %6.1f..%6.1f (w%5.1f) | d %+6.1f %+6.1f"
                  % (i, a, b, b - a + 1, wr[i][0], wr[i][1], wr[i][1] - wr[i][0] + 1, d0, d1))
        print("  => same word count; mean |left delta| %.1f, max %+.1f"
              % (tot / len(wo), max(abs(wr[i][0] - wo[i][0]) for i in range(len(wo)))))
    else:
        print("  => WORD COUNT DIFFERS — inspect manually")


mo, mr = masks(load(ORG)), None
rg = sys.argv[1] if len(sys.argv) > 1 else HERE + "/render_4.png"
mr = masks(load(rg))
SX, SY = mr["inkW"].shape[1] / 960.0, mr["inkW"].shape[0] / 540.0
print("render scale %.4f x %.4f" % (SX, SY))

# convert render windows to render px
def wy(a, b):
    return int(a * SY), int(b * SY)

LINES = [
    ("gdhdr  ", "red", 105, 133, 100, 860),
    ("rowA   ", "blue", 138, 168, 140, 860),
    ("rowB   ", "blue", 172, 202, 140, 860),
    ("rowC-bl", "blue", 205, 236, 140, 516),
    ("rowD   ", "blue", 238, 268, 140, 860),
    ("N1     ", "inkW", 338, 366, 86, 860),
    ("N2     ", "inkW", 372, 400, 100, 860),
    ("N3     ", "inkW", 437, 465, 86, 860),
    ("N4     ", "inkW", 470, 496, 100, 860),
]

for nm, mk, y0, y1, x0, x1 in LINES:
    # run the comparator with the render in FRAME px by slicing its masks at render px
    ry0, ry1 = int(y0 * SY), int(y1 * SY)
    rx0, rx1 = int(x0 * SX), int(x1 * SX)
    wo = wordruns(mo[mk], y0, y1, x0, x1)
    wr = [(a / SX, b / SX) for a, b in wordruns(mr[mk], ry0, ry1, rx0, rx1)]
    print("\n== %s (y %d..%d, %s) ==" % (nm, y0, y1, mk))
    print("  ORIG: %s" % wo)
    print("  REN : %s" % ["%.1f..%.1f" % t for t in wr])
    if len(wo) == len(wr) and wo:
        d = [(wr[i][0] - wo[i][0], wr[i][1] - wo[i][1]) for i in range(len(wo))]
        print("  n=%d  d(left) %s" % (len(wo), " ".join("%+.1f" % t[0] for t in d)))
        print("          d(right) %s" % " ".join("%+.1f" % t[1] for t in d))
        ls = [t[0] for t in d]
        print("  left deltas: min %+.1f max %+.1f mean %+.1f | right: min %+.1f max %+.1f"
              % (min(ls), max(ls), sum(ls) / len(ls),
                 min(t[1] for t in d), max(t[1] for t in d)))
    else:
        print("  >>> word count differs (%d vs %d) — inspect" % (len(wo), len(wr)))
