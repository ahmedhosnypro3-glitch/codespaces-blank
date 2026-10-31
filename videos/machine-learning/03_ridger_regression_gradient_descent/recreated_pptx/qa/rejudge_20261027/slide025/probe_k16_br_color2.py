#!/usr/bin/env python3
import numpy as np
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location(
    "t3", "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_tune3.py")
src = open(spec.origin).read().split("oprof_strict =")[0]
T = importlib.util.module_from_spec(spec)
exec(src, T.__dict__)

ORIG = T.ORIG


def rowmask(row):
    mx, mn = row.max(1), row.min(1)
    red = (row[:, 0] > 170) & (row[:, 1] < 90) & (row[:, 2] < 90)
    return ((mx - mn) > 30) & (mx > 90) & ~red


print("orig band mean RGB (x672..816):")
for y in range(468, 526, 4):
    row = ORIG[y, 672:817]
    m = rowmask(row)
    print("  y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0) if m.sum() else "-"))

for tag, kw in [("jet", (1.0, 255)), ("b50g150", (0.5, 150)), ("b35g120", (0.35, 120))]:
    buf = T.render_br(1.45, 6, 0.15, kw[0], kw[1], (0.08, 0.08, 0.08, 0.7), 2, 0.45)
    ren = T.to_slide(buf)
    print("== %s ==" % tag)
    for y in range(468, 526, 6):
        row = ren[y, 672:817]
        m = rowmask(row)
        print("  y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0) if m.sum() else "-"))
    mx, cells = T.band_stats(ren)
    print("  maxcell=%d" % mx)
