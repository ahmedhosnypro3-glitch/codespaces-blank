#!/usr/bin/env python3
"""Column-class analyzer: for the green box's 3 text lines, classify each column's
ink into dark/red/yellow within the text band; print exact runs per class."""
import numpy as np
from PIL import Image

im = Image.open('/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg')
a = np.array(im).astype(int)
R, G, B = a[:,:,0], a[:,:,1], a[:,:,2]

def runs(idx, gap=2):
    """runs of True with gap-merge; returns (start, end) index pairs"""
    out = []
    i = 0
    n = len(idx)
    while i < n:
        if idx[i]:
            s = i
            while i < n and idx[i]:
                i += 1
            e = i - 1
            # merge with next if gap small
            out.append([s, e])
        else:
            i += 1
    merged = []
    for r in out:
        if merged and r[0] - merged[-1][1] - 1 <= gap:
            merged[-1][1] = r[1]
        else:
            merged.append(r)
    return merged

def analyze(y0, y1, x0, x1, label):
    print(f"\n===== {label} (y{y0}..{y1}, x{x0}..{x1})")
    reg = a[y0:y1+1, x0:x1+1]
    r, g, b = reg[:,:,0], reg[:,:,1], reg[:,:,2]
    dark = (r < 150) & (g < 150) & (b < 150)
    red_strict = (r > 120) & (r - g > 80) & (r - b > 80)
    red_loose = (r > 130) & (r - g > 60) & (r - b > 60)
    yel = (r > 230) & (g > 190) & (g - b > 25) & (r - b > 40)
    classes = [('DARK', dark), ('REDstrict', red_strict), ('REDloose', red_loose), ('YELLOW', yel)]
    for name, m in classes:
        colhas = m.any(axis=0)
        rr = runs(colhas, gap=3)
        print(f"  {name}: " + ", ".join(f"[{s+x0}..{e+x0}]" for s, e in rr))
    # for each dark/loose-red run, print y-extent and dominant color
    print("  -- cluster details (merged ink = dark OR red_loose):")
    ink = dark | red_loose
    colhas = ink.any(axis=0)
    rr = runs(colhas, gap=4)
    for s, e in rr:
        sub = ink[:, s:e+1]
        cols = np.where(sub.any(axis=0))[0]
        # y extent
        ys = np.where(sub.any(axis=1))[0]
        px = reg[:, s:e+1][sub]
        nred = int(red_loose[:, s:e+1][sub].sum())
        ndark = int(dark[:, s:e+1][sub].sum())
        from collections import Counter
        dom = Counter(tuple(p) for p in px).most_common(1)[0][0] if len(px) else None
        print(f"   x[{s+x0}..{e+x0}] w={e-s+1} y[{ys[0]+y0}..{ys[-1]+y0}] dark={ndark} red={nred} dom={dom}")

analyze(110, 145, 100, 400, "LINE1 Recall:")
analyze(146, 192, 100, 460, "LINE2 equation")
analyze(193, 216, 100, 770, "LINE3 dimension note")
