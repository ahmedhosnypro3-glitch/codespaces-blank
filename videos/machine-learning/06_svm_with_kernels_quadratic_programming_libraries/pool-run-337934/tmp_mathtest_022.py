from PIL import Image
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
matplotlib.rcParams["mathtext.fontset"] = "cm"

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
im = Image.open(NS + "/qa/rejudge2/orig_png/slide_022.png").convert("RGB")
a = np.asarray(im).astype(int)
H, W, _ = a.shape
r, g, b = a[..., 0], a[..., 1], a[..., 2]
pink = (r > 170) & (b > 200) & (g < 210) & (r - g > 20) & (b - g > 40)
ys, xs = np.nonzero(pink)
sel = (xs < W * 0.42) & (ys > H * 0.70)
print("callout tight: n=%d x %.3f..%.3f y %.3f..%.3f" % (sel.sum(), xs[sel].min()/W, xs[sel].max()/W, ys[sel].min()/H, ys[sel].max()/H))

tests = {
    "array_cc": r"\begin{array}{cc} a_1^2 & b_1^2 \\ 1 & 1 \end{array}",
    "array_cc_brackets": r"\left[\begin{array}{cc} a_1^2 & b_1^2 \\ 1 & 1 \end{array}\right]",
    "matrix": r"\begin{matrix} a & b \\ c & d \end{matrix}",
    "pmatrix": r"\begin{pmatrix} a_1 & b_1 \\ a_2 & b_2 \end{pmatrix}",
    "top": r"\left[a^{T}b+1\right]^{2}",
    "calc": r"\mathrm{Calculate}\ a^{T}b",
}
for name, latex in tests.items():
    try:
        fig = plt.figure(figsize=(6, 3), dpi=100)
        fig.text(0.05, 0.5, f"${latex}$", fontsize=16)
        fig.canvas.draw()
        buf = np.asarray(fig.canvas.buffer_rgba())
        print(name, "OK ink:", int((buf[..., 3] > 0).sum()))
        plt.close(fig)
    except Exception as e:
        print(name, "FAILED:", str(e)[:120])
