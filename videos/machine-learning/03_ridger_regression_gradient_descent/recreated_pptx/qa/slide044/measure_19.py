#!/usr/bin/env python3
"""Colour-map the rule text line + all red/blue text clusters in the centre."""
import numpy as np
from PIL import Image

IM = np.asarray(Image.open(
    "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
    "03_ridger_regression_gradient_descent/unique_slides/slide_044.jpg"
).convert("RGB")).astype(int)
rf, gf, bf = IM[:, :, 0], IM[:, :, 1], IM[:, :, 2]
LUM = 0.299 * rf + 0.587 * gf + 0.114 * bf
satred = (rf - gf > 45) & (rf - bf > 45) & (rf > 110)
satblue = (bf - rf > 40) & (bf - gf > 25) & (bf > 110)
dark = LUM < 175

print("=== RULE LINE y105..128, x470..620 ===")
print("     " + "".join(str((x // 10) % 10) for x in range(470, 620)))
print("     " + "".join(str(x % 10) for x in range(470, 620)))
for y in range(105, 129):
    line = ""
    for x in range(470, 620):
        if satblue[y, x]: line += "B"
        elif satred[y, x]: line += "R"
        elif dark[y, x]: line += "#"
        elif LUM[y, x] < 200: line += "+"
        else: line += " "
    print(f"{y:>4} {line}")

print("\n=== RED clusters in centre-text region (x250..715, y58..128) ===")
sub = satred[58:129, 250:716]
cc = sub.sum(axis=0)
xs = np.where(cc > 0)[0]
if len(xs):
    runs = []
    s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 3:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        ys = np.where(sub[:, a:b + 1].any(axis=1))[0]
        print(f"  RED x{250+a}..{250+b} w{b-a+1}  y{58+ys.min()}..{58+ys.max()} px={int(sub[:, a:b+1].sum())}")

print("\n=== BLUE clusters in centre-text region ===")
sub = satblue[58:129, 250:716]
cc = sub.sum(axis=0)
xs = np.where(cc > 0)[0]
if len(xs):
    runs = []
    s = xs[0]
    for i in range(1, len(xs)):
        if xs[i] - xs[i - 1] > 3:
            runs.append((s, xs[i - 1])); s = xs[i]
    runs.append((s, xs[-1]))
    for a, b in runs:
        ys = np.where(sub[:, a:b + 1].any(axis=1))[0]
        print(f"  BLUE x{250+a}..{250+b} w{b-a+1}  y{58+ys.min()}..{58+ys.max()} px={int(sub[:, a:b+1].sum())}")
