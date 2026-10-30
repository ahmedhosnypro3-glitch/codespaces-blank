#!/usr/bin/env python3
"""Structural color map of the original + render: classify every cell of a
frame-px grid into a color class and print a compact ASCII map, so the true band
layout (full-width vs half-width, gradients, overlapping bands) is visible.
"""
import numpy as np
from PIL import Image

DECK = "videos/machine-learning/03_ridger_regression_gradient_descent"
o = np.asarray(Image.open(f"{DECK}/unique_slides/slide_014.jpg").convert("RGB")).astype(int)
r = np.asarray(Image.open(f"{DECK}/recreated_pptx/qa/slide014/render_2.png").convert("RGB")).astype(int)
SC = r.shape[0] / 540.0

# reference colors (frame-px space)
REFS = {
    "W": (255, 255, 255),   # white
    "g": (232, 233, 232),   # panel gray E9E9E7 / E8E8E8
    "y": (250, 253, 219),   # pale yellow band
    "p": (250, 224, 194),   # peach band
    "s": (255, 225, 229),   # pale pink band
    "b": (236, 254, 252),   # pale blue band
    "B": (0, 0, 0),         # black ink
    "R": (192, 0, 0),       # red
    "G": (0, 128, 0),       # green
    "u": (0, 0, 255),       # blue ink
}

CELL = 10  # frame px per map cell


def classify(c):
    best, bd = "?", 1e9
    for k, v in REFS.items():
        d = abs(int(c[0])-v[0]) + abs(int(c[1])-v[1]) + abs(int(c[2])-v[2])
        if d < bd:
            bd, best = d, k
    return best if bd <= 60 else "."


def render_map(im, scale, title):
    H = im.shape[0]
    print("=" * 100)
    print(title)
    print("     " + "".join(str((x // 10) % 10) for x in range(0, 960, CELL)))
    for y in range(0, 540, CELL):
        row = []
        for x in range(0, 960, CELL):
            c = im[int((y + CELL/2) * scale), int((x + CELL/2) * scale)]
            row.append(classify(c))
        print(f"{y:4d} " + "".join(row))
    print()


render_map(o, 1.0, "ORIGINAL slide_014.jpg (960x540), cell = 10 frame-px")
render_map(r, SC, "RENDER render_2.png at 150dpi (cell center sampled in frame-px space)")
