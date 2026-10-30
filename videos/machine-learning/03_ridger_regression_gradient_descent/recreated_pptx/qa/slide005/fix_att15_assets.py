#!/usr/bin/env python3
"""Attempt-15 asset fixes for slide 005 (deck 03) — att13 left-edge clips + rem1.

The banked assets for eq2/eq4/eq5 were LEFT-TRIMMED by an intermediate process
(proven PIL-first: eq_005_loss2.png opens mid-"Loss" with "oss = ...", ink starts
col 4 instead of the rendered PAD=12; eq_005_deriv2.png numerator opens "oss";
eq_005_deriv1.png lost 25px of the ∂ limb). Re-rendering with the exact
eq_fit_slide005.py probe()/render() reproduces clean untrimmed output.

eq_005_remember1.png carries the WRONG identity: the original's UPPER Remember
box reads Y^T(XW) = (XW)^T Y (glyph-verified), not X^T(XW) = (XW)^T X.

Only these four assets + sidecars are rewritten. eq_005_loss1 keeps its red-½
recolor (this script is black-only, so it must never run over loss1), and
eq_005_remember2 keeps the prior carrier's X-terminal fix. eq_fit_slide005.json
(the aggregate fit record) is NOT rewritten.
"""
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

DPI = 600
PAD = 12
ROOT = "videos/machine-learning/03_ridger_regression_gradient_descent"
ASSETS = ROOT + "/recreated_pptx/build/assets"

EQS = [
    ("eq2", r"Loss = \dfrac{1}{2}\left[Y^{T}Y + (XW)^{T}(XW) - "
            r"Y^{T}(XW) - (XW)^{T}Y\right]", (97, 629, 173, 214), "eq_005_loss2"),
    ("eq4", r"\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[(XW)^{T}(X) + "
            r"(X)^{T}(XW) - 2(X)^{T}Y\right]", (97, 592, 375, 417), "eq_005_deriv1"),
    ("eq5", r"\dfrac{\partial Loss}{\partial W} = 0 = \dfrac{1}{2}\left[2X^{T}XW - "
            r"2X^{T}Y\right] \rightarrow (X^{T}X)\underline{W} = X^{T}Y \rightarrow",
     (96, 637, 460, 502), "eq_005_deriv2"),
    ("rem1", r"Y^{T}(XW) = (XW)^{T}Y", (680, 864, 213, 235), "eq_005_remember1"),
]


def probe(mathtext, size):
    fig = plt.figure(figsize=(4, 2), dpi=72)
    fig.patch.set_alpha(0.0)
    t = fig.text(0.5, 0.5, f"${mathtext}$", fontsize=size, color="black",
                 ha="center", va="baseline")
    fig.canvas.draw()
    bb = t.get_window_extent(renderer=fig.canvas.get_renderer())
    plt.close(fig)
    return (bb.width, bb.height)


def render(mathtext, size, out):
    wf, hf = probe(mathtext, size)
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
    if cols.min() < PAD or (buf.shape[1] - 1 - cols.max()) < PAD:
        raise SystemExit(f"ink touches canvas edge for {mathtext!r} — would trim")
    y0 = int(rows.min()) - PAD
    y1 = int(rows.max()) + PAD + 1
    x0 = int(cols.min()) - PAD
    x1 = int(cols.max()) + PAD + 1
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    # post-save proof: inside the saved crop, ink must start exactly at col PAD
    a = np.asarray(Image.open(out))[:, :, 3]
    first = int(np.where((a > 8).any(axis=0))[0].min())
    assert first == PAD, f"{out}: first ink col {first} != {PAD}"
    return x1 - x0, y1 - y0


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
    print(f"{key:5s} size={size:5.1f}pt  ink {wf:6.1f}x{hf:5.1f} fr px "
          f"vs orig {ow}x{oh}  -> {wpx}x{hpx} px@600  first_ink_col=PAD ok")
