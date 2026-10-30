"""Definitive slide_022 measurement: all vertical border lines, fills, text colors."""
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

CY0, CY1 = 110, 503  # container top/bottom

print("=== vertical line scan over content rows (y 110..503) ===")
for name, m in [("red", redish), ("blue", bluish), ("green", greenish)]:
    colsum = m[CY0:CY1].sum(axis=0)
    cols = [i for i, c in enumerate(colsum) if c > 60]
    groups = []
    for c in cols:
        if groups and c - groups[-1][-1] <= 2:
            groups[-1].append(c)
        else:
            groups.append([c])
    print("  %s lines:" % name, [(g[0], g[-1], int(colsum[g].sum())) for g in groups])

print("\n=== per-row horizontal line scan (border tops/bottoms) ===")
for row, (y0, y1) in enumerate([(110, 208), (208, 306), (306, 405), (405, 503)], 1):
    for name, m in [("red", redish), ("blue", bluish)]:
        rowsum = m[y0:y1].sum(axis=1)
        rows = [i for i, c in enumerate(rowsum) if c > 150]
        gg = []
        for r in rows:
            if gg and r - gg[-1][-1] <= 2:
                gg[-1].append(r)
            else:
                gg.append([r])
        ggf = [(g[0] + y0, g[-1] + y0) for g in gg]
        if ggf:
            print("  row%d %s horiz groups: %s" % (row, name, ggf))

print("\n=== fill-region scan: uniform horizontal runs per row ===")
for row, (y0, y1) in enumerate([(110, 208), (208, 306), (306, 405), (405, 503)], 1):
    band = a[y0 + 8:y1 - 8]
    # median color per column
    med = np.median(band, axis=0)
    runs = []
    start = 0
    for i in range(1, band.shape[1] + 1):
        if i == band.shape[1] or np.abs(med[i] - med[start]).sum() > 40:
            if i - start > 25:
                c = med[start:i].mean(axis=0)
                runs.append((start, i - 1, "#%02x%02x%02x" % tuple(int(round(v)) for v in c)))
            start = i
    print("  row%d runs:" % row)
    for r in runs:
        print("     x %3d..%3d (%3d wide)  %s" % (r[0], r[1], r[1] - r[0] + 1, r[2]))
