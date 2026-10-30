import os
from PIL import Image
import numpy as np

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_031.jpg"
REND = DECK + "/recreated_pptx/qa/slide031/render_9.png"
SC = 1125 / 540.0  # render px per frame px

o = np.asarray(Image.open(ORIG).convert("RGB")).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
print("orig", o.shape, "render", r.shape, "scale", SC)


def lum(a):
    return 0.299 * a[:, :, 0] + 0.587 * a[:, :, 1] + 0.114 * a[:, :, 2]


# ---------- TITLE BAND: frame y 55..95, x 30..700 ----------
print("\n=== TITLE BAND (frame y55..95) ===")
oTitle = lum(o)
# red pixels
def mask_color(a, rgb, tol):
    return (np.abs(a[:, :, 0] - rgb[0]) <= tol) & \
           (np.abs(a[:, :, 1] - rgb[1]) <= tol) & \
           (np.abs(a[:, :, 2] - rgb[2]) <= tol)


def spans(mask, rowrng, colrng, axis="row"):
    """Return contiguous spans of True along rowrng/colrng."""
    sub = mask[rowrng[0]:rowrng[1], colrng[0]:colrng[1]]
    if axis == "row":
        colsum = sub.sum(axis=0)
    else:
        colsum = sub.sum(axis=1)
    on = colsum > 0
    out = []
    st = None
    for i, v in enumerate(on):
        if v and st is None:
            st = i
        elif not v and st is not None:
            out.append((st, i - 1))
            st = None
    if st is not None:
        out.append((st, len(on) - 1))
    # offset back to absolute coords
    if axis == "row":
        return [(a + colrng[0], b + colrng[0]) for a, b in out]
    return [(a + rowrng[0], b + rowrng[0]) for a, b in out]


# ORIGINAL: red-ish ink in title band
oRed = (oTitle < 150) & (o[:, :, 0] > 110) & (o[:, :, 0] - o[:, :, 1] > 40) & (o[:, :, 0] - o[:, :, 2] > 40)
print("orig red spans (row 55:95):", spans(oRed, (55, 95), (30, 700)))
# green-ish
oGreen = (oTitle < 150) & (o[:, :, 1] > 90) & (o[:, :, 1] - o[:, :, 0] > 25) & (o[:, :, 1] - o[:, :, 2] > 25)
print("orig green spans (row 55:95):", spans(oGreen, (55, 95), (30, 700)))
# blue-ish
oBlue = (oTitle < 150) & (o[:, :, 2] > 90) & (o[:, :, 2] - o[:, :, 0] > 25) & (o[:, :, 2] - o[:, :, 1] > 25)
print("orig blue spans (row 55:95):", spans(oBlue, (55, 95), (30, 700)))

# RENDER (scale by SC to frame px)
rR = (r[:, :, 0] > 110) & (r[:, :, 0] - r[:, :, 1] > 40) & (r[:, :, 0] - r[:, :, 2] > 40) & (lum(r) < 150)
print("render red spans (rows 55*SC:95*SC):",
      spans(rR, (int(55 * SC), int(95 * SC)), (int(30 * SC), int(700 * SC))))
rG = (r[:, :, 1] > 90) & (r[:, :, 1] - r[:, :, 0] > 25) & (r[:, :, 1] - r[:, :, 2] > 25) & (lum(r) < 150)
print("render green spans:",
      spans(rG, (int(55 * SC), int(95 * SC)), (int(30 * SC), int(700 * SC))))
rB = (r[:, :, 2] > 90) & (r[:, :, 2] - r[:, :, 0] > 25) & (r[:, :, 2] - r[:, :, 1] > 25) & (lum(r) < 150)
print("render blue spans:",
      spans(rB, (int(55 * SC), int(95 * SC)), (int(30 * SC), int(700 * SC))))

# ---------- EQUATION BOX ----------
print("\n=== EQUATION BOX ===")
# frame box: x 398..531, y 184..212. Inside: x 400..530, y 186..210
oEq = lum(o)[186:211, 400:531]
dark = oEq < 120
ys, xs = np.nonzero(dark)
if len(xs):
    print("orig eq ink bbox: x %.1f..%.1f y %.1f..%.1f  (%d px)" %
          (xs.min() + 400, xs.max() + 400, ys.min() + 186, ys.max() + 186, len(xs)))
rEq = lum(r)[int(186 * SC):int(211 * SC), int(400 * SC):int(531 * SC)]
darkr = rEq < 120
ys2, xs2 = np.nonzero(darkr)
if len(xs2):
    print("render eq ink bbox (render px): x %.1f..%.1f y %.1f..%.1f (%d px) -> frame x %.1f..%.1f" %
          (xs2.min() + int(400 * SC), xs2.max() + int(400 * SC),
           ys2.min() + int(186 * SC), ys2.max() + int(186 * SC), len(xs2),
           (xs2.min() + int(400 * SC)) / SC, (xs2.max() + int(400 * SC)) / SC))
print("orig eq ink density per column (last 20 cols of box):")
prof = dark.sum(axis=0)
print("  ", " ".join(str(v) for v in prof[-30:]))
prof2 = darkr.sum(axis=0)
print("render last 30 cols:", " ".join(str(v) for v in prof2[-30:]))

# ---------- ANNOTATION BOX: line1 line2 ----------
print("\n=== ANNOTATION LINES ===")
for name, y0, y1 in [("ann line1", 244, 264), ("ann line2", 265, 288)]:
    oA = lum(o)[y0:y1, 245:810]
    d = oA < 120
    ys3, xs3 = np.nonzero(d)
    if len(xs3):
        print("orig %s ink x %.1f..%.1f y %.1f..%.1f (%d px)" % (name, xs3.min() + 245, xs3.max() + 245, ys3.min() + y0, ys3.max() + y0, len(xs3)))
    rA = lum(r)[int(y0 * SC):int(y1 * SC), int(245 * SC):int(810 * SC)]
    dr = rA < 120
    ys4, xs4 = np.nonzero(dr)
    if len(xs4):
        print("render %s ink x %.1f..%.1f (render px) -> frame %.1f..%.1f  (%d px)" %
              (name, xs4.min() + int(245 * SC), xs4.max() + int(245 * SC),
               (xs4.min() + int(245 * SC)) / SC, (xs4.max() + int(245 * SC)) / SC, len(xs4)))
