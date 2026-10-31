#!/usr/bin/env python3
"""Bounded robust fit of data->pixel affine for each plot in slide_021.jpg.

Each plot is a matplotlib render of a known analytic activation function, so
the red ink constrains (cx, cy, sx, sy) tightly; gridlines then fall on ticks.
"""
import numpy as np
from PIL import Image
from scipy.optimize import least_squares

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(float)
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]
red = (R > 105) & (R - G > 25) & (R - B > 25)


def pxset(box):
    x0, y0, x1, y1 = box
    sub = red[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.nonzero(sub)
    return xs + x0, ys + y0


def residual(p, px, py, fn):
    cx, cy, sx, sy = p[0], p[1], p[2], p[3]
    al = p[4] if len(p) > 4 else None
    xd = (px - cx) / sx
    if al is not None:
        yd = np.where(xd < 0, al * xd, xd)
    else:
        yd = fn(xd)
    # model pixel position of the curve at data x
    mx = cx + xd * sx
    my = cy - yd * sy
    return np.hypot(px - mx, py - my)


def report(name, box, fn, p0, names, five=False):
    px, py = pxset(box)
    lo, hi = [p * 0.4 for p in p0], [p * 2.5 if p > 0 else p * 0.6 for p in p0]
    lo[0], hi[0] = box[0], box[2]
    lo[1], hi[1] = box[1], box[3]
    if five:
        lo.append(0.02)
        hi.append(0.6)
        p0 = list(p0) + [0.1]
    res = least_squares(residual, p0, bounds=(lo, hi), loss="soft_l1", f_scale=1.0,
                        args=(px, py, fn), max_nfev=4000)
    p = res.x
    print(f"\n{name}: n={len(px)} params {dict(zip(names, [round(float(v), 4) for v in p]))}")
    return p


# ---------------- TL ReLU -------------------------------------------------
box = (122, 110, 399, 271)
p = report("TL_relu", box, lambda x: np.maximum(0.0, x), [260, 254, 9.7, 13.0], ["cx", "cy", "sx", "sy"])
cx, cy, sx, sy = p
print("   x ticks:", {v: round(cx + v * sx, 1) for v in (-10, -5, 5, 10)})
print("   f ticks:", {v: round(cy - v * sy, 1) for v in (5, 10)})

# ---------------- TR PReLU ------------------------------------------------
box = (564, 110, 841, 274)
p = report("TR_prelu", box, lambda x: x, [716, 216, 28, 28, 0.1], ["cx", "cy", "sx", "sy", "a"], five=True)
cx, cy, sx, sy = p[:4]; al = p[4] if len(p) > 4 else None
print("   x ticks:", {v: round(cx + v * sx, 1) for v in (-4, -2, 2, 4)})
print("   f ticks:", {v: round(cy - v * sy, 1) for v in (-2, -1, 1, 2, 3)})

# ---------------- BL ELU --------------------------------------------------
box = (122, 347, 399, 508)
p = report("BL_elu", box, lambda x: np.where(x<0, np.exp(x)-1.0, x), [265, 455.5, 35.2, 32.3, 1.0], ["cx", "cy", "sx", "sy", "a"], five=True)
cx, cy, sx, sy = p[:4]; al = p[4] if len(p) > 4 else None
print("   x ticks:", {v: round(cx + v * sx, 1) for v in (-3, -2, -1, 1, 2, 3)})
print("   f ticks:", {v: round(cy - v * sy, 1) for v in (-1, 1, 2, 3)})

# ---------------- BR SoftPlus --------------------------------------------
box = (564, 347, 841, 508)
p = report("BR_softplus", box, lambda x: np.logaddexp(0.0,x), [705.5, 477.5, 35, 35], ["cx", "cy", "sx", "sy"])
cx, cy, sx, sy = p
print("   x ticks:", {v: round(cx + v * sx, 1) for v in (-4, -2, 2, 4, 6)})
print("   f ticks:", {v: round(cy - v * sy, 1) for v in (-2, 2)})
