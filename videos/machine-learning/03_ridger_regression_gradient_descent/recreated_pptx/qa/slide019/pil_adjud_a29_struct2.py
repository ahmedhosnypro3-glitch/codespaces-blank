#!/usr/bin/env python3
# pil_adjud_a29_struct2.py — decisive geometry bank for A29 finding (a) fix:
#   1) vertical-line census at candidate x (runs + band-row interaction)
#   2) horizontal-rule census (ink-heavy rows)
#   3) per-band text clusters (bbox + dominant color)
# ORIG = unique_slides/slide_019.jpg (960x540), REND = qa/slide019/render_27.png
# (2001x1125, s=2.0844). Frame px == pt.
import sys
from PIL import Image

ROOT = "/home/ahmed/Projects/ai_llm_slides"
ORIG = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_019.jpg"
REND = ROOT + "/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide019/render_27.png"
S = 2001 / 960.0

oi = Image.open(ORIG).convert("RGB")
ri = Image.open(REND).convert("RGB")
ow, oh = oi.size
rw, rh = ri.size
op, rp = oi.load(), ri.load()

BANDS = [(272, 302), (379, 409), (487, 514)]

def cls(p):
    r, g, b = p
    if r > 180 and g < 110 and b < 110: return "R"
    if b > 140 and r < 110 and g < 110: return "B"
    if g > 110 and r < 110 and b < 110: return "G"
    if r > 225 and g > 225 and b < 165: return "y"    # yellow band (F8F880)
    if r > 200 and g > 200 and b > 200: return "."   # white
    if r + g + b < 260: return "#"                    # navy/dark
    if abs(r - g) < 40 and abs(g - b) < 40: return "+"  # gray-ish
    return "o"

def in_band(y):
    return any(a <= y <= b for a, b in BANDS)

def vruns(get, x0, xs, y0=166, y1=530, min_run=4):
    col = []
    for y in range(y0, y1):
        c = cls(get(xs, y))
        col.append((y, c))
    runs, cur = [], None
    for y, c in col:
        ink = c not in ".y"
        if ink and cur is None:
            cur = [y, y, {}]
        if ink:
            cur[1] = y
            cur[2][c] = cur[2].get(c, 0) + 1
        elif cur is not None:
            if cur[1] - cur[0] + 1 >= min_run:
                runs.append(cur)
            cur = None
    if cur is not None and cur[1] - cur[0] + 1 >= min_run:
        runs.append(cur)
    return runs

def fmt_runs(runs):
    out = []
    for y0, y1, cc in runs:
        dom = max(cc, key=cc.get)
        bnd = "B" if in_band(y0) and in_band(y1) else ("b" if in_band(y0) or in_band(y1) else "-")
        out.append(f"y{y0}..{y1}:{dom}x{cc[dom]}{bnd}")
    return " ".join(out) if out else "(none)"

print("== 1) VERTICAL CENSUS (orig frame px) ==")
XCAND_ORIG = [65, 66, 117, 118, 124, 125, 130, 206, 207, 208, 222, 230, 236, 237,
              269, 270, 302, 303, 335, 336, 368, 369, 377, 378, 379, 383, 384, 389,
              390, 421, 441, 449, 466, 467, 496, 529, 562, 595, 629, 637, 638, 639,
              643, 644, 671, 724, 888, 889, 894, 895]
for x in XCAND_ORIG:
    ro = vruns(lambda xx, yy, X=x: op[X, yy], x, x)
    print(f"ORIG x={x:<4}: {fmt_runs(ro)}")
print("-- render (same frame coords, sampled at x*S) --")
for x in XCAND_ORIG:
    xs = int(round(x * S))
    if xs >= rw: xs = rw - 1
    rr = vruns(lambda xx, yy, X=xs: rp[X, yy], x, x)
    print(f"REND x={x:<4}: {fmt_runs(rr)}")

print()
print("== 2) HORIZONTAL RULE CENSUS ==")
def hrow_ink(get, y, x0, x1):
    n = 0
    dom = {}
    for x in range(x0, x1):
        c = cls(get(x, y))
        if c not in ".yo":
            n += 1
            dom[c] = dom.get(c, 0) + 1
    return n, (max(dom, key=dom.get) if dom else ".")

def hcensus(get, x0, x1, y0=164, y1=532):
    rows = []
    for y in range(y0, y1):
        n, d = hrow_ink(get, y, x0, x1)
        if n >= (x1 - x0) * 0.55:
            rows.append((y, n, d))
    # merge adjacent
    merged = []
    for y, n, d in rows:
        if merged and y - merged[-1][1] <= 1:
            m = merged[-1]
            best = (n, d) if n >= m[3][0] else m[3]
            merged[-1] = (m[0], y, m[2] + n, best)
        else:
            merged.append((y, y, n, (n, d)))
    return [(a, b, dd[1]) for a, b, n, dd in merged]

print("ORIG full table width x70..895:")
for a, b, d in hcensus(lambda x, y: op[x, y], 70, 895):
    print(f"  y{a}..{b} dom={d}")
print("ORIG NO REG col x126..376:")
for a, b, d in hcensus(lambda x, y: op[x, y], 126, 376):
    print(f"  y{a}..{b} dom={d}")
print("ORIG RIDGE3 col x386..636:")
for a, b, d in hcensus(lambda x, y: op[x, y], 386, 636):
    print(f"  y{a}..{b} dom={d}")
print("ORIG RIDGE10 col x646..892:")
for a, b, d in hcensus(lambda x, y: op[x, y], 646, 892):
    print(f"  y{a}..{b} dom={d}")
print("ORIG anomaly col x68..115:")
for a, b, d in hcensus(lambda x, y: op[x, y], 68, 115):
    print(f"  y{a}..{b} dom={d}")
print("REND full table width x70..895 (frame coords):")
for a, b, d in hcensus(lambda x, y: rp[min(int(x * S), rw - 1), min(int(y * S), rh - 1)], 70, 895):
    print(f"  y{a}..{b} dom={d}")

print()
print("== 3) TEXT CLUSTERS per band (orig, NO REG grid x210..380) ==")
def clusters(get, x0, x1, y0, y1, gap=3):
    cols = []
    for x in range(x0, x1):
        ink = sum(1 for y in range(y0, y1) if cls(get(x, y)) not in ".y")
        cols.append((x, ink))
    cl, cur = [], None
    for x, n in cols:
        if n > 0 and cur is None:
            cur = [x, x]
        elif n > 0:
            if x - cur[1] <= gap:
                cur[1] = x
            else:
                cl.append(cur); cur = [x, x]
        elif cur and x - cur[1] > gap:
            cl.append(cur); cur = None
    if cur: cl.append(cur)
    out = []
    for a, b in cl:
        ys = [y for y in range(y0, y1) for x in range(a, b + 1) if cls(get(x, y)) not in ".y"]
        dom = {}
        for y in ys:
            for x in range(a, b + 1):
                c = cls(get(x, y))
                if c not in ".y":
                    dom[c] = dom.get(c, 0) + 1
        d = max(dom, key=dom.get) if dom else "."
        out.append((a, b, min(ys), max(ys), d, dom.get(d, 0)))
    return out

for (a, b, label) in [(205, 222, "g1 band1"), (224, 246, "g1 band2"), (248, 270, "g1 band3"),
                      (270, 300, "g1 band4")]:
    print(f"ORIG NO REG g1 {label} y{a}..{b}:")
    for x0, x1, yl, yh, d, n in clusters(lambda x, y: op[x, y], 210, 380, a, b):
        print(f"   x{x0}..{x1} y{yl}..{yh} dom={d} n={n}")
print()
for (a, b, label) in [(408, 428, "g3 band1"), (428, 452, "g3 band2"), (452, 476, "g3 band3"),
                      (476, 512, "g3 band4")]:
    print(f"ORIG RIDGE3 g3 {label} y{a}..{b} (grid x468..636):")
    for x0, x1, yl, yh, d, n in clusters(lambda x, y: op[x, y], 468, 640, a, b):
        print(f"   x{x0}..{x1} y{yl}..{yh} dom={d} n={n}")

print()
print("== 4) RIDGE3 g3 W third entry byte-read (orig) ==")
# W box x389..466; entries col ~x433..449; g3 gy=420 -> third entry y~460..478
for yl, yh in [(455, 482)]:
    print(f"ORIG x425..462 y{yl}..{yh} ds1:")
    hdr = "     " + "".join(str((x // 10) % 10) for x in range(425, 462))
    hdr2 = "     " + "".join(str(x % 10) for x in range(425, 462))
    print(hdr); print(hdr2)
    for y in range(yl, yh):
        row = "".join(cls(op[x, y]) if cls(op[x, y]) not in "oy" else "." for x in range(425, 462))
        print(f"y{y:<4}{row}")
print("REND same region ds1 (x*S):")
for yl, yh in [(455, 482)]:
    print(f"REND x425..462 y{yl}..{yh}:")
    print(hdr); print(hdr2)
    for y in range(yl, yh):
        yy = int(y * S)
        if yy >= rh: yy = rh - 1
        row = "".join(cls(rp[min(int(x * S), rw - 1), yy]) if cls(rp[min(int(x * S), rw - 1), yy]) not in "oy" else "." for x in range(425, 462))
        print(f"y{y:<4}{row}")

print()
print("== 5) HEADER INK CENSUS (orig y172..203) ==")
for nm, x0, x1 in [("NO REG", 126, 378), ("RIDGE 3", 386, 636), ("RIDGE 10", 646, 892)]:
    dom = {}
    xs_by = {}
    for x in range(x0, x1):
        for y in range(173, 203):
            c = cls(op[x, y])
            if c in "RBG#":
                dom[c] = dom.get(c, 0) + 1
                xs_by.setdefault(c, []).append(x)
    tot = sum(dom.values())
    parts = []
    for c, n in sorted(dom.items(), key=lambda kv: -kv[1]):
        xs = xs_by[c]
        parts.append(f"{c}={n} x{min(xs)}..{max(xs)}")
    print(f"{nm}: total_ink={tot} | " + " | ".join(parts))
