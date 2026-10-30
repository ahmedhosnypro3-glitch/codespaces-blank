import numpy as np
from PIL import Image

im = Image.open('unique_slides/slide_031.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape

# Red-bordered boxes: FF0000-ish borders. Find red-ish pixels grouped by bbox.
red = (a[:, :, 0] > 120) & (a[:, :, 1] < 90) & (a[:, :, 2] < 90)
print('=== red-ish components (boxes / arrows / dashed lines) ===')
seen = np.zeros((H, W), bool)
from collections import deque
for y0 in range(H):
    for x0 in range(W):
        if red[y0, x0] and not seen[y0, x0]:
            q = deque([(y0, x0)]); seen[y0, x0] = True
            pts = []
            while q:
                cy, cx = q.popleft(); pts.append((cy, cx))
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < H and 0 <= nx < W and red[ny, nx] and not seen[ny, nx]:
                            seen[ny, nx] = True; q.append((ny, nx))
            if len(pts) < 60:
                continue
            ys = [p[0] for p in pts]; xs = [p[1] for p in pts]
            print('  n=%5d  x %d..%d  y %d..%d' % (len(pts), min(xs), max(xs), min(ys), max(ys)))

# Purple text
purple = (a[:, :, 2] > 90) & (a[:, :, 0] > 60) & (a[:, :, 0] < 150) & (a[:, :, 1] < 80)
ys, xs = np.nonzero(purple[:340, :])
if len(xs):
    print('=== purple (Bouncing + arrow) above y340: bbox x %d..%d y %d..%d n=%d' % (xs.min(), xs.max(), ys.min(), ys.max(), len(xs)))

# Title text bbox (colored, top-left)
print('=== title band ink (y 50..120, x 50..500) ===')
band = a[50:125, 50:520]
gray = (abs(band[:, :, 0] - 233) < 16) & (abs(band[:, :, 1] - 233) < 16) & (abs(band[:, :, 2] - 231) < 18)
ink = ~gray
ys, xs = np.nonzero(ink)
if len(xs):
    print('  ink bbox x %d..%d  y %d..%d' % (50 + xs.min(), 50 + xs.max(), 50 + ys.min(), 50 + ys.max()))
