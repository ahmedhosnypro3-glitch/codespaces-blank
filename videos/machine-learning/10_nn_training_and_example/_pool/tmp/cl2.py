from PIL import Image
import numpy as np
from collections import deque
im = np.array(Image.open('unique_slides/slide_030.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

def clusters(x0, x1, y0, y1, name, m, minpts=20):
    reg = im[y0:y1, x0:x1]
    rr, gg, bb = reg[:, :, 0], reg[:, :, 1], reg[:, :, 2]
    H, W = m.shape
    seen = np.zeros_like(m, bool)
    out = []
    for yy in range(H):
        for xx in range(W):
            if m[yy, xx] and not seen[yy, xx]:
                q = deque([(yy, xx)])
                seen[yy, xx] = True
                comp = []
                while q:
                    y, x = q.popleft()
                    comp.append((x, y))
                    for dy in (-1, 0, 1):
                        for dx in (-1, 0, 1):
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < H and 0 <= nx < W and m[ny, nx] and not seen[ny, nx]:
                                seen[ny, nx] = True
                                q.append((ny, nx))
                if len(comp) >= minpts:
                    cxs = [p[0] for p in comp]
                    cys = [p[1] for p in comp]
                    out.append((len(comp), min(cxs) + x0, max(cxs) + x0, min(cys) + y0, max(cys) + y0))
    out.sort(reverse=True)
    print(name, out[:10])

blue = (b > 130) & (r < 120) & (g < 150) & ((b - r) > 40)
red = (r > 130) & (g < 100) & (b < 100) & ((r - g) > 60)
yellow = (r > 200) & (g > 190) & (b < 170)
clusters(600, 935, 245, 445, "blue", blue)
clusters(600, 935, 245, 445, "red", red)
clusters(600, 935, 245, 445, "yellow", yellow, minpts=40)
clusters(430, 925, 45, 250, "green-fill", (g > 120) & (r < 150) & (b < 150) & ((g - r) > 20), minpts=30)
clusters(430, 925, 45, 250, "red-fill", (r > 150) & (g < 130) & (b < 130), minpts=30)
clusters(430, 925, 45, 250, "blue-fill", (b > 140) & (r < 150) & (g < 170), minpts=30)
