#!/usr/bin/env python3
"""Render a crop of an original frame as ASCII art so digits/labels can be read offline.
Usage: read_text.py <img> <x0> <y0> <x1> <y1> [mode]
mode: green (default) | magenta | dark | blue"""
import sys
import numpy as np
from PIL import Image

path = sys.argv[1]
x0, y0, x1, y1 = (int(v) for v in sys.argv[2:6])
mode = sys.argv[6] if len(sys.argv) > 6 else "green"

a = np.asarray(Image.open(path).convert("RGB")).astype(int)[y0:y1, x0:x1]
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
if mode == "green":
    mask = (G - R > 18) & (G - B > 18) & (G > 50)
elif mode == "magenta":
    mask = (R - G > 25) & (B - G > 25) & (R > 80) & (B > 80)
elif mode == "blue":
    mask = (B - R > 45) & (B > 100)
else:
    lum = a.mean(axis=2)
    mask = lum < 150

H, W = mask.shape
for y in range(H):
    print("".join("#" if mask[y, x] else "." for x in range(W)))
