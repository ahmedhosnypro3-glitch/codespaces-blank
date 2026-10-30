"""Targeted per-element geometry measurement for slide_021.jpg."""
import numpy as np
from PIL import Image

V = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/"
im = Image.open(V + "unique_slides/slide_021.jpg").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
ppf = 13.3333 / W     # inches per frame px


def report(name, mask, min_frac=0.30):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        print(f"  {name}: NONE")
        return None
    print(f"  {name}: x {xs.min()/W:.3f}-{xs.max()/W:.3f}  y {ys.min()/H:.3f}-{ys.max()/H:.3f}"
          f"   in: x {xs.min()*ppf:.2f}-{xs.max()*ppf:.2f}  y {ys.min()*ppf:.2f}-{ys.max()*ppf:.2f}")
    return xs, ys


r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]

print("=== BACKGROUND ===")
print("  bg sample (10,10), (470,10), (10,500):", a[10, 10], a[470, 10], a[10, 500])

print("\n=== PINK FORMULA BOX FILL (R>G>B, light) ===")
pink = (r > 245) & (r - g > 12) & (r - g < 45) & (r - b > 12) & (r - b < 45)
report("pink fill", pink)

# Column-run analysis for pink: find x-bands where pink is present in rows 60..110 (top formula row)
print("\n=== PINK x-extents in the TOP formula row (y 58-102) ===")
band = pink[58:103, :]
colcount = band.sum(axis=0)
xs = np.where(colcount > 20)[0]
print("  x runs:", end=" ")
seg = []
prev = None
for x in xs:
    if prev is None or x - prev > 3:
        seg.append([x, x])
    else:
        seg[-1][1] = x
    prev = x
for s in seg:
    print(f"[{s[0]},{s[1]}] -> in {s[0]*ppf:.2f}-{s[1]*ppf:.2f}  frac {s[0]/W:.3f}-{s[1]/W:.3f}", end="  ")
print()

print("\n=== PINK x-extents in the BOTTOM formula row (y 287-338) ===")
band = pink[287:339, :]
colcount = band.sum(axis=0)
xs = np.where(colcount > 20)[0]
seg = []; prev = None
for x in xs:
    if prev is None or x - prev > 3:
        seg.append([x, x])
    else:
        seg[-1][1] = x
    prev = x
for s in seg:
    print(f"[{s[0]},{s[1]}] -> in {s[0]*ppf:.2f}-{s[1]*ppf:.2f}", end="  ")
print()

print("\n=== PINK y-extents (top boxes, x 130-380) ===")
col = pink[:, 130:380]
rowcount = col.sum(axis=1)
ys = np.where(rowcount > 60)[0]
seg = []; prev = None
for y in ys:
    if prev is None or y - prev > 3:
        seg.append([y, y])
    else:
        seg[-1][1] = y
    prev = y
for s in seg:
    print(f"  y {s[0]}-{s[1]} -> in {s[0]*ppf:.2f}-{s[1]*ppf:.2f}  frac {s[0]/H:.3f}-{s[1]/H:.3f}")

print("\n=== BLUE/INDIGO BORDERS of graph boxes (R low, B high, saturation) ===")
blue = (b > 100) & (b - r > 50) & (b - g > 25)
# find blue row/col runs -> rectangle borders
browsum = blue.sum(axis=1)
bcolsum = blue.sum(axis=0)
print("  blue rows > 150:", [(y, int(browsum[y])) for y in range(H) if browsum[y] > 150][:60])
print("  blue cols > 150:", [(x, int(bcolsum[x])) for x in range(W) if bcolsum[x] > 150][:60])

print("\n=== INDIGO exact-color census of border hue ===")
# sample the known border pixel at (109, 122ish) and (110,564)
print("  px(109,150)=", a[109, 150], " px(110,300)=", a[110, 300], " px(507,900)=", a[507, 900])

print("\n=== RED TEXT/border census (exact) ===")
red = (r > 150) & (g < 120) & (b < 120) & (r - g > 60) & (r - b > 60)
from collections import Counter
cnt = Counter(map(tuple, a[red] // 16 * 16))
print("  top red colors:", cnt.most_common(10))

print("\n=== BLUE TEXT census ===")
bl = (b > 130) & (b - r > 60)
cnt2 = Counter(map(tuple, a[bl] // 16 * 16))
print("  top blue colors:", cnt2.most_common(8))

print("\n=== GREEN TEXT census ===")
gr = (g > 100) & (g - r > 40) & (g - b > 40)
cnt3 = Counter(map(tuple, a[gr] // 16 * 16))
print("  top green colors:", cnt3.most_common(8))

print("\n=== ORANGE census ===")
orng = (r > 180) & (g > 100) & (g < 200) & (b < 100) & (r - b > 80)
report("orange", orng)

print("\n=== BLACK TEXT census (excluding bottom bar) ===")
blk = (r < 80) & (g < 80) & (b < 80)
blk2 = blk.copy(); blk2[505:, :] = False
report("black ink (excl bar)", blk2)
