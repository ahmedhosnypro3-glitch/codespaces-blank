import sys
from PIL import Image
import numpy as np
from collections import deque

n = int(sys.argv[1])
im = Image.open(f"unique_slides/slide_{n:03d}.jpg").convert("RGB")
ar = np.array(im).astype(int)
H, W, _ = ar.shape
r, g, b = ar[:, :, 0], ar[:, :, 1], ar[:, :, 2]
mx = ar.max(2); mn = ar.min(2); sat = mx - mn
gray = ar.mean(2)

masks = {
    "red":    (r > 110) & (r - g > 55) & (r - b > 55),
    "pink":   (r > 150) & (g > 80) & (g < 200) & (r - g > 45) & (b - g > 15) & (b > 90),
    "orange": (r > 150) & (g > 90) & (g < 190) & (r - g > 35) & (r - b > 55),
    "yellow": (r > 170) & (g > 150) & (b < g - 40),
    "green":  (g > 130) & (g - r > 25) & (g - b > 25),
    "blue":   (b > 110) & (b - r > 40) & (b - g > 25),
    "dark":   (gray < 110) & (sat < 45),
}

def comps(mask, minpx=40):
    seen = np.zeros_like(mask, dtype=bool)
    out = []
    for y in range(H):
        for x in range(W):
            if mask[y, x] and not seen[y, x]:
                q = deque([(y, x)]); seen[y, x] = True
                pts = []
                while q:
                    cy, cx = q.popleft(); pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True; q.append((ny, nx))
                if len(pts) >= minpx:
                    ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
                    out.append((len(pts), min(xs), min(ys), max(xs), max(ys)))
    out.sort(reverse=True)
    return out

for name, m in masks.items():
    cs = comps(m, 60)
    print(f"== {name}: {len(cs)} components >=60px")
    for px, x0, y0, x1, y1 in cs[:22]:
        print(f"   px={px:6d} bbox x[{x0},{x1}] y[{y0},{y1}] w={x1-x0+1} h={y1-y0+1}")
