#!/usr/bin/env python3
"""Slide 006 stacked matrices / column vectors with spanning square brackets.

True 2-D layout: each entry is a mathtext glyph, brackets drawn as lines
spanning all rows. Transparent tight PNGs at 600 dpi + JSON sidecars.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

matplotlib.rcParams["mathtext.fontset"] = "cm"
matplotlib.rcParams["mathtext.default"] = "it"

DPI = 600
OUT = ("/home/codespace/ai_llm_slides/videos/machine-learning/"
       "06_svm_with_kernels_quadratic_programming_libraries/recreated_pptx/build/eq_006")
BLACK, BLUE = "#000000", "#0000FF"


def render_grid(name, rows, color, fs=8, col_w=0.42, row_h=0.13):
    nr, nc = len(rows), len(rows[0])
    fig = plt.figure(figsize=(col_w * nc + 0.7, row_h * nr + 0.35), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, col_w * nc + 0.7)
    ax.set_ylim(0, row_h * nr + 0.35)
    ax.axis("off")
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ax.text(0.3 + c * col_w + col_w / 2, (nr - 1 - r) * row_h + row_h / 2,
                    f"${val}$", fontsize=fs, color=color, ha="center", va="center")
    x_l, x_r = 0.12, 0.3 + (nc - 1) * col_w + col_w + 0.02
    y_b, y_t = 0.06, row_h * nr + 0.04
    tick = 0.14
    for x, sgn in ((x_l, 1), (x_r, -1)):
        ax.plot([x, x], [y_b, y_t], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_b, y_b], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_t, y_t], color=color, linewidth=1.6)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rr = np.where(ink.any(axis=1))[0]
    cc = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rr[0] - 8, 0), min(rr[-1] + 9, buf.shape[0])
    x0, x1 = max(cc[0] - 8, 0), min(cc[-1] + 9, buf.shape[1])
    out = f"{OUT}/{name}.png"
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}
    with open(f"{OUT}/{name}.json", "w") as fh:
        json.dump(info, fh, indent=2)
    print(json.dumps(info))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    render_grid("m3_id", [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]], BLACK)
    render_grid("m3_neg", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"]], BLACK)
    render_grid("m6", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"],
                       ["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"]], BLACK,
                row_h=0.15)
    render_grid("vx3", [["x_{1}"], ["x_{2}"], ["x_{3}"]], BLUE, col_w=0.55)
    render_grid("vz3", [["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, col_w=0.55)
    render_grid("vnegz3", [["-z_{1}"], ["-z_{2}"], ["-z_{3}"]], BLUE, col_w=0.62)
    render_grid("vyz6", [["-y_{1}"], ["-y_{2}"], ["-y_{3}"],
                         ["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, col_w=0.62, row_h=0.15)
