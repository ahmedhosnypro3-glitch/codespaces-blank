#!/usr/bin/env python3
"""Rebuild-wave-3 math assets for slide 006 (fresh, spec-driven).

Inline strings go through render_math.py (matplotlib mathtext, 600 dpi,
tight transparent PNG). Stacked matrices/vectors use a custom bracketed
grid renderer (mathtext has no \\begin{bmatrix}). All outputs land in
eq_006/ with an rb3_ prefix so prior banked assets are untouched.
"""
import json
import os
import subprocess
import sys

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
BLACK, BLUE, GREEN, RED = "#000000", "#0000FF", "#008000", "#FF0000"


def render_math(name, rows, size, maxw, maxh):
    out = os.path.join(OUT, f"rb3_{name}.png")
    jout = os.path.join(OUT, f"rb3_{name}.json")
    cmd = [sys.executable, os.path.join(HERE, "render_math.py"),
           "--out", out, "--size", str(size), "--maxw", str(maxw),
           "--maxh", str(maxh), "--out-json", jout]
    for r in rows:
        cmd += ["--row", r]
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    info = json.load(open(jout))
    print(name, info["w_in"], "x", info["h_in"], "in")


def render_grid(name, rows, color, fs=9, col_w=0.40, row_h=0.14):
    nr, nc = len(rows), len(rows[0])
    fw, fh = col_w * nc + 0.55, row_h * nr + 0.30
    fig = plt.figure(figsize=(fw, fh), dpi=DPI)
    fig.patch.set_alpha(0.0)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, fw)
    ax.set_ylim(0, fh)
    ax.axis("off")
    for r, row in enumerate(rows):
        for c, val in enumerate(row):
            ax.text(0.22 + c * col_w + col_w / 2, (nr - 1 - r) * row_h + row_h / 2,
                    f"${val}$", fontsize=fs, color=color, ha="center", va="center")
    x_l, x_r = 0.10, 0.22 + (nc - 1) * col_w + col_w + 0.03
    y_b, y_t = 0.05, row_h * nr + 0.03
    tick = 0.12
    for x, sgn in ((x_l, 1), (x_r, -1)):
        ax.plot([x, x], [y_b, y_t], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_b, y_b], color=color, linewidth=1.6)
        ax.plot([x, x + sgn * tick], [y_t, y_t], color=color, linewidth=1.6)
    fig.canvas.draw()
    buf = np.asarray(fig.canvas.buffer_rgba())
    ink = buf[:, :, 3] > 8
    rr = np.where(ink.any(axis=1))[0]
    cc = np.where(ink.any(axis=0))[0]
    y0, y1 = max(rr[0] - 6, 0), min(rr[-1] + 7, buf.shape[0])
    x0, x1 = max(cc[0] - 6, 0), min(cc[-1] + 7, buf.shape[1])
    out = os.path.join(OUT, f"rb3_{name}.png")
    Image.fromarray(buf[y0:y1, x0:x1]).save(out)
    info = {"path": out, "w_px": int(x1 - x0), "h_px": int(y1 - y0),
            "w_in": round((x1 - x0) / DPI, 5), "h_in": round((y1 - y0) / DPI, 5)}
    with open(os.path.join(OUT, f"rb3_{name}.json"), "w") as fh:
        json.dump(info, fh, indent=2)
    plt.close(fig)
    print(name, info["w_in"], "x", info["h_in"], "in")


def main():
    os.makedirs(OUT, exist_ok=True)
    le = "||".join(["0000FF:x_{1}", "000000:\\leq", "0000FF:z_{1}", "000000: , ",
                   "0000FF:x_{2}", "000000:\\leq", "0000FF:z_{2}", "000000: , ",
                   "0000FF:x_{3}", "000000:\\leq", "0000FF:z_{3}"])
    ge = le.replace("\\leq", "\\geq")
    chain = "||".join(["0000FF:y_{1}", "000000:\\leq", "0000FF:x_{1}", "000000:\\leq",
                       "0000FF:z_{1}", "000000: , ",
                       "0000FF:y_{2}", "000000:\\leq", "0000FF:x_{2}", "000000:\\leq",
                       "0000FF:z_{2}", "000000: , ",
                       "0000FF:y_{3}", "000000:\\leq", "0000FF:x_{3}", "000000:\\leq",
                       "0000FF:z_{3}"])
    conv1 = "||".join(["008000:x_{1}", "008000:\\geq", "008000:z_{1}", "008000: , ",
                       "008000:x_{2}", "008000:\\geq", "008000:z_{2}", "008000: , ",
                       "008000:x_{3}", "008000:\\geq", "008000:z_{3}"])
    conv2 = "||".join(["008000:-x_{1}", "008000:\\leq", "008000:-z_{1}", "008000: , ",
                       "008000:-x_{2}", "008000:\\leq", "008000:-z_{2}", "008000: , ",
                       "008000:-x_{3}", "008000:\\leq", "008000:-z_{3}"])
    render_math("le_str", [le], 16, 3.6, 0.30)
    render_math("ge_str", [ge], 16, 3.6, 0.30)
    render_math("chain_str", [chain], 16, 3.6, 0.30)
    render_math("conv1", [conv1], 12, 2.5, 0.24)
    render_math("conv2", [conv2], 12, 2.5, 0.24)
    render_math("gxleh", ["FF0000:G\\,x \\leq h"], 16, 1.45, 0.24)
    render_math("arrow", ["FF0000:\\Rightarrow"], 18, 0.35, 0.30)
    render_math("leq", ["000000:\\leq"], 16, 0.22, 0.22)
    render_grid("m3id", [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]], BLACK)
    render_grid("m3neg", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"]], BLACK)
    render_grid("m6", [["-1", "0", "0"], ["0", "-1", "0"], ["0", "0", "-1"],
                       ["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"]], BLACK,
                row_h=0.15)
    render_grid("vx3", [["x_{1}"], ["x_{2}"], ["x_{3}"]], BLUE, col_w=0.5)
    render_grid("vz3", [["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, col_w=0.5)
    render_grid("vnegz3", [["-z_{1}"], ["-z_{2}"], ["-z_{3}"]], BLUE, col_w=0.58)
    render_grid("vyz6", [["-y_{1}"], ["-y_{2}"], ["-y_{3}"],
                         ["z_{1}"], ["z_{2}"], ["z_{3}"]], BLUE, col_w=0.58,
                row_h=0.15)


if __name__ == "__main__":
    main()
