# precise panel/ink geometry for slide_030 original
from PIL import Image

im = Image.open("unique_slides/slide_030.jpg").convert("RGB")
W, H = im.size
px = im.load()

def red(c):
    r, g, b = c
    return r > 140 and g < 95 and b < 95 and (r - g) > 55

def blue(c):
    r, g, b = c
    return b > 120 and b - r > 45 and b - g > 45

def green(c):
    r, g, b = c
    return g > 110 and g - r > 40 and g - b > 40

def yellow(c):
    r, g, b = c
    return r > 215 and g > 175 and b < 175

def orange(c):
    r, g, b = c
    return r > 215 and 145 < g < 205 and b < 175

def dark(c):
    return (c[0] + c[1] + c[2]) < 260

# Diagram red panel border: red cols 846/847 with 187 tall = right border.
# Find the left border of that panel: scan cols 100-600 for long red vertical runs
def vrun(col, y0, y1):
    n = 0
    for y in range(y0, y1):
        if red(px[col, y]):
            n += 1
    return n

def hrun(row, x0, x1):
    n = 0
    for x in range(x0, x1):
        if red(px[x, row]):
            n += 1
    return n

print("=== diagram panel border (tall right border x=846) ===")
top = None; bot = None
for y in range(H):
    if vrun(846, y, y + 1):
        if top is None:
            top = y
        bot = y
print("right border y span:", top, bot)
# horizontal borders
for x0, x1, lab in [(100, 850, "panel"), (850, 960, "right-of-panel")]:
    print(lab, "red h-run count rows>200px:", [y for y in range(H) if hrun(y, x0, x1) > 200])
# left border candidates
print("red v-run (y 100-450) per col:", {x: vrun(x, 100, 450) for x in range(120, 480, 10) if vrun(x, 100, 450) > 50})

print("=== equation panels ===")
# blue box borders: blue cols 71/72/73 = left border
print("blue left col x=72 v-span y:", [y for y in range(H) if blue(px[72, y])][:1], [y for y in range(H) if blue(px[72, y])][-1:])
print("blue right border cols (v-run y 400-520):", {x: sum(1 for y in range(400, 520) if blue(px[x, y])) for x in range(740, 800)})
print("green right border cols (v-run y 400-520):", {x: sum(1 for y in range(400, 520) if green(px[x, y])) for x in range(860, 900)})
