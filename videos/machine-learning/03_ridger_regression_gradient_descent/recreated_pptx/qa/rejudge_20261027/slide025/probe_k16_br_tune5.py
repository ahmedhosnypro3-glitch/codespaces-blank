#!/usr/bin/env python3
"""BR tune 5: focused grid around variant A; print cell grids for top candidates."""
import numpy as np
from PIL import Image
import importlib.util
spec = importlib.util.spec_from_file_location(
    "t4", "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/rejudge_20261027/slide025/probe_k16_br_tune4.py")
src = open(spec.origin).read().split("results = []")[0]
T = importlib.util.module_from_spec(spec)
exec(src, T.__dict__)
ORIG = T.ORIG
OUTD = T.OUTD

results = []
for zoom in (1.50, 1.55, 1.60):
    for split in (0.50, 0.55, 0.60):
        for mesh, rs, lw, tag in (((0.45, 0.45, 0.45, 0.5), 3, 0.22, "lm"),
                                   ((0.08, 0.08, 0.08, 0.7), 2, 0.45, "dm2"),
                                   ((0.08, 0.08, 0.08, 0.7), 3, 0.30, "dm3")):
            cmap = T.pastel_jet(split, (60, 115, 155), (105, 160, 180))
            buf = T.render_br(zoom, 0.15, cmap, mesh, rs, lw)
            ren = T.to_slide(buf)
            mx, cells, tot = T.band_stats(ren)
            results.append((mx, tot, zoom, split, tag, cells, ren))

results.sort(key=lambda r: (r[0], r[1]))
print("maxcell tot zoom split mesh")
for r in results[:10]:
    print("%3d %6d  %.2f %.2f %s" % r[:5])

for r in results[:3]:
    print("\n== maxcell=%d zoom=%.2f split=%.2f mesh=%s ==" % (r[0], r[2], r[3], r[4]))
    for row in r[5]:
        print("   ", row)

best = results[0]
ren = best[6]
Image.fromarray(ren.astype(np.uint8)).save(OUTD + "/probe_k16_br_best5.png")
print("\nwind:", T.wind_ratio(ren))
rprof = 100.0 * T.colmask(ren[:, 615:880], 30).mean(1)
r20 = [y for y in range(344, 526) if rprof[y] > 20]
print("rows>20%%: %d..%d" % (r20[0], r20[-1]))
# cell means orig vs render for worst cell
mx, cells, tot = T.band_stats(ren)
worst = max(((cells[iy][ix], iy, ix) for iy in range(5) for ix in range(12)))
_, iy, ix = worst
bx0, by0, bx1, by1 = 672, 472, 816, 517
H, W = by1 - by0, bx1 - bx0
cy0, cy1 = iy * H // 5, (iy + 1) * H // 5
cx0, cx1 = ix * W // 12, (ix + 1) * W // 12
print("worst cell iy=%d ix=%d diff=%d" % (iy, ix, cells[iy][ix]))
print("orig cell mean", ORIG[by0 + cy0:by0 + cy1, bx0 + cx0:bx0 + cx1].mean((0, 1)).round(0))
print("rend cell mean", ren[by0 + cy0:by0 + cy1, bx0 + cx0:bx0 + cx1].mean((0, 1)).round(0))
