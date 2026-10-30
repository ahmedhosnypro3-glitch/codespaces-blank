"""Self-check for slide 042 attempt 1: PIL measurement vs the original frame.

Frame space = original unique_slides/slide_042.jpg at 960x540 (1px = 1pt).
Render = qa/slide042/render_1.png at 150dpi (2.0833 render-px per frame-px).
"""
import sys
from PIL import Image

RENDER = "videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide042/render_1.png"
ORIG = "videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_042.jpg"
S = 150 / 72.0  # render px per frame px

r = Image.open(RENDER).convert("RGB")
o = Image.open(ORIG).convert("RGB")
print("render", r.size, "orig", o.size, "scale", round(S, 4))

rb, ob = r.load(), o.load()


def ink_bbox(img, x0, y0, x1, y1, thresh=140):
    """Bbox of dark ink in a frame-space box, returned in frame px."""
    px = img.load()
    pts = [(x, y)
           for y in range(max(0, y0), min(img.size[1] - 1, y1))
           for x in range(max(0, x0), min(img.size[0] - 1, x1))
           if (0.299 * px[x, y][0] + 0.587 * px[x, y][1] + 0.114 * px[x, y][2]) < thresh]
    if not pts:
        return None
    return min(p[0] for p in pts), min(p[1] for p in pts), \
        max(p[0] for p in pts), max(p[1] for p in pts)


def color_bbox(img, x0, y0, x1, y1, kind):
    """Bbox of colour-family ink in a frame-space box, in frame px."""
    px = img.load()
    pts = []
    for y in range(max(0, y0), min(img.size[1] - 1, y1)):
        for x in range(max(0, x0), min(img.size[0] - 1, x1)):
            R, G, B = px[x, y]
            if kind == "red" and R > 120 and R - G > 60 and R - B > 60:
                pts.append((x, y))
            elif kind == "blue" and B > 100 and B - R > 40 and B - G > 30:
                pts.append((x, y))
            elif kind == "green" and G > 90 and G - R > 40 and G - B > 40:
                pts.append((x, y))
            elif kind == "black" and R < 90 and G < 90 and B < 90:
                pts.append((x, y))
    if not pts:
        return None
    return min(p[0] for p in pts), min(p[1] for p in pts), \
        max(p[0] for p in pts), max(p[1] for p in pts)


def f(v):
    return int(v * S)


def done(bb):
    return None if bb is None else tuple(round(v / S, 1) for v in bb)


checks = []


def chk(name, cond, detail):
    checks.append((name, cond, detail))
    print(("PASS " if cond else "FAIL ") + name + " :: " + detail)


# --- 1. top-left vector table ---
for label, ytop, ybot in [("TL dig band1", 80, 93), ("TL dig band2", 93, 106)]:
    bb = ink_bbox(r, f(85), f(ytop), f(258), f(ybot))
    chk(label, bb is not None, "render %s" % (done(bb),))

bb = color_bbox(r, f(85), f(62), f(258), f(78), "blue")
chk("TL caption blue", bb is not None, str(done(bb)))
if bb:
    g = done(bb)
    chk("TL caption x-extent", 85 <= g[0] <= 95 and 205 <= g[2] <= 215, str(g))

red = color_bbox(r, f(85), f(108), f(160), f(127), "red")
blu = color_bbox(r, f(160), f(108), f(215), f(127), "blue")
chk("TL class C1 red", red is not None, str(done(red)))
chk("TL class C2 blue", blu is not None, str(done(blu)))
chk("TL C1 left of C2", red and blu and done(red)[0] < done(blu)[0],
    "%s vs %s" % (done(red), done(blu)))

red = color_bbox(r, f(230), f(108), f(260), f(127), "red")
chk("TL red arrow right of classes", red is not None, str(done(red)))

# --- 2. blue-bordered box ---
bb = color_bbox(r, f(64), f(50), f(730), f(135), "blue")
chk("blue box ink present", bb is not None, str(done(bb)))
if bb:
    g = done(bb)
    chk("blue box left ~68", abs(g[0] - 68) <= 8, "x0=%.1f" % g[0])
    chk("blue box top ~54", abs(g[1] - 54) <= 8, "y0=%.1f" % g[1])
    chk("blue box right ~720", abs(g[2] - 720) <= 8, "x1=%.1f" % g[2])
    chk("blue box bottom ~130", abs(g[3] - 130) <= 8, "y1=%.1f" % g[3])

# --- 3. top-centre ---
bb = color_bbox(r, f(260), f(60), f(440), f(100), "black")
chk("Initial W black ink", bb is not None, str(done(bb)))
if bb:
    chk("Initial W x0 ~266", abs(done(bb)[0] - 266) <= 10, "x0=%.1f" % done(bb)[0])
red = color_bbox(r, f(355), f(60), f(440), f(100), "red")
chk("Step eta red italic", red is not None, str(done(red)))
grn = color_bbox(r, f(385), f(105), f(430), f(128), "green")
chk("green Zero", grn is not None, str(done(grn)))

# --- 4. top-right check classes + legend ---
bb = color_bbox(r, f(495), f(74), f(600), f(98), "black")
chk("Check classes caption", bb is not None, str(done(bb)))
bb = color_bbox(r, f(575), f(60), f(670), f(75), "blue")
chk("Z1 Z1 Z1 header blue", bb is not None, str(done(bb)))
bb = color_bbox(r, f(590), f(78), f(665), f(115), "black")
chk("Z matrix digits", bb is not None, str(done(bb)))
if bb:
    chk("Z matrix x0 ~597", abs(done(bb)[0] - 597) <= 12, "x0=%.1f" % done(bb)[0])
    chk("Z matrix x1 ~655", abs(done(bb)[2] - 655) <= 14, "x1=%.1f" % done(bb)[2])

lr = color_bbox(r, f(250), f(108), f(700), f(127), "red")
lg = color_bbox(r, f(250), f(108), f(700), f(127), "green")
lb = color_bbox(r, f(250), f(108), f(700), f(127), "blue")
chk("legend red term", lr is not None, str(done(lr)))
chk("legend green term", lg is not None, str(done(lg)))
chk("legend blue term", lb is not None, str(done(lb)))
if lr and lg:
    chk("legend order C1<Zero", done(lr)[0] < done(lg)[0],
        "%s < %s" % (done(lr)[0], done(lg)[0]))

# --- 5. left-middle upgraded vectors ---
bb = color_bbox(r, f(78), f(146), f(235), f(164), "blue")
chk("Upgraded Vectors caption blue", bb is not None, str(done(bb)))
for i, (ytop, ybot) in enumerate([(164, 181), (181, 198), (198, 215)]):
    bb = ink_bbox(r, f(88), f(ytop), f(225), f(ybot))
    chk("LM row%d digits" % i, bb is not None, str(done(bb)))
red = color_bbox(r, f(88), f(226), f(150), f(245), "red")
blu = color_bbox(r, f(150), f(226), f(225), f(245), "blue")
chk("LM class C1 red", red is not None, str(done(red)))
chk("LM class C2 blue", blu is not None, str(done(blu)))

# --- 6. iteration badge ---
red = color_bbox(r, f(50), f(258), f(205), f(305), "red")
chk("Iteration badge red rect", red is not None, str(done(red)))
if red:
    g = done(red)
    chk("badge x0 ~54", abs(g[0] - 54) <= 10, "x0=%.1f" % g[0])
    chk("badge x1 ~200", abs(g[2] - 200) <= 10, "x1=%.1f" % g[2])
    chk("badge y0 ~263", abs(g[1] - 263) <= 10, "y0=%.1f" % g[1])
    chk("badge y1 ~300", abs(g[3] - 300) <= 10, "y1=%.1f" % g[3])
wht = sum(1 for y in range(f(264), f(300)) for x in range(f(60), f(195))
          if sum(rb[x, y]) > 690)
chk("badge white text present", wht > 200, "white px=%d" % wht)

# --- 7. right computation stack ---
for y in [263, 272, 338, 395, 404, 461, 470]:
    bb = ink_bbox(r, f(380), f(y - 2), f(854), f(y + 2))
    chk("rule y=%d" % y, bb is not None and abs(done(bb)[1] - y) <= 4, str(done(bb)))

gg = color_bbox(r, f(380), f(225), f(860), f(515), "green")
chk("green arrows present", gg is not None, str(done(gg)))

rr = color_bbox(r, f(495), f(225), f(620), f(515), "red")
chk("red Update Weight actions", rr is not None, str(done(rr)))

# --- 8. original cross-check: same bands hold ink in the original ---
orig_ok = all([
    ink_bbox(o, 85, 80, 258, 106) is not None,
    color_bbox(o, 85, 62, 258, 78, "blue") is not None,
    color_bbox(o, 85, 108, 160, 127, "red") is not None,
    color_bbox(o, 50, 258, 205, 305, "red") is not None,
    ink_bbox(o, 380, 225, 854, 515) is not None,
])
chk("original bands have ink at same coords", orig_ok, "measured above")

bad = [c for c in checks if not c[1]]
print("\n%d/%d checks passed" % (len(checks) - len(bad), len(checks)))
sys.exit(1 if bad else 0)
