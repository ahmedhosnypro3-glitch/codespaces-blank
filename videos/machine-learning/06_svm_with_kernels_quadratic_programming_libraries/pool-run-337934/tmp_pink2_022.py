from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
for name, p in [("orig", "qa/rejudge2/orig_png/slide_022.png"),
                ("render", "recreated_pptx/renders/slide_022_recreated-1.png")]:
    im = Image.open(NS + "/" + p).convert("RGB")
    a = np.asarray(im).astype(int)
    H, W, _ = a.shape
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    pink = (r > 170) & (b > 200) & (g < 210) & (r - g > 20) & (b - g > 40)
    print(name, im.size)
    for by in range(16):
        row = ""
        for bx in range(24):
            blk = pink[by * H // 16:(by + 1) * H // 16, bx * W // 24:(bx + 1) * W // 24]
            m = blk.mean()
            row += "#" if m > 0.3 else ("+" if m > 0.08 else ".")
        print(row)
