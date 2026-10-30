#!/usr/bin/env python3
"""Settle slide_016 title font by correlating rendered candidates against the
original's column ink profile (title band only)."""
from PIL import Image, ImageDraw, ImageFont
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
TITLE = "Adding non-Linearity to Perceptrons"

a = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]
# mid threshold: catches AA core without dropping strokes
red = (r > 140) & (r - g > 70) & (r - b > 70)
band = red[213:251, :]
origprof = band.sum(axis=0).astype(float)
xs = np.where(origprof > 0)[0]
x0, x1 = xs.min(), xs.max()
orig = origprof[x0:x1 + 1]
orig_w = x1 - x0 + 1
print(f"original title ink: x {x0}-{x1} (w={orig_w}), rows with ink: {np.where(band.any(axis=1))[0].min()}-{np.where(band.any(axis=1))[0].max()}")

cands = [
    ("LibSansBold", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"),
    ("LibSerifBold", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"),
    ("LibSansNarrowBold", "/usr/share/fonts/truetype/liberation/LiberationSansNarrow-Bold.ttf"),
    ("LibSans", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"),
    ("DejaVuSansCondBold", "/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed-Bold.ttf"),
]
import os
best = []
for name, path in cands:
    if not os.path.exists(path):
        print(f"{name}: MISSING")
        continue
    for size in range(33, 44):
        f = ImageFont.truetype(path, size)
        img = Image.new("L", (1200, 120), 0)
        d = ImageDraw.Draw(img)
        d.text((20, 20), TITLE, font=f, fill=255)
        arr = np.asarray(img).astype(float)
        cols = arr.sum(axis=0)
        xs2 = np.where(cols > 0)[0]
        if len(xs2) == 0:
            continue
        cand = cols[xs2.min():xs2.max() + 1]
        w = xs2.max() - xs2.min() + 1
        # resample candidate to original width for shape correlation
        ci = np.interp(np.linspace(0, 1, len(orig)), np.linspace(0, 1, len(cand)), cand)
        ci = ci / (ci.max() + 1e-9)
        o = orig / (orig.max() + 1e-9)
        corr = float(np.corrcoef(o, ci)[0, 1])
        best.append((corr, name, size, w, orig_w))
best.sort(reverse=True)
print("\ntop candidates (corr, font, size, rendered_w, orig_w):")
for c in best[:12]:
    print(f"  corr={c[0]:.4f} {c[1]:20s} size={c[2]} w={c[3]} (orig {c[4]})")
