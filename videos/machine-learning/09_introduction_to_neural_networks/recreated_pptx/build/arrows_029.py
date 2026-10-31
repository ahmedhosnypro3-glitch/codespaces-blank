from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
px = im.load()
SW = 13.33

def tin(x):
    return round(x / w * SW, 2)

def tint(y):
    return round(y / h * 7.5, 2)

blue = lambda c: c[2] > c[0] + 45 and c[2] > 130 and c[0] < 110
green = lambda c: c[1] > c[0] + 45 and c[1] > c[2] + 45 and c[1] > 110

print("== BLUE stroke pixels in band y 4.8-5.7in ==")
from collections import defaultdict
byx = defaultdict(int)
for y in range(int(4.8 / 7.5 * h), int(5.7 / 7.5 * h)):
    for x in range(w):
        if blue(px[(x, y)]):
            byx[x] += 1
xs = [x for x, n in byx.items() if n >= 2]
if xs:
    print(f"  x range {tin(min(xs))}-{tin(max(xs))} in")
    prev = None
    for x in sorted(byx):
        if byx[x] >= 2:
            if prev is None or x - prev > 3:
                print(f"   group starts x={tin(x)}")
            prev = x
    print(f"   group ends x={tin(prev)}")
    ys = [y for y in range(int(4.8 / 7.5 * h), int(5.7 / 7.5 * h)) for x in range(w) if byx.get(x, 0) >= 2 and blue(px[(x, y)])]
    if ys:
        print(f"  y span {tint(min(ys))}-{tint(max(ys))} in")

print("\n== GREEN stroke pixels in band y 4.8-5.7in ==")
byx = defaultdict(int)
for y in range(int(4.8 / 7.5 * h), int(5.7 / 7.5 * h)):
    for x in range(w):
        if green(px[(x, y)]):
            byx[x] += 1
xs = [x for x, n in byx.items() if n >= 2]
if xs:
    prev = None
    print(f"  x range {tin(min(xs))}-{tin(max(xs))} in")
    for x in sorted(byx):
        if byx[x] >= 2:
            if prev is None or x - prev > 3:
                print(f"   group starts x={tin(x)}")
            prev = x
    print(f"   group ends x={tin(prev)}")
    ys = [y for y in range(int(4.8 / 7.5 * h), int(5.7 / 7.5 * h)) for x in range(w) if byx.get(x, 0) >= 2 and green(px[(x, y)])]
    if ys:
        print(f"  y span {tint(min(ys))}-{tint(max(ys))} in")

print("\n== beige panel exact bounds ==")
beige = lambda c: 195 < c[0] < 250 and 185 < c[1] < 240 and 145 < c[2] < 215 and c[0] - c[2] > 16
cnt = defaultdict(int)
for y in range(h):
    for x in range(w):
        if beige(px[(x, y)]):
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > 200)
ys = [y for y in range(h) for x in range(xs[0], xs[-1] + 1, 7) if beige(px[(x, y)])]
print(f"  panel x {tin(xs[0])}-{tin(xs[-1])} in, y {tint(min(ys))}-{tint(max(ys))} in")

print("\n== diagram node columns: red sigma cells inside panel ==")
redsig = lambda c: c[0] > 150 and c[0] - c[1] > 90 and c[0] - c[2] > 90
cnt = defaultdict(int)
for y in range(int(1.9 / 7.5 * h), int(5.4 / 7.5 * h)):
    for x in range(int(1.0 / 13.33 * w), int(7.5 / 13.33 * w)):
        if redsig(px[(x, y)]):
            cnt[x] += 1
runs = []
prev = None
for x in sorted(cnt):
    if cnt[x] >= 2:
        if prev is None or x - prev > 4:
            runs.append([x, x])
        else:
            runs[-1][1] = x
        prev = x
print("  red-sigma x bands:", [(tin(a), tin(b)) for a, b in runs])
