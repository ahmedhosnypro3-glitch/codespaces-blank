import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)

# non-background = not near-white and not near-panel-gray
bg = ((abs(im[:, :, 0] - 254) < 6) & (abs(im[:, :, 1] - 255) < 6) & (abs(im[:, :, 2] - 253) < 6)) | \
     ((abs(im[:, :, 0] - 233) < 8) & (abs(im[:, :, 1] - 233) < 8) & (abs(im[:, :, 2] - 231) < 10))
ink = ~bg


def label(mask):
    labels = np.zeros(mask.shape, dtype=np.int32)
    parent = [0]
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a
    nxt = 1
    H, W = mask.shape
    for y in range(H):
        for x in np.where(mask[y])[0]:
            up = labels[y - 1, x] if y > 0 else 0
            left = labels[y, x - 1] if x > 0 else 0
            if up and left:
                labels[y, x] = min(up, left)
                a, c = find(up), find(left)
                if a != c:
                    parent[max(a, c)] = min(a, c)
            elif up:
                labels[y, x] = up
            elif left:
                labels[y, x] = left
            else:
                parent.append(nxt); labels[y, x] = nxt; nxt += 1
    remap = {}
    for y in range(H):
        for x in range(W):
            v = labels[y, x]
            if v:
                rl = find(v)
                if rl not in remap: remap[rl] = len(remap) + 1
                labels[y, x] = remap[rl]
    return labels, len(remap)


y0, y1, x0, x1 = 120, 530, 440, 720
sub = ink[y0:y1, x0:x1]
lab, n = label(sub)
print(f"components in y{y0}..{y1} x{x0}..{x1}: {n}")
comps = []
for i in range(1, n + 1):
    ys, xs = np.where(lab == i)
    if len(ys) < 25:
        continue
    comps.append((ys.min() + y0, ys.max() + y0, xs.min() + x0, xs.max() + x0, len(ys)))
comps.sort()
for (cy0, cy1, cx0, cx1, a) in comps:
    print(f"\n-- comp y{cy0}..{cy1} x{cx0}..{cx1} w{cx1-cx0+1} h{cy1-cy0+1} area{a}")
    for y in range(cy0, cy1 + 1):
        print("   " + ''.join('#' if lab[y - y0, x - x0] else '.' for x in range(cx0, cx1 + 1)))
