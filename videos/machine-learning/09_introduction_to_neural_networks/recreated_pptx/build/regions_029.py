from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5

def to_in(px, py):
    return (round(px / w * SW, 2), round(py / h * SH, 2))

def bbox(pred, label, xr=(0, w), yr=(0, h), step=1, minpx=5):
    xs, ys = [], []
    for y in range(yr[0], yr[1], step):
        for x in range(xr[0], xr[1], step):
            if pred(im.getpixel((x, y))):
                xs.append(x); ys.append(y)
    if len(xs) < minpx:
        print(f"{label}: NOT FOUND")
        return
    print(f"{label}: px x[{min(xs)}-{max(xs)}] y[{min(ys)}-{max(ys)}]  -> in {to_in(min(xs), min(ys))} .. {to_in(max(xs), max(ys))}")

mag = lambda c: c[0] > 180 and c[1] > 120 and c[2] > 180 and c[0] - c[1] > 30 and c[2] - c[1] > 30
dkred = lambda c: c[0] > 140 and c[0] - c[1] > 60 and c[0] - c[2] > 60 and c[1] < 110
beige = lambda c: 195 < c[0] < 250 and 180 < c[1] < 240 and 140 < c[2] < 210 and c[0] - c[2] > 18
palegreen = lambda c: 200 < c[0] < 245 and 215 < c[1] < 250 and 180 < c[2] < 235 and c[1] - c[0] > 8 and c[1] - c[2] > 12
lightblue = lambda c: 200 < c[0] < 245 and 220 < c[1] < 250 and 240 < c[2] < 256 and c[1] - c[0] > 8
paleyellow = lambda c: c[0] > 245 and c[1] > 245 and 180 < c[2] < 235
whitebox = lambda c: min(c) > 248

print("== MAGENTA (input/target boxes + arrow) ==")
bbox(mag, "magenta all")
# left vs right box
props = im.load()
lx = [x for x in range(w) for y in range(0, int(h*0.30)) if mag(props[x, y])]
import collections
cnt = collections.Counter(lx)
groups = []
for x in sorted(cnt):
    if cnt[x] >= 6:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
print(" magenta x groups:", [(round(g[0]/w,3), round(g[-1]/w,3), to_in(g[0],0), to_in(g[-1],0)) for g in groups])
for g in groups:
    ys = [y for y in range(int(h*0.15), int(h*0.35)) for x in range(g[0], g[-1]+1) if mag(props[x, y])]
    if ys:
        print(f"   group x{g[0]/w:.3f}-{g[-1]/w:.3f}: y {min(ys)/h:.3f}-{max(ys)/h:.3f} -> in {to_in(0,min(ys))[1]}-{to_in(0,max(ys))[1]}")

print("\n== DARK RED error bar ==")
bbox(dkred, "dkred error-bar band", xr=(int(w*0.55), int(w*0.66)), yr=(int(h*0.25), int(h*0.72)))

print("\n== BEIGE panels ==")
bbox(beige, "beige all")
cnt = collections.Counter()
for y in range(0, h, 2):
    for x in range(w):
        if beige(props[x, y]):
            cnt[x] += 1
groups = []
for x in sorted(cnt):
    if cnt[x] > 30:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
for g in groups:
    ys = [y for y in range(0, h, 2) for x in range(g[0], min(g[-1], w-1)+1, 5) if beige(props[x, y])]
    print(f" beige x {g[0]/w:.3f}-{g[-1]/w:.3f} ({to_in(g[0],0)[0]}-{to_in(g[-1],0)[0]} in): y {min(ys)/h:.3f}-{max(ys)/h:.3f} ({to_in(0,min(ys))[1]:.2f}-{to_in(0,max(ys))[1]:.2f} in)")

print("\n== PALE GREEN class boxes ==")
bbox(palegreen, "palegreen all", minpx=10)
cnt = collections.Counter()
for y in range(int(h*0.25), int(h*0.70)):
    for x in range(int(w*0.55), w):
        if palegreen(props[x, y]):
            cnt[(x, y)] = 1
xs = [x for (x, y) in cnt]
ys = [y for (x, y) in cnt]
if xs:
    # cluster by y bands
    import itertools
    rows = collections.Counter(y for y in ys)
    bands = []
    for y in sorted(rows):
        if rows[y] > 15:
            if bands and y - bands[-1][-1] <= 4:
                bands[-1].append(y)
            else:
                bands.append([y])
    for b in bands:
        xs2 = [x for (x, y) in cnt if b[0] <= y <= b[-1]]
        print(f" palegreen y-band {b[0]/h:.3f}-{b[-1]/h:.3f} ({to_in(0,b[0])[1]:.2f}-{to_in(0,b[-1])[1]:.2f} in): x {min(xs2)/w:.3f}-{max(xs2)/w:.3f} ({to_in(min(xs2),0)[0]:.2f}-{to_in(max(xs2),0)[0]:.2f} in)")

print("\n== LIGHT BLUE (previous layer callout) ==")
bbox(lightblue, "lightblue all", minpx=10)
print("\n== LIGHT GREEN callout (E2EFDA) ==")
c2 = lambda c: 215 < c[0] < 250 and 230 < c[1] < 252 and 210 < c[2] < 245
bbox(c2, "E2EFDA all", minpx=10)

print("\n== PALE YELLOW formula boxes ==")
bbox(paleyellow, "paleyellow all", minpx=10)
cnt = collections.Counter()
for y in range(int(h*0.70), h):
    for x in range(w):
        if paleyellow(props[x, y]):
            cnt[x] += 1
groups = []
for x in sorted(cnt):
    if cnt[x] > 20:
        if groups and x - groups[-1][-1] <= 3:
            groups[-1].append(x)
        else:
            groups.append([x])
for g in groups:
    ys = [y for y in range(int(h*0.70), h) for x in range(g[0], g[-1]+1, 5) if paleyellow(props[x, y])]
    print(f" paleyellow x {g[0]/w:.3f}-{g[-1]/w:.3f} ({to_in(g[0],0)[0]:.2f}-{to_in(g[-1],0)[0]:.2f} in): y {min(ys)/h:.3f}-{max(ys)/h:.3f} ({to_in(0,min(ys))[1]:.2f}-{to_in(0,max(ys))[1]:.2f} in)")
