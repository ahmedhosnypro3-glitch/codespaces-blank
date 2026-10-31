#!/usr/bin/env python3
"""W5 PIL-first probe for slide014 crop FAIL (crop_dense_judge_retry.txt 02:32).
Claims: #1 color-code (Loss red / R green in orig vs render), #2 dropped vector
underlines in band 2, #3 band/row offset. Read-only."""
import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
D = f"{NS}/recreated_pptx/qa/rejudge_20261027/slide014"
r = np.asarray(Image.open(f"{D}/crop_dense_render.png").convert("RGB")).astype(int)
o = np.asarray(Image.open(f"{D}/crop_dense_orig.png").convert("RGB")).astype(int)
H, W = r.shape[:2]
print(f"crop size {W}x{H}")

def dark_rows(a, thr=600, minrun=200):
    rows = []
    ink = a.sum(axis=2) < thr
    for y in range(a.shape[0]):
        # longest run
        best = cur = 0
        for v in ink[y]:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= minrun:
            rows.append(y)
    # group
    groups = []
    for y in rows:
        if groups and y - groups[-1][-1] <= 2:
            groups[-1].append(y)
        else:
            groups.append([y])
    return [int(np.mean(g)) for g in groups]

print("render band-rule rows:", dark_rows(r))
print("orig   band-rule rows:", dark_rows(o))

# color census of band-2 equation text: find non-background ink in the
# middle horizontal band of each crop (judge: y~225-265 crop px)
def color_census(a, y0, y1, label):
    band = a[y0:y1]
    ink = band.sum(axis=2) < 600
    px = band[ink]
    if len(px) == 0:
        print(label, "no ink"); return
    med = np.median(px, axis=0).astype(int)
    red = int(((px[:, 0] > 120) & (px[:, 0] > px[:, 2] + 40) & (px[:, 0] > px[:, 1] + 40)).sum())
    green = int(((px[:, 1] > 80) & (px[:, 1] > px[:, 0] + 30) & (px[:, 1] > px[:, 2] + 30)).sum())
    blue = int(((px[:, 2] > 100) & (px[:, 2] > px[:, 0] + 40) & (px[:, 2] > px[:, 1] + 40)).sum())
    dark = int((px.sum(axis=1) < 300).sum())
    print(f"{label}: ink={len(px)} med={tuple(med)} red={red} green={green} blue={blue} dark={dark}")

# locate band 2 (yellow) rows in each crop to bound the eq text
for name, a in (("render", r), ("orig", o)):
    yel = (np.abs(a[:, :, 0] - 255) < 25) & (np.abs(a[:, :, 1] - 255) < 25) & (a[:, :, 2] < 120)
    rows = np.where(yel.sum(axis=1) > W * 0.3)[0]
    if len(rows):
        # find groups
        groups = []
        for y in rows:
            if groups and y - groups[-1][-1] <= 3:
                groups[-1].append(y)
            else:
                groups.append([y])
        print(name, "yellow band row groups:", [(g[0], g[-1]) for g in groups])

# underline probe: in band-2 text row, look for horizontal dark/colored runs
# BELOW the glyph baseline (rows with long runs of same hue within text band)
def underline_probe(a, name):
    yel = (np.abs(a[:, :, 0] - 255) < 25) & (np.abs(a[:, :, 1] - 255) < 25) & (a[:, :, 2] < 120)
    rowsum = yel.sum(axis=1)
    ys = np.where(rowsum > W * 0.3)[0]
    if not len(ys):
        print(name, "no yellow band"); return
    y0, y1 = ys.min(), ys.max()
    sub = a[y0:y1 + 1]
    ink = sub.sum(axis=2) < 600
    # rows below mid-band with runs >= 25 px
    mid = (y1 - y0) // 2
    found = []
    for yy in range(mid, sub.shape[0]):
        cur = best = 0
        for v in ink[yy]:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= 25:
            found.append((y0 + yy, best))
    print(name, "band2 rows y%d-%d; sub-baseline long runs (y,run):" % (y0, y1), found[:20])

underline_probe(r, "render")
underline_probe(o, "orig")

# color census of the equation line inside band 2 (middle of yellow band)
def band2_colors(a, name):
    yel = (np.abs(a[:, :, 0] - 255) < 25) & (np.abs(a[:, :, 1] - 255) < 25) & (a[:, :, 2] < 120)
    rowsum = yel.sum(axis=1)
    ys = np.where(rowsum > W * 0.3)[0]
    if not len(ys):
        return
    y0, y1 = ys.min(), ys.max()
    mid0, mid1 = y0 + (y1 - y0) // 3, y0 + 2 * (y1 - y0) // 3
    color_census(a, mid0, mid1, f"{name} band2 text rows {mid0}-{mid1}")

band2_colors(r, "render")
band2_colors(o, "orig")
