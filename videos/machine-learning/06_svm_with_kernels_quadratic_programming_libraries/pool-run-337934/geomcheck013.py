from PIL import Image
import numpy as np
NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
orig = Image.open(NS + "/qa/rejudge2/orig_png/slide_013.png").convert("RGB")
ren = Image.open(NS + "/recreated_pptx/renders/slide_013_recreated-1.png").convert("RGB")
a = np.asarray(ren).astype(int)
H, W = a.shape[:2]
r, g, b = a[..., 0], a[..., 1], a[..., 2]
red = (r > 150) & (g < 110) & (b < 110)
blue = (b > 150) & (r < 110) & (g < 110)
green = (g > 110) & (r < 120) & (b < 120) & (g > r + 30)


def bands(m, axis=0, minpx=3):
    rows = m.sum(axis=1) if axis == 0 else m.sum(axis=0)
    cur = None
    out = []
    for i, v in enumerate(rows):
        if v > minpx:
            if cur is None:
                cur = [i, i]
            else:
                cur[1] = i
        else:
            if cur:
                out.append(tuple(cur))
                cur = None
    if cur:
        out.append(tuple(cur))
    return out


sc = W / 960.0
print("== render red row bands (y in 960-frame px) ==")
for bd in bands(red):
    seg = red[bd[0]:bd[1] + 1, :]
    xs = np.nonzero(seg.sum(axis=0))[0]
    print("y %.0f-%.0f x %.0f-%.0f" % (bd[0] / sc, bd[1] / sc, xs.min() / sc, xs.max() / sc))
print("== render blue row bands ==")
for bd in bands(blue):
    seg = blue[bd[0]:bd[1] + 1, :]
    xs = np.nonzero(seg.sum(axis=0))[0]
    print("y %.0f-%.0f x %.0f-%.0f" % (bd[0] / sc, bd[1] / sc, xs.min() / sc, xs.max() / sc))
print("== render green extent ==")
ys, xs = np.nonzero(green)
print("x %.0f-%.0f y %.0f-%.0f" % (xs.min() / sc, xs.max() / sc, ys.min() / sc, ys.max() / sc))
