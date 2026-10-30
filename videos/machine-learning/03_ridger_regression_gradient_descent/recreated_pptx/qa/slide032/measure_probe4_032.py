# STEP 1d — final adjudication probes: green dot, red y309 line (full extent),
# box2/box3 exact bounds, ASCII map of the arrow corridor, y-axis extension.
from PIL import Image

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
OUT = QA + "/measure_probe4_032.txt"

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
P("V. GREEN DOT (5,1) — search the whole plot box for green ink")
P("=" * 78)
gpts = [(x, y) for y in range(67, 266) for x in range(574, 810)
        if px[x, y][1] - px[x, y][0] > 25 and px[x, y][1] - px[x, y][2] > 25]
P("  green-ish pixels in plot: n=%d" % len(gpts))
if gpts:
    xs = [p[0] for p in gpts]; ys = [p[1] for p in gpts]
    P("  bbox x %d..%d y %d..%d" % (min(xs), max(xs), min(ys), max(ys)))
    per = {}
    for x, y in gpts:
        per.setdefault(y, []).append(x)
    for y in sorted(per):
        v = per[y]
        P("   y=%3d x %d..%d n=%d core=%s" % (y, min(v), max(v), len(v), hx(px[min(v), y])))
else:
    P("  NONE -> the green dot is NOT in the original frame")
# also scan whole frame for green blobs outside plot
gall = [(x, y) for y in range(45, 540) for x in range(54, 904)
        if px[x, y][1] - px[x, y][0] > 40 and px[x, y][1] - px[x, y][2] > 40 and px[x, y][1] > 120]
P("  strong-green whole-frame (excl. table bands): n=%d" % len(gall))

P("")
P("=" * 78)
P("W. RED HORIZONTAL LINE at y~309 — full horizontal extent")
P("=" * 78)
for y in range(303, 316):
    xs = []
    for x in range(540, 900):
        r, g, b = px[x, y]
        # red: r clearly dominant
        if r - g > 50 and r - b > 50:
            xs.append(x)
    if xs:
        cl = [[xs[0]]]
        for v in xs[1:]:
            if v - cl[-1][-1] <= 2:
                cl[-1].append(v)
            else:
                cl.append([v])
        P(" y=%3d red clusters: %s" % (y, " | ".join("%d..%d" % (c[0], c[-1]) for c in cl)))
    else:
        P(" y=%3d none" % y)
P(" -- exact vertical profile at x=650 and x=760:")
for x in (650, 760):
    P("   x=%d: y306 %s y307 %s y308 %s y309 %s y310 %s y311 %s y312 %s"
      % (x, hx(px[x, 306]), hx(px[x, 307]), hx(px[x, 308]), hx(px[x, 309]),
         hx(px[x, 310]), hx(px[x, 311]), hx(px[x, 312])))

P("")
P("=" * 78)
P("X. BOX2 GREEN BORDER + BOX3 FILL — horizontal extents")
P("=" * 78)
for tag, y in [("box2 top border", 234), ("box2 fill", 250), ("box2 bottom border", 279),
               ("box3 fill", 300), ("box3 fill lower", 316),
               ("greyish band below box3", 322)]:
    P(" -- %s y=%d" % (tag, y))
    runs = []; cur = None; st = None
    for x in range(360, 600):
        h = hx(px[x, y])
        if h != cur:
            if cur is not None:
                runs.append((st, x - 1, cur))
            cur = h; st = x
    runs.append((st, 599, cur))
    for a, b, h in runs:
        if b - a >= 2:
            P("    %d..%d %s" % (a, b, h))

P("")
P("=" * 78)
P("Y. Y-AXIS / RED-VERTICAL EXTENSION below the plot")
P("=" * 78)
for x0, x1, tag in [(628, 636, "black y-axis"), (684, 694, "red vertical x=687.5")]:
    P(" -- %s : vertical profile x%d..%d" % (tag, x0, x1))
    prev = None
    for y in range(264, 312):
        # dark = any channel < 200
        darks = [x for x in range(x0, x1 + 1) if min(px[x, y]) < 200]
        if darks:
            s = "y=%3d dark x %s" % (y, ",".join(str(x) for x in darks))
            if s != prev:
                P("   " + s)
                prev = s
        else:
            if prev != "none":
                P("   y=%3d none" % y)
                prev = "none"

P("")
P("=" * 78)
P("Z. ASCII MAP of the arrow corridor x335..620 y288..340")
P("   legend:  W=white  P=panel-gray  Y=yellow  G=green  R=red  M=magenta/purple")
P("            B=blue  /workspaces/codespaces-blank/ai_llm_slides=black/dark  .=other")
P("=" * 78)
def cls(c):
    r, g, b = c
    if r > 245 and g > 245 and b > 245: return "W"
    if abs(r - 233) < 14 and abs(g - 233) < 14 and abs(b - 231) < 16: return "P"
    if r - g > 50 and r - b > 50: return "R"
    if g - r > 25 and g - b > 25: return "G"
    if b - r > 25 and b - g > 15: return "B"
    if r - b > 40 and b - g > 20: return "M"
    if min(r, g, b) < 150: return "/workspaces/codespaces-blank/ai_llm_slides"
    return "."
hdr = "     " + "".join(str((x // 10) % 10) for x in range(335, 620, 1))
P(hdr)
for y in range(288, 341):
    P("y=%3d %s" % (y, "".join(cls(px[x, y]) for x in range(335, 620))))

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
print("\nWROTE " + OUT)
