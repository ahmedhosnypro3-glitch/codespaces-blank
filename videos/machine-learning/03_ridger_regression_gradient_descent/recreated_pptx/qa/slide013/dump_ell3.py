import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)

REGIONS = [("ELL1", 214, 250, 508, 610), ("ELL2", 352, 389, 508, 612), ("ELL3", 490, 527, 512, 616)]
for (name, y0, y1, x0, x1) in REGIONS:
    sub = a[y0:y1, x0:x1]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    ys, xs = np.where(lum < 235)
    print(f"### {name}: n={len(ys)}")
    if len(ys):
        print("   bbox y%d..%d x%d..%d" % (ys.min() + y0, ys.max() + y0, xs.min() + x0, xs.max() + x0))
        print("   lum range %.0f..%.0f" % (lum.min(), lum[ys].max()))
    # print everything under 235 as ink
    print("### map (lum<200 = #, lum<225 = +, else .)")
    for y in range(y0, y1):
        row = ''
        for x in range(x0, x1):
            v = 0.299 * a[y, x, 0] + 0.587 * a[y, x, 1] + 0.114 * a[y, x, 2]
            row += '#' if v < 200 else ('+' if v < 225 else '.')
        print(f"{y:4d}| {row}")
    print()
