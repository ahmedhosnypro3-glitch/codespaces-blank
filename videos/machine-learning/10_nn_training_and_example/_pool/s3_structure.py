#!/usr/bin/env python3
"""Structural probe of the original slide_003 diagram (PIL, no vision).

Detects the purple input dots, the coloured summation-node circles, and the
green output boxes so the recreation can match node counts and columns.
"""
import sys
import numpy as np
from PIL import Image

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example"
PPI = 13.33 / 960


def blobs(mask, gap=6):
    """Group mask pixels into connected components via row runs."""
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return []
    pts = sorted(zip(ys.tolist(), xs.tolist()))
    seen = set()
    out = []
    for y, x in pts:
        if (y, x) in seen:
            continue
        stack = [(y, x)]
        comp = []
        seen.add((y, x))
        while stack:
            cy, cx = stack.pop()
            comp.append((cy, cx))
            for dy in range(-gap, gap + 1):
                for dx in range(-gap, gap + 1):
                    p = (cy + dy, cx + dx)
                    if p in seen:
                        continue
                    if 0 <= p[0] < mask.shape[0] and 0 <= p[1] < mask.shape[1] and mask[p]:
                        seen.add(p)
                        stack.append(p)
        cys = [p[0] for p in comp]
        cxs = [p[1] for p in comp]
        out.append((min(cxs), min(cys), max(cxs), max(cys), len(comp)))
    return out


def main():
    a = np.asarray(Image.open(f"{BASE}/unique_slides/slide_003.jpg").convert("RGB")).astype(int)
    H, W = a.shape[:2]
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    purple = (r > 70) & (r < 180) & (g < 80) & (b > 90) & (b < 200)
    print(f"# purple blobs (input dots / bias circles): {len(blobs(purple))}")
    for x0, y0, x1, y1, n in sorted(blobs(purple), key=lambda t: (t[1], t[0])):
        print(f"  bbox x={x0}-{x1} y={y0}-{y1} px={n}  center=({(x0+x1)//2},{(y0+y1)//2})")

    for name, m in [
        ("dark-red", (r > 100) & (r < 180) & (g < 55) & (b < 55)),
        ("blue", (b > 110) & (b > r + 45) & (b > g + 45) & (g < 120)),
        ("green", (g > 90) & (g > r + 45) & (g > b + 45) & (r < 130)),
    ]:
        bs = [t for t in blobs(m, gap=4) if t[4] >= 12]
        print(f"# {name} blobs: {len(bs)}")
        for x0, y0, x1, y1, n in sorted(bs, key=lambda t: (t[0], t[1])):
            print(f"  bbox x={x0}-{x1} y={y0}-{y1} px={n} center=({(x0+x1)//2},{(y0+y1)//2})")


if __name__ == "__main__":
    main()
