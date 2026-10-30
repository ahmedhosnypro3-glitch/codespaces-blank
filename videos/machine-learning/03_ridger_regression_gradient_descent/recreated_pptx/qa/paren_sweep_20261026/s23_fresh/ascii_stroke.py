#!/usr/bin/env python3
"""ASCII-render an image region's ink mask so curve direction is readable
in text (PIL-first adjudication; no vision calls)."""
import argparse

import numpy as np
from PIL import Image


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("image")
    ap.add_argument("x0", type=int)
    ap.add_argument("y0", type=int)
    ap.add_argument("x1", type=int)
    ap.add_argument("y1", type=int)
    ap.add_argument("--thresh", type=int, default=160)
    ap.add_argument("--step", type=int, default=2, help="pixel step per cell")
    ap.add_argument("--chars", default=" .:#@")
    args = ap.parse_args()

    im = Image.open(args.image).convert("L")
    a = np.asarray(im, dtype=np.float64)
    reg = a[args.y0:args.y1, args.x0:args.x1]
    h, w = reg.shape
    ink = np.clip(args.thresh - reg, 0, None)
    ny, nx = h // args.step, w // args.step
    print(f"# {args.image} region x{args.x0}..{args.x1} y{args.y0}..{args.y1} "
          f"({w}x{h}) step={args.step} -> grid {nx}x{ny}")
    chars = args.chars
    levels = len(chars) - 1
    for gy in range(ny):
        row = ""
        for gx in range(nx):
            cell = ink[gy*args.step:(gy+1)*args.step,
                       gx*args.step:(gx+1)*args.step]
            v = cell.mean() / (args.thresh * 0.6)
            idx = min(levels, int(v * levels + 0.5))
            row += chars[idx]
        print(row)


if __name__ == "__main__":
    main()
