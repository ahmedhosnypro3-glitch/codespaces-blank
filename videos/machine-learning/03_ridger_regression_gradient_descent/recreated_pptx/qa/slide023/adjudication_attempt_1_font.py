#!/usr/bin/env python3
"""A4: is the frame's title serif or sans?

Method: rasterise the measured verbatim title string at matched cap height with the
candidate faces installed here (Arial Bold = the build's choice, and the serif
candidates a judge would plausibly read as 'Times-like') and compare
(1) the ink bbox width / advance, (2) the per-row ink profile.

Frame law: original frame is 960x540, 1px = 1pt = 1/72in. Title ink measured x219..654,
y78..104 (w 436, h 27; cap height ~19-20px, 'g' descender to 104).
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ORIG = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg"
TEXT = "Inverse of High Dimension Matrix"

o = np.array(Image.open(ORIG).convert("RGB")).astype(int)
S = 1.0

def frame_bbox(x0, y0, x1, y1, pred):
    sub = o[y0:y1, x0:x1]
    m = pred(sub)
    if not m.any():
        return None
    ys, xs = np.where(m)
    return (x0 + xs.min(), x0 + xs.max(), y0 + ys.min(), y0 + ys.max())

t = frame_bbox(210, 70, 670, 112, lambda s: s.mean(axis=2) < 150)
print(f"ORIGINAL title ink bbox: x{t[0]}..{t[1]} y{t[2]}..{t[3]}  (w={t[1]-t[0]+1}, h={t[3]-t[2]+1})")

# cap height of the original: 'I' of "Inverse" or the tallest cap band
sub = o[70:112, 210:670]
m = sub.mean(axis=2) < 150
rows = np.where(m.any(axis=1))[0] + 70
print(f"ORIGINAL title ink rows: y{rows.min()}..{rows.max()}")
# count rows occupied near the leftmost glyph 'I' (x219..240)
subI = o[70:112, 219:245]
mI = subI.mean(axis=2) < 150
rI = np.where(mI.any(axis=1))[0] + 70
print(f"ORIGINAL 'I' rows: y{rI.min()}..{rI.max()} (cap height {rI.max()-rI.min()+1})")

FONTS = {
    "Arial Bold": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "DejaVu Sans Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "Liberation Sans Bold (Arial)": "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "Liberation Serif Bold (Times)": "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "DejaVu Serif Bold": "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
}
import os
print()
print("candidate faces present on this system:")
for name, path in FONTS.items():
    print(f"  {'FOUND ' if os.path.exists(path) else 'MISSING'} {name}: {path}")

def raster(text, face_path, size_px):
    f = ImageFont.truetype(face_path, size_px)
    im = Image.new("L", (1400, 120), 0)
    d = ImageDraw.Draw(im)
    d.text((20, 20), text, font=f, fill=255)
    a = np.array(im)
    m = a > 100
    if not m.any():
        return None
    ys, xs = np.where(m)
    return xs.min(), xs.max(), ys.min(), ys.max()

print()
print("cap height in the frame is ~19-20px => at 150dpi that is ~19*2.083 = 40 render px")
print("but we compare at FRAME scale (1px = 1pt), so size_px here = pt-equivalent.")
print()
print(f"{'face':34s} {'size':>5s} {'w':>6s} {'h':>5s}  vs frame w=436 h=27")
# We don't know the exact cap height to compare directly; instead, for each face, find
# the size whose ink WIDTH matches the frame's 436, then report that size's height.
for name, path in FONTS.items():
    if not os.path.exists(path):
        continue
    lo, hi = 14, 40
    best = None
    # binary search the size whose ink width matches 436
    for _ in range(30):
        mid = (lo + hi) / 2
        r = raster(TEXT, path, mid)
        if r is None:
            break
        w = r[1] - r[0] + 1
        if w < 436:
            lo = mid
        else:
            hi = mid
        best = (mid, r)
    if best:
        size_px, r = best
        w, h = r[1] - r[0] + 1, r[3] - r[2] + 1
        print(f"  {name:32s} {size_px:5.2f} {w:6d} {h:5d}")
