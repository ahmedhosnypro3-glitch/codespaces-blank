"""Extract curve polylines + fill color + arrow geometry from slide_037 plot."""
from PIL import Image
from collections import Counter
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()
PL, PT, PR, PB = 259, 217, 632, 512

mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
grn = lambda p: p[1] > 100 and p[1] > p[0] + 50 and p[1] > p[2] + 40
blu = lambda p: p[2] > 120 and p[2] > p[0] + 60 and p[2] > p[1] + 50

# dominant background color inside plot
c = Counter()
for y in range(PT + 3, PB - 2, 3):
    for x in range(PL + 3, PR - 2, 3):
        c[px[x, y]] += 1
print("plot interior dominant colors:", ["#%02X%02X%02X:%d" % (k + (v,)) for k, v in c.most_common(6)])

# fill under magenta curve: sample region y 300..505 x 320..500 dominant non-dark color
c = Counter()
for y in range(300, 505, 2):
    for x in range(320, 500, 2):
        p = px[x, y]
        if sum(p) > 500:
            c[p] += 1
print("below-curve region colors:", ["#%02X%02X%02X:%d" % (k + (v,)) for k, v in c.most_common(6)])

# dense magenta polyline (exclude text rows 228..266)
def poly(pred, step=4, exclude=()):
    pts = []
    for x in range(PL, PR + 1, step):
        ys = [y for y in range(PT, PB + 1) if pred(px[x, y]) and not any(a <= y <= b for a, b in exclude)]
        if ys:
            pts.append((x, round(sum(ys) / len(ys), 1)))
    return pts
print("MAGENTA polyline (excl text 228-266):")
print(poly(mag, 6, [(228, 266)]))
print("GREEN polyline (excl text 228-266):")
print(poly(grn, 6, [(228, 266)]))
print("BLUE polyline (excl text 285-380):")
print(poly(blu, 6, [(285, 380)]))

# find straight lines from origin: for angles, count colored px along ray from (259,512)
import math
def ray(pred, ang_deg, rmax=380):
    hits = 0
    for r in range(5, rmax, 2):
        x = int(PL + r * math.cos(math.radians(ang_deg)))
        y = int(PB - r * math.sin(math.radians(ang_deg)))
        if 0 <= x < W and 0 <= y < H and pred(px[x, y]):
            hits += 1
    return hits
print("green ray hits by angle (deg from +x):")
for a in range(10, 90, 5):
    print("  a=%d hits=%d" % (a, ray(grn, a)))
print("blue ray hits by angle:")
for a in range(10, 90, 5):
    print("  a=%d hits=%d" % (a, ray(blu, a)))
print("magenta ray hits by angle:")
for a in range(30, 90, 5):
    print("  a=%d hits=%d" % (a, ray(mag, a)))
