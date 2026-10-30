"""Measure slide_037: badge, frame verticals, plot contents (curves/annotations/arrows/text rows)."""
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

# badge: dense yellow in top-right quadrant
yel = lambda p: p[0] > 200 and p[1] > 185 and p[2] < 160
bb = bbox_of(yel, 820, 0, 960, 120)
print("badge bbox (top-right):", bb)
if bb:
    cx, cy = (bb[0]+bb[2])/2, (bb[1]+bb[3])/2
    print("badge center=(%.0f,%.0f) w=%d h=%d" % (cx, cy, bb[2]-bb[0], bb[3]-bb[1]))

# frame verticals: long dark vertical lines full height
dark = lambda p: sum(p) < 330
def vruns(x, y0=0, y1=H, minlen=200):
    runs = []; y = y0
    while y < y1:
        if dark(px[x, y]):
            s = y
            while y < y1 and dark(px[x, y]): y += 1
            if y - s > minlen: runs.append((s, y - 1))
        else: y += 1
    return runs
print("long dark vertical lines (full height):")
for x in range(W):
    r = vruns(x)
    if r: print("  x=%d" % x, r)

def hruns(y, x0=0, x1=W, minlen=200):
    runs = []; x = x0
    while x < x1:
        if dark(px[x, y]):
            s = x
            while x < x1 and dark(px[x, y]): x += 1
            if x - s > minlen: runs.append((s, x - 1))
        else: x += 1
    return runs
print("long dark horizontal lines (full width):")
for y in range(H):
    r = hruns(y)
    if r: print("  y=%d" % y, r)

# title text rows (dark) y<120
print("dark row counts y<130 (n>20):")
for y in range(0, 130):
    n = sum(1 for x in range(W) if dark(px[x, y]))
    if n > 20: print("  y=%d n=%d" % (y, n))

# text block region: white box? find rows 130-220
print("dark row counts 130..230 (n>20):")
for y in range(130, 230):
    n = sum(1 for x in range(W) if dark(px[x, y]))
    if n > 20: print("  y=%d n=%d" % (y, n))

# colored ink bboxes within plot region (259,217)-(632,512)
mag = lambda p: p[0] > 100 and p[2] > 100 and p[1] < p[0] - 50 and p[1] < p[2] - 50
grn = lambda p: p[1] > 100 and p[1] > p[0] + 50 and p[1] > p[2] + 40
blu = lambda p: p[2] > 120 and p[2] > p[0] + 60 and p[2] > p[1] + 50
red = lambda p: p[0] > 130 and p[0] > p[1] + 70 and p[0] > p[2] + 70
yel2 = lambda p: p[0] > 210 and p[1] > 200 and p[2] < 120
for name, pred in [("magenta", mag), ("green", grn), ("blue", blu), ("red", red), ("yellow", yel2)]:
    bb = bbox_of(pred, 150, 180, 960, 540)
    print(name, "bbox in lower half:", bb)
