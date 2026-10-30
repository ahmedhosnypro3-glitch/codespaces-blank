# Focused 1px dumps, slide 003 crops (frame space 960x540; crops upscaled).
from PIL import Image

R = "/home/ahmed/Projects/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide003"

def load(n):
    return Image.open(f"{R}/{n}").convert('RGB').load(), Image.open(f"{R}/{n}").size

def ch(px, x, y):
    r, g, b = px[x, y][:3]
    if r > 120 and r - g > 40 and r - b > 40: return 'r'
    if max(r, g, b) < 120: return '#'
    if r > 200 and g > 170 and b < 160: return 'y'
    if b > 170 and g > 150 and r < 170: return 'c'
    if r > 200 and b > 150 and g < 190 and r - g > 30: return 'm'
    return '.'

def dump(px, x0, x1, y0, y1, step=1):
    hdr = '     ' + ''.join(str((x // 10) % 10) if x % 5 == 0 else ' ' for x in range(x0, x1, step))
    print(hdr)
    for y in range(y0, y1):
        print(f"{y:4d} " + ''.join(ch(px, x, y) for x in range(x0, x1, step)))

print("=== A) topbox: tall dark vertical bars (cols, dark count over y20..350) ===")
for name in ("crop_32_topbox_orig.png", "crop_32_topbox_render.png"):
    px, (W, H) = load(name)
    print("--", name, W, H)
    bars = []
    for x in range(W):
        n = sum(1 for y in range(20, min(350, H)) if ch(px, x, y) == '#')
        if n >= 100:
            bars.append((x, n))
    print("tall dark bars:", bars)
    reds = [(x, y) for y in range(H) for x in range(W) if ch(px, x, y) == 'r']
    xs = sorted(set(p[0] for p in reds))
    cl = []
    if xs:
        cur = [xs[0], xs[0]]
        for x in xs[1:]:
            if x - cur[1] <= 8: cur[1] = x
            else: cl.append(tuple(cur)); cur = [x, x]
        cl.append(tuple(cur))
    print("loose-red clusters:", [(a, b, sum(1 for x, y in reds if a <= x <= b)) for a, b in cl])

print("=== B) orig red mark x415..455 y368..388 (1px) ===")
px, _ = load("crop_32_topbox_orig.png")
dump(px, 413, 458, 368, 388)
print("=== B2) render same box ===")
px2, _ = load("crop_32_topbox_render.png")
dump(px2, 413, 458, 368, 388)

print("=== C) orig bottom band x225..305 y352..396 (find y2) ===")
dump(px, 225, 305, 352, 396, step=1)

print("=== D) matrix whole-crop ASCII (step 4x8) ===")
pxm, (W, H) = load("crop_31_matrix_orig.png")
print("size", W, H)
for y in range(0, H, 8):
    print(f"{y:4d} " + ''.join(ch(pxm, x, y) for x in range(0, W, 4)))

print("=== E) matrix yellow row 1px dumps ===")
print("--- x296..352 y100..150 (outer-left paren zone) ---")
dump(pxm, 296, 352, 100, 150)
print("--- x272..300 y100..150 (the x280 dark column) ---")
dump(pxm, 272, 300, 100, 150)
print("--- x606..690 y100..150 (claimed inner right paren ~660) ---")
dump(pxm, 606, 690, 100, 150)
