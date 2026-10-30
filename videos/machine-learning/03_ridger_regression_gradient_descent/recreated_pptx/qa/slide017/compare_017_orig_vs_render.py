#!/usr/bin/env python3
"""Slide 017 side-by-side original vs render_4 comparison (frame 960x540, 1px=1pt).

Measures the same geometry/colour/ink quantities on BOTH images: the original frame
(960x540 native) and render_4.png (2001x1125 LANCZOS-downscaled x2.0833 to 960x540).
Every number the K=4 judges can cite is therefore pre-measured, so any FAIL/MINOR can
be adjudicated PIL-first against this bank.

Run: python3 compare_017_orig_vs_render.py | tee compare_017_orig_vs_render.txt
"""
import numpy as np
from PIL import Image

ROOT = "/workspaces/codespaces-blank/ai_llm_slides"
VROOT = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = VROOT + "/recreated_pptx/qa/slide017"
ORIG_PATH = VROOT + "/unique_slides/slide_017.jpg"
RENDER_PATH = QA + "/render_4.png"

S = 2001 / 960.0  # render-px per frame-px

orig_im = Image.open(ORIG_PATH).convert("RGB")
rend_im = Image.open(RENDER_PATH).convert("RGB")
print("orig", orig_im.size, "render", rend_im.size, "scale S =", S)

def to_arr(im, downscale):
    if downscale:
        im = im.resize((960, 540), Image.LANCZOS)
    return np.asarray(im).astype(int)

def stats(path, downscale):
    im = Image.open(path).convert("RGB")
    a = to_arr(im, downscale)
    lum = a.mean(axis=2)
    red = (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50) & (a[:, :, 0] > 90)
    blue = (a[:, :, 2] - a[:, :, 0] > 60) & (a[:, :, 2] - a[:, :, 1] > 50) & (a[:, :, 2] > 90)
    dark = lum < 150
    ink = dark | red | blue
    return a, lum, red, blue, dark, ink

O = stats(ORIG_PATH, False)
R = stats(RENDER_PATH, True)
names = ["lum", "ink"]

def vlines(s, x0, x1, y0, y1, frac=0.6, thr=226):
    band = s[1][y0:y1, x0:x1]
    colsum = (band < thr).sum(axis=0)
    hits = [x0 + i for i, c in enumerate(colsum) if c > (y1 - y0) * frac]
    groups = []
    for x in hits:
        if groups and x - groups[-1][-1] <= 1:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [(g[0], g[-1]) for g in groups]

def hlines(s, x0, x1, y0, y1, frac=0.55, thr=226):
    band = s[1][y0:y1, x0:x1]
    rowsum = (band < thr).sum(axis=1)
    hits = [y0 + i for i, c in enumerate(rowsum) if c > (x1 - x0) * frac]
    groups = []
    for y in hits:
        if groups and y - groups[-1][-1] <= 1:
            groups[-1].append(y)
        else:
            groups.append([y])
    return [(g[0], g[-1]) for g in groups]

def bb(s, mask, x0, y0, x1, y1):
    m = mask[y0:y1, x0:x1]
    yy, xx = np.where(m)
    if len(xx) == 0:
        return None
    return (x0 + xx.min(), x0 + xx.max(), y0 + yy.min(), y0 + yy.max(), int(len(xx)))

def med(s, x0, y0, x1, y1):
    return tuple(int(v) for v in np.median(s[0][y0:y1, x0:x1].reshape(-1, 3), axis=0))

def both(label, fn):
    print(f"  {label:34s} orig {fn(O)}  |  rend {fn(R)}")

print("\n== CHROME ==")
both("canvas @(100,50)", lambda s: tuple(int(v) for v in s[0][50, 100]))
both("panel @(70,300)", lambda s: tuple(int(v) for v in s[0][300, 70]))
both("left stroke x58-59", lambda s: (tuple(int(v) for v in s[0][300, 58]),
                                      tuple(int(v) for v in s[0][300, 59])))
both("right stroke x901", lambda s: tuple(int(v) for v in s[0][300, 901]))
both("top band red px (y45..55)", lambda s: int(s[2][45:55, 60:900].sum()))
both("badge fill @(870,60)", lambda s: tuple(int(v) for v in s[0][60, 870]))
both("badge numeral dark bbox", lambda s: bb(s, s[4], 860, 55, 895, 92))

print("\n== TRAIN TABLE GRIDS ==")
for i, (y0, y1) in enumerate([(120, 255), (258, 395), (396, 532)], start=1):
    both(f"band{i} v-lines", lambda s, y0=y0, y1=y1: vlines(s, 70, 500, y0, y1))
    both(f"band{i} h-lines", lambda s, y0=y0, y1=y1: hlines(s, 70, 500, y0, y1))

print("\n== TEST TABLE GRIDS ==")
for i, (y0, y1) in enumerate([(120, 255), (258, 395), (396, 532)], start=1):
    both(f"band{i} v-lines", lambda s, y0=y0, y1=y1: vlines(s, 640, 900, y0, y1))
    both(f"band{i} h-lines", lambda s, y0=y0, y1=y1: hlines(s, 640, 900, y0, y1))

print("\n== TEST TABLE y-ROW FILLS (label / c1 / c2 / c3) ==")
for tag, ya, yb in [("B1", 224, 247), ("B2", 362, 385), ("B3", 500, 523)]:
    for k, (x0, x1) in enumerate([(669, 719), (720, 770), (771, 821), (822, 872)]):
        both(f"{tag} cell{k+1} fill", lambda s, x0=x0, ya=ya, x1=x1, yb=yb: med(s, x0 + 4, ya, x1 - 4, yb))

print("\n== PER-CELL INK (ink px / dark px, per table cell) ==")
# train rows: header (h0+4..h1-3), label row, data row 1, data row 2, y-row(mint)
def cell_ink(s, x0, x1, ya, yb):
    sub = s[5][ya:yb, x0 + 3:x1 - 3]
    dk = s[4][ya:yb, x0 + 3:x1 - 3]
    return (int(sub.sum()), int(dk.sum()))

train_cols = [(91, 132), (134, 172), (175, 213), (216, 254), (257, 296), (298, 336), (339, 377), (379, 418), (420, 459), (461, 500)]
for tag, rows in [("B1", [(130, 156), (160, 187), (190, 217), (222, 248)]),
                  ("B2", [(270, 293), (300, 324), (328, 354), (361, 386)]),
                  ("B3", [(408, 431), (436, 462), (469, 493), (500, 523)])]:
    for ri, (ya, yb) in enumerate(rows):
        for ci, (x0, x1) in enumerate(train_cols):
            both(f"{tag} r{ri} c{ci}", lambda s, x0=x0, ya=ya, x1=x1, yb=yb: cell_ink(s, x0, x1, ya, yb))

test_cols = [(669, 718), (721, 769), (772, 820), (823, 872)]
for tag, rows in [("B1", [(132, 157), (163, 188), (192, 217), (224, 248)]),
                  ("B2", [(270, 295), (300, 325), (330, 355), (361, 386)]),
                  ("B3", [(408, 433), (437, 463), (470, 494), (500, 523)])]:
    for ri, (ya, yb) in enumerate(rows):
        for ci, (x0, x1) in enumerate(test_cols):
            both(f"{tag} r{ri} c{ci}", lambda s, x0=x0, ya=ya, x1=x1, yb=yb: cell_ink(s, x0, x1, ya, yb))

print("\n== LABELS / W BOXES / ARROWS ==")
both("Train blue label box", lambda s: bb(s, s[3], 80, 92, 200, 132))
both("Test blue label box", lambda s: bb(s, s[3], 780, 96, 900, 132))
for i, (y0, y1) in enumerate([(115, 260), (255, 400), (395, 535)], start=1):
    both(f"band{i} W red border", lambda s, y0=y0, y1=y1: bb(s, s[2], 480, y0, 660, y1))
    both(f"band{i} norm line (blue)", lambda s, y0=y0, y1=y1: bb(s, s[3], 510, y1 - 40, 625, y1 - 3))
for i, (y0, y1) in enumerate([(170, 225), (300, 360), (435, 495)], start=1):
    for x0, x1, side in [(455, 510, "left"), (620, 675, "right")]:
        both(f"band{i} arrow {side}", lambda s, x0=x0, y0=y0, x1=x1, y1=y1: bb(s, s[3], x0, y0, x1, y1))

print("\n== TITLE RUNS (ink bbox + red/blue px) ==")
for name, x0, x1 in [("Adding", 170, 280), ("Ridge", 285, 372), ("Regularizer", 378, 542),
                     ("to", 548, 578), ("the", 584, 630), ("model", 638, 726),
                     ("lambda=3", 744, 810)]:
    def one(s, x0=x0, x1=x1):
        return (bb(s, s[5], x0, 55, x1, 100),
                int(s[2][55:100, x0:x1].sum()), int(s[3][55:100, x0:x1].sum()))
    both(f"title '{name}'", one)

print("\n== TEST-LABEL INK COLOUR (Train / Test label boxes) ==")
def inkcolor(s, x0, y0, x1, y1):
    r = s[0][y0:y1, x0:x1].reshape(-1, 3)
    idx = np.argsort(r.mean(axis=1))[:30]
    return tuple(int(v) for v in np.median(r[idx], axis=0))
both("Train label ink", lambda s: inkcolor(s, 96, 100, 160, 120))
both("Test  label ink", lambda s: inkcolor(s, 801, 100, 866, 120))
both("Train label red px", lambda s: int(s[2][96:125, 96:160].sum()))
both("Test  label red px", lambda s: int(s[2][96:125, 801:866].sum()))
both("Train label blue px", lambda s: int(s[3][96:125, 96:160].sum()))
both("Test  label blue px", lambda s: int(s[3][96:125, 801:866].sum()))

print("\nRESULT: compared")
