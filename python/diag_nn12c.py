#!/usr/bin/env python3
"""Precise geometry of slide_012.jpg: content frame, diagram boxes, strips."""
import numpy as np
from PIL import Image

P = "videos/machine-learning/10_nn_training_and_example/unique_slides/slide_012.jpg"
o = np.asarray(Image.open(P).convert("RGB")).astype(int)
H, W = 540, 960
IN = 13.33 / W
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

# --- red border: dark-red saturated pixels
red = (r > 120) & (r - g > 45) & (r - b > 45)
ys, xs = np.where(red)
print("red ink rows:", ys.min(), "-", ys.max(), " cols:", xs.min(), "-", xs.max())
# border line thickness: scan col 480 downward
col = red[:, 480]
rr = np.where(col)[0]
print("col480 red rows:", rr[:8], "...", rr[-8:] if len(rr) > 8 else "")
col2 = red[:, 100]
rr2 = np.where(col2)[0]
print("col100 red rows:", rr2[:8], "...", rr2[-8:] if len(rr2) > 8 else "")
row = red[480, :]
cc = np.where(row)[0]
print("row480 red cols:", cc[:8], "...", cc[-8:] if len(cc) > 8 else "")

# --- dark bands (black bottom bar, gray content area)
grayish = (np.abs(r - 231) < 12) & (np.abs(g - 233) < 12) & (np.abs(b - 230) < 12)
ys, xs = np.where(grayish)
print("\ngray #E7E9E6 rows:", ys.min(), "-", ys.max(), " cols:", xs.min(), "-", xs.max())
e8 = (np.abs(r - 232) < 6) & (np.abs(g - 232) < 6) & (np.abs(b - 232) < 6)
ys, xs = np.where(e8)
print("gray #E8E8E8 rows:", ys.min(), "-", ys.max(), " cols:", xs.min(), "-", xs.max())

# --- black bar
blk = (r < 20) & (g < 20) & (b < 20)
ys, xs = np.where(blk)
print("black rows:", ys.min(), "-", ys.max(), " cols:", xs.min(), "-", xs.max())

# --- green circles (fill)  - saturated light green
gfill = (g > 120) & (g - r > 40) & (g - b > 40) & (g < 220)
from scipy import ndimage
lbl, k = ndimage.label(gfill)
print("\ngreen components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 200:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f}) "
              f"cx={((xs.min()+xs.max())/2)*IN:.2f} cy={((ys.min()+ys.max())/2)*IN:.2f}")

# --- orange fill
ofill = (r > 230) & (g > 150) & (g < 210) & (b < 120) & (r - b > 100)
lbl, k = ndimage.label(ofill)
print("orange components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 100:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f}) "
              f"cx={((xs.min()+xs.max())/2)*IN:.2f} cy={((ys.min()+ys.max())/2)*IN:.2f}")

# --- red box (Error) fill
redf = (r > 190) & (g < 90) & (b < 90) & (r - g > 110)
lbl, k = ndimage.label(redf)
print("red-fill components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 300:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f})")

# --- light blue t_j rects
bf = (b > 200) & (r > 150) & (r < 220) & (g > 180) & (g < 225) & (b - r > 25)
lbl, k = ndimage.label(bf)
print("lightblue components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 200:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f}) "
              f"cx={((xs.min()+xs.max())/2)*IN:.2f} cy={((ys.min()+ys.max())/2)*IN:.2f}")

# --- pale green strip
pf = (r > 225) & (r < 245) & (g > 245) & (b < 230)
lbl, k = ndimage.label(pf)
print("palegreen components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 400:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f})")

# --- white definition box
wf = (r > 248) & (g > 248) & (b > 250) & (r == 255) & (b < 256)
ys, xs = np.where(wf)
print("pure-white rows:", ys.min(), "-", ys.max(), " cols:", xs.min(), "-", xs.max())
lbl, k = ndimage.label(wf)
print("white components:", k)
for i in range(1, k + 1):
    ys, xs = np.where(lbl == i)
    if len(ys) >= 800:
        print(f"  c{i}: n={len(ys)} rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} "
              f"in=({ (xs.max()-xs.min()+1)*IN:.2f}x{(ys.max()-ys.min()+1)*IN:.2f})")
