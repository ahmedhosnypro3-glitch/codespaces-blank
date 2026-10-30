import numpy as np
from PIL import Image
from collections import deque

im = Image.open('unique_slides/slide_031.jpg').convert('RGB')
a = np.asarray(im).astype(int)
H, W, _ = a.shape


def components(mask):
    lab = np.zeros(mask.shape, int)
    out = []
    nxt = 0
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if mask[y, x] and lab[y, x] == 0:
                nxt += 1
                q = deque([(y, x)])
                lab[y, x] = nxt
                pts = []
                while q:
                    cy, cx = q.popleft()
                    pts.append((cy, cx))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = cy + dy, cx + dx
                            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] \
                                    and mask[ny, nx] and lab[ny, nx] == 0:
                                lab[ny, nx] = nxt
                                q.append((ny, nx))
                out.append(pts)
    return out


def region(y0, y1, x0, x1):
    m = np.zeros((H, W), bool)
    m[y0:y1, x0:x1] = True
    return m


# green (minimum point marker)
gm = (a[:, :, 1] > 80) & (a[:, :, 0] < 130) & (a[:, :, 2] < 130) & region(60, 280, 540, 840)
# red (start point marker + dashed lines)
rm = (a[:, :, 0] > 130) & (a[:, :, 1] < 100) & (a[:, :, 2] < 100) & region(60, 280, 540, 840)
# blue (parabola)
bm = (a[:, :, 2] > 110) & (a[:, :, 0] < 110) & (a[:, :, 1] < 120) & region(60, 280, 540, 840)

for name, m in (('green', gm), ('red', rm), ('blue', bm)):
    print('=== %s components (n>=8 px) ===' % name)
    for pts in components(m):
        if len(pts) < 8:
            continue
        ys = [p[0] for p in pts]
        xs = [p[1] for p in pts]
        print('  n=%5d  x %d..%d (cx %.0f)  y %d..%d (cy %.0f)'
              % (len(pts), min(xs), max(xs), sum(xs) / len(xs),
                 min(ys), max(ys), sum(ys) / len(ys)))
