"""Self-check for slide 042 attempt 2: PIL measurement vs the original frame.

Frame space = unique_slides/slide_042.jpg at 960x540 (1px = 1pt).
Render = qa/slide042/render_10.png at 150dpi (H/150 in); 2.0833 render-px per frame-px.
"""
import sys
from PIL import Image

RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/render_10.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_042.jpg"
S = 150 / 72.0

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
rb, ob = r.load(), o.load()
print("render", r.size, "orig", o.size, "scale", round(S, 4))


def bbox(img, x0, y0, x1, y1, pred):
    px = img.load()
    pts = [(x, y)
           for y in range(max(0, y0), min(img.size[1] - 1, y1))
           for x in range(max(0, x0), min(img.size[0] - 1, x1))
           if pred(px[x, y])]
    if not pts:
        return None
    return min(p[0] for p in pts), min(p[1] for p in pts), \
        max(p[0] for p in pts), max(p[1] for p in pts)


def fr(bb):
    return None if bb is None else tuple(round(v / S, 1) for v in bb)


def f(v):
    return int(v * S)


RED = lambda c: c[0] > 110 and c[0] - c[1] > 40 and c[0] - c[2] > 40
BLUE = lambda c: c[2] > 100 and c[2] - c[0] > 35 and c[2] - c[1] > 20
GREEN = lambda c: c[1] > 100 and c[1] - c[0] > 25 and c[1] - c[2] > 25
DARK = lambda c: (0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]) < 170
PANEL = lambda c: abs(c[0] - c[1]) < 10 and abs(c[1] - c[2]) < 10 and 215 < c[0] < 248
WHITE = lambda c: sum(c) > 740

checks = []


def chk(name, cond, detail):
    checks.append((name, cond, detail))
    print(("PASS " if cond else "FAIL ") + name + " :: " + detail)


# 1. blue box border, white interior
bb = bbox(r, f(64), f(50), f(730), f(135), BLUE)
chk("blue box border", bb is not None, str(fr(bb)))
if bb:
    g = fr(bb)
    chk("box L ~68", abs(g[0] - 68) <= 6, "%.1f" % g[0])
    chk("box T ~54", abs(g[1] - 54) <= 6, "%.1f" % g[1])
    chk("box R ~720", abs(g[2] - 720) <= 6, "%.1f" % g[2])
    chk("box B ~130", abs(g[3] - 130) <= 6, "%.1f" % g[3])
bb = bbox(r, f(200), f(60), f(600), f(126), WHITE)
chk("box interior white", bb is not None and fr(bb)[0] < 400, str(fr(bb)))
chk("original box interior white",
    bbox(o, 200, 60, 600, 126, WHITE) is not None,
    str(bbox(o, 200, 60, 600, 126, WHITE)))

# 2. TL table: caption blue, two digit bands, class row C1 red / C2 blue, red arrow
bb = bbox(r, f(85), f(60), f(215), f(76), BLUE)
chk("TL caption blue", bb is not None, str(fr(bb)))
for i, (y0, y1) in enumerate([(78, 90), (95, 106)]):
    bb = bbox(r, f(88), f(y0), f(212), f(y1), DARK)
    chk("TL band%d digits" % i, bb is not None, str(fr(bb)))
red = bbox(r, f(85), f(107), f(150), f(127), RED)
blu = bbox(r, f(150), f(107), f(215), f(127), BLUE)
chk("TL C1 red", red is not None, str(fr(red)))
chk("TL C2 blue", blu is not None, str(fr(blu)))
ar = bbox(r, f(235), f(105), f(258), f(127), RED)
chk("TL red arrow", ar is not None, str(fr(ar)))

# 3. top-centre: Initial W, matrix brackets, red Step eta
bb = bbox(r, f(260), f(70), f(330), f(90), DARK)
chk("Initial W", bb is not None and fr(bb)[0] < 280, str(fr(bb)))
bb = bbox(r, f(328), f(64), f(358), f(105), DARK)
chk("matrix brackets", bb is not None, str(fr(bb)))
bb = bbox(r, f(362), f(62), f(440), f(84), RED)
chk("Step eta red", bb is not None, str(fr(bb)))
if bb:
    g = fr(bb)
    chk("Step eta x0 ~365", abs(g[0] - 365) <= 8, "%.1f" % g[0])
    chk("Step eta y0 ~66", abs(g[1] - 66) <= 8, "%.1f" % g[1])
    chk("Step eta x1 ~435", abs(g[2] - 435) <= 10, "%.1f" % g[2])

# 4. top-right: caption, Z header, Z digits
bb = bbox(r, f(492), f(74), f(590), f(98), DARK)
chk("Check classes caption", bb is not None, str(fr(bb)))
bb = bbox(r, f(590), f(60), f(660), f(76), BLUE)
chk("Z1 Z1 Z1 header", bb is not None, str(fr(bb)))
for i, (y0, y1) in enumerate([(82, 95), (98, 109)]):
    bb = bbox(r, f(594), f(y0), f(660), f(y1), DARK)
    chk("Z band%d digits" % i, bb is not None, str(fr(bb)))

# 5. legend: black/blue/black/green/black, spans x257..508
lr = bbox(r, f(255), f(106), f(312), f(126), DARK)
lb = bbox(r, f(308), f(106), f(340), f(126), BLUE)
lg = bbox(r, f(392), f(106), f(428), f(126), GREEN)
lr2 = bbox(r, f(428), f(106), f(512), f(126), DARK)
chk("legend seg1 black", lr is not None, str(fr(lr)))
chk("legend seg2 blue C2", lb is not None, str(fr(lb)))
chk("legend seg3 green Zero", lg is not None, str(fr(lg)))
chk("legend seg4 black", lr2 is not None, str(fr(lr2)))
if lr and lg and lr2:
    chk("legend order", fr(lr)[0] < fr(lb)[0] < fr(lg)[0] < fr(lr2)[0],
        "%s %s %s %s" % (fr(lr)[0], fr(lb)[0], fr(lg)[0], fr(lr2)[0]))
rd = bbox(r, f(255), f(106), f(512), f(126), RED)
chk("legend has NO red (frame-correct)", rd is None, str(fr(rd)))
chk("original legend has no red", bbox(o, 255, 106, 512, 126, RED) is None, "ok")

# 6. LM table
bb = bbox(r, f(78), f(146), f(235), f(164), BLUE)
chk("Upgraded Vectors caption", bb is not None, str(fr(bb)))
for i, (y0, y1) in enumerate([(163, 176), (181, 193), (196, 209), (211, 224)]):
    bb = bbox(r, f(88), f(y0), f(220), f(y1), DARK)
    chk("LM band%d" % i, bb is not None, str(fr(bb)))
par = bbox(r, f(88), f(160), f(222), f(226), DARK)
chk("LM parens+digits span", par is not None, str(fr(par)))
if par:
    chk("LM paren top ~163", abs(fr(par)[1] - 163) <= 10, "%.1f" % fr(par)[1])
red = bbox(r, f(88), f(228), f(150), f(246), RED)
blu = bbox(r, f(150), f(228), f(220), f(246), BLUE)
chk("LM C1 red", red is not None, str(fr(red)))
chk("LM C2 blue", blu is not None, str(fr(blu)))

# 7. badge
red = bbox(r, f(80), f(273), f(220), f(310), RED)
chk("badge red rect", red is not None, str(fr(red)))
if red:
    g = fr(red)
    chk("badge x0 ~84", abs(g[0] - 84) <= 6, "%.1f" % g[0])
    chk("badge x1 ~214", abs(g[2] - 214) <= 6, "%.1f" % g[2])
    chk("badge y0 ~277", abs(g[1] - 277) <= 6, "%.1f" % g[1])
    chk("badge y1 ~305", abs(g[3] - 305) <= 6, "%.1f" % g[3])
wht = bbox(r, f(90), f(280), f(210), f(302), WHITE)
chk("badge white text", wht is not None, str(fr(wht)))
if wht:
    chk("badge text y ~284..298", 280 <= fr(wht)[1] <= 290 and 294 <= fr(wht)[3] <= 302,
        str(fr(wht)))
chk("original white text rows",
    bbox(o, 90, 280, 210, 302, WHITE) is not None,
    str(bbox(o, 90, 280, 210, 302, WHITE)))

# 8. right stack: white boxes + gray gaps
for i, ((y0, y1), gapy) in enumerate([
    ((228, 261), 265), ((272, 327), 332), ((338, 393), 398),
    ((404, 459), 464), ((470, 527), 532),
]):
    bb = bbox(r, f(280), f(y0 + 2), f(896), f(y1 - 2), WHITE)
    chk("box%d white" % i, bb is not None, str(fr(bb)))
    if bb:
        g = fr(bb)
        chk("box%d left ~276" % i, abs(g[0] - 276) <= 8, "%.1f" % g[0])
        chk("box%d right ~898" % i, abs(g[2] - 898) <= 8, "%.1f" % g[2])
        chk("box%d span y %d..%d" % (i, y0, y1),
            g[1] >= y0 - 4 and g[3] <= y1 + 4, "%.1f..%.1f" % (g[1], g[3]))
    gp = bbox(r, f(280), f(gapy - 2), f(896), f(gapy + 2), PANEL)
    chk("gap%d panel" % i, gp is not None, str(fr(gp)))
    drk = bbox(r, f(280), f(gapy - 2), f(896), f(gapy + 2), DARK)
    chk("gap%d no black rule" % i, drk is None, str(fr(drk)))
chk("original gaps are panel not black",
    bbox(o, 280, 263, 896, 269, DARK) is None, "ok")

# 9. green marks
gg = bbox(r, f(380), f(225), f(760), f(515), GREEN)
chk("green marks present", gg is not None, str(fr(gg)))
if gg:
    g = fr(gg)
    chk("green left ~384", abs(g[0] - 384) <= 10, "%.1f" % g[0])
    chk("green right ~748", abs(g[2] - 748) <= 10, "%.1f" % g[2])
chk("original green present", bbox(o, 380, 225, 760, 515, GREEN) is not None, "ok")

# 10. red Update Weight (2 occurrences)
rr = bbox(r, f(590), f(225), f(720), f(515), RED)
chk("red Update Weight", rr is not None, str(fr(rr)))
cnt = 0
px = r.load()
for y in range(f(225), f(515)):
    row = [x for x in range(f(590), f(720)) if RED(px[x, y])]
    if len(row) > 3:
        cnt += 1
chk("red rows span 2 boxes (>60px)", cnt > 60, "rows=%d" % cnt)

bad = [c for c in checks if not c[1]]
print("\n%d/%d checks passed" % (len(checks) - len(bad), len(checks)))
sys.exit(1 if bad else 0)
