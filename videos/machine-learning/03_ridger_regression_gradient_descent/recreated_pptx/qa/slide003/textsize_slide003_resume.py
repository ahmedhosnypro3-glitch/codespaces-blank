#!/usr/bin/env python3
"""Compare text-block ink heights/positions between original and render."""
import numpy as np
from PIL import Image

B = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
     "03_ridger_regression_gradient_descent")
o = np.asarray(Image.open(B + "/unique_slides/slide_003.jpg").convert(
    "RGB")).astype(int)
r = np.asarray(Image.open(B + "/recreated_pptx/qa/slide003/render_9.png").convert(
    "RGB").resize((960, 540), Image.LANCZOS)).astype(int)

# x-window that isolates the element, full y-range to scan
ELEMENTS = {
    "title":            (80, 58, 840, 96),
    "N Train Samples":  (78, 160, 285, 212),
    "topbox hdr X_1":   (294, 112, 340, 142),
    "topbox hdr X_2":   (370, 112, 418, 142),
    "topbox hdr X_n":   (512, 112, 560, 142),
    "topbox entries":   (292, 155, 560, 250),
    "topbox red y_1":   (294, 272, 340, 300),
    "Remember word":    (654, 155, 700, 185),
    "remember eq":      (695, 180, 872, 222),
    "In General":       (655, 260, 855, 300),
    "bl y_1":           (108, 360, 136, 395),
    "bl row1 cells":    (196, 366, 396, 394),
    "bl row2 cells":    (196, 395, 396, 424),
    "bl row4 cells":    (196, 455, 396, 482),
    "bl dim labels":    (75, 468, 545, 518),
    "w vector b":       (458, 355, 526, 385),
    "w vector entries": (460, 388, 522, 478),
    "br Y=X W":         (584, 350, 755, 378),
    "br where1":        (584, 382, 752, 410),
    "br where2":        (584, 412, 752, 470),
    "badge 3":          (860, 60, 896, 88),
}

print(f"{'element':20s} {'ORIG ink bbox':28s} {'RENDER ink bbox':28s}")
for nm, (x0, y0, x1, y1) in ELEMENTS.items():
    def ext(a):
        ys, xs = [], []
        for y in range(y0, y1):
            for x in range(x0, x1):
                if a[y, x].sum() < 560:
                    ys.append(y); xs.append(x)
        if not ys:
            return "-"
        return f"x{min(xs)}..{max(xs)} y{min(ys)}..{max(ys)} " \
               f"h={max(ys)-min(ys)+1} w={max(xs)-min(xs)+1}"
    print(f"{nm:20s} {ext(o):28s} {ext(r):28s}")
