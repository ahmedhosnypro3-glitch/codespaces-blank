#!/usr/bin/env python3
"""Geometry measurement for scope_a18 slides (31, 32).

Measures: red/blue/green ink bands, long vertical+horizontal rules, gray fill
regions, yellow badge bbox. Source frames are 960x540 -> 13.33x7.5in (72.02 px/in).
"""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
PPI = 13.33 / 960


def runs_of(idx, minlen=2):
    out, start = [], None
    for i in idx:
        if start is None:
            start = i
        elif i != idx[len(out) and -1] + 1:
            pass
    # simpler: contiguous grouping
    vals = list(idx)
    out, start, prev = [], None, None
    for v in vals:
        if start is None:
            start = prev = v
        elif v == prev + 1:
            prev = v
        else:
            out.append((start, prev))
            start = prev = v
    if start is not None:
        out.append((start, prev))
    return [o for o in out if o[1] - o[0] + 1 >= minlen]


def bands(mask, axis, minlen=3):
    """Return list of (start,end) runs along axis where mask has any ink."""
    if axis == 0:
        prof = mask.any(axis=0)
    else:
        prof = mask.any(axis=1)
    idx = np.where(prof)[0]
    return runs_of(idx, minlen)


def analyze(n):
    img = Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB")
    a = np.asarray(img).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    H, W = a.shape[:2]
    print(f"===== SLIDE {n}  ({W}x{H}) =====")

    red = (r > 130) & (r - g > 45) & (r - b > 45)
    blue = (b > 130) & (b - r > 45) & (b - g > 25)
    green = (g > 100) & (g - r > 25) & (g - b > 25)
    yellow = (r > 210) & (g > 200) & (b < 180)
    gray = (abs(r - g) < 12) & (abs(g - b) < 12) & (r > 170) & (r < 210)

    for name, m in (("RED", red), ("BLUE", blue), ("GREEN", green)):
        rb = bands(m, 1, 3)
        cb = bands(m, 0, 3)
        print(f"-- {name} ink: {m.sum()} px")
        print(f"   row bands: {[(int(s), int(e)) for s, e in rb]}")
        print(f"   col bands: {[(int(s), int(e)) for s, e in cb]}")

    # long vertical red rules
    cs = red.sum(axis=0)
    print("-- RED cols with >40px vertical run:",
          [(x, int(cs[x])) for x in range(W) if cs[x] > 40])
    rs = red.sum(axis=1)
    print("-- RED rows with >40px horizontal run:",
          [(y, int(rs[y])) for y in range(H) if rs[y] > 40])

    # gray fill blocks
    gs = gray.sum(axis=1)
    print("-- GRAY rows with >50px:",
          [(y, int(gs[y])) for y in range(H) if gs[y] > 50][:40])

    # yellow badge
    ys, xs = np.where(yellow)
    if len(xs):
        print(f"-- YELLOW badge bbox x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}"
              f"  (in: {xs.min()*PPI:.2f}..{xs.max()*PPI:.2f} / {ys.min()*PPI:.2f}..{ys.max()*PPI:.2f})")


for n in [int(x) for x in sys.argv[1:]] or [31, 32]:
    analyze(n)
    print()
