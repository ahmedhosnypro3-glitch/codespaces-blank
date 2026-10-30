#!/usr/bin/env python3
"""Locate a colored-text cluster in render vs original by cell histogram.

Usage: cluster_r5.py <NNN> <r> <g> <b> <tol> <cell> <x0> <y0> <x1> <y1> [render_path]
Prints non-empty cells (color pixels per cell) for render and original.
"""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"


def load(path, size=(960, 540)):
    im = Image.open(path).convert("RGB")
    if im.size != size:
        im = im.resize(size, Image.LANCZOS)
    return np.asarray(im).astype(int)


def cells(a, rgb, tol, cell, x0, y0, x1, y1):
    rgb = tuple(int(v) for v in rgb)
    mask = (np.abs(a - np.array(rgb, dtype=int)).sum(axis=2) < tol)
    rows = []
    for y in range(y0, y1, cell):
        line = ""
        for x in range(x0, x1, cell):
            n = int(mask[y:y + cell, x:x + cell].sum())
            line += "." if n == 0 else (str(n) if n < 10 else chr(ord("a") + min(n // 10, 25)))
        rows.append(line)
    return rows


def main():
    n, r, g, b, tol, cell, x0, y0, x1, y1 = sys.argv[1:11]
    tol, cell = int(tol), int(cell)
    x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
    rp = sys.argv[11] if len(sys.argv) > 11 else f"{BASE}/qa/slide{n}/rejudge/render-1.png"
    rend = load(rp)
    orig = load(f"{BASE}/unique_slides/slide_{n}.jpg")
    rc = cells(rend, (r, g, b), tol, cell, x0, y0, x1, y1)
    oc = cells(orig, (r, g, b), tol, cell, x0, y0, x1, y1)
    hdr = f"### slide {n} color=({r},{g},{b}) tol={tol} cell={cell} region=({x0},{y0})-({x1},{y1})"
    print(hdr)
    print("    RENDER                                 |   ORIGINAL")
    for a, b2 in zip(rc, oc):
        print(f"    {a}   |   {b2}")


main()
