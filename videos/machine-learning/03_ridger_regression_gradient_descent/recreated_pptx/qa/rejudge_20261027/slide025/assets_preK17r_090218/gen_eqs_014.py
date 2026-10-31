#!/usr/bin/env python3
"""Render slide 014's equations as 600dpi transparent mathtext PNGs (founder 2D
format) + eq_*.json sidecars. Colors/notation per the zoomed crop verdict:
matrix notation is RED C00000, column vectors use TALL PARENTHESES with stacked
entries and an N x 1 subscript.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

OUT = ("/workspaces/codespaces-blank/ai_llm_slides/videos/machine-learning/"
       "03_ridger_regression_gradient_descent/recreated_pptx/build/assets/")
os.makedirs(OUT, exist_ok=True)
DPI = 600
PAD = 8
RED = "C00000"

EQS = {
    "eq_014_a_Y":   r"\begin{pmatrix} y_{1} \\ y_{2} \\ \vdots \\ y_{n} \end{pmatrix}_{N \times 1}",
    "eq_014_a_Yh":  r"\begin{pmatrix} \hat{y}_{1} \\ \hat{y}_{2} \\ \vdots \\ \hat{y}_{n} \end{pmatrix}_{N \times 1}",
    "eq_014_model": r"\hat{Y} = \underline{X} \underline{W}",
    "eq_014_loss":  r"\left\| Y - \hat{Y} \right\|^{2} = (Y - \hat{Y})^{\top} (Y - \hat{Y})",
    "eq_014_reg":   r"R = \left\| W \right\|^{2} = W^{\top} W",
    "eq_014_obj":   r"J (W) = \frac{1}{2} \left[ (Y - \hat{Y})^{\top} (Y - \hat{Y}) + \lambda W^{\top} W \right]",
    "eq_014_J":     r"J (W) = Loss (X, Y, W) + \lambda R (W)",
}


def render(latex, out, fontsize, color):
    fig = plt.figure(figsize=(10, 4), dpi=DPI)
    fig.patch.set_alpha(0.0)
    eq = fig.text(0.5, 0.5, "$" + latex + "$", fontsize=fontsize, color=color,
                  ha="center", va="baseline")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    if len(rows) == 0:
        raise SystemExit(f"no ink for {latex!r} (mathtext parse error?)")
    y0, y1 = max(rows[0] - PAD, 0), min(rows[-1] + PAD, buf.shape[0])
    x0, x1 = max(cols[0] - PAD, 0), min(cols[-1] + PAD, buf.shape[1])
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round(float(x1 - x0) / DPI, 5),
            "h_in": round(float(y1 - y0) / DPI, 5),
            "dpi": DPI, "fontsize_pt": fontsize, "color": color,
            "mathtext": latex}
    plt.close(fig)
    return info


results = {}
for name, m in EQS.items():
    fs = 16
    p = OUT + name + ".png"
    results[name] = render(m, p, fs, "#" + RED)
    print(f"{name}: {results[name]['w_px']}x{results[name]['h_px']}px "
          f"= {results[name]['w_in']}x{results[name]['h_in']}in")

with open(OUT + "eq_index_014.json", "w") as f:
    json.dump(results, f, indent=1)
print("wrote " + OUT + "eq_index_014.json")
