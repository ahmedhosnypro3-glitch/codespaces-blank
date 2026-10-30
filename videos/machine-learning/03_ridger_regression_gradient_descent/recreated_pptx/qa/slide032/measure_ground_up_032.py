# STEP 1 — ground-up re-measurement of slide 032's row-band gradient, plot box,
# calibration, callouts and arrow, per ORCHESTRATOR_FINDINGS.md authorisation.
# Own PIL probes over the 960x540 original frame. Outputs JSON + human log.
from PIL import Image
import json, os, sys

NS = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
QA = NS + "/recreated_pptx/qa/slide032"
OUT = QA + "/measure_ground_up_032.json"

im = Image.open(NS + "/unique_slides/slide_032.jpg").convert("RGB")
W, H = im.size
assert (W, H) == (960, 540), (W, H)
px = im.load()

def hex_of(rgb):
    return "%02X%02X%02X" % tuple(int(round(c)) for c in rgb[:3])

def sample_row(x, y, xs):
    return [(x, px[x, y]) for x in xs]

def band(y, x0, x1):
    """per-x colour stats across a horizontal band"""
    cols = {}
    for x in range(x0, x1 + 1):
        h = hex_of(px[x, y])
        cols[h] = cols.get(h, 0) + 1
    top = sorted(cols.items(), key=lambda kv: -kv[1])[:6]
    return top, len(cols)

res = {"frame": [W, H], "bands": {}, "row_bands": {}, "probes": {}}

# ---------------------------------------------------------------- ROW BANDS
# ORCHESTRATOR: re-measure all 5 ROW bands with per-row, per-y sampling.
# Inherited claim: row3 y229..251 flat FBFF0B. Fresh: gradient at y~248.
print("=" * 78)
print("A. PARAMETER-TABLE ROW BANDS (per-y sampling, x=150 mid-band)")
print("=" * 78)
param_y = [(178, 203, "row1 step 0.4"), (204, 228, "row2 initial X 3"), (229, 251, "row3 delta 0.1")]
for y0, y1, name in param_y:
    print("\n-- %s  y%d..%d" % (name, y0, y1))
    per_y = []
    for y in range(y0, y1 + 1):
        top, distinct = band(y, 150, 196)
        h, n = top[0]
        per_y.append({"y": y, "dominant": h, "count": n, "distinct": distinct, "top": top})
        print("   y=%3d  dominant %s x%d  (distinct=%d)  top: %s"
              % (y, h, n, distinct, " ".join("%s:%d" % t for t in top[:4])))
    res["row_bands"][name] = per_y

# gradient probe: vertical scan at x=150 across row3 and beyond
print("\n%s\nB. GRADIENT PROBE — vertical scan, x=150, y=176..256\n%s" % ("=" * 78, "=" * 78))
scan = []
for y in range(176, 257):
    r, g, b = px[150, y]
    scan.append({"y": y, "rgb": [r, g, b], "hex": hex_of((r, g, b))})
    print("   y=%3d  %s  (%d,%d,%d)" % (y, hex_of((r, g, b)), r, g, b))
res["probes"]["row3_gradient_x150"] = scan

# horizontal scan of the y=248 line across the whole row width
print("\n%s\nC. HORIZONTAL SCAN y=248, x=76..208\n%s" % ("=" * 78, "=" * 78))
h248 = []
for x in range(76, 209):
    h = hex_of(px[x, 248])
    h248.append({"x": x, "hex": h})
    if x % 4 == 0 or x in (76, 77, 208):
        print("   x=%3d %s" % (x, h))
res["probes"]["row3_y248_horizontal"] = h248

# ------------------------------------------------------------- PLOT BOX
print("\n%s\nD. PLOT BOX — white rect detection\n%s" % ("=" * 78, "=" * 78))
def is_white(c):
    return c[0] >= 248 and c[1] >= 248 and c[2] >= 248
# scan rows for long white runs in the top-right quadrant
for y in [66, 70, 100, 150, 200, 264, 266, 270, 272]:
    row = [x for x in range(500, 850) if is_white(px[x, y])]
    if row:
        print("   y=%3d white run x %d..%d (n=%d)" % (y, min(row), max(row), len(row)))
    else:
        print("   y=%3d no white" % y)
res["probes"]["plot_white_runs"] = {}

# find exact plot rect by scanning for the white block bounded by non-white
print("\n-- vertical white-run extents at y=150 / y=250")
for y in (150, 250):
    row = [x for x in range(500, 850) if is_white(px[x, y])]
    print("   y=%d white x %d..%d" % (y, min(row), max(row)))
print("\n-- column white-run extents at x=650 / x=780")
for x in (650, 780):
    col = [y for y in range(50, 320) if is_white(px[x, y])]
    print("   x=%d white y %d..%d" % (x, min(col), max(col)))
res["probes"]["plot_rect_probe"] = {
    "rows": {y: [min(x for x in range(500, 850) if is_white(px[x, y])),
                 max(x for x in range(500, 850) if is_white(px[x, y]))] for y in (150, 250)},
    "cols": {x: [min(y for y in range(50, 320) if is_white(px[x, y])),
                 max(y for y in range(50, 320) if is_white(px[x, y]))] for x in (650, 780)},
}

# --------------------------------------------------------- PLOT BORDER COLOURS
print("\n%s\nE. PLOT BORDER — colour scan on candidate edges\n%s" % ("=" * 78, "=" * 78))
edges = {
    "top_candidates": [(576, y) for y in range(62, 74)],
    "bottom_candidates": [(576, y) for y in range(262, 272)],
    "left_candidates": [(x, 150) for x in range(508, 582)],
    "right_candidates": [(x, 150) for x in range(800, 818)],
}
for name, pts in edges.items():
    print(" --", name)
    for (x, y) in pts:
        print("    (%d,%d) %s" % (x, y, hex_of(px[x, y])))
res["probes"]["plot_borders"] = {k: [{"p": p, "hex": hex_of(px[p[0], p[1]])} for p in v] for k, v in edges.items()}

# ------------------------------------------------------------ CALL: CALIBRATION
print("\n%s\nF. BLUE CURVE sampling (for calibration refit)\n%s" % ("=" * 78, "=" * 78))
def blueish(c):
    return c[2] > 120 and c[2] - c[0] > 60 and c[2] - c[1] > 30
blue = {}
for y in range(60, 300):
    xs = [x for x in range(560, 830) if blueish(px[x, y])]
    if xs:
        blue[y] = (min(xs), max(xs), len(xs))
for y in sorted(blue):
    print("   y=%3d  blue x %d..%d  n=%d" % (y, blue[y][0], blue[y][1], blue[y][2]))
res["probes"]["blue_curve"] = {"%d" % y: list(v) for y, v in blue.items()}

# -------------------------------------------------------------- DOTS
print("\n%s\nG. DOTS — green (5,1) and red (2,10)\n%s" % ("=" * 78, "=" * 78))
def flood(c, sx, sy, tol):
    seen, stack = set(), [(sx, sy)]
    while stack:
        (a, b) = stack.pop()
        if (a, b) in seen or not (0 <= a < W and 0 <= b < H):
            continue
        if abs(px[a, b][0] - c[0]) > tol or abs(px[a, b][1] - c[1]) > tol or abs(px[a, b][2] - c[2]) > tol:
            continue
        seen.add((a, b))
        stack += [(a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)]
    return seen

for name, c, probe in [("green", (0, 128, 0), (688, 255)), ("red", (255, 0, 0), (660, 182))]:
    try:
        s = flood(c, probe[0], probe[1], 60)
        xs = [p[0] for p in s]; ys = [p[1] for p in s]
        print("   %s dot n=%d  x %d..%d  y %d..%d  centre (%.1f,%.1f)"
              % (name, len(s), min(xs), max(xs), min(ys), max(ys),
                 (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0))
        res["probes"]["dot_" + name] = {"n": len(s), "x": [min(xs), max(xs)], "y": [min(ys), max(ys)]}
    except Exception as e:
        print("   %s dot probe failed: %s" % (name, e))

# ------------------------------------------------------------- ARROW
print("\n%s\nH. MAGENTA ARROW (C000C0 family)\n%s" % ("=" * 78, "=" * 78))
mag = [(x, y) for y in range(250, 400) for x in range(400, 650)
       if px[x, y][0] > 140 and px[x, y][1] < 70 and px[x, y][2] > 140]
if mag:
    mx0 = min(p[0] for p in mag); mx1 = max(p[0] for p in mag)
    my0 = min(p[1] for p in mag); my1 = max(p[1] for p in mag)
    print("   magenta ink x %d..%d  y %d..%d  n=%d" % (mx0, mx1, my0, my1, len(mag)))
    res["probes"]["arrow"] = {"x": [mx0, mx1], "y": [my0, my1], "n": len(mag)}
else:
    print("   NO magenta ink found in region")
    res["probes"]["arrow"] = None

# --------------------------------------------------------- HOUSE CHROME
print("\n%s\nI. HOUSE CHROME\n%s" % ("=" * 78, "=" * 78))
chrome = {}
# panel
panel = {}
for y in (500, 530):
    top, _ = band(y, 60, 900)
    panel["y%d" % y] = top[:3]
    print("   y=%d panel dominant: %s" % (y, top[:3]))
# top band (should be WHITE, outside panel)
top, _ = band(20, 100, 700)
print("   y=20 (above panel) dominant: %s" % (top[:3],))
# strokes
for name, pts in [
    ("left_x58.5", [(58, y) for y in (100, 300, 500)]),
    ("right_x901", [(901, y) for y in (100, 300, 500)]),
    ("bottom_y538.5", [(x, 538) for x in (200, 500, 800)]),
    ("top_y45..47", [(x, y) for x, y in [(200, 45), (500, 46), (800, 47)]]),
]:
    print(" --", name, [(p, hex_of(px[p[0], p[1]])) for p in pts])
    chrome[name] = [(list(p), hex_of(px[p[0], p[1]])) for p in pts]
# badge
badge = {}
for y in range(55, 92):
    row = [x for x in range(855, 900) if px[x, y][0] > 230 and px[x, y][1] > 230 and px[x, y][2] < 190]
    if row:
        badge[y] = [min(row), max(row)]
if badge:
    bx0 = min(v[0] for v in badge.values()); bx1 = max(v[1] for v in badge.values())
    by0 = min(badge); by1 = max(badge)
    print("   badge yellow fill x %d..%d y %d..%d -> centre (%.1f,%.1f) d~%d"
          % (bx0, bx1, by0, by1, (bx0 + bx1) / 2.0, (by0 + by1) / 2.0, (bx1 - bx0)))
    chrome["badge_fill"] = {"x": [bx0, bx1], "y": [by0, by1]}
res["chrome"] = chrome

# --------------------------------------------------------------- TITLE
print("\n%s\nJ. TITLE — colour runs\n%s" % ("=" * 78, "=" * 78))
for y in (65, 72, 78, 85):
    xs = [x for x in range(60, 900) if not is_white(px[x, y]) and px[x, y] != (233, 233, 231)]
    # restrict to the title zone above the plot
    xs = [x for x in xs if y < 60 or x < 560]
    if xs:
        print("   y=%d title ink x %d..%d" % (y, min(xs), max(xs)))
        res["probes"].setdefault("title", []).append({"y": y, "x": [min(xs), max(xs)]})
# find colour runs at the title's mid-line
mid = 76
runs = []
cur = None
for x in range(60, 600):
    c = px[x, mid]
    near_white = c[0] > 245 and c[1] > 245 and c[2] > 245
    panel_gray = abs(c[0] - 233) < 12 and abs(c[1] - 233) < 12 and abs(c[2] - 231) < 12
    if near_white or panel_gray:
        h = None
    else:
        h = hex_of(c)
    if h != cur:
        runs.append((x, h))
        cur = h
print("   run boundaries at y=%d:" % mid)
print("     " + "  ".join("x%d:%s" % (x, h) for x, h in runs if h))
res["probes"]["title_runs_y76"] = [{"x": x, "hex": h} for x, h in runs]

with open(OUT, "w") as f:
    json.dump(res, f, indent=1)
print("\nWROTE " + OUT)
