#!/usr/bin/env python3
"""PIL-first adjudication of judge_attempt_33's 4 MINORs (slide 031, render_33).

M1: gap 'bold'->'5.1' on annotation-box line 1 (topblock crop)
M2: red dashed line at x=5 extends below x-axis (graph crop)
M3: parabola stroke tint grayer in render (graph crop)
M4: '(?,?)' missing space after comma vs original '(?, ?)' (graph crop)

Crop pairs are at matched effective scale -> coords directly comparable.
Graph crop region = frame [565,58]-[817,275]; topblock = [36,52]-[648,342].
"""
import numpy as np
from PIL import Image

D = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide031"

def load(n):
    return np.asarray(Image.open(f"{D}/crop_33_{n}_render.png").convert("RGB")).astype(int), \
           np.asarray(Image.open(f"{D}/crop_33_{n}_orig.png").convert("RGB")).astype(int)

gr, go = load("graph")
tr, to = load("topblock")

def redmask(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (R > 90) & (G < 0.72 * R) & (B < 0.78 * R)

def darkmask(im, t=100):
    return (im[..., 0] < t) & (im[..., 1] < t) & (im[..., 2] < t)

def col_clusters(mask, y0, y1, x0, x1, gap=3):
    cols = mask[y0:y1, x0:x1].sum(axis=0)
    runs, s = [], None
    for i, c in enumerate(cols):
        if c > 0 and s is None: s = i
        if c == 0 and s is not None:
            runs.append((s, i - 1)); s = None
    if s is not None: runs.append((s, len(cols) - 1))
    merged = []
    for a, b in runs:
        if merged and a - merged[-1][1] <= gap: merged[-1] = (merged[-1][0], b)
        else: merged.append((a, b))
    return [(x0 + a, x0 + b) for a, b in merged], cols

print("=" * 70)
print("M2: red dashed line at x=5 — red-ink row profile in graph crop")
print("=" * 70)
# frame x=5 tick at 687 -> crop x ~254; scan band
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    rm = redmask(im)
    band = rm[:, 240:270]
    rows = band.sum(axis=1)
    ink = np.nonzero(rows)[0]
    print(f"{tag}: red rows {ink.min()}..{ink.max()}, total {rows.sum()}")
    # per-row detail near the bottom (y 380..452)
    print("  y:count from y380:", " ".join(f"{y}:{rows[y]}" for y in range(380, min(452, len(rows))) if rows[y] > 0))
# black axis row: longest horizontal dark run
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    dm = darkmask(im, 110)
    rowsum = dm.sum(axis=1)
    cand = [(y, int(rowsum[y])) for y in range(380, 452) if rowsum[y] > 100]
    print(f"{tag}: dark horizontal runs >100px in y380..452: {cand[:8]}")

print()
print("=" * 70)
print("M4: '(?, ?)' label glyph clusters in graph crop (dark ink)")
print("=" * 70)
# find it: scan right half of graph crop for dark text rows
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    dm = darkmask(im, 120)
    # labels live above y~200; search x 260..520, y 130..215
    sub = dm[125:220, 255:520]
    rows = sub.sum(axis=1)
    ys = np.nonzero(rows > 2)[0]
    if len(ys):
        print(f"{tag}: dark-text rows y{125+ys.min()}..{125+ys.max()}")
        # cluster columns in the densest band
        y0, y1 = 125 + ys.min(), 125 + ys.max() + 1
        cl, cols = col_clusters(dm, y0, y1, 255, 520, gap=4)
        print(f"  clusters x: {cl}")
    else:
        print(f"{tag}: no dark text rows found in y125..220, x255..520")

print()
print("=" * 70)
print("M3: parabola stroke tint — blue-ink mean RGB along right arm")
print("=" * 70)
def bluemask(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (B > R + 25) & (B > G + 10) & (B > 90)
for tag, im in (("RENDER", gr), ("ORIG  ", go)):
    bm = bluemask(im)
    sel = im[bm & (np.arange(gr.shape[0])[:, None] < 400)]
    # restrict to parabola x-range (crop x 100..420), exclude axis labels region x<60
    ys, xs = np.nonzero(bm)
    keep = (xs > 60) & (xs < 430) & (ys > 20)
    px = im[ys[keep], xs[keep]]
    if len(px):
        print(f"{tag}: n={len(px)} meanRGB=({px[:,0].mean():.0f},{px[:,1].mean():.0f},{px[:,2].mean():.0f}) "
              f"median=({np.median(px[:,0]):.0f},{np.median(px[:,1]):.0f},{np.median(px[:,2]):.0f})")

print()
print("=" * 70)
print("M1: annotation box line 1 — glyph clusters, gap 'bold'->'5.1' (topblock crop)")
print("=" * 70)
# locate the green annotation box: green fill G>R and G>B
def greenfill(im):
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    return (G > 150) & (G > R + 15) & (G > B + 5)
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    gm = greenfill(im)
    ys, xs = np.nonzero(gm)
    print(f"{tag}: green fill bbox x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(xs)}")

# text inside box = dark OR red OR blue ink on light green
for tag, im in (("RENDER", tr), ("ORIG  ", to)):
    gm = greenfill(im)
    ys, xs = np.nonzero(gm)
    bx0, bx1, by0, by1 = xs.min(), xs.max(), ys.min(), ys.max()
    R, G, B = im[..., 0], im[..., 1], im[..., 2]
    ink = ((R < 150) & (G < 160) & (B < 170)) | redmask(im) | bluemask(im)
    # line bands: horizontal ink profile inside box
    prof = ink[by0:by1+1, bx0:bx1+1].sum(axis=1)
    lines, s = [], None
    for i, c in enumerate(prof):
        if c > 3 and s is None: s = i
        if c <= 3 and s is not None:
            if i - s > 6: lines.append((by0 + s, by0 + i - 1))
            s = None
    if s is not None: lines.append((by0 + s, by0 + len(prof) - 1))
    print(f"{tag}: text-line bands inside green box: {lines}")
    if lines:
        y0, y1 = lines[0]
        cl, cols = col_clusters(ink, y0, y1 + 1, bx0, bx1 + 1, gap=4)
        print(f"  line1 y{y0}..{y1} clusters: {cl}")
        # gaps between consecutive clusters
        gaps = [(cl[i+1][0] - cl[i][1], cl[i][1], cl[i+1][0]) for i in range(len(cl) - 1)]
        print(f"  line1 gaps: {gaps}")
        # red clusters on line 1 (the '5.1')
        rm = redmask(im)
        rcl, _ = col_clusters(rm, y0, y1 + 1, bx0, bx1 + 1, gap=4)
        print(f"  line1 RED clusters: {rcl}")
