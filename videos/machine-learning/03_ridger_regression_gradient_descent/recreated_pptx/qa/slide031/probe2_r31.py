#!/usr/bin/env python3
"""Probe 2: resolve the four suspect deltas + gridline census at matched thresholds."""
from PIL import Image

V = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ren = Image.open(f"{V}/recreated_pptx/qa/slide031/render_31.png").convert("RGB")
org = Image.open(f"{V}/unique_slides/slide_031.jpg").convert("RGB")
RW, _ = ren.size
S = RW / 960.0
rp, op = ren.load(), org.load()

def r(fx, fy): return rp[int(fx * S), int(fy * S)]
def o(fx, fy): return op[fx, fy]

print("== K. render's tall red col ~687: colors down the column ==")
for fy in (75, 100, 130, 160, 190, 220, 245, 258):
    print(f" y={fy}: REND {r(687.5, fy)}  |  ORIG {o(687, fy)}")
print(" neighbors x686/689 at y150:", r(686, 150), r(689, 150))

print("\n== L. light-gray gridline census (200-245) in plot, verticals minn=30 ==")
def is_lgray(c, lo=196, hi=246):
    rr, g, b = c
    return lo <= rr <= hi and abs(rr - g) < 12 and abs(g - b) < 12
def cols(pxl, sc, y0, y1, minn):
    out = []
    for x in range(int(575 * sc), int(808 * sc)):
        n = sum(1 for y in range(int(y0 * sc), int(y1 * sc)) if is_lgray(pxl[x, y]))
        if n >= minn: out.append(round(x / sc, 1))
    groups = []
    for v in out:
        if groups and v - groups[-1][-1] <= 2.6 / sc + 0.5: groups[-1].append(v)
        else: groups.append([v])
    return [round(sum(g) / len(g), 1) for g in groups]
print(" ORIG v-cols:", cols(op, 1, 70, 258, 30))
print(" REND v-cols:", cols(rp, S, 70, 258, 30))
def rows(pxl, sc, x0, x1, minn):
    out = []
    for y in range(int(68 * sc), int(300 * sc)):
        n = sum(1 for x in range(int(x0 * sc), int(x1 * sc)) if is_lgray(pxl[x, y]))
        if n >= minn: out.append(round(y / sc, 1))
    groups = []
    for v in out:
        if groups and v - groups[-1][-1] <= 2.6 / sc + 0.5: groups[-1].append(v)
        else: groups.append([v])
    return [round(sum(g) / len(g), 1) for g in groups]
print(" ORIG h-rows:", rows(op, 1, 640, 800, 60))
print(" REND h-rows:", rows(rp, S, 640, 800, 60))

print("\n== M. eq box red borders census (render), region x385..545 y180..220 ==")
def is_red(c): rr, g, b = c; return rr > 120 and g < 90 and b < 90
vcols = []
for x in range(int(385 * S), int(545 * S)):
    n = sum(1 for y in range(int(184 * S), int(214 * S)) if is_red(rp[x, y]))
    if n >= 15: vcols.append(round(x / S, 1))
hrows = []
for y in range(int(178 * S), int(222 * S)):
    n = sum(1 for x in range(int(395 * S), int(535 * S)) if is_red(rp[x, y]))
    if n >= 40: hrows.append(round(y / S, 1))
print(" REND eq red v-cols:", vcols)
print(" REND eq red h-rows:", hrows)
print(" sample interior:", r(460, 200), " (orig interior:", o(460, 200), ")")

print("\n== N. orig blue arrows: direct samples ==")
for fx in (403, 439, 476, 518):
    print(f" ORIG col {fx}: ", [o(fx, fy) for fy in (310, 316, 322, 330, 338)])
print(" ORIG scan y310..345 any-blue cols (b>80, b-r>30):")
out = []
for x in range(390, 540):
    n = sum(1 for y in range(308, 348) if (lambda c: c[2] > 80 and c[2] - c[0] > 30)(op[x, y]))
    if n >= 4: out.append((x, n))
print(" ", out)

print("\n== O. band fills multi-point (avoid text): medians of 5 samples ==")
import statistics
def med(pxl, sc, pts):
    vals = [pxl[int(fx * sc), int(fy * sc)] for fx, fy in pts]
    return tuple(int(statistics.median([v[i] for v in vals])) for i in range(3))
bands = [
    ("band3 peach", [(360, 440), (500, 442), (700, 455), (820, 438), (560, 460)]),
    ("band4 green", [(360, 482), (500, 480), (700, 483), (820, 481), (560, 490)]),
    ("band5 pink", [(360, 505), (700, 505), (820, 505), (500, 505), (560, 507)]),
    ("band1 olive", [(360, 352), (700, 352), (820, 352), (500, 375), (560, 375)]),
    ("band2 violet", [(360, 395), (700, 395), (820, 395), (500, 415), (560, 415)]),
]
for nm, pts in bands:
    print(f" {nm}: ORIG {med(op,1,pts)}  REND {med(rp,S,pts)}")

print("\n== P. red arrow bbox refined: orig vs render, red OR dark-red ink ==")
def is_r(c): rr, g, b = c; return (rr > 120 and g < 90 and b < 90) or (rr > 100 and 20 <= g < 90 and 20 <= b < 100 and rr - g > 50)
for name, pxl, sc in (("ORIG", op, 1), ("REND", rp, S)):
    pts = [(x, y) for x in range(int(125 * sc), int(200 * sc)) for y in range(int(295 * sc), int(370 * sc)) if is_r(pxl[x, y])]
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        print(f" {name}: x {min(xs)/sc:.1f}..{max(xs)/sc:.1f} y {min(ys)/sc:.1f}..{max(ys)/sc:.1f} n={len(pts)}")

print("\n== Q. purple 3/3 marks + plot text ink clusters in orig (dark, non-curve) ==")
def is_ink(c): rr, g, b = c; return rr < 120 and g < 120 and b < 120
for name, pxl, sc, rg in (("ORIG", op, 1, (655, 690, 125, 142)), ("REND", rp, S, (655, 690, 125, 142))):
    x0, x1, y0, y1 = rg
    n = sum(1 for x in range(int(x0*sc), int(x1*sc)) for y in range(int(y0*sc), int(y1*sc)) if is_ink(pxl[x, y]))
    print(f" {name} purple-mark zone (655..690,125..142) dark n={n}")
for name, pxl, sc, rg in (("ORIG", op, 1, (626, 660, 146, 160)), ("REND", rp, S, (626, 660, 146, 160))):
    x0, x1, y0, y1 = rg
    n = sum(1 for x in range(int(x0*sc), int(x1*sc)) for y in range(int(y0*sc), int(y1*sc)) if is_ink(pxl[x, y]))
    print(f" {name} '(2,10)' zone (626..660,146..160) dark n={n}")
for name, pxl, sc, rg in (("ORIG", op, 1, (720, 752, 137, 152)), ("REND", rp, S, (720, 752, 137, 152))):
    x0, x1, y0, y1 = rg
    n = sum(1 for x in range(int(x0*sc), int(x1*sc)) for y in range(int(y0*sc), int(y1*sc)) if is_ink(pxl[x, y]))
    print(f" {name} '(?,?)' zone (720..752,137..152) dark n={n}")
