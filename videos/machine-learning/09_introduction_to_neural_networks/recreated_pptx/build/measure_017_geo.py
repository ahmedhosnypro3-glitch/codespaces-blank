#!/usr/bin/env python3
"""Detailed geometry extraction for slide 017 original at 960x540.

Fills in every region the judge cares about:
  - blue graph panel borders (3 panels)
  - peach/pink equation boxes (2 bottom) + red outlines
  - top-right label box (pale rounded rect)
  - title text (dark red)
  - graph interior ink: axes, red function lines, labels
"""
import sys
import numpy as np
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "unique_slides/slide_017.jpg"
a = np.array(Image.open(SRC).convert("RGB")).astype(int)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

BG = np.array([232, 232, 232])
PEACH = np.array([251, 234, 216])
WHITE = np.array([255, 255, 255])


def near(px, ref, tol):
    return np.abs(px - ref).sum(axis=2) <= tol


print(f"=== {SRC} {W}x{H} ===\n")

# ---------- blue panel borders ----------
blue = (B > 130) & (B - R > 45) & (B - G > 30)
ys, xs = np.where(blue)
print("BLUE border pixels:", len(ys))
# cluster blue pixels into 3 panels by finding rows/cols with high density
rowc = blue.sum(axis=1)
colc = blue.sum(axis=0)
print("  blue row profile (rows with >30 blue px):",
      [(int(y), int(rowc[y])) for y in np.where(rowc > 30)[0]])
print("  blue col profile (cols with >20 blue px):",
      [(int(x), int(colc[x])) for x in np.where(colc > 20)[0]][:60])

# panels: find x-runs of vertical border lines
vruns = []
s = None
for x in range(W):
    if colc[x] > 20:
        if s is None:
            s = x
    else:
        if s is not None:
            vruns.append((s, x - 1))
            s = None
if s is not None:
    vruns.append((s, W - 1))
print("  vertical blue lines (x runs):", vruns)

# ---------- peach fill (equation boxes) ----------
peach = near(a, PEACH, 40)
ys, xs = np.where(peach)
print("\nPEACH fill pixels:", len(ys), "rows", ys.min(), ys.max(), "cols", xs.min(), xs.max())
for label, (y0, y1) in [("bottom band", (440, 530)), ("all", (0, 540))]:
    m = peach[y0:y1 + 1]
    if m.sum() == 0:
        continue
    cc = m.sum(axis=0)
    runs = []
    s = None
    for x in range(W):
        if cc[x] > 5:
            if s is None:
                s = x
        else:
            if s is not None:
                runs.append((s, x - 1))
                s = None
    if s is not None:
        runs.append((s, W - 1))
    print(f"  {label} y{y0}-{y1} peach col runs:",
          [(int(u), int(v), int(v - u + 1)) for u, v in runs if v - u > 15])

# row runs of peach in the bottom band
band = peach[440:530]
rc = band.sum(axis=1)
runs = []
s = None
for i, v in enumerate(rc):
    if v > 5:
        if s is None:
            s = i
    else:
        if s is not None:
            runs.append((s + 440, i - 1 + 440))
            s = None
if s is not None:
    runs.append((s + 440, 529))
print("  peach row runs y440-530:", runs)

# ---------- top-right label box: find its pale fill ----------
print("\n--- top-right region x580-830 y80-300 ---")
reg = a[80:300, 580:830]
from collections import Counter
c = Counter(map(tuple, reg.reshape(-1, 3)))
for col, n in c.most_common(6):
    print("   ", col, n)

# ---------- title (dark red) ----------
darkred = (R > 100) & (R < 210) & (G < 80) & (B < 80)
ys, xs = np.where(darkred)
if len(ys):
    print(f"\nDARK RED (title) rows {ys.min()}-{ys.max()} cols {xs.min()}-{xs.max()} px={len(ys)}")

# ---------- black ink inside each graph panel ----------
print("\n--- black ink per region (axes + labels) ---")
regions = {
    "top_graph": (309, 120, 595, 268),
    "bl_graph": (137, 289, 422, 437),
    "br_graph": (487, 289, 773, 437),
    "label_box": (580, 80, 830, 300),
}
black = (R < 80) & (G < 80) & (B < 80)
redink = (R > 120) & (G < 90) & (B < 90) & (R - G > 70)
for name, (x0, y0, x1, y1) in regions.items():
    for cname, cm in (("black", black), ("red", redink)):
        m = cm[y0:y1 + 1, x0:x1 + 1]
        if m.sum() == 0:
            print(f"  {name:11s} {cname:5s}: none")
            continue
        yy, xx = np.where(m)
        print(f"  {name:11s} {cname:5s}: rows {yy.min()+y0}-{yy.max()+y0} "
              f"cols {xx.min()+x0}-{xx.max()+x0} px={m.sum()}")

# red function line endpoints in each graph (column extremes of red)
print("\n--- red function-line extent per graph ---")
for name, (x0, y0, x1, y1) in [("top_graph", (309, 120, 595, 268)),
                               ("bl_graph", (137, 289, 422, 437)),
                               ("br_graph", (487, 289, 773, 437))]:
    m = redink[y0:y1 + 1, x0:x1 + 1]
    yy, xx = np.where(m)
    if len(yy) == 0:
        print(f"  {name}: no red")
        continue
    print(f"  {name}: rows {yy.min()+y0}-{yy.max()+y0} cols {xx.min()+x0}-{xx.max()+x0}")
    # leftmost and rightmost red columns -> y positions
    for label, sel in (("left", xx == xx.min()), ("right", xx == xx.max())):
        print(f"     {label}: x={xx.min()+x0 if label=='left' else xx.max()+x0} "
              f"y {yy[sel].min()+y0}-{yy[sel].max()+y0}")
