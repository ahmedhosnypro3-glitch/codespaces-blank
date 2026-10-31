#!/usr/bin/env python3
"""Slide 015 closed-loop landmark check: original 960x540 frame vs 150dpi render.

Original frame is 72px/in; render is 150px/in. SC = 150/72.
Tolerance = 4 original-px (per worker law).

Landmarks are PREDICTED from the build chain, then measured in BOTH images:
  gen_diagram_v2.py: canvas 12.3x4.4in placed at (0.5,1.3);
    node local cols x 1.50/5.43/7.60, local rows y 3.18/2.16/1.02, R 0.25
    => global node centres x 2.00/5.93/8.10, y 2.52/3.54/4.68 in
  slide_015_attempt2.js: error bar 10.96..11.26 x 2.08..5.04
    input/target boxes 0.89..1.79 / 11.36..12.25, y 1.33..1.74
    tan band 0.83..12.49 x 6.00..7.15 ; annotation row y 5.70..6.14

Position is measured with the DARK-INK centroid (black ring + sigma glyph) inside a
disc around each predicted node centre. Node FILL colours are reported as info only:
the original frame's fills are video-washed (measured hidden (208,248,176),
output (244,200,156)) against the nominal spec colours (#90EE90 / #FFA07A) - that is
video-compression artifact, ground rule (c), not a defect.
"""
from PIL import Image
import sys

ORIG = "unique_slides/slide_015.jpg"
RENDER = sys.argv[1]
o = Image.open(ORIG).convert("RGB")
r = Image.open(RENDER).convert("RGB")
OW, OH = 960, 540
RW, RH = r.size
SC = RW / OW
TOL = 4.0  # original-px
print(f"original {OW}x{OH}  render {RW}x{RH}  scale {SC:.4f}  tol {TOL} orig-px")
op, rp = o.load(), r.load()
FAILS = []


def in2(v):
    return v * 72


def disc_centroid(px, W, H, cx, cy, rad, pred):
    """Centroid + count of pred-matching pixels inside a disc."""
    x0, x1 = max(0, int(cx - rad)), min(W, int(cx + rad + 1))
    y0, y1 = max(0, int(cy - rad)), min(H, int(cy + rad + 1))
    sx = sy = n = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if (x - cx) ** 2 + (y - cy) ** 2 > rad * rad:
                continue
            if pred(px[x, y]):
                sx += x
                sy += y
                n += 1
    return (sx / n, sy / n, n) if n else None


def extent(px, W, H, x0, x1, y0, y1, pred):
    xs, ys = [], []
    for y in range(max(0, int(y0)), min(H, int(y1 + 1))):
        for x in range(max(0, int(x0)), min(W, int(x1 + 1))):
            if pred(px[x, y]):
                xs.append(x)
                ys.append(y)
    return (min(xs), min(ys), max(xs), max(ys), len(xs)) if xs else None


DARK = lambda p: max(p) < 110
SIGRED = lambda p: p[0] > 120 and p[0] - p[1] > 55 and p[0] - p[2] > 45
GREENISH = lambda p: p[1] > p[0] + 25 and p[1] > p[2] + 15
ORANGEISH = lambda p: p[0] > p[1] + 30 and p[1] > p[2] + 5


def node_check(name, cx_in, cy_in):
    """Position check via dark-ink centroid; fill reported as info."""
    pred = SIGRED
    R = 0.11  # tight disc: isolates the sigma glyph, excludes nearby red labels
    c_o = disc_centroid(op, OW, OH, in2(cx_in), in2(cy_in), in2(R), pred)
    c_r = disc_centroid(rp, RW, RH, cx_in * 72 * SC, cy_in * 72 * SC, in2(R) * SC, pred)
    if c_o is None or c_r is None:
        # fall back to dark ring ink
        c_o = disc_centroid(op, OW, OH, in2(cx_in), in2(cy_in), in2(0.20), DARK)
        c_r = disc_centroid(rp, RW, RH, cx_in * 72 * SC, cy_in * 72 * SC, in2(0.20) * SC, DARK)
        lbl = "ring"
    else:
        lbl = "sigma"
    if c_o is None or c_r is None:
        FAILS.append(f"{name}: no ink at predicted centre")
        print(f"{name}: FAIL no ink (orig={c_o and round(c_o[2])}, render={c_r and round(c_r[2])})")
        return
    ddx = abs(c_r[0] / SC - c_o[0])
    ddy = abs(c_r[1] / SC - c_o[1])
    ok = ddx <= TOL and ddy <= TOL
    print(f"{name} [{lbl}]: orig ({c_o[0]:.1f},{c_o[1]:.1f})  render ({c_r[0]/SC:.1f},{c_r[1]/SC:.1f})"
          f"  d=({ddx:.1f},{ddy:.1f})  {'OK' if ok else 'FAIL'}")
    if not ok:
        FAILS.append(f"{name}: centroid d=({ddx:.1f},{ddy:.1f}) > {TOL}")


print("--- node landmark positions (predicted x 2.00/5.93/8.10, y 2.52/3.54/4.68) ---")
for i, gy in enumerate([2.52, 3.54, 4.68]):
    node_check(f"input node  r{i+1}", 2.00, gy)
    node_check(f"hidden node r{i+1}", 5.93, gy)
    node_check(f"output node r{i+1}", 8.10, gy)

print("--- original fill colours (info: video-washed, not a defect) ---")
def dom_fill(cx_in, cy_in, rad=0.13):
    from collections import Counter
    c = Counter()
    cx, cy, rr = in2(cx_in), in2(cy_in), in2(rad)
    for y in range(int(cy - rr), int(cy + rr + 1)):
        for x in range(int(cx - rr), int(cx + rr + 1)):
            if (x - cx) ** 2 + (y - cy) ** 2 > rr * rr:
                continue
            p = op[x, y]
            if max(p) < 110 or SIGRED(p):
                continue
            c[(p[0] // 8 * 8, p[1] // 8 * 8, p[2] // 8 * 8)] += 1
    return c.most_common(1)[0][0] if c else None

for nm, cx in [("hidden", 5.93), ("output", 8.10)]:
    print(f"  orig {nm}-node dominant fill ~{dom_fill(cx, 3.54)}  (nominal spec "
          f"{'#90EE90' if nm == 'hidden' else '#FFA07A'})")

print("--- error bar extent ---")
eo = extent(op, OW, OH, in2(10.7), in2(11.5), in2(1.9), in2(5.2),
            lambda p: p[0] > 100 and p[0] - p[1] > 45 and p[0] - p[2] > 45)
er = extent(rp, RW, RH, 10.7 * 72 * SC, 11.5 * 72 * SC, 1.9 * 72 * SC, 5.2 * 72 * SC,
            lambda p: p[0] > 100 and p[0] - p[1] > 45 and p[0] - p[2] > 45)
print(f"  orig {eo}  render {er}")
if eo and er:
    dx = max(abs(er[0] / SC - eo[0]), abs(er[2] / SC - eo[2]))
    dy = max(abs(er[1] / SC - eo[1]), abs(er[3] / SC - eo[3]))
    print(f"  delta dx={dx:.1f} dy={dy:.1f} orig-px  {'OK' if dx <= TOL and dy <= TOL else 'FAIL'}")
    if dx > TOL or dy > TOL:
        FAILS.append(f"error bar extent d=({dx:.1f},{dy:.1f})")

# --- error bar caption: word COUNT and per-word position (the v2 defect) ---
# Original (rotated 90 deg readable) reads "Error Error Error": three white letter
# clusters inside the bar at orig-px y 185..222 / 241..278 / 290..329.
CAP_CLUSTERS = [(185, 222), (241, 278), (290, 329)]


def bar_interior(px, W, H, y0, y1):
    """Detect the dark-red bar's x extent from the render itself, then inset."""
    RED = lambda p: p[0] > 100 and p[0] - p[1] > 45 and p[0] - p[2] > 45
    xs = [x for y in range(max(0, int(y0)), min(H, int(y1 + 1)))
          for x in range(0, W) if RED(px[x, y])]
    if not xs:
        return None
    lo, hi = min(xs), max(xs)
    inset = max(2, int((hi - lo) * 0.12))
    return lo + inset, hi - inset


def letter_runs(px, W, H, x0, x1, y0, y1, gap):
    """Contiguous y-runs of white ink inside the bar, merged by gap px."""
    runs, cur = [], None
    for y in range(max(0, int(y0)), min(H, int(y1 + 1))):
        n = sum(1 for x in range(max(0, int(x0)), min(W, int(x1 + 1)))
                if px[x, y][0] > 200 and px[x, y][1] > 200 and px[x, y][2] > 200)
        if n >= 1:
            if cur is None:
                cur = [y, y]
            else:
                cur[1] = y
        else:
            if cur:
                runs.append(tuple(cur))
                cur = None
    if cur:
        runs.append(tuple(cur))
    merged = []
    for a in runs:
        if merged and a[0] - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], a[1])
        else:
            merged.append(a)
    return merged


# word gaps in the original are ~11-18 px; letter gaps <= ~6 px -> merge gap 9
GAP = 9
Y0, Y1 = 152, 360  # excludes the bar's own top/bottom edges
bi_o = bar_interior(op, OW, OH, Y0, Y1)
bi_r = bar_interior(rp, RW, RH, Y0 * SC, Y1 * SC)
print(f"  bar interior x: orig {bi_o}  render {[round(v/SC,1) for v in bi_r] if bi_r else None}")
co = letter_runs(op, OW, OH, bi_o[0], bi_o[1], Y0, Y1, GAP)
cr = letter_runs(rp, RW, RH, bi_r[0], bi_r[1], Y0 * SC, Y1 * SC, GAP)
cr = [(round(a / SC), round(b / SC)) for a, b in cr]
print(f"  caption clusters: orig {co}  render {cr}")
if len(cr) != len(CAP_CLUSTERS):
    FAILS.append(f"caption word count: render has {len(cr)} words, original has "
                 f"{len(CAP_CLUSTERS)} ('Error Error Error')")
    print(f"  FAIL: word count {len(cr)} != {len(CAP_CLUSTERS)}")
else:
    for i, ((cy0, cy1), (ry0, ry1)) in enumerate(zip(CAP_CLUSTERS, cr)):
        d = max(abs(ry0 - cy0), abs(ry1 - cy1))
        print(f"  word{i+1}: orig y{cy0}..{cy1}  render y{ry0}..{ry1}  d={d}px  "
              f"{'OK' if d <= TOL else 'FAIL'}")
        if d > TOL:
            FAILS.append(f"caption word{i+1} y d={d}px > {TOL}")

print("--- tan equation band (top + bottom edge) ---")
TAN = lambda p: p[0] > p[2] + 12 and 190 < p[0] < 254 and abs(p[0] - p[1]) < 40
bo = extent(op, OW, OH, in2(0.9), in2(12.4), in2(6.0), in2(7.12), TAN)
br = extent(rp, RW, RH, 0.9 * 72 * SC, 12.4 * 72 * SC, 6.0 * 72 * SC, 7.12 * 72 * SC, TAN)
print(f"  orig {bo}  render {br}")
if bo and br:
    dy_top = abs(br[1] / SC - bo[1])
    dy_bot = abs(br[3] / SC - bo[3])
    print(f"  edges dy_top={dy_top:.1f} dy_bottom={dy_bot:.1f}  "
          f"{'OK' if dy_top <= TOL and dy_bot <= TOL else 'FAIL'}")
    if dy_top > TOL or dy_bot > TOL:
        FAILS.append(f"tan band edges d=({dy_top:.1f},{dy_bot:.1f})")

print("--- input / target label boxes (purple-ish) ---")
PURP = lambda p: p[0] > p[1] + 18 and p[2] > p[1] + 18
for nm, (x0, x1) in [("Input Sample", (0.85, 1.82)), ("Target Label", (11.32, 12.30))]:
    eo = extent(op, OW, OH, in2(x0), in2(x1), in2(1.28), in2(1.80), PURP)
    er = extent(rp, RW, RH, x0 * 72 * SC, x1 * 72 * SC, 1.28 * 72 * SC, 1.80 * 72 * SC, PURP)
    print(f"  {nm}: orig {eo}  render {er}")
    if eo and er:
        dx = max(abs(er[0] / SC - eo[0]), abs(er[2] / SC - eo[2]))
        dy = max(abs(er[1] / SC - eo[1]), abs(er[3] / SC - eo[3]))
        print(f"     d=({dx:.1f},{dy:.1f})  {'OK' if dx <= TOL and dy <= TOL else 'FAIL'}")
        if dx > TOL or dy > TOL:
            FAILS.append(f"{nm} box d=({dx:.1f},{dy:.1f})")

print("--- house chrome ---")
bg = [rp[5, 5], rp[RW - 6, 5], rp[5, RH - 6], rp[RW - 6, RH - 6]]
print("  corners (expect 232,232,232):", bg)
if not all(all(abs(a - 232) <= 6 for a in s) for s in bg):
    FAILS.append(f"background not #E8E8E8: {bg}")
fy = round(0.15 * 72 * SC)
band = [rp[x, fy] for x in range(round(30 * SC), round(300 * SC), 3)]
reds = sum(1 for s in band if s[0] > 150 and s[1] < 90 and s[2] < 90)
print(f"  top red frame y={fy}: {reds}/{len(band)} red")
if reds < len(band) * 0.6:
    FAILS.append("outer red frame missing on top edge")
bx0, by0 = round(12.48 * 72 * SC), round(0.30 * 72 * SC)
bx1, by1 = round(12.98 * 72 * SC), round(0.80 * 72 * SC)
badge = [rp[x, y] for y in range(by0, by1, 3) for x in range(bx0, bx1, 3)]
yels = sum(1 for s in badge if s[0] > 235 and s[1] > 225 and s[2] < 230)
print(f"  yellow badge: {yels}/{len(badge)} yellow-ish")
if yels < len(badge) * 0.3:
    FAILS.append("yellow badge missing at house position")

print()
print("PIL CHECK:", "PASS" if not FAILS else "FAIL")
for f in FAILS:
    print("  -", f)
sys.exit(1 if FAILS else 0)
