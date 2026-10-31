from PIL import Image
import numpy as np

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
im = Image.open(NS + "/qa/rejudge2/orig_png/slide_022.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
pink = (r > 170) & (b > 200) & (g < 210) & (r - g > 20) & (b - g > 40)
ys, xs = np.nonzero(pink)
sel = xs < W * 0.42
xs2, ys2 = xs[sel], ys[sel]
print("left pink cluster: n=%d x %.3f..%.3f y %.3f..%.3f" % (sel.sum(), xs2.min()/W, xs2.max()/W, ys2.min()/H, ys2.max()/H))
sel2 = xs >= W * 0.42
xs3, ys3 = xs[sel2], ys[sel2]
print("right pink cluster: n=%d x %.3f..%.3f y %.3f..%.3f" % (sel2.sum(), xs3.min()/W, xs3.max()/W, ys3.min()/H, ys3.max()/H))

# test mathtext array with c|c
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "cm"
for latex in [r"\left[\begin{array}{c|c} a_1^2 & b_1^2 \\ 1 & 1 \end{array}\right]"]:
    try:
        fig = plt.figure(figsize=(4, 2), dpi=100)
        fig.text(0.05, 0.5, f"${latex}$", fontsize=16)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        print("array c|c OK, ink px:", (buf[..., 3] > 0).sum())
        plt.close(fig)
    except Exception as e:
        print("array c|c FAILED:", e)
