"""Locate container border, row bands, and sample box fills + text colors per row."""
from PIL import Image
import numpy as np
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape

def near(col, tol):
    d = np.abs(a - np.array(col)).sum(axis=2)
    return d < tol

# Container blue border: bluish = B noticeably > R and G, and reasonably dark
bluish = (a[:, :, 2] - a[:, :, 0] > 30) & (a[:, :, 2] - a[:, :, 1] > 20) & (a[:, :, 2] < 190)
print("bluish px:", bluish.sum())
ys, xs = np.where(bluish)
if len(xs):
    print("bluish bbox x:%d-%d y:%d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    colsum = bluish.sum(axis=0)
    colrun = [i for i, c in enumerate(colsum) if c > 80]
    print("vertical-ish cols (>80):", colrun[:5], "...", colrun[-5:], "n=", len(colrun))
    rowsum = bluish.sum(axis=1)
    rowrun = [i for i, c in enumerate(rowsum) if c > 100]
    print("horizontal-ish rows (>100):", rowrun[:5], "...", rowrun[-5:], "n=", len(rowrun))

# Peach/tan box fill #f0e0d0
peach = near((240, 224, 208), 45)
ys, xs = np.where(peach)
print("\npeach bbox x:%d-%d y:%d-%d  n=%d" % (xs.min(), xs.max(), ys.min(), ys.max(), peach.sum()))
colsum = peach.sum(axis=0)
colrun = [i for i, c in enumerate(colsum) if c > 40]
print("peach cols>40: %d..%d n=%d" % (colrun[0], colrun[-1], len(colrun)))
rowsum = peach.sum(axis=1)
rowrun = [(i, c) for i, c in enumerate(rowsum) if c > 100]
if rowrun:
    print("peach rows>100: %d..%d n=%d" % (rowrun[0][0], rowrun[-1][0], len(rowrun)))
