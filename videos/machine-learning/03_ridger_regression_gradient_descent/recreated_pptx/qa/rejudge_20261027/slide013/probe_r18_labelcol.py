#!/usr/bin/env python3
"""r18 slide013 targeted probe: does the ORIGINAL test table have a row-label
column (X1/X2/y) that the recreation lacks? Slide-space px."""
from PIL import Image
import numpy as np

NS = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_013.jpg").convert("L")).astype(int)
r = np.asarray(Image.open(f"{NS}/recreated_pptx/qa/rejudge_20261027/slide013/render.png").convert("L")).astype(int)
sy = r.shape[0] / 540.0
sx = r.shape[1] / 960.0

# 1) render: where is the test table? ink row profile x600-900
sub = r[:, int(600 * sx):int(900 * sx)] < 200
rows = [(y, int(sub[int(y * sy):int((y + 10) * sy)].sum())) for y in range(0, 540, 10)]
print("RENDER ink per 10px row band, x600-900:", rows)

# 2) render test-table vlines in its actual band (find band with most ink first)
best = max(rows, key=lambda t: t[1])[0]
y0, y1 = best, best + 60
reg = r[int(y0 * sy):int((y1 + 100) * sy), int(600 * sx):int(900 * sx)] < 200
cf = reg.mean(axis=0)
out = []
for i, v in enumerate(cf):
    if v > 0.35:
        x = 600 + i / sx
        if out and x - out[-1][-1] < 2:
            out[-1].append(x)
        else:
            out.append([x])
print(f"RENDER vlines y{y0}-{y1+100} x600-900:", [round(sum(g) / len(g), 1) for g in out])

# 3) orig test label column glyph strips vs train label column glyph strips
#    test label col x671-718; train label col: train table left edge ~x92, first col ~92-141
def strip(a, x0, x1, y0, y1, thr, s=1.0):
    reg = a[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]
    return reg < thr

print("ORIG test-label col ink (hdr/r1/r2/r3):",
      [int(strip(o, 671, 718, y0, y1, 200).sum()) for y0, y1 in [(130, 159), (161, 189), (191, 220), (222, 250)]])
# train table: vlines within x90-460 y95-265 were fragmented; use label col x93-140
print("ORIG train-label col ink (guess x93-140, rows 130-250):")
rf = (o[95:265, 90:465] < 200).mean(axis=1)
hl = [95 + i for i, v in enumerate(rf) if v > 0.25]
print("  train hlines(>0.25):", hl)
for y0, y1 in [(130, 159), (161, 189), (191, 220), (222, 250)]:
    print("  train-label", y0, y1, int(strip(o, 93, 140, y0, y1, 200).sum()))

# 4) render: ink in the slide-space zone x669-720 (orig label col) per test row
print("RENDER ink in x669-720 y130-250 (orig label-col zone):",
      int((r[int(130 * sy):int(250 * sy), int(669 * sx):int(720 * sx)] < 200).sum()))
# and render test header text location: col runs of ink in y130-159
rego = r[int(130 * sy):int(159 * sy), int(600 * sx):int(900 * sx)] < 200
cs = rego.sum(axis=0)
runs = []
inr = False
for i, v in enumerate(cs):
    x = 600 + i / sx
    if v > 1 and not inr:
        st = x; inr = True
    elif v <= 1 and inr:
        runs.append((round(st, 1), round(x, 1))); inr = False
if inr: runs.append((round(st, 1), 900.0))
print("RENDER header-row y130-159 ink col runs x600-900:", runs)
