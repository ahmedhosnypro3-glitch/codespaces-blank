#!/usr/bin/env python3
"""Precise ink-run listing + grayscale ASCII for slide-041 regions."""
import os, sys
import numpy as np
from PIL import Image

ORIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "unique_slides", "slide_041.jpg"))
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)


def bgdist(a):
    return np.abs(a - np.array([254, 255, 232])).sum(axis=-1)


def runs(x0, x1, y):
    """Ink runs on row y between x0..x1 (inclusive)."""
    d = bgdist(A[y, x0:x1 + 1])
    m = d > 90
    out = []
    i = 0
    while i < len(m):
        if m[i]:
            j = i
            while j + 1 < len(m) and m[j + 1]:
                j += 1
            out.append((x0 + i, x0 + j))
            i = j + 1
        else:
            i += 1
    return out


def gray(x0, y0, x1, y1, ramp=" .:-=+*#%@"):
    g = A[y0:y1 + 1, x0:x1 + 1].mean(axis=2)
    print(f"--- grayscale x{x0}..{x1} y{y0}..{y1}")
    hdr = "".join(str((x0 + i) // 100 % 10) if (x0 + i) % 10 == 0 else " " for i in range(x1 - x0 + 1))
    print("    " + hdr)
    hdr = "".join(str((x0 + i) // 10 % 10) if (x0 + i) % 10 == 0 else " " for i in range(x1 - x0 + 1))
    print("    " + hdr)
    for j, row in enumerate(g):
        s = "".join(ramp[min(9, int((255 - v) / 25.6))] for v in row)
        print(f"y{y0+j:3d} {s}")


def rowruns(x0, x1, y0, y1, label=""):
    print(f"=== ink runs {label} x{x0}..{x1}")
    for y in range(y0, y1 + 1):
        print(f"y{y:3d} " + " ".join(f"{a}-{b}" for a, b in runs(x0, x1, y)))


if __name__ == "__main__":
    print("###### MID BAND ######")
    rowruns(255, 360, 56, 108, "mid")
    print()
    gray(262, 74, 330, 86, ramp=" .:-=+*#%@")
    print()
    print("###### RIGHT TEXT ######")
    gray(494, 76, 588, 91)
    print()
    print("###### LEGEND TAIL ######")
    gray(425, 108, 525, 124)
    print()
    print("###### Z LABELS ######")
    gray(596, 60, 660, 78)
    print()
    print("###### CLASS SUBSCRIPTS ######")
    for (x0, x1) in [(90, 104), (112, 126), (134, 148), (156, 171), (178, 194), (201, 216)]:
        gray(x0, 108, x1, 126)
        print()
