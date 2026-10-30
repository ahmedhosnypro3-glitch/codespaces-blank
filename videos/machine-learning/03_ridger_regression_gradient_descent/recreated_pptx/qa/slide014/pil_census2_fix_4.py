#!/usr/bin/env python3
"""Fill-aware census: for each band rect, modal fill color, then ink = deviation.
Extracts text lines (rows), their x extents, and ink colors. Both ORIGINAL and RENDER.
"""
from PIL import Image
import numpy as np
from collections import Counter

def census(path, bands, ymax, tag):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    print(f"\n########## {tag}: {path} size={a.shape[1]}x{a.shape[0]}")
    for (name, x0, x1, y0, y1) in bands:
        if y1 >= a.shape[0]: y1 = a.shape[0] - 1
        sub = a[y0:y1+1, x0:x1+1].reshape(-1, 3)
        # modal color
        cnt = Counter(map(tuple, sub[::3]))
        mode, n = cnt.most_common(1)[0]
        d = np.abs(sub - np.array(mode)).sum(axis=1)
        ink = sub[d > 90]          # deviation from fill = ink/border
        dwhite = np.abs(sub - np.array([255, 255, 255])).sum(axis=1)
        ink2 = sub[(d > 90) & (dwhite > 90)]  # exclude pure white (canvas/other bg)
        # rows with ink
        sub2 = a[y0:y1+1, x0:x1+1]
        dd = np.abs(sub2 - np.array(mode)).sum(axis=2)
        dw = np.abs(sub2 - np.array([255, 255, 255])).sum(axis=2)
        mask = (dd > 90) & (dw > 90)
        rows = mask.sum(axis=1)
        inkrows = [y0 + i for i, v in enumerate(rows) if v >= 3]
        lines = []
        if inkrows:
            s = inkrows[0]; p = inkrows[0]
            for y in inkrows[1:]:
                if y - p > 3:
                    lines.append((s, p)); s = y
                p = y
            lines.append((s, p))
        print(f"\n--- {name}: x{x0}..{x1} y{y0}..{y1} mode={mode} (n={n}/{len(sub)}) inkpx_total={int(mask.sum())}")
        for (ly0, ly1) in lines:
            xs = []
            cols = []
            for y in range(ly0, ly1 + 1):
                row = mask[y - y0]
                curry = a[y]
                for x in range(x0, x1 + 1):
                    if row[x - x0]:
                        xs.append(x); cols.append(tuple(curry[x]))
            xa, xb = min(xs), max(xs)
            cc = Counter(cols)
            top = cc.most_common(4)
            print(f"    line y{ly0}..{ly1} (h={ly1-ly0+1}) x{xa}..{xb} (w={xb-xa+1}) inkpx={len(xs)} colors={top}")

if __name__ == "__main__":
    import sys
    # bands in FRAME space (960x540): name, x0, x1, y0, y1
    orig_bands = [
        ("title", 60, 900, 48, 110),
        ("ridge", 92, 877, 246, 282),
        ("objective", 91, 877, 306, 337),
        ("midband1", 90, 665, 348, 392),
        ("midband2", 89, 471, 402, 445),
        ("midband3", 533, 880, 403, 445),
        ("lowerblue", 91, 883, 467, 530),
        ("leftbox", 80, 433, 100, 236),
        ("rightbox", 457, 810, 100, 236),
    ]
    census("unique_slides/slide_014.jpg", orig_bands, 540, "ORIGINAL")
