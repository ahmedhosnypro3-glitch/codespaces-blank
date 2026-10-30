#!/usr/bin/env python3
"""Definitive T1 row count: per column, find digit-glyph y-bands."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
dark = LUM < 185

# Column centres measured from the subscripts: x101, x123, x145, x167, x189, x212
CENTERS = [101, 123, 145, 167, 189, 212]
print("T1: per column, digit-glyph y-bands (excluding paren columns +/-8..-3 and +3..+8)")
for cx in CENTERS:
    bands = []
    for y in range(58, 132):
        # digit zone: cx-2 .. cx+4
        n = int(dark[y, cx - 2:cx + 5].sum())
        bands.append((y, n))
    print(f"  col x{cx}: ", end="")
    out = []
    inrun = False
    for y, n in bands:
        if n >= 2 and not inrun:
            inrun = True; a = y
        elif n < 2 and inrun:
            inrun = False; out.append((a, y - 1))
    if inrun: out.append((a, 131))
    print(" ".join(f"y{a}-{b}" for a, b in out))

print("\nT1: paren column x-bands per row (to see cell structure)")
for y0, y1 in [(76, 110)]:
    sub = dark[y0:y1 + 1, 88:229]
    cc = sub.sum(axis=0)
    xs = np.where(cc > 0)[0]
    runs = []; s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 3:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    print(f"  rows {y0}..{y1}: " + " ".join(f"[{88+a}-{88+b}]" for a, b in runs))

print("\nT2: per column, digit-glyph y-bands")
for cx in [101, 123, 145, 167, 189, 212]:
    bands = []
    for y in range(140, 250):
        n = int(dark[y, cx - 2:cx + 5].sum())
        bands.append((y, n))
    out = []; inrun = False
    for y, n in bands:
        if n >= 2 and not inrun:
            inrun = True; a = y
        elif n < 2 and inrun:
            inrun = False; out.append((a, y - 1))
    if inrun: out.append((a, 249))
    print(f"  col x{cx}: " + " ".join(f"y{a}-{b}" for a, b in out))
