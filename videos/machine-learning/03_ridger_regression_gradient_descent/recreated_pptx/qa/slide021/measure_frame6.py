#!/usr/bin/env python3
"""measure_frame6.py — per-element y-bands + hairline colors + missing unknowns."""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
yellow = (r > 170) & (g > 170) & (b < 150)
dark = (r < 110) & (g < 110) & (b < 110)
ink_lt = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

def yband(name, mask, x0, x1, y0, y1):
    m = mask[y0:y1 + 1, x0:x1 + 1]
    rr = runs(m.any(axis=1))
    if rr:
        ys, xs = np.where(m)
        pts = a[ys + y0, xs + x0]
        if name.startswith("red") or name.startswith("chain-red") or "label" in name:
            srt = pts[pts.sum(axis=1).argsort()][:6]
        else:
            srt = pts[pts.sum(axis=1).argsort()][:6]
        med = np.median(srt, axis=0).astype(int)
        print(f" {name}: y runs {[(s+y0, e+y0) for s, e in rr]}  x {xs.min()+x0}..{xs.max()+x0}  darkest-core {tuple(med)}")
    else:
        print(f" {name}: EMPTY")

print("=== TOP TABLE hairlines: low-threshold col runs at specific columns ===")
for x in (98, 166, 234, 302, 97, 99, 165, 167, 233, 235, 301, 303):
    m = ink_lt[168:232, x]
    rr = runs(m)
    if rr:
        pts = []
        for (s, e) in rr:
            for y in range(s, e + 1):
                pts.append(tuple(a[168 + y, x]))
        print(f" x={x}: row runs {[(s+168, e+168) for s, e in rr]}, px colors {pts[:6]}...{pts[-3:] if len(pts)>6 else ''}")
print(" horizontal low-threshold runs (len>=180) in top table y168..232:")
for y in range(168, 233):
    rr = runs(ink_lt[y, 90:310])
    longr = [(s + 90, e + 90) for s, e in rr if e - s >= 170]
    if longr:
        pts = [tuple(a[y, x]) for (s0, e0) in longr for x in range(s0, e0 + 1, 40)]
        print(f"  y={y}: {longr} colors {pts}")

print("\n=== MIDDLE TABLE: gridlines + yellow cells + digit bands ===")
print(" horizontal low-threshold runs (len>=150) y330..400 x88..320:")
for y in range(330, 401):
    rr = runs(ink_lt[y, 88:320])
    longr = [(s + 88, e + 88) for s, e in rr if e - s >= 150]
    if longr:
        pts = [tuple(a[y, x]) for (s0, e0) in longr for x in range(s0, e0 + 1, 30)]
        print(f"  y={y}: {longr} colors {pts}")
print(" vertical low-threshold runs (len>=25) in middle table:")
for x in range(88, 320):
    rr = runs(ink_lt[330:400, x])
    longr = [(s + 330, e + 330) for s, e in rr if e - s >= 25]
    if longr:
        pts = [tuple(a[y2, x]) for (s0, e0) in longr for y2 in range(s0, e0 + 1, 6)]
        print(f"  x={x}: {longr} colors {pts}")
print(" yellow row runs in middle table zone:")
for y in range(330, 401):
    rr = runs(yellow[y, 88:320])
    if rr:
        print(f"  y={y}: {[(s+88, e+88) for s, e in rr]}")
print(" dark digit bands in middle table (y330..400, x88..320):")
dig = dark[330:401, 88:320]
for (y0, y1) in runs(dig.any(axis=1)):
    xs3 = np.where(dig[y0:y1 + 1].any(axis=0))[0]
    ccl = []; s = xs3[0]; p = xs3[0]
    for x in xs3[1:]:
        if x - p > 8: ccl.append((s + 88, p + 88)); s = x
        p = x
    ccl.append((s + 88, p + 88))
    print(f"  y {y0+330}..{y1+330}: x clusters {ccl}")

print("\n=== BOTTOM TABLE digit bands ===")
dig = dark[440:520, 400:660]
for (y0, y1) in runs(dig.any(axis=1)):
    xs3 = np.where(dig[y0:y1 + 1].any(axis=0))[0]
    ccl = []; s = xs3[0]; p = xs3[0]
    for x in xs3[1:]:
        if x - p > 8: ccl.append((s + 400, p + 400)); s = x
        p = x
    ccl.append((s + 400, p + 400))
    print(f"  y {y0+440}..{y1+440}: x clusters {ccl}")
print(" bottom table hairlines: vertical low-threshold runs (len>=20):")
for x in range(400, 660):
    rr = runs(ink_lt[450:515, x])
    longr = [(s + 450, e + 450) for s, e in rr if e - s >= 20]
    if longr:
        pts = [tuple(a[y2, x]) for (s0, e0) in longr for y2 in range(s0, e0 + 1, 5)]
        print(f"  x={x}: {longr} colors {pts}")

print("\n=== PER-ELEMENT Y BANDS ===")
# top chain elements
yband("top-chain red X^TX (x330..400)", red, 330, 400, 175, 220)
yband("top-chain dark =0 (x400..440)", dark, 400, 440, 175, 220)
yband("top-chain arrow1 BLUE (x455..485)", blue, 455, 485, 175, 220)
yband("top-chain 'Singular Matrix' (x490..630)", dark, 490, 630, 175, 220)
yband("top-chain arrow2 BLUE (x655..685)", blue, 655, 685, 175, 220)
yband("top-chain 'No Inverse' RED (x700..800)", red, 700, 800, 175, 220)
# middle chain
yband("mid-chain red X^TX (x330..395)", red, 330, 395, 340, 390)
yband("mid-chain dark =5685 (x395..465)", dark, 395, 465, 340, 390)
yband("mid-chain arrow1 BLUE (x485..510)", blue, 485, 510, 340, 390)
yband("mid-chain 'Non-Singular Matrix' (x515..695)", dark, 515, 695, 340, 390)
yband("mid-chain arrow2 BLUE (x720..750)", blue, 720, 750, 340, 390)
yband("mid-chain 'Inverse Exists' RED (x755..880)", red, 755, 880, 340, 390)
# labels
yband("top label red X^TX (x90..145)", red, 90, 145, 128, 165)
yband("mid label (X^TX part x85..165)", red, 85, 165, 292, 330)
yband("mid label blue lambda-I (x165..210)", blue, 165, 210, 292, 330)
yband("mid label green lambda=3 (x240..295)", green, 240, 295, 292, 330)
yband("mid label dark paren (x85..95)", dark, 85, 95, 292, 330)
# bottom expression
yband("bot expr red X^TX (x150..210)", red, 150, 210, 455, 505)
yband("bot expr blue lambda-I (x235..295)", blue, 235, 295, 455, 505)
yband("bot expr dark paren/-1 (x150..320)", dark, 150, 320, 455, 505)
# green exact
ys, xs = np.where(green)
print(f" green bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}")

print("\n=== BOTTOM EXPRESSION beyond x288 (superscript -1?) ===")
m = ink_lt[455:510, 285:340]
for (y0, y1) in runs(m.any(axis=1)):
    xs3 = np.where(m[y0:y1 + 1].any(axis=0))[0]
    print(f"  y {y0+455}..{y1+455}: x {xs3.min()+285}..{xs3.max()+285}")
    for x0x in range(285, 340):
        col = m[y0:y1 + 1, x0x - 285]
        if col.sum():
            pts2 = [tuple(a[455 + y2, x0x]) for y2 in np.where(col)[0][:4]]
            print(f"     x={x0x}: y {[455+t for t in np.where(col)[0]]} {pts2}")

print("\n=== BOTTOM ARROW: blue + dark runs per row (x280..470, y455..510) ===")
for y in range(455, 511):
    rb = runs(blue[y, 280:470])
    rd = runs(dark[y, 280:470])
    if rb or rd:
        print(f"  y={y}: blue {[(s+280, e+280) for s, e in rb]}  dark {[(s+280, e+280) for s, e in rd]}")

print("\n=== TOP/MID ARROW blue-mask bboxes ===")
for name, (x0, x1, y0, y1) in {
    "top arrow1": (450, 490, 175, 220), "top arrow2": (650, 690, 175, 220),
    "mid arrow1": (480, 512, 340, 390), "mid arrow2": (715, 755, 340, 390)}.items():
    m = blue[y0:y1, x0:x1]
    if m.any():
        ys, xs = np.where(m)
        print(f" {name}: x {xs.min()+x0}..{xs.max()+x0} y {ys.min()+y0}..{ys.max()+y0}")
        # row-by-row x extent (shape of the arrow)
        for yy in range(ys.min(), ys.max() + 1):
            rr = runs(m[yy])
            if rr:
                print(f"    y={yy+y0}: {[(s+x0, e+x0) for s, e in rr]}")
