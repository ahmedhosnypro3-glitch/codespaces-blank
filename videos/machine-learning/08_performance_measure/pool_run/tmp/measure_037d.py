"""Measure slide_037: text lines, plot curves (per-color polylines), annotations, arrows, axes labels."""
from PIL import Image
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()

def bbox_of(pred, x0=0, y0=0, x1=W, y1=H):
    bx0, by0, bx1, by1 = W, H, -1, -1
    cnt = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                cnt += 1
                bx0 = min(bx0, x); bx1 = max(bx1, x); by0 = min(by0, y); by1 = max(by1, y)
    return (bx0, by0, bx1, by1, cnt) if cnt else None

dark = lambda p: sum(p) < 330
# text line bands: group dark rows in regions
def bands(y0, y1, min_n=15, min_gap=4):
    rows = [sum(1 for x in range(W) if dark(px[x, y])) for y in range(y0, y1)]
    out = []
    s = None
    for i, n in enumerate(rows):
        if n > min_n:
            if s is None: s = i
        else:
            if s is not None:
                out.append((y0 + s, y0 + i - 1))
                s = None
    if s is not None: out.append((y0 + s, y1 - 1))
    # merge close
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= min_gap:
            merged[-1] = (merged[-1][0], b[1])
        else:
            merged.append(b)
    return merged

print("TITLE band y<60:", bands(44, 64, 15))
print("SUBTITLE bands 60..130:", bands(60, 130, 15))
print("BODY bands 130..216:", bands(130, 216, 15))
print("below plot 513..517:", bands(513, 517, 10))

# horizontal extent of each text band
def band_xext(y0, y1):
    xs = [x for y in range(y0, y1) for x in range(W) if dark(px[x, y])]
    return (min(xs), max(xs)) if xs else None
for label, (a, b) in [("title", (44, 64)), ("sub", (60, 130)), ("body", (130, 216))]:
    for (y0, y1) in bands(a, b, 15):
        print(label, "band y=%d..%d xext=" % (y0, y1), band_xext(y0, y1 + 1))

# plot interior
PL, PT, PR, PB = 259, 217, 632, 512
mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
grn = lambda p: p[1] > 100 and p[1] > p[0] + 50 and p[1] > p[2] + 40
blu = lambda p: p[2] > 120 and p[2] > p[0] + 60 and p[2] > p[1] + 50
yel = lambda p: p[0] > 200 and p[1] > 190 and p[2] < 140
print("plot-region color bboxes (within 259..632 x 217..512, plus margins):")
for name, pred in [("magenta", mag), ("green", grn), ("blue", blu), ("yellow", yel)]:
    print(" ", name, bbox_of(pred, 150, 180, 960, 516))

# sample magenta curve points: for each x in plot, mean y of magenta pixels
def curve_samples(pred, x0, x1, y0, y1, step=8):
    pts = []
    for x in range(x0, x1, step):
        ys = [y for y in range(y0, y1) if pred(px[x, y])]
        if ys:
            pts.append((x, sum(ys) / len(ys), min(ys), max(ys), len(ys)))
    return pts
print("magenta curve samples (x, meany, miny, maxy, n):")
for t in curve_samples(mag, PL, PR + 1, PT, PB + 1, 12):
    print("   ", t)
print("green curve samples:")
for t in curve_samples(grn, PL, PR + 1, PT, PB + 1, 12):
    print("   ", t)
print("blue curve samples:")
for t in curve_samples(blu, PL, PR + 1, PT, PB + 1, 12):
    print("   ", t)

# yellow fill: bbox + coverage
yb = bbox_of(yel, PL, PT, PR, PB)
print("yellow fill bbox in plot:", yb)
# count yellow pixels per row in plot
print("yellow rows in plot (y:count>5):")
for y in range(PT, PB + 1):
    n = sum(1 for x in range(PL, PR + 1) if yel(px[x, y]))
    if n > 5: print("   y=%d n=%d" % (y, n))
