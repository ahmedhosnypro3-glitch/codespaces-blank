# STEP 1c — decisive probes: blue curve strands (full, untruncated), magenta arrow,
# callout box bounds, salmon band, region below plot, y-axis tick labels.
from PIL import Image
import json

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
OUT = QA + "/measure_probe3_032.txt"

im = Image.open(NS + "/unique_slides/slide_032.jpg").convert("RGB")
W, H = im.size
px = im.load()

def hx(c):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in c[:3])

lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); lines.append(s)

P("=" * 78)
P("P. CURVE STRANDS — full untruncated per-row strand extraction in plot box")
P("   excluding: gridline gray (|r-g|<8 and |g-b|<8 and r>200), axis/red, white")
P("=" * 78)
strands = {}
for y in range(70, 266):
    pts = []
    for x in range(574, 810):
        r, g, b = px[x, y]
        # white interior
        if r > 245 and g > 245 and b > 245:
            continue
        # pure gray (gridline / axis / border blend) -> skip
        if abs(r - g) <= 8 and abs(g - b) <= 8:
            continue
        # red family (C00000 border, FF0000 vertical, F7BFC2-ish pink) -> skip
        if r - b > 40 and r - g > 40:
            continue
        # green dot family (008000) -> skip
        if g - r > 30 and g - b > 30:
            continue
        pts.append((x, (r, g, b)))
    if pts:
        # cluster contiguous
        cl = []
        cur = [pts[0]]
        for v in pts[1:]:
            if v[0] - cur[-1][0] <= 1:
                cur.append(v)
            else:
                cl.append(cur); cur = [v]
        cl.append(cur)
        desc = []
        for c in cl:
            xs = [p[0] for p in c]
            # average colour of the strand core (darkest pixel)
            core = min(c, key=lambda p: p[1][0] + p[1][1] + p[1][2])
            desc.append("x%d..%d(n%d,core%s)" % (xs[0], xs[-1], len(c), hx(core[1])))
        strands[y] = desc
        P(" y=%3d  %s" % (y, " | ".join(desc)))
    else:
        strands[y] = None

P("")
P("=" * 78)
P("Q. MAGENTA ARROW — strict C000C0 hunt in the callout->table corridor")
P("=" * 78)
# C000C0 = (192,0,192). Allow JPEG-drifted versions but require strong magenta:
# r and b high, g clearly low, and |r-b| small.
def ismag(c):
    r, g, b = c
    return r > 110 and g < 95 and b > 110 and abs(r - b) < 70
for (x0, x1, y0, y1, tag) in [(330, 620, 280, 345, "corridor wide"),
                              (420, 620, 300, 340, "below box3"),
                              (330, 620, 176, 300, "callouts above")]:
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if ismag(px[x, y])]
    P(" -- %s x%d..%d y%d..%d : n=%d" % (tag, x0, x1, y0, y1, len(pts)))
    if pts:
        per = {}
        for x, y in pts:
            per.setdefault(y, []).append((x, hx(px[x, y])))
        for y in sorted(per):
            v = per[y]
            xs = [p[0] for p in v]
            P("    y=%3d x %d..%d n=%d  cores: %s" % (y, min(xs), max(xs), len(v),
                                                      " ".join(sorted(set(p[1] for p in v))[:6])))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        P("    BBOX x %d..%d y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))

P("")
P("=" * 78)
P("R. BELOW-PLOT REGION — colour classes down the x=650 column and x=700 column")
P("=" * 78)
for x in (650, 700, 760):
    P(" -- x=%d" % x)
    prev = None
    for y in range(262, 340):
        h = hx(px[x, y])
        if h != prev:
            P("    y=%3d %s" % (y, h))
            prev = h

P("")
P("=" * 78)
P("S. CALLOUT BOX BOUNDS — vertical scans at box x-centres")
P("=" * 78)
for tag, x in [("box1 x@450", 450), ("box2 x@450", 450), ("box3 x@450", 450),
               ("left of boxes x@378", 378), ("right x@560", 560)]:
    P(" -- %s" % tag)
    prev = None; runs = []
    for y in range(176, 345):
        h = hx(px[x, y])
        if h != prev:
            runs.append((y, h)); prev = h
    for r in runs:
        P("    y=%3d %s" % r)

P("")
P("=" * 78)
P("T. SALMON BAND y495..520 (left-edge x302)")
P("=" * 78)
for y in range(495, 521):
    P("   y=%3d %s" % (y, hx(px[302, y])))

P("")
P("=" * 78)
P("U. Y-AXIS / TICK LABEL TEXT — ink columns below plot (y 268..296), x 550..830")
P("=" * 78)
# cluster non-panel pixels: panel is ~E9E9E7, white is >245
def is_bg(c):
    r, g, b = c
    return (r > 240 and g > 240 and b > 240) or (abs(r - g) < 14 and abs(g - b) < 14 and 200 < r < 245)
ink = [(x, y) for y in range(266, 300) for x in range(548, 835) if not is_bg(px[x, y])]
if ink:
    per = {}
    for x, y in ink:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = sorted(per[y])
        cl = [[v[0]]]
        for a in v[1:]:
            if a - cl[-1][-1] <= 3:
                cl[-1].append(a)
            else:
                cl.append([a])
        P(" y=%3d clusters: %s" % (y, " | ".join("%d..%d" % (c[0], c[-1]) for c in cl)))
else:
    P("   no ink found")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nWROTE " + OUT)
print("STRAND SUMMARY: %d rows with strands" % sum(1 for v in strands.values() if v))
