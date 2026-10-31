#!/usr/bin/env python3
"""Integrator PIL check of a candidate plot_025_bl.png against ground truth.

Ground-truth anchors are in original-frame px (960x540). The BL PNG is placed
by build/slide_025.js at frame x83 y290 w293 h237, so frame box -> asset px:
a = (f - origin) * (asset_size / box_size).

Checks:
  A. dark ink present in all 4 label anchor boxes
  B. no red (X-marker) pixels inside any label anchor box
  C. red X markers present near frame (199,445) and (270,482)
  D. red horizontal line present at frame y418 across x124..381
Usage: integrator_bl_check.py <plot_025_bl.png> [out.txt]
Prints VERDICT: PASS|FAIL plus per-check detail.
"""
import sys
import os
import numpy as np
from PIL import Image

BL_ORIGIN = (83, 290)   # frame px
BL_BOX = (293, 237)     # frame px

ANCHORS = [
    ("Global Maxima", 242, 268, 304, 319),
    ("Local Maxima", 286, 315, 337, 352),
    ("Local Minima", 286, 311, 390, 399),
    ("Global Minima", 145, 201, 439, 465),
]
RED_X = [(199, 445), (270, 482)]
RED_LINE = (418, 124, 381)  # y, x0, x1 in frame px


def redmask(a):
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    return (r > 110) & (r - g > 50) & (r - b > 50)


def darkmask(a):
    lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
    return lum < 100


def main():
    png = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else None
    im = Image.open(png).convert("RGB")
    a = np.asarray(im).astype(np.int32)
    H, W = a.shape[:2]
    sx, sy = W / BL_BOX[0], H / BL_BOX[1]

    def to_asset(x0, y0, x1, y1):
        return (int((x0 - BL_ORIGIN[0]) * sx), int((y0 - BL_ORIGIN[1]) * sy),
                int(np.ceil((x1 - BL_ORIGIN[0]) * sx)), int(np.ceil((y1 - BL_ORIGIN[1]) * sy)))

    lines = []

    def log(s=""):
        lines.append(s)
        print(s)

    log("== integrator BL check: %s (%dx%d, scale %.3f,%.3f) ==" % (png, W, H, sx, sy))
    rm = redmask(a)
    dm = darkmask(a)

    ok = True
    log("-- A/B: label anchor boxes --")
    for name, x0, x1, y0, y1 in ANCHORS:
        ax0, ay0, ax1, ay1 = to_asset(x0, y0, x1, y1)
        ax1 = min(ax1, W); ay1 = min(ay1, H)
        box = a[ay0:ay1, ax0:ax1]
        dfrac = float(dm[ay0:ay1, ax0:ax1].mean())
        rfrac = float(rm[ay0:ay1, ax0:ax1].mean())
        ink_ok = dfrac > 0.01
        nored_ok = rfrac < 0.005
        ok &= ink_ok and nored_ok
        log("  %-14s frame x%d..%d y%d..%d asset x%d..%d y%d..%d dark=%.3f red=%.4f ink=%s nored=%s" % (
            name, x0, x1, y0, y1, ax0, ax1, ay0, ay1, dfrac, rfrac,
            "OK" if ink_ok else "MISSING", "OK" if nored_ok else "RED!"))

    log("-- C: red X markers --")
    for fx, fy in RED_X:
        ax = int((fx - BL_ORIGIN[0]) * sx)
        ay = int((fy - BL_ORIGIN[1]) * sy)
        r = 12
        sub = rm[max(0, ay - r):ay + r, max(0, ax - r):ax + r]
        found = int(sub.sum()) >= 8
        ok &= found
        log("  frame (%d,%d) asset (%d,%d) red_px_in_24px_win=%d %s" % (
            fx, fy, ax, ay, int(sub.sum()), "OK" if found else "MISSING"))

    log("-- D: red line y418 x124..381 --")
    ly, lx0, lx1 = RED_LINE
    ay0, ay1 = to_asset(lx0, ly - 2, lx1, ly + 2)[1], to_asset(lx0, ly - 2, lx1, ly + 2)[3]
    ax0, _, ax1, _ = to_asset(lx0, ly - 2, lx1, ly + 2)
    ax1 = min(ax1, W)
    band = rm[ay0:ay1, ax0:ax1]
    cols = band.any(0)
    cover = float(cols.mean()) if cols.size else 0.0
    line_ok = cover > 0.8
    ok &= line_ok
    log("  frame y%d x%d..%d asset row y%d..%d x%d..%d red col coverage=%.3f %s" % (
        ly, lx0, lx1, ay0, ay1, ax0, ax1, cover, "OK" if line_ok else "MISSING"))

    log("VERDICT: %s" % ("PASS" if ok else "FAIL"))
    if out:
        with open(out, "w") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
