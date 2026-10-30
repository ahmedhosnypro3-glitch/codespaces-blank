#!/usr/bin/env python3
"""Probe 8j: raw loose-threshold structure of the ORIG vector regions (left + right box)."""
from PIL import Image
import numpy as np

ORIG = np.asarray(Image.open("unique_slides/slide_004.jpg").convert("RGB")).astype(int)

def raw_map(x0, y0, x1, y1, label):
    print(f"--- {label} x{x0}..{x1} y{y0}..{y1} (2px/char; ink=any ch<235; r>150&g<135&b<135=red) ---")
    reg = ORIG[y0:y1, x0:x1]
    ink = reg.max(axis=2) < 235
    red = (reg[:,:,0] > 150) & (reg[:,:,1] < 135) & (reg[:,:,2] < 135)
    for yy in range(0, y1 - y0, 2):
        row = ""
        for xx in range(0, x1 - x0, 2):
            bd = ink[yy:yy+2, xx:xx+2].sum()
            br = red[yy:yy+2, xx:xx+2].sum()
            row += "R" if br >= 2 else "#" if bd >= 3 else ("+" if bd else ".")
        print(f"{y0+yy:3d} {row}")
    # per-row x-extent of ink in the delim candidate bands
    print("  per-row ink x-extent (rows with ink):")
    for yy in range(y0, y1):
        cols = np.where(ink[yy - y0])[0]
        if len(cols) > 1:
            print(f"    y{yy}: x{x0+cols.min()}..{x0+cols.max()} n={len(cols)}")

raw_map(150, 100, 215, 212, "ORIG left-box vector region")
print()
raw_map(455, 100, 545, 212, "ORIG right-box vector region")
