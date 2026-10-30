import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
H, W = im.shape[:2]
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
RED = (r > g + 40) & (r > b + 40)
YELLOW = (r > 150) & (g > 130) & (b < 130) & (abs(r - g) < 70)


def label(mask):
    """Two-pass 4-connected labeling (numpy, no scipy)."""
    labels = np.zeros(mask.shape, dtype=np.int32)
    parent = [0]

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, c):
        ra, rc = find(a), find(c)
        if ra != rc:
            parent[max(ra, rc)] = min(ra, rc)

    nxt = 1
    for y in range(mask.shape[0]):
        row = mask[y]
        for x in np.where(row)[0]:
            up = labels[y - 1, x] if y > 0 else 0
            left = labels[y, x - 1] if x > 0 else 0
            if up and left:
                labels[y, x] = min(up, left)
                union(up, left)
            elif up:
                labels[y, x] = up
            elif left:
                labels[y, x] = left
            else:
                parent.append(nxt)
                labels[y, x] = nxt
                nxt += 1
    # flatten
    remap = {}
    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            v = labels[y, x]
            if v:
                rl = find(v)
                if rl not in remap:
                    remap[rl] = len(remap) + 1
                labels[y, x] = remap[rl]
    return labels, len(remap)


def report(mask, label_name, min_area=60, max_rows=200):
    lab, n = label(mask)
    print(f"--- {label_name}: {n} raw components ---")
    rows = []
    for i in range(1, n + 1):
        ys, xs = np.where(lab == i)
        if len(ys) < min_area:
            continue
        rows.append((int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()), int(len(ys))))
    rows.sort(key=lambda t: (t[1], t[0]))
    for x0, y0, x1, y1, a in rows[:max_rows]:
        print(f"  x{x0}..{x1} y{y0}..{y1}  w{x1-x0+1} h{y1-y0+1} area{a}")
    if len(rows) > max_rows:
        print(f"  ... {len(rows)-max_rows} more")
    print(f"  total kept: {len(rows)}")


for m, l in ((RED, 'RED'), (BLUE, 'BLUE'), (YELLOW, 'YELLOW')):
    report(m, l)
    print()
