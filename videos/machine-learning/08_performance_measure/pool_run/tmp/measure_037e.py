"""Measure slide_037: text bands interior extents+colors, axis labels, plot contents, annotations, shaded fill."""
from PIL import Image
from collections import Counter
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()

def near(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

dark = lambda p: sum(p) < 330

def band_rows(y0, y1, min_n=12):
    out = []
    rows = [sum(1 for x in range(70, 890) if dark(px[x, y])) for y in range(y0, y1)]
    s = None
    for i, n in enumerate(rows):
        if n > min_n:
            if s is None: s = i
        else:
            if s is not None:
                out.append((y0 + s, y0 + i - 1)); s = None
    if s is not None: out.append((y0 + s, y1 - 1))
    merged = []
    for b in out:
        if merged and b[0] - merged[-1][1] <= 5: merged[-1] = (merged[-1][0], b[1])
        else: merged.append(list(b) if False else b)
    return merged

def band_info(y0, y1):
    for (a, b) in band_rows(y0, y1):
        xs = [x for y in range(a, b + 1) for x in range(70, 890) if dark(px[x, y])]
        cols = Counter(px[x, y] for y in range(a, b + 1) for x in range(70, 890) if dark(px[x, y]))
        top = cols.most_common(2)
        print("  band y=%d..%d x=%d..%d h=%d topcolors=%s" % (a, b, min(xs), max(xs), b - a + 1, ["#%02X%02X%02X:%d" % (c + (n,)) for c, n in top]))

print("== text bands above plot (interior x 70..890) ==")
band_info(44, 216)

# colors of specific bands
def dom_color(y0, y1, pred):
    c = Counter()
    for y in range(y0, y1 + 1):
        for x in range(70, 890):
            if pred(px[x, y]): c[px[x, y]] += 1
    return c.most_common(3)
red = lambda p: p[0] > 120 and p[0] > p[1] + 60 and p[0] > p[2] + 60
blue = lambda p: p[2] > 110 and p[2] > p[0] + 50 and p[2] > p[1] + 40
print("title 65-80 red?", dom_color(65, 80, red), "blue?", dom_color(65, 80, blue))
print("sub 100-115 blue?", dom_color(100, 115, blue))
print("body 154-170 dark:", dom_color(154, 170, lambda p: sum(p) < 330))
print("body 186-198 dark:", dom_color(186, 198, lambda p: sum(p) < 330))

# badge interior: numeral color
print("badge 861-893 x 58-84 dark:", dom_color(58, 84, lambda p: sum(p) < 330), "yellow:", dom_color(58, 84, lambda p: p[0]>200 and p[1]>185 and p[2]<160))

# plot region details
PL, PT, PR, PB = 259, 217, 632, 512
# shaded fill: look for pale yellow / cream in plot
def fill_rows():
    for y in range(PT, PB + 1):
        c = Counter()
        for x in range(PL + 2, PR - 1):
            p = px[x, y]
            if not (sum(p) < 500) and not near(p, (240, 248, 255), 14) and not near(p, (255, 255, 255), 10):
                c[p] += 1
        if c:
            top = c.most_common(1)[0]
            if top[1] > 30:
                print("  y=%d fill #%02X%02X%02X n=%d" % (y, top[0][0], top[0][1], top[0][2], top[1]))
print("== plot fill rows ==")
fill_rows()

# grid: gray lines inside plot
gray = lambda p: abs(p[0]-p[1])<12 and abs(p[1]-p[2])<12 and 150 < p[0] < 235
print("grid vertical x positions (count of gray px per col > 60):")
for x in range(PL, PR + 1):
    n = sum(1 for y in range(PT, PB + 1) if gray(px[x, y]))
    if n > 60: print("   x=%d n=%d" % (x, n))
print("grid horizontal y positions (count > 60):")
for y in range(PT, PB + 1):
    n = sum(1 for x in range(PL, PR + 1) if gray(px[x, y]))
    if n > 60: print("   y=%d n=%d" % (y, n))

# axis labels: TPR left of plot (x<259), FPR below plot (y>512)
print("ink left of plot (x 200..258, y 217..512):")
xs = [x for y in range(PT, PB+1) for x in range(200, 259) if dark(px[x, y])]
ys = [y for y in range(PT, PB+1) for x in range(200, 259) if dark(px[x, y])]
if xs: print("  bbox x=%d..%d y=%d..%d" % (min(xs), max(xs), min(ys), max(ys)))
print("  TPR color:", dom_color(min(ys) if ys else PT, max(ys) if ys else PT, red) if ys else None)
print("ink below plot (y 513..540, x 259..700):")
xs = [x for y in range(513, 540) for x in range(259, 700) if dark(px[x, y])]
ys = [y for y in range(513, 540) for x in range(259, 700) if dark(px[x, y])]
if xs: print("  bbox x=%d..%d y=%d..%d" % (min(xs), max(xs), min(ys), max(ys)))
if ys: print("  FPR color red?:", dom_color(min(ys), max(ys), red))

# annotations: colored text outside/inside plot. magenta text above plot (y 217..260?), blue text right (x>632)
mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
blu = lambda p: p[2] > 120 and p[2] > p[0] + 60 and p[2] > p[1] + 50
def bbox_of(pred, x0, y0, x1, y1):
    bx0, by0, bx1, by1 = W, H, -1, -1
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                bx0 = min(bx0, x); bx1 = max(bx1, x); by0 = min(by0, y); by1 = max(by1, y)
    return (bx0, by0, bx1, by1) if bx1 >= 0 else None
print("magenta ink overall:", bbox_of(mag, 0, 0, W, H))
print("magenta above plot y<217:", bbox_of(mag, 0, 180, 960, 217))
print("blue ink right of plot x>632 y 217..516:", bbox_of(blu, 633, 217, 960, 516))
print("blue ink above plot y<217 x 0..960:", bbox_of(blu, 0, 150, 960, 217))
