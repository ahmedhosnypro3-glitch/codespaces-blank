#!/usr/bin/env python3
"""Pixel measurement of slide_016 original frame vs fresh render.

Measures: background color, title/subtitle ink bands, cap heights, ink widths,
per-span colors (red vs blue), badge bbox+color, bottom strip, border.
"""
import sys
from PIL import Image
import numpy as np

ORIG = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_016.jpg"
RENDER = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/recreated_pptx/build/slide_016_rendered-1.png"


def load(p):
    im = Image.open(p).convert("RGB")
    return np.asarray(im).astype(int)


def classify(arr):
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    mx = arr.max(axis=2)
    mn = arr.min(axis=2)
    sat = mx - mn
    bg = (abs(r - 234) < 12) & (abs(g - 234) < 12) & (abs(b - 234) < 12)
    red = (r > 90) & (r < 235) & (g < 110) & (b < 110) & (r - g > 55) & (r - b > 55)
    blue = (b > 90) & (b - r > 55) & (b - g > 55)
    black = (mx < 110)
    yellow = (r > 190) & (g > 170) & (b < 150) & (r - b > 60)
    ink = ~bg
    return dict(r=r, g=g, b=b, bg=bg, red=red, blue=blue, black=black, yellow=yellow, ink=ink)


def rowprofile(m, label):
    print(f"\n--- {label}: rows with ink counts (rows where ink>3) ---")
    ink = m["ink"]
    rows = []
    for y in range(ink.shape[0]):
        c = int(ink[y].sum())
        if c > 3:
            rows.append((y, c))
    # group contiguous bands
    bands = []
    start = prev = None
    for y, c in rows:
        if start is None:
            start = prev = y
        elif y == prev + 1:
            prev = y
        else:
            bands.append((start, prev))
            start = prev = y
    if start is not None:
        bands.append((start, prev))
    for (a, b) in bands:
        seg = ink[a:b + 1]
        cols = np.where(seg.any(axis=0))[0]
        print(f"  band rows {a}-{b} (h={b-a+1})  x {cols.min()}-{cols.max()} (w={cols.max()-cols.min()+1})  maxrow={int(seg.sum(axis=1).max())}")
    return bands


def span_report(m, label, y0, y1):
    seg = lambda k: m[k][y0:y1 + 1]
    red, blue, black = seg("red"), seg("blue"), seg("black")
    print(f"\n--- {label}: region rows {y0}-{y1} ---")
    for name, msk in (("red", red), ("blue", blue), ("black", black)):
        n = int(msk.sum())
        if n:
            cols = np.where(msk.any(axis=0))[0]
            print(f"  {name}: {n} px, x {cols.min()}-{cols.max()}")
        else:
            print(f"  {name}: 0 px")
    # strongest ink colors
    reg = (slice(y0, y1 + 1), slice(None))
    cols, counts = np.unique(m["r"][reg].ravel(), return_counts=True)
    order = np.argsort(-counts)[:6]
    print("  top R-channel values:", [(int(cols[i]), int(counts[i])) for i in order])


def main():
    for path, label in ((ORIG, "ORIGINAL 960x540"), (RENDER, "RENDER 2001x1125")):
        arr = load(path)
        m = classify(arr)
        h, w = arr.shape[:2]
        print(f"\n==================== {label} ====================")
        print("bg sample px:", arr[5, 5], arr[h // 2, 10], "corner count:", int(m["bg"].sum()), "/", h * w)
        bands = rowprofile(m, label)
        # badge region: top-right
        bx0, bx1 = int(w * 0.90), w - 1
        by0, by1 = 0, int(h * 0.12)
        ymask = m["yellow"][by0:by1, bx0:bx1]
        if ymask.any():
            ys, xs = np.where(ymask)
            print(f"\n  BADGE yellow bbox: x {bx0+xs.min()}-{bx0+xs.max()}, y {by0+ys.min()}-{by0+ys.max()} "
                  f"(w={xs.max()-xs.min()+1}, h={ys.max()-ys.min()+1})")
            cols = np.unique(m["r"][by0:by1, bx0:bx1][ymask])
            print("  badge fill R values (top5):", np.sort(cols)[-5:].tolist())
        else:
            print("\n  BADGE: no yellow found in top-right")
        # bottom strip
        tail = m["black"][int(h * 0.90):, :]
        ys = np.where(tail.any(axis=1))[0]
        print(f"  bottom black strip: rows {int(h*0.90)+ys.min() if len(ys) else None}-{int(h*0.90)+ys.max() if len(ys) else None}")
        # text bands = bands excluding frame/badge/strip: use red+blue+dark ink in central area
        print("\n  RED pixel rows (any):", end=" ")
        rr = np.where(m["red"].any(axis=1))[0]
        print(f"{rr.min()}-{rr.max()}" if len(rr) else "none")
        print("  BLUE pixel rows (any):", end=" ")
        br = np.where(m["blue"].any(axis=1))[0]
        print(f"{br.min()}-{br.max()}" if len(br) else "none")
        if len(br):
            span_report(m, label + " BLUE zone", br.min() - 2, br.max() + 2)


if __name__ == "__main__":
    main()
