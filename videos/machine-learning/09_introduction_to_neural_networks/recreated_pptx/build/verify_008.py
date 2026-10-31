#!/usr/bin/env python3
"""Verify slide_008_recreated.pptx against the measured original geometry.

Checks the rejudge PNG (render_pdf.sh output, 2001x1125 @150dpi; S = 2001/960
render px per original px) against the measurements taken from
unique_slides/slide_008.jpg (960x540, 1px == 1pt). Element positions carry a
+-4px tolerance; house chrome follows the house frame rule.
"""
import sys
import numpy as np
from PIL import Image

S = 2001 / 960.0
TOL = 4  # original px

im = Image.open("slide_008_rejudge_rendered-1.png").convert("RGB")
A = np.asarray(im).astype(np.int32)
RH, RW = A.shape[:2]
print("render %d x %d px, scale %.4f" % (RW, RH, S))

results = []


def check(name, ok, detail):
    results.append((name, ok))
    print("%-4s %-34s %s" % ("PASS" if ok else "FAIL", name, detail))


def rect(x0, y0, x1, y1):
    """Original-px rect -> render-px slice, expanded by TOL."""
    return (slice(int((y0 - TOL) * S), int((y1 + TOL) * S) + 1),
            slice(int((x0 - TOL) * S), int((x1 + TOL) * S) + 1))


def count(name, x0, y0, x1, y1, pred, minimum, label):
    r = rect(x0, y0, x1, y1)
    sub = A[r]
    n = int(pred(sub).sum())
    check(name, n >= minimum, "%d px >= %d (%s)" % (n, minimum, label))


is_red = lambda sub: (sub[..., 0] > 120) & (sub[..., 0] - sub[..., 1] > 60) & (sub[..., 0] - sub[..., 2] > 60)
is_blue = lambda sub: (sub[..., 2] > 170) & (sub[..., 2] - sub[..., 0] > 60) & (sub[..., 2] - sub[..., 1] > 40)
is_green = lambda sub: (sub[..., 1] > 140) & (sub[..., 1] - sub[..., 0] > 40) & (sub[..., 1] - sub[..., 2] > 40)
is_magenta = lambda sub: (sub[..., 0] > 200) & (sub[..., 2] > 200) & (sub[..., 1] < 100)
is_yellow = lambda sub: (sub[..., 0] > 230) & (sub[..., 1] > 230) & (sub[..., 2] < 120)
is_salmon = lambda sub: (sub[..., 0] > 240) & (sub[..., 1] > 195) & (sub[..., 1] < 240) & (sub[..., 2] > 185) & (sub[..., 2] < 228)
is_black = lambda sub: (sub[..., 0] < 70) & (sub[..., 1] < 70) & (sub[..., 2] < 70)
is_white = lambda sub: (sub[..., 0] > 235) & (sub[..., 1] > 235) & (sub[..., 2] > 235)

# ---------- house chrome ----------
bg = A[int(25 * S), int(550 * S)]
check("bg #E8E8E8", abs(bg[0] - 232) <= 8 and abs(bg[1] - 232) <= 8 and abs(bg[2] - 232) <= 8,
      "rgb(%d,%d,%d)" % tuple(bg))
fr = A[int(300 * S), int(0.15 * 150)]
check("outer red frame", fr[0] > 140 and fr[0] - fr[1] > 50,
      "rgb(%d,%d,%d) @x=0.15in" % tuple(fr))
ov = A[int(0.75 * 150), int(12.73 * 150)]
check("badge oval #FFF9C4", abs(ov[0] - 255) <= 10 and abs(ov[1] - 249) <= 10 and abs(ov[2] - 196) <= 12,
      "rgb(%d,%d,%d)" % tuple(ov))
badge = A[int(0.30 * 150):int(0.80 * 150), int(12.48 * 150):int(12.98 * 150)]
check("badge numeral ink", int(is_black(badge).sum()) >= 20, "%d black px in badge" % int(is_black(badge).sum()))

# ---------- title: two lines + pure-blue [ONE VS ALL] ----------
band = slice(int(20 * S), int(220 * S))
rows = is_red(A[band]).sum(axis=1)
strong = rows > 8
if strong.any():
    idx = np.where(strong)[0]
    groups = np.split(idx, np.where(np.diff(idx) > 3)[0] + 1)
    bands = [(int(g[0] / S) + 20, int(g[-1] / S) + 20) for g in groups if len(g) > 2]
else:
    bands = []
check("title two red lines", len(bands) >= 2, "red line bands (orig px y): %s" % bands)
tblue = A[int(20 * S):int(220 * S), int(90 * S):int(1900 * S)]
check("title blue [ONE VS ALL]", int(is_blue(tblue).sum()) >= 30,
      "%d blue px in title box" % int(is_blue(tblue).sum()))

# ---------- Undefined callout: blue border/text, white fill ----------
count("Undefined box ink", 73, 131, 147, 160, is_blue, 40, "blue glyph px")
und = A[int(136 * S):int(155 * S), int(80 * S):int(140 * S)]
wfrac = float(is_white(und).mean())
check("Undefined white fill", wfrac > 0.55, "%.0f%% white interior" % (100 * wfrac))

# ---------- New Class: magenta border + text ----------
count("New Class magenta", 715, 372, 786, 395, is_magenta, 25, "magenta px")

# ---------- decision-boundary labels ----------
count("d1(x) red label", 254, 181, 292, 207, is_red, 8, "red px")
count("d2(x) blue label", 556, 141, 592, 167, is_blue, 8, "blue px")
count("d3(x) green label", 705, 199, 746, 223, is_green, 8, "green px")

# ---------- C tag boxes (yellow) ----------
count("C1 tag yellow", 525, 153, 567, 187, is_yellow, 200, "yellow px")
count("C2 tag yellow", 594, 295, 636, 329, is_yellow, 200, "yellow px")
count("C3 tag yellow", 260, 395, 302, 429, is_yellow, 200, "yellow px")

# ---------- "?" boxes (pale pink + red-orange glyph) ----------
count("? box 1 salmon", 434, 318, 477, 353, is_salmon, 300, "salmon px")
count("? box 2 salmon", 591, 177, 632, 209, is_salmon, 300, "salmon px")
count("? box 3 salmon", 243, 264, 282, 296, is_salmon, 300, "salmon px")
count("? box 4 salmon", 422, 418, 461, 451, is_salmon, 300, "salmon px")

# ---------- +ve labels ----------
count("+ve label 1", 638, 131, 672, 146, is_black, 15, "black px")
count("+ve label 2", 251, 312, 288, 327, is_black, 15, "black px")
count("+ve label 3", 494, 448, 530, 463, is_black, 15, "black px")

# ---------- axes: red shafts + red arrowheads (measured original px) ----------
axis_row = A[int(430 * S):int(442 * S), int(167 * S):int(798 * S)]
check("horizontal red axis", int(is_red(axis_row).sum()) >= 800,
      "%d red px on axis row y435-437" % int(is_red(axis_row).sum()))
axis_col = A[int(145 * S):int(443 * S), int(302 * S):int(316 * S)]
check("vertical red axis", int(is_red(axis_col).sum()) >= 800,
      "%d red px on axis column x307-312" % int(is_red(axis_col).sum()))
count("red arrowhead (right)", 655, 425, 682, 448, is_red, 40, "red px")
count("red arrowhead (top)", 302, 128, 318, 143, is_red, 40, "red px")

# ---------- boundary lines (sampled at measured on-line points) ----------
count("d1(x) red line", 370, 305, 380, 315, is_red, 8, "red px")
count("d2(x) blue line", 571, 235, 581, 245, is_blue, 8, "blue px")
count("d3(x) green line", 460, 273, 470, 283, is_green, 8, "green px")

# ---------- point clusters ----------
count("green cluster dot", 368, 158, 384, 174, is_green, 15, "green px")
count("blue cluster dot", 637, 290, 653, 306, is_blue, 15, "blue px")
count("red cluster dot", 352, 337, 368, 353, is_red, 15, "red px")

# ---------- BLOCKER: hatched class-region shading ----------
pan = A[int(120 * S):int(505 * S), int(167 * S):int(798 * S)]
area = pan.shape[0] * pan.shape[1]
gt = (pan[..., 0] > 185) & (pan[..., 0] < 250) & (pan[..., 1] > 230) & (pan[..., 2] > 185) & (pan[..., 2] < 232)
lt = (pan[..., 2] > 215) & (pan[..., 0] < 225) & (pan[..., 1] < 225) & (pan[..., 2] - pan[..., 0] > 15)
pt = (pan[..., 0] > 235) & (pan[..., 1] > 195) & (pan[..., 1] < 240) & (pan[..., 2] > 195) & (pan[..., 2] < 240) & (pan[..., 0] - pan[..., 1] > 12)
gr = (np.abs(pan[..., 0] - pan[..., 1]) < 12) & (np.abs(pan[..., 1] - pan[..., 2]) < 12) & (pan[..., 0] > 195) & (pan[..., 0] < 250)
for nm, m, thr in [("green tint", gt, 0.05), ("lavender tint", lt, 0.05),
                   ("pink tint", pt, 0.02), ("grey tint", gr, 0.02)]:
    frac = float(m.sum()) / area
    check("region %s" % nm, frac >= thr, "%.1f%% of panel >= %.0f%%" % (100 * frac, 100 * thr))
hatch = (pan[..., 0] < 225) & (pan[..., 1] < 235) & (pan.max(axis=2) - pan.min(axis=2) > 20) & (pan.min(axis=2) > 60)
hf = float(hatch.sum()) / area
check("hatch strokes visible", hf >= 0.02, "%.1f%% of panel is mid-tone hatch" % (100 * hf))

# ---------- bottom black band ----------
band2 = A[int(520 * S):int(537 * S), :]
check("bottom black band", int(is_black(band2).sum()) > band2[..., 0].size * 0.6,
      "%.0f%% black" % (100 * float(is_black(band2).sum()) / band2[..., 0].size))

bad = [n for n, ok in results if not ok]
print()
print("%d checks, %d failed" % (len(results), len(bad)))
if bad:
    print("FAILED: " + ", ".join(bad))
    sys.exit(1)
print("ALL CHECKS PASSED")
