#!/usr/bin/env python3
"""ASCII ink maps of the original's NO REG test blocks (row 1/2/3), slide 019.

The colour census shows the original carries essentially NO green inside the
y= value cells (0 green px) while render_8 paints every y= glyph green
(#008000).  Two readings are possible:
  (a) the original's y= glyphs are genuinely black -> render has a colour defect
  (b) the original's y= glyphs are green but sit at a different offset
      (the green census puts original green at x309..330 and x568..589)

This dump resolves it by printing the raw ink map of the original's test block
and of the render (resampled to frame px) side by side region by region.
  '#' = dark ink, 'G' = green ink, 'r' = red ink, '.' = background
"""
from PIL import Image
import numpy as np

Q = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
     "recreated_pptx/qa/slide019")
ORIG = ("videos/machine-learning/03_ridger_regression_gradient_descent/"
        "unique_slides/slide_019.jpg")

O = np.asarray(Image.open(ORIG).convert("RGB")).astype(np.int16)
RIM = Image.open(f"{Q}/render_8.png").convert("RGB").resize((960, 540), Image.LANCZOS)
R = np.asarray(RIM).astype(np.int16)


def classify(a):
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    lum = a.mean(axis=2)
    out = np.full(a.shape[:2], ".", dtype="<U1")
    green = (g > r + 15) & (g > b + 15) & (g > 60) & (g < 235)
    red = (r > g + 40) & (r > b + 40) & (r > 90)
    dark = lum < 120
    out[green & ~red] = "G"
    out[red] = "r"
    out[dark & ~green & ~red] = "#"
    return out


def dump(label, arr, x0, x1, y0, y1):
    print(f"--- {label}  x{x0}..{x1} y{y0}..{y1} ---")
    grid = classify(arr[y0:y1, x0:x1])
    hdr = "".join(str((x0 + i) // 10 % 10) if (x0 + i) % 10 == 0 else " "
                  for i in range(x1 - x0))
    print("      " + hdr)
    for i, row in enumerate(grid):
        print(f"  {y0 + i:4d} " + "".join(row))
    print()


for gy, rname in ((205, "ROW1"), (310, "ROW2"), (420, "ROW3")):
    dump(f"ORIGINAL {rname}", O, 200, 385, gy - 5, gy + 60)

print("=" * 100)
print("RENDER (resampled to 960x540) ROW2 — for layout comparison")
print("=" * 100)
dump("RENDER ROW2", R, 200, 385, 310 - 5, 310 + 60)
