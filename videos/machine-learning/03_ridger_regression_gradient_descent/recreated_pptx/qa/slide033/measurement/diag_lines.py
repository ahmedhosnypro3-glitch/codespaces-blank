#!/usr/bin/env python3
"""Count real table rows/cols by clustering text-token positions in the original."""
import numpy as np
from PIL import Image

o = np.asarray(Image.open("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_033.jpg").convert("RGB")).astype(int)
r, g, b = o[:, :, 0], o[:, :, 1], o[:, :, 2]

print("=== TEXT-LINE DETECTION: dark ink row-clusters inside table (y320-519) ===")
# dark ink: luminance low
lum = o.sum(axis=2)
dark = lum < 330
sub = dark[318:522, 86:870]
has_ink = sub.any(axis=1)
runs = []
start = None
for i, v in enumerate(has_ink):
    if v and start is None:
        start = i
    elif not v and start is not None:
        runs.append((start + 318, i - 1 + 318))
        start = None
if start is not None:
    runs.append((start + 318, 521))
print("dark-ink row runs:", runs)

print("\n=== Per text-line: column token clusters (numbers) ===")
for y0, y1 in runs:
    if y1 - y0 < 3:
        continue
    cols = np.where(dark[y0:y1 + 1, 86:870].any(axis=0))[0] + 86
    # cluster columns into tokens with gap >=4
    toks = []
    cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] >= 4:
            toks.append((cur[0], cur[-1]))
            cur = [c]
        else:
            cur.append(c)
    toks.append((cur[0], cur[-1]))
    print(f"  rows {y0}-{y1} (h={y1-y0+1}): {len(toks)} tokens")
    print(f"    token cols: {toks}")

print("\n=== WHITE/light text on dark bands? (bands 0,1 are light) ===")
# check the yellow-highlight band0 for white text
band0 = o[332:368, 86:870]
lum0 = band0.sum(axis=2)
light = lum0 > 650
ys_, xs_ = np.where(light)
print(f"  band0 light(>650) px: {len(ys_)}")
if len(ys_):
    cols = xs_ + 86
    toks = []
    cur = [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] >= 4:
            toks.append((cur[0], cur[-1])); cur = [c]
        else: cur.append(c)
    toks.append((cur[0], cur[-1]))
    print(f"  band0 light tokens: {len(toks)}: {toks}")

print("\n=== Red-bold text rows: exact rows and token cols ===")
red = (r > 140) & (r - g > 60) & (r - b > 60)
R = np.zeros_like(red); R[460:520, 86:870] = red[460:520, 86:870]
ys_, xs_ = np.where(R)
if len(ys_):
    runs = []
    start = None
    has = R[460:520, 86:870].any(axis=0)
    # row clusters
    hrows = R[460:520, :].any(axis=1)
    for i, v in enumerate(hrows):
        if v and start is None: start = i
        elif not v and start is not None:
            runs.append((start+460, i-1+460)); start = None
    if start is not None: runs.append((start+460, 519))
    print("  red row runs:", runs)
    for y0, y1 in runs:
        if y1-y0 < 3: continue
        cols = np.where(red[y0:y1+1, 86:870].any(axis=0))[0] + 86
        toks = []
        cur = [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] >= 4:
                toks.append((cur[0], cur[-1])); cur=[c]
            else: cur.append(c)
        toks.append((cur[0], cur[-1]))
        print(f"    rows {y0}-{y1}: {len(toks)} tokens {toks}")

print("\n=== Yellow highlight band0: is the WHOLE band yellow or just columns? ===")
band0y = o[336:366, 86:870]
yy = (band0y[:,:,0] > 190) & (band0y[:,:,1] > 190) & (band0y[:,:,2] < 170)
frac = yy.mean(axis=0)
# find contiguous runs where frac > 0.5
runs = []
start = None
for i, v in enumerate(frac > 0.5):
    if v and start is None: start = i
    elif not v and start is not None:
        if i - start > 8: runs.append((start + 86, i - 1 + 86))
        start = None
if start is not None: runs.append((start + 86, len(frac) - 1 + 86))
print(f"  yellow column runs (>50% of rows): {runs}")

print("\n=== Title/subtitle exact text rows ===")
for name, y0, y1, x0, x1 in [("title", 60, 95, 150, 460), ("subL1", 92, 118, 90, 520), ("subL2", 118, 145, 150, 860)]:
    sub_dark = (o[y0:y1, x0:x1].sum(axis=2) < 420)
    ys_, xs_ = np.where(sub_dark)
    if len(ys_):
        cols = xs_ + x0
        toks = []
        cur = [cols[0]]
        for c in cols[1:]:
            if c - cur[-1] >= 10:
                if cur[-1]-cur[0] > 3: toks.append((cur[0], cur[-1]))
                cur = [c]
            else: cur.append(c)
        if cur[-1]-cur[0] > 3: toks.append((cur[0], cur[-1]))
        print(f"  {name}: rows {y0+ys_.min()}-{y0+ys_.max()}, {len(toks)} word-groups")
        print(f"     groups: {toks}")
