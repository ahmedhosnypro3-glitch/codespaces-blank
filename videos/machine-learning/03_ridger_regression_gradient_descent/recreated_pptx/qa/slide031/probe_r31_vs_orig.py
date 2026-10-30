#!/usr/bin/env python3
"""Disk-truth probe: render_31.png vs unique_slides/slide_031.jpg (frame px)."""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ren = Image.open(f"{V}/recreated_pptx/qa/slide031/render_31.png").convert("RGB")
org = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
RW, RH = ren.size
S = RW / 960.0
rp, op = ren.load(), org.load()
print(f"render {RW}x{RH} scale {S:.4f}; orig {org.size}")

def r(fx, fy):
    return rp[int(fx * S), int(fy * S)]

def o(fx, fy):
    return op[fx, fy]

def is_red(c): r, g, b = c; return r > 120 and g < 90 and b < 90
def is_darkred(c): r, g, b = c; return r > 60 and g < 60 and b < 60 and r - g > 40
def is_gray(c, lo=140, hi=215):
    r, g, b = c
    return lo <= r <= hi and abs(r - g) < 14 and abs(g - b) < 14

def census_red_cols(img_px, x0, x1, y0, y1, scale, minn):
    out = []
    for x in range(int(x0 * scale), int(x1 * scale)):
        n = sum(1 for y in range(int(y0 * scale), int(y1 * scale)) if is_red(img_px[x, y]))
        if n >= minn:
            out.append((round(x / scale, 1), n))
    return out

def gray_cols(img_px, x0, x1, y0, y1, scale, minn):
    out = []
    for x in range(int(x0 * scale), int(x1 * scale)):
        n = sum(1 for y in range(int(y0 * scale), int(y1 * scale)) if is_gray(img_px[x, y]))
        if n >= minn:
            out.append(round(x / scale, 1))
    # collapse consecutive
    groups = []
    for v in out:
        if groups and v - groups[-1][-1] <= 2.5 / scale + 0.5:
            groups[-1].append(v)
        else:
            groups.append([v])
    return [round(sum(g) / len(g), 1) for g in groups]

print("\n== A. PLOT: red verticals (guide/borders), y70..260, minn=4 ==")
print(" ORIG:", census_red_cols(op, 575, 808, 70, 260, 1, 4))
print(" REND:", census_red_cols(rp, 575, 808, 70, 260, S, 4))

print("\n== B. PLOT: gray verticals x575..808 y70..258, minn=30 ==")
print(" ORIG:", gray_cols(op, 575, 808, 70, 258, 1, 30))
print(" REND:", gray_cols(rp, 575, 808, 70, 258, S, 30))

print("\n== C. red dot bbox around (650..670,175..192) ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    xs = [x for x in range(int(645 * sc), int(675 * sc)) for y in range(int(170 * sc), int(195 * sc)) if is_red(pxl[x, y])]
    ys = [y for x in range(int(645 * sc), int(675 * sc)) for y in range(int(170 * sc), int(195 * sc)) if is_red(pxl[x, y])]
    if xs:
        print(f" {name}: x {min(xs)/sc:.1f}..{max(xs)/sc:.1f} y {min(ys)/sc:.1f}..{max(ys)/sc:.1f} n={len(xs)}")
    else:
        print(f" {name}: NONE")

print("\n== D. green ellipse bbox (670..710,240..265) ==")
def is_green(c): r, g, b = c; return g > 90 and r < 100 and b < 110 and g - r > 40
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    pts = [(x, y) for x in range(int(665 * sc), int(715 * sc)) for y in range(int(238 * sc), int(268 * sc)) if is_green(pxl[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f" {name}: x {min(xs)/sc:.1f}..{max(xs)/sc:.1f} y {min(ys)/sc:.1f}..{max(ys)/sc:.1f} n={len(pts)}")
    else:
        print(f" {name}: NONE")

print("\n== E. TABLE navy frame: verticals x55..910 y340..525, dark-blue ==")
def is_navy(c): r, g, b = c; return b > 60 and b - r > 25 and r < 120 and g < 120
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    cols = []
    for x in range(int(55 * sc), int(910 * sc)):
        n = sum(1 for y in range(int(340 * sc), int(525 * sc)) if is_navy(pxl[x, y]))
        if n >= 100:
            cols.append(round(x / sc, 1))
    print(f" {name}: {cols[:6]}{'...' if len(cols)>6 else ''}{cols[-3:] if len(cols)>3 else ''} n={len(cols)}")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    rows = []
    for y in range(int(325 * sc), int(540 * sc)):
        n = sum(1 for x in range(int(70 * sc), int(890 * sc)) if is_navy(pxl[x, y]))
        if n >= 400:
            rows.append(round(y / sc, 1))
    print(f" {name} navy full-width rows: {rows}")

print("\n== F. band fills at frame sample points ==")
pts = [("band1 olive y360", 400, 360), ("gap y384", 400, 384), ("band2 violet y400", 400, 400),
       ("gap y428", 400, 428), ("band3 peach y450", 400, 450), ("band4 green y485", 400, 485),
       ("band5 pink y510", 400, 510), ("param label1 y190", 110, 190), ("param label3 y240", 110, 240),
       ("annot fill y255", 300, 255), ("annot border top y244", 300, 244), ("annot border left x245", 245, 260),
       ("eq border left x399 y200", 399, 200), ("plot bottom border y309", 700, 309), ("plot left border x573", 573, 150),
       ("bounce fill y300", 340, 300)]
for nm, fx, fy in pts:
    print(f" {nm}: ORIG {o(fx,fy)} REND {r(fx,fy)}")

print("\n== G. red hollow arrow region (130..190, 300..360): red-ink bbox ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    pts = [(x, y) for x in range(int(125 * sc), int(195 * sc)) for y in range(int(295 * sc), int(365 * sc)) if is_red(pxl[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f" {name}: x {min(xs)/sc:.1f}..{max(xs)/sc:.1f} y {min(ys)/sc:.1f}..{max(ys)/sc:.1f} n={len(pts)}")
    else:
        print(f" {name}: NONE")

print("\n== H. blue hollow arrows region (395..535, 305..345): blue-ink cols ==")
def is_blue(c): r, g, b = c; return b > 90 and b - r > 40 and b - g > 25
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    cols = []
    for x in range(int(390 * sc), int(540 * sc)):
        n = sum(1 for y in range(int(303 * sc), int(348 * sc)) if is_blue(pxl[x, y]))
        if n >= 3:
            cols.append(round(x / sc, 1))
    groups = []
    for v in cols:
        if groups and v - groups[-1][-1] <= 3:
            groups[-1].append(v)
        else:
            groups.append([v])
    print(f" {name}: {[round((g[0]+g[-1])/2,1) for g in groups]} (n={len(groups)})")

print("\n== I. title red run start (scan y67..83, x62..300; skip house stroke x58) ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    first = None
    for x in range(int(63 * sc), int(300 * sc)):
        if any(is_darkred(pxl[x, y]) or (pxl[x, y][0] > 150 and pxl[x, y][1] < 90 and pxl[x, y][2] < 90) for y in range(int(67 * sc), int(84 * sc))):
            first = x / sc
            break
    print(f" {name}: first title-red ink at x={first}")

print("\n== J. plot bottom edge y305..315 red row census x600..790 ==")
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    rows = []
    for y in range(int(300 * sc), int(320 * sc)):
        n = sum(1 for x in range(int(600 * sc), int(790 * sc)) if is_red(pxl[x, y]))
        if n >= 100:
            rows.append(round(y / sc, 1))
    print(f" {name}: {rows}")
