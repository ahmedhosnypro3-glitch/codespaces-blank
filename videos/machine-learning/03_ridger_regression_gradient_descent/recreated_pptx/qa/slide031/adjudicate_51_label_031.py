# Exact numeric adjudication of the "(5,1)" label in ORIGINAL vs CURRENT render.
# 1) raw RGB of the region to settle what the weak-green cast is
# 2) ink = pixels distinguishable from the local background, clustered into
#    glyph groups with bboxes, for each image independently.
import numpy as np
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide031"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
R = np.asarray(Image.open(QA + "/render_cur.png").convert("RGB")).astype(int)
SX = 2001 / 960.0

print("=== ORIGINAL raw RGB samples (x,y) ===")
for (x, y) in [(490, 255), (500, 255), (510, 255), (520, 255), (525, 255), (530, 255),
               (534, 255), (537, 255), (540, 255), (545, 255), (550, 255), (555, 255),
               (500, 248), (500, 262), (300, 255), (450, 255)]:
    print("   (%3d,%3d) = %s" % (x, y, tuple(O[y, x])))

print("\n=== ORIGINAL green-cast map: mean G-R over x 470..570, rows 244..264 ===")
for y in range(244, 265):
    row = []
    for x in range(470, 571, 5):
        p = O[y, x]
        row.append("G" if (p[1] > p[0] + 8 and p[1] > p[2] + 8) else
                   ("R" if (p[0] > p[1] + 25 and p[0] > p[2] + 25) else
                    ("D" if max(p) < 170 else ".")))
    print("   y%3d %s" % (y, "".join(row)))
print("   x ruler:   " + "".join(str((470 + i * 5) // 10 % 10) for i in range(21)))
print("               " + "".join(str((470 + i * 5) % 10) for i in range(21)))


def ink_groups(tag, a, x0, x1, y0, y1, sc, bgtest):
    print("\n=== %s glyph groups x%d..%d y%d..%d ===" % (tag, x0, x1, y0, y1))
    pts = []
    for fy in range(y0, y1):
        for fx in range(x0, x1):
            yy, xx = int(round(fy * sc)), int(round(fx * sc))
            if bgtest(a[yy, xx]):
                pts.append((fx, fy))
    if not pts:
        print("   no ink")
        return
    # cluster by x gaps > 2px
    cols = sorted(set(p[0] for p in pts))
    groups, cur = [], [cols[0]]
    for c in cols[1:]:
        if c - cur[-1] > 2:
            groups.append(cur); cur = [c]
        else:
            cur.append(c)
    groups.append(cur)
    for g in groups:
        gp = [p for p in pts if p[0] in g]
        ys = [p[1] for p in gp]
        print("   x %d..%d  y %d..%d  n=%d" % (min(g), max(g), min(ys), max(ys), len(gp)))


# ORIGINAL ink = not the weak-green cast and not near-white: dark glyphs OR red glyphs
def o_ink(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if max(p) < 170:
        return True
    if r > g + 25 and r > b + 25:
        return True
    return False


def r_ink(p):
    r, g, b = int(p[0]), int(p[1]), int(p[2])
    if max(p) < 210:
        return True
    if r > g + 25 and r > b + 25:
        return True
    return False


ink_groups("ORIGINAL", O, 470, 575, 247, 264, 1.0, o_ink)
ink_groups("RENDER", R, 470, 575, 247, 264, SX, r_ink)

print("\n=== does the ORIGINAL contain ANY ink at x 490..525, y 246..264? ===")
n = 0
for y in range(246, 265):
    for x in range(490, 526):
        p = O[y, x]
        if max(p) < 170 or (p[0] > p[1] + 25 and p[0] > p[2] + 25):
            n += 1
            if n < 12:
                print("   (%d,%d) %s" % (x, y, tuple(p)))
print("   count =", n)

print("\n=== RENDER ink at x 490..525, y 246..264 ===")
n = 0
for y in range(int(246 * SX), int(264 * SX)):
    for x in range(int(490 * SX), int(526 * SX)):
        p = R[y, x]
        if max(p) < 210:
            n += 1
print("   count =", n)
