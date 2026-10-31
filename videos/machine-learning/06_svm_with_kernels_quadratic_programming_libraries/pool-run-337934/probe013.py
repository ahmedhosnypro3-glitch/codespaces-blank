from PIL import Image
import numpy as np
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
im = Image.open(NS + "/qa/rejudge2/orig_png/slide_013.png").convert("RGB")
a = np.asarray(im)
r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
dark = (r < 120) & (g < 120) & (b < 120)
red = (r > 150) & (g < 110) & (b < 110)
y0, y1, x0, x1 = 395, 485, 660, 830
for name, m in [("dark", dark), ("red", red)]:
    mm = m[y0:y1, x0:x1]
    rows = mm.sum(axis=1)
    cur = None
    bands = []
    for i, v in enumerate(rows):
        if v > 0:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur and cur[1] - cur[0] >= 2:
                bands.append(cur)
            cur = None
    if cur and cur[1] - cur[0] >= 2:
        bands.append(cur)
    print(name)
    for bd in bands:
        seg = mm[bd[0]:bd[1] + 1, :]
        cols = np.nonzero(seg.sum(axis=0))[0]
        print("  y %d-%d: x %d-%d w %d px %d" % (y0 + bd[0], y0 + bd[1], x0 + cols.min(), x0 + cols.max(), cols.max() - cols.min(), seg.sum()))
