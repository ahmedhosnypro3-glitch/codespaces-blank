#!/usr/bin/env python3
"""Font fitting for slide 029's title block.

Measured (sensitive-mask ink bbox, 960x540 frame, 1px=1pt):
  L1 "Example: Obtain Minimum Value"  ink w=688 h=46  (y191-236, x137-824, cx 480.5)
  L2 "of a function using"            ink w=397 h=46  (y269-314, x269-665, cx 467)
  L3 "Gradient Descent (GD)"           ink w=477 h=46  (y347-392, x235-711, cx 473)
Baseline pitch = 78px. Cap ~34px, x-height ~26px, descender ~10px.

For each candidate TTF: sweep sizes, report ink w/h per line; find the size
minimizing combined width+height error.
"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

LINES = [
    ("Example: Obtain Minimum Value", 688, 46),
    ("of a function using", 397, 46),
    ("Gradient Descent (GD)", 477, 46),
]
FONTS = [
    ("Arial Bold", "/usr/share/fonts/TTF/Arialbd.TTF"),
    ("Liberation Sans Bold", "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"),
    ("Carlito Bold", "/usr/share/fonts/carlito/Carlito-Bold.ttf"),
    ("Verdana Bold", "/usr/share/fonts/TTF/Verdanab.TTF"),
    ("DejaVu Sans Bold", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
    ("DejaVu Sans Cond Bold", "/usr/share/fonts/TTF/DejaVuSansCondensed-Bold.ttf"),
]

def ink_bbox(font, text):
    # render big for AA-free measurement: scale up 4x, measure, divide
    S = 4
    f = ImageFont.truetype(font.path if hasattr(font, "path") else font, 200)
    raise RuntimeError("unused")

def measure(fontpath, text, size):
    f = ImageFont.truetype(fontpath, int(round(size)))
    # supersample x4 for precise ink edges, then scale down
    img = Image.new("L", (1600, 400), 0)
    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=f, fill=255)
    a = np.asarray(img) > 40
    ys, xs = np.where(a)
    if not len(xs):
        return None
    return (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1, xs.min() - 100, ys.min() - 100)

import os
print(f"{'font':26s} {'size':>5s}  per-line (w,h) vs target  | err")
results = {}
for name, path in FONTS:
    if not os.path.exists(path):
        print(f"{name}: MISSING {path}")
        continue
    best = None
    for size in range(40, 58, 0.5) if False else [s / 2 for s in range(80, 116)]:
        tot = 0.0
        per = []
        for text, tw, th in LINES:
            m = measure(path, text, size)
            if not m:
                tot = 1e9; break
            w, h = m[0] / 4.0, m[1] / 4.0   # supersample /4
            err = (w - tw) / tw * 100
            tot += err ** 2
            per.append((w, h, err))
        if best is None or tot < best[0]:
            best = (tot, size, per)
    tot, size, per = best
    hs = [f"{p[0]:.0f}/{p[1]:.1f}" for p in per]
    # also height errors at the same size
    herr = sum(abs(p[1] - 46) for p in per) / 3
    print(f"{name:26s} {size:5.1f}  {' '.join(hs):38s} | werr_rmse={tot ** 0.5:5.1f}% mean|h-46|={herr:.1f}px")
    results[name] = (size, per)

print("\nHeight-fit check (size chosen to match h=46 per line, then resulting w):")
for name, path in FONTS:
    if not os.path.exists(path):
        continue
    out = [name]
    for text, tw, th in LINES:
        lo, hi = 20, 120
        for _ in range(30):
            mid = (lo + hi) / 2
            m = measure(path, text, mid)
            h = m[1] / 4.0 if m else 0
            if h < th: lo = mid
            else: hi = mid
        m = measure(path, text, (lo + hi) / 2)
        out.append(f"w={m[0]/4.0:.0f}(t{tw}) h={m[1]/4.0:.1f} sz={(lo+hi)/2:.1f}")
    print("  " + " | ".join(out))
