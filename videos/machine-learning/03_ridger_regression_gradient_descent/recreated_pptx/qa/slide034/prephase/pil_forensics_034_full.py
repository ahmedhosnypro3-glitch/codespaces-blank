#!/usr/bin/env python3
"""S20c prephase PIL re-verification of the fresh desc_full.txt (034 full-frame
desc leg, banked 20:07). Settles the transcript claims that conflict with the
banked forensics: frame/chrome, eq+param box borders, param/slope/next-x fills,
cyan-insert extent, title runs, explanatory line-2 ink, dark-rule inventory,
axis positions, green dot shape."""
import numpy as np
from PIL import Image

F = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_034.jpg"
im = np.asarray(Image.open(F).convert("RGB")).astype(int)

def px(x, y):
    return tuple(im[y, x])

def census(x0, x1, y0, y1, pred, label):
    n, first = 0, None
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = im[y, x]
            if pred(r, g, b):
                n += 1
                if first is None:
                    first = (x, y, (r, g, b))
    print(f"  {label}: n={n} first={first}")
    return n, first

red = lambda r, g, b: r > 110 and g < 90 and b < 90
blue = lambda r, g, b: b > 110 and b > r + 40 and b > g + 40
green = lambda r, g, b: g > 110 and g > r + 30 and g > b + 30

print("== 1. gray panel + top band (transcript: '#D9D9D9 rect (55,38)-(905,540) red border ALL sides') ==")
print(f"  panel sample (400,50)={px(400,50)} (400,300)={px(400,300)} (30,300)={px(30,300)} (400,20)={px(400,20)}")
for y in (40, 44, 46, 48):
    row = im[y, 55:905]
    n = sum(1 for p in row if red(*p))
    print(f"  red px in top band y={y}: {n}")

print("== 2. eq box border color (transcript: blue #2E4FD8) ==")
for pt in ((500, 169), (500, 218), (465, 190), (600, 190), (466, 170), (599, 217)):
    print(f"  {pt}={px(*pt)}")
n, _ = census(465, 601, 169, 219, blue, "blue px in eq-box border band")
census(465, 601, 169, 219, red, "red px in eq-box border band")

print("== 3. param box border color (transcript: green #00A000) ==")
for pt in ((75, 275), (176, 275), (100, 246), (100, 309), (125, 247)):
    print(f"  {pt}={px(*pt)}")
census(75, 177, 246, 310, blue, "blue px in param-box frame band")

print("== 4. param box row fills label vs value cell (transcript: r1 green/pink, r2 pink/pink, r3 yellow/yellow) ==")
for y in (255, 260, 272, 276, 290, 294):
    print(f"  y={y}: label(x100)={px(100, y)} value(x150)={px(150, y)}")

print("== 5. table band fills (transcript: header CCCC66, f(x) DDDD99, x-delta C9A0E8, fx-delta D9C2F0, x+delta FFCC99, f(x+delta) FFDDAA) ==")
for y, name in ((345, "header"), (362, "f(x)"), (383, "x-delta"), (403, "f(x-delta)"), (425, "x+delta"), (445, "f(x+delta)")):
    print(f"  {name} y={y}: x100={px(100, y)} x300={px(300, y)} x600={px(600, y)}")

print("== 6. slope row (transcript: data cells RED #CC4444, dark-red cell borders) ==")
for y in (462, 466, 468, 472):
    print(f"  y={y}: x100={px(100, y)} x300={px(300, y)} x600={px(600, y)}")
census(140, 880, 458, 480, red, "red px in slope row y458..479")

print("== 7. next-x row (transcript: salmon #FF9999, red cell outlines) ==")
for y in (485, 490, 495):
    print(f"  y={y}: x100={px(100, y)} x300={px(300, y)} x600={px(600, y)}")

print("== 8. cyan insert x-extent (transcript: rect (628,333)-(750,371); banked: x666..790) ==")
for y in (340, 345, 350, 360, 368):
    row = []
    for x in range(620, 800):
        r, g, b = im[y, x]
        if green(r, g, b):
            row.append(x)
    if row:
        print(f"  y={y}: green cols x{row[0]}..{row[-1]} n={len(row)}")
    else:
        print(f"  y={y}: no green cols in x620..800")
print(f"  y=390 (band2): x100={px(100, 390)} x680={px(680, 390)} x730={px(730, 390)}")
census(620, 800, 333, 372, lambda r, g, b: g > 110 and g > r + 20 and g > b + 20, "greenish px y333..371 x620..800")

print("== 9. title ink census (transcript: ONE run #B22222; banked row 2: two runs 8B0000/C00000) ==")
hist = {}
for y in range(67, 85):
    for x in range(195, 435):
        r, g, b = im[y, x]
        if r > 90 and g < 90 and b < 90:
            key = (r // 32, g // 32, b // 32)
            hist[key] = hist.get(key, 0) + 1
for k in sorted(hist, key=hist.get, reverse=True):
    print(f"  bucket(r//32,g//32,b//32)={k} n={hist[k]} -> family r~{k[0]*32},g~{k[1]*32},b~{k[2]*32}")

print("== 10. explanatory box line 2 ink (transcript: all black; leftblock audit: math tokens blue) ==")
census(265, 600, 280, 302, blue, "blue px line2 y280..301 x265..599")
census(265, 600, 256, 278, blue, "blue px line1 y256..277 x265..599")
census(265, 600, 256, 302, red, "red px box y256..301 (line-1 tokens)")

print("== 11. table frame (transcript: blue #2222CC box (66,320)-(874,522)) ==")
for pt in ((68, 400), (881, 400), (400, 320), (400, 321), (400, 517), (70, 400), (870, 330)):
    print(f"  {pt}={px(*pt)}")
census(60, 890, 318, 522, blue, "blue px table frame band")

print("== 12. full-width dark rules scan y315..520 (transcript: ONLY y354..356 + top edge; banked row 15: y459,477/478,483/484,502,517) ==")
for y in range(315, 521):
    n = sum(1 for x in range(80, 871) if max(im[y, x]) < 150)
    if n > 500:
        print(f"  y={y}: dark px over x80..870 = {n}")

print("== 13. plot axes (transcript: x-axis y165, y-axis x718; plot audit: cross (721.5,171.5)) ==")
for y in range(155, 185):
    n = sum(1 for x in range(615, 840) if max(im[y, x]) < 120)
    if n > 100:
        print(f"  dark row y={y}: n={n}")
for x in range(705, 735):
    n = sum(1 for y in range(66, 305) if max(im[y, x]) < 120)
    if n > 100:
        print(f"  dark col x={x}: n={n}")

print("== 14. green dot shape (transcript: circle r6 @(800,258); plot audit: ellipse x799..816 y255..265) ==")
xs, ys = [], []
for y in range(245, 275):
    for x in range(790, 830):
        r, g, b = im[y, x]
        if green(r, g, b):
            xs.append(x)
            ys.append(y)
if xs:
    print(f"  green bbox x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(xs)}")

print("== 15. pink label box (transcript: fill #FFC0CB border #C000C0 (743,268)-(842,307)) ==")
for pt in ((750, 271), (795, 269), (838, 270), (745, 285), (750, 300), (795, 305)):
    print(f"  {pt}={px(*pt)}")

print("== 16. red dashed guide x-extent (transcript: x784 y153..164) ==")
for x in range(775, 795):
    n = sum(1 for y in range(148, 175) if red(*im[y, x]))
    if n >= 3:
        print(f"  red col x={x}: n={n} (y148..174)")

print("== 17. subtitle runs (transcript L1 #B22222; L2 blue/red/blue) ==")
hist = {}
for y in range(94, 114):
    for x in range(113, 534):
        r, g, b = im[y, x]
        if r > 90 and g < 90 and b < 90:
            hist[(r // 32)] = hist.get((r // 32), 0) + 1
print(f"  L1 red-ink r-buckets: {hist}")
for x0, x1, name in ((185, 305, "run1"), (305, 345, "run2"), (345, 465, "run3")):
    nb = sum(1 for y in range(118, 140) for x in range(x0, x1) if blue(*im[y, x]))
    nr = sum(1 for y in range(118, 140) for x in range(x0, x1) if red(*im[y, x]))
    print(f"  L2 {name} x{x0}..{x1}: blue n={nb} red n={nr}")
