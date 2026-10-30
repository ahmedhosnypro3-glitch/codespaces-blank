"""DEFINITIVE slide_022 measurement: per-row exact boxes, fills, borders, ink colors."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hx(px):
    return "#%02x%02x%02x" % tuple(int(v) for v in px)

# ---- masks ----
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2)
xn = a.min(axis=2)
sat = mx - xn

peach = (R > 235) & (G > 185) & (G < 250) & (B > 160) & (B < 245) & (R - B > 12) & (R - B < 45) & (sat > 15)
pyellow = (R > 240) & (G > 235) & (B > 175) & (B < 252) & (G - B >= 5) & (G - B < 40) & (sat > 5)
white = (mx > 243) & (sat < 10)
graybg = (abs(R - 240) < 12) & (abs(G - 240) < 12) & (abs(B - 240) < 12) & (sat < 12)
redtxt = (R > 100) & (R - G > 65) & (R - B > 65) & (G < 120)
grntxt = (G > 85) & (G - R > 35) & (G - B > 35)
blktxt = (mx < 140) & (sat < 80)

print("=== mask counts: peach=%d pyellow=%d redtxt=%d green=%d black=%d" % (
    peach.sum(), pyellow.sum(), redtxt.sum(), grntxt.sum(), blktxt.sum()))

ROWS = [(112, 184), (216, 270), (316, 372), (418, 500)]
for i, (y0, y1) in enumerate(ROWS, 1):
    print("\n########## ROW %d  y=%d..%d ##########" % (i, y0, y1))
    for nm, m in [("peach", peach), ("pyellow", pyellow), ("redtxt", redtxt), ("green", grntxt), ("black", blktxt)]:
        sub = m[y0:y1]
        ys, xs = np.where(sub)
        if len(xs) == 0:
            print("  %-8s : none" % nm)
            continue
        # x extent of contiguous-ish region (allow 6px gaps)
        cols = np.zeros(W, bool)
        cols[xs] = True
        runs, st = [], None
        for x in range(W):
            if cols[x] and st is None:
                st = x
            elif not cols[x] and st is not None:
                runs.append((st, x - 1)); st = None
        if st is not None:
            runs.append((st, W - 1))
        merged = []
        for r in runs:
            if merged and r[0] - merged[-1][1] <= 8:
                merged[-1] = (merged[-1][0], r[1])
            else:
                merged.append(r)
        merged = [r for r in merged if r[1] - r[0] > 12]
        print("  %-8s : x=%s   y=%d..%d  n=%d" % (nm, merged, ys.min() + y0, ys.max() + y0, sub.sum()))
