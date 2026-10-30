#!/usr/bin/env python3
"""Render the training/test column vectors for slide 038 as 2D mathtext PNGs.
Q[i][j] = 1/2 * y_i y_j (x_i . x_j + 1)^2 with x1=(1,1) x2=(2,2) x3=(7,4) x4=(8,4),
y=(1,1,-1,-1) reproduces all 16 coefficients of the validated Q matrix.
"""
import json, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_038")
RED = "#CC0000"

VEC = {
    "vec_x1": r"x_1 = \binom{1}{1}",
    "vec_x2": r"x_2 = \binom{2}{2}",
    "vec_x3": r"x_3 = \binom{7}{4}",
    "vec_x4": r"x_4 = \binom{8}{4}",
    "vec_T1": r"T_1 = \binom{2}{3}",
    "vec_T2": r"T_2 = \binom{4}{5}",
    "vec_T3": r"T_3 = \binom{6}{2}",
}


def render(name, latex, color=RED, fs=15):
    fig = plt.figure(figsize=(3, 1.6), dpi=DPI)
    fig.patch.set_alpha(0.0)
    fig.text(0.5, 0.5, f"${latex}$", fontsize=fs, color=color, ha="center", va="center")
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rows = np.where(ink.any(axis=1))[0]
    cols = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rows[0] - 6, 0), min(rows[-1] + 6, buf.shape[0])
    x0, x1 = max(cols[0] - 6, 0), min(cols[-1] + 6, buf.shape[1])
    out = f"{OUT}/{name}.png"
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    print(json.dumps({"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
                      "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n, l in VEC.items():
        render(n, l)
