import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"

EQ_BOXES = {
    31: [(0.121, 0.246, 0.217, 0.289), (0.125, 0.387, 0.235, 0.431),
         (0.408, 0.387, 0.535, 0.431), (0.121, 0.533, 0.238, 0.580),
         (0.408, 0.533, 0.560, 0.580), (0.129, 0.717, 0.333, 0.770)],
    32: [(0.10, 0.29, 0.90, 0.41), (0.10, 0.51, 0.75, 0.58),
         (0.10, 0.67, 0.85, 0.75), (0.10, 0.84, 0.92, 0.92)],
}

def classify(px):
    r, g, b = px[..., 0], px[..., 1], px[..., 2]
    dark = (r + g + b) < 450
    red = dark & (r > g + 40) & (r > b + 40)
    blue = dark & (b > r + 40) & (b > g + 20)
    green = dark & (g > r + 30) & (g > b + 30)
    black = dark & ~red & ~blue & ~green
    return black.sum(), red.sum(), blue.sum(), green.sum()

for n in (31, 32):
    im = Image.open(f"{NS}/recreated_pptx/renders/slide_{n:03d}_recreated-1.png").convert("RGB")
    a = np.asarray(im).astype(int)
    h, w = a.shape[:2]
    print(f"slide {n} render {w}x{h}")
    for i, (x0, y0, x1, y1) in enumerate(EQ_BOXES[n]):
        sub = a[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
        bk, rd, bl, gr = classify(sub)
        print(f"  eqbox{i}: black={bk:5d} red={rd:5d} blue={bl:5d} green={gr:5d}")
