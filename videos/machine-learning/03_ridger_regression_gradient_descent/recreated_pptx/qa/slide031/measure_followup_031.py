# Targeted follow-up measurements for slide 031.
# Questions:
#  1. Exact colour/row of the original's x-axis line (is it black at y265/266?)
#  2. Exact colour/row of the original's plot-box bottom border (y308..311)
#  3. Plot-box left/right vertical borders exact columns and colours
#  4. Census of RED dashed lines inside the original plot interior
#  5. Fine ASCII map of the original's green vertex marker region
#  6. Annotation interior fill samples far from borders + panel gray
#  7. Title colour-segment x-spans: original vs render
#  8. y-tick label / x-tick label ink bands: original vs render
import numpy as np
from PIL import Image
import collections

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
Q = NS + "/recreated_pptx/qa/slide031/"
O = np.asarray(Image.open(NS + "/unique_slides/slide_031.jpg").convert("RGB")).astype(int)
Rimg = Image.open(Q + "render_cur.png").convert("RGB").resize((960, 540), Image.LANCZOS)
Rn = np.asarray(Rimg).astype(int)
print("render_cur size", Image.open(Q + "render_cur.png").size, "-> downscaled", Rimg.size)


def raw(img, pts):
    return {p: tuple(img[p[1], p[0]]) for p in pts}


print("\n=== 1. original rows 258..272 at x=600,690,760 (axis hunt) ===")
for y in range(258, 273):
    print("  y%3d  x600=%s x690=%s x760=%s" % (y, tuple(O[y, 600]), tuple(O[y, 690]), tuple(O[y, 760])))
print("  render rows 258..272 at same x:")
for y in range(258, 273):
    print("  y%3d  x600=%s x690=%s x760=%s" % (y, tuple(Rn[y, 600]), tuple(Rn[y, 690]), tuple(Rn[y, 760])))

print("\n=== 2. original rows 304..314 at x=600,690,760 (plot bottom) ===")
for y in range(304, 315):
    print("  y%3d  x600=%s x690=%s x760=%s" % (y, tuple(O[y, 600]), tuple(O[y, 690]), tuple(O[y, 760])))

print("\n=== 3. plot verticals: original col 568..578 & 804..814 at y=150 ===")
for x in list(range(568, 579)) + list(range(804, 815)):
    print("  x%3d o=%s r=%s" % (x, tuple(O[150, x]), tuple(Rn[150, x])))

print("\n=== 4. red census inside original plot interior (cols 576..806, rows 70..306) ===")
R, G, B = O[:, :, 0], O[:, :, 1], O[:, :, 2]
red = (R > 90) & ((R - G) > 35) & ((R - B) > 8)
for x in range(576, 807):
    ys = np.nonzero(red[70:307, x])[0] + 70
    if len(ys):
        runs = []
        s = ys[0]; p = ys[0]
        for c in ys[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((int(s), int(p))); s = c; p = c
        runs.append((int(s), int(p)))
        print("  x%3d red n=%3d runs=%s" % (x, len(ys), runs))
print("  render red census, same region:")
Rr, Rg, Rb = Rn[:, :, 0], Rn[:, :, 1], Rn[:, :, 2]
redr = (Rr > 90) & ((Rr - Rg) > 35) & ((Rr - Rb) > 8)
for x in range(576, 807):
    ys = np.nonzero(redr[70:307, x])[0] + 70
    if len(ys):
        runs = []
        s = ys[0]; p = ys[0]
        for c in ys[1:]:
            if c == p + 1:
                p = c
            else:
                runs.append((int(s), int(p))); s = c; p = c
        runs.append((int(s), int(p)))
        print("  x%3d red n=%3d runs=%s" % (x, len(ys), runs))

print("\n=== 5. ASCII map x655..720 y232..272 (original): g=green, r=red, #=dark, .=light ===")
for y in range(232, 273):
    line = ""
    for x in range(655, 721):
        r, g, b = O[y, x]
        if g > r + 18 and g > b + 18 and g < 215:
            ch = "g"
        elif r > 90 and (r - g) > 35 and (r - b) > 8:
            ch = "r"
        elif max(r, g, b) < 150:
            ch = "#"
        elif max(r, g, b) < 220:
            ch = "+"
        else:
            ch = "."
        line += ch
    print("  y%3d %s" % (y, line))

print("\n=== 5b. ASCII map same region (render) ===")
for y in range(232, 273):
    line = ""
    for x in range(655, 721):
        r, g, b = Rn[y, x]
        if g > r + 18 and g > b + 18 and g < 215:
            ch = "g"
        elif r > 90 and (r - g) > 35 and (r - b) > 8:
            ch = "r"
        elif max(r, g, b) < 150:
            ch = "#"
        elif max(r, g, b) < 220:
            ch = "+"
        else:
            ch = "."
        line += ch
    print("  y%3d %s" % (y, line))

print("\n=== 6. annotation interior fill samples (far from borders) + panel gray ===")
for (x, y) in [(300, 250), (300, 285), (400, 250), (400, 285), (500, 250), (500, 285),
               (560, 250), (260, 262), (350, 262), (450, 262), (550, 262)]:
    print("  (%3d,%3d) o=%s r=%s" % (x, y, tuple(O[y, x]), tuple(Rn[y, x])))
print("  panel gray samples original:", tuple(O[520, 700]), tuple(O[100, 900]), tuple(O[520, 300]))

print("\n=== 7. title colour segments (rows 60..92) ===")
def segs(img):
    r, g, b = img[:, :, 0], img[:, :, 1], img[:, :, 2]
    redm = (r > 90) & ((r - g) > 40) & ((r - b) > 40)
    grnm = (g > r + 40) & (g > b + 40)
    blum = (b > r + 40) & (b > g + 30)
    out = {}
    for name, m in (("red", redm), ("green", grnm), ("blue", blum)):
        xs = np.nonzero(m[60:95].any(axis=0))[0]
        out[name] = (int(xs.min()), int(xs.max()), len(xs)) if len(xs) else None
    return out
print("  original:", segs(O))
print("  render  :", segs(Rn))

print("\n=== 8. tick-label ink bands ===")
def bands(img, x0, x1, y0, y1, thr=150):
    v = img.max(axis=2)
    m = v[0:540, 0:960] < thr
    reg = m[y0:y1, x0:x1]
    rows = [(y0 + i, int(reg[i].sum())) for i in range(reg.shape[0]) if reg[i].sum() > 0]
    cols = [(x0 + j, int(reg[:, j].sum())) for j in range(reg.shape[1]) if reg[:, j].sum() > 0]
    return rows, cols
for label, img in (("ORIG", O), ("REND", Rn)):
    rows, cols = bands(img, 574, 808, 268, 300)
    print("  %s x-tick rows:" % label, rows)
    rows2, cols2 = bands(img, 520, 572, 70, 300)
    print("  %s y-tick rows:" % label, rows2)
    print("  %s y-tick cols:" % label, cols2[:3], "...", cols2[-3:] if cols2 else [])
