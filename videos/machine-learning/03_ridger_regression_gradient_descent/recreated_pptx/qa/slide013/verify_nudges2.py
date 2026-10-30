import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0

ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)


def sub(arr, x0, y0, x1, y1):
    return arr[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


def bbox_x(cond, x0):
    ys, xs = np.nonzero(cond)
    if len(xs) == 0:
        return None
    return (round(x0 + xs.min() / s), round(x0 + xs.max() / s), len(xs))


# 1. BLACK-only value ink inside the W boxes (brackets are RED: R>120,G<80,B<80)
for tag, (x0, y0, x1, y1) in (
    ("B1", (566, 135, 586, 215)),
    ("B2", (566, 272, 586, 353)),
    ("B3", (566, 406, 586, 491)),
):
    rr = sub(ra, x0, y0, x1, y1)
    black = (rr[:, :, 0] < 110) & (rr[:, :, 1] < 110) & (rr[:, :, 2] < 110)
    print(f"{tag} render BLACK value ink -> frame x", bbox_x(black, x0))
    oo = ro[y0:y1, x0:x1]
    blacko = (oo[:, :, 0] < 110) & (oo[:, :, 1] < 110) & (oo[:, :, 2] < 110)
    print(f"{tag} orig   BLACK value ink -> frame x", bbox_x(blacko, x0))

# 2. WHITE text ink inside the label boxes
for tag, (x0, y0, x1, y1) in (("Train", (96, 96, 161, 126)), ("Test", (801, 96, 867, 126))):
    rr = sub(ra, x0, y0, x1, y1)
    wr = (rr[:, :, 0] > 150) & (rr[:, :, 1] > 150) & (rr[:, :, 2] > 150)
    print(f"{tag} render WHITE text -> frame x", bbox_x(wr, x0))
    oo = ro[y0:y1, x0:x1]
    wo = (oo[:, :, 0] > 150) & (oo[:, :, 1] > 150) & (oo[:, :, 2] > 150)
    print(f"{tag} orig   WHITE text -> frame x", bbox_x(wo, x0))

# 3. title CORE red: saturated red pixels only, render and original
rr = sub(ra, 200, 70, 760, 95)
cr = (rr[:, :, 0] > 130) & (rr[:, :, 1] < 90) & (rr[:, :, 2] < 90)
print("render title core red median:", np.median(rr[cr][:, 0]), np.median(rr[cr][:, 1]), np.median(rr[cr][:, 2]), "n=", len(rr[cr]))
oo = ro[70:95, 200:760]
co = (oo[:, :, 0] > 130) & (oo[:, :, 1] < 90) & (oo[:, :, 2] < 90)
if len(oo[co]):
    print("orig   title core red median:", np.median(oo[co][:, 0]), np.median(oo[co][:, 1]), np.median(oo[co][:, 2]), "n=", len(oo[co]))
    print("orig   title core red  min/max R:", oo[co][:, 0].min(), oo[co][:, 0].max())
