# STEP 1b — focused probes: blue curve (wide), callout column, magenta arrow,
# iteration-table 5 bands, gridline calibration, tick labels.
from PIL import Image
import json

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
OUT = QA + "/measure_probe2_032.txt"

im = Image.open(NS + "/unique_slides/slide_032.jpg").convert("RGB")
W, H = im.size
px = im.load()

def hx(c):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in c[:3])

lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    lines.append(s)

P("=" * 78)
P("/workspaces/codespaces-blank/ai_llm_slides. BLUE CURVE — wide scan over the whole plot box + surroundings")
P("=" * 78)
# loose blue test: blue clearly dominant
def isblue(c):
    r, g, b = c
    return b > 90 and b - r > 40 and b - g > 25

blue = [(x, y) for y in range(55, 320) for x in range(540, 840) if isblue(px[x, y])]
P("loose-blue pixels in x540..840 y55..320: n=%d" % len(blue))
if blue:
    xs = [p[0] for p in blue]; ys = [p[1] for p in blue]
    P("  bbox x %d..%d  y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))
    # per-y extent
    per = {}
    for x, y in blue:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = per[y]
        P("   y=%3d  blue x %d..%d  n=%d" % (y, min(v), max(v), len(v)))
else:
    P("  NONE — try even looser (b dominant, any r,g)")
    blue2 = [(x, y) for y in range(55, 320) for x in range(500, 900) if px[x, y][2] > px[x, y][0] + 20]
    P("  very-loose-blue n=%d" % len(blue2))
    if blue2:
        xs = [p[0] for p in blue2]; ys = [p[1] for p in blue2]
        P("  bbox x %d..%d y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))

# strict pure-blue (0000FF-ish) cores
P("")
P("-- strict blue core scan (b>=200, r<=80, g<=80), plot box x570..815 y66..266")
strict = [(x, y) for y in range(66, 267) for x in range(570, 816)
          if px[x, y][2] >= 200 and px[x, y][0] <= 80 and px[x, y][1] <= 80]
P("   n=%d" % len(strict))
if strict:
    per = {}
    for x, y in strict:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = per[y]
        P("   y=%3d  x %d..%d n=%d" % (y, min(v), max(v), len(v)))

P("")
P("=" * 78)
P("L. GRIDLINE / TICK CALIBRATION — find real vertical gridline x positions")
P("=" * 78)
# scan a plot row away from curve/dots for vertical gridlines: look for columns that
# are slightly darker than neighbours inside the white interior
for y in (100, 120, 160, 200, 230):
    cols = []
    for x in range(576, 808):
        c = px[x, y]
        if c[0] < 250 or c[1] < 250 or c[2] < 250:
            cols.append((x, hx(c)))
    P(" y=%d non-white cols in plot: %s" % (y, " ".join("%s:%s" % t for t in cols[:60])))

P("")
P("-- horizontal gridlines: scan a plot column away from curve")
for x in (600, 620, 700, 740):
    rows = []
    for y in range(69, 265):
        c = px[x, y]
        if c[0] < 250 or c[1] < 250 or c[2] < 250:
            rows.append((y, hx(c)))
    P(" x=%d non-white rows in plot: %s" % (x, " ".join("%s:%s" % t for t in rows[:40])))

P("")
P("=" * 78)
P("M. X-TICK LABELS below the plot (y 268..292)")
P("=" * 78)
for y in range(268, 294):
    xs = [x for x in range(555, 830) if not (px[x, y][0] > 240 and px[x, y][1] > 240 and px[x, y][2] > 240)]
    if xs:
        # cluster
        cl = []
        cur = [xs[0]]
        for v in xs[1:]:
            if v - cur[-1] <= 2:
                cur.append(v)
            else:
                cl.append(cur); cur = [v]
        cl.append(cur)
        P(" y=%3d clusters: %s" % (y, " | ".join("%d..%d" % (c[0], c[-1]) for c in cl)))

P("")
P("=" * 78)
P("N. CALLOUT COLUMN — boxes, fills, borders, arrow")
P("=" * 78)
P("-- horizontal colour-run probe at callout mid-lines")
for label, y in [("box1 mid", 197), ("box1 edge top", 185), ("box1 edge bot", 211),
                 ("box2 mid", 255), ("box3 mid", 302), ("arrow zone", 320), ("gap", 325),
                 ("gap below box3", 316)]:
    runs = []
    cur = None; start = None
    for x in range(370, 570):
        c = px[x, y]
        h = hx(c)
        if h != cur:
            if cur is not None:
                runs.append((start, x - 1, cur))
            cur = h; start = x
    runs.append((start, 569, cur))
    # merge tiny runs
    merged = []
    for r in runs:
        if merged and r[1] - r[0] <= 1:
            merged[-1] = (merged[-1][0], r[1], r[2])
        else:
            merged.append(list(r) if False else (r[0], r[1], r[2]))
    P(" %-18s y=%d: %s" % (label, y, " ".join("%d-%d:%s" % r for r in merged if r[1] - r[0] >= 1)))

P("")
P("-- magenta/C000C0 probe, wide region x330..620 y280..345")
mag = [(x, y) for y in range(280, 346) for x in range(330, 621)
       if px[x, y][0] > 120 and px[x, y][1] < 90 and px[x, y][2] > 120]
if mag:
    xs = [p[0] for p in mag]; ys = [p[1] for p in mag]
    P("   magenta n=%d bbox x %d..%d y %d..%d" % (len(mag), min(xs), max(xs), min(ys), max(ys)))
    per = {}
    for x, y in mag:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = per[y]
        P("    y=%3d x %d..%d n=%d  (width %d)" % (y, min(v), max(v), len(v), max(v) - min(v) + 1))
else:
    P("   NONE")

P("")
P("=" * 78)
P("O. ITERATION TABLE — 5 band fills / borders, measured")
P("=" * 78)
# for each candidate band, sample the fill at a text-free x and the border rows
BANDS = [(344, 383, "olive"), (387, 424, "lavender"), (431, 468, "peach"),
         (472, 494, "green"), (497, 517, "salmon")]
for y0, y1, nm in BANDS:
    P(" -- %s band y%d..%d" % (nm, y0, y1))
    for y in range(y0 - 3, y1 + 4):
        # sample a text-poor column: right edge of label col (x 300..320 is label text)
        # use x 340..352 (between label col and first data col) -> actually data col1 x354.5..395.5
        # pick x 340 (inside band, left of first data col, likely blank)
        samples = [px[x, y] for x in (330, 336, 342, 348)]
        uniq = {}
        for s in samples:
            uniq[hx(s)] = uniq.get(hx(s), 0) + 1
        P("    y=%3d %s" % (y, " ".join("%s:%d" % t for t in sorted(uniq.items(), key=lambda kv: -kv[1]))))
    # border rows: sample near left edge x302
    P("    left-edge x302 scan:")
    for y in range(y0 - 2, y1 + 3):
        P("      y=%3d %s" % (y, hx(px[302, y])))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nWROTE " + OUT)
