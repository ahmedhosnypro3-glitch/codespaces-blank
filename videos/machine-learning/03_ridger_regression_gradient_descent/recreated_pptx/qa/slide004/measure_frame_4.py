#!/usr/bin/env python3
"""Structural measurement of slide_004.jpg — pass 4.

A) Long-run border line detection (red / blue / lavender), grouped into boxes.
B) Zoomed 4px ASCII maps per box interior to read the text-line structure.
"""
import numpy as np
from PIL import Image

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_004.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

red = (r > 100) & ((r - g) > 50) & ((r - b) > 30)
blue = (b > 90) & ((b - r) > 50) & ((b - g) > 30)
lav = ((b - r) >= 4) & (b > 225) & (r > 180) & ((b - g) >= 3)  # pale blue border family
dark = (r + g + b) < 330


def runs(mask_1d, min_len=1):
    out, d = [], np.diff(np.concatenate(([0], mask_1d.astype(int), [0])))
    for s, e in zip(np.where(d == 1)[0], np.where(d == -1)[0] - 1):
        if e - s + 1 >= min_len:
            out.append((int(s), int(e)))
    return out


print("=== A) long horizontal border lines (len>=60 of consecutive-ish ink) ===")
for name, m in [("RED", red), ("BLUE", blue), ("LAV", lav)]:
    for y in range(45, 540):
        rr = runs(m[y, 60:903], min_len=40)
        for s, e in rr:
            print(f"  {name} hline y={y} x {60+s}..{60+e} (len {e-s+1})")

print("\n=== B) long vertical border lines (len>=40) ===")
for name, m in [("RED", red), ("BLUE", blue), ("LAV", lav)]:
    for x in range(60, 905):
        rr = runs(m[45:540, x], min_len=30)
        for s, e in rr:
            print(f"  {name} vline x={x} y {45+s}..{45+e} (len {e-s+1})")

print("\n=== C) zoomed 4px maps ===")
CL = {
    "R": lambda R, G, B: R > 100 and (R - G) > 50 and (R - B) > 30,
    "B": lambda R, G, B: B > 90 and (B - R) > 50 and (B - G) > 30,
    "K": lambda R, G, B: (R + G + B) < 330,
    # fills
    "Y": lambda R, G, B: R > 235 and G > 235 and 195 < B < 245,   # cream/yellow fill
    "P": lambda R, G, B: R > 245 and 210 < G < 250 and B < 225 and (R - B) > 20,  # salmon
    "L": lambda R, G, B: (B - R) >= 4 and B > 225 and 180 < R < 240,  # lavender
    "G": lambda R, G, B: abs(R - 231) < 10 and abs(G - 233) < 10 and abs(B - 230) < 12,
}


def zoom(name, x0, x1, y0, y1, cell=4):
    print(f"\n--- {name} x {x0}..{x1} y {y0}..{y1} (cell {cell}px) ---")
    hdr = "     " + "".join(str((x0 + i * cell) // 100 % 10) for i in range((x1 - x0) // cell))
    print(hdr)
    for cy in range(y0, y1, cell):
        line = []
        for cx in range(x0, x1, cell):
            block = im[cy:cy + cell, cx:cx + cell].reshape(-1, 3)
            best, bestc = 0, "."
            for ch, fn in (("R", CL["R"]), ("B", CL["B"]), ("K", CL["K"]),
                           ("P", CL["P"]), ("L", CL["L"]), ("Y", CL["Y"]), ("G", CL["G"])):
                cnt = sum(1 for px in block[::2] if fn(*px))
                if cnt > best:
                    best, bestc = cnt, ch
            line.append(bestc if best >= 2 else ("W" if best == 0 else bestc))
        print(f"{cy:4d} " + "".join(line))


zoom("TITLE", 280, 660, 60, 100, cell=4)
zoom("BOX1 Original Labels", 70, 400, 94, 226, cell=4)
zoom("BOX2 Predicted Labels", 420, 750, 94, 226, cell=4)
zoom("REMEMBER box", 750, 900, 94, 226, cell=4)
zoom("FORMULA box", 490, 890, 210, 240, cell=4)
zoom("L1+L2 left boxes", 70, 495, 238, 372, cell=4)
zoom("OBJ/DEFINE boxes", 70, 670, 380, 530, cell=4)
