from PIL import Image
import numpy as np, sys
from collections import Counter

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
H, W = a.shape[:2]

# slide content area (inside video letterbox) for the original 960x540
x0, x1, y0, y1 = 38, 921, 43, 517
c = Counter()
for y in range(y0, y1 + 1, 2):
    for x in range(x0, x1 + 1, 2):
        c[tuple((a[y, x] // 16 * 16))] += 1
print("top quantized colors in slide area:")
for col, n in c.most_common(14):
    print("  ", col, n)

R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
nonbg = ~((R > 240) & (G > 240) & (B > 240))
print("\n-- rows with long horizontal non-white runs (>=80px) inside content --")
for y in range(y0, y1 + 1):
    row = nonbg[y, x0:x1 + 1]
    n = int(row.sum())
    if n >= 80:
        xs = np.nonzero(row)[0] + x0
        runs = []
        s = xs[0]; p = xs[0]
        for x in xs[1:]:
            if x != p + 1:
                runs.append((int(s), int(p))); s = x
            p = x
        runs.append((int(s), int(p)))
        print(f"y={y} n={n} runs={runs[:8]}{'...' if len(runs) > 8 else ''}")
