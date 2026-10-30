#!/usr/bin/env python3
"""Map orig rule positions in test-grid zones + outlier blue x-extent (frame space)."""
from PIL import Image
import numpy as np

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
oi = Image.open(f"{V}/unique_slides/slide_019.jpg").convert("RGB")
ri = Image.open(f"{V}/recreated_pptx/qa/slide019/render_20.png").convert("RGB")
oa = np.asarray(oi).astype(int)
ra = np.asarray(ri).astype(int)
RS = ri.size[0] / 960.0

def dark(a):
    return a.sum(axis=2) < 480

print("=== 1. OUTLIER x-extent of colored ink (orig), per row cluster ===")
ow = oa[190:300, 78:118]
r, g, b = ow[..., 0], ow[..., 1], ow[..., 2]
blue = (b > 120) & (b - r > 50) & (b - g > 40)
for y0, y1 in [(199, 210), (219, 233), (236, 239), (244, 261), (269, 284)]:
    m = blue[y0-190:y1-190]
    xs = np.nonzero(m.any(axis=0))[0]
    if len(xs):
        # column runs
        runs, st = [], xs[0]
        for i in range(1, len(xs)):
            if xs[i] != xs[i-1] + 1:
                runs.append((st, xs[i-1])); st = xs[i]
        runs.append((st, xs[-1]))
        print(f"  y{y0}..{y1}: x runs " + ", ".join(f"{78+a}..{78+b_}" for a, b_ in runs))
    else:
        print(f"  y{y0}..{y1}: none")

print("=== 2. ORIG horizontal rule rows (dark cols count>30) in grid zones ===")
def hscan(tag, x0, x1, y0, y1, a=oa):
    d = dark(a[y0:y1, x0:x1])
    counts = d.sum(axis=1)
    rows = np.nonzero(counts > 30)[0]
    if len(rows) == 0:
        print(f"  {tag}: none"); return
    runs, st = [], rows[0]
    for i in range(1, len(rows)):
        if rows[i] != rows[i-1] + 1:
            runs.append((st, rows[i-1])); st = rows[i]
    runs.append((st, rows[-1]))
    out = ", ".join(f"y{y0+a_}..{y0+b_}(w{int(counts[a_:b_+1].mean())})" for a_, b_ in runs)
    print(f"  {tag}: {out}")

def vscan(tag, x0, x1, y0, y1, a=oa):
    d = dark(a[y0:y1, x0:x1])
    counts = d.sum(axis=0)
    cols = np.nonzero(counts > 25)[0]
    if len(cols) == 0:
        print(f"  {tag}: none"); return
    runs, st = [], cols[0]
    for i in range(1, len(cols)):
        if cols[i] != cols[i-1] + 1:
            runs.append((st, cols[i-1])); st = cols[i]
    runs.append((st, cols[-1]))
    out = ", ".join(f"x{x0+a_}..{x0+b_}(h{int(counts[a_:b_+1].mean())})" for a_, b_ in runs)
    print(f"  {tag}: {out}")

print("-- NO REG grid zone x208..378, y205..300 (orig):")
hscan("hlines", 208, 378, 205, 300)
vscan("vlines", 208, 378, 210, 296)
print("-- RIDGE3 grid zone x468..638, y205..300 (orig):")
hscan("hlines", 468, 638, 205, 300)
vscan("vlines", 468, 638, 210, 296)
print("-- NO REG W-zone x130..204, y205..300 (orig):")
hscan("hlines", 130, 204, 205, 300)
vscan("vlines", 130, 204, 210, 296)
print("-- same zones in RENDER_20 (frame space):")
hscan("hlines", 208, 378, 205, 300, ra)
vscan("vlines", 208, 378, 210, 296, ra)
hscan("hlines", 468, 638, 205, 300, ra)
vscan("vlines", 468, 638, 210, 296, ra)
print("=== 3. ORIG right-edge of test grid (x376..384) hue, group1 ===")
d = oa[210:296, 376:384]
dm = dark(d)
print(f"  n={int(dm.sum())}", end=" ")
if dm.sum():
    rr, gg, bb = d[..., 0][dm], d[..., 1][dm], d[..., 2][dm]
    print(f"mean rgb ({int(rr.mean())},{int(gg.mean())},{int(bb.mean())})")
    xs = np.nonzero(dm.any(axis=0))[0]
    print(f"  x cols with ink: {[376+int(x_) for x_ in xs]}")
else:
    print()
