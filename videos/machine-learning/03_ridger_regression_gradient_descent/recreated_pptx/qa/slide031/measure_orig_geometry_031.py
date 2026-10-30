# Exhaustive measurement of the ORIGINAL frame's plot box, grid, axes, and
# annotation box, so the recreation can be re-specified from the frame itself.
import numpy as np
from PIL import Image
import collections

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R, G, B = O[:, :, 0], O[:, :, 1], O[:, :, 2]
V = O.max(axis=2)

red = (R > 90) & ((R - G) > 35) & ((R - B) > 8)
green = (G > R + 18) & (G > B + 18) & (G < 210)

print("=== A. plot-box outer RED rectangle: row profile of red, x 560..820, rows 60..315 ===")
for y in range(60, 316):
    xs = np.nonzero(red[y, 560:821])[0] + 560
    if len(xs):
        runs = []
        s = xs[0]; p = xs[0]
        for c in xs[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p)); s = c; p = c
        runs.append((s, p))
        wide = [r for r in runs if r[1] - r[0] > 100]
        if wide:
            print("   y%3d wide-red run %s" % (y, wide))

print("\n=== B. plot-box LEFT/RIGHT red vertical: per-column red count rows 60..315 ===")
for x in range(565, 585):
    n = int(red[60:316, x].sum())
    if n > 50:
        print("   x%3d red n=%d" % (x, n))
print("   ...")
for x in range(803, 816):
    n = int(red[60:316, x].sum())
    if n > 50:
        print("   x%3d red n=%d" % (x, n))

print("\n=== C. light-gray GRID lines (gray, 195..232) in the plot ===")
gray = (abs(R - G) < 8) & (abs(G - B) < 8) & (V >= 195) & (V <= 233)
print("  vertical grid columns (count in rows 70..300):")
for x in range(565, 815):
    n = int(gray[70:301, x].sum())
    if n > 150:
        print("     x%3d n=%d  sample(200,x)=%s" % (x, n, tuple(O[200, x])))
print("  horizontal grid rows (count in x 585..800):")
for y in range(60, 315):
    n = int(gray[y, 585:801].sum())
    if n > 120:
        print("     y%3d n=%d  sample(y,690)=%s" % (y, n, tuple(O[y, 690])))

print("\n=== D. BLACK axis lines ===")
blk = V < 150
print("  vertical black runs (>=40 rows) in x 560..820:")
for x in range(560, 821):
    ys = np.nonzero(blk[55:320, x])[0] + 55
    if len(ys) >= 40:
        runs = []
        s = ys[0]; p = ys[0]
        for c in ys[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p)); s = c; p = c
        runs.append((s, p))
        print("     x%3d n=%3d runs=%s" % (x, len(ys), runs[:5]))
print("  horizontal black runs (>=60 cols) in rows 60..315:")
for y in range(60, 316):
    xs = np.nonzero(blk[y, 560:821])[0] + 560
    if len(xs) >= 60:
        runs = []
        s = xs[0]; p = xs[0]
        for c in xs[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((s, p)); s = c; p = c
        runs.append((s, p))
        print("     y%3d n=%3d runs=%s" % (y, len(xs), runs[:5]))

print("\n=== E. green (5,1) marker: saturated-green blob in x 640..740, y 230..280 ===")
for y in range(230, 281):
    xs = np.nonzero(green[y, 640:741])[0] + 640
    if len(xs):
        print("   y%3d n=%2d x %d..%d" % (y, len(xs), xs.min(), xs.max()))
print("  raw samples inside the blob:")
for (x, y) in [(680, 250), (685, 252), (690, 253), (695, 250), (678, 248), (699, 254), (686, 256)]:
    print("     (%3d,%3d) = %s" % (x, y, tuple(O[y, x])))

print("\n=== F. plot interior fill colour (original) vs panel ===")
for (x, y) in [(620, 120), (700, 180), (760, 290), (620, 290), (700, 300), (790, 110)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(O[y, x])))

print("\n=== G. annotation box: green border rows/cols ===")
for y in range(238, 250):
    xs = np.nonzero(green[y, 235:575])[0] + 235
    if len(xs) > 100:
        print("   top-ish y%3d green x %d..%d n=%d" % (y, xs.min(), xs.max(), len(xs)))
for y in range(283, 295):
    xs = np.nonzero(green[y, 235:575])[0] + 235
    if len(xs) > 100:
        print("   bot-ish y%3d green x %d..%d n=%d" % (y, xs.min(), xs.max(), len(xs)))
for x in range(238, 250):
    ys = np.nonzero(green[235:295, x])[0] + 235
    if len(ys) > 30:
        print("   left-ish x%3d green y %d..%d n=%d" % (x, ys.min(), ys.max(), len(ys)))
for x in range(560, 575):
    ys = np.nonzero(green[235:295, x])[0] + 235
    if len(ys) > 30:
        print("   right-ish x%3d green y %d..%d n=%d" % (x, ys.min(), ys.max(), len(ys)))
print("   annotation interior modal:")
reg = O[246:288, 248:562].reshape(-1, 3)
print("     ", collections.Counter(map(tuple, reg // 4 * 4)).most_common(4))
print("     median", np.median(reg, axis=0))
