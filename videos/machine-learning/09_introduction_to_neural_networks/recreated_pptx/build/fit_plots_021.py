#!/usr/bin/env python3
"""Fit the data->pixel affine transform of each of the four plots in
slide_021.jpg by minimizing red-ink distance to the known activation curves,
and sample the frame/badge colors."""
import numpy as np
from PIL import Image
from scipy.optimize import minimize

SRC = "/home/codespace/ai_llm_slides/videos/machine-learning/09_introduction_to_neural_networks/unique_slides/slide_021.jpg"
im = Image.open(SRC).convert("RGB")
a = np.asarray(im).astype(float)
H, W, _ = a.shape
R, G, B = a[:, :, 0], a[:, :, 1], a[:, :, 2]

red = (R > 105) & (R - G > 25) & (R - B > 25)

# --- colors -------------------------------------------------------------
redmask = (R > 100) & (R - G > 45) & (R - B > 45)
bluemask = (B > 100) & (B - R > 45) & (B - G > 30)
pinkmask = (R > 235) & (R - G > 10) & (R - G < 40) & (R - B > 10) & (R - B < 45)


def strongest(mask, region=None):
    sat = np.max(a, axis=2) - np.min(a, axis=2)
    m = mask & (sat > 40)
    if region:
        x0, y0, x1, y1 = region
        m = np.zeros_like(m)
        sub = a[y0:y1 + 1, x0:x1 + 1]
        s2 = np.max(sub, axis=2) - np.min(sub, axis=2)
        m[y0:y1 + 1, x0:x1 + 1] = s2 > 40
        satm = sat
        sc = np.where(m, satm, -1)
        i = np.argmax(sc)
        y, x = np.unravel_index(i, sc.shape)
        return tuple(int(v) for v in a[y, x]), (x, y)
    sc = np.where(m, sat, -1)
    i = np.argmax(sc)
    y, x = np.unravel_index(i, sc.shape)
    return tuple(int(v) for v in a[y, x]), (x, y)


print("red frame color:", strongest(redmask, (60, 350, 63, 360)))
print("pink fill color  :", strongest(pinkmask, (200, 70, 300, 90)))
print("badge numeral dark px near (876,70):")
for dy in range(-6, 7):
    row = []
    for dx in range(-14, 15):
        px = a[70 + dy, 876 + dx]
        if px.sum() < 400:
            row.append((dx, int(px[0]), int(px[1]), int(px[2])))
    if row:
        print("  dy", dy, row[:8])

print("\nblue frame color:", strongest(bluemask, (550, 250, 567, 260)))
print("bg color:", tuple(int(v) for v in a[300, 470]))

# --- fits ---------------------------------------------------------------
CURVES = {
    "TL_relu": (122, 110, 399, 271, lambda x: np.maximum(0.0, x)),
    "TR_prelu": (564, 110, 841, 274, lambda x: np.where(x < 0, 0.1 * x, x)),
    "BL_elu": (122, 347, 399, 508, lambda x: np.where(x < 0, np.exp(x) - 1.0, x)),
    "BR_softplus": (564, 347, 841, 508, lambda x: np.logaddexp(0.0, x)),
}


def fit(name, box, fn, xguess0=0.0, p0=None):
    x0, y0, x1, y1 = box
    sub = red[y0:y1 + 1, x0:x1 + 1]
    ys, xs = np.nonzero(sub)
    if len(xs) == 0:
        print(f"{name}: no red ink")
        return
    px = xs + x0
    py = ys + y0
    # drop obviously-outlier pixels (formula red, badge) by bbox of this plot
    t = np.linspace(-12, 12, 3000)

    def obj(p):
        cx, cy, sx, sy = p
        # convert each red pixel to data and compare with fn
        xd = (px - cx) / sx
        yd = (py - cy) / sy
        return np.mean((yd - fn(np.clip(xd, -30, 30))) ** 2)

    if p0 is None:
        # initial guess: use extreme points
        p0 = [(x0 + x1) / 2, (y0 + y1) / 2, 10.0, 10.0]
    res = minimize(obj, p0, method="Nelder-Mead",
                   options={"maxiter": 4000, "xatol": 1e-4, "fatol": 1e-6})
    cx, cy, sx, sy = res.x
    resid = np.sqrt(np.mean((obj(res.x))))
    print(f"\n{name}: n={len(px)} origin=({cx:.2f},{cy:.2f}) sx={sx:.3f} sy={sy:.3f} rms={resid:.3f}")
    for gx, gv in [("x ticks", None)]:
        pass
    return cx, cy, sx, sy


res = {}
for name, (x0, y0, x1, y1, fn) in CURVES.items():
    r = fit(name, (x0, y0, x1, y1), fn)
    res[name] = r
    if r is None:
        continue
    cx, cy, sx, sy = r
    # verify against measured gridlines
    if name == "TL_relu":
        print("   predict grid col for x=-10,0,10:", [round(cx + v * sx, 1) for v in (-10, 0, 10)],
              " rows for f=5,10:", [round(cy - v * sy, 1) for v in (5, 10)])
    if name == "BL_elu":
        print("   predict grid col for x=-3,0,3:", [round(cx + v * sx, 1) for v in (-3, 0, 3)],
              " rows for f=-1,3:", [round(cy - v * sy, 1) for v in (-1, 3)])
    if name == "BR_softplus":
        print("   predict grid col for x=-4,0,4:", [round(cx + v * sx, 1) for v in (-4, 0, 4)],
              " rows for f=1,2,3:", [round(cy - v * sy, 1) for v in (1, 2, 3)])
    if name == "TR_prelu":
        print("   predict grid col for x=-4,0,4:", [round(cx + v * sx, 1) for v in (-4, 0, 4)],
              " rows for f=-1,1,3:", [round(cy - v * sy, 1) for v in (-1, 1, 3)])
