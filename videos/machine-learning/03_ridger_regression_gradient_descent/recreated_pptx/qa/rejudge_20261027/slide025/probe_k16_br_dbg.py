#!/usr/bin/env python3
import sys
sys.path.insert(0, "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025")
import numpy as np
from PIL import Image
import probe_k16_br_tune as T

ORIG = T.ORIG
# orig band mean color per row (x672..816), rows 470..526
print("orig band rows (mean RGB of colored px):")
for y in range(470, 527, 4):
    row = ORIG[y, 672:817]
    mx, mn = row.max(1), row.min(1)
    m = ((mx - mn) > 30) & (mx > 90)
    if m.sum() > 5:
        print("  y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0)))
    else:
        print("  y=%d n=0 (white)" % y)

for shade in (False, True):
    for zoom in (0.5, 0.7, 0.9):
        buf = T.render_br(0.0, zoom, 0.15, shade, 0.5)
        ren = T.to_slide(buf)
        rprof = T.row_profile(ren, 615, 880)
        r20 = [y for y in range(344, 526) if rprof[y] > 20]
        mx, _ = T.band_maxcell(ren)
        print("shade=%d zoom=%.2f rows>20%%: %s..%s  maxcell=%d" % (
            shade, zoom, r20[0] if r20 else -1, r20[-1] if r20 else -1, mx))
        if zoom == 0.7:
            print("  band rows:")
            for y in range(470, 527, 6):
                row = ren[y, 672:817]
                mx2, mn2 = row.max(1), row.min(1)
                m = ((mx2 - mn2) > 30) & (mx2 > 90)
                if m.sum() > 5:
                    print("    y=%d n=%3d mean=%s" % (y, m.sum(), row[m].mean(0).round(0)))
                else:
                    print("    y=%d n=0 white" % y)
