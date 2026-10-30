#!/usr/bin/env python3
"""Equation fit + asset generation for slide 005 (deck 03).

Equations are rendered with matplotlib mathtext in Professional 2D format
(stacked fractions with a horizontal bar, spatially aligned super/subscripts —
founder directive 2026-10-09) at 600 dpi. Font size is chosen by matching the
RENDERED INK EXTENT to the measured ORIGINAL ink box (see
qa/slide005/measure_slide005.json) so the recreation's geometry matches the
original at 150 dpi.

Measurement uses Text.get_window_extent() (no full-figure rasterisation, so no
huge allocations); the PNG is rasterised once per equation at the fitted size.

Output: recreated_pptx/build/assets/eq_005_*.png + .json sidecars
         (rel_id/image/mathtext/font_size_pt/color + w_px/h_px/w_in/h_in)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD = 12                      # px padding baked into the tight bbox (600 dpi)
ROOT = "videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = ROOT + "/recreated_pptx/build/assets"
OUTJSON = ROOT + "/recreated_pptx/qa/slide005/eq_fit_slide005.json"

# mathtext, measured ORIGINAL ink box (frame px, inclusive), asset basename
# ink boxes re-measured 2026-10-24 from unique_slides/slide_005.jpg with clean
# windows (the earlier bands were contaminated by the blue box border and the
# "Remember" label — see qa/slide005/id_rem2.py for the glyph-group proof that
# both Remember boxes carry the same identity X^T(XW) = (XW)^T X).
# \dfrac (not \frac) — measured 2026-10-24: the original's stacked fractions set
# the numerator/denominator at FULL size, which \dfrac reproduces (h/w = 0.101 vs
# the original's 0.094) while plain \frac is far too flat (h/w = 0.068).
EQS = [
    ("eq1", r"Loss = \dfrac{1}{2}\,(Y-\hat{Y})^{T}(Y-\hat{Y}) = "
            r"\dfrac{1}{2}\,(Y-XW)^{T}(Y-XW)", (98, 544, 109, 150), "eq_005_loss1"),
    ("eq2", r"Loss = \dfrac{1}{2}\left[Y^{T}Y + (XW)^{T}(XW) - "
            r"Y^{T}(XW) - (XW)^{T}Y\right]", (97, 629, 173, 214), "eq_005_loss2"),
    ("eq3", r"Loss = \dfrac{1}{2}\left[Y^{T}Y + (XW)^{T}(XW) - "
            r"2(XW)^{T}Y\right]", (98, 522, 230, 271), "eq_005_loss3"),
    ("pink", r"\dfrac{\partial Loss}{\partial W} = 0", (79, 164, 294, 338),
     "eq_005_pinkfrac"),
    ("eq4", r"\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[(XW)^{T}(X) + "
            r"(X)^{T}(XW) - 2(X)^{T}Y\right]", (97, 592, 375, 417), "eq_005_deriv1"),
    # eq5 is the arrow CHAIN (analysis/slide_005_final.json equations[5]):
    # ... -> (X^T X)W = X^T Y ->  ; the final W = (X^T X)^-1 X^T Y sits in the
    # green-outlined box at the right of the same row.
    ("eq5", r"\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[2X^{T}XW - "
            r"2X^{T}Y\right] \rightarrow (X^{T}X)\underline{W} = X^{T}Y \rightarrow",
     (96, 637, 460, 502), "eq_005_deriv2"),
    ("green", r"W = (X^{T}X)^{-1}X^{T}Y", (690, 878, 465, 497), "eq_005_finalw"),
    ("rem1", r"X^{T}(XW) = (XW)^{T}X", (680, 864, 213, 235), "eq_005_remember1"),
    ("rem2", r"X^{T}(XW) = (XW)^{T}X", (660, 867, 395, 420), "eq_005_remember2"),
]


def probe(mathtext, size):
    """Ink extent in FRAME px (72dpi) for mathtext at `size` pt. Cheap: no raster."""
    fig = plt.figure(figsize=(4, 2), dpi=72)
    fig.patch.set_alpha(0.0)
    t = fig.text(0.5, 0.5, f"${mathtext}$", fontsize=size, color="black",
                 ha="center", va="baseline")
    fig.canvas.draw()
    r = fig.canvas.get_renderer()
    bb = t.get_window_extent(renderer=r)
    plt.close(fig)
    return (bb.width, bb.height)      # px at 72 dpi == frame px


def render(mathtext, size, out):
    """Render tight transparent 600dpi PNG with PAD margin; return px geometry."""
    wf, hf = probe(mathtext, size)
    # canvas sized to the measured ink + generous slack, in inches
    win, hin = wf / 72 + 1.0, hf / 72 + 1.0
    fig = plt.figure(figsize=(win, hin), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${mathtext}$", fontsize=size, color="black",
             ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    plt.close(fig)
    if not len(rows):
        raise SystemExit(f"no ink for {mathtext!r}")
    y0 = max(int(rows.min()) - PAD, 0)
    y1 = min(int(rows.max()) + PAD + 1, buf.shape[0])
    x0 = max(int(cols.min()) - PAD, 0)
    x1 = min(int(cols.max()) + PAD + 1, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    h, w = y1 - y0, x1 - x0
    return w, h


os.makedirs(ASSETS, exist_ok=True)
results = {}
for key, mx, (x0, x1, y0, y1), name in EQS:
    ow, oh = x1 - x0 + 1, y1 - y0 + 1
    lo, hi = 4.0, 60.0
    for _ in range(26):
        mid = (lo + hi) / 2
        if probe(mx, mid)[0] < ow:
            lo = mid
        else:
            hi = mid
    size = round((lo + hi) / 2, 1)
    wf, hf = probe(mx, size)
    out = f"{ASSETS}/{name}.png"
    wpx, hpx = render(mx, size, out)
    geo = {
        "path": out, "w_px": wpx, "h_px": hpx,
        "w_in": round(wpx / DPI, 5), "h_in": round(hpx / DPI, 5),
        "pad_px": PAD, "dpi": DPI,
        "mathtext": mx, "font_size_pt": size, "color": "000000",
        "rel_id": None, "image": name + ".png",
        "orig_ink_px": [x0, x1, y0, y1],
        "render_ink_frames_px": [round(wf, 1), round(hf, 1)],
    }
    with open(out.replace(".png", ".json"), "w") as f:
        json.dump(geo, f, indent=1)
    results[key] = geo
    print(f"{key:6s} size={size:5.1f}pt  ink {wf:6.1f}x{hf:5.1f} fr px "
          f"vs orig {ow}x{oh}  -> {wpx}x{hpx} px@600")

with open(OUTJSON, "w") as f:
    json.dump(results, f, indent=1)
print("wrote", OUTJSON)
