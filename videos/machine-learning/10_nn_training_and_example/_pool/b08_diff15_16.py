import sys
from PIL import Image, ImageChops
import numpy as np

A = Image.open("unique_slides/slide_015.jpg").convert("RGB")
B = Image.open("unique_slides/slide_016.jpg").convert("RGB")
print("dims", A.size, B.size)
a = np.asarray(A).astype(int)
b = np.asarray(B).astype(int)
h, w = a.shape[:2]
d = np.abs(a - b).sum(axis=2)
print("total differing pixels (>30):", int((d > 30).sum()), "of", h * w)
# row/col bands
rows = (d > 30).sum(axis=1)
cols = (d > 30).sum(axis=0)
print("\nrows with diffs (y:count) where count>200:")
for i, c in enumerate(rows):
    if c > 200:
        print(f"  y={i:4d} ({i/h*100:5.2f}%) count={c}")
print("\ncols with diffs (x:count) where count>150:")
for i, c in enumerate(cols):
    if c > 150:
        print(f"  x={i:4d} ({i/w*100:5.2f}%) count={c}")
