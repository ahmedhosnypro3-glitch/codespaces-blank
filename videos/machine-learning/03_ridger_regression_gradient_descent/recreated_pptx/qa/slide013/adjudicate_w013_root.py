#!/usr/bin/env python3
"""PIL-first adjudication harness for slide 013 (w013-root lane).

Measures EVERY region of the current certified render (render_6.png) against
unique_slides/slide_013.jpg at 960x540 frame space (render scale 2001/960).
Emits per-region ink censuses, gridline positions, cell-value bboxes, colour
medians and yellow-fill extents so judge findings can be refuted or confirmed
with numbers before any build change.
"""
import os

import numpy as np
from PIL import Image

DECK = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")) + os.sep

R = Image.open(DECK + "recreated_pptx/qa/slide013/render_6.png").convert("RGB")
O = Image.open(DECK + "unique_slides/slide_013.jpg").convert("RGB")
S = R.size[1] / 540.0
ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)
print(f"render {R.size} scale {S:.4f}   original {O.size}")


def rpx(x, y):
    return ra[int(y * S), int(x * S)]


def rbox(x0, y0, x1, y1):
    """Downsample render frame-space box to 1px/frame-px via nearest sample."""
    X0, X1, Y0, Y1 = int(round(x0 * S)), int(round(x1 * S)), int(round(y0 * S)), int(round(y1 * S))
    sub = ra[Y0:Y1, X0:X1]
    h, w = sub.shape[:2]
    ys = (np.arange(int(y1 - y0)) * (h / (y1 - y0))).astype(int)
    xs = (np.arange(int(x1 - x0)) * (w / (x1 - x0))).astype(int)
    return sub[np.clip(ys, 0, h - 1)][:, np.clip(xs, 0, w - 1)]


def obox(x0, y0, x1, y1):
    return ro[y0:y1, x0:x1]


def stats(a, name):
    print(f"  {name}: shape {a.shape} median {tuple(np.median(a.reshape(-1, 3), axis=0).astype(int))}")


# ---------- masks ----------
def ink_mask(a):
    """Non-background (white OR panel-gray)."""
    bg = (np.abs(a[:, :, 0] - 255) < 10) & (np.abs(a[:, :, 1] - 255) < 10) & (np.abs(a[:, :, 2] - 255) < 10)
    bg |= (np.abs(a[:, :, 0] - 233) < 10) & (np.abs(a[:, :, 1] - 233) < 10) & (np.abs(a[:, :, 2] - 231) < 12)
    return ~bg


def yellow(a):
    return (a[:, :, 0] > 235) & (a[:, :, 1] > 200) & (a[:, :, 2] < 170) & (a[:, :, 0] - a[:, :, 2] > 90)


def red(a):
    return (a[:, :, 0] > a[:, :, 1] + 40) & (a[:, :, 0] > a[:, :, 2] + 40)


def blue(a):
    return (a[:, :, 2] > a[:, :, 0] + 60) & (a[:, :, 2] > 100) & (a[:, :, 1] < a[:, :, 0] + 30)


def mint(a):
    return (a[:, :, 0] < 235) & (a[:, :, 1] > 240) & (a[:, :, 2] > 200) & (a[:, :, 2] - a[:, :, 0] > 10) & (a[:, :, 1] - a[:, :, 0] > 20)


REGIONS = [
    ("title",        154, 62, 800, 100),
    ("label Train",   90, 92, 175, 130),
    ("label Test",   795, 92, 875, 130),
    ("train B1",      92, 120, 465, 258),
    ("train B2",      92, 260, 465, 396),
    ("train B3",      92, 398, 465, 532),
    ("test  B1",     715, 120, 876, 258),
    ("test  B2",     715, 260, 876, 396),
    ("test  B3",     715, 398, 876, 532),
    ("Wbox  B1",     503, 124, 626, 253),
    ("Wbox  B2",     503, 263, 626, 392),
    ("Wbox  B3",     503, 400, 626, 528),
    ("arrow L B1",   460, 180, 506, 216),
    ("arrow R B1",   623, 180, 670, 216),
    ("arrow L B3",   460, 446, 506, 482),
    ("arrow R B3",   623, 446, 670, 482),
]

print("\n=== region censuses (ink / yellow / red / blue px, frame-space) ===")
print(f"{'region':14s} {'ink R':>8s} {'ink O':>8s} {'yel R':>7s} {'yel O':>7s} {'red R':>7s} {'red O':>7s} {'blu R':>7s} {'blu O':>7s} {'mint R':>7s} {'mint O':>7s}")
for (name, x0, y0, x1, y1) in REGIONS:
    rr, oo = rbox(x0, y0, x1, y1), obox(x0, y0, x1, y1)
    iR, iO = ink_mask(rr).sum(), ink_mask(oo).sum()
    yR, yO = yellow(rr).sum(), yellow(oo).sum()
    dR, dO = red(rr).sum(), red(oo).sum()
    bR, bO = blue(rr).sum(), blue(oo).sum()
    mR, mO = mint(rr).sum(), mint(oo).sum()
    print(f"{name:14s} {iR:8d} {iO:8d} {yR:7d} {yO:7d} {dR:7d} {dO:7d} {bR:7d} {bO:7d} {mR:7d} {mO:7d}")

# ---------- gridlines ----------
def vlines(a, x0, x1, y0, y1, thresh, label):
    """Crop-relative: a is already cropped; x0/y0 is its origin in frame px."""
    out = []
    h, w = a.shape[:2]
    for x in range(w):
        col = a[y0:y1, x]
        n = (~((col[:, 0] > 240) & (col[:, 1] > 240) & (col[:, 2] > 240))).sum()
        if n > (y1 - y0) * thresh:
            out.append(x0 + x)
    # collapse runs
    groups = []
    for x in out:
        if groups and x - groups[-1][-1] <= 2:
            groups[-1].append(x)
        else:
            groups.append([x])
    return [g[len(g) // 2] for g in groups]


print("\n=== train table B1 vertical gridlines (x92..465, y157..248) ===")
for tag, a in (("RENDER", rbox(92, 157, 465, 248)), ("ORIG  ", obox(92, 157, 465, 248))):
    print(f"  {tag}: {vlines(a, 92, 465, 0, 91, 0.60, 'trainv')}")

print("\n=== train table B1 horizontal gridlines (y126..250) ===")
for tag, a in (("RENDER", rbox(92, 126, 465, 250)), ("ORIG  ", obox(92, 126, 465, 250))):
    rows = []
    for y in range(0, a.shape[0]):
        row = a[y]
        n = (~((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240))).sum()
        if n > 367 * 0.60:
            rows.append(126 + y)
    print(f"  {tag}: {rows}")

print("\n=== test table B1 gridlines (x715..876, y126..250) ===")
for tag, a in (("RENDER", rbox(715, 126, 876, 250)), ("ORIG  ", obox(715, 126, 876, 250))):
    print(f"  {tag} v: {vlines(a, 715, 876, 0, 124, 0.60, 'testv')}")
    rows = []
    for y in range(a.shape[0]):
        row = a[y]
        n = (~((row[:, 0] > 240) & (row[:, 1] > 240) & (row[:, 2] > 240))).sum()
        if n > 161 * 0.60:
            rows.append(126 + y)
    print(f"  {tag} h: {rows}")

# ---------- yellow cell fills ----------
print("\n=== yellow fills (x420..460, train B2/B3 X8 col; test y rows) ===")
for name, x0, y0, x1, y1 in [
    ("train B2 X8", 420, 296, 459, 326),
    ("train B3 X8", 420, 435, 459, 464),
    ("test  B2 yrow", 720, 355, 872, 385),
    ("test  B3 yrow", 720, 492, 872, 522),
]:
    rr, oo = rbox(x0, y0, x1, y1), obox(x0, y0, x1, y1)
    print(f"  {name}: render {yellow(rr).sum():5d}px  orig {yellow(oo).sum():5d}px")

# ---------- label boxes ----------
print("\n=== label box fill medians (interior) ===")
for name, x0, y0, x1, y1 in [("Train", 100, 100, 158, 123), ("Test", 806, 100, 863, 123)]:
    rr, oo = rbox(x0, y0, x1, y1), obox(x0, y0, x1, y1)
    print(f"  {name}: render {tuple(np.median(rr.reshape(-1,3),axis=0).astype(int))}  orig {tuple(np.median(oo.reshape(-1,3),axis=0).astype(int))}")

# ---------- W box red borders ----------
print("\n=== W box red border presence (scan border rows/cols) ===")
for bi, (bx0, by0, bx1, by1) in enumerate([(505, 126, 624, 251), (505, 265, 624, 389), (505, 402, 624, 526)], start=1):
    ro_b = rbox(bx0 - 6, by0 - 6, bx1 + 6, by1 + 6)
    oo_b = obox(bx0 - 6, by0 - 6, bx1 + 6, by1 + 6)
    print(f"  Wbox B{bi}: render red {red(ro_b).sum():5d}px  orig red {red(oo_b).sum():5d}px")

# ---------- arrows ----------
print("\n=== arrow cores (blue px in shaft window) ===")
for name, x0, y0, x1, y1 in [
    ("L arrow B1 shaft", 466, 189, 494, 210),
    ("R arrow B1 shaft", 629, 189, 657, 210),
    ("L arrow B3 shaft", 466, 455, 494, 476),
    ("R arrow B3 shaft", 629, 455, 657, 476),
]:
    rr, oo = rbox(x0, y0, x1, y1), obox(x0, y0, x1, y1)
    print(f"  {name}: render blue {blue(rr).sum():5d}px red {red(rr).sum():4d}px | orig blue {blue(oo).sum():5d}px red {red(oo).sum():4d}px")

# ---------- ellipses ----------
print("\n=== ellipse yellow extents ===")
for bi, (x0, y0, x1, y1) in enumerate([(510, 210, 620, 251), (513, 348, 620, 388), (516, 488, 622, 526)], start=1):
    oo_b = obox(x0, y0, x1, y1)
    rr_b = rbox(x0, y0, x1, y1)
    ys, xs = np.where(yellow(oo_b))
    ys2, xs2 = np.where(yellow(rr_b))
    if len(xs):
        print(f"  ellipse B{bi} ORIG  x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={len(xs)}")
    if len(xs2):
        print(f"  ellipse B{bi} RNDER x{x0+xs2.min()}..{x0+xs2.max()} y{y0+ys2.min()}..{y0+ys2.max()} n={len(xs2)}")
    if not len(xs) or not len(xs2):
        print(f"  ellipse B{bi}: MISSING (orig n={len(xs)}, render n={len(xs2)})")

# ---------- title ----------
print("\n=== title ink bbox ===")
for tag, a in (("RENDER", rbox(140, 60, 820, 105)), ("ORIG  ", obox(140, 60, 820, 105))):
    m = ink_mask(a)
    ys, xs = np.where(m)
    if len(xs):
        print(f"  {tag} ink bbox x{140+xs.min()}..{140+xs.max()} y{60+ys.min()}..{60+ys.max()} n={len(xs)}")
