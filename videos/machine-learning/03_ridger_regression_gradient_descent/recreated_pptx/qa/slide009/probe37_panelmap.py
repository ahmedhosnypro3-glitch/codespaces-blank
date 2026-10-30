#!/usr/bin/env python3
"""Probe 37: full-panel class-map ASCII (every 2nd px) for both chart panels.
Classes: ' '=white interior, '.'=grid gray, 'R'=red family, 'B'=blue family,
'O'=orange family, '#'=navy border, '~'=pale-blue annotation box.
"""
import numpy as np
from PIL import Image

SRC = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_009.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
mx = np.maximum(np.maximum(r, g), b)
mn = np.minimum(np.minimum(r, g), b)
sat = mx - mn

RED = (r > 90) & ((r - g) > 40) & ((r - b) > 10)
ORA = (r >= 160) & (g >= 85) & (g <= 155) & (b <= 125) & ((r - b) >= 70)
BLU = (b > 120) & ((b - r) > 40) & ((b - g) > 30)
NAVY = (b > 90) & ((b - r) > 40) & ((b - g) > 30)   # dark navy border family
PALE = (b > 240) & ((b - r) > 6) & (g >= r - 4)     # annotation box fill
GRID = (r > 225) & (r < 250) & (sat < 12)           # light gray grid

def cls(y, x):
    if NAVY[y, x]: return "#"
    if PALE[y, x]: return "~"
    if ORA[y, x]: return "O"
    if RED[y, x]: return "R"
    if BLU[y, x]: return "B"
    if GRID[y, x]: return "."
    return " "

def panel(name, x0, x1, y0, y1, step=2):
    print(f"===== {name} x{x0}..{x1} y{y0}..{y1} (step {step}) =====")
    hdr = "       "
    for xx in range(x0, x1+1, step):
        hdr += str((xx // 100) % 10) if xx % 50 < step else " "
    print(hdr)
    hdr2 = "       "
    for xx in range(x0, x1+1, step):
        hdr2 += str((xx // 10) % 10) if xx % 50 < step else " "
    print(hdr2)
    for yy in range(y0, y1+1, step):
        print(f"{yy:5d}  " + "".join(cls(yy, xx) for xx in range(x0, x1+1, step)))

panel("LEFT", 94, 466, 106, 475, 2)
