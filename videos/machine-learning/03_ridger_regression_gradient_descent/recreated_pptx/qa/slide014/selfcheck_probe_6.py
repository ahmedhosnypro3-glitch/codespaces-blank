#!/usr/bin/env python3
"""Measure precise fill-color band extents with tight masks."""
import numpy as np
from PIL import Image

im = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_014.jpg"
).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]


def extent(mask, name):
    # require a solid run horizontally so we exclude text pixels
    rowc = mask.sum(axis=1)
    ys = np.where(rowc > 200)[0]
    if not len(ys):
        print(f"{name}: none")
        return
    y0, y1 = ys.min(), ys.max()
    colc = mask[y0:y1 + 1].sum(axis=0)
    xs = np.where(colc > 20)[0]
    x0, x1 = xs.min(), xs.max()
    # dominant color
    region = im[y0:y1 + 1, x0:x1 + 1]
    print(f"{name}: x {x0}-{x1}, y {y0}-{y1}, w={x1-x0+1}, h={y1-y0+1}, "
          f"rgb={tuple(int(v) for v in np.median(region.reshape(-1,3), axis=0))}")


# yellow band FFF9C4 -> JPEG reads ~(249,253,218)
extent((r >= 240) & (r <= 253) & (g >= 245) & (b >= 205) & (b <= 235) & (r - b > 20), "Yellow band")
# pink band FFEBEE -> ~(255,250,255)? sample at y=470 showed purple-ish (119,117,201)
# purple-pink boxes -> sample (119,117,201) which is a PURPLE fill (6A5ACD-ish?) not pink
extent((r > 100) & (r < 135) & (g > 85) & (g < 130) & (b > 185) & (b < 215), "Purple fill (y470)")
# final band E1F5FE -> (237,253,250)
extent((r >= 225) & (r <= 242) & (g >= 245) & (b >= 240) & (b <= 255), "Blue band E1F5FE")
# vector box white region (y 110..185)
extent((r >= 250) & (g >= 250) & (b >= 250), "White interior")

# Vector box black border (upper-middle left) - find black border rows
print("\n--- looking for box borders ---")
sub = im[95:200, 100:900]
bsub = (sub.max(axis=2) < 100)
rowc = bsub.sum(axis=1)
for i, c in enumerate(rowc):
    if c > 100:
        print(f"  y={95+i}: {c} px")

print("\n--- x=480 col profile y=100..200 ---")
for y in range(100, 200, 4):
    print(f"  y={y:3d} rgb={tuple(int(v) for v in im[y,480])}")
