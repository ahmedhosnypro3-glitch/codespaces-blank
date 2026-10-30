#!/usr/bin/env python3
"""Probe 5 — precise run-lengths per color class inside each panel.

For LEFT (x99..462 y112..470) and RIGHT (x491..866 y112..470):
- strict-red px (r>150, r-g>70, r-b>70, g<110) grouped per x: y-runs
- dark-green px (g>80, g-r>35, g-b>35, r<150) grouped per x: y-runs
- bright-green px (g>130, g-r>60, g-b>60) grouped per x: y-runs
- blue interior fitted line: per-x mean y (x where 3<=n<=12)
Also caption red/dark x-runs per line.
"""
from PIL import Image
import sys, collections

img_path, label = sys.argv[1], sys.argv[2]
im = Image.open(img_path).convert("RGB")
W, H = im.size
px = im.load()
print(f"== {label}: {img_path} {im.size}")

def is_sr(c):
    r, g, b = c
    return r > 150 and r - g > 70 and r - b > 70 and g < 110
def is_dg(c):
    r, g, b = c
    return g > 80 and g - r > 35 and g - b > 35 and r < 150
def is_bg(c):
    r, g, b = c
    return g > 130 and g - r > 60 and g - b > 60
def is_nav(c):
    r, g, b = c
    return b > 110 and b - r > 50 and b - g > 50
def is_dark(c):
    r, g, b = c
    return r < 100 and g < 100 and b < 100

PANELS = (("LEFT", 99, 462, 112, 470), ("RIGHT", 491, 866, 112, 470))

for pname, x0, x1, y0, y1 in PANELS:
    print(f"\n===== {pname} panel =====")
    for cname, test in (("strict-red", is_sr), ("dark-green", is_dg), ("bright-green", is_bg)):
        perx = collections.defaultdict(list)
        for y in range(y0, y1):
            for x in range(x0, x1):
                if test(px[x, y]):
                    perx[x].append(y)
        print(f"-- {cname}: per-x y-runs (only x with runs) --")
        for x in sorted(perx):
            ys = perx[x]
            # group into runs (gap>2 breaks)
            runs = []
            cur = [ys[0], ys[0]]
            for y in ys[1:]:
                if y - cur[1] <= 2:
                    cur[1] = y
                else:
                    runs.append(tuple(cur))
                    cur = [y, y]
            runs.append(tuple(cur))
            rs = " ".join(f"{a}-{b}" for a, b in runs)
            print(f"   x={x}: n={len(ys)} runs: {rs}")
    # blue fitted line: per-x navy pixels in interior, thin columns = the line
    perx = collections.defaultdict(list)
    for y in range(y0, y1):
        for x in range(x0, x1):
            if is_nav(px[x, y]):
                perx[x].append(y)
    pts = []
    for x in sorted(perx):
        if 3 <= len(perx[x]) <= 12:
            ym = sum(perx[x]) / len(perx[x])
            pts.append((x, ym))
    print(f"-- blue fitted line: {len(pts)} columns --")
    if pts:
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        # least squares fit
        n = len(pts)
        sx = sum(xs); sy = sum(ys); sxx = sum(v * v for v in xs); sxy = sum(a * b for a, b in pts)
        slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
        icept = (sy - slope * sx) / n
        print(f"   fit: y = {slope:.4f}x + {icept:.1f}   x {xs[0]}..{xs[-1]}")
        print(f"   endpoints: ({xs[0]}, {slope*xs[0]+icept:.1f}) .. ({xs[-1]}, {slope*xs[-1]+icept:.1f})")
        for x, ym in pts[::max(1, len(pts) // 15)]:
            print(f"   x={x}: mean y={ym:.1f}")

# ---- caption bands: red & dark runs per x ----
print("\n===== captions =====")
for ylo, yhi, name in ((486, 503, "line1"), (507, 523, "line2")):
    for pname, (xa, xb) in (("L", (60, 470)), ("R", (480, 900))):
        reds, darks = [], []
        for x in range(xa, xb):
            r_ = any(is_sr(px[x, y]) for y in range(ylo, yhi))
            d_ = any(is_dark(px[x, y]) for y in range(ylo, yhi))
            if r_:
                reds.append(x)
            if d_:
                darks.append(x)
        def runs_of(lst):
            out = []
            cur = None
            for v in lst:
                if cur and v - cur[1] <= 3:
                    cur[1] = v
                else:
                    if cur:
                        out.append(tuple(cur))
                    cur = [v, v]
            if cur:
                out.append(tuple(cur))
            return " ".join(f"{a}-{b}" for a, b in out)
        print(f"   {name} {pname}: dark runs: {runs_of(darks)}")
        print(f"   {name} {pname}: RED  runs: {runs_of(reds)}")

# ---- mouse cursor hunt: dark compact clusters inside LEFT interior ----
print("\n===== dark clusters in LEFT interior (cursor?) =====")
dark = set()
for y in range(112, 470):
    for x in range(99, 462):
        if is_dark(px[x, y]):
            dark.add((x, y))
seen = set()
clusters = []
for p0 in dark:
    if p0 in seen:
        continue
    stack = [p0]
    seen.add(p0)
    comp = [p0]
    while stack:
        x, y = stack.pop()
        for dx in (-2, -1, 0, 1, 2):
            for dy in (-2, -1, 0, 1, 2):
                q = (x + dx, y + dy)
                if q in dark and q not in seen:
                    seen.add(q)
                    stack.append(q)
                    comp.append(q)
    xs = [p[0] for p in comp]; ys = [p[1] for p in comp]
    w = max(xs) - min(xs); h = max(ys) - min(ys)
    if len(comp) >= 15 and w <= 30 and h <= 30:
        clusters.append((min(xs), min(ys), max(xs), max(ys), len(comp)))
for c in sorted(clusters):
    print(f"   dark cluster x{c[0]}..{c[2]} y{c[1]}..{c[3]} n={c[4]}")
