#!/usr/bin/env python3
"""w017 measurement dossier generator — slide 017 frame (960x540, 1px = 1pt).

Prints every geometry/colour number the build uses, straight from the frame.
Run: python3 qa/slide017/measure_017.py | tee qa/slide017/measure_017.txt
"""
from PIL import Image
import numpy as np

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VROOT = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
IMG = VROOT + "/unique_slides/slide_017.jpg"

im = Image.open(IMG).convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
lum = a.mean(axis=2)
red = (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50) & (a[:, :, 0] > 90)
blue = (a[:, :, 2] - a[:, :, 0] > 60) & (a[:, :, 2] - a[:, :, 1] > 50) & (a[:, :, 2] > 90)
dark = lum < 150
ink = dark | red | blue

print("frame", im.size, "(960x540, 1px = 1pt)")
print("md5-measured frame path:", IMG)


def vlines(x0, x1, y0, y1, frac=0.6, thr=226):
    band = lum[y0:y1, x0:x1]
    colsum = (band < thr).sum(axis=0)
    hits = [x0 + i for i, c in enumerate(colsum) if c > (y1 - y0) * frac]
    groups = []
    for x in hits:
        if groups and x - groups[-1][-1] <= 1:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [(g[0], g[-1]) for g in groups]


def hlines(x0, x1, y0, y1, frac=0.55, thr=226):
    band = lum[y0:y1, x0:x1]
    rowsum = (band < thr).sum(axis=1)
    hits = [y0 + i for i, c in enumerate(rowsum) if c > (x1 - x0) * frac]
    groups = []
    for y in hits:
        if groups and y - groups[-1][-1] <= 1:
            groups[-1].append(y)
        else:
            groups.append([y])
    return [(g[0], g[-1]) for g in groups]


def bb(mask, x0, y0, x1, y1):
    m = mask[y0:y1, x0:x1]
    yy, xx = np.where(m)
    if len(xx) == 0:
        return None
    return (x0 + xx.min(), x0 + xx.max(), y0 + yy.min(), y0 + yy.max(), len(xx))


def med(x0, y0, x1, y1):
    return tuple(np.median(a[y0:y1, x0:x1].reshape(-1, 3), axis=0).astype(int))


print("\n== CHROME ==")
print(" canvas @(100,50):", tuple(a[50, 100]), " panel @(70,300):", tuple(a[300, 70]))
print(" left stroke x58-59:", tuple(a[300, 58]), tuple(a[300, 59]),
      " right stroke x901:", tuple(a[300, 901]))
print(" top band red px (y45..55):", int(red[45:55, 60:900].sum()))
print(" badge fill @(870,60):", tuple(a[60, 870]), " numeral dark bbox:",
      bb(dark, 860, 55, 895, 92))

print("\n== TRAIN TABLES (x measured per band, y per band) ==")
for i, (y0, y1) in enumerate([(120, 255), (258, 395), (396, 532)], start=1):
    print(f" band{i} v:", vlines(70, 500, y0, y1))
    print(f" band{i} h:", hlines(70, 500, y0, y1))

print("\n== TEST TABLES (4 cols incl. a black label column) ==")
for i, (y0, y1) in enumerate([(120, 255), (258, 395), (396, 532)], start=1):
    print(f" band{i} v:", vlines(640, 900, y0, y1))
    print(f" band{i} h:", hlines(640, 900, y0, y1))
print(" test gridline colour @(719,200):", tuple(a[200, 719]),
      " @(770,340):", tuple(a[340, 770]))
print(" train gridline colour @(133,200):", tuple(a[200, 133]),
      " @(296,340):", tuple(a[340, 296]))
print(" test y-row fills B1:", [med(x0 + 4, 224, x1 - 4, 247)
                               for x0, x1 in [(669, 719), (720, 770), (771, 821), (822, 872)]])
print(" test y-row fills B2:", [med(x0 + 4, 362, x1 - 4, 385)
                               for x0, x1 in [(669, 719), (720, 770), (771, 821), (822, 872)]])
print(" test y-row fills B3:", [med(x0 + 4, 500, x1 - 4, 523)
                               for x0, x1 in [(669, 719), (720, 770), (771, 821), (822, 872)]])
print(" train cell fill:", med(95, 161, 131, 187), " yellow cell:", med(422, 299, 457, 326))

print("\n== LABELS ==")
print(" Train blue box:", bb(blue, 80, 92, 200, 132))
print(" Test  blue box:", bb(blue, 780, 96, 900, 132))

print("\n== TITLE runs ==")
print(" title ink bbox (y55..96):", bb(ink, 140, 55, 830, 96))
for name, x0, x1 in [("Adding", 170, 280), ("Ridge", 285, 372), ("Regularizer", 378, 542),
                     ("to", 548, 578), ("the", 584, 630), ("model", 638, 726),
                     ("lambda=3", 744, 810)]:
    b = bb(ink, x0, 55, x1, 100)
    print(f"  {name:11s} ink {b}  colour red_px={int(red[55:100, x0:x1].sum())}"
          f" blue_px={int(blue[55:100, x0:x1].sum())}")

print("\n== W BOXES (red border rect + interior items) ==")
for i, (y0, y1) in enumerate([(115, 260), (255, 400), (395, 535)], start=1):
    b = bb(red, 480, y0, 660, y1)
    print(f" band{i} red border bbox:", b)
    print("   interior W (red):", bb(red, 512, y0 + 12, 546, y0 + 60))
    print("   interior = (dark):", bb(dark, 540, y0 + 30, 560, y0 + 55))
    for j, (ya, yb) in enumerate([(y0 + 4, y0 + 55), (y0 + 35, y0 + 80), (y0 + 60, y0 + 105)], start=1):
        print(f"   value line{j}:", bb(dark, 564, ya, 602, yb))
    print("   norm line (blue):", bb(blue, 510, y1 - 40, 625, y1 - 3))

print("\n== ARROWS (blue, hollow) ==")
for i, (y0, y1) in enumerate([(170, 225), (300, 360), (435, 495)], start=1):
    for x0, x1, side in [(455, 510, "left"), (620, 675, "right")]:
        print(f" band{i} {side}:", bb(blue, x0, y0, x1, y1))
print(" arrow interior @(482,198):", tuple(a[198, 482]))

print("\n== INK COLOUR SAMPLES ==")


def inkcolor(x0, y0, x1, y1):
    r = a[y0:y1, x0:x1].reshape(-1, 3)
    idx = np.argsort(r.mean(axis=1))[:30]
    return tuple(np.median(r[idx], axis=0).astype(int))


print(" train header X1 ink:", inkcolor(135, 130, 172, 157))
print(" train label col X1 ink:", inkcolor(93, 160, 132, 188))
print(" train data odd col:", inkcolor(135, 160, 172, 188),
      " even col:", inkcolor(175, 160, 213, 188))
print(" test header Test1:", inkcolor(721, 132, 769, 158),
      " Test2:", inkcolor(772, 132, 820, 158))
print(" test data 30:", inkcolor(721, 163, 769, 188),
      " 40:", inkcolor(772, 163, 820, 188))
print(" test y cell ink:", inkcolor(721, 224, 769, 247))
print(" test row label X1:", inkcolor(670, 163, 718, 188))
print(" W glyph:", inkcolor(521, 163, 539, 176))
print(" vector digits:", inkcolor(566, 192, 600, 206))
print(" norm line:", inkcolor(524, 224, 606, 241))
print(" parens:", inkcolor(556, 160, 564, 200))
print("\nRESULT: measured")
