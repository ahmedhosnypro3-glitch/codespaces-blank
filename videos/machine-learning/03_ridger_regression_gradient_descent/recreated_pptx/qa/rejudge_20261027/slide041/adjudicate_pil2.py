#!/usr/bin/env python3
"""Refined read-only measurements for slide 041 adjudication (slide space 960x540)."""
import numpy as np
from PIL import Image

ROOT = "/home/codespace/ai_llm_slides"
NS = f"{ROOT}/videos/machine-learning/03_ridger_regression_gradient_descent"
RJ = f"{NS}/recreated_pptx/qa/rejudge_20261027"

orig = Image.open(f"{NS}/unique_slides/slide_041.jpg").convert("RGB")
ren = Image.open(f"{RJ}/slide041/render.png").convert("RGB").resize((960, 540), Image.LANCZOS)
o = np.asarray(orig).astype(int)
r = np.asarray(ren).astype(int)


def neutral_dark(a, thr=560):
    # gray/black ink only: excludes blue border, red, magenta
    mx = a.max(axis=2)
    mn = a.min(axis=2)
    return (a.sum(axis=2) < thr) & ((mx - mn) < 60)


def redish(a):
    return (a[:, :, 0] > 110) & (a[:, :, 0] - a[:, :, 1] > 50) & (a[:, :, 0] - a[:, :, 2] > 50)


def blueish(a):
    return (a[:, :, 2] > 100) & (a[:, :, 2] - a[:, :, 0] > 40) & (a[:, :, 2] - a[:, :, 1] > 30)


print("=== W-vector delimiters, neutral ink, row-by-row profile ===")
for img, tag in ((o, "ORIG"), (r, "REN")):
    m = neutral_dark(img)
    for x0, x1, lab in ((327, 336, "left"), (349, 358, "right")):
        band = m[57:107, x0:x1]
        rows = []
        for y in range(band.shape[0]):
            xs = np.where(band[y])[0]
            rows.append((x0 + xs.min(), x0 + xs.max()) if len(xs) else None)
        nz = [i for i, v in enumerate(rows) if v]
        if not nz:
            print(f"  {tag} {lab} delim: NO INK")
            continue
        y0, y1 = 57 + nz[0], 57 + nz[-1]
        top = [v for i, v in enumerate(rows) if v and i < (nz[-1] - nz[0] + 1) // 3]
        mid = [v for i, v in enumerate(rows) if v and abs(i - (nz[-1] - nz[0]) / 2) <= 3]
        bot = [v for i, v in enumerate(rows) if v and i >= 2 * (nz[-1] - nz[0] + 1) / 3]
        f = lambda L: (min(v[0] for v in L), max(v[1] for v in L))
        lt, mt, bt = f(top), f(mid), f(bot)
        print(f"  {tag} {lab} delim: ink y{y0}-{y1}; "
              f"top-third x[{lt[0]}..{lt[1]}] w={lt[1]-lt[0]+1} | mid x[{mt[0]}..{mt[1]}] w={mt[1]-mt[0]+1} | "
              f"bot-third x[{bt[0]}..{bt[1]}] w={bt[1]-bt[0]+1}")
        print(f"    interpretation: '(' => mid leftmost < top/bot leftmost, all widths narrow; "
              f"'[' => constant leftmost, top/bot width >> mid width")

print("\n=== col-6 class label color in ORIG (loose thresholds), y108-124, x200-216 ===")
reg = o[108:124, 200:216]
print(f"  red={int(redish(reg).sum())} blue={int(blueish(reg).sum())} neutral_dark={int(neutral_dark(reg).sum())}")
reg_r = r[108:124, 200:216]
print(f"  REN same region: red={int(redish(reg_r).sum())} blue={int(blueish(reg_r).sum())} neutral_dark={int(neutral_dark(reg_r).sum())}")

print("\n=== col-3 digit values: ORIG vs REN crops (slide space), cols x132-148 ===")
for y0, y1, lab in ((74, 90, "top digit"), (92, 108, "bottom digit")):
    co = neutral_dark(o)[y0:y1, 132:148]
    cr = neutral_dark(r)[y0:y1, 132:148]
    print(f"  col3 {lab} y{y0}-{y1}: orig ink={int(co.sum())} ren ink={int(cr.sum())}")

print("\n=== per-column diff orig-vs-render in table region y54-130 ===")
d = np.abs(r - o).sum(axis=2)
mask = d > 90
for i, cx in enumerate([96.5, 118, 140, 163, 185.5, 208]):
    x0, x1 = int(cx) - 11, int(cx) + 11
    sub = mask[54:130, x0:x1]
    print(f"  col{i+1} x{x0}-{x1}: diff px={int(sub.sum())} of {sub.size}")

print("\n=== header subscript digits: are they 1..6? compare orig header crops to ren ===")
for i, cx in enumerate([96.5, 118, 140, 163, 185.5, 208]):
    x0, x1 = int(cx) - 8, int(cx) + 8
    co = neutral_dark(o)[58:74, x0:x1]
    cr = neutral_dark(r)[58:74, x0:x1]
    dd = np.abs(o[58:74, x0:x1] - r[58:74, x0:x1]).sum(axis=2)
    print(f"  header{i+1} x{x0}-{x1}: orig ink={int(co.sum())} ren ink={int(cr.sum())} cropdiff>{90}: {int((dd>90).sum())} px")

print("\n=== gap test: any blank vertical band between col2 and col4 in ORIG headers? ===")
col = neutral_dark(o)[58:74, 60:240].sum(axis=0)
runs = []
idx = np.where(col > 0)[0]
if len(idx):
    s = p = idx[0]
    for i in idx[1:]:
        if i - p > 4:
            runs.append((60 + s, 60 + p))
            s = i
        p = i
    runs.append((60 + s, 60 + p))
print("  orig header ink runs:", runs)
print("  => gap widths between consecutive runs:", [runs[i+1][0]-runs[i][1] for i in range(len(runs)-1)])
