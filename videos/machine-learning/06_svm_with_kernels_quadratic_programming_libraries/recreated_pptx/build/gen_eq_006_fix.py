#!/usr/bin/env python3
"""Slide 006 fix-pass math assets: matrices/vectors with tall round-parenthesis
arcs (pattern from gen_p_matrix_012.py) instead of square brackets.
Outputs land in eq_006/ with an fx_ prefix; prior banked assets untouched.
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

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "eq_006")
DPI = 600
BLACK, BLUE = "#000000", "#0000FF"


def render_grid_paren(name, rows, color, fs, col_w, row_h):
    nr, nc = len(rows), len(rows[0])
    fw = 0.30 + col_w * nc + 0.25
    fh = row_h * nr + 0.28
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, fw)
    ax.set_ylim(0, fh)
    ax.axis("off")
    x0 = 0.30
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ax.text(x0 + c * col_w + col_w / 2, (nr - 1 - r) * row_h + row_h / 2 + 0.02,
                    f"${val}$", fontsize=fs, color=color, ha="center", va="center")
    y_b, y_t = 0.04, row_h * nr + 0.10
    y_m = (y_b + y_t) / 2
    for x, flip in ((x0 - 0.10, 1), (x0 + (nc - 1) * col_w + col_w, -1)):
        th = np.linspace(-0.32 * np.pi, 0.32 * np.pi, 60)
        rr = (y_t - y_b) / 2
        ax.plot(x + flip * 0.08 * np.cos(th), y_m + rr * np.sin(th),
                color=color, linewidth=1.8)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rr = np.where(ink.any(axis=1))[0]
    cc = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rr[0] - 8, 0), min(rr[-1] + 8, buf.shape[0])
    x0c, x1c = max(cc[0] - 8, 0), min(cc[-1] + 8, buf.shape[1])
    out = os.path.join(OUT, f"fx_{name}.png")
    Image.fromarray(buf[y0:y1, x0c:x1c]).save(out)
    info = {"path": out, "w_px": int(x1c - x0c), "h_px": int(y1 - y0),
            "w_in": round((x1c - x0c) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}
    with open(os.path.join(OUT, f"fx_{name}.json"), "w") as fh:
        json.dump(info, fh, indent=2)
    plt.close(fig)
    print(name, info["w_in"], "x", info["h_in"], "in")


def main():
    os.makedirs(OUT, exist_ok=True)
    render_grid_paren("m3id", [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]],
                      BLACK, 12, 0.40, 0.16)
    render_grid_paren("m3neg", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"]],
                      BLACK, 12, 0.40, 0.16)
    render_grid_paren("m6", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"],
                             ["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"]],
                      BLACK, 11, 0.38, 0.155)
    render_grid_paren("vx3", [["x_{1}"], ["x_{2}"], ["x_{3}"]], BLUE, 13, 0.50, 0.17)
    render_grid_paren("vz3", [["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, 13, 0.50, 0.17)
    render_grid_paren("vnegz3", [["-z_{1}"], ["-z_{2}"], ["-z_{3}"]], BLUE, 13, 0.62, 0.17)
    render_grid_paren("vyz6", [["-y_{1}"], ["-y_{2}"], ["-y_{3}"],
                               ["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, 12, 0.62, 0.155)


if __name__ == "__main__":
    main()
