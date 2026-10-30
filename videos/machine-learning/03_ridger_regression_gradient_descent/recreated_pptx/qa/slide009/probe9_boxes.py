#!/usr/bin/env python3
"""Probe 9: exact ink runs inside/around the annotation boxes."""
import numpy as np
from PIL import Image

FRAME = ("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/"
         "03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg")
a = np.asarray(Image.open(FRAME).convert("RGB")).astype(int)
H, W = a.shape[:2]

def runs(idx, gap=1):
    idx = [int(v) for v in idx]
    if not idx:
        return []
    out, s, p = [], idx[0], idx[0]
    for v in idx[1:]:
        if v <= p + gap:
            p = v
            continue
        out.append((s, p))
        s = p = v
    out.append((s, p))
    return out

def ink_scan(nm, x0, x1, y0, y1, mask):
    print(f"\n=== {nm}: x{x0}..{x1} y{y0}..{y1} ink runs ===")
    for y in range(y0, y1 + 1):
        xs = np.where(mask[y, x0:x1])[0]
        rr = runs(xs + x0, gap=2)
        if rr:
            tot = sum(b - s + 1 for s, b in rr)
            print(f"  y={y:4d} n={tot:4d}: {rr}")

# ---------- LEFT annotation box: any non-pure-white pixel ----------
left_white = (a[:, :, 0] > 250) & (a[:, :, 1] > 249) & (a[:, :, 2] > 249)
left_ink = ~left_white
print("### LEFT box: non-white runs (rows 100..190, x 88..475) ###")
ink_scan("LEFTBOX", 88, 475, 100, 190, left_ink)

print("\n### LEFT box bottom: rows 460..480 ###")
ink_scan("LEFTBOT", 88, 475, 458, 480, left_ink)

# ---------- RIGHT annotation box ----------
print("\n### RIGHT box: non-white runs (rows 100..190, x 478..880) ###")
ink_scan("RIGHTBOX", 478, 880, 100, 190, left_ink)
print("\n### RIGHT box bottom: rows 458..480 ###")
ink_scan("RIGHTBOT", 478, 880, 458, 480, left_ink)

# ---------- exact colors across the box border ----------
print("\n=== LEFT box top border profile (x=250, y 103..115) ===")
for y in range(103, 116):
    print(f"  y={y}: {tuple(int(v) for v in a[y, 250])}")
print("=== LEFT box left border profile (y=120, x 90..101) ===")
for x in range(90, 102):
    print(f"  x={x}: {tuple(int(v) for v in a[120, x])}")
print("=== LEFT box right border profile (y=120, x 460..473) ===")
for x in range(460, 474):
    print(f"  x={x}: {tuple(int(v) for v in a[120, x])}")

# ---------- equation text ink rows (dark) ----------
print("\n=== LEFT equation dark text rows ===")
dark = (a[:, :, 0] < 120) & (a[:, :, 1] < 120) & (a[:, :, 2] < 150)
ink_scan("LEFTEQ", 88, 475, 140, 185, dark)
print("\n=== RIGHT equation dark text rows ===")
ink_scan("RIGHTEQ", 478, 880, 140, 185, dark)

# ---------- '50.85 mm' label: dark text near the axis ----------
print("\n=== LEFT 'mm' label dark ink (x 96..140, y 440..535) ===")
ink_scan("LEFTMM", 96, 145, 440, 535, dark)
print("\n=== RIGHT 'mm' label dark ink (x 490..545, y 440..535) ===")
ink_scan("RIGHTMM", 490, 545, 440, 535, dark)

# ---------- caption text rows (red) ----------
red = (a[:, :, 0] > 90) & ((a[:, :, 0] - a[:, :, 1]) > 40) & ((a[:,:,0]-a[:,:,2]) > 10)
print("\n=== LEFT caption red ink rows (y 480..535) ===")
ink_scan("LEFTCAP", 88, 475, 480, 535, red)
print("\n=== RIGHT caption red ink rows (y 480..535) ===")
ink_scan("RIGHTCAP", 478, 880, 480, 535, red)
