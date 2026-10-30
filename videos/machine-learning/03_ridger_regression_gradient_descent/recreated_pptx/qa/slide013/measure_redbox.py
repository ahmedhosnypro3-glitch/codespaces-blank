import numpy as np
from PIL import Image

BASE = '/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/'
im = Image.open(BASE + 'unique_slides/slide_013.jpg').convert('RGB')
a = np.asarray(im).astype(float)
lum = 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]
r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
RED = (r > g + 40) & (r > b + 40)

BANDS = [("B1", 126, 251), ("B2", 265, 389), ("B3", 402, 526)]
for (tag, y0, y1) in BANDS:
    print(f"### {tag} red-ink column groups inside the box (x508..622), whole band")
    cols = []
    for x in range(508, 623):
        cols.append((x, int(RED[y0 + 5:y1 - 5, x].sum())))
    nz = [c for c in cols if c[1] > 3]
    grp = []
    if nz:
        s = p = nz[0][0]
        for x, _ in nz[1:]:
            if x - p <= 2:
                p = x
            else:
                grp.append((s, p))
                s = p = x
        grp.append((s, p))
    print("  red col groups:", grp)
    # row groups
    rows = [(y, int(RED[y, 509:621].sum())) for y in range(y0, y1 + 1)]
    nzr = [c for c in rows if c[1] > 3]
    grpr = []
    if nzr:
        s = p = nzr[0][0]
        for y, _ in nzr[1:]:
            if y - p <= 2:
                p = y
            else:
                grpr.append((s, p))
                s = p = y
        grpr.append((s, p))
    print("  red row groups:", grpr)
