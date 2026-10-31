from PIL import Image
import numpy as np
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
orig = Image.open(NS + "/qa/rejudge2/orig_png/slide_013.png").convert("RGB")
ren = Image.open(NS + "/recreated_pptx/renders/slide_013_recreated-1.png").convert("RGB")
print("orig", orig.size, "render", ren.size)
a = np.asarray(ren).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 150) & (g < 110) & (b < 110)
blue = (b > 150) & (r < 110) & (g < 110)
green = (g > 110) & (r < 120) & (b < 120) & (g > r + 30)
cyan = (g > 200) & (b > 200) & (r < 230) & (b > r + 20)
black = (r < 80) & (g < 80) & (b < 80)

def extent(m, label):
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        print(label, "NONE")
    else:
        print(label, "x %d-%d y %d-%d px %d" % (xs.min(), xs.max(), ys.min(), ys.max(), m.sum()))

scale = W / 960.0
extent(red, "red")
extent(blue, "blue")
extent(green, "green")
extent(cyan, "cyan-fill")
extent(black, "black")
# ink coverage fraction
ink = (a.sum(axis=2) < 700)
print("ink fraction %.4f" % ink.mean())
