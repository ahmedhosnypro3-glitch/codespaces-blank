"""Per-row box extents, border families, and ink color census for slide_022 original."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn

def hx(px):
    return "#%02x%02x%02x" % tuple(int(v) for v in px)

# gold/olive border family: R,G mid-high, B lower
gold = (R > 120) & (G > 95) & (B < 170) & (R - B > 35) & (G - B > 15) & (mx < 225)
# muted red border family (peach-adjacent red)
mred = (R > 140) & (R - G > 60) & (R - B > 60) & (mx < 235)
# strong saturated red TEXT
sred = (R > 120) & (R - G > 80) & (R - B > 80) & (G < 110)
# green text
grn = (G > 90) & (G - R > 45) & (G - B > 45)
# black text
blk = (mx < 120) & (sat < 70)

print("gold=%d mred=%d sred=%d green=%d black=%d" % (gold.sum(), mred.sum(), sred.sum(), grn.sum(), blk.sum()))

ROWS = [(110, 208), (208, 306), (306, 405), (405, 504)]
for i, (y0, y1) in enumerate(ROWS, 1):
    print("\n===== ROW %d (y %d..%d) =====" % (i, y0, y1))
    for nm, m in [("gold", gold), ("mred", mred), ("sred", sred), ("green", grn)]:
        sub = m[y0:y1]
        ys, xs = np.where(sub)
        if len(xs):
            print("  %-6s bbox x:%3d-%3d y:%3d-%3d n=%d" % (nm, xs.min(), xs.max(), ys.min() + y0, ys.max() + y0, sub.sum()))
        else:
            print("  %-6s none" % nm)

print("\n=== GOLD pixels: row/col profile ===")
for i, (y0, y1) in enumerate(ROWS, 1):
    sub = gold[y0:y1]
    colhits = sub.sum(axis=0)
    cols = [x for x in range(W) if colhits[x] > 0]
    gg = []
    for x in cols:
        if gg and x - gg[-1][-1] <= 3:
            gg[-1].append(x)
        else:
            gg.append([x])
    rowhits = sub.sum(axis=1)
    rows = [y + y0 for y in range(y1 - y0) if rowhits[y] > 0]
    rg = []
    for y in rows:
        if rg and y - rg[-1][-1] <= 3:
            rg[-1].append(y)
        else:
            rg.append([y])
    print("  row%d gold colgroups=%s" % (i, [(g[0], g[-1]) for g in gg]))
    print("       gold rowgroups=%s" % ([(g[0], g[-1]) for g in rg],))
