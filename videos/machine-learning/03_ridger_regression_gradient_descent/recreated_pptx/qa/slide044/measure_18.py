#!/usr/bin/env python3
"""Find all long straight blue strokes (box borders) and long red strokes."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
blue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
red = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)

print("=== HORIZONTAL blue runs >= 25px ===")
for y in range(48, 536):
    xs = np.where(blue[y])[0]
    if len(xs) < 25:
        continue
    # group into runs
    runs = []
    s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 2:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        if b - a >= 25:
            print(f"  y{y}: x{a}..{b} len {b - a + 1}")

print("\n=== VERTICAL blue runs >= 25px ===")
for x in range(60, 900):
    ys = np.where(blue[:, x])[0]
    if len(ys) < 25:
        continue
    runs = []
    s = ys[0]
    for i in range(1, len(ys)):
        if ys[i] - ys[i - 1] > 2:
            runs.append((s, ys[i - 1])); s = ys[i]
    runs.append((s, ys[-1]))
    for a, b in runs:
        if b - a >= 25:
            print(f"  x{x}: y{a}..{b} len {b - a + 1}")

print("\n=== HORIZONTAL red runs >= 30px ===")
for y in range(48, 536):
    xs = np.where(red[y])[0]
    if len(xs) < 30:
        continue
    runs = []
    s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 2:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        if b - a >= 30:
            print(f"  y{y}: x{a}..{b} len {b - a + 1}")
