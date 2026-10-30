import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
ra = np.asarray(R).astype(float)
ro = np.asarray(O).astype(float)


def lum(a, x0, y0, x1, y1, sc):
    sub = a[int(y0 * sc):int(y1 * sc), int(x0 * sc):int(x1 * sc)]
    return 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]


def stack(tag, a, x0, y0, x1, y1, sc):
    L = lum(a, x0, y0, x1, y1, sc)
    m = L < 215 * 0.75
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        print(tag, "empty"); return
    fx0 = x0 + int(xs.min()) / sc; fx1 = x0 + int(xs.max()) / sc
    fy0 = y0 + int(ys.min()) / sc; fy1 = y0 + int(ys.max()) / sc
    print(f"{tag}: bbox x{round(fx0)}..{round(fx1)} y{round(fy0)}..{round(fy1)} n={len(xs)}")


for tag, (x0, y0, x1, y1) in (("B1", (560, 138, 590, 212)), ("B2", (560, 276, 590, 350)), ("B3", (560, 418, 590, 492))):
    stack("ORIG  " + tag, ro, x0, y0, x1, y1, 1.0)
    stack("RENDER" + tag, ra, x0, y0, x1, y1, s)
    print()

for nm, a, sc in (("ORIG", ro, 1.0), ("RENDER", ra, s)):
    for tag, (x0, y0, x1, y1) in (("ell1", (512, 212, 618, 250)), ("ell3", (518, 488, 624, 527))):
        stack(f"{nm} {tag}", a, x0, y0, x1, y1, sc)
    print()
