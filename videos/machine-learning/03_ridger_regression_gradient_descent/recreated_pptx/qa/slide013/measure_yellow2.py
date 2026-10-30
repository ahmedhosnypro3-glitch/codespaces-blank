import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
YEL = (r > 235) & (g > 200) & (b < 170) & (r - b > 90) & (abs(r - g) < 60)

# connected components on yellow
def report(m, name, min_area=30):
    labels = np.zeros(m.shape, dtype=np.int32)
    parent = [0]
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    nxt = 1
    for y in range(m.shape[0]):
        for x in np.where(m[y])[0]:
            up = labels[y-1, x] if y > 0 else 0
            left = labels[y, x-1] if x > 0 else 0
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
    for y in range(m.shape[0]):
        for x in range(m.shape[1]):
            v = labels[y, x]
            if v:
                rl = find(v)
                if rl not in remap: remap[rl] = len(remap)+1
                labels[y, x] = remap[rl]
    print(f"--- {name} ---")
    out = []
    for i in range(1, len(remap)+1):
        ys, xs = np.where(labels == i)
        if len(ys) < min_area: continue
        out.append((int(ys.min()), int(ys.max()), int(xs.min()), int(xs.max()), len(ys)))
    out.sort()
    for y0,y1,x0,x1,a in out:
        print(f"  y{y0}..{y1} x{x0}..{x1}  w{x1-x0+1} h{y1-y0+1} area{a}")

report(YEL, "YELLOW fills (all)")
