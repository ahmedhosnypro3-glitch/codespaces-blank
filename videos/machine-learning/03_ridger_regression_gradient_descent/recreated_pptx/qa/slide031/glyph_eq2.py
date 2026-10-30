import numpy as np
from PIL import Image

DECK = "/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/03_ridger_regression_gradient_descent"
ORIG = DECK + "/unique_slides/slide_031.jpg"
REND = DECK + "/recreated_pptx/qa/slide031/render_9.png"

# matched effective scale: original upscaled by H_render/540 via LANCZOS
K = 1125 / 540.0
o_img = Image.open(ORIG).convert("RGB")
o_up = o_img.resize((int(round(960 * K)), int(round(540 * K))), Image.LANCZOS)
o = np.asarray(o_up).astype(int)
r = np.asarray(Image.open(REND).convert("RGB")).astype(int)
print("orig upscaled", o.shape, "render", r.shape)


def region_box(arr, fx0, fy0, fx1, fy1):
    """Return (lum, mask) for a frame-px window, at render resolution."""
    x0, x1 = int(round(fx0 * K)), int(round(fx1 * K))
    y0, y1 = int(round(fy0 * K)), int(round(fy1 * K))
    sub = arr[y0:y1, x0:x1]
    lum = 0.299 * sub[:, :, 0] + 0.587 * sub[:, :, 1] + 0.114 * sub[:, :, 2]
    return lum


def groups(lum, thresh=170, gap=8):
    m = lum < thresh
    colsum = m.sum(axis=0)
    on = colsum > 0
    raw, st = [], None
    for i, v in enumerate(on):
        if v and st is None:
            st = i
        elif not v and st is not None:
            raw.append((st, i - 1)); st = None
    if st is not None:
        raw.append((st, len(on) - 1))
    merged = []
    for a, b in raw:
        if merged and a - merged[-1][1] <= gap:
            merged[-1] = (merged[-1][0], b)
        else:
            merged.append((a, b))
    return merged, m


def art(m, a, b, label, maxh=200):
    sub = m[:, a:b + 1]
    # vertical trim
    rs = np.nonzero(sub.sum(axis=1))[0]
    if len(rs) == 0:
        print("  %s EMPTY" % label); return
    sub = sub[rs[0]:rs[-1] + 1]
    if len(sub) > maxh:
        step = int(np.ceil(len(sub) / maxh))
        sub = sub[::step]
    print("  %-10s x %d..%d (w=%.1f frame px)  y %d..%d"
          % (label, a, b, (b - a + 1) / K, rs[0], rs[-1]))
    for row in sub:
        print("    |" + "".join("#" if v else "." for v in row) + "|")


# EQUATION interior: frame x 400..528, y 186..210
print("############ EQUATION: ORIGINAL (upscaled x%d LANCZOS) ############" % K)
lo = region_box(o, 400, 186, 528, 210)
go, mo = groups(lo)
print("groups:", len(go))
for i, (a, b) in enumerate(go):
    art(mo, a, b, "orig-g%d" % i)

print()
print("############ EQUATION: RENDER ############")
lr = region_box(r, 400, 186, 528, 210)
gr, mr = groups(lr)
print("groups:", len(gr))
for i, (a, b) in enumerate(gr):
    art(mr, a, b, "rend-g%d" % i)
