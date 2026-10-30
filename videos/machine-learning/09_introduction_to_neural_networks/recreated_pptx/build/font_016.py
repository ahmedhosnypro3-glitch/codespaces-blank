#!/usr/bin/env python3
"""Decide slide_016 title font family + size from measured original ink metrics.

Original (960x540 frame, 1px == 1pt on a 13.33in slide):
  title band rows 217-249, ink x 166-835
  subtitle blue "Activation" rows 279-308, ink x 313-493
"""
import glob
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
TITLE = "Adding non-Linearity to Perceptrons"
SUB = "(Activation Functions)"

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 165) & (g < 90) & (b < 90)
blue = (b > 90) & (b - r > 60) & (b - g > 60)


def band(mask, x0, x1):
    sub = mask[:, x0:x1]
    rows = [y for y in range(sub.shape[0]) if sub[y].sum() > 0]
    cols = np.where(sub.any(axis=0))[0]
    return rows[0], rows[-1], x0 + cols.min(), x0 + cols.max()


print("ORIGINAL title red band:", band(red, 150, 850))
print("ORIGINAL blue band    :", band(blue, 300, 500))

# per-letter segmentation of the title using column ink profile
cols = red[210:255].sum(axis=0)
runs = []
inrun = False
for x in range(150, 850):
    if cols[x] > 0 and not inrun:
        start = x
        inrun = True
    elif cols[x] == 0 and inrun:
        runs.append((start, x - 1))
        inrun = False
print("\ntitle letter runs (x start-end, width):")
print("  " + "  ".join(f"{s}-{e}({e-s+1})" for s, e in runs))

# cap height from the first letter 'A'
if runs:
    s0, e0 = runs[0]
    sub = red[200:260, s0:e0 + 1]
    rr = [y + 200 for y in range(sub.shape[0]) if sub[y].sum() > 0]
    print(f"\nfirst letter '{TITLE[0]}' x {s0}-{e0} width {e0-s0+1} ink rows {rr[0]}-{rr[-1]} height {rr[-1]-rr[0]+1}")

# blue word first letter 'A' of Activation
bcols = blue[270:315].sum(axis=0)
bruns = []
inrun = False
for x in range(300, 500):
    if bcols[x] > 0 and not inrun:
        start = x
        inrun = True
    elif bcols[x] == 0 and inrun:
        bruns.append((start, x - 1))
        inrun = False
print("\nblue letter runs:", "  ".join(f"{s}-{e}({e-s+1})" for s, e in bruns))
if bruns:
    s0, e0 = bruns[0]
    sub = blue[265:320, s0:e0 + 1]
    rr = [y + 265 for y in range(sub.shape[0]) if sub[y].sum() > 0]
    print(f"  blue 'A' x {s0}-{e0} width {e0-s0+1} ink rows {rr[0]}-{rr[-1]} height {rr[-1]-rr[0]+1}")

# font comparison
cands = {
    "Arial/LiberationSans-Bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "Times/LiberationSerif-Bold": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "DejaVuSans-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "DejaVuSerif-Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
print("\nfont candidates:", {k: (v if glob.glob(v) else "MISSING") for k, v in cands.items()})
print("\nAt each candidate size: rendered ink width of TITLE and cap height of 'A'")
for name, path in cands.items():
    if not glob.glob(path):
        continue
    for size in (34, 35, 36, 37, 38, 40):
        f = ImageFont.truetype(path, size)
        bbox = f.getbbox(TITLE)
        w = bbox[2] - bbox[0]
        ab = f.getbbox("A")
        cap = ab[3] - ab[1]
        mark = "  <== title width 669?" if abs(w - 669) <= 14 else ""
        print(f"  {name:26s} size {size}: title ink w={w:4d}  'A' cap h={cap:3d}{mark}")
