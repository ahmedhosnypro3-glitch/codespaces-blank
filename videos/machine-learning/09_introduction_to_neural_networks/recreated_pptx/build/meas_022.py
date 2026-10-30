"""Measure slide_022 original geometry: container border, row bands, box edges, fills."""
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(V + "/unique_slides/slide_022.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
print("frame", W, "x", H)

def mask_color(target, tol=40):
    return (np.abs(a - np.array(target)).sum(axis=2) < tol)

# Blue container border (#0000cc)
blue = mask_color((0, 0, 204), 60)
print("blue px:", blue.sum())
ys, xs = np.where(blue)
if len(xs):
    print("blue bbox x: %d-%d  y: %d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    # column histogram of blue: find long vertical runs (the two vertical border lines)
    colsum = blue.sum(axis=0)
    runs = [(i, c) for i, c in enumerate(colsum) if c > 100]
    print("cols with >100 blue px:", runs)
    rowsum = blue.sum(axis=1)
    runsy = [(i, c) for i, c in enumerate(rowsum) if c > 200]
    print("rows with >200 blue px:", runsy)

# Red borders (#c00000)
red = mask_color((192, 0, 0), 60)
print("\nred px:", red.sum())
ys, xs = np.where(red)
if len(xs):
    print("red bbox x: %d-%d  y: %d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()))
    rowsum = red.sum(axis=1)
    bands = [(i, c) for i, c in enumerate(rowsum) if c > 60]
    print("red rows >60px:", bands)

# Black footer
black = mask_color((0, 0, 0), 30)
rowsum = black.sum(axis=1)
foot = [i for i, c in enumerate(rowsum) if c > W * 0.5]
print("\nfooter rows:", foot)
