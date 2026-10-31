#!/usr/bin/env python3
"""W5 PIL-first probe for slide015 FULL FAIL (judge_full.txt 02:18).
Claims: D-1 'W' missing inside J( ) on eq line 1; D-2 'I' missing in lambda*I*W
on gradient line 2. Build assets: eq_015_eq1_l1.png mathtext has J(\\underline{W});
deriv_l2 has \\lambda I \\underline{W}. Verify in the RENDER pixels. Read-only."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide015"
r = np.asarray(Image.open(f"{D}/render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{NS}/unique_slides/slide_015.jpg").convert("RGB")).astype(int)
sc = r.shape[1] / 960.0
print(f"render {r.shape[1]}x{r.shape[0]} scale {sc:.4f}")

# eq1 line 1 lives in cream rect A; from build: rect(73,?,...) -- locate the
# first equation band by scanning for dense ink rows in x73-894
def ink_rows(a, x0, x1):
    s = a.shape[1] / 960.0
    sub = a[:, int(x0 * s):int(x1 * s)]
    ink = sub.sum(axis=2) < 600
    return ink.sum(axis=1)

for name, a in (("orig", o), ("render", r)):
    rows = ink_rows(a, 73, 894)
    # find text bands (groups of rows with ink > 5)
    bands = []
    inb = False
    for y, v in enumerate(rows):
        if v > 5 and not inb:
            start = y; inb = True
        elif v <= 5 and inb:
            bands.append((start, y)); inb = False
    s = a.shape[1] / 960.0
    print(name, "ink row bands (slide y):", [(round(a0 / s, 1), round(a1 / s, 1)) for a0, a1 in bands][:14])

# zoom on the J( ... ) opening of eq line 1: find first ink cluster after x~90
# in the first eq band of each image
def first_eq_band(a):
    s = a.shape[1] / 960.0
    rows = ink_rows(a, 73, 894)
    bands = []
    inb = False
    for y, v in enumerate(rows):
        if v > 5 and not inb:
            start = y; inb = True
        elif v <= 5 and inb:
            bands.append((start, y)); inb = False
    return bands[0] if bands else None

for name, a in (("orig", o), ("render", r)):
    s = a.shape[1] / 960.0
    b = first_eq_band(a)
    if not b:
        continue
    y0, y1 = b
    band = a[y0:y1, int(80 * s):int(320 * s)]
    ink = band.sum(axis=2) < 600
    colprof = ink.sum(axis=0)
    prof = "".join("#" if c > 0 else "." for c in colprof)
    print(f"{name} eq1-L1 col-profile x80-320 (slide): {prof}")
    # ink inside the J( ) parens: parens are first tall cluster; count ink
    # columns between first and second tall glyph group
    ys, xs = np.where(ink)
    if len(xs):
        print(f"   ink bbox in zone: x{80+xs.min()/s:.1f}-{80+xs.max()/s:.1f} ink={int(ink.sum())}")
