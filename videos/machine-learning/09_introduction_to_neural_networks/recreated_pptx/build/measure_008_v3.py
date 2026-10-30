#!/usr/bin/env python3
"""Pixel measurements of the original slide 008 frame (960x540) for the v2 re-analysis geometry."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
im = Image.open(SRC).convert("RGB")
a = np.array(im).astype(int)
H, W = a.shape[:2]
print("size", W, H)


def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(label, "EMPTY")
        return None
    print(f"{label}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()}  n={len(xs)}")
    return (xs.min(), xs.max(), ys.min(), ys.max())


def near(hexs, tol=40):
    c = np.array([int(hexs[i:i + 2], 16) for i in (1, 3, 5)])
    d = np.abs(a - c).sum(axis=2)
    return d < tol * 3


r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = near("#CC2222", 45)
blue = near("#0000FF", 45)
magenta = near("#FF00FF", 60)
yellow = near("#FFFF00", 40)
pale_y = near("#FFFF99", 30)
salmon = near("#FFE0CC", 30)
green = near("#00A000", 45)
lav = near("#E4E4F5", 18)
pink = near("#F7E0E0", 18)
paleg = near("#E0F0E0", 18)

print("--- title band (y<70) ---")
bbox(red[:70], "title red")
bbox(blue[:70], "title blue")

print("--- badge region (x>780,y<120) ---")
bbox(magenta[:120, 780:], "badge magenta outline")
bbox(pale_y[:120, 780:], "badge pale yellow fill")

print("--- panel: red long lines ---")
col_red = red.sum(axis=0)
row_red = red.sum(axis=1)
print("red cols with >200 px:", [i for i, v in enumerate(col_red) if v > 200])
print("red rows with >200 px:", [i for i, v in enumerate(row_red) if v > 200])

print("--- yellow blobs (class tags) ---")
ys, xs = np.where(yellow)
pts = sorted(set(zip(xs.tolist(), ys.tolist())))
if pts:
    # cluster by proximity
    clusters = []
    used = set()
    for p in pts:
        if p in used:
            continue
        stack = [p]
        comp = []
        used.add(p)
        while stack:
            cx, cy = stack.pop()
            comp.append((cx, cy))
            for dx in range(-3, 4):
                for dy in range(-3, 4):
                    q = (cx + dx, cy + dy)
                    if q in set(pts) and q not in used:
                        used.add(q)
                        stack.append(q)
        if len(comp) > 20:
            cx = [p[0] for p in comp]
            cy = [p[1] for p in comp]
            clusters.append((min(cx), max(cx), min(cy), max(cy), len(comp)))
    for c in sorted(clusters, key=lambda t: t[2]):
        print("  yellow blob x %d-%d y %d-%d n=%d" % c)

print("--- salmon (?) boxes ---")
ys, xs = np.where(salmon)
pts = set(zip(xs.tolist(), ys.tolist()))
used = set()
for p in sorted(pts):
    if p in used:
        continue
    stack = [p]
    used.add(p)
    comp = []
    while stack:
        cx, cy = stack.pop()
        comp.append((cx, cy))
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                q = (cx + dx, cy + dy)
                if q in pts and q not in used:
                    used.add(q)
                    stack.append(q)
    if len(comp) > 30:
        cx = [p[0] for p in comp]
        cy = [p[1] for p in comp]
        print("  salmon blob x %d-%d y %d-%d n=%d center (%.0f,%.0f)" %
              (min(cx), max(cx), min(cy), max(cy), len(comp),
               (min(cx) + max(cx)) / 2, (min(cy) + max(cy)) / 2))

print("--- colored point clusters (saturated fills) ---")
for name, mask in (("green pts", green & (g > 120) & (r < 120)),
                   ("blue pts", (b > 140) & (r < 120) & (g < 160)),
                   ("red pts", (r > 140) & (g < 110) & (b < 110))):
    ys, xs = np.where(mask)
    if len(xs):
        print(f"{name}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} n={len(xs)}")

print("--- hatch region fills ---")
for name, mask in (("pale green", paleg), ("lavender", lav), ("pink", pink)):
    ys, xs = np.where(mask)
    if len(xs):
        print(f"{name}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} n={len(xs)}")
        # sample a few pixel colors
        for (sx, sy) in [(xs.min() + 2, ys.min() + 2), (xs.max() - 2, ys.max() - 2)]:
            print("   sample", (sx, sy), a[sy, sx])

print("--- unique colors in left column x 60..160 ---")
reg = a[100:200, 60:160].reshape(-1, 3)
uniq, cnt = np.unique(reg, axis=0, return_counts=True)
order = np.argsort(-cnt)[:12]
for i in order:
    print("   ", tuple(uniq[i]), cnt[i])

print("--- unique colors bottom-right x 660..760, y 340..390 ---")
reg = a[340:390, 660:760].reshape(-1, 3)
uniq, cnt = np.unique(reg, axis=0, return_counts=True)
order = np.argsort(-cnt)[:12]
for i in order:
    print("   ", tuple(uniq[i]), cnt[i])

print("--- row/column profile of strong black (axes) ---")
blk = (r < 90) & (g < 90) & (b < 90)
for yy in range(100, 500):
    n = blk[yy, 150:760].sum()
    if n > 250:
        print("  dark row", yy, n)
for xx in range(150, 760):
    n = blk[100:500, xx].sum()
    if n > 250:
        print("  dark col", xx, n)

print("--- bottom black band ---")
dark_rows = [yy for yy in range(H) if blk[yy].mean() > 0.5]
print("rows >50% black:", dark_rows[:5], "...", dark_rows[-5:] if dark_rows else None)
