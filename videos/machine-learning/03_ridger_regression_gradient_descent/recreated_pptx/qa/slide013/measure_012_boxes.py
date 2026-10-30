import numpy as np
from PIL import Image

# 012 label boxes per the banked component: LABELS[0] = x68..198 y104..134 fill BLUE
# TEST_DATA_LABEL = x767..867 y96..126 fill BLUE, white bold text
# Check the certified render and the original frame for filled colour boxes.
for path, s in (
    ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/recreated_pptx/qa/slide012/render_3.png', 2001 / 960.0),
    ('/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/unique_slides/slide_012.jpg', 1.0),
):
    im = np.asarray(Image.open(path).convert('RGB')).astype(int)
    H, W = im.shape[:2]
    r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    print(f"### {path.split('/')[-1]} ({W}x{H})")


    def label(mask):
        labels = np.zeros(mask.shape, dtype=np.int32)
        parent = [0]
        def find(a):
            while parent[a] != a:
                parent[a] = parent[parent[a]]
                a = parent[a]
            return a
        nxt = 1
        for y in range(mask.shape[0]):
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
                    parent.append(nxt)
                    labels[y, x] = nxt
                    nxt += 1
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


    BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
    RED = (r > g + 40) & (r > b + 40)
    YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)
    for name, m in (("BLUE", BLUE), ("RED", RED), ("YEL", YEL)):
        lab, n = label(m)
        out = []
        for i in range(1, n + 1):
            ys, xs = np.where(lab == i)
            if len(ys) < 300:
                continue
            out.append((int(xs.min() / s), int(ys.min() / s), int(xs.max() / s), int(ys.max() / s), len(ys)))
        out.sort(key=lambda t: (t[1], t[0]))
        print(f"  {name} filled boxes (frame px):")
        for x0, y0, x1, y1, a in out:
            print(f"    x{x0}..{x1} y{y0}..{y1} w{x1-x0+1} h{y1-y0+1} area{a}")
