import sys
from PIL import Image
import statistics as st

orig = Image.open("/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_031.jpg").convert("RGB")
rend = Image.open("render_34.png").convert("RGB")
ow, oh = orig.size; rw, rh = rend.size
s = rw / ow
print(f"orig {ow}x{oh}  render {rw}x{rh}  scale {s:.4f}")

def region_stats(im, x0, y0, x1, y1, tag):
    px = im.load()
    vals, red_n, navy_n, green_n, violet_n = [], 0, 0, 0, 0
    for y in range(y0, y1):
        for x in range(x0, x1):
            r, g, b = px[x, y]
            if r + g + b < 450:  # ink
                continue
            if min(r, g, b) > 235:  # white
                continue
            vals.append((r, g, b))
            if r > 110 and r - g > 60 and r - b > 60: red_n += 1
            if b > 110 and b - r > 40: navy_n += 1
            if g > 180 and g - b > 20 and g - r > 0: green_n += 1
            if b > 150 and b - g > 20: violet_n += 1
    if vals:
        med = tuple(int(st.median(c[i] for c in vals)) for i in range(3))
    else:
        med = None
    print(f"{tag}: nonwhite={len(vals)} median={med} red={red_n} navy={navy_n} green={green_n} violet={violet_n}")
    return med, red_n, navy_n, green_n, violet_n

print("\n== FINDING 1: band2 (x-delta / f(x-delta)) fill, rows y389..405 & y411..423, x140..870 ==")
region_stats(orig, 140, 389, 870, 405, "ORIG band2 upper")
region_stats(orig, 140, 411, 870, 423, "ORIG band2 lower")
region_stats(rend, int(140*s), int(389*s), int(870*s), int(405*s), "REND band2 upper")
region_stats(rend, int(140*s), int(411*s), int(870*s), int(423*s), "REND band2 lower")

print("\n== FINDING 2: big-table frame edges ==")
region_stats(orig, 150, 333, 800, 339, "ORIG frame top strip y333..338")
region_stats(orig, 62, 350, 68, 510, "ORIG frame left strip x62..67")
region_stats(rend, int(150*s), int(333*s), int(800*s), int(339*s), "REND frame top strip")
region_stats(rend, int(62*s), int(350*s), int(68*s), int(510*s), "REND frame left strip")

# row-profile of the frame top edge: per-row nonwhite median, y330..342
pxo = orig.load()
print("\nORIG per-row median y329..343 (x150..800):")
for y in range(329, 344):
    vals = [pxo[x, y] for x in range(150, 800) if sum(pxo[x, y]) < 720]
    if vals:
        med = tuple(int(st.median(c[i] for c in vals)) for i in range(3))
        print(f"  y{y}: n={len(vals)} median={med}")
    else:
        print(f"  y{y}: n=0")
