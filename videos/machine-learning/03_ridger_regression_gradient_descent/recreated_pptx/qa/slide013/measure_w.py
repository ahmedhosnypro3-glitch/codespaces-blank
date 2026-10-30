import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = np.asarray(Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')).astype(int)
r, g, b = im[:, :, 0], im[:, :, 1], im[:, :, 2]

RED = (r > g + 40) & (r > b + 40)
BLUE = (b > r + 60) & (b > 100) & (g < r + 30)
BLK = (r < 120) & (g < 120) & (b < 120)


def prof(y0, y1, x0, x1, name):
    print(f"--- {name}: y{y0}..{y1} x{x0}..{x1} ---")
    for tag, m in (("BLUE", BLUE), ("RED", RED), ("BLK", BLK)):
        seg = m[y0:y1 + 1, x0:x1 + 1]
        cnt = seg.sum(axis=0)
        xs = np.where(cnt > 0)[0]
        if not len(xs):
            print(f"  {tag}: none")
            continue
        groups = []
        s = p = xs[0]
        for x in xs[1:]:
            if x - p <= 4:
                p = x
            else:
                groups.append((s, p))
                s = p = x
        groups.append((s, p))
        print(f"  {tag}: " + "  ".join(f"x{x0+a}..{x0+c}({int(seg[:,a:c+1].sum())})" for a, c in groups))


# band 1: the W construct region
prof(150, 250, 455, 690, "BAND1 W+arrow")
# band 2
prof(290, 390, 455, 690, "BAND2 W+arrow")
# band 3
prof(430, 528, 455, 690, "BAND3 W+arrow")

# yellow ellipse interiors
print("\n=== ellipse text ink (inside yellow, step map) ===")
YEL = (r > 240) & (g > 235) & (b < 150) & (abs(r - g) < 12)
for (y0, y1, x0, x1, tag) in ((215, 248, 512, 617, "ELL1"), (296, 327, 517, 618, "ELL2"),
                              (354, 386, 517, 619, "ELL3"), (435, 466, 519, 621, "ELL4"),
                              (491, 524, 520, 622, "ELL5")):
    ys, xs = np.where(YEL[y0:y1, x0:x1])
    if not len(ys):
        print(f"{tag}: no yellow")
        continue
    print(f"{tag}: yellow y{y0+ys.min()}..{y0+ys.max()} x{x0+xs.min()}..{x0+xs.max()}")
    # dark ink inside ellipse
    sub = im[y0:y1, x0:x1]
    dk = (sub[:, :, 0] < 150) & (sub[:, :, 1] < 150) & (sub[:, :, 2] < 150)
    ys2, xs2 = np.where(dk)
    if len(ys2):
        print(f"   dark-ink inside: y{y0+ys2.min()}..{y0+ys2.max()} x{x0+xs2.min()}..{x0+xs2.max()} n={dk.sum()}")
