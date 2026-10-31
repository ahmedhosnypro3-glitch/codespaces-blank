#!/usr/bin/env python3
"""Compare band RGB orig vs candidate renders; find what t/blend the band needs."""
import numpy as np
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location(
    "t3", "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_tune3.py")
# avoid running the grid: exec only defs up to oprof line
src = open(spec.origin).read()
src = src.split("oprof_strict =")[0]
T = importlib.util.module_from_spec(spec)
exec(src, T.__dict__)

ORIG = T.ORIG
print("orig band mean RGB per row (x672..816, colored px):")
for y in range(470, 524, 4):
    row = ORIG[y, 672:817]
    m = T.colmask(row[None, :, :])[0]
    if m.sum() > 5:
        print("  y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0)))
    else:
        print("  y=%d white" % y)

for tag, kw in [("jet", dict(blend=1.0, gray=255)),
                ("b50g150", dict(blend=0.5, gray=150)),
                ("b35g120", dict(blend=0.35, gray=120)),
                ("b60g170", dict(blend=0.6, gray=170))]:
    buf = T.render_br(1.45, 6, 0.15, kw["blend"], kw["gray"], (0.08, 0.08, 0.08, 0.7), 2, 0.45)
    ren = T.to_slide(buf)
    print("== %s ==" % tag)
    for y in range(470, 524, 6):
        row = ren[y, 672:817]
        m = T.colmask(row[None, :, :])[0]
        if m.sum() > 5:
            print("  y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0)))
        else:
            print("  y=%d white" % y)
