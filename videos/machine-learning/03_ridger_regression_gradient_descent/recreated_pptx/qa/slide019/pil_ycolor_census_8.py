#!/usr/bin/env python3
"""Colour census of the y= value cells, slide 019 original vs render_8.

Question: the build paints every 'y=<value>' glyph green (#008000, per
analysis/slide_019_final.json).  judge_attempt_6 MINOR #3 claimed the ORIGINAL
carries 'small green per-component figures flanking the W labels' and the render
omits them.  pil_green_adjud_8.py already showed the original has ZERO green in
the W-label zone (frame x124..206) for all three row groups.

This script answers the follow-up: where does green live in the ORIGINAL at all,
and what colour are the original's y= glyphs in every column group / row group?

Row-group tops are the build's measured values: 205 / 310 / 420 (frame px).
The 'y=' line is the third line of the test block (block top = gy+25), so the
glyph band is approx gy+43 .. gy+55.  A +/-4 px pad is used.
Phantom-trap law: an ink column/row counts only with >=3 px of ink.
"""
from PIL import Image
import numpy as np

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_019.jpg")

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
R = np.asarray(Image.open(f"{Q}/render_8.png").convert("RGB")).astype(np.int16)
SX, SY = R.shape[1] / 960.0, R.shape[0] / 540.0


def is_green(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (g > r + 15) & (g > b + 15) & (g > 60) & (g < 235)


def is_dark(a):
    return a.mean(axis=2) < 120


def is_red(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    return (r > g + 40) & (r > b + 40) & (r > 90)


def census(a, x0, x1, y0, y1):
    band = a[y0:y1, x0:x1]
    g, d, rd = is_green(band), is_dark(band), is_red(band)
    gcols = np.nonzero(g.sum(axis=0) >= 3)[0]
    dcols = np.nonzero(d.sum(axis=0) >= 3)[0]
    return int(g.sum()), len(gcols), int(d.sum()), len(dcols), int(rd.sum())


print("=" * 78)
print("A — whole-frame green census (where does green live in each image?)")
print("=" * 78)
for label, arr in (("original", O), ("render_8", R)):
    g = is_green(arr)
    cols = np.nonzero(g.sum(axis=0) >= 3)[0]
    rows = np.nonzero(g.sum(axis=1) >= 3)[0]
    print(f"  {label:9s} green px={int(g.sum()):6d}  cols>=3px={len(cols):4d} "
          f"rows>=3px={len(rows):4d}")
    if len(cols):
        # group contiguous column runs
        runs, s = [], cols[0]
        for p, q in zip(cols, cols[1:]):
            if q != p + 1:
                runs.append((s, p))
                s = q
        runs.append((s, cols[-1]))
        runs = [r for r in runs if r[1] - r[0] >= 2]
        shown = runs[:12]
        print(f"            green col runs (>=3px wide): {len(runs)}  first: "
              + ", ".join(f"x{a}..{b}" for a, b in shown))
    print()

print("=" * 78)
print("B — y= value-cell colour, per column group x per row group")
print("=" * 78)
COLS = [
    ("NO REG  ", 124, 380),
    ("RIDGE 3 ", 384, 640),
    ("RIDGE 10", 644, 900),
]
ROWY = [(205, "row1"), (310, "row2"), (420, "row3")]

for name, x0, x1 in COLS:
    test_x0 = x0 + 82
    test_w = (x1 - x0 - 82) / 3.0
    print(f"  {name}  (test boxes x{test_x0:.0f}..{x1})")
    for gy, rname in ROWY:
        y0, y1 = gy + 40, gy + 58
        og = census(O, int(test_x0), x1, y0, y1)
        rg = census(R, int(test_x0 * SX), int(x1 * SX), int(y0 * SY), int(y1 * SY))
        print(f"    {rname} y{y0}..{y1}  original: green={og[0]:5d}px/cols{og[1]:3d} "
              f"dark={og[2]:5d}px/cols{og[3]:3d} red={og[4]:4d}   |   "
              f"render_8: green={rg[0]:5d}px/cols{rg[1]:3d} "
              f"dark={rg[2]:5d}px/cols{rg[3]:3d} red={rg[4]:4d}")
    print()

print("=" * 78)
print("C — per-test-box y= line (NO REG rows 1-3, the disputed column)")
print("=" * 78)
for gy, rname in ROWY:
    y0, y1 = gy + 40, gy + 58
    for ti in range(3):
        bx0 = 206 + ti * 58
        bx1 = bx0 + 58
        og = census(O, bx0, bx1, y0, y1)
        rg = census(R, int(bx0 * SX), int(bx1 * SX), int(y0 * SY), int(y1 * SY))
        print(f"  {rname} test{ti + 1} x{bx0}..{bx1}:  original green={og[0]:4d} "
              f"dark={og[2]:4d}   |  render_8 green={rg[0]:4d} dark={rg[2]:4d}")
    print()

print("=" * 78)
print("D — mean RGB of the darkest ink pixels in the NO REG row2/row3 y= cells")
print("=" * 78)
for gy, rname in ((310, "row2"), (420, "row3")):
    y0, y1 = gy + 40, gy + 58
    band = O[y0:y1, 206:380]
    lum = band.mean(axis=2)
    thr = np.percentile(lum, 99)
    sel = band[lum <= thr]
    print(f"  original {rname}  darkest-1% mean RGB = "
          f"({sel[:, 0].mean():.0f}, {sel[:, 1].mean():.0f}, {sel[:, 2].mean():.0f})"
          f"  min lum={lum.min():.0f}")
    rband = R[int(y0 * SY):int(y1 * SY), int(206 * SX):int(380 * SX)]
    rlum = rband.mean(axis=2)
    rthr = np.percentile(rlum, 99)
    rsel = rband[rlum <= rthr]
    print(f"  render_8 {rname} darkest-1% mean RGB = "
          f"({rsel[:, 0].mean():.0f}, {rsel[:, 1].mean():.0f}, {rsel[:, 2].mean():.0f})"
          f"  min lum={rlum.min():.0f}")
