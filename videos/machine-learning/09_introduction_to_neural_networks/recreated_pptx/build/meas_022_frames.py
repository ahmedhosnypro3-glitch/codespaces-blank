from PIL import Image
im = Image.open("/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_022.jpg").convert("RGB")
W, H = im.size
px = im.load()

def p(x, y): return "#%02X%02X%02X" % px[x, y]

print("corner (2,2)", p(2,2), " (5,5)", p(5,5), " (10,10)", p(10,10))
print("bottom strip (10,530)", p(10,530), " (300,530)", p(300,530))
print("top edge row y=1..8:", [(y, p(300,y)) for y in range(0,10)])

# scan down column x=84 (left panel left edge region) from y=108 to y=500
print("\n-- column x=82..90 at y=150, row1 left panel border --")
for x in range(78, 96):
    print(x, p(x, 150))

# right panel border x~825
print("\n-- right panel border at y=150 --")
for x in range(815, 840):
    print(x, p(x, 150))

# find blue frame: scan rows for strongly blue pixels
print("\n-- scan for blue frame strokes (b - r > 25) --")
from collections import Counter
c = Counter()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if b - r > 25 and b - g > 10:
            c[(x, y)] += 1
# histogram of rows/cols
rows = Counter(); cols = Counter()
for (x, y) in c:
    rows[y] += 1; cols[x] += 1
print("blue rows top:", rows.most_common(12))
print("blue cols left:", cols.most_common(12))

# crimson frame (r > 150, g < 90, b < 90)
c2 = Counter()
rr = Counter(); cc = Counter()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if r > 150 and g < 90 and b < 90:
            c2[(x, y)] += 1; rr[y] += 1; cc[x] += 1
print("\ncrimson rows:", rr.most_common(10))
print("crimson cols:", cc.most_common(10))

# green pixels
c3r = Counter(); c3c = Counter()
for y in range(H):
    for x in range(W):
        r, g, b = px[x, y]
        if g > 120 and g - r > 40 and g - b > 40:
            c3r[y] += 1; c3c[x] += 1
print("\ngreen rows:", c3r.most_common(14))
print("green cols:", c3c.most_common(10))

# yellow badge: scan top-right region for saturated pale yellow
print("\n-- top-right region x 780-880, y 20-120 --")
for y in range(30, 120, 5):
    rowout = []
    for x in range(790, 890, 10):
        rowout.append(p(x, y))
    print(y, rowout)
