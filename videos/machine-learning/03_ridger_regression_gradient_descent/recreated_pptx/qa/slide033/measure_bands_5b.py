#!/usr/bin/env python3
"""Precise, clean band measurement for slide 033 (frame px, 1px=1pt).

Two questions, answered with numbers:
  A) exact y-extent of each of the 5 fill bands (contiguous runs, >100px wide),
  B) does the fill cover the LABEL column (x86-121) or only the data columns?

Samples the label column and the data columns separately, and reports the modal
colour of the label column inside each band's y-range.
"""
from PIL import Image
import numpy as np, collections

ORIG = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
        "03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg")
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

BANDS = {
    "D9E275": (217, 226, 119),
    "D6B2F5": (214, 178, 248),
    "F7DDC2": (247, 221, 194),
    "DEAC95": (222, 172, 149),
    "F7BEC4": (247, 190, 196),
}

# A) contiguous y runs with >60 px of the colour in x121..869
print("=== A) contiguous y-runs (>60 px wide in x121..869) ===")
for name, (R, G, B) in BANDS.items():
    m = (np.abs(o[:, :, 0] - R) < 20) & (np.abs(o[:, :, 1] - G) < 20) & (np.abs(o[:, :, 2] - B) < 28)
    counts = {y: int(m[y, 121:869].sum()) for y in range(320, 520)}
    runs, cur = [], None
    for y in range(320, 520):
        if counts[y] > 60:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur:
            if cur[1] - cur[0] >= 2: runs.append(tuple(cur))
            cur = None
    if cur and cur[1] - cur[0] >= 2: runs.append(tuple(cur))
    print(f"{name}: {runs}")

print()
print("=== B) label-column (x86-121) modal colour inside each band ===")
for name, (R, G, B) in BANDS.items():
    m = (np.abs(o[:, :, 0] - R) < 20) & (np.abs(o[:, :, 1] - G) < 20) & (np.abs(o[:, :, 2] - B) < 28)
    counts = {y: int(m[y, 121:869].sum()) for y in range(320, 520)}
    runs, cur = [], None
    for y in range(320, 520):
        if counts[y] > 60:
            cur = [y, y] if cur is None else [cur[0], y]
        elif cur:
            if cur[1] - cur[0] >= 2: runs.append(tuple(cur))
            cur = None
    if cur and cur[1] - cur[0] >= 2: runs.append(tuple(cur))
    for (y0, y1) in runs:
        cl = collections.Counter()
        for y in range(y0, y1 + 1):
            for x in range(88, 120):
                cl[tuple(o[y, x])] += 1
        cd = collections.Counter()
        for y in range(y0, y1 + 1):
            for x in range(125, 865, 2):
                cd[tuple(o[y, x])] += 1
        print(f"{name} y{y0}-{y1}:")
        print(f"   label col modal: {cl.most_common(3)}")
        print(f"   data  col modal: {cd.most_common(2)}")
        # match fraction of the target colour in each
        def frac(cnt, tot):
            hit = sum(v for k, v in cnt.items() if all(abs(k[i] - (R, G, B)[i]) < 20 for i in range(3)))
            return hit / tot if tot else 0
        print(f"   label-col match frac {frac(cl, sum(cl.values())):.3f} ; data-col match frac {frac(cd, sum(cd.values())):.3f}")
