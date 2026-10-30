"""Precisely locate left (red-bordered) and right (blue-bordered) boxes per row."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
redish = (R > 110) & (R - G > 55) & (R - B > 55)
bluish = (B > 80) & (B - R > 45) & (B - G > 45)
greenish = (G > 80) & (G - R > 40) & (G - B > 40)
print("redish=%d bluish=%d greenish=%d" % (redish.sum(), bluish.sum(), greenish.sum()))

for row, (y0, y1) in enumerate([(110, 208), (208, 306), (306, 405), (405, 504)], 1):
    print("\n=== ROW %d  y=%d..%d ===" % (row, y0, y1))
    for name, m in [("red", redish), ("blue", bluish)]:
        sub = m[y0:y1]
        colsum = sub.sum(axis=0)
        cols = [i for i, c in enumerate(colsum) if c > (y1 - y0) * 0.45]
        # group consecutive
        groups = []
        for c in cols:
            if groups and c - groups[-1][-1] <= 2:
                groups[-1].append(c)
            else:
                groups.append([c])
        print("  %s vertical-border cols: %s" % (name, [(g[0], g[-1]) for g in groups]))
        rowsum = sub.sum(axis=1)
        rows = [i for i, c in enumerate(rowsum) if c > 120]
        gg = []
        for r in rows:
            if gg and r - gg[-1][-1] <= 2:
                gg[-1].append(r)
            else:
                gg.append([r])
        print("  %s horizontal-border rows(abs): %s" % (name, [(g[0] + y0, g[-1] + y0) for g in gg]))
    sub_g = greenish[y0:y1]
    ys, xs = np.where(sub_g)
    if len(xs):
        print("  greenish bbox x:%d-%d y:%d-%d n=%d" % (xs.min(), xs.max(), ys.min() + y0, ys.max() + y0, sub_g.sum()))
