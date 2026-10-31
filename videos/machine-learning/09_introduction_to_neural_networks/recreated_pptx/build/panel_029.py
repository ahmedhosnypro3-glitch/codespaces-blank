from PIL import Image
from collections import defaultdict

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
px = im.load()
SW, SH = 13.33, 7.5

def tx(x):
    return round(x / w * SW, 2)
def ty(y):
    return round(y / h * SH, 2)

beige = lambda c: 200 < c[0] < 250 and 190 < c[1] < 242 and 150 < c[2] < 218 and c[0] - c[2] > 16

print("== panel y extent (x limited to 0.94-7.55in) ==")
x0, x1 = int(0.94 / SW * w), int(7.55 / SW * w)
ys = [y for y in range(h) if sum(1 for x in range(x0, x1, 4) if beige(px[(x, y)])) > (x1 - x0) / 4 * 0.55]
runs = []
for y in ys:
    if runs and y - runs[-1][-1] <= 3:
        runs[-1].append(y)
    else:
        runs.append([y])
for r in runs:
    print(f"  y run {ty(r[0])}-{ty(r[-1])} in (h={(r[-1]-r[0])/h*SH:.2f})")

print("\n== panel x extent (y limited to panel body) ==")
y0, y1 = int(1.9 / SH * h), int(5.4 / SH * h)
xs = [x for x in range(w) if sum(1 for y in range(y0, y1, 4) if beige(px[(x, y)])) > (y1 - y0) / 4 * 0.55]
runs = []
for x in xs:
    if runs and x - runs[-1][-1] <= 3:
        runs[-1].append(x)
    else:
        runs.append([x])
for r in runs:
    print(f"  x run {tx(r[0])}-{tx(r[-1])} in (w={(r[-1]-r[0])/w*SW:.2f})")

print("\n== white node circles (find via white pixels inside panel) ==")
y0, y1 = int(1.9 / SH * h), int(5.4 / SH * h)
cnt = defaultdict(int)
for y in range(y0, y1):
    for x in range(x0, x1):
        c = px[(x, y)]
        if min(c) > 243 and abs(c[0] - c[2]) < 12:
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > 25)
runs = []
for x in xs:
    if runs and x - runs[-1][-1] <= 8:
        runs[-1].append(x)
    else:
        runs.append([x])
print("  white-column x bands (in):", [(tx(r[0]), tx(r[-1])) for r in runs])

print("\n== node row y positions (white circles, at each column center) ==")
for (a, b) in runs:
    xc = (a + b) // 2
    col = [y for y in range(y0, y1) if min(px[(xc, y)]) > 243]
    rr = []
    for y in col:
        if rr and y - rr[-1][-1] <= 2:
            rr[-1].append(y)
        else:
            rr.append([y])
    rr = [r for r in rr if len(r) > 4]
    print(f"  band x {tx(a)}-{tx(b)}: node rows y {[ (ty(r[0]), ty(r[-1])) for r in rr ]}")

print("\n== magenta input dots (left edge of panel) ==")
mag = lambda c: c[0] > 150 and c[0] - c[1] > 40 and c[2] - c[1] > 40 and c[0] > 150
ys = [y for y in range(y0, y1) for x in range(x0, x0 + int(0.9 / SW * w)) if mag(px[(x, y)])]
rr = []
for y in ys:
    if rr and y - rr[-1][-1] <= 3:
        rr[-1].append(y)
    else:
        rr.append([y])
print("  magenta dot rows y:", [(ty(r[0]), ty(r[-1])) for r in rr if len(r) > 3])

print("\n== Output boxes (white with black outline, right of col3) ==")
y0f, y1f = 1.9, 5.4
cnt = defaultdict(int)
for y in range(int(y0f / SH * h), int(y1f / SH * h)):
    for x in range(int(6.3 / SW * w), int(7.6 / SW * w)):
        if min(px[(x, y)]) > 243:
            cnt[x] += 1
xs = sorted(x for x, n in cnt.items() if n > 10)
if xs:
    print(f"  white area x {tx(xs[0])}-{tx(xs[-1])}")
