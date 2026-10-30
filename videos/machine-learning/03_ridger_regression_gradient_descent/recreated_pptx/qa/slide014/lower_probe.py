#!/usr/bin/env python3
"""Definitive probe of the lower blue region + the two missing middle bands.

Answers:
  1. Is the original's lower blue region ONE continuous band (x 86..882) or two
     boxes with a gutter?  Column-scan the gutter at x=460..500.
  2. Is there a horizontal divider between the 'two boxes' row and the final band?
  3. Exact y-extent and bottom edge of the blue region in both images.
  4. Exact y-extent, x-extent and fill of the two missing middle bands.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0


def is_blue(c):
    return int(c[2]) - int(c[0]) > 4 and int(c[1]) > int(c[0]) and int(c[1]) >= 215


def is_yellow(c):
    R, G, B = int(c[0]), int(c[1]), int(c[2])
    return G - B > 12 and R >= 240 and G >= 235


def is_peach(c):
    R, G, B = int(c[0]), int(c[1]), int(c[2])
    return R - G > 18 and R - B > 28 and R >= 238 and 190 <= G <= 236


def is_pink(c):
    R, G, B = int(c[0]), int(c[1]), int(c[2])
    return R - G > 10 and R - B > 10 and R >= 238 and 200 <= G <= 242


def is_gray(c):
    R, G, B = int(c[0]), int(c[1]), int(c[2])
    return max(R, G, B) - min(R, G, B) < 14 and 200 <= max(R, G, B) <= 248


def col_profile(im, x, y0, y1, scale, pred, tag):
    """Print the y-runs where pred holds, at column x."""
    line = im[:, int(x * scale)]
    runs = []
    cur = None
    for y in range(int(y0 * scale), int(y1 * scale)):
        c = line[y]
        if pred(c):
            if cur is None:
                cur = [y, y]
            else:
                cur[1] = y
        else:
            if cur is not None:
                runs.append(tuple(cur))
                cur = None
    if cur is not None:
        runs.append(tuple(cur))
    runs = [(a / scale, b / scale) for a, b in runs if b - a >= 2 * scale]
    print(f"  {tag}: x={x}: " + ("  ".join(f"y {a:.0f}..{b:.0f}" for a, b in runs) if runs else "NONE"))


def row_profile(im, y, x0, x1, scale, pred, tag):
    line = im[int((y + .5) * scale), :]
    runs = []
    cur = None
    for x in range(int(x0 * scale), int(x1 * scale)):
        if pred(line[x]):
            if cur is None:
                cur = [x, x]
            else:
                cur[1] = x
        else:
            if cur is not None:
                runs.append(tuple(cur))
                cur = None
    if cur is not None:
        runs.append(tuple(cur))
    runs = [(a / scale, b / scale) for a, b in runs if b - a >= 2 * scale]
    print(f"  {tag}: y={y}: " + ("  ".join(f"x {a:.0f}..{b:.0f}" for a, b in runs) if runs else "NONE"))


print("=== 1. GUTTER between the two lower columns (x 455..500) ===")
for x in (455, 462, 470, 478, 485, 492, 498):
    col_profile(o, x, 465, 530, 1.0, is_blue, "ORIG")
print("--- render gutter ---")
for x in (455, 462, 470, 478, 485, 492, 498):
    col_profile(r, x, 465, 530, SC, is_blue, "REND")

print()
print("=== 2. Horizontal divider inside the blue region? column-scan x=200 and x=700 ===")
col_profile(o, 200, 460, 535, 1.0, is_blue, "ORIG x=200")
col_profile(o, 700, 460, 535, 1.0, is_blue, "ORIG x=700")
col_profile(r, 200, 460, 535, SC, is_blue, "REND x=200")
col_profile(r, 700, 460, 535, SC, is_blue, "REND x=700")

print()
print("=== 3. Bottom edge / full extent of the blue region (text-free columns) ===")
for x in (95, 130, 430, 470, 700, 850, 880):
    col_profile(o, x, 465, 535, 1.0, is_blue, "ORIG")
print("--- render ---")
for x in (95, 130, 430, 470, 700, 850, 880):
    col_profile(r, x, 465, 535, SC, is_blue, "REND")

print()
print("=== 3b. Any dark divider line in the gutter (x 460..500, y 470..525)? ===")
for x in (470, 475, 480, 485, 490):
    col_profile(o, x, 470, 525, 1.0, lambda c: max(int(c[0]), int(c[1]), int(c[2])) < 150, f"ORIG dark x={x}")

print()
print("=== 4. The two missing middle bands: exact extents ===")
print("PEACH-like fill (y 340..395):")
for x in (95, 200, 400, 640, 660, 665, 670, 690):
    col_profile(o, x, 340, 395, 1.0, is_peach, f"ORIG x={x}")
print()
print("YELLOW-mid fill (y 395..450):")
for x in (520, 540, 600, 700, 860, 880, 885, 890):
    col_profile(o, x, 395, 450, 1.0, is_yellow, f"ORIG x={x}")
print()
print("PINK fill in original's define-loss area (y 395..450):")
for x in (95, 200, 400, 460, 470, 475, 480):
    col_profile(o, x, 395, 450, 1.0, is_pink, f"ORIG x={x}")

print()
print("=== 5. Row profiles of the two missing bands ===")
for y in (352, 360, 372, 382, 388):
    row_profile(o, y, 60, 910, 1.0, is_peach, f"ORIG y={y} peach")
for y in (400, 410, 424, 440, 443):
    row_profile(o, y, 60, 910, 1.0, is_yellow, f"ORIG y={y} yellow")
    row_profile(o, y, 60, 910, 1.0, is_pink, f"ORIG y={y} pink")
