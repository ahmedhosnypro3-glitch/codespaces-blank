#!/usr/bin/env python3
"""Slide 010 — PIL-vs-original geometry measurement (child lane, render_3).
PIL-FIRST adjudication grounding: compare the delta geometry (green cross,
bright-green dots, pale-rose projection pairs, fitted lines, point count) of the
render_3 render against unique_slides/slide_010.jpg in FRAME px (960x540,
1px=1pt). Reports per-element render-vs-original numbers so any judge finding
can be refuted/confirmed with banked numbers, never vibes. Portable paths.
"""
from PIL import Image
import numpy as np, os

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
R = os.path.join(HERE, "render_3.png")
O = os.path.join(DECK, "unique_slides", "slide_010.jpg")

def load(p):
    return np.asarray(Image.open(p).convert("RGB")).astype(int)

ar = load(R); ao = load(O)
H, W = ar.shape[:2]
SX, SY = W / 960.0, H / 540.0

def to_r(x, y):  # frame px -> render px
    return int(round(x * SX)), int(round(y * SY))

def m(img, kind):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    if kind == "green":  return (g > 90) & (g - r > 30) & (g - b > 30) & (g < 235)
    if kind == "bright": return (g > 200) & (r < 130) & (b < 190)
    if kind == "pale":   return (r > 170) & (r - g > 18) & (r - b > 18) & (g > 105) & (b > 100)
    if kind == "orange": return (r > 190) & (g > 90) & (g < 200) & (b < 110)
    if kind == "blue":   return (b > 120) & (r < 110) & (g < 110)
    raise ValueError(kind)

def band_ink(mask, x0, x1, y_center_f, half=4):
    yc = int(round(y_center_f * SY))
    return int(mask[max(0, yc - half):yc + half + 1, to_r(x0, 0)[0]:to_r(x1, 0)[0]].sum())

def col_ink(mask, x_f, y0, y1, half=4):
    xc = to_r(x_f, 0)[0]
    return int(mask[to_r(0, y0)[1]:to_r(0, y1)[1], max(0, xc - half):xc + half + 1].sum())

print("render_3 %dx%d  SX=%.5f SY=%.5f" % (W, H, SX, SY))
print("(original is 960x540; render is frame px x %.4f)" % SX)
print()

# green cross horizontals/verticals: render vs original band ink (original in native frame px)
tests = []
for label, kind, x0, x1, y in (("green h LEFT", "green", 128, 360, 238.5),
                               ("green h RIGHT", "green", 540, 772, 287)):
    tests.append((label, kind, "row_band", (x0, x1, y)))
for label, kind, x, y0, y1 in (("green v LEFT", "green", 353, 240, 431),
                               ("green v RIGHT", "green", 766.5, 288.5, 431)):
    tests.append((label, kind, "col_band", (x, y0, y1)))

gr = m(ar, "green"); go = m(ao, "green")
for label, kind, mode, p in tests:
    if kind == "green":
        if mode == "row_band":
            x0, x1, y = p
            nr = band_ink(gr, x0, x1, y); no = int(go[int(y) - 4: int(y) + 5, x0:x1].sum())
        else:
            x, y0, y1 = p
            nr = col_ink(gr, x, y0, y1); no = int(go[int(y0):int(y1), int(round(x)) - 4: int(round(x)) + 5].sum())
        print("%-16s render ink=%4d   original ink=%4d" % (label, nr, no))

print()
# bright-green axis dots: render comp diameter vs original
def comp_center_diam(mask, minpix):
    ys, xs = np.nonzero(mask)
    return list(zip(xs, ys))
br = m(ar, "bright"); bo = m(ao, "bright")
for label, cxf, cyf in (("bright dot LEFT", 353, 433), ("bright dot RIGHT", 766.5, 433)):
    rcx, rcy = to_r(cxf, cyf)
    sub = br[rcy - 12:rcy + 13, rcx - 12:rcx + 13]
    n_r = int(sub.sum())
    subo = bo[cyf - 6:cyf + 7, int(round(cxf)) - 6: int(round(cxf)) + 7]
    n_o = int(subo.sum())
    print("%-16s render 25x25win ink=%4d   original 13x13win ink=%4d" % (label, n_r, n_o))

print()
# pale-rose projections
pr = m(ar, "pale"); po = m(ao, "pale")
for label, mode, p in (("pale h L y289.5", "row_band", (136, 320, 289.5)),
                       ("pale h L y300.5", "row_band", (136, 377, 300.5)),
                       ("pale h R y291.5", "row_band", (549, 733, 291.5)),
                       ("pale h R y301.5", "row_band", (549, 790, 301.5)),
                       ("pale v L x324", "col_band", (324, 301, 434)),
                       ("pale v L x382", "col_band", (382, 312, 434)),
                       ("pale v R x737", "col_band", (737, 302, 434)),
                       ("pale v R x795", "col_band", (795, 313, 434))):
    if mode == "row_band":
        x0, x1, y = p
        nr = band_ink(pr, x0, x1, y); no = int(po[int(y) - 4: int(y) + 5, x0:x1].sum())
    else:
        x, y0, y1 = p
        nr = col_ink(pr, x, y0, y1); no = int(po[int(y0):int(y1), int(round(x)) - 4: int(round(x)) + 5].sum())
    print("%-16s render ink=%4d   original ink=%4d" % (label, nr, no))

print()
# fitted line sample points (frame px) vs original — both should carry blue ink
from collections import namedtuple
def line_hits(mask, x0, y0, x1, y1, is_orig):
    hits = 0
    for t in (0.1, 0.3, 0.5, 0.7, 0.9):
        fx = x0 + (x1 - x0) * t; fy = y0 + (y1 - y0) * t
        if is_orig:
            win = mask[int(fy) - 3: int(fy) + 4, int(fx) - 3: int(fx) + 4]
        else:
            rx, ry = to_r(fx, fy)
            win = mask[ry - 6: ry + 7, rx - 6: rx + 7]
        if win.sum() >= 6: hits += 1
    return hits
blr = m(ar, "blue"); blo = m(ao, "blue")
for label, seg in (("LEFT", (142, 352, 432, 200)), ("RIGHT", (556, 390, 830, 256))):
    print("fitted line %s: render hits=%d/5  original hits=%d/5 (5 sampled pts)" %
          (label, line_hits(blr, *seg, False), line_hits(blo, *seg, True)))

print()
# orange data-point count per panel: render vs original
def count_orange(mask, split_x_f, minpix):
    seen = np.zeros_like(mask, dtype=bool); Hh, Ww = mask.shape; left = right = 0
    ys, xs = np.nonzero(mask)
    splitx = int(round(split_x_f * (W / 960.0))) if mask.shape[1] != 960 else split_x_f
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]: continue
        stack = [(y0, x0)]; seen[y0, x0] = True; n = 0
        while stack:
            y, x = stack.pop(); n += 1
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < Hh and 0 <= nx < Ww and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True; stack.append((ny, nx))
        if n >= (80 if mask.shape[1] != 960 else 12):
            if x0 < splitx: left += 1
            else: right += 1
    return left, right
oro = m(ao, "orange")
lor, ror = count_orange(m(ar, "orange"), 480, 80)
loo, roo = count_orange(oro, 480, 12)
print("orange dots  RENDER L=%d R=%d   ORIGINAL L=%d R=%d" % (lor, ror, loo, roo))
