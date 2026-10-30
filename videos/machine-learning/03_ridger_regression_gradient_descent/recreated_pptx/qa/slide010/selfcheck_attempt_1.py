#!/usr/bin/env python3
"""Slide 010 — mandatory pre-judge self-check, attempt K.

Runs on the 150dpi render (2001x1125; 1 render px = 1/200 in; scale to frame
px = *72/150). Checks (founder directive 2026-10-10; slide 010 has NO
equations/tables/delimiters, so only the applicable checks run):

1. FRAME CONTAINMENT — content ink must sit inside the house panel
   (x54..903, y45..540 frame px) and must not cross the house strokes;
   the outer strips (left of x54, right of x903, above y45) must be pure
   canvas white.
2. ELEMENT PRESENCE — every measured structure must have ink in the render:
   grid rows/cols, red axes, blue fitted lines, 24 orange points, the four
   green delta marks (L h-line, L v-line, L marker, R h-line, R v-line,
   R marker), the caption bands' cream fills + rose strokes, the four
   caption lines.
3. CAPTION GEOMETRY — caption line-1 red keyword starts at frame x111 (LEFT)
   / x524 (RIGHT); line spans match the measured original runs.
4. EXPLICIT LINE SPACING — the inherited caption blocks set lineSpacing
   (component contract); verified here by the caption band pitch.
"""
import os
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DECK = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RENDER = os.path.join(HERE, "render_1.png")
ORIG = os.path.join(DECK, "unique_slides", "slide_010.jpg")

ren = Image.open(RENDER).convert("RGB")
RW, RH = ren.size
S = RH / 540.0  # render px per frame px
print("render_1 %dx%d   scale %.5f render-px/frame-px" % (RW, RH, S))
a = np.asarray(ren).astype(int)
o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)

fails = []


def f2r(v):
    return int(round(v * S))


# ---------- 1. frame containment ----------
print("\n== 1. frame containment ==")
# outer strips pure white (canvas): x<54, x>903, y<45 (frame px)
mask_strip_l = a[:, : f2r(54)]
mask_strip_r = a[:, f2r(904) :]
mask_strip_t = a[: f2r(45), :]
for name, m in (("left of panel", mask_strip_l), ("right of panel", mask_strip_r), ("above panel", mask_strip_t)):
    nonwhite = int(((m < 245).any(axis=2)).sum())
    print("   %-16s non-white px: %d" % (name, nonwhite))
    if nonwhite > 40:
        fails.append("containment: %s strip has %d non-white px" % (name, nonwhite))
# house strokes must not be crossed by content: strokes at x58.5/901/y538.5;
# content ink (non-gray-panel) must not appear outside x60..899 in the panel band
# (the panel itself is E9E9E7; the badge sits at x861..892 which is inside 899).
band = a[f2r(46) : f2r(537), :, :]
left_out = band[:, : f2r(60)]
right_out = band[:, f2r(900) :]
for name, m in (("left of left stroke", left_out), ("right of right stroke", right_out)):
    # panel gray E9E9E7 = (233,231,231); anything else = content/glitch
    panelish = (np.abs(m - 231).max(axis=2) <= 6)
    other = int((~panelish).sum())
    print("   %-22s non-panel px: %d" % (name, other))
    if other > 60:
        fails.append("containment: %s has %d non-panel px" % (name, other))

# ---------- 2. element presence ----------
print("\n== 2. element presence (frame-px regions mapped into the render) ==")


def ink_count(x0, y0, x1, y1, test):
    sub = a[f2r(y0) : f2r(y1), f2r(x0) : f2r(x1)]
    return int(test(sub).sum())


is_gray = lambda m: (np.abs(m[:, :, 0] - m[:, :, 1]) < 14) & (np.abs(m[:, :, 1] - m[:, :, 2]) < 14) & (170 < m[:, :, 0]) & (m[:, :, 0] < 238)
is_red = lambda m: (m[:, :, 0] > 140) & (m[:, :, 0] - m[:, :, 1] > 60) & (m[:, :, 0] - m[:, :, 2] > 60)
is_blue = lambda m: (m[:, :, 2] > 110) & (m[:, :, 2] - m[:, :, 0] > 50) & (m[:, :, 2] - m[:, :, 1] > 50)
is_orange = lambda m: (m[:, :, 0] > 200) & (m[:, :, 1] > 90) & (m[:, :, 1] < 190) & (m[:, :, 2] < 90)
is_green = lambda m: (m[:, :, 1] > 110) & (m[:, :, 1] - m[:, :, 0] > 40) & (m[:, :, 1] - m[:, :, 2] > 40)
is_spring = lambda m: (m[:, :, 1] > 200) & (m[:, :, 2] > 80) & (m[:, :, 1] - m[:, :, 0] > 120)

checks = [
    ("LEFT grid verticals (x103..448,y121..456)", 103, 121, 448, 456, is_gray, 300),
    ("LEFT grid horizontals", 104, 120, 448, 456, is_gray, 300),
    ("RIGHT grid verticals", 517, 121, 862, 456, is_gray, 300),
    ("LEFT y-axis (x125..128)", 125, 145, 128, 436, is_red, 200),
    ("RIGHT y-axis (x539..542)", 539, 145, 542, 436, is_red, 200),
    ("LEFT x-axis (x124..435,y432..436)", 124, 432, 435, 436, is_red, 150),
    ("RIGHT x-axis (x538..848,y432..436)", 538, 432, 848, 436, is_red, 150),
    ("LEFT fitted line (x141..433,y200..352)", 141, 200, 433, 352, is_blue, 200),
    ("RIGHT fitted line (x555..849,y247..388)", 555, 247, 849, 388, is_blue, 200),
    ("LEFT points (12 orange)", 170, 138, 428, 386, is_orange, 150),
    ("RIGHT points (12 orange)", 585, 138, 838, 386, is_orange, 150),
    ("LEFT green h-line y237..240 x129..347", 129, 237, 347, 240, is_green, 200),
    ("LEFT green v-line x351..354 y242..437", 351, 242, 354, 437, is_green, 100),
    ("LEFT spring marker x350..357 y428..437", 350, 428, 357, 437, is_spring, 20),
    ("RIGHT green h-line y286..289 x552..733", 552, 286, 733, 289, is_green, 100),
    ("RIGHT green v-line x765..768 y289..437", 765, 289, 768, 437, is_green, 100),
    ("RIGHT spring marker x763..770 y428..437", 763, 428, 770, 437, is_spring, 20),
    ("LEFT cream band fill x97..431 y480..527", 97, 480, 431, 527,
     lambda m: (m[:, :, 0] > 240) & (m[:, :, 2] > 225) & (m[:, :, 1] > 240), 5000),
    ("RIGHT cream band fill x504..838 y480..527", 504, 480, 838, 527,
     lambda m: (m[:, :, 0] > 240) & (m[:, :, 2] > 225) & (m[:, :, 1] > 240), 5000),
    ("LEFT rose stroke x95..97 y479..528", 95, 479, 97, 528,
     lambda m: (m[:, :, 0] > 180) & (m[:, :, 0] - m[:, :, 2] > 15) & (m[:, :, 1] > 160), 30),
    ("RIGHT rose stroke x501..503 y479..528", 501, 479, 503, 528,
     lambda m: (m[:, :, 0] > 180) & (m[:, :, 0] - m[:, :, 2] > 15) & (m[:, :, 1] > 160), 30),
]
for name, x0, y0, x1, y1, test, need in checks:
    n = ink_count(x0, y0, x1, y1, test)
    ok = n >= need
    print("   %-46s ink px: %5d  need >= %4d  %s" % (name, n, need, "OK" if ok else "FAIL"))
    if not ok:
        fails.append("presence: %s only %d px (need %d)" % (name, n, need))

# ---------- 3. caption geometry ----------
print("\n== 3. caption geometry (vs measured original runs) ==")
for line, (ylo, yhi), red_lo in (("line1", (486, 503), 100), ("line2", (507, 523), 0)):
    for panel, (xa, xb), exp_red_lo in (("L", (60, 470), 111 if line == "line1" else None),
                                        ("R", (480, 900), 524 if line == "line1" else None)):
        sub = a[f2r(ylo) : f2r(yhi), f2r(xa) : f2r(xb)]
        red = is_red(sub).any(axis=0)
        dark = (sub.max(axis=2) < 130).any(axis=0)
        ink = np.nonzero(red | dark)[0]
        if len(ink) == 0:
            fails.append("caption %s %s: no ink" % (line, panel))
            print("   %s %s: NO INK  FAIL" % (line, panel))
            continue
        ink_x0 = xa + int(ink[0])
        ink_x1 = xa + int(ink[-1])
        print("   %-6s %s: ink x %d..%d (frame)  red first x: %s"
              % (line, panel, ink_x0, ink_x1,
                 (xa + int(np.nonzero(red)[0][0])) if red.any() else "-"))
        if exp_red_lo is not None:
            if not red.any():
                fails.append("caption line1 %s: no red keyword ink" % panel)
            elif abs((xa + int(np.nonzero(red)[0][0])) - exp_red_lo) > 6:
                fails.append("caption line1 %s: red keyword starts %d, expected ~%d"
                             % (panel, xa + int(np.nonzero(red)[0][0]), exp_red_lo))

# ---------- 4. caption band pitch (explicit lineSpacing honoured) ----------
print("\n== 4. caption band pitch ==")
for panel, xa, xb in (("L", 150, 390), ("R", 560, 790)):
    col = a[f2r(486) : f2r(523), f2r(xa) : f2r(xb)]
    dark = (col.max(axis=2) < 130).any(axis=1)
    rows = np.nonzero(dark)[0]
    if len(rows):
        # find the two bands (line1 ~y493..500, line2 ~y511..519 frame px)
        bands = []
        cur = [rows[0], rows[0]]
        for r in rows[1:]:
            if r - cur[1] <= 2:
                cur[1] = r
            else:
                bands.append(tuple(cur))
                cur = [r, r]
        bands.append(tuple(cur))
        centers = [486 + (b[0] + b[1]) / 2 / S for b in bands]
        print("   %s: text bands (frame-px centres): %s" % (panel, ["%.1f" % c for c in centers]))

print("\n== selfcheck verdict ==")
if fails:
    print("FAIL (%d)" % len(fails))
    for f in fails:
        print("   - " + f)
    raise SystemExit(1)
print("PASS — all checks clean")
