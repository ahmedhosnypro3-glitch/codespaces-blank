#!/usr/bin/env python3
"""Pink-box row-count adjudication for slide 050 (render_13 vs original vs PNG asset).
w7 proved the ORIGINAL construct is 2-row (5 / -1). The current eq_050_finalW.json
sidecar claims a 3-row substack. Decide what the RENDER actually shows."""
import numpy as np
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
NS = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide050"

def row_runs(ink, axis_name):
    rows = np.where(ink.any(axis=1))[0]
    if len(rows) == 0:
        print("  %s: no ink" % axis_name)
        return []
    runs, s = [], rows[0]
    for a, b in zip(rows, rows[1:]):
        if b - a > 2:
            runs.append((s, a)); s = b
    runs.append((s, rows[-1]))
    print("  %s ink-row runs (start..end,height): %s" % (axis_name, [(int(a), int(b), int(b-a+1)) for a, b in runs]))
    return runs

# --- 1. the PNG asset itself (600dpi transparent) ---
im = Image.open(NS + "/recreated_pptx/build/assets/eq_050_finalW.png")
a = np.asarray(im)
print("asset eq_050_finalW.png mode=%s size=%s" % (im.mode, im.size))
ink = a[:, :, 3] > 8 if a.shape[2] == 4 else (a.mean(axis=2) < 200)
runs = row_runs(ink, "asset")
print("  asset digit-row count (gap>2px runs): %d" % len(runs))

# --- 2. render_13 pink box, frame x735..836 y52..178, scale 2001/960 ---
r = Image.open(QA + "/render_13.png").convert("RGB")
SC = r.size[1] / 540.0
print("\nrender_13 %s scale=%.4f" % (r.size, SC))
x0, y0, x1, y1 = int(743*SC), int(58*SC), int(830*SC), int(171*SC)
rc = np.asarray(r.crop((x0, y0, x1, y1)))
lum = rc.mean(axis=2)
ink = lum < 200
runs = row_runs(ink, "render pinkbox (frame x743..830 y58..171)")
# column profile of the construct zone to find parens vs digits
cols = np.where(ink.any(axis=0))[0]
print("  render ink columns %d..%d (rel), abs %d..%d" % (cols[0], cols[-1], x0+cols[0], x0+cols[-1]))
# print ascii of the render construct
print("\nrender pinkbox ascii (x=%d..%d y=%d..%d, lum<200):" % (x0, x1, y0, y1))
ys, xs = np.where(ink)
if len(ys):
    for yy in range(ys.min(), ys.max()+1, 2):
        line = "".join("#" if ink[yy, xx] else "." for xx in range(0, rc.shape[1], 2))
        print("%4d %s" % (y0+yy, line))

# --- 3. original pink box, same frame coords ---
o = Image.open(NS + "/unique_slides/slide_050.jpg").convert("RGB")
oc = np.asarray(o.crop((743, 58, 830, 171)))
lum = oc.mean(axis=2)
ink = lum < 200
print("\norig pinkbox ascii (frame x743..830 y58..171, lum<200):")
row_runs(ink, "orig pinkbox")
ys, xs = np.where(ink)
if len(ys):
    for yy in range(ys.min(), ys.max()+1):
        line = "".join("#" if ink[yy, xx] else "." for xx in range(0, oc.shape[1]))
        print("%4d %s" % (58+yy, line))
