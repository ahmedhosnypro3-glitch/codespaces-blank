#!/usr/bin/env python3
"""Refined measurement: pink formula box rects, badge circle, graph inner plot areas."""
import numpy as np
from PIL import Image

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
a = np.asarray(Image.open(SRC).convert("RGB")).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
H, W = R.shape

# pink fill: light warm pink, distinct from white bg and gray bg
pink = (R > 225) & (R < 254) & (G > 205) & (G < 245) & (B > 195) & (B < 235) & (R - B > 20)
for label, (y0, y1) in [("TOP row of pink boxes", (50, 108)), ("BOTTOM row", (280, 345))]:
    sub = pink[y0:y1]
    colsum = sub.sum(axis=0)
    runs, start = [], None
    for i, v in enumerate(colsum):
        if v > 8 and start is None:
            start = i
        elif v <= 8 and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, W - 1))
    print(label, "pink col runs:", runs)

# pink row runs within each box column band
for label, (x0, x1) in [("TL", (113, 412)), ("TR", (550, 849)), ("BL", (94, 428)), ("BR", (584, 813))]:
    sub = pink[:, x0:x1 + 1]
    rowsum = sub.sum(axis=1)
    runs, start = [], None
    for i, v in enumerate(rowsum):
        if v > 8 and start is None:
            start = i
        elif v <= 8 and start is not None:
            runs.append((start, i - 1))
            start = None
    if start is not None:
        runs.append((start, H - 1))
    print(label, "pink row runs:", [r for r in runs if r[1] - r[0] > 3])

# badge: yellow circle pixels in region x>840, y<120
yellow = (R > 230) & (G > 230) & (B > 120) & (B < 200)
reg = yellow[0:130, 830:960]
ys, xs = np.nonzero(reg)
print("\nbadge yellow bbox x", 830 + xs.min(), "..", 830 + xs.max(),
      " y", ys.min(), "..", ys.max(), "n=", len(xs))
print("badge center approx:", (830 + xs.min() + 830 + xs.max()) / 2, (ys.min() + ys.max()) / 2,
      "size", 830 + xs.max() - 830 + xs.min(), ys.max() - ys.min())
# blue outline around badge
blueish = (B - R > 40) & (B - G > 40)
reg2 = blueish[0:130, 830:960]
ys2, xs2 = np.nonzero(reg2)
if len(xs2):
    print("badge blue bbox x", 830 + xs2.min(), "..", 830 + xs2.max(),
          " y", ys2.min(), "..", ys2.max(), "n=", len(xs2))

# black numeral 21 inside badge: dark pixels
dark = (R < 120) & (G < 120) & (B < 120)
reg3 = dark[40:110, 845:910]
ys3, xs3 = np.nonzero(reg3)
if len(xs3):
    print("badge numeral bbox x", 845 + xs3.min(), "..", 845 + xs3.max(),
          " y", 40 + ys3.min(), "..", 40 + ys3.max(), "n=", len(xs3))

# graph frame interior: find the blue frame rect precisely per graph
blueish = (B - R > 40) & (B - G > 40)
for name, (x0, x1, y0, y1) in [("TL", (100, 420, 100, 280)), ("TR", (545, 860, 100, 280)),
                                ("BL", (100, 420, 340, 515)), ("BR", (545, 860, 340, 515))]:
    sub = blueish[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if len(xs):
        print(f"{name} blue frame ink bbox x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")

# black bar extent
dark = (R < 60) & (G < 60) & (B < 60)
for y in [517, 518, 519, 530, 539]:
    xs = np.nonzero(dark[y])[0]
    if len(xs):
        print(f"black bar row {y}: x {xs.min()}..{xs.max()} n={len(xs)}")
