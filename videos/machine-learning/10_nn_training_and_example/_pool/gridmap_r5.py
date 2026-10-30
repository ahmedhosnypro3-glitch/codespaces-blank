#!/usr/bin/env python3
"""Coarse color-grid map of render vs original (ASCII, per-cell dominant class).

Usage: gridmap_r5.py <NNN> [cols] [rows] [x0 y0 x1 y1]
Region defaults to the full frame; cells are classified by nearest palette.
"""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
PAL = {
    ".": (232, 232, 232),   # house bg
    "#": (255, 255, 255),   # white
    "k": (30, 30, 30),      # black ink
    "R": (220, 30, 30),     # red
    "B": (30, 30, 210),     # blue
    "G": (40, 190, 60),     # green
    "O": (255, 130, 40),    # orange
    "Y": (250, 245, 140),   # yellow
    "P": (250, 150, 180),   # pink
    "M": (215, 60, 215),    # magenta
    "c": (247, 241, 228),   # cream panel
    "-": (200, 200, 200),   # light gray
}


def classify(cell):
    c = cell.reshape(-1, 3).mean(axis=0)
    best, bd = None, 1e9
    for ch, ref in PAL.items():
        d = float(((c - np.array(ref)) ** 2).sum())
        if d < bd:
            bd, best = d, ch
    return best


def grid(path, cols, rows, x0, y0, x1, y1, size=(960, 540)):
    im = Image.open(path).convert("RGB")
    if im.size != size:
        im = im.resize(size, Image.LANCZOS)
    a = np.asarray(im).astype(float)
    out = []
    for r in range(rows):
        line = ""
        for c in range(cols):
            xa = x0 + (x1 - x0) * c // cols
            xb = x0 + (x1 - x0) * (c + 1) // cols
            ya = y0 + (y1 - y0) * r // rows
            yb = y0 + (y1 - y0) * (r + 1) // rows
            line += classify(a[ya:yb, xa:xb])
        out.append(line)
    return out


def main():
    n = sys.argv[1]
    cols = int(sys.argv[2]) if len(sys.argv) > 2 else 48
    rows = int(sys.argv[3]) if len(sys.argv) > 3 else 27
    if len(sys.argv) >= 8:
        x0, y0, x1, y1 = (int(v) for v in sys.argv[4:8])
    else:
        x0, y0, x1, y1 = 0, 0, 960, 540
    ren = grid(f"{BASE}/qa/slide{n}/rejudge/render-1.png", cols, rows, x0, y0, x1, y1)
    org = grid(f"{BASE}/unique_slides/slide_{n}.jpg", cols, rows, x0, y0, x1, y1)
    print(f"### slide {n} region=({x0},{y0})-({x1},{y1})  LEFT=render  RIGHT=original")
    for r, o in zip(ren, org):
        print(f"{r}   |   {o}")


main()
