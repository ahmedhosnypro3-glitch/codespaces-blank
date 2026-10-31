#!/usr/bin/env python3
import numpy as np
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location(
    "t4", "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_tune4.py")
src = open(spec.origin).read().split("results = []")[0]
T = importlib.util.module_from_spec(spec)
exec(src, T.__dict__)
ORIG = T.ORIG


def rowmask(row):
    mx, mn = row.max(1), row.min(1)
    red = (row[:, 0] > 170) & (row[:, 1] < 90) & (row[:, 2] < 90)
    return ((mx - mn) > 30) & (mx > 90) & ~red


def darkfrac(row):
    lum = 0.299 * row[:, 0] + 0.587 * row[:, 1] + 0.114 * row[:, 2]
    return float(((lum < 100) & ((row.max(1) - row.min(1)) < 80)).mean())


print("orig band: y  meanRGB  darkfrac")
for y in range(472, 518, 6):
    row = ORIG[y, 672:817]
    print("  %d %s %.2f" % (y, row.mean(0).round(0), darkfrac(row)))

for tag, zoom, split, lo, hi, mesh, rs, lw in [
    ("A z1.55 s0.55 light", 1.55, 0.55, (60, 115, 155), (105, 160, 180), (0.45, 0.45, 0.45, 0.5), 3, 0.22),
    ("B z1.55 s0.45 light", 1.55, 0.45, (60, 115, 155), (105, 160, 180), (0.45, 0.45, 0.45, 0.5), 3, 0.22),
    ("C z1.55 s0.35 light", 1.55, 0.35, (60, 115, 155), (105, 160, 180), (0.45, 0.45, 0.45, 0.5), 3, 0.22),
    ("D z1.65 s0.55 light", 1.65, 0.55, (60, 115, 155), (105, 160, 180), (0.45, 0.45, 0.45, 0.5), 3, 0.22),
    ("E z1.55 s0.55 lo_dark", 1.55, 0.55, (40, 90, 130), (90, 145, 170), (0.45, 0.45, 0.45, 0.5), 3, 0.22),
]:
    cmap = T.pastel_jet(split, lo, hi)
    buf = T.render_br(zoom, 0.15, cmap, mesh, rs, lw)
    ren = T.to_slide(buf)
    mx, cells, tot = T.band_stats(ren)
    print("== %s == maxcell=%d tot=%d" % (tag, mx, tot))
    for y in range(472, 518, 12):
        row = ren[y, 672:817]
        print("  %d %s dark=%.2f" % (y, row.mean(0).round(0), darkfrac(row)))
