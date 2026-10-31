# PIL ground-truth measurements for slide_030 original
from PIL import Image
import collections

im = Image.open("unique_slides/slide_030.jpg").convert("RGB")
W, H = im.size
px = im.load()

def dom(crop, n=6):
    c = collections.Counter(crop.getdata())
    return c.most_common(n)

def box(x0, y0, x1, y1):
    return im.crop((x0, y0, x1, y1))

# 1. locate red frames (C00000-ish)
redrows = collections.Counter()
for y in range(H):
    n = 0
    for x in range(W):
        r, g, b = px[x, y]
        if r > 150 and g < 90 and b < 90:
            n += 1
    if n > 100:
        redrows[y] = n
print("strong red rows:", sorted(redrows.items())[:12])

redcols = collections.Counter()
for x in range(W):
    n = 0
    for y in range(H):
        r, g, b = px[x, y]
        if r > 150 and g < 90 and b < 90:
            n += 1
    if n > 100:
        redcols[x] = n
print("strong red cols:", sorted(redcols.items())[:12])

# background mean
sm = im.resize((60, 34))
print("bg mean:", tuple(round(v) for v in sm.resize((1,1)).getpixel((0,0))))

# 2. pink F8CBAD-ish region (Bad Weights button)
pink = []
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if abs(r-0xF8) < 22 and abs(g-0xCB) < 22 and abs(b-0xAD) < 22:
            pink.append((x, y))
if pink:
    xs = [p[0] for p in pink]; ys = [p[1] for p in pink]
    print("pink bbox x", min(xs), max(xs), "y", min(ys), max(ys), "count", len(pink))

# 3. blue-ish and green-ish ink
def inkcount(fn, box=None):
    r_ = box or (0, 0, W, H)
    n = 0
    pts = []
    for y in range(r_[1], r_[3]):
        for x in range(r_[0], r_[2]):
            if fn(px[x, y]):
                n += 1
                pts.append((x, y))
    return n, pts

# green equation box borders
gpts = [(x, y) for y in range(H) for x in range(W) if (lambda p: p[1] > 120 and p[0] < 110 and p[2] < 110)(px[x, y])]
print("green ink count", len(gpts))
if gpts:
    xs = [p[0] for p in gpts]; ys = [p[1] for p in gpts]
    print("green bbox", min(xs), max(xs), min(ys), max(ys))

bpts = [(x, y) for y in range(H) for x in range(W) if (lambda p: p[2] > 140 and p[0] < 110 and p[1] < 110)(px[x, y])]
print("blue ink count", len(bpts))
if bpts:
    xs = [p[0] for p in bpts]; ys = [p[1] for p in bpts]
    print("blue bbox", min(xs), max(xs), min(ys), max(ys))
