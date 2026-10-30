# Border scan of the ORIGINAL frame: find every long horizontal / vertical
# coloured run in the annotation-box and plot-box bands, so the box extents are
# read from the frame itself rather than inherited from the build comments.
import numpy as np
from PIL import Image
import collections

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R, G, B = O[:, :, 0], O[:, :, 1], O[:, :, 2]
V = O.max(axis=2)

GREEN = (G > R + 18) & (G > B + 18) & (G < 210)
RED = (R > 90) & ((R - G) > 35) & ((R - B) > 8)
DARK = V < 150

print("=== ORIGINAL: horizontal runs of GREEN, length>=40, rows 230..300 ===")
for y in range(230, 301):
    xs = np.nonzero(GREEN[y])[0]
    if not len(xs):
        continue
    runs = []
    s = xs[0]; p = xs[0]
    for c in xs[1:]:
        if c == p + 1:
            p = c
        else:
            runs.append((s, p)); s = c; p = c
    runs.append((s, p))
    long = [r for r in runs if r[1] - r[0] >= 40]
    if long:
        print("   y%3d  long green runs: %s   (all runs: %s)" % (y, long, runs[:8]))

print("\n=== ORIGINAL: vertical runs of GREEN, length>=30, cols 230..830 ===")
for x in range(230, 831):
    ys = np.nonzero(GREEN[:, x])[0]
    ys = ys[(ys >= 230) & (ys <= 300)]
    if len(ys) >= 30:
        print("   x%3d  green rows %d..%d  n=%d" % (x, ys.min(), ys.max(), len(ys)))

print("\n=== ORIGINAL: vertical runs of RED, length>=30, cols 230..830 ===")
for x in range(230, 831):
    ys = np.nonzero(RED[:, x])[0]
    ys = ys[(ys >= 225) & (ys <= 305)]
    if len(ys) >= 30:
        print("   x%3d  red rows %d..%d  n=%d" % (x, ys.min(), ys.max(), len(ys)))

print("\n=== ORIGINAL: horizontal runs of RED, length>=40, rows 55..320 ===")
for y in range(55, 321):
    xs = np.nonzero(RED[y])[0]
    if not len(xs):
        continue
    runs = []
    s = xs[0]; p = xs[0]
    for c in xs[1:]:
        if c == p + 1:
            p = c
        else:
            runs.append((s, p)); s = c; p = c
    runs.append((s, p))
    long = [r for r in runs if r[1] - r[0] >= 40]
    if long:
        print("   y%3d  long red runs: %s" % (y, long))

print("\n=== ORIGINAL: horizontal runs of DARK, length>=40, rows 55..320 ===")
for y in range(55, 321):
    xs = np.nonzero(DARK[y])[0]
    if not len(xs):
        continue
    runs = []
    s = xs[0]; p = xs[0]
    for c in xs[1:]:
        if c == p + 1:
            p = c
        else:
            runs.append((s, p)); s = c; p = c
    runs.append((s, p))
    long = [r for r in runs if r[1] - r[0] >= 40]
    if long:
        print("   y%3d  long dark runs: %s" % (y, long))

print("\n=== ORIGINAL: vertical runs of DARK, length>=40, cols 540..840 ===")
for x in range(540, 841):
    ys = np.nonzero(DARK[:, x])[0]
    ys = ys[(ys >= 55) & (ys <= 320)]
    if len(ys) >= 40:
        print("   x%3d  dark rows %d..%d  n=%d" % (x, ys.min(), ys.max(), len(ys)))
