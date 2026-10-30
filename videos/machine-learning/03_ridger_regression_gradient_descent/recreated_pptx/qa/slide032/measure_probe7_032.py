# STEP 1g - final: y=146 line, gridlines below y266, plot box borders,
# full-frame magenta/warm object census.
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
OUT = QA + "/measure_probe7_032.txt"

im = Image.open(NS + "/unique_slides/slide_032.jpg").convert("RGB")
px = im.load()

def hx(c):
    return "%02X%02X%02X" % tuple(int(round(v)) for v in c[:3])

lines = []
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); lines.append(s)

P("=" * 78)
P("KK. PLOT LINE AT data y=10 (frame y=146)")
P("=" * 78)
for y in range(143, 151):
    xs = [x for x in range(576, 806) if min(px[x, y]) < 235]
    if xs:
        cl = [[xs[0]]]
        for a in xs[1:]:
            if a - cl[-1][-1] <= 1:
                cl[-1].append(a)
            else:
                cl.append([a])
        P(" y=%3d clusters: %s" % (y, " | ".join("%d..%d" % (c[0], c[-1]) for c in cl)))
        P("      cores: %s" % " ".join(hx(px[(c[0] + c[-1]) // 2, y]) for c in cl))
    else:
        P(" y=%3d none" % y)
cand = [(x, y) for y in range(144, 149) for x in range(576, 806)]
dark = sorted(cand, key=lambda p: sum(px[p[0], p[1]]))[:12]
P("  darkest 12 in y144..148: %s" % " ".join("(%d,%d)%s" % (x, y, hx(px[x, y])) for x, y in dark))
P(" -- horizontal profile at y=145, x 645..690:")
for x in range(645, 691):
    P("    x=%d %s" % (x, hx(px[x, 145])))

P("")
P("=" * 78)
P("LL. GRIDLINES BELOW y266")
P("=" * 78)
for x in (600, 620, 700, 740, 760, 790):
    rows = []
    for y in range(267, 309):
        c = px[x, y]
        if c[0] < 243 or c[1] < 243 or c[2] < 243:
            rows.append((y, hx(c)))
    P(" x=%d : %s" % (x, " ".join("%d:%s" % r for r in rows)))

P("")
P("=" * 78)
P("MM. PLOT BOX BORDERS")
P("=" * 78)
P(" -- top border, column x=700, y62..74")
for y in range(62, 75):
    P("    y=%3d %s" % (y, hx(px[700, y])))
P(" -- bottom border, column x=700, y303..316")
for y in range(303, 316):
    P("    y=%3d %s" % (y, hx(px[700, y])))
P(" -- left border, row y=150, x570..578")
for x in range(570, 579):
    P("    x=%d %s" % (x, hx(px[x, 150])))
P(" -- right border, row y=150, x806..814")
for x in range(806, 815):
    P("    x=%d %s" % (x, hx(px[x, 150])))

P("")
P("=" * 78)
P("NN. FULL-FRAME MAGENTA (C000C0 family) CENSUS - excludes pink fills")
P("=" * 78)
def ismag(c):
    r, g, b = c
    return r > 100 and g < 90 and b > 100 and abs(r - b) < 80
pts = [(x, y) for y in range(45, 540) for x in range(54, 904) if ismag(px[x, y])]
P("  n=%d" % len(pts))
if pts:
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    P("  BBOX x %d..%d y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))
    per = {}
    for x, y in pts:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = sorted(per[y])
        cl = [[v[0]]]
        for a in v[1:]:
            if a - cl[-1][-1] <= 3:
                cl[-1].append(a)
            else:
                cl.append([a])
        P("   y=%3d clusters: %s" % (y, " | ".join("%d..%d(n%d)" % (c[0], c[-1], len(c)) for c in cl)))
    hist = {}
    for x, y in pts:
        h = hx(px[x, y]); hist[h] = hist.get(h, 0) + 1
    P("  top colours: %s" % " ".join("%s:%d" % t for t in sorted(hist.items(), key=lambda kv: -kv[1])[:15]))

P("")
P("=" * 78)
P("OO. FULL-FRAME WARM (red/maroon) OBJECT CENSUS")
P("=" * 78)
def warm(c):
    r, g, b = c
    if r > 235 and g > 185 and b > 185:
        return False
    return (r - b > 30) and (r - g > 25) and r > 70
pts = [(x, y) for y in range(45, 540) for x in range(54, 904) if warm(px[x, y])]
P("  n=%d" % len(pts))
if pts:
    # simple connected-component labelling on a grid
    S = set(pts)
    comps = []
    seen = set()
    for p in pts:
        if p in seen:
            continue
        stack = [p]; seen.add(p); comp = []
        while stack:
            (a, b) = stack.pop(); comp.append((a, b))
            for d in ((1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)):
                q = (a + d[0], b + d[1])
                if q in S and q not in seen:
                    seen.add(q); stack.append(q)
        comps.append(comp)
    P("  components: %d" % len(comps))
    for c in sorted(comps, key=lambda c: -len(c)):
        xs = [p[0] for p in c]; ys = [p[1] for p in c]
        hist = {}
        for x, y in c:
            h = hx(px[x, y]); hist[h] = hist.get(h, 0) + 1
        top = sorted(hist.items(), key=lambda kv: -kv[1])[:3]
        P("   comp n=%5d bbox x%4d..%4d y%3d..%3d  top: %s"
          % (len(c), min(xs), max(xs), min(ys), max(ys),
             " ".join("%s:%d" % t for t in top)))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nWROTE " + OUT)
