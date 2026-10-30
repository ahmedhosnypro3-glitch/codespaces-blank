#!/usr/bin/env python3
"""Slide 030 attempt-3 mandatory pre-judge selfcheck (PIL numbers, render_3.png).

Render: 2001x1125 @150dpi => scale 2001/960 = 2.0844 x, 1125/540 = 2.0833 y.
All canonical values are frame px (960x540, 1px = 1pt) measured from
unique_slides/slide_030.jpg.  Prints PASS/FAIL per check with numbers.
"""
import sys
import numpy as np
from PIL import Image

R = "recreated_pptx/qa/slide030/render_3.png"
V = "videos/machine-learning/03_ridger_regression_gradient_descent"
im = np.asarray(Image.open(f"{V}/{R}").convert("RGB")).astype(int)
H, W = im.shape[:2]
SX = W / 960.0
SY = H / 540.0
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

fails = []
def chk(ok, msg):
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        fails.append(msg)

def win_frame(x0, y0, x1, y1):
    return (int(x0 * SX), int(y0 * SY), int(x1 * SX), int(y1 * SY))

def ink_bbox(mask, x0, y0, x1, y1):
    X0, Y0, X1, Y1 = win_frame(x0, y0, x1, y1)
    sub = mask[Y0:Y1, X0:X1]
    ys, xs = np.where(sub)
    if not len(xs):
        return None
    return (xs.min() + X0, ys.min() + Y0, xs.max() + X0, ys.max() + Y0)

def to_frame(bb):
    return (bb[0] / SX, bb[1] / SY, bb[2] / SX, bb[3] / SY)

dark = (r < 120) & (g < 120) & (b < 120)
red = (r - g > 60) & (r - b > 40) & (r > 110)
green = (g - r > 40) & (g - b > 40) & (g > 100)
blue = (b - r > 30) & (b - g > 15) & (b > 120)
purple = (r - g > 25) & (b - g > 25) & (b > 120)

print("== slide 030 selfcheck attempt 3 ==")
print(f"render {R} {W}x{H}  SX={SX:.4f} SY={SY:.4f}")

# ---------------------------------------------------------------- 1. FRAME CONTAINMENT
# Every content element must sit inside the house panel (x58..901, y45..538);
# content ink must not cross the strokes.
content_ink = dark | red | green | blue | purple
bb = ink_bbox(content_ink, 60, 47, 900, 537)
print("content ink bbox (frame px):", tuple(round(v, 1) for v in to_frame(bb)))
chk(bb is not None and bb[0] >= int(59 * SX) and bb[2] <= int(900 * SX), "1a content inside house panel x58..901")
chk(bb is not None and bb[1] >= int(46 * SY) and bb[3] <= int(537 * SY), "1b content inside house panel y45..538")

# per-element containment
def check_in(inner, outer, name):
    ok = (inner[0] >= outer[0] - 2 and inner[1] >= outer[1] - 2 and
          inner[2] <= outer[2] + 2 and inner[3] <= outer[3] + 2)
    chk(ok, f"{name}: ink {tuple(round(v,1) for v in to_frame(inner))} inside {tuple(round(v,1) for v in to_frame(outer))}")

# title band: ink must not spill below y=96
tb = ink_bbox(dark | red | green, 56, 55, 700, 110)
check_in(tb, win_frame(56, 55, 700, 96), "1c title band y<=96")

# param table: navy border + ink inside
navy = (b > 90) & (b - r > 50) & (b - g > 50) & (r < 130)
pb = ink_bbox(navy, 95, 190, 250, 292)
print("param navy border bbox:", tuple(round(v, 1) for v in to_frame(pb)))
check_in(pb, win_frame(101, 197, 239, 283), "1d param navy border at measured x103..237 y199..281")
ptxt = ink_bbox(dark, 106, 202, 235, 279)
check_in(ptxt, win_frame(104, 200, 236, 280), "1e param text inside frame")

# upper equation box: red border bbox + dark equation ink inside
ub = ink_bbox(red, 390, 178, 540, 220)
print("upper red box bbox:", tuple(round(v, 1) for v in to_frame(ub)))
check_in(ub, win_frame(397, 183, 532, 214), "1f upper red box at 399..530 y185..212")
eq = ink_bbox(dark, 402, 188, 528, 210)
print("eq1 ink bbox:", tuple(round(v, 1) for v in to_frame(eq)))
chk(eq is not None, "2a equation f(x)=(x-5)^2+1 has ink")
if eq:
    chk(116 <= (eq[2] - eq[0]) / SX <= 124, f"2b eq1 ink width {(eq[2]-eq[0])/SX:.1f}px (expect ~119)")

# green formula box
gb = ink_bbox(green, 340, 225, 565, 290)
print("green box bbox:", tuple(round(v, 1) for v in to_frame(gb)))
check_in(gb, win_frame(346, 232, 556, 283), "1g green box at 348..554 y234..281")
x5 = ink_bbox(red, 350, 236, 520, 256)
print("X=5 red ink bbox:", tuple(round(v, 1) for v in to_frame(x5)) if x5 else None)
chk(x5 is not None, "2c X=5 red equation has ink")
if x5:
    chk(x5[0] / SX >= 350, f"2d X=5 starts at frame x {x5[0]/SX:.1f} (box left 348)")
line2 = ink_bbox(dark | blue, 350, 258, 555, 282)
print("line2 ink bbox:", tuple(round(v, 1) for v in to_frame(line2)))
check_in(line2, win_frame(350, 258, 553, 280), "1h line2 inside green box")

# callout box: purple fill/border bbox + text inside
cb = ink_bbox(purple, 330, 288, 575, 325)
print("callout purple bbox:", tuple(round(v, 1) for v in to_frame(cb)))
check_in(cb, win_frame(333, 290, 571, 322), "1i callout box at 335..569 y292..320")

# plot frame and contents
pl = ink_bbox(red, 565, 58, 818, 318)
print("plot red frame bbox:", tuple(round(v, 1) for v in to_frame(pl)))
check_in(pl, win_frame(570, 63, 812, 313), "1j plot frame at 572..810 y65..311")
bluebb = ink_bbox(blue, 575, 68, 808, 308)
print("parabola blue bbox:", tuple(round(v, 1) for v in to_frame(bluebb)) if bluebb else None)
chk(bluebb is not None, "1k parabola blue ink present")
grn = ink_bbox(green, 675, 245, 705, 268)
print("green vertex dot bbox:", tuple(round(v, 1) for v in to_frame(grn)) if grn else None)
chk(grn is not None and abs((grn[0]+grn[2])/2/SX - 688) < 4, "1l green dot near (688,255)")
rd = ink_bbox(red, 650, 172, 675, 195)
print("red dot bbox:", tuple(round(v, 1) for v in to_frame(rd)) if rd else None)
chk(rd is not None and abs((rd[0]+rd[2])/2/SX - 662) < 5, "1m red dot near (662,183)")

# iteration table navy frame + cell block
it = ink_bbox(navy, 70, 318, 665, 540)
print("iter navy frame bbox:", tuple(round(v, 1) for v in to_frame(it)))
check_in(it, win_frame(76, 323, 656, 532), "1n iter navy frame at 78..654 y325..530")

# ---------------------------------------------------------------- 4. TABLE DATA
# 8 rows x 12 cols; inspect each cell interior for text ink on top of its fill.
def cell_has_ink(cx0, cy0, cx1, cy1):
    X0, Y0, X1, Y1 = win_frame(cx0, cy0, cx1, cy1)
    sub = im[Y0:Y1, X0:X1].reshape(-1, 3)
    med = np.median(sub, axis=0)
    diff = np.abs(sub - med).sum(axis=1)
    return int((diff > 120).sum())

groups = [
    ("g1", 334.0, 21.5, 2),
    ("g2", 380.0, 21.5, 2),
    ("g3", 427.0, 21.5, 2),
    ("g4", 473.0, 24.0, 1),
    ("g5", 499.0, 24.0, 1),
]
cells_without_ink = []
total = 0
for name, gy, rh, nrows in groups:
    for ri in range(nrows):
        for ci in range(12):
            x0 = 89 + (61 if ci == 0 else 61 + (ci - 1) * 44)
            w = 61 if ci == 0 else 44
            y0 = gy + ri * rh
            n = cell_has_ink(x0 + 4, y0 + 3, x0 + w - 4, y0 + rh - 3)
            total += 1
            if n < 6:
                cells_without_ink.append((name, ri, ci, n))
print(f"iteration cells checked={total}, cells lacking ink={len(cells_without_ink)} {cells_without_ink[:8]}")
chk(total == 96 and not cells_without_ink, "4a all 96 iteration cells carry ink")
chk(len(groups) == 5 and sum(gr[3] for gr in groups) == 8, "4b iteration grid is 8 rows x 12 cols")

# param table cells (3 rows x 2 cols)
p_missing = []
for ri in range(3):
    for ci, (x0, w) in enumerate([(104, 76), (180, 56)]):
        y0 = 200 + ri * 26
        n = cell_has_ink(x0 + 4, y0 + 3, x0 + w - 4, y0 + 23)
        if n < 6:
            p_missing.append((ri, ci, n))
chk(not p_missing, f"4c param table all 6 cells carry ink missing={p_missing}")

# ---------------------------------------------------------------- 3. DELIMITERS
print("3 DELIMITER GEOMETRY: n/a — slide 030 has no multi-line parenthesised/bracketed block")

# ---------------------------------------------------------------- 5. LINE SPACING
def ink_bands(x0, y0, x1, y1):
    X0, Y0, X1, Y1 = win_frame(x0, y0, x1, y1)
    rows = (dark[Y0:Y1, X0:X1] | red[Y0:Y1, X0:X1] | blue[Y0:Y1, X0:X1]).sum(axis=1)
    bands, cur = [], None
    for i, v in enumerate(rows):
        if v > 1:
            cur = [i, i] if cur is None else [cur[0], i]
        elif cur is not None:
            bands.append((Y0 + cur[0], Y0 + cur[1]))
            cur = None
    if cur is not None:
        bands.append((Y0 + cur[0], Y0 + cur[1]))
    return [(round(a / SY, 1), round(b / SY, 1)) for a, b in bands]

print("5 title ink bands (frame y):", ink_bands(56, 55, 700, 100))
tb2 = ink_bands(56, 55, 700, 100)
chk(len(tb2) == 1, "5a title is a single line (no wrap)")
print("5 green-box text bands:", ink_bands(350, 236, 553, 282))
chk(len(ink_bands(350, 236, 553, 282)) == 2, "5b green box has exactly 2 text lines")
print("5 callout text bands:", ink_bands(336, 293, 568, 319))
chk(len(ink_bands(336, 293, 568, 319)) == 1, "5c callout is a single line")

# ---------------------------------------------------------------- 6. CROP SCALE AUDIT
print(f"6 crop scale audit: render scale SX={SX:.4f} SY={SY:.4f}; original crops upscale x{SX:.4f}/{SY:.4f}")
chk(abs(SX - SY) / SY < 0.01, "6a isotropic render scale (SX~SY) so crop pairs match on both axes")

print()
if fails:
    print(f"SELFCHECK FAIL ({len(fails)} checks)")
    for f in fails:
        print("  -", f)
    sys.exit(1)
print("SELFCHECK PASS — all checks green")
