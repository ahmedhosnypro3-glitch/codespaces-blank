#!/usr/bin/env python3
"""Panel/frame geometry for scope_a18 slides: find red rectangle borders and dividers."""
import sys
from PIL import Image
import numpy as np

BASE = "/home/codespace/ai_llm_slides/videos/machine-learning/10_nn_training_and_example/unique_slides"
PPI = 13.33 / 960


def groups(idx, gap=2):
    idx = sorted(idx)
    out, start, prev = [], None, None
    for v in idx:
        if start is None:
            start = prev = v
        elif v - prev <= gap:
            prev = v
        else:
            out.append((start, prev))
            start = prev = v
    if start is not None:
        out.append((start, prev))
    return out


def analyze(n):
    a = np.asarray(Image.open(f"{BASE}/slide_{n:03d}.jpg").convert("RGB")).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    H, W = a.shape[:2]
    print(f"===== SLIDE {n} =====")
    red = (r > 130) & (r - g > 45) & (r - b > 45)

    # Strong red lines: rows where >=120 red px (full-width rules)
    rs = red.sum(axis=1)
    strong_rows = [(y, int(rs[y])) for y in range(H) if rs[y] >= 120]
    print("-- strong RED horizontal rules (>=120px):")
    for y0, y1 in groups([y for y, _ in strong_rows]):
        print(f"   rows {y0}..{y1}  ({y0*PPI:.2f}in..{y1*PPI:.2f}in)")

    cs = red.sum(axis=0)
    strong_cols = [(x, int(cs[x])) for x in range(W) if cs[x] >= 120]
    print("-- strong RED vertical rules (>=120px):")
    for x0, x1 in groups([x for x, _ in strong_cols]):
        print(f"   cols {x0}..{x1}  ({x0*PPI:.2f}in..{x1*PPI:.2f}in)")

    # Green rules
    green = (g > 100) & (g - r > 25) & (g - b > 25)
    grs = green.sum(axis=1)
    print("-- GREEN horizontal rules (>=40px):",
          [(y, int(grs[y])) for y in range(H) if grs[y] >= 40][:25])
    grc = green.sum(axis=0)
    print("-- GREEN vertical rules (>=40px):",
          [(x, int(grc[x])) for x in range(W) if grc[x] >= 40][:25])

    # Blue text bands grouped
    blue = (b > 130) & (b - r > 45) & (b - g > 25)
    bs = blue.sum(axis=1)
    print("-- BLUE row groups (rows with >=3 blue px):")
    for y0, y1 in groups([y for y in range(H) if bs[y] >= 3]):
        m = blue[y0:y1 + 1]
        cc = np.where(m.any(axis=0))[0]
        print(f"   rows {y0}..{y1} ({y0*PPI:.2f}..{y1*PPI:.2f}in) cols {cc.min()}..{cc.max()}")


for n in [int(x) for x in sys.argv[1:]] or [31, 32]:
    analyze(n)
    print()
