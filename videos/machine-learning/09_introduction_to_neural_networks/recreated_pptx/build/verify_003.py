"""Closed-loop check of the recreated slide 003 against the original frame.

Compares ink geometry in the original's 960x540 coordinate space (1px = 1pt)
between unique_slides/slide_003.jpg and the LibreOffice render, and asserts the
house-frame chrome. Every expectation below was measured with PIL on the
original frame; tolerances are in original pixels.
"""
import sys
from PIL import Image
import numpy as np

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
ORIG = V + "/unique_slides/slide_003.jpg"
REND = V + "/recreated_pptx/build/slide_003_rejudge_rendered-1.png"
TOL = 4

orig = Image.open(ORIG).convert("RGB")
rend = Image.open(REND).convert("RGB")
r = rend.resize((960, 540), Image.LANCZOS)


def arr(im):
    return np.asarray(im).astype(np.int16)


def ink_mask(im, thr=200):
    a = arr(im)
    return a.min(axis=2) < thr


def bbox(mask, x0, x1, y0, y1):
    sub = mask[y0:y1, x0:x1]
    ys, xs = np.nonzero(sub)
    if not len(xs):
        return None
    return (int(xs.min()) + x0, int(xs.max()) + x0,
            int(ys.min()) + y0, int(ys.max()) + y0)


def rows_with_ink(mask, x0, x1, y0, y1, min_frac=0.25):
    out = []
    span = x1 - x0
    for y in range(y0, y1):
        if mask[y, x0:x1].sum() >= min_frac * span:
            out.append(y)
    return out


def groups(vals, gap=2):
    if not vals:
        return []
    out = [[vals[0], vals[0]]]
    for v in vals[1:]:
        if v - out[-1][1] <= gap:
            out[-1][1] = v
        else:
            out.append([v, v])
    return [tuple(g) for g in out]


def color_of(im, x0, x1, y0, y1):
    """dominant saturated hue of the ink in a box: R / G / B / K"""
    a = arr(im)[y0:y1, x0:x1]
    m = a.min(axis=2) < 200
    if not m.any():
        return "."
    px = a[m]
    r, g, b = px[:, 0].astype(int), px[:, 1].astype(int), px[:, 2].astype(int)
    red = ((r - g > 50) & (r - b > 35)).sum()
    grn = ((g - r > 35) & (g - b > 35)).sum()
    blu = ((b - r > 35) & (b - g > 35)).sum()
    best = max((red, "R"), (grn, "G"), (blu, "B"))
    if best[0] < max(3, 0.12 * len(px)):
        return "K"
    return best[1]


om, rm = ink_mask(orig), ink_mask(r)
fails = []
lines = []


def check(label, expected, got, tol=TOL):
    if expected is None or got is None:
        ok = False
        delta = "-"
    elif isinstance(expected, (tuple, list)) and isinstance(got, (tuple, list)):
        deltas = [g - e for e, g in zip(expected, got)]
        ok = all(abs(d) <= tol for d in deltas)
        delta = ",".join("%+d" % d for d in deltas)
    else:
        delta = got - expected
        ok = abs(delta) <= tol
    lines.append("%-46s exp=%-22s got=%-22s d=%-12s %s"
                 % (label, expected, got, delta, "PASS" if ok else "FAIL"))
    if not ok:
        fails.append(label)
    return ok


print("original %dx%d   render %dx%d (resampled to 960x540)" %
      (orig.size[0], orig.size[1], rend.size[0], rend.size[1]))
print("-" * 118)

# ---- house frame chrome (house rule wins over the original) ----------------
fr = [(10, 12), (947, 950)]
for i, (y0, y1) in enumerate(fr):
    exp = [10, 949] if i == 0 else [10, 529]
    got = bbox(rm, 0, 960, y0, y1)
    got = (got[0], got[1], got[2], got[3]) if got else None
    lines.append("%-46s exp=house-red-frame        got=%-22s        %s"
                 % ("house red frame row %d" % i, got, "PASS" if got else "FAIL"))
    if not got:
        fails.append("house frame row %d" % i)
for i, (x0, x1) in enumerate([(8, 13), (946, 952)]):
    got = bbox(rm, x0, x1, 0, 540)
    ok = got is not None
    lines.append("%-46s exp=house-red-frame-col    got=%-22s        %s"
                 % ("house red frame col %d" % i, got, "PASS" if ok else "FAIL"))
    if not ok:
        fails.append("house frame col %d" % i)
bb = bbox(rm, 880, 960, 10, 70)
check("house badge oval bbox (898..934, 21..57)", (898, 934, 21, 57), bb, 6)
bi = bbox(rm, 905, 930, 28, 52)
check("house badge numeral ink bbox", (909, 924, 32, 49), bi, 8)

# ---- panel borders --------------------------------------------------------
for label, rows in [("p1", (89, 91)), ("p1", (203, 205)), ("p2", (216, 218)),
                    ("p2", (300, 302)), ("p3", (314, 316)), ("p3", (403, 405)),
                    ("p4", (418, 419)), ("p4", (502, 504))]:
    y0, y1 = rows
    exp = (y0 + y1) / 2.0
    got = rows_with_ink(rm, 70, 870, y0 - 4, y1 + 5)
    g = (got[0] + got[-1]) / 2.0 if got else None
    check("panel %s border row %d-%d" % (label, y0, y1), exp, g, 3)
for label, x0 in [("left", 67), ("right", 869)]:
    got = [x for x in range(x0 - 4, x0 + 8)
           if rm[95:500, x].sum() > 0.5 * (500 - 95)]
    g = (got[0] + got[-1]) / 2.0 if got else None
    check("panel %s vertical border near %d" % (label, x0), x0 + 1, g, 3)

# ---- body baselines (ink bottom of each line's leading capital) -----------
LEAD = [("p1 L1 'D'", (79, 90), 92, 116, 111), ("p1 L2 'l'", (79, 88), 116, 146, 138),
        ("p1 L3 'X'", (99, 113), 144, 175, 165), ("p1 L4 'X'", (99, 113), 172, 203, 193),
        ("p2 L1 'F'", (79, 90), 217, 243, 235), ("p2 L2 'I'", (79, 88), 243, 270, 263),
        ("p2 L3 'I'", (79, 88), 270, 297, 290), ("p3 hdr 'D'", (79, 90), 318, 344, 338),
        ("p4 L1 'D'", (79, 90), 420, 446, 437), ("p4 L2 'I'", (79, 88), 446, 470, 464),
        ("p4 L3 'I'", (79, 88), 470, 497, 489)]
for label, (x0, x1), y0, y1, base in LEAD:
    got = bbox(rm, x0, x1, y0, y1)
    check("baseline %s" % label, base, got[3] if got else None, 4)

# ---- body cap height ------------------------------------------------------
got = bbox(rm, 79, 90, 92, 116)
exp = bbox(om, 79, 90, 92, 116)
check("p1 'D' cap height", exp[3] - exp[2] + 1,
      got[3] - got[2] + 1 if got else None, 3)

# ---- text left edge -------------------------------------------------------
for label, (x0, x1), y0, y1 in [("p1 L1", (75, 200), 92, 116), ("p2 L1", (75, 200), 217, 243),
                                ("p3 hdr", (75, 310), 318, 344), ("p4 L1", (75, 200), 420, 446)]:
    b = bbox(rm, x0, x1, y0, y1)
    check("text left edge %s" % label, 79, b[0] if b else None, 3)

# ---- underlines -----------------------------------------------------------
def underline_row(mask, x0, x1, y0, y1, min_run=0.6):
    for y in range(y0, y1):
        row = mask[y, x0:x1]
        best = cur = 0
        for v in row:
            cur = cur + 1 if v else 0
            best = max(best, cur)
        if best >= min_run * (x1 - x0):
            return y
    return None


for label, x0, x1, y0, y1, exp in [
        ("p1 L3 X underline", 99, 114, 163, 174, 168),
        ("p1 L4 X underline", 99, 114, 190, 201, 196),
        ("p3 header underline", 79, 305, 336, 346, 340),
        ("p4 'Define' underline", 79, 136, 434, 444, 438),
        ("p4 'as :' NOT underlined", 163, 186, 434, 446, None)]:
    got = underline_row(rm, x0, x1, y0, y1)
    if exp is None:
        ok = got is None
        lines.append("%-46s exp=no-rule                 got=%-22s        %s"
                     % (label, got, "PASS" if ok else "FAIL"))
        if not ok:
            fails.append(label)
    else:
        check(label, exp, got, 3)

# ---- equation strip -------------------------------------------------------
eq = bbox(rm, 75, 740, 345, 400)
check("equation strip ink bbox x0,x1", (84, 733), (eq[0], eq[1]) if eq else None, 6)
check("equation strip ink bbox y0,y1", (354, 396), (eq[2], eq[3]) if eq else None, 6)
sig = bbox(rm, 200, 260, 345, 385)
check("sigma ink bbox x0,x1", (219, 240), (sig[0], sig[1]) if sig else None, 8)
lim = bbox(rm, 150, 310, 382, 400)
check("sigma limits band bbox x0,x1", (162, 298), (lim[0], lim[1]) if lim else None, 12)
check("sigma limits band bbox y0,y1", (384, 396), (lim[2], lim[3]) if lim else None, 6)
rx = bbox(rm, 740, 810, 340, 390)
check("trailing red X bbox x0,x1", (762, 786), (rx[0], rx[1]) if rx else None, 8)
check("trailing red X bbox y0,y1", (352, 374), (rx[2], rx[3]) if rx else None, 8)
check("trailing X colour", "R", color_of(r, *rx) if rx else None, 0)
# limit word colours: "misclassified" red, "vectors" black
mc = bbox(rm, 175, 248, 382, 400)
check("limit word 'misclassified' colour", "R", color_of(r, *mc) if mc else None, 0)
vec = bbox(rm, 250, 282, 382, 400)
check("limit word 'vectors' colour", "K", color_of(r, *vec) if vec else None, 0)
grn = bbox(rm, 330, 360, 355, 378)
check("X_i colour", "G", color_of(r, *grn) if grn else None, 0)

# ---- word colours in the body text ---------------------------------------
COLORS = [("class I (p1 L1)", (210, 245), 94, 112, "R"),
          ("Class II (p1 L1)", (258, 300), 94, 112, "B"),
          ("misclassified (p2 L1)", (86, 175), 218, 242, "K"),
          ("class I (p2 L2)", (127, 160), 246, 266, "R"),
          ("Class II (p2 L2)", (300, 340), 246, 266, "B"),
          ("class I (p2 L3)", (127, 160), 273, 293, "R"),
          ("Class II (p2 L3)", (285, 325), 273, 293, "B"),
          ("<0 (p2 L2)", (620, 650), 246, 266, "R"),
          (">0 (p2 L3)", (610, 645), 273, 293, "B"),
          ("<0 (p4 L2)", (455, 485), 447, 468, "R"),
          (">0 (p4 L3)", (450, 480), 472, 494, "B"),
          ("delta (p4 L1)", (140, 155), 420, 444, "G")]
for label, (x0, x1), y0, y1, exp in COLORS:
    got = color_of(r, x0, x1, y0, y1)
    ok = got == exp
    lines.append("%-46s exp=%-22s got=%-22s d=%-12s %s"
                 % (label, exp, got, "-", "PASS" if ok else "FAIL"))
    if not ok:
        fails.append(label)

# ---- no ink crossing any panel border ------------------------------------
for label, rows in [("p1", (89, 91)), ("p1", (203, 205)), ("p2", (216, 218)),
                    ("p2", (300, 302)), ("p3", (314, 316)), ("p3", (403, 405)),
                    ("p4", (418, 419)), ("p4", (502, 504))]:
    y0, y1 = rows
    inside = rm[y0 + 2:y1 - 1, 75:865]
    # count ink columns that also carry ink well above/below the border
    above = rm[y0 - 6:y0 - 2, 75:865].sum(axis=0) > 0
    below = rm[y1 + 2:y1 + 6, 75:865].sum(axis=0) > 0
    cross = int((above & below).sum())
    ok = cross < 12
    lines.append("%-46s exp=<12 crossing cols       got=%-22s d=%-12s %s"
                 % ("no text crossing %s border %d" % (label, y0), cross, "-",
                    "PASS" if ok else "FAIL"))
    if not ok:
        fails.append("crossing %s border %d" % (label, y0))

print("\n".join(lines))
print("-" * 118)
print("checks failed: %d" % len(fails))
for f in fails:
    print("  FAIL:", f)
sys.exit(1 if fails else 0)
