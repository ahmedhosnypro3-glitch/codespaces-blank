from PIL import Image
import numpy as np
O=np.asarray(Image.open('unique_slides/slide_031.jpg').convert('RGB')).astype(int)
V=O.max(axis=2)
print("== per-column pixels with V<215 in x 574..808, y 67..263 (excl grid 224) ==")
for x in range(574,809):
    ys=[y for y in range(67,264) if V[y,x]<215]
    if ys:
        # compact runs
        runs=[]; s=ys[0]; p=ys[0]
        for y in ys[1:]:
            if y==p+1: p=y
            else: runs.append((s,p)); s=y; p=y
        runs.append((s,p))
        print(f" x{x:3d}: "+" ".join(f"{a}" if a==b else f"{a}-{b}" for a,b in runs))
