from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
SW, SH = 13.33, 7.5
px = im.load()

def to_in(xf, yf):
    return (round(xf * SW, 2), round(yf * SH, 2))

def col_extent(xf, pred, label):
    x = int(xf * w)
    ys = [y for y in range(h) if pred(px[(x, y)])]
    if not ys:
        print(f"  {label} @x={xf}: none")
        return
    runs = []
    for y in ys:
        if runs and y - runs[-1][-1] <= 2:
            runs[-1].append(y)
        else:
            runs.append([y])
    print(f"  {label} @x={xf} ({to_in(xf,0)[0]}in): " +
          ", ".join(f"y{r[0]/h:.3f}-{r[-1]/h:.3f}({to_in(0,r[0]/h)[1]:.2f}-{to_in(0,r[-1]/h)[1]:.2f}in)" for r in runs))

beige = lambda c: 195 < c[0] < 250 and 185 < c[1] < 240 and 145 < c[2] < 215 and c[0] - c[2] > 16
paleyellow = lambda c: c[0] > 248 and c[1] > 248 and 190 < c[2] < 240
white = lambda c: min(c) > 245
greenfill = lambda c: 200 < c[0] < 240 and 215 < c[1] < 245 and 190 < c[2] < 230 and c[1] - c[0] > 10 and c[1] - c[2] > 10

print("== beige panel vertical extent at x = 0.10, 0.30, 0.50 ==")
for xf in (0.10, 0.30, 0.50, 0.80):
    col_extent(xf, beige, "beige")

print("\n== pale-yellow at x = 0.10 (left formula box), 0.45 (center), 0.80 (right) ==")
for xf in (0.10, 0.45, 0.80):
    col_extent(xf, paleyellow, "paleyellow")

print("\n== class boxes: rows where greenfill present in x 8.0-8.9in ==")
x0, x1 = int(8.0 / SW * w), int(8.93 / SW * w)
rows = [y for y in range(int(h * 0.25), int(h * 0.70)) if sum(1 for x in range(x0, x1, 2) if greenfill(px[(x, y)])) > 5]
runs = []
for y in rows:
    if runs and y - runs[-1][-1] <= 3:
        runs[-1].append(y)
    else:
        runs.append([y])
for r in runs:
    print(f"  class box row y{r[0]/h:.3f}-{r[-1]/h:.3f} -> {to_in(0,r[0]/h)[1]:.2f}-{to_in(0,r[-1]/h)[1]:.2f} in  (h={ (r[-1]-r[0])/h*SH:.2f} in)")

print("\n== legend box (light beige F2E4D0) x 9.0-12.3 in ==")
lbeige = lambda c: 235 < c[0] < 252 and 220 < c[1] < 240 and 200 < c[2] < 225
x = int(10.5 / SW * w)
col_extent(0.79, lbeige, "legend-lbeige")

print("\n== note box white area x 9.2-12.2 in ==")
x = int(10.7 / SW * w)
col_extent(0.80, white, "white")

print("\n== badge yellow FFFF99 x ~ 12.5-12.98 in ==")
badge = lambda c: c[0] > 240 and c[1] > 240 and 150 < c[2] < 220
col_extent(0.955, badge, "badge-yellow")
xs = [x for x in range(w) if any(badge(px[(x, y)]) for y in range(int(h * 0.05), int(h * 0.20)))]
if xs:
    print(f"  badge x {min(xs)/w:.3f}-{max(xs)/w:.3f} -> {to_in(min(xs)/w,0)[0]}-{to_in(max(xs)/w,0)[0]} in")

print("\n== letterbox black bar ==")
black = lambda c: max(c) < 40
ys = [y for y in range(h) if sum(1 for x in range(0, w, 10) if black(px[(x, y)])) > 60]
if ys:
    print(f"  black bar y {min(ys)/h:.3f}-{max(ys)/h:.3f} -> {to_in(0,min(ys)/h)[1]:.2f}-{to_in(0,max(ys)/h)[1]:.2f} in")

print("\n== red frame inset in original ==")
red = lambda c: c[0] > 120 and c[0] - c[1] > 50 and c[0] - c[2] > 50
cols = [x for x in range(w) if sum(1 for y in range(0, h, 3) if red(px[(x, y)])) > 60]
rows = [y for y in range(h) if sum(1 for x in range(0, w, 3) if red(px[(x, y)])) > 60]
print("  vertical red lines at x:", [f"{c/w:.3f}({to_in(c/w,0)[0]}in)" for c in cols][:8])
print("  horizontal red lines at y:", [f"{r/h:.3f}({to_in(0,r/h)[1]}in)" for r in rows][:8])
