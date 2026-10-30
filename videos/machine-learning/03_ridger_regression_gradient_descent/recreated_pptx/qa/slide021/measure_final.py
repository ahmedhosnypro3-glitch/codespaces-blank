#!/usr/bin/env python3
"""measure_final.py — consolidated geometry/color probe for slide 021 build.

Banked under qa/slide021/ (predecessor evidence measure_frame*.py is preserved).
Frame px, 1px = 1pt = 1/72in. Output feeds build/slide_021.js.
"""
from PIL import Image
import numpy as np

F = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_021.jpg"
im = Image.open(F).convert("RGB")
a = np.asarray(im).astype(int)
r, g, b = a[..., 0], a[..., 1], a[..., 2]

blue = (b > 120) & (b - r > 60) & (b - g > 60)
red = (r > 100) & (r - g > 60) & (r - b > 60)
green = (g > 100) & (g - r > 50) & (g - b > 50)
yellow = (r > 170) & (g > 170) & (b < 150)
dark = (r < 110) & (g < 110) & (b < 110)
ink = (r < 215) | (g < 215) | (b < 215)

def runs(vec):
    out = []; s = None
    for i, v in enumerate(vec):
        if v and s is None: s = i
        elif not v and s is not None: out.append((s, i - 1)); s = None
    if s is not None: out.append((s, len(vec) - 1))
    return out

def bbox(m, x0, y0, x1, y1):
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if not len(ys): return None
    return (xs.min() + x0, ys.min() + y0, xs.max() + x0, ys.max() + y0)

def core(m, x0, y0, x1, y1, n=8):
    sub = m[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.where(sub)
    if not len(ys): return None
    pts = a[ys + y0, xs + x0]
    srt = pts[np.argsort(pts.sum(axis=1))][:n]
    return tuple(np.median(srt, axis=0).astype(int))

def cls(x, y):
    if dark[y, x]: return '#'
    if blue[y, x]: return 'B'
    if red[y, x]: return 'R'
    if green[y, x]: return 'G'
    if yellow[y, x]: return 'Y'
    if ink[y, x]: return '+'
    return '.'

def ascii_map(x0, x1, y0, y1, label):
    print(f" -- {label} (x{x0}..{x1}, y{y0}..{y1})")
    for y in range(y0, y1 + 1):
        print(f"   {y:3d} " + ''.join(cls(x, y) for x in range(x0, x1 + 1)))

print("### 1. TITLE")
t = red.copy(); t[:, :250] = False; t[:, 730:] = False; t[:60] = False; t[120:] = False
ys, xs = np.where(t)
print(f" title red ink bbox: x {xs.min()}..{xs.max()} y {ys.min()}..{ys.max()}  (w {xs.max()-xs.min()+1}, h {ys.max()-ys.min()+1})")
cc = []
for y in range(ys.min(), ys.max() + 1):
    rr = runs(t[y])
    cc.append((y, rr))
print(" title row runs (x-clusters, gap>12):")
prev = None
for y, rr in cc:
    cl = []
    for s, e in rr:
        if e - s < 3: continue
        if cl and s - cl[-1][1] <= 12: cl[-1] = (cl[-1][0], e)
        else: cl.append((s, e))
    if cl != prev:
        print(f"   y={y}: {cl}")
        prev = cl
print(f" title darkest core: {core(t, 0, 0, 959, 539)}")
print(f" title cap-height probe: first/last rows with >=20 red px:", end=" ")
rows = [y for y in range(ys.min(), ys.max() + 1) if t[y].sum() >= 20]
print(rows[0], rows[-1])

print("\n### 2. PANELS (blue outline)")
m = blue.copy()
for lbl, (x0, x1, y0, y1) in {"P1": (100, 850, 120, 265), "P2": (100, 850, 280, 425), "P3": (100, 850, 430, 535)}.items():
    print(f" {lbl}: ink bbox {bbox(m, x0, x1, y0, y1)}")
# panel fill color (interior, away from ink)
print(" P1 interior sample x300 y160:", tuple(a[160, 300]), " P2 x300 y300:", tuple(a[300, 300]), " P3 x300 y500:", tuple(a[500, 300]))
print(" gray bg outside panels x300 y20:", tuple(a[20, 300]), " x20 y300:", tuple(a[300, 20]))
print(f" panel blue border core: {core(blue, 70, 200, 90, 220)} / right {core(blue, 875, 200, 895, 220)}")

print("\n### 3. TABLES")
for name, (x0, x1, y0, y1) in {"TOP": (80, 320, 160, 240), "MID": (80, 320, 330, 405), "BOT": (400, 660, 445, 520)}.items():
    print(f" {name} TABLE")
    # vertical gridlines: columns with long vertical ink
    for x in range(x0, x1 + 1):
        rr = runs(ink[y0:y1 + 1, x])
        for s, e in rr:
            if e - s >= 30:
                print(f"   v-grid x={x}: rows {s+y0}..{e+y0} core {tuple(np.median(a[y0+s:y0+e+1, x], axis=0).astype(int))}")
                break
    # horizontal gridlines
    for y in range(y0, y1 + 1):
        rr = runs(ink[y, x0:x1 + 1])
        for s, e in rr:
            if e - s >= 150:
                print(f"   h-grid y={y}: cols {s+x0}..{e+x0} core {tuple(np.median(a[y, x0+s:x0+e+1:x0+s+40 or x0+s+40], axis=0).astype(int))}")
                break

print("\n### 4. PER-CELL DIGIT BBOXES")
cells = {
    "top": (98, 166, 234, 302, 174, 191, 209, 226),
    "mid": (90, 158, 226, 294, 342, 360, 377, 395),
    "bot": (422, 490, 558, 625, 458, 475, 493, 511),
}
for name, (v0, v1, v2, v3, h0, h1, h2, h3) in cells.items():
    print(f" {name}: cols {v0},{v1},{v2},{v3} rows {h0},{h1},{h2},{h3}")
    for ri, (ya, yb) in enumerate(((h0, h1), (h1, h2), (h2, h3))):
        for ci, (xa, xb) in enumerate(((v0, v1), (v1, v2), (v2, v3))):
            d = dark[ya:yb + 1, xa:xb + 1]
            ys2, xs2 = np.where(d)
            if len(ys2):
                print(f"   r{ri+1}c{ci+1}: x {xs2.min()+xa}..{xs2.max()+xa} y {ys2.min()+ya}..{ys2.max()+ya} n={len(ys2)}")

print("\n### 5. MIDDLE TABLE YELLOW (diagonal cells)")
for ci, (xa, xb) in enumerate(((90, 158), (158, 226), (226, 294))):
    for ri, (ya, yb) in enumerate(((341, 359), (359, 377), (377, 395))):
        sub = yellow[ya:yb + 1, xa:xb + 1]
        n = int(sub.sum())
        if n > 5:
            ys2, xs2 = np.where(sub)
            print(f"   cell r{ri+1}c{ci+1}: yellow n={n} bbox x {xs2.min()+xa}..{xs2.max()+xa} y {ys2.min()+ya}..{ys2.max()+ya} core {core(yellow, xa, ya, xb, yb, 12)}")
ascii_map(100, 300, 340, 396, "middle table zone (yellow strokes)")

print("\n### 6. CHAIN TEXT + LABELS (already measured; re-verify bboxes)")
for lbl, (mask, x0, x1, y0, y1) in {
    "top-label X^TX red": (red, 90, 150, 128, 162),
    "top-chain red X^TX": (red, 330, 400, 175, 220),
    "top-chain dark =0": (dark, 400, 440, 175, 220),
    "top-chain 'Singular Matrix'": (dark, 490, 630, 175, 220),
    "top-chain 'No Inverse' red": (red, 700, 800, 175, 220),
    "mid-label paren+red": (red, 85, 165, 292, 330),
    "mid-label dark +": (dark, 150, 170, 292, 330),
    "mid-label blue λI": (blue, 165, 215, 292, 330),
    "mid-label green λ=3": (green, 240, 295, 292, 330),
    "mid-chain red X^TX": (red, 330, 400, 340, 390),
    "mid-chain dark =5685": (dark, 395, 470, 340, 390),
    "mid-chain 'Non-Singular Matrix'": (dark, 515, 695, 340, 390),
    "mid-chain 'Inverse Exists' red": (red, 755, 880, 340, 390),
    "bot-expr paren+red": (red, 150, 215, 455, 505),
    "bot-expr dark +": (dark, 210, 235, 455, 505),
    "bot-expr blue λI": (blue, 235, 300, 455, 505),
}.items():
    print(f" {lbl}: bbox {bbox(mask, x0, x1, y0, y1)} core {core(mask, x0, y0, x1, y1)}")
# dark parens (not covered by red/blue)
for lbl, (x0, x1, y0, y1) in {
    "mid-label dark parens": (85, 100, 292, 330),
    "mid-label closing paren": (198, 215, 292, 330),
    "bot-expr dark parens+sup": (145, 300, 455, 505),
}.items():
    print(f" {lbl}: bbox {bbox(dark, x0, x1, y0, y1)} core {core(dark, x0, y0, x1, y1)}")

print("\n### 7. ARROWS")
for lbl, (x0, x1, y0, y1) in {
    "top arrow1": (455, 485, 190, 212), "top arrow2": (655, 685, 190, 212),
    "mid arrow1": (485, 512, 358, 378), "mid arrow2": (725, 752, 358, 378),
    "bottom arrow": (360, 390, 470, 490),
}.items():
    print(f" {lbl}: blue bbox {bbox(blue, x0, x1, y0, y1)} core {core(blue, x0, y0, x1, y1)}")
asm = {"top arrow1": (458, 480, 195, 207), "mid arrow1": (487, 507, 361, 374), "bottom arrow": (363, 383, 473, 486)}
for k, (x0, x1, y0, y1) in asm.items():
    ascii_map(x0, x1, y0, y1, k)
print(" bottom arrow: full blue/dark span x360..400:")
for y in range(470, 490):
    rr = runs(blue[y, 360:400]); rd = runs(dark[y, 360:400])
    if rr or rd: print(f"   y={y}: blue {[(s+360,e+360) for s,e in rr]} dark {[(s+360,e+360) for s,e in rd]}")

print("\n### 8. BOTTOM EXPRESSION detail (x255..300, y460..500)")
ascii_map(255, 300, 460, 500, "bottom expr right end")
print(" dark-ink x-cluster census in x300..340 (nothing expected):", bbox(dark, 300, 340, 455, 505))

print("\n### 9. BADGE")
by, bx = np.where(yellow[55:95, 850:900])
pts = a[by + 55, bx + 850]
print(f" badge yellow px: n={len(by)} bbox x {bx.min()+850}..{bx.max()+850} y {by.min()+55}..{by.max()+55}")
# numeral '21' ink: dark inside badge
d = dark[55:95, 850:900]
ys2, xs2 = np.where(d)
if len(ys2):
    print(f" badge numeral dark ink: x {xs2.min()+850}..{xs2.max()+850} y {ys2.min()+55}..{ys2.max()+55}")

print("\n### 10. FONT PROBE — digits and letters (serif vs sans)")
ascii_map(192, 212, 193, 208, "top-table r2c2 '40' (digits)")
ascii_map(260, 280, 193, 208, "top-table r2c3 '46'")
ascii_map(570, 600, 190, 212, "chain 'Mat' of 'Matrix'")
ascii_map(340, 400, 186, 210, "top chain |X^T X| = 0")
ascii_map(420, 470, 356, 378, "mid chain = 5685 digits")

print("\n### 11. KEY COLORS")
print(" title red darkest:", core(red, 250, 0, 730, 120, 6))
print(" label red darkest:", core(red, 90, 130, 145, 158, 6))
print(" chain red darkest:", core(red, 700, 190, 800, 210, 6))
print(" green darkest:", core(green, 240, 300, 290, 325, 6))
print(" yellow cell core:", core(yellow, 100, 340, 300, 396, 20))
print(" top-table digit black core:", core(dark, 120, 175, 300, 225, 6))
print(" bot-table digit black core:", core(dark, 420, 455, 630, 510, 6))
print(" gridline gray core (top h-grid y191):", tuple(np.median(a[191, 100:300], axis=0).astype(int)))
print(" gridline gray core (bot v-grid x490):", tuple(np.median(a[460:505, 490], axis=0).astype(int)))
