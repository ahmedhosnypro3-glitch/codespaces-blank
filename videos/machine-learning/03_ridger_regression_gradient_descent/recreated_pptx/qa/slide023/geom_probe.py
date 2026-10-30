#!/usr/bin/env python3
"""Consolidated geometry probe: badge circle+numeral, box bboxes/borders, text
baselines, and Arial size hypotheses. 960x540, 1px=1pt."""
import numpy as np
from PIL import Image, ImageDraw, ImageFont

IM = '/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_023.jpg'
a = np.array(Image.open(IM)).astype(int)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]


def bbox(m, y0, y1, x0, x1):
    s = m[y0:y1 + 1, x0:x1 + 1]
    if not s.any(): return None
    ys, xs = np.where(s)
    return (int(xs.min() + x0), int(ys.min() + y0), int(xs.max() + x0), int(ys.max() + y0))


print("== BADGE (yellow FDFD96 fill) ==")
# yellow: R&B high, G slightly lower
yel = (R > 235) & (B > 200) & (G > 195) & (G < 245) & (R - G > 3)
print(" yellow bbox:", bbox(yel, 40, 110, 820, 940))
ys, xs = np.where(yel[40:111, 820:941])
print(" yellow w=%d h=%d" % (xs.max() - xs.min() + 1, ys.max() - ys.min() + 1))
# dark ink inside the circle (numeral 333333)
dk = (R < 150) & (G < 150) & (B < 150)
sub = dk[55:95, 858:895]
ys2, xs2 = np.where(sub)
if len(xs2):
    print(" numeral ink bbox x%d..%d y%d..%d w=%d h=%d" % (xs2.min() + 858, xs2.max() + 858,
          ys2.min() + 55, ys2.max() + 55, xs2.max() - xs2.min() + 1, ys2.max() - ys2.min() + 1))
# per-glyph
cc = sub.any(axis=0); xx = np.where(cc)[0]
r = []; s = xx[0]; p = xx[0]
for x in xx[1:]:
    if x > p + 1: r.append((s, p)); s = x
    p = x
r.append((s, p))
for (s, e) in r:
    g = sub[:, s:e + 1]; yy = np.where(g.any(axis=1))[0]
    print("   glyph x%d..%d w%d y%d..%d h%d n=%d" % (s + 858, e + 858, e - s + 1,
          yy.min() + 55, yy.max() + 55, yy.max() - yy.min() + 1, int(g.sum())))
for sz in [16, 17, 18, 19, 20]:
    f = ImageFont.truetype('/usr/share/fonts/TTF/Arialbd.TTF', sz * 8)
    img = Image.new('L', (300, 80), 0); d = ImageDraw.Draw(img); d.text((10, 10), '23', font=f, fill=255)
    m = np.array(img) > 128
    yy, xxv = np.where(m)
    print(f"   Arialbd {sz}pt '23': ink w={xxv.max()-xxv.min()+1} h={yy.max()-yy.min()+1}")

print()
print("== RED TITLE clean glyph metrics ==")
red = (R > 120) & (R - G > 60) & (R - B > 60)
for label, x0, x1 in [("I", 218, 226), ("H", 355, 378), ("D", 424, 446), ("M", 573, 600), ("t", 622, 634)]:
    s = red[70:110, x0:x1 + 1]
    ys, xs = np.where(s)
    if len(ys):
        print(f"  {label}: x{x0+xs.min()}..{x0+xs.max()} y{70+ys.min()}..{70+ys.max()} w={xs.max()-xs.min()+1} h={ys.max()-ys.min()+1}")

print()
print("== BOXES (fill-class extents) ==")
greenfill = (G > R + 6) & (G > B + 10) & (G > 200) & (R > 180) & (G < 250)
print(" green fill bbox:", bbox(greenfill, 100, 235, 60, 900))
yelfill = (R > 245) & (G > 245) & (B > 210) & (B < 245)
print(" yellow fill bbox:", bbox(yelfill, 430, 540, 60, 900))
bluefill = (B > R + 5) & (B > 250) & (R > 245) & (G > 248)
print(" blue-ish fill bbox:", bbox(bluefill, 225, 430, 60, 900))

print()
print("== text baselines (per line, using a robust ink mask) ==")
panel = (np.abs(a - np.array([233, 233, 231])).sum(axis=2) > 150)
for name, y0, y1, x0, x1 in [("title", 74, 110, 200, 700), ("recall", 112, 146, 95, 400),
                             ("dimnote", 191, 219, 95, 780), ("blueL1", 238, 270, 90, 870),
                             ("blueL2", 272, 304, 90, 870), ("blueL3", 306, 338, 90, 870),
                             ("exL1", 360, 392, 90, 870), ("exL2", 396, 426, 90, 870),
                             ("solL1", 470, 500, 240, 730), ("solL2", 500, 528, 300, 670)]:
    s = panel[y0:y1 + 1, x0:x1 + 1]
    rows = np.where(s.sum(axis=1) > 1)[0]
    if len(rows):
        print(f"  {name:8s} first_ink_y={rows[0]+y0} last_ink_y={rows[-1]+y0} rows={len(rows)}")

print()
print("== box border strokes (row/col profiles) ==")
for name, m in [("green_border", (G > R + 40) & (G > B + 40) & (G > 90) & (G < 190)),
                ("violet_border", (B - R > 20) & (B > 180) & (R > 160) & (R < 220)),
                ("brown_border", (R - G > 20) & (R - B > 40) & (R < 200) & (R > 60))]:
    rows = np.where(m.sum(axis=1) > 200)[0]
    cols = np.where(m.sum(axis=0) > 100)[0]
    print(f"  {name}: rows={rows[:6]}{'...' if len(rows)>6 else ''} n={len(rows)}  cols={cols[:6]}...{cols[-4:] if len(cols)>8 else ''}")
