import sys
from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
for name, p in [("orig", "qa/rejudge2/orig_png/slide_022.png"),
                ("render", "recreated_pptx/renders/slide_022_recreated-1.png")]:
    im = Image.open(NS + "/" + p).convert("L")
    a = np.asarray(im).astype(float)
    H, W = a.shape
    ink = (a < 128)
    print(name, im.size)
    for by in range(8):
        row = ""
        for bx in range(16):
            blk = ink[by * H // 8:(by + 1) * H // 8, bx * W // 16:(bx + 1) * W // 16]
            row += "#" if blk.mean() > 0.08 else ("+" if blk.mean() > 0.02 else ".")
        print(row)
