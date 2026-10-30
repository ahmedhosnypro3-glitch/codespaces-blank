#!/usr/bin/env python3
"""Font fitting for slide 029's title block (RESUMED worker's fixed version).

Supersedes fit_fonts.py (kept banked, untouched): that script rendered at 1x
and divided by 4 — the intended 4x supersample was never wired, so its sweep
was garbage. This version renders at 4x font size and divides by 4, giving
sub-pixel-precise ink widths for fractional point sizes.

Measured (sensitive-mask ink bbox, 960x540 frame, 1px=1pt):
  L1 "Example: Obtain Minimum Value"  ink w=688 h=46  (y191-236, x137-824, cx 480.5)
  L2 "of a function using"            ink w=397 h=46  (y269-314, x269-665, cx 467)
  L3 "Gradient Descent (GD)"           ink w=477 h=46  (y347-392, x235-711, cx 473)
Baseline pitch = 78px. Cap ~35px (rows 192-226 on L1), x-height ~27px,
descender ~10px.
"""
import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw

LINES = [
    ("Example: Obtain Minimum Value", 688),
    ("of a function using", 397),
    ("Gradient Descent (GD)", 477),
]
FONTS = [
    ("Arial Bold", "/usr/share/fonts/TTF/Arialbd.TTF"),
    ("Liberation Sans Bold", "/usr/share/fonts/liberation/LiberationSans-Bold.ttf"),
    ("Carlito Bold", "/usr/share/fonts/carlito/Carlito-Bold.ttf"),
    ("Verdana Bold", "/usr/share/fonts/TTF/Verdanab.TTF"),
    ("DejaVu Sans Bold", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
]
SS = 4  # supersample factor


def measure(fontpath, text, size):
    """Render text at SS*size px, return ink (w, h) in size-pt px (divided by SS)."""
    f = ImageFont.truetype(fontpath, int(round(size * SS)))
    img = Image.new("L", (5200, 1100), 0)
    d = ImageDraw.Draw(img)
    d.text((150, 150), text, font=f, fill=255)
    a = np.asarray(img) > 40
    ys, xs = np.where(a)
    if not len(xs):
        return None
    if xs.max() >= img.size[0] - 1 or ys.max() >= img.size[1] - 1:
        return None  # clipped: canvas too small at this size
    return ((xs.max() - xs.min() + 1) / SS, (ys.max() - ys.min() + 1) / SS)


print(f"{'font':24s} {'size':>6s}  per-line ink w (target) err%  | rmse%")
best_overall = None
for name, path in FONTS:
    if not os.path.exists(path):
        print(f"{name}: MISSING {path}")
        continue
    best = None
    for i in range(401):  # sizes 38.0 .. 58.0 in 0.05 steps
        size = 38.0 + i * 0.05
        tot, per = 0.0, []
        for text, tw in LINES:
            m = measure(path, text, size)
            if not m:
                tot = 1e9
                break
            err = (m[0] - tw) / tw * 100
            tot += err ** 2
            per.append((m[0], m[1], err))
        if best is None or tot < best[0]:
            best = (tot, size, per)
    tot, size, per = best
    ws = " ".join(f"{p[0]:6.1f}(t{tw}) {p[2]:+5.1f}%" for (text, tw), p in zip(LINES, per))
    print(f"{name:24s} {size:6.2f}  {ws} | {tot ** 0.5:5.2f}")
    if best_overall is None or tot < best_overall[0]:
        best_overall = (tot, size, per, name)

tot, size, per, name = best_overall
print(f"\nBEST: {name} at {size:.2f}pt")
print("Height-fit cross-check (cap-height 35px -> S=35/0.716="
      f"{35 / 0.716:.1f}pt; x-height 27px -> S=27/0.524={27 / 0.524:.1f}pt):")
for (text, tw), p in zip(LINES, per):
    print(f"  '{text}': ink w={p[0]:.1f} h={p[1]:.1f} (target w={tw}, "
          f"measured band h=46; h/1.117 -> S={p[1] / 1.117:.1f}pt)")

# charSpacing residuals at the chosen common size (building.md law):
print("\ncharSpacing that would close each residual at the common size:")
for (text, tw), p in zip(LINES, per):
    resid = tw - p[0]
    gaps = max(1, len(text) - 1)
    print(f"  '{text}': residual={resid:+.1f}px -> charSpacing={(resid / 2) / gaps:+.3f}pt")
