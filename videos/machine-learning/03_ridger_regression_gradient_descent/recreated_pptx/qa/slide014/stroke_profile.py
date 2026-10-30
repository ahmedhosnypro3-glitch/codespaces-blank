#!/usr/bin/env python3
"""Stroke-curvature + horizontal-run profile for the vector boxes.
A curved x-center vs y profile => parenthesis; a straight one => bracket."""
import numpy as np
from PIL import Image

NS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
      "03_ridger_regression_gradient_descent/")
og = np.asarray(Image.open(NS + "unique_slides/slide_014.jpg").convert("RGB")).astype(int)


def ink(y, x):
    R, G, B = og[y, x]
    if R > 242 and G > 242 and B > 242:
        return False
    if abs(R - 233) < 14 and abs(G - 233) < 14 and abs(B - 231) < 14:
        return False
    return True


def stroke_center(y, xa, xb):
    xs = [x for x in range(xa, xb) if ink(y, x)]
    return (min(xs) + max(xs)) / 2.0 if xs else None


print("### LEFT BOX stroke centers (window x 160..200)")
for y in range(100, 225):
    a = stroke_center(y, 160, 172)
    b = stroke_center(y, 172, 200)
    c = stroke_center(y, 200, 240)
    print(f"  y={y:3d} L~{a if a else '-'} M~{b if b else '-'} R~{c if c else '-'}")

print("\n### RIGHT BOX stroke centers (window x 534..576)")
for y in range(100, 225):
    a = stroke_center(y, 534, 546)
    b = stroke_center(y, 546, 574)
    c = stroke_center(y, 574, 610)
    print(f"  y={y:3d} L~{a if a else '-'} M~{b if b else '-'} R~{c if c else '-'}")

print("\n### LEFT BOX horizontal ink runs > 8px (underline candidates)")
for y in range(100, 240):
    xs = [x for x in range(84, 430) if ink(y, x)]
    if not xs:
        continue
    runs, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= 2:
            cur.append(x)
        else:
            runs.append((cur[0], cur[-1]))
            cur = [x]
    runs.append((cur[0], cur[-1]))
    long_runs = [r for r in runs if r[1] - r[0] >= 8]
    if long_runs:
        print(f"  y={y:3d}: {long_runs}")

print("\n### RIGHT BOX horizontal ink runs > 8px")
for y in range(100, 240):
    xs = [x for x in range(462, 806) if ink(y, x)]
    if not xs:
        continue
    runs, cur = [], [xs[0]]
    for x in xs[1:]:
        if x - cur[-1] <= 2:
            cur.append(x)
        else:
            runs.append((cur[0], cur[-1]))
            cur = [x]
    runs.append((cur[0], cur[-1]))
    long_runs = [r for r in runs if r[1] - r[0] >= 8]
    if long_runs:
        print(f"  y={y:3d}: {long_runs}")
