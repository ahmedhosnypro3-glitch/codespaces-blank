# finer ground-truth measurements for slide_030 original
from PIL import Image
import collections

im = Image.open("unique_slides/slide_030.jpg").convert("RGB")
W, H = im.size
px = im.load()

def red(c):
    r, g, b = c
    return r > 140 and g < 95 and b < 95 and (r - g) > 55

def pink(c):
    r, g, b = c
    return 225 < r < 255 and 185 < g < 215 and 155 < b < 190

def blue(c):
    r, g, b = c
    return b > 120 and b - r > 45 and b - g > 45

def green(c):
    r, g, b = c
    return g > 110 and g - r > 40 and g - b > 40

def bbox(fn):
    pts = [(x, y) for y in range(H) for x in range(W) if fn(px[x, y])]
    if not pts:
        return None, 0
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return (min(xs), max(xs), min(ys), max(ys)), len(pts)

for name, fn in [("red", red), ("pink", pink), ("blue", blue), ("green", green)]:
    print(name, bbox(fn))

# rows/cols for red ink (panel border + house frame)
rr = [y for y in range(H) if sum(1 for x in range(W) if red(px[x, y])) > 40]
print("red rows>40:", rr)
cc = [x for x in range(W) if sum(1 for y in range(H) if red(px[x, y])) > 40]
print("red cols>40:", cc)

# thin-line version for panel border
rr2 = [y for y in range(H) if sum(1 for x in range(W) if red(px[x, y])) > 12]
cc2 = [x for x in range(W) if sum(1 for y in range(H) if red(px[x, y])) > 12]
print("red rows>12:", rr2[:6], "...", rr2[-6:] if len(rr2) > 6 else "")
print("red cols>12:", cc2[:6], "...", cc2[-6:] if len(cc2) > 6 else "")

# blue/green line rows (equation box borders)
bl = [y for y in range(H) if sum(1 for x in range(W) if blue(px[x, y])) > 60]
gl = [y for y in range(H) if sum(1 for x in range(W) if green(px[x, y])) > 60]
print("blue rows>60:", bl)
print("green rows>60:", gl)
blx = [x for x in range(W) if sum(1 for y in range(H) if blue(px[x, y])) > 40]
glx = [x for x in range(W) if sum(1 for y in range(H) if green(px[x, y])) > 40]
print("blue cols>40:", blx)
print("green cols>40:", glx)
