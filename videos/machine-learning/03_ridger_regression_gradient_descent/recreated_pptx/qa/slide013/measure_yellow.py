import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# pure yellow FFFF00 (JPEG-warm)
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
RED = (r > g + 40) & (r > b + 40)
BLK = (r < 90) & (g < 90) & (b < 90)


def show(m, name):
    ys, xs = np.where(m)
    if not len(ys):
        print(f"{name}: none")
        return
    # cluster by rows
    print(f"{name}: x{xs.min()}..{xs.max()} y{ys.min()}..{ys.max()} n={len(ys)}")
    # row bands
    rb = []
    s = p = ys.min()
    for v in ys:
        if v == p + 1:
            p = v
        else:
            rb.append((s, p))
            s = p = v
    rb.append((s, p))
    # merge close
    merged = []
    for s2, e2 in rb:
        if merged and s2 - merged[-1][1] <= 2:
            merged[-1] = (merged[-1][0], e2)
        else:
            merged.append((s2, e2))
    for s2, e2 in merged:
        seg = m[s2:e2 + 1]
        xs2 = np.where(seg.any(axis=0))[0]
        print(f"   y{s2}..{e2} x{xs2.min()}..{xs2.max()} n={int(seg.sum())}")


for m, n in ((YEL, 'YELLOW'), (BLK, 'BLACK')):
    show(m, n)

# blue arrow regions: solid blue strokes that are wide-ish
print("\n=== blue ink column profile in mid-gap columns x640..790 ===")
BLUE_AREA = BLUE & (np.arange(H)[:, None] >= 0)
for y0 in range(0, 540, 10):
    seg = BLUE[y0:y0 + 10]
    xs = np.where(seg.any(axis=0))[0]
    if len(xs):
        print(f"  y{y0}..{y0+9}: cols {xs.min()}..{xs.max()} n={int(seg.sum())}")
