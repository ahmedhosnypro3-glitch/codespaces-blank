#!/usr/bin/env python3
"""Probe 3: threshold-swept stroke extents + contrast-dip profiles for all 8
topbox delimiters; band fill extents; y-label zone check."""
from PIL import Image

ORIG = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_003.jpg"
im = Image.open(ORIG).convert("RGB")
px = im.load()

DELIMS = [
    ("yellowL", 296.5), ("yellowR", 331.5), ("cyanL", 373.5), ("cyanR", 409),
    ("midcolL", 451), ("midcolR", 475), ("pinkL", 517.5), ("pinkR", 552.5),
]

def col_min_window(xc, y, halfw=3):
    return min(sum(px[xx, y]) / 3 for xx in range(int(xc) - halfw, int(xc) + halfw + 1))

print("### stroke y-extent via contrast dip vs local fill baseline")
print("### (baseline = median of window min over y150..250; dip>15 counts as stroke)")
for name, xc in DELIMS:
    vals = [(y, col_min_window(xc, y)) for y in range(130, 306)]
    import statistics
    base = statistics.median(v for _, v in vals if 150 <= _ <= 250)
    rows = [y for y, v in vals if base - v > 15]
    # longest consecutive stretch (allow 2-row gaps)
    stretches = []
    for y in rows:
        if stretches and y - stretches[-1][-1] <= 2: stretches[-1].append(y)
        else: stretches.append([y])
    main = max(stretches, key=len)
    print(f"  {name:8} x~{xc}: baseline={base:.0f} extent y{main[0]}..{main[-1]}  (all dips: {[(s[0], s[-1]) for s in stretches]})")

print()
print("### threshold sweep on each delimiter column (max consecutive run)")
for name, xc in DELIMS:
    xi = int(xc)
    line = f"  {name:8} x~{xc}:"
    for th in (160, 190, 210, 230, 245):
        best = 0; run = 0; bs = be = 0; start = 0
        for y in range(130, 306):
            v = min(sum(px[xx, y]) / 3 for xx in range(xi - 2, xi + 3))
            if v < th:
                if run == 0: start = y
                run += 1
                if run > best: best, bs, be = run, start, y
            else: run = 0
        line += f"  th{th}:{best}({bs}-{be})"
    print(line)

print()
print("### band fill extents (row y=210, between entry rows)")
def fill_extent(y, pred, x0, x1):
    xs = [x for x in range(x0, x1) if pred(px[x, y])]
    return (min(xs), max(xs)) if xs else None
yellow = lambda p: p[0] > 230 and p[1] > 230 and p[2] < 190
cyan   = lambda p: p[0] < 230 and p[1] > 230 and p[2] > 230
pink   = lambda p: p[0] > 200 and p[2] > 200 and p[1] < 200
for y in (210, 260, 285):
    print(f"  y={y}: yellow={fill_extent(y, yellow, 280, 350)} cyan={fill_extent(y, cyan, 360, 430)} pink={fill_extent(y, pink, 500, 570)}")

print()
print("### red y-label zone: rows y268..302, ink census per row in x285..345 (yellow band), x505..565 (pink band)")
for y in range(268, 303, 2):
    yj = sum(1 for x in range(285, 346) if px[x, y][0] > 150 and px[x, y][1] < 90 and px[x, y][2] < 90)
    yk = sum(1 for x in range(505, 566) if px[x, y][0] > 150 and px[x, y][1] < 90 and px[x, y][2] < 90)
    yw = sum(1 for x in range(365, 426) if px[x, y][0] > 150 and px[x, y][1] < 90 and px[x, y][2] < 90)
    print(f"  y={y}: redpx yellowband={yj:3d} cyanband={yw:3d} pinkband={yk:3d}")
