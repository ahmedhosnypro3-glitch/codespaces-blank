import numpy as np
from PIL import Image

BASE = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent/"
R = Image.open(BASE + "recreated_pptx/qa/slide013/render/render_3-1.png").convert("RGB")
O = Image.open(BASE + "unique_slides/slide_013.jpg").convert("RGB")
s = R.size[1] / 540.0
print("render", R.size, "scale", s)

ra = np.asarray(R).astype(int)
ro = np.asarray(O).astype(int)


def px_region(arr, x0, y0, x1, y1):
    return arr[int(y0 * s):int(y1 * s), int(x0 * s):int(x1 * s)]


def mask_where(arr, cond):
    out = []
    ys, xs = np.nonzero(cond)
    if len(xs) == 0:
        return None
    return (xs.min(), ys.min(), xs.max(), ys.max(), len(xs))


# 1. black value ink inside band-1 W box (frame x566..586, y135..215)
for tag, (x0, y0, x1, y1) in (
    ("B1", (566, 135, 586, 215)),
    ("B2", (566, 272, 586, 353)),
    ("B3", (566, 406, 586, 491)),
):
    rx = px_region(ra, * (x0, y0, x1, y1))
    ro_ = px_region(ro, * (x0, y0, x1, y1))
    lum_r = 0.299 * rx[:, :, 0] + 0.587 * rx[:, :, 1] + 0.114 * rx[:, :, 2]
    lum_o = 0.299 * ro_[:, :, 0] + 0.587 * ro_[:, :, 1] + 0.114 * ro_[:, :, 2]
    mr = mask_where(None, lum_r < 100)
    mo = mask_where(None, lum_o < 120)
    print(f"{tag} render black-ink bbox (sub-px of region x{x0} y{y0}):", mr,
          "-> frame x", None if mr is None else (round(x0 + mr[0] / s), round(x0 + mr[2] / s)),
          "| original:", mo,
          "-> frame x", None if mo is None else (round(x0 + mo[0] / s), round(x0 + mo[2] / s)))

# 2. label-box white ink inside the blue boxes (frame bboxes)
for tag, (x0, y0, x1, y1) in (("Train", (96, 96, 161, 126)), ("Test", (801, 96, 867, 126))):
    rx = px_region(ra, * (x0, y0, x1, y1))
    ro_ = px_region(ro, * (x0, y0, x1, y1))
    wr = mask_where(None, rx[:, :, 0] > 230)
    wo = mask_where(None, ro_[:, :, 0] > 200)
    print(f"{tag} render white-ink bbox:", wr,
          "-> frame x", None if wr is None else (round(x0 + wr[0] / s), round(x0 + wr[2] / s)),
          "| original:", wo,
          "-> frame x", None if wo is None else (round(x0 + wo[0] / s), round(x0 + wo[2] / s)))

# 3. title ink colour core (render vs original), frame x200..760 y70..95
rx = px_region(ra, 200, 70, 760, 95)
ro_ = px_region(ro, 200, 70, 760, 95)
dark_r = rx[(0.299 * rx[:, :, 0] + 0.587 * rx[:, :, 1] + 0.114 * rx[:, :, 2]) < 190]
dark_o = ro_[(0.299 * ro_[:, :, 0] + 0.587 * ro_[:, :, 1] + 0.114 * ro_[:, :, 2]) < 190]
for nm, d in (("render", dark_r), ("orig", dark_o)):
    if len(d):
        print(f"title {nm} median dark RGB:", np.median(d[:, 0]), np.median(d[:, 1]), np.median(d[:, 2]), "n=", len(d))
