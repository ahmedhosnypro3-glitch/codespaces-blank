#!/usr/bin/env python3
"""Verify the five fix points on render_31.png (2001x1125; frame px * 2001/960)."""
from PIL import Image
import sys

im = Image.open("render_31.png").convert("RGB")
W, H = im.size
S = 2001 / 960.0
px = im.load()

def frame(v):
    return v * S

def is_gray(c, lo=200, hi=240):
    r, g, b = c
    return lo <= r <= hi and abs(r - g) < 8 and abs(g - b) < 8

fails = []
def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("  " + detail if detail else ""))
    if not ok:
        fails.append(name)

# 1. vertical grid: gray col groups along a row inside the plot (frame y=144 -> render 300)
ry = 300
cols = []
x = 1200
while x < 1690:
    if is_gray(px[x, ry]):
        x0 = x
        while x < 1690 and is_gray(px[x, ry]):
            x += 1
        cols.append((x0 + x - 1) / 2 / S)
    x += 1
expected_v = [585, 596, 607, 619, 642, 653, 664, 676, 699, 710, 722, 733, 745, 756, 768, 779, 790, 802]
missing = [e for e in expected_v if not any(abs(c - e) < 2.5 for c in cols)]
# axis col 630.5 (gray axis) and dash col 687 (red) excluded from expected list
check("vertical every-unit grid", not missing, f"{len(cols)} gray cols, missing={missing}")

# 2. horizontal grid: gray row groups along a column between gridlines (frame x=580 -> render 1209)
rx = 1209
rows = []
y = 145
while y < 645:
    if is_gray(px[rx, y]):
        y0 = y
        while y < 645 and is_gray(px[rx, y]):
            y += 1
        rows.append((y0 + y - 1) / 2 / S)
    y += 1
expected_h = [87, 98, 110, 122, 134, 146, 158, 170, 182, 194, 206, 218, 230, 254, 265, 278, 290, 302]
missing_h = [e for e in expected_h if not any(abs(c - e) < 2.5 for c in rows)]
check("horizontal every-unit grid", not missing_h, f"{len(rows)} gray rows, missing={missing_h}")

# 3. gaps white (frame-space sample points)
gap_pts = [
    ("band gap 384", 400, 384), ("band gap 428", 400, 428), ("band gap 472", 400, 472),
    ("band gap 497.5", 400, 497.5), ("west strip x70", 70, 400), ("east strip x888", 888, 400),
    ("below pink y525", 400, 525),
]
for nm, fx, fy in gap_pts:
    c = px[int(frame(fx)), int(frame(fy))]
    check(f"gap white {nm}", c == (255, 255, 255), str(c))

# 4. green dots pure 008000
for nm, gx, gy in [("green dot 1", 682, 252), ("green dot 2", 694, 252)]:
    c = px[int(frame(gx)), int(frame(gy))]
    check(nm, c == (0, 128, 0), str(c))

# 5. title ink runs along frame y=74 (render 154)
ry = 154
runs = {}
cur = None
for x in range(100, 1300):
    r, g, b = px[x, ry]
    kind = None
    if r > 150 and g < 90 and b < 90:
        kind = "red"
    elif g > 90 and r < 90 and b < 90:
        kind = "green"
    elif b > 150 and r < 90 and g < 90:
        kind = "blue"
    if kind != cur:
        if cur:
            runs.setdefault(cur, []).append((prev_x0, x - 1))
        cur = kind
        prev_x0 = x
if cur:
    runs.setdefault(cur, []).append((prev_x0, 1299))
for kind in ("red", "green", "blue"):
    spans = runs.get(kind, [])
    if spans:
        a, b_ = spans[0]
        check(f"title {kind} ink start", abs(a / S - {"red": 81, "green": 259, "blue": 446}[kind]) < 6,
              f"frame {a / S:.1f}..{b_ / S:.1f}")
    else:
        check(f"title {kind} ink present", False, "no ink found")

# 6. arrow red-outline bbox (search frame x134..185, y300..360)
xs, ys = [], []
for fy in range(int(300 * S), int(360 * S)):
    for fxr in range(int(134 * S), int(185 * S)):
        r, g, b = px[fxr, fy]
        if 100 <= r <= 190 and g < 90 and 20 <= b <= 90:
            xs.append(fxr)
            ys.append(fy)
if xs:
    a, b_ = min(xs) / S, max(xs) / S
    c, d = min(ys) / S, max(ys) / S
    ok = abs(a - 152) <= 4 and abs(b_ - 173) <= 5 and abs(c - 313) <= 4 and abs(d - 350) <= 5
    check("arrow bbox ~152..173 x 313..350", ok, f"frame {a:.1f}..{b_:.1f} x {c:.1f}..{d:.1f}")
else:
    check("arrow bbox present", False)

# 7. "(5, 1)" label: leftmost label-gray ink along frame y 244..258, x 690..740
lx = None
for fy in range(int(244 * S), int(258 * S)):
    for fxr in range(int(688 * S), int(745 * S)):
        r, g, b = px[fxr, fy]
        if abs(r - g) < 12 and abs(g - b) < 12 and 80 <= r <= 170:
            if lx is None or fxr < lx:
                lx = fxr
check("(5,1) label ink starts ~x700", lx is not None and abs(lx / S - 700) < 5,
      f"leftmost gray ink frame x={lx / S:.1f}" if lx else "none")

# 8. dashed red line at frame x687: tall red run
reds = [fy for fy in range(int(70 * S), int(300 * S)) if (lambda c: c[0] > 150 and c[1] < 120 and c[2] < 120)(px[int(frame(687)), fy])]
check("dashed C00000 col 687 present", len(reds) >= 90, f"{len(reds)} red px at col 687")

print("---")
print("ALL PASS" if not fails else f"FAILURES: {fails}")
sys.exit(0 if not fails else 1)
