import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
BLK = (r < 120) & (g < 120) & (b < 120)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)

# title ink: red, in the top band
print("=== TITLE (red ink y60..105, x140..800) ===")
seg = RED[60:105, 140:800]
ys, xs = np.where(seg)
print(f"  bbox x{140+xs.min()}..{140+xs.max()} y{60+ys.min()}..{60+ys.max()} n={seg.sum()}")
# colour sample of the darkest red title pixels
m = RED[60:105, 140:800]
vals = im[60:105, 140:800][m]
print(f"  red-ink colour median: {tuple(int(v) for v in np.median(vals, axis=0))}")
print(f"  red-ink colour range R{vals[:,0].min()}..{vals[:,0].max()} G{vals[:,1].min()}..{vals[:,1].max()} B{vals[:,2].min()}..{vals[:,2].max()}")
# per-row extent of title
for y in range(60, 105):
    row = RED[y, 140:800]
    xs2 = np.where(row)[0]
    if len(xs2):
        print(f"  y{y}: x{140+xs2.min()}..{140+xs2.max()} n={row.sum()}")

print()
print("=== W CONSTRUCT ASCII with ruler (band1, x455..690, y150..255) ===")
syms = ['R', 'B', 'K', 'Y']
masks = [RED, BLUE, BLK, YEL]
y0, y1, x0, x1 = 150, 255, 455, 690
# ruler in tens
tens = ''.join('|' if (x % 25 == 0) else ('+' if (x % 5 == 0) else '.') for x in range(x0, x1))
print("      " + tens)
for y in range(y0, y1):
    line = ''.join(
        next((s for m, s in zip(masks, syms) if m[y, x]), '.')
        for x in range(x0, x1)
    )
    print(f"{y:4d}| {line}")
