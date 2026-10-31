from PIL import Image
from collections import Counter

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks"
im = Image.open(f"{V}/unique_slides/slide_029.jpg").convert("RGB")
w, h = im.size
print("orig", im.size)

def q(c):
    return (c[0] // 24 * 24, c[1] // 24 * 24, c[2] // 24 * 24)

def band(y0f, y1f, label):
    cnt = Counter()
    for y in range(int(h * y0f), int(h * y1f)):
        for x in range(0, w, 2):
            cnt[q(im.getpixel((x, y)))] += 1
    print(f"--- band y {y0f}-{y1f} ({label}) top 12 colors ---")
    for c, n in cnt.most_common(12):
        print(f"   {c}  {n}  ({100*n/(int(h*(y1f-y0f))*(w//2)):.1f}%)")

band(0.17, 0.24, "input/target row")
band(0.55, 0.62, "error bar row")
band(0.28, 0.44, "legend area")
band(0.44, 0.60, "note box area")

# magenta-ish loose detector across top 40%
print("\n--- loose magenta scan (top 40% of height) ---")
cols = {}
for x in range(w):
    for y in range(0, int(h * 0.40)):
        r, g, b = im.getpixel((x, y))
        if r > 180 and b > 180 and g < r - 30 and g < b - 30:
            cols[x] = cols.get(x, 0) + 1
xs = [x for x, n in cols.items() if n > 8]
groups = []
for x in xs:
    if groups and x - groups[-1][-1] <= 3:
        groups[-1].append(x)
    else:
        groups.append([x])
print(" magenta bands x-frac:", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

# pale green box scan (#D9EAD3-ish) across whole image
print("\n--- pale-green box scan (all height) ---")
cols = {}
for x in range(w):
    for y in range(0, h, 2):
        r, g, b = im.getpixel((x, y))
        if 190 < r < 245 and 210 < g < 248 and 175 < b < 235 and g > r and g > b:
            cols[x] = cols.get(x, 0) + 1
xs = [x for x, n in cols.items() if n > 10]
groups = []
for x in xs:
    if groups and x - groups[-1][-1] <= 3:
        groups[-1].append(x)
    else:
        groups.append([x])
print(" pale-green bands x-frac:", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])

# white box with red border (note box) region 0.46-0.58 y
print("\n--- white-with-red-border note box rows ---")
for yf in [0.50, 0.53, 0.56]:
    row = [im.getpixel((int(fx * w), int(yf * h))) for fx in [0.70, 0.75, 0.80, 0.85, 0.90, 0.94]]
    print(f"  y={yf}: {row}")

# title row: check red text extent
print("\n--- title area red-text x extent (y 0.10-0.17) ---")
cols = []
for x in range(w):
    c = sum(1 for y in range(int(h * 0.10), int(h * 0.17))
            if (lambda p: p[0] > 140 and p[0] > p[1] + 60 and p[0] > p[2] + 60)(im.getpixel((x, y))))
    if c > 4:
        cols.append(x)
groups = []
for x in cols:
    if groups and x - groups[-1][-1] <= 3:
        groups[-1].append(x)
    else:
        groups.append([x])
print(" red bands x-frac:", [(round(g[0]/w, 3), round(g[-1]/w, 3)) for g in groups])
