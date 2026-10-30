#!/usr/bin/env python3
"""Render slide_004 equations in PROFESSIONAL 2D FORMAT (matplotlib mathtext
-> 600dpi tight transparent PNG) + eq_*.json sidecars (fleet contract).

Vectors use \substack inside \left(...\right) -- matplotlib mathtext has no
\begin{pmatrix}/matrix environments.
"""
import json
import os
import subprocess
import sys

import matplotlib
matplotlib.use("Agg")
import numpy as np
from PIL import Image

RENDER_EQ = "/workspaces/codespaces-blank/ai_llm_slides/scripts/render_eq.py"
ASSETS = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
          "03_ridger_regression_gradient_descent/recreated_pptx/build/assets")
DPI = 600

EQS = [
    # (name, mathtext, box interior x0..x1, available y0..y1, color)
    ("eq_004_Yvec",
     r"Let \ \mathbf{Y} = \left( \substack{y_1 \\ y_2 \\ \cdots \\ y_n} \right)_{n \times 1}",
     (84, 391), (103, 148), "000000"),
    ("eq_004_Yhatvec",
     r"Let \ \mathbf{\hat{Y}} = \left( \substack{\hat{y}_1 \\ \hat{y}_2 \\ \cdots \\ \hat{y}_n} \right)_{n \times 1}",
     (432, 741), (103, 155),
     "000000"),
    ("eq_004_norm",
     r"\|a\|_2 = a^{T} a", (787, 877), (120, 150), "000000"),
    ("eq_004_formula",
     r"Loss = \left\|Y - \mathbf{\hat{Y}}\right\|_2 = \left(Y - \mathbf{\hat{Y}}\right)^{T} \left(Y - \mathbf{\hat{Y}}\right)",
     (84, 480), (466, 518), "000000"),
]


def render(latex, out, fs, color):
    r = subprocess.run([sys.executable, RENDER_EQ, latex, out, str(fs), color],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def ink_box(png):
    a = np.asarray(Image.open(png).convert("RGBA")).astype(int)
    ys, xs = np.where(a[:, :, 3] > 8)
    if len(ys) == 0:
        return None
    return xs.min(), xs.max(), ys.min(), ys.max()


for name, latex, (bx0, bx1), (by0, by1), color in EQS:
    out = os.path.join(ASSETS, name + ".png")
    fs = 14.0
    best = None
    for _ in range(10):
        info = render(latex, out, fs, color)
        if info is None:
            fs = 12.0
            continue
        x0, x1, y0, y1 = ink_box(out)
        w = (x1 - x0 + 1) / (DPI / 72.0)
        h = (y1 - y0 + 1) / (DPI / 72.0)
        fits_w = w <= (bx1 - bx0) * 0.92
        fits_h = h <= (by1 - by0)
        if fits_w and fits_h:
            best = (fs, w, h, x0, x1, y0, y1, info)
            break
        ratio = min((bx1 - bx0) * 0.92 / w, (by1 - by0) / h)
        fs = round(fs * ratio, 1)
    if best is None:
        print(f"FAILED to size {name}")
        continue
    fs, w, h, ix0, ix1, iy0, iy1, info = best
    # trim the 8px renderer pad -> exact tight ink bbox
    im = Image.open(out)
    im2 = im.crop((ix0, iy0, ix1 + 1, iy1 + 1))
    im2.save(out)
    a = np.asarray(Image.open(out).convert("RGBA"))
    ys, xs = np.where(a[:, :, 3] > 8)
    ink_w, ink_h = int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)
    w_in, h_in = ink_w / DPI, ink_h / DPI
    # centre the ink in its box region (frame px == pt)
    fcx = (bx0 + bx1) / 2.0
    fcy = (by0 + by1) / 2.0
    fr_x = round(fcx - (ink_w / (DPI / 72.0)) / 2.0, 2)
    fr_y = round(fcy - (ink_h / (DPI / 72.0)) / 2.0, 2)
    side = {
        "path": out,
        "w_px": ink_w,
        "h_px": ink_h,
        "w_in": round(w_in, 5),
        "h_in": round(h_in, 5),
        "ink_w_frame_px": round(ink_w / (DPI / 72.0), 2),
        "ink_h_frame_px": round(ink_h / (DPI / 72.0), 2),
        "frame_x": fr_x,
        "frame_y": fr_y,
        "dpi": DPI,
        "fontsize_pt": fs,
        "color": color,
        "fontset": "dejavusans",
        "mathtext": latex,
        "renderer": "scripts/render_eq.py (CERTIFIED), slide_004 2D rebuild 2026-10-23",
        "notes": "tight ink bbox (pad trimmed). Place with w=w_in h=h_in at "
                 "x=frame_x/72 in, y=frame_y/72 in -- ink centred in its box.",
    }
    with open(os.path.join(ASSETS, name + ".json"), "w") as f:
        json.dump(side, f, indent=1)
    print(f"{name}: fs={fs}pt ink={ink_w}x{ink_h}px = {side['ink_w_frame_px']}x"
          f"{side['ink_h_frame_px']} frame-px  -> place at frame ({fr_x},{fr_y})")
