"""PIL measurement of slide_037.jpg (960x540): colors, border, badge, ink regions."""
from PIL import Image
from collections import Counter
import sys

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/08_performance_measure"
im = Image.open(f"{NS}/unique_slides/slide_037.jpg").convert("RGB")
W, H = im.size
px = im.load()
print("size", W, H)

# dominant colors
c = Counter()
for y in range(0, H, 2):
    for x in range(0, W, 2):
        c[px[x, y]] += 1
print("top colors:")
for col, n in c.most_common(25):
    print("  #%02X%02X%02X" % col, n)

def near(c1, c2, tol=40):
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

def bbox_of(pred):
    x0, y0, x1, y1 = W, H, -1, -1
    cnt = 0
    for y in range(H):
        for x in range(W):
            if pred(px[x, y]):
                cnt += 1
                if x < x0: x0 = x
                if x > x1: x1 = x
                if y < y0: y0 = y
                if y > y1: y1 = y
    return (x0, y0, x1, y1, cnt) if cnt else None

# non-background ink (bg is near-white)
print("non-white bbox:", bbox_of(lambda p: not near(p, (255, 255, 255), 18)))
# dark ink (text/lines)
print("dark bbox:", bbox_of(lambda p: sum(p) < 260))
# red-ish (frame/title)
print("red bbox:", bbox_of(lambda p: p[0] > 120 and p[0] > p[1] + 60 and p[0] > p[2] + 60))
# blue-ish
print("blue bbox:", bbox_of(lambda p: p[2] > 110 and p[2] > p[0] + 50 and p[2] > p[1] + 40))
# magenta/purple
print("magenta bbox:", bbox_of(lambda p: p[0] > 90 and p[2] > 90 and p[1] < p[0] - 40 and p[1] < p[2] - 40))
# green
print("green bbox:", bbox_of(lambda p: p[1] > 90 and p[1] > p[0] + 40 and p[1] > p[2] + 30))
# yellow
print("yellow bbox:", bbox_of(lambda p: p[0] > 180 and p[1] > 170 and p[2] < 130))
# light blue bg (plot area #F0F8FF-ish)
print("lightblue bbox:", bbox_of(lambda p: p[2] > 235 and p[0] > 225 and p[1] > 235 and p[2] >= p[0]))

# row/col ink profiles for dark pixels to find text rows and chart box
def row_profile(pred):
    rows = []
    for y in range(H):
        n = sum(1 for x in range(W) if pred(px[x, y]))
        rows.append(n)
    return rows

dark = row_profile(lambda p: sum(p) < 300)
print("dark rows (y:count) with count>30:")
for y, n in enumerate(dark):
    if n > 30:
        print("  y=%d n=%d" % (y, n))
