#!/usr/bin/env python3
"""Scan-line color transition probe for slide 006 original (PIL only)."""
from PIL import Image
import numpy as np
from pathlib import Path

V = Path("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks")
a = np.array(Image.open(V / "unique_slides/slide_006.jpg").convert("RGB")).astype(int)

def hscan(label, y, x0, x1, step=1):
    print(f"\n--- hscan {label} y={y} x{x0}-{x1} ---")
    prev = None
    for x in range(x0, x1, step):
        c = a[y, x]
        key = tuple((c // 24) * 24)
        if key != prev:
            print(f"  x={x:4d} rgb={tuple(c)}")
            prev = key

def vscan(label, x, y0, y1, step=1):
    print(f"\n--- vscan {label} x={x} y{y0}-{y1} ---")
    prev = None
    for y in range(y0, y1, step):
        c = a[y, x]
        key = tuple((c // 24) * 24)
        if key != prev:
            print(f"  y={y:4d} rgb={tuple(c)}")
            prev = key

hscan("eq box middle row (inside box)", 168, 60, 500)
hscan("below eq box (panel + callout)", 380, 60, 500)
vscan("eq box left edge", 200, 90, 260)
vscan("panel interior", 850, 130, 510)
hscan("panel mid", 300, 380, 900)
hscan("panel top strip", 150, 380, 900)
hscan("panel bottom strip", 490, 380, 900)

print("\n=== pink activation boxes (tight mask, x>690) ===")
sub = a[:, 690:800]
d = np.abs(sub - np.array([255, 204, 255])).sum(axis=2)
m = d <= 45
ys, xs = np.where(m)
print("pink px:", len(ys), end=" ")
if len(ys):
    print(f"x {690+xs.min()}-{690+xs.max()} y {ys.min()}-{ys.max()}")
    # row profile
    for y in range(ys.min(), ys.max() + 1):
        xs2 = np.where(m[y])[0]
        if len(xs2):
            print(f"  y={y}: x {690+xs2.min()}-{690+xs2.max()} n={len(xs2)}")
