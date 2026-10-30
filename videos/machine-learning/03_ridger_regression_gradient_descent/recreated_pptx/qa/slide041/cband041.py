#!/usr/bin/env python3
"""Colour-coded ASCII dump of slide-041 text bands."""
import os, sys
import numpy as np
from PIL import Image

ORIG = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "unique_slides", "slide_041.jpg"))
A = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)


def cls(r, g, b):
    mx, mn = max(r, g, b), min(r, g, b)
    if mx - mn < 40:
        if mx < 140:
            return "K"   # black/dark
        return "."       # pale background
    if r == mx and g < 170 and b < 170:
        return "R"
    if b == mx and r < 180:
        return "B"
    if g == mx and r < 180:
        return "G"
    return "?"


def dump(x0, y0, x1, y1, step=1, chunk=130):
    for xs in range(x0, x1, chunk):
        xe = min(xs + chunk, x1)
        print(f"### x {xs}..{xe-1}  y {y0}..{y1-1}")
        hdr = "".join(str((xs + i) // 100 % 10) if (xs + i) % 10 == 0 else " " for i in range(xe - xs))
        print("     " + hdr)
        hdr2 = "".join(str((xs + i) // 10 % 10) if (xs + i) % 10 == 0 else " " for i in range(xe - xs))
        print("     " + hdr2)
        for y in range(y0, y1, step):
            row = "".join(cls(*A[y, x]) for x in range(xs, xe))
            print(f"y{y:3d} {row}")
        print()


if __name__ == "__main__":
    args = sys.argv[1:]
    if args:
        dump(*[int(a) for a in args])
    else:
        dump(230, 55, 365, 95)
        dump(360, 55, 600, 95)
        dump(230, 104, 600, 130)
