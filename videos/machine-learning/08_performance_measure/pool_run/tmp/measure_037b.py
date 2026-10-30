"""Deeper measurement of slide_037.jpg: frame rect, badge, plot area, curves, annotations."""
from PIL import Image
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()

def near(c1, c2, tol):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

def bbox_of(pred, x0=0, y0=0, x1=W, y1=H):
    bx0, by0, bx1, by1 = W, H, -1, -1
    cnt = 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            if pred(px[x, y]):
                cnt += 1
                if x < bx0: bx0 = x
                if x > bx1: bx1 = x
                if y < by0: by0 = y
                if y > by1: by1 = y
    return (bx0, by0, bx1, by1, cnt) if cnt else None

# 1. outer frame: strong red pixels (#C00000-ish) — find long straight lines
red = lambda p: p[0] > 130 and p[0] > p[1] + 70 and p[0] > p[2] + 70
# scan rows/cols for red runs
def red_runs_row(y):
    runs = []; x = 0
    while x < W:
        if red(px[x, y]):
            s = x
            while x < W and red(px[x, y]): x += 1
            if x - s > 100: runs.append((s, x - 1))
        else: x += 1
    return runs
def red_runs_col(x):
    runs = []; y = 0
    while y < H:
        if red(px[x, y]):
            s = y
            while y < H and red(px[x, y]): y += 1
            if y - s > 100: runs.append((s, y - 1))
        else: y += 1
    return runs
print("long red horizontal runs:")
for y in range(0, H, 4):
    r = red_runs_row(y)
    if r: print("  y=%d" % y, r)
print("long red vertical runs:")
for x in range(0, W, 4):
    r = red_runs_col(x)
    if r: print("  x=%d" % x, r)

# 2. badge: yellow circle top-right
yel = lambda p: p[0] > 200 and p[1] > 190 and p[2] < 150
print("yellow bbox:", bbox_of(yel))
# badge center approx
bb = bbox_of(yel)
if bb:
    print("badge center=(%d,%d) r~%d" % ((bb[0]+bb[2])//2, (bb[1]+bb[3])//2, (bb[2]-bb[0])//2))

# 3. plot area: light blue fill (#F0F8FF-ish) — find large region of near (240,248,255)
lb = lambda p: abs(p[0]-240)<12 and abs(p[1]-248)<10 and abs(p[2]-255)<8
bb = bbox_of(lb)
print("lightblue plot bbox:", bb)

# 4. axes: dark lines within plot; find the axis rectangle (black lines)
# scan for long dark horizontal/vertical lines below y=200
dark = lambda p: sum(p) < 330
def dark_runs_row(y, x0=0, x1=W, minlen=80):
    runs = []; x = x0
    while x < x1:
        if dark(px[x, y]):
            s = x
            while x < x1 and dark(px[x, y]): x += 1
            if x - s > minlen: runs.append((s, x - 1))
        else: x += 1
    return runs
def dark_runs_col(x, y0=0, y1=H, minlen=80):
    runs = []; y = y0
    while y < y1:
        if dark(px[x, y]):
            s = y
            while y < y1 and dark(px[x, y]): y += 1
            if y - s > minlen: runs.append((s, y - 1))
        else: y += 1
    return runs
print("long dark horizontal lines (y>=180):")
for y in range(180, H):
    r = dark_runs_row(y, minlen=150)
    if r: print("  y=%d" % y, r)
print("long dark vertical lines (x in plot):")
for x in range(150, 750):
    r = dark_runs_col(x, 180, H, minlen=100)
    if r: print("  x=%d" % x, r)
