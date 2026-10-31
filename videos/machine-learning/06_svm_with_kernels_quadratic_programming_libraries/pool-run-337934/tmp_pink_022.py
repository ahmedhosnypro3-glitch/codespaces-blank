from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
im = Image.open(NS + "/qa/rejudge2/orig_png/slide_022.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
# pink-ish: high R, mid G, high B, R-B moderate (CC99FF ~ (204,153,255))
r, g, b = a[..., 0], a[..., 1], a[..., 2]
pink = (r > 170) & (b > 200) & (g < 200) & (r - g > 20) & (b - g > 40)
ys, xs = np.nonzero(pink)
print("orig size", W, H, "pink px", pink.sum())
if pink.sum():
    print("pink bbox x", xs.min() / W, xs.max() / W, "y", ys.min() / H, ys.max() / H)
# also map purple box in our render
im2 = Image.open(NS + "/recreated_pptx/renders/slide_022_recreated-1.png").convert("RGB")
a2 = np.asarray(im2).astype(int)
r, g, b = a2[..., 0], a2[..., 1], a2[..., 2]
pink2 = (r > 170) & (b > 200) & (g < 200) & (r - g > 20) & (b - g > 40)
ys, xs = np.nonzero(pink2)
H2, W2 = pink2.shape
print("render size", W2, H2, "pink px", pink2.sum())
if pink2.sum():
    print("render pink bbox x", xs.min() / W2, xs.max() / W2, "y", ys.min() / H2, ys.max() / H2)
# fine ink map of orig bottom half, 16 cols x 16 rows
ink = (a.sum(axis=2) < 400)
for by in range(8, 16):
    row = ""
    for bx in range(16):
        blk = ink[by * H // 16:(by + 1) * H // 16, bx * W // 16:(bx + 1) * W // 16]
        row += "#" if blk.mean() > 0.08 else ("+" if blk.mean() > 0.02 else ".")
    print(row)
