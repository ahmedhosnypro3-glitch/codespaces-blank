import numpy as np
from PIL import Image

NS = "/home/codespace/ai_llm_slides/videos/machine-learning/06_svm_with_kernels_quadratic_programming_libraries"
ren = Image.open(NS + "/recreated_pptx/renders/slide_043_recreated-1.png").convert("RGB")
orig = Image.open(NS + "/qa/rejudge2/orig_png/slide_043.png").convert("RGB")
print("render", ren.size, "orig", orig.size)

def scale_to(img, w=2001, h=1125):
    return img.resize((w, h))

R = np.asarray(scale_to(ren)).astype(int)
O = np.asarray(scale_to(orig)).astype(int)

def frac_color(arr, hexc, tol=60, region=None):
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    m = (abs(arr[..., 0] - r) < tol) & (abs(arr[..., 1] - g) < tol) & (abs(arr[..., 2] - b) < tol)
    if region:
        x0, y0, x1, y1 = region
        mm = np.zeros_like(m); mm[y0:y1, x0:x1] = m[y0:y1, x0:x1]; m = mm
    return m.mean()

# plot region in 2001x1125 space: [0.23,0.14,0.76,0.82]
px0, py0, px1, py1 = int(0.23*2001), int(0.14*1125), int(0.76*2001), int(0.82*1125)
region = (px0, py0, px1, py1)
print("plot region px:", region)
for name, c in [("blue", "0000FF"), ("green", "00FF00"), ("yellow", "FFFF00"),
                ("magenta", "FF00FF"), ("red", "FF0000"), ("cyan", "00FFFF"), ("black", "000000")]:
    fr = frac_color(R, c, 70, region)
    fo = frac_color(O, c, 70, region)
    print(f"{name:8s} {c} render_frac={fr:.5f} orig_frac={fo:.5f}")

# gray axes / grid presence in render
print("grid C0C0C0 render_frac:", frac_color(R, "C0C0C0", 25, region))
print("grid C0C0C0 orig_frac:  ", frac_color(O, "C0C0C0", 25, region))
# axis ink (dark gray 808080)
print("axis 808080 render_frac:", frac_color(R, "808080", 25, region))

# house chrome: red frame near edges, badge yellow at top-right
edge = np.concatenate([R[ int(0.15/7.5*1125)-3:int(0.15/7.5*1125)+4, :].reshape(-1,3),
                       R[:, int(0.15/13.33*2001)-3:int(0.15/13.33*2001)+4].reshape(-1,3)])
print("frame C00000 frac on edges:", frac_color(R, "C00000", 60))
bx0, by0, bx1, by1 = int(12.48/13.33*2001), int(0.30/7.5*1125), int(12.98/13.33*2001), int(0.80/7.5*1125)
badge = R[by0:by1, bx0:bx1]
print("badge FFF9C4 frac:", frac_color(R, "FFF9C4", 40, (bx0, by0, bx1, by1)))
# dark text ink in badge
m = (badge.sum(axis=2) < 250).mean()
print("badge dark-ink frac (numeral):", round(float(m), 4))

# overall ink coverage comparison
def inkfrac(arr):
    return (arr.sum(axis=2) < 600).mean()
print("ink frac render:", round(inkfrac(R), 5), " orig:", round(inkfrac(O), 5))

# text presence: count dark pixels in y-label strip and x-label strip (render)
yl = (int(0.20*2001), int(0.12*1125), int(0.23*2001), int(0.82*1125))
xl = (int(0.23*2001), int(0.82*1125), int(0.76*2001), int(0.87*1125))
print("y-label strip dark frac render:", round(float((R[yl[1]:yl[3], yl[0]:yl[2]].sum(axis=2) < 300).mean()), 5))
print("x-label strip dark frac render:", round(float((R[xl[1]:xl[3], xl[0]:xl[2]].sum(axis=2) < 300).mean()), 5))
print("y-label strip dark frac orig:  ", round(float((O[yl[1]:yl[3], yl[0]:yl[2]].sum(axis=2) < 300).mean()), 5))
print("x-label strip dark frac orig:  ", round(float((O[xl[1]:xl[3], xl[0]:xl[2]].sum(axis=2) < 300).mean()), 5))
