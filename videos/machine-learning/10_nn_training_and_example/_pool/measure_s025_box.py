#!/usr/bin/env python3
"""Final: box extents, header extents, chart inner geometry, Node Bias color."""
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
img = Image.open(f"{BASE}/slide_025.jpg").convert("RGB")
a = np.asarray(img).astype(int)


def profile(y, x0, x1, label):
    prev = None
    print(f"  {label} y={y}:")
    for x in range(x0, x1):
        px = tuple(a[y, x])
        kind = "bg"
        if px[0] > 240 and px[1] > 222 and px[2] < 235 and px[0] - px[2] > 18:
            kind = "peach"
        elif px[0] > 243 and px[1] > 248 and px[2] > 215 and px[2] < 248:
            kind = "cream"
        elif abs(px[0] - px[1]) < 12 and abs(px[1] - px[2]) < 12 and 210 < px[0] < 245:
            kind = "gray"
        if kind != prev:
            print(f"     x={x} {kind} {px}")
            prev = kind


print("=== box1 row y=175 ===")
profile(175, 30, 320, "box1")
print("=== box2 row y=250 ===")
profile(250, 30, 320, "box2")
print("=== box1 col x=300 ===")
for y in range(160, 240):
    px = tuple(a[y, 300])
    if y % 3 == 0:
        print(f"     y={y} {px}")

print("\n=== Node Bias color samples ===")
for x in (322, 330, 345, 355, 365):
    print(f"  ({x},293)={tuple(a[293,x])}  ({x},296)={tuple(a[296,x])}")

print("\n=== navy frame rows/cols ===")
navy = (a[:, :, 2] > 90) & (a[:, :, 0] < 80) & (a[:, :, 1] < 80)
for y in (346, 496, 516):
    xs = np.where(navy[y, 40:360])[0] + 40
    print(f"  left chart y={y}: navy cols {xs[:12]} ... {xs[-6:] if len(xs) else ''}")
for x in (54, 56, 88, 199, 311, 344):
    ys = np.where(navy[340:520, x])[0] + 340
    print(f"  left chart x={x}: navy rows {ys[:8]} ... {ys[-6:] if len(ys) else ''}")

print("\n=== right chart navy frame ===")
for y in (361, 362, 503, 516):
    xs = np.where(navy[y, 360:900])[0] + 360
    print(f"  y={y}: cols {xs[:10]} ... {xs[-6:] if len(xs) else ''}")
for x in (363, 385, 610, 665, 875, 888):
    ys = np.where(navy[355:520, x])[0] + 355
    print(f"  x={x}: rows {ys[:8]} ... {ys[-6:] if len(ys) else ''}")
