# locate elements in original slide_030 and report ink colors per region
from PIL import Image
import collections

im = Image.open("unique_slides/slide_030.jpg").convert("RGB")
W, H = im.size
px = im.load()

def cls(c):
    r, g, b = c
    if r > 215 and g > 175 and b < 180: return "yellow"
    if r > 210 and 140 < g < 210 and b < 185: return "orange"
    if r > 230 and g > 230 and b > 230: return "white"
    if abs(r - 232) < 26 and abs(g - 232) < 26 and abs(b - 230) < 28: return "bg"
    if r > 140 and g < 100 and b < 100: return "red"
    if b > 120 and b - r > 45 and b - g > 45: return "blue"
    if g > 105 and g - r > 38 and g - b > 38: return "green"
    if (r + g + b) < 300: return "black"
    return "other"

# 1. yellow circles (hidden nodes) and orange circles (output nodes)
ys = collections.defaultdict(list)
for y in range(H):
    for x in range(W):
        k = cls(px[x, y])
        if k in ("yellow", "orange"):
            ys[k].append((x, y))
for k, pts in ys.items():
    xs = [p[0] for p in pts]; yy = [p[1] for p in pts]
    print(k, "count", len(pts), "bbox x", min(xs), max(xs), "y", min(yy), max(yy))
    # cluster by x
    xs_sorted = sorted(set(xs))
    groups = []
    cur = [xs_sorted[0]]
    for a in xs_sorted[1:]:
        if a - cur[-1] <= 4:
            cur.append(a)
        else:
            groups.append((cur[0], cur[-1])); cur = [a]
    groups.append((cur[0], cur[-1]))
    print("   x clusters:", groups)

def hist(box, label):
    c = collections.Counter(cls(px[x, y]) for y in range(box[1], box[3]) for x in range(box[0], box[2]))
    print(label, box, dict(c.most_common(8)))

# 2. weight-label region between inputs and hidden nodes
hist((150, 90, 300, 230), "left-weight region")
# 3. region just right of output nodes
hist((640, 90, 780, 230), "right-of-output region")
# 4. title region
hist((60, 40, 260, 80), "title region")
# 5. badge region
hist((880, 20, 950, 70), "badge region")
