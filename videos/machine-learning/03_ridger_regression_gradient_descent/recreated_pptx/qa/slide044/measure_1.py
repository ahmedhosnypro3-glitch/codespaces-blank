#!/usr/bin/env python3
"""PIL measurement of unique_slides/slide_044.jpg (960x540, 1px=1pt).

Frame-wins law: derive every element's geometry from the pixels, not the spec.
"""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)

H, W = IM.shape[:2]
r, g, b = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]

def hx(v):
    return f"#{v[0]:02X}{v[1]:02X}{v[2]:02X}"

print("=== IMAGE", W, "x", H)
print("corner colors:", hx(IM[0, 0]), hx(IM[5, 5]), hx(IM[100, 100]), hx(IM[300, 600]))

# ---------- ink mask (dark text/lines) ----------
dark = (r < 150) & (g < 150) & (b < 150)
print("dark px total:", dark.sum())

# ---------- red mask ----------
red = (r > 100) & (r - g > 55) & (r - b > 55)
print("red px total:", red.sum())
ys, xs = np.where(red)
if len(ys):
    print("red bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())

# ---------- blue mask ----------
blue = (b > 100) & (b - r > 45) & (b - g > 30)
print("blue px total:", blue.sum())
ys, xs = np.where(blue)
if len(ys):
    print("blue bbox: x", xs.min(), xs.max(), "y", ys.min(), ys.max())

# ---------- row profile of all "content" (non-panel) ----------
# panel fill E9E9E7 = (233,232,231)-ish
panel = (abs(r - 233) < 22) & (abs(g - 233) < 22) & (abs(b - 231) < 22)
content = ~panel & ~((r > 245) & (g > 245) & (b > 245))  # not panel, not white
print("\n=== ROW PROFILE of content (rows with >8 content px) ===")
rowcnt = content.sum(axis=1)
runs = []
inrun = False
for y in range(H):
    if rowcnt[y] > 8 and not inrun:
        inrun = True; y0 = y
    elif rowcnt[y] <= 8 and inrun:
        inrun = False; runs.append((y0, y - 1))
if inrun: runs.append((y0, H - 1))
for y0, y1 in runs:
    sub = content[y0:y1+1]
    cols = np.where(sub.sum(axis=0) > 0)[0]
    if len(cols):
        print(f"  rows {y0:>3}-{y1:<3} h={y1-y0+1:>2}  x {cols.min():>3}..{cols.max():>3}  px={int(sub.sum())}")

print("\n=== COLUMN PROFILE (cols with >8 content px) ===")
colcnt = content.sum(axis=0)
runs = []
inrun = False
for x in range(W):
    if colcnt[x] > 8 and not inrun:
        inrun = True; x0 = x
    elif colcnt[x] <= 8 and inrun:
        inrun = False; runs.append((x0, x - 1))
if inrun: runs.append((x0, W - 1))
for x0, x1 in runs:
    sub = content[:, x0:x1+1]
    rows_ = np.where(sub.sum(axis=1) > 0)[0]
    if len(rows_):
        print(f"  cols {x0:>3}-{x1:<3} w={x1-x0+1:>3}  y {rows_.min():>3}..{rows_.max():>3}  px={int(sub.sum())}")
