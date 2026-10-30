#!/usr/bin/env python3
"""Targeted pixel probes of the original slide 008 frame."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_008.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W = a.shape[:2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(mask, label):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(label, "EMPTY")
        return
    print(f"{label}: x {xs.min()}-{xs.max()} y {ys.min()}-{ys.max()} n={len(xs)}")


def hist(x0, x1, y0, y1, label, top=10):
    reg = a[y0:y1, x0:x1].reshape(-1, 3)
    u, c = np.unique(reg, axis=0, return_counts=True)
    o = np.argsort(-c)[:top]
    print(label, [(tuple(u[i]), int(c[i])) for i in o])


# --- title ---
tred = (r > 150) & (r < 235) & (g < 90) & (b < 90)
tblue = (b > 170) & (r < 110) & (g < 130)
bbox(tred[:60, 200:760], "title red (x200-760,y<60)")
bbox(tred[55:120, 200:760], "title red (y55-120)")
bbox(tblue[50:120, 200:760], "title blue (y50-120)")
bbox(tblue[:60, 200:760], "title blue (y<60)")
# per-row counts of title ink
for yy in range(40, 125):
    n = tred[yy, 200:760].sum() + tblue[yy, 200:760].sum()
    if n > 3:
        print("  title ink row", yy, n)

# --- badge ---
hist(840, 910, 45, 100, "badge hist")
bbox((g > 200) & (b > 200) & (r > 200), "unused")

# --- Undefined callout ---
hist(60, 170, 115, 175, "undefined region hist")
bbox((b > 150) & (r < 130) & (g < 140), "blue in undefined region")

# --- New Class ---
hist(655, 780, 335, 395, "new class region hist")
bbox((r > 170) & (b > 170) & (g < 140), "magenta in new class region")

# --- salmon ? boxes ---
salmon = (r >= 246) & (g >= 208) & (g <= 240) & (b >= 190) & (b <= 222) & ((r - b) >= 24)
salmon[:110] = False
salmon[500:] = False
pts = set(zip(*np.where(salmon)))
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
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                q = (cx + dx, cy + dy)
                if q in pts and q not in used:
                    used.add(q)
                    stack.append(q)
    if len(comp) > 150:
        cx = [q[0] for q in comp]
        cy = [q[1] for q in comp]
        print("salmon box x %d-%d y %d-%d n=%d center (%.0f,%.0f)" %
              (min(cx), max(cx), min(cy), max(cy), len(comp), (min(cx) + max(cx)) / 2, (min(cy) + max(cy)) / 2))

# --- axes probes ---
print("vertical axis column samples:")
for xx in (290, 291, 292, 293, 294, 295, 296):
    col = a[120:480, xx]
    dark = [(yy + 120, tuple(col[yy])) for yy in range(360) if col[yy].sum() < 560]
    if dark:
        print("  x", xx, dark[:6], "...", len(dark))
print("horizontal axis row samples:")
for yy in (410, 411, 412, 413, 414, 415, 416):
    row = a[yy, 150:760]
    dark = [(xx + 150, tuple(row[xx])) for xx in range(610) if row[xx].sum() < 560]
    if dark:
        print("  y", yy, dark[:6], "...", len(dark))

# --- panel border lines (red) ---
red = (r > 150) & (g < 110) & (b < 110)
red[:35] = False
red[525:] = False
colc = red.sum(axis=0)
print("red columns count>250:", [(i, int(colc[i])) for i in np.where(colc > 250)[0]])
rowc = red.sum(axis=1)
print("red rows count>250:", [(i, int(rowc[i])) for i in np.where(rowc > 250)[0]])
print("red rows count>100:", [(i, int(rowc[i])) for i in np.where(rowc > 100)[0]])

# --- hatch region interior samples ---
for (sx, sy, lab) in [(300, 140, "upper-left"), (600, 150, "upper-right"), (700, 300, "right"),
                      (300, 330, "lower-left"), (450, 450, "bottom-center"), (215, 250, "left wedge"),
                      (400, 250, "center"), (200, 470, "bottom-left edge"), (500, 470, "bottom edge")]:
    print("  sample", lab, (sx, sy), tuple(a[sy, sx]))

# --- green/blue/red saturated clusters inside panel ---
green = (g > 110) & (r < 140) & (b < 140) & ((g - r) > 40)
blue = (b > 140) & (r < 140) & ((b - r) > 50) & ((b - g) > 20)
redp = (r > 140) & (g < 110) & (b < 110)
for name, m in (("green", green), ("blue", blue), ("red", redp)):
    m2 = m.copy()
    m2[:120] = False
    m2[500:] = False
    ys, xs = np.where(m2)
    print(name, "ink x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "n", len(xs))
