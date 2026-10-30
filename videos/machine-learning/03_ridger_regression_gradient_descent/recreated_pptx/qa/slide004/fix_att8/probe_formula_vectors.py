# PIL probes for slide_004 attempt-8 fixes, frame space 960x540 (1px=1pt).
# A) loss-formula ink colour: original frame box x78..486 y464..522 vs asset
# B) vector assets eq_004_Yvec/Yhatvec: black-leadin vs red-vector column split
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"

def cls(p):
    r, g, b = p[0], p[1], p[2]
    if r > 150 and r - g > 60 and r - b > 60:
        return 'red'
    if max(r, g, b) < 110:
        return 'black'
    return None

def rng(pts):
    if not pts:
        return "none"
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return f"x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} n={len(pts)}"

print("=== A) formula box on ORIGINAL ===")
im = Image.open(f"{R}/unique_slides/slide_004.jpg").convert('RGB')
print("orig size", im.size)
x0, y0, x1, y1 = 78, 464, 486, 522
reds = []; blacks = []
for y in range(y0 + 2, y1 - 2):
    for x in range(x0 + 3, x1 - 3):
        c = cls(im.getpixel((x, y)))
        if c == 'red':
            reds.append((x, y))
        elif c == 'black':
            blacks.append((x, y))
print("ORIG formula red  :", rng(reds))
print("ORIG formula black:", rng(blacks))
for name, pts in (("red", reds), ("black", blacks)):
    bins = {}
    for x, y in pts:
        bins[x // 20 * 20] = bins.get(x // 20 * 20, 0) + 1
    print(f"{name} 20-col bins:", sorted(bins.items()))

print("=== A2) formula ASSET ===")
im2 = Image.open(f"{R}/recreated_pptx/build/assets/eq_004_formula.png").convert('RGBA')
print("asset size", im2.size)
px2 = im2.load()
areds = []; ablacks = []
for y in range(im2.height):
    for x in range(im2.width):
        p = px2[x, y]
        if p[3] < 64:
            continue
        c = cls(p)
        if c == 'red':
            areds.append(x)
        elif c == 'black':
            ablacks.append(x)
print("ASSET formula red n=", len(areds), " black n=", len(ablocks := ablacks))
if areds: print("  red  x", min(areds), "..", max(areds))
if ablacks: print("  black x", min(ablacks), "..", max(ablacks))

print("=== B) vector asset column segmentation ===")
for name in ("eq_004_Yvec.png", "eq_004_Yhatvec.png"):
    im = Image.open(f"{R}/recreated_pptx/build/assets/{name}").convert('RGBA')
    W, H = im.size
    px = im.load()
    lab = []
    for x in range(W):
        hr = hb = False
        for y in range(H):
            p = px[x, y]
            if p[3] < 64:
                continue
            c = cls(p)
            if c == 'red': hr = True
            elif c == 'black': hb = True
        lab.append('R' if hr and not hb else ('B' if hb and not hr else ('X' if hr else '.')))
    segs = []
    cur = None; start = 0
    for x, l in enumerate(lab):
        if l != cur:
            if cur is not None:
                segs.append((cur, start, x - 1))
            cur = l; start = x
    segs.append((cur, start, W - 1))
    segs = [(l, a, b) for l, a, b in segs if l != '.' and b - a >= 1]
    print(f"{name} {W}x{H} segments:", segs)
    nr = sum(1 for x in range(W) for y in range(H) if px[x, y][3] >= 64 and cls(px[x, y]) == 'red')
    nb = sum(1 for x in range(W) for y in range(H) if px[x, y][3] >= 64 and cls(px[x, y]) == 'black')
    print(f"  red px={nr} black px={nb}")
