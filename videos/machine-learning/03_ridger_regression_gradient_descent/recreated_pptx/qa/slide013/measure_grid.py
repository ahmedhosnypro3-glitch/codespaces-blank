import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

# 1. label-box interior colours
print("=== label box samples ===")
for name, (x0, x1, y0, y1) in (("TrainBox", (96, 161, 96, 126)), ("TestBox", (801, 867, 96, 125))):
    seg = im[y0:y1, x0:x1].reshape(-1, 3)
    med = np.median(seg, axis=0)
    print(f"{name} x{x0}..{x1} y{y0}..{y1} median={tuple(int(v) for v in med)}")

print("\n=== white-text pixels inside boxes ===")
wh = (r > 235) & (g > 235) & (b > 235)
for name, (x0, x1, y0, y1) in (("TrainBox", (96, 161, 96, 126)), ("TestBox", (801, 867, 96, 125))):
    m = wh[y0:y1, x0:x1]
    ys, xs = np.where(m)
    if len(ys):
        print(f"{name}: white ink x{x0+xs.min()}..{x0+xs.max()} y{y0+ys.min()}..{y0+ys.max()} n={m.sum()}")
    else:
        print(f"{name}: no white ink")

# 2. dark gridlines: long runs
dk = (r < 150) & (g < 150) & (b < 150)
print("\n=== horizontal gridline candidates (row-wise, x>90, width>200) ===")
for y in range(H):
    row = dk[y]
    # longest run
    best = cur = 0
    bs = cs = 0
    for x in range(W):
        if row[x]:
            if cur == 0:
                cs = x
            cur += 1
            if cur > best:
                best, bs = cur, cs
        else:
            cur = 0
    if best > 200:
        print(f"  y={y} runlen={best} x{bs}..{bs+best-1}")

print("\n=== vertical gridline candidates (col-wise, y>120, height>80) ===")
for x in range(W):
    col = dk[:, x]
    best = cur = 0
    bs = cs = 0
    for y in range(H):
        if col[y]:
            if cur == 0:
                cs = y
            cur += 1
            if cur > best:
                best, bs = cur, cs
        else:
            cur = 0
    if best > 80:
        print(f"  x={x} runlen={best} y{bs}..{bs+best-1}")
