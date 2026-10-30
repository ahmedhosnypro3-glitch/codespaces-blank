#!/usr/bin/env python3
"""Final probes: vector bboxes, box2 subscript, remember-box border."""
import numpy as np
from PIL import Image

D = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = np.asarray(Image.open(D + "/unique_slides/slide_004.jpg").convert("RGB")).astype(int)

def masks(a):
    R, G, B = a[..., 0], a[..., 1], a[..., 2]
    red = (R > 125) & (R - G > 35) & (R - B > 20)
    dark = (a.max(axis=-1) < 165) & ~red
    return red, dark

print("=== Q1: box1 vector red-ink bbox x150..225 y100..218 ===")
reg = o[100:218, 150:225]
red, dark = masks(reg)
ys, xs = np.nonzero(red)
print("  red bbox: x%d..%d y%d..%d  n=%d" % (150+xs.min(), 150+xs.max(), 100+ys.min(), 100+ys.max(), red.sum()))
rows = np.flatnonzero(red.any(axis=1))
print("  red row spans (contiguous):")
for s in np.split(rows, np.flatnonzero(np.diff(rows) > 2) + 1):
    sub = red[s[0]:s[-1]+1]
    xs2 = np.flatnonzero(sub.any(axis=0))
    print("    y%d..%d x%d..%d" % (100+s[0], 100+s[-1], 150+xs2.min(), 150+xs2.max()))

print("=== Q1b: box2 vector red-ink bbox x495..570 y100..218 ===")
reg = o[100:218, 495:570]
red, dark = masks(reg)
ys, xs = np.nonzero(red)
print("  red bbox: x%d..%d y%d..%d  n=%d" % (495+xs.min(), 495+xs.max(), 100+ys.min(), 100+ys.max(), red.sum()))
rows = np.flatnonzero(red.any(axis=1))
for s in np.split(rows, np.flatnonzero(np.diff(rows) > 2) + 1):
    sub = red[s[0]:s[-1]+1]
    xs2 = np.flatnonzero(sub.any(axis=0))
    print("    y%d..%d x%d..%d" % (100+s[0], 100+s[-1], 495+xs2.min(), 495+xs2.max()))

print("=== Q2: box2 subscript search x540..660 y185..232 (red then dark) ===")
reg = o[185:232, 540:660]
red, dark = masks(reg)
for nm, m in (("red", red), ("dark", dark)):
    ys, xs = np.nonzero(m)
    if ys.size == 0:
        print("  %s: none" % nm); continue
    print("  %s bbox: x%d..%d y%d..%d n=%d" % (nm, 540+xs.min(), 540+xs.max(), 185+ys.min(), 185+ys.max(), m.sum()))
    rows = np.flatnonzero(m.any(axis=1))
    for s in np.split(rows, np.flatnonzero(np.diff(rows) > 3) + 1):
        sub = m[s[0]:s[-1]+1]
        xs2 = np.flatnonzero(sub.any(axis=0))
        print("    y%d..%d x%d..%d" % (185+s[0], 185+s[-1], 540+xs2.min(), 540+xs2.max()))

print("=== Q3: remember box border probe x780..885 y96..156 ===")
reg = o[96:156, 780:885]
red, dark = masks(reg)
edges = {
    "top y96..102": red[0:6, :], "bottom y150..156": red[54:60, :],
    "left x780..788": red[:, 0:8], "right x877..885": red[:, 97:105],
}
for tag, m in edges.items():
    print("  %s: red=%d" % (tag, m.sum()))
# where exactly along the perimeter?
ys, xs = np.nonzero(red)
if ys.size:
    print("  all red bbox: x%d..%d y%d..%d n=%d" % (780+xs.min(), 780+xs.max(), 96+ys.min(), 96+ys.max(), red.sum()))
