#!/usr/bin/env python3
"""Clean subscript digit identification: header row has x1..x6 (known digits),
so their glyph shapes calibrate the class-row subscripts."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 175


def glyph(y0, y1, x0, x1):
    sub = dark[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if not len(ys):
        return None
    return (x0 + int(xs.min()), x0 + int(xs.max()), y0 + int(ys.min()), y0 + int(ys.max()),
            int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1))


def show(y0, y1, x0, x1, label):
    print(f"--- {label} y{y0}..{y1} ---")
    for y in range(y0, y1 + 1):
        line = "".join("#" if dark[y, x] else ("+" if LUM[y, x] < 200 else " ") for x in range(x0, x1 + 1))
        print(f"  {y:>4} {line}")


COLS = [95, 117, 139, 163, 186, 209]   # column anchor for the 6 columns

print("=== T1 HEADER subscripts (digit rows only, y70..74) ===")
for i, cx in enumerate(COLS):
    b = glyph(70, 74, cx - 4, cx + 8)
    print(f"  digit{i+1}: {b}")

print("\n=== T1 CLASS-ROW subscripts (digit rows only, y122..125) ===")
for i, cx in enumerate(COLS):
    b = glyph(122, 125, cx - 4, cx + 8)
    print(f"  cell{i+1}: {b}")

print("\n=== T2 CLASS-ROW subscripts (y241..244) ===")
for i, cx in enumerate(COLS):
    b = glyph(241, 244, cx - 4, cx + 8)
    print(f"  cell{i+1}: {b}")

print()
show(70, 74, 92, 216, "T1 header subscripts")
print()
show(120, 125, 92, 216, "T1 class-row subscripts")
