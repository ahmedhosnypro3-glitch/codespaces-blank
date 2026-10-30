"""Definitive: box borders from stroke lines + ink color classification per box."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def hx(px):
    return "#%02x%02x%02x" % tuple(int(v) for v in px)

mx = a.max(axis=2); mn = a.min(axis=2)
sat = mx - mn
stroke = (mx < 215) & (sat > 25)

# 1. Box horizontal border lines: for each candidate y, report x-runs of stroke
print("=== horizontal stroke runs (y, x_runs) ===")
for y in range(105, 510):
    row = stroke[y]
    runs = []
    start = None
    for x in range(W):
        if row[x] and start is None:
            start = x
        elif not row[x] and start is not None:
            runs.append((start, x - 1))
            start = None
    if start is not None:
        runs.append((start, W - 1))
    runs = [r for r in runs if r[1] - r[0] + 1 > 60]
    if runs:
        cols = []
        for r in runs:
            seg = a[y, r[0]:r[1] + 1][row[r[0]:r[1] + 1]]
            cols.append(hx(np.median(seg, axis=0)))
        print("  y=%3d  %s" % (y, list(zip(runs, cols))))
