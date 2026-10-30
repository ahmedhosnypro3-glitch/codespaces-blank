#!/usr/bin/env python3
"""Find the blue box extents + cream/white background regions."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

# cream/near-white background: high R,G, moderate B, and NOT gray panel
grayish = (abs(r - g) < 8) & (abs(g - b) < 12) & (abs(r - b) < 14)
cream = (r > 238) & (g > 238) & (b > 215) & ~grayish | ((r > 248) & (g > 250) & (b > 230))

print("=== CREAM/WHITE-BG region extents ===")
ys, xs = np.where(cream)
print("cream px:", cream.sum())
# restrict to panel
m = cream.copy(); m[:, :63] = False; m[:, 898:] = False; m[:48] = False; m[535:] = False
ys, xs = np.where(m)
if len(ys):
    print("cream bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())
# per-row cream x-extent for rows in top band
for y in (55, 70, 90, 120, 130, 135, 150, 200, 250, 260):
    cols = np.where(cream[y])[0]
    if len(cols):
        print(f"  y{y}: cream x {cols.min()}..{cols.max()} n={len(cols)}")

print("\n=== BLUE BOX borders ===")
blue = (b > 110) & (b - r > 40) & (b - g > 25)
bm = blue.copy(); bm[:, :63] = False; bm[:, 898:] = False; bm[:48] = False; bm[535:] = False
ys, xs = np.where(bm)
print("blue bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "px", bm.sum())
# horizontal blue lines (rows with many blue px)
rc = bm.sum(axis=1)
for y in range(48, 136):
    if rc[y] > 30:
        cols = np.where(bm[y])[0]
        print(f"  row y{y}: {rc[y]} blue px, x {cols.min()}..{cols.max()}")
# vertical blue lines
cc = bm.sum(axis=0)
for x in range(60, 740):
    if cc[x] > 25:
        rows = np.where(bm[:, x])[0]
        print(f"  col x{x}: {cc[x]} blue px, y {rows.min()}..{rows.max()}")
